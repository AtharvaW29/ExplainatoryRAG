from typing import cast
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.controllers.explanation_session_controller import (
    ExplanationSessionController,
)
from src.database import get_db
from src.dependencies.auth import get_current_user
from src.models.user import User
from src.schemas.explanation_sessions import (
    ExplanationSessionCreate,
    ExplanationSessionHistory,
    ExplanationSessionResponse,
)

router = APIRouter(
    prefix="/explanation_sessions", tags=["Explanation Sessions"]
)


@router.post(
    "",
    response_model=bool,
    status_code=status.HTTP_201_CREATED,
)
async def create_explanation_session(
    payload: ExplanationSessionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await ExplanationSessionController.create_explanation_session(
        db, payload, cast(UUID, current_user.id)
    )


@router.get("", response_model=ExplanationSessionHistory)
async def get_exp_sessions_for_user(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_id = cast(UUID, current_user.id)
    return await ExplanationSessionController.get_exp_sessions_for_user(
        db, user_id
    )


@router.get("/{exp_session_id}", response_model=ExplanationSessionResponse)
async def get_exp_sessions_by_id(
    exp_session_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ExplanationSessionResponse:
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Resource Access Not Allowed",
        )
    return await ExplanationSessionController.get_exp_session_by_id(
        db, exp_session_id
    )
