from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.explanation_session import (
    db_create_explanation_session,
    db_get_sessions_for_user,
)
from src.schemas.explanation_sessions import (
    ExplanationSessionCreate,
    ExplanationSessionResponse,
)


class ExplanationSessionController:
    @staticmethod
    async def create_explanation_session(
        db: AsyncSession, payload: ExplanationSessionCreate, user_id: UUID
    ) -> ExplanationSessionResponse:
        payload.user_id = user_id

        session = await db_create_explanation_session(db, payload)

        if not session:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not create explanation session. Verify input structure.",
            )
        return ExplanationSessionResponse.model_validate(session)

    @staticmethod
    async def list_sessions(
        db: AsyncSession, user_id: UUID
    ) -> list[ExplanationSessionResponse]:
        sessions = await db_get_sessions_for_user(db, user_id)
        return [ExplanationSessionResponse.model_validate(s) for s in sessions]
