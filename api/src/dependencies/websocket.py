from dataclasses import dataclass

from fastapi import WebSocket

from src.websocket.manager import WebSocketManager


@dataclass(frozen=True, slots=True)
class DevelopmentUser:
    id: str


def get_websocket_manager(
    websocket: WebSocket,
) -> WebSocketManager:
    return websocket.app.state.websocket_manager


def get_development_user() -> DevelopmentUser:
    return DevelopmentUser(id="test-dev-user")
