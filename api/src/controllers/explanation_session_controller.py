import asyncio
from collections import defaultdict
from typing import cast
from uuid import UUID, uuid4

from pydantic import ValidationError
from starlette.websockets import WebSocketDisconnect

from src.schemas.websocket.client_events import (
    ChatSendEvent,
    ClientEvent,
    GenerationCancelEvent,
    PingEvent,
    client_event_adapter,
)
from src.schemas.websocket.server_events import (
    ChatAcceptedEvent,
    ChatAcceptedPayload,
    ErrorEvent,
    ErrorPayload,
    GenerationCancelledEvent,
    GenerationCancelledPayload,
    GenerationCompletedEvent,
    GenerationCompletedPayload,
    GenerationDeltaEvent,
    GenerationDeltaPayload,
    GenerationStartedEvent,
    GenerationStartedPayload,
    PongEvent,
    PongPayload,
    ServerEventBase,
)
from src.services.mock_generation_service import (
    MockGenerationService,
)
from src.websocket.manager import ManagedConnection, WebSocketManager


class ExplanationSessionController:
    def __init__(
        self,
        connection: ManagedConnection,
        manager: WebSocketManager,
        generation_service: MockGenerationService,
    ) -> None:
        self.connection = connection
        self.manager = manager
        self.generation_service = generation_service

        self._generation_tasks: dict[UUID, asyncio.Task[None]] = {}

        self._assistant_message_ids: dict[UUID, UUID] = {}
        self._sequences: dict[UUID | None, int] = defaultdict(int)

    async def read_loop(self) -> None:
        while True:
            raw_message = await self.connection.webSocket.receive_text()

            try:
                event = client_event_adapter.validate_json(raw_message)
            except ValidationError as exc:
                await self._send_validation_error(exc)
                continue

            await self._dispatch(event)

    async def _dispatch(self, event: ClientEvent) -> None:
        match event:
            case PingEvent():
                await self._handle_ping(event)

            case ChatSendEvent():
                await self._handle_chat_send(event)

            case GenerationCancelEvent():
                await self._handle_generation_cancel(event)

    async def _handle_ping(
        self,
        event: PingEvent,
    ) -> None:
        await self._send(
            PongEvent(
                request_id=event.request_id,
                seq=self._next_sequence(event.request_id),
                payload=PongPayload(nonce=event.payload.nonce),
            )
        )

    async def _handle_chat_send(
        self,
        event: ChatSendEvent,
    ) -> None:
        if event.request_id in self._generation_tasks:
            await self._send(
                ErrorEvent(
                    request_id=event.request_id,
                    seq=self._next_sequence(event.request_id),
                    payload=ErrorPayload(
                        code="duplicate_request",
                        message=("This request_id is already active."),
                    ),
                )
            )
            return

        conversation_id = event.payload.conversation_id or uuid4()
        user_message_id = uuid4()
        assistant_message_id = uuid4()

        self._assistant_message_ids[event.request_id] = assistant_message_id

        # In production, persist the user message before this ACK.
        await self._send(
            ChatAcceptedEvent(
                conversation_id=conversation_id,
                request_id=event.request_id,
                seq=self._next_sequence(event.request_id),
                payload=ChatAcceptedPayload(user_message_id=user_message_id),
            )
        )

        task = asyncio.create_task(
            self._run_generation(
                request_id=event.request_id,
                conversation_id=conversation_id,
                assistant_message_id=assistant_message_id,
                prompt=event.payload.content,
            ),
            name=f"mock-generation-{event.request_id}",
        )

        self._generation_tasks[event.request_id] = task

        task.add_done_callback(
            lambda completed_task: self._generation_finished(
                event.request_id, completed_task
            )
        )

    async def _run_generation(
        self,
        *,
        request_id: UUID,
        conversation_id: UUID,
        assistant_message_id: UUID,
        prompt: str,
    ) -> None:
        try:
            await self._send(
                GenerationStartedEvent(
                    conversation_id=conversation_id,
                    request_id=request_id,
                    seq=self._next_sequence(request_id),
                    payload=GenerationStartedPayload(
                        assistant_message_id=(assistant_message_id),
                        provider="mock",
                        model="mock-stream-v1",
                    ),
                )
            )

            async for chunk in self.generation_service.stream(prompt):
                await self._send(
                    GenerationDeltaEvent(
                        conversation_id=conversation_id,
                        request_id=request_id,
                        seq=self._next_sequence(request_id),
                        payload=GenerationDeltaPayload(
                            assistant_message_id=(assistant_message_id),
                            text=chunk,
                        ),
                    )
                )

            await self._send(
                GenerationCompletedEvent(
                    conversation_id=conversation_id,
                    request_id=request_id,
                    seq=self._next_sequence(request_id),
                    payload=GenerationCompletedPayload(
                        assistant_message_id=(assistant_message_id),
                        finish_reason="stop",
                    ),
                )
            )

        except asyncio.CancelledError:
            await self._send(
                GenerationCancelledEvent(
                    conversation_id=conversation_id,
                    request_id=request_id,
                    seq=self._next_sequence(request_id),
                    payload=GenerationCancelledPayload(
                        assistant_message_id=(assistant_message_id),
                        reason="Cancelled by client",
                    ),
                )
            )
            raise

    async def _handle_generation_cancel(
        self,
        event: GenerationCancelEvent,
    ) -> None:
        generation_request_id = event.payload.generation_request_id

        task = self._generation_tasks.get(generation_request_id)

        if task is None or task.done():
            await self._send(
                ErrorEvent(
                    request_id=event.request_id,
                    seq=self._next_sequence(event.request_id),
                    payload=ErrorPayload(
                        code="generation_not_found",
                        message=(
                            "No active generation exists for "
                            "the supplied generation_request_id."
                        ),
                    ),
                )
            )
            return

        task.cancel()

    async def cancel_active_generations(self) -> None:
        tasks = tuple(self._generation_tasks.values())

        for task in tasks:
            if not task.done():
                task.cancel()

        if tasks:
            await asyncio.gather(
                *tasks,
                return_exceptions=True,
            )

    async def _send(
        self,
        event: ServerEventBase,
    ) -> None:
        sent = await self.manager.send(
            self.connection.connection_id,
            event,
        )

        if not sent:
            raise WebSocketDisconnect(code=1001)

    async def _send_validation_error(
        self,
        exc: ValidationError,
    ) -> None:
        details = [
            {
                "path": ".".join(str(part) for part in error["loc"]),
                "message": error["msg"],
                "type": error["type"],
            }
            for error in exc.errors(
                include_url=False,
                include_context=False,
                include_input=False,
            )
        ]

        await self._send(
            ErrorEvent(
                seq=self._next_sequence(None),
                payload=ErrorPayload(
                    code="invalid_event",
                    message="The WebSocket event is invalid.",
                    details=cast(list[dict[str, object]], details),
                ),
            )
        )

    def _next_sequence(
        self,
        request_id: UUID | None,
    ) -> int:
        sequence = self._sequences[request_id]
        self._sequences[request_id] += 1
        return sequence

    def _generation_finished(
        self,
        request_id: UUID,
        task: asyncio.Task[None],
    ) -> None:
        self._generation_tasks.pop(request_id, None)
        self._assistant_message_ids.pop(request_id, None)
        self._sequences.pop(request_id, None)

        # Retrieve exceptions so asyncio doesn't report
        # "Task exception was never retrieved."
        if not task.cancelled():
            try:
                task.exception()
            except Exception:
                pass
