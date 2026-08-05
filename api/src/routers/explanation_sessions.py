from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    WebSocket,
    WebSocketDisconnect,
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.controllers.explanation_session_controller import (
    ExplanationSessionController,
)
from src.database import get_db
from src.dependencies.websocket import (
    DevelopmentUser,
    get_development_user,
    get_websocket_manager,
)
from src.services.mock_generation_service import MockGenerationService
from src.websocket.manager import WebSocketManager

router = APIRouter(
    prefix="/explanation_sessions", tags=["Explanation Sessions"]
)


@router.websocket("/start_exp_session")
async def exp_chat_socket(
    websocket: WebSocket,
    user: Annotated[DevelopmentUser, Depends(get_development_user)],
    manager: Annotated[WebSocketManager, Depends(get_websocket_manager)],
    db: AsyncSession = Depends(get_db),
) -> None:

    connection = await manager.connect(websocket, user_id=user.id)
    controller = ExplanationSessionController(
        connection, manager, MockGenerationService()
    )

    try:
        await controller.read_loop()
    except WebSocketDisconnect:
        pass
    finally:
        await controller.cancel_active_generations()
        await manager.disconnect(connection.connection_id)
