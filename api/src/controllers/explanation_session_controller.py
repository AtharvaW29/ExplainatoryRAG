from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.explanation_session import (
    db_create_session,
    db_get_sessions_for_user,
)
from src.schemas.explanation_sessions import ExplanationSessionResponse


class ExplanationSessionController:
    @staticmethod
    async def create_session(
        db: AsyncSession, user_id: UUID, topic: str
    ) -> ExplanationSessionResponse:
        session = await db_create_session(db, user_id, topic)
        return ExplanationSessionResponse.model_validate(session)

    @staticmethod
    async def list_sessions(
        db: AsyncSession, user_id: UUID
    ) -> list[ExplanationSessionResponse]:
        sessions = await db_get_sessions_for_user(db, user_id)
        return [ExplanationSessionResponse.model_validate(s) for s in sessions]
