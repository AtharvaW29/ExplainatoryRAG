from __future__ import annotations

import asyncio
from collections import defaultdict
from contextlib import suppress
from dataclasses import dataclass, field
from typing import TypeAlias
from uuid import UUID, uuid4

from fastapi import WebSocket
from pydantic import BaseModel
from starlette.websockets import WebSocketDisconnect

UserId: TypeAlias = str | UUID


@dataclass(slots=True)
class ManagedConnection:
    connection_id: UUID
    user_id: UserId
    ip_address: str
    webSocket: WebSocket  # noqa: N815
    outgoing: asyncio.Queue[BaseModel]
    writer_task: asyncio.Task[None] | None = None
    closed: asyncio.Event = field(default_factory=asyncio.Event)


class WebSocketManager:
    def __init__(self, queue_size) -> None:
        self.connections: dict[UUID, ManagedConnection] = {}
        self.queue_size = queue_size
        self.connected_users: dict[UserId, set[UUID]] = defaultdict(
            set
        )  # ignore
        self.lock = asyncio.Lock()

    async def connect(
        self,
        websocket: WebSocket,
        user_id: UserId,
        *,
        subprotocol: str | None = "llm-chat.v1",
    ) -> ManagedConnection:
        offered_protocols: list[str] = websocket.scope.get(
            "subprotocols",
            [],
        )

        selected_protocol = (
            subprotocol
            if subprotocol and subprotocol in offered_protocols
            else None
        )

        await websocket.accept(subprotocol=selected_protocol)

        connection = ManagedConnection(
            connection_id=uuid4(),
            user_id=user_id,
            ip_address="1:",
            webSocket=websocket,
            outgoing=asyncio.Queue(maxsize=self.queue_size),
        )

        async with self.lock:
            self.connections[connection.connection_id] = connection
            self.connected_users[user_id].add(connection.connection_id)

        connection.writer_task = asyncio.create_task(
            self._writer_loop(connection),
            name=f"websocket-writer-{connection.connection_id}",
        )

        return connection

    async def disconnect(
        self,
        connection_id: UUID,
        *,
        code: int = 1000,
        reason: str = "Connection Closed",
    ) -> None:
        connection = await self._remove_connection(connection_id)

        if connection is None:
            return
        writer_task = connection.writer_task
        if (
            writer_task is not None
            and writer_task is not asyncio.current_task()
        ):
            writer_task.cancel()

            with suppress(asyncio.CancelledError):
                await writer_task

        with suppress(
            RuntimeError,
            WebSocketDisconnect,
        ):
            await connection.webSocket.close(
                code=code,
                reason=reason,
            )
        connection.closed.set()

    async def send(self, connection_id: UUID, event: BaseModel) -> bool:
        connection = await self.get_connection(connection_id)
        if connection is None or connection.closed.is_set():
            return False
        try:
            connection.outgoing.put_nowait(event)
            return True
        except asyncio.QueueFull:
            await self.disconnect(
                connection_id, code=1013, reason="Processing Queue Full"
            )
            return False

    async def send_to_user(self, user_id: UserId, event: BaseModel) -> int:
        connection_ids = await self.get_user_connection_ids(user_id)
        if not connection_ids:
            return 0
        results = await asyncio.gather(
            *(
                self.send(connection_id, event)
                for connection_id in connection_ids
            )
        )
        return sum(results)

    async def broadcast(self, event: BaseModel) -> int:
        async with self.lock:
            connection_ids = tuple(self.connections)

        if not connection_ids:
            return 0

        results = await asyncio.gather(
            *(
                self.send(connection_id, event)
                for connection_id in connection_ids
            )
        )

        return sum(results)

    async def get_connection(
        self, connection_id: UUID
    ) -> ManagedConnection | None:
        async with self.lock:
            return self.connections.get(connection_id)

    async def get_user_connection_ids(
        self, user_id: UserId
    ) -> tuple[UUID, ...]:
        async with self.lock:
            return tuple(self.connected_users.get(user_id, set()))

    async def is_connected(self, connection_id: UUID) -> bool:
        async with self.lock:
            return connection_id in self.connections

    async def connection_count(self) -> int:
        async with self.lock:
            return len(self.connections)

    async def shutdown(self) -> None:
        async with self.lock:
            connectionids = tuple(self.connections)

        await asyncio.gather(
            *(
                self.disconnect(
                    connection_id, code=1001, reason="server shutting down"
                )
                for connection_id in connectionids
            ),
            return_exceptions=True,
        )

    async def _writer_loop(self, connection: ManagedConnection) -> None:
        try:
            while True:
                event = await connection.outgoing.get()

                try:
                    await connection.webSocket.send_text(
                        event.model_dump_json()
                    )
                finally:
                    connection.outgoing.task_done()

        except asyncio.CancelledError:
            raise
        except (WebSocketDisconnect, RuntimeError):
            pass
        finally:
            await self._remove_connection(connection.connection_id)
            connection.closed.set()

    async def _remove_connection(
        self,
        connection_id: UUID,
    ) -> ManagedConnection | None:
        async with self.lock:
            connection = self.connections.pop(connection_id, None)

        if connection is None:
            return None

        user_connections = self.connected_users.get(connection.user_id)

        if user_connections is not None:
            user_connections.discard(connection_id)

            if not user_connections:
                self.connected_users.pop(connection.user_id, None)

        return connection
