from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.explanation_session import (
    db_create_explanation_session,
    db_get_exp_session_by_id,
    db_get_exp_sessions_for_user,
)
from src.schemas.explanation_sessions import (
    ExplanationSessionCreate,
    ExplanationSessionHistory,
    ExplanationSessionResponse,
)


class ExplanationSessionController:
    @staticmethod
    async def create_explanation_session(
        db: AsyncSession, payload: ExplanationSessionCreate, user_id: UUID
    ) -> bool:
        payload.user_id = user_id

        session = await db_create_explanation_session(db, payload)

        if not session:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not create explanation session. Verify input structure.",
            )
        return session

    @staticmethod
    async def get_exp_sessions_for_user(
        db: AsyncSession, user_id: UUID
    ) -> ExplanationSessionHistory | None:
        sessions = await db_get_exp_sessions_for_user(db, user_id)
        if not sessions:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The Request Session could not be found",
            )
        return sessions

    @staticmethod
    async def get_exp_session_by_id(
        db: AsyncSession, exp_session_id: UUID
    ) -> ExplanationSessionResponse:
        exp_session = await db_get_exp_session_by_id(db, exp_session_id)

        if not exp_session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The Request Session could not be found",
            )
        return exp_session
