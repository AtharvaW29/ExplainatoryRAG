from typing import cast
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.controllers.feedback_controller import FeedbackController
from src.database import get_db
from src.dependencies.auth import get_current_user
from src.models.user import User
from src.schemas.feedback import (
    FeedbackCreate,
    FeedbackPatch,
    FeedbackResponse,
)

router = APIRouter(prefix="/feedback", tags=["Explanation feedback"])


@router.post("", response_model=bool, status_code=status.HTTP_201_CREATED)
async def createfeedback(
    payload: FeedbackCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> bool:
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Resource Access Not Allowed",
        )
    return await FeedbackController.create_feedback(db, payload)


@router.get(
    "/{explanation_id}",
    response_model=FeedbackResponse,
    status_code=status.HTTP_200_OK,
)
async def get_feedback(
    explanation_id: UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> FeedbackResponse | None:
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Resource Access Not Allowed",
        )
    return await FeedbackController.get_feedback(
        db, cast(PG_UUID, explanation_id)
    )


@router.patch(
    "/{explanation_id}",
    response_model=bool,
    status_code=status.HTTP_202_ACCEPTED,
)
async def patch_feedback(
    explanation_id: UUID,
    payload: FeedbackPatch,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> bool:
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Resource Access Not Allowed",
        )
    updated = await FeedbackController.patch_feedback(
        db, cast(PG_UUID, explanation_id), payload
    )
    return updated
