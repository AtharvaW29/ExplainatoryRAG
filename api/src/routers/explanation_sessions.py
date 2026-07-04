from typing import cast
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.controllers.explanation_session_controller import (
    ExplanationSessionController,
)
from src.database import get_db
from src.dependencies.auth import get_current_user
from src.models.user import User
from src.schemas.explanation_sessions import (
    ExplanationSessionCreate,
    ExplanationSessionResponse,
)

router = APIRouter(
    prefix="/explanation_sessions", tags=["Explanation Sessions"]
)


@router.post(
    "",
    response_model=ExplanationSessionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_explanation_session(
    payload: ExplanationSessionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_id = cast(UUID, current_user.id)
    return await ExplanationSessionController.create_session(
        db, user_id, payload.topic
    )


@router.get("", response_model=list[ExplanationSessionResponse])
async def list_my_explanation_sessions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_id = cast(UUID, current_user.id)
    return await ExplanationSessionController.list_sessions(db, user_id)
