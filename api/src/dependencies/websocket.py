from fastapi import WebSocket

from src.websocket.manager import WebSocketManager


def get_websocket_manager(
    websocket: WebSocket,
) -> WebSocketManager:
    return websocket.app.state.websocket_manager
