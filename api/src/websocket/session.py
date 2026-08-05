import asyncio

from fastapi import WebSocket

from src.models.user import User
from src.schemas.websocket.common import ServerEventBase


class WebSocketSession:
    def __init__(self, websocket: WebSocket, user: User) -> None:
        self.websocket = websocket
        self.user = user
        self.outgoing: asyncio.Queue[ServerEventBase] = asyncio.Queue(
            maxsize=100
        )
        self._sequence_counter: int = 0

    def next_sequence(self) -> int:
        sequence = self._sequence_counter
        self._sequence_counter += 1
        return int(sequence)

    async def enqueue(self, event: ServerEventBase) -> None:
        await self.outgoing.put(event)

    async def writer_loop(self) -> None:
        while True:
            event = await self.outgoing.get()
            try:
                await self.websocket.send_text(event.model_dump_json())
            finally:
                self.outgoing.task_done()
