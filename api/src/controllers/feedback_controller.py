from fastapi import HTTPException, status
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.feedback import (
    db_create_feedback,
    db_get_feedback,
    db_patch_feedback,
)
from src.schemas.feedback import (
    FeedbackCreate,
    FeedbackPatch,
    FeedbackResponse,
)


class FeedbackController:
    @staticmethod
    async def create_feedback(
        db: AsyncSession, payload: FeedbackCreate
    ) -> bool:
        return await db_create_feedback(db, payload)

    @staticmethod
    async def get_feedback(
        db: AsyncSession, explanation_id: PG_UUID
    ) -> FeedbackResponse | None:
        result = await db_get_feedback(db, explanation_id)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Requested Feedback not Found!",
            )
        return result

    @staticmethod
    async def patch_feedback(
        db: AsyncSession, explanation_id: PG_UUID, payload: FeedbackPatch
    ) -> bool:
        return await db_patch_feedback(db, explanation_id, payload)
