import uuid
from uuid import UUID

from sqlalchemy import Column, DateTime, ForeignKey, String, select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base
from src.models.explanation import db_create_explanation, db_get_explanation
from src.schemas.explanation_sessions import (
    ExplanationSessionCreate,
    ExplanationSessionHistory,
    ExplanationSessionHistoryItem,
    ExplanationSessionResponse,
)


class ExplanationSession(Base):
    __tablename__ = "explanation_sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    topic: Mapped[str] = mapped_column(String(255), nullable=False)

    created_at = Column(
        DateTime(timezone=True), server_default=text("NOW()"), nullable=False
    )

    updated_at = Column(DateTime(timezone=True), nullable=True)


async def db_create_explanation_session(
    db: AsyncSession, payload: ExplanationSessionCreate
) -> bool:
    try:
        filtered_data = payload.model_dump(exclude={"explanations"})
        exp_session = ExplanationSession(**filtered_data)

        db.add(exp_session)
        await db.flush()

        for e in payload.explanations:
            res = await db_create_explanation(db, e, exp_session.id)
            if not res:
                await db.rollback()
                return False

        await db.commit()
        return True
    except Exception as e:
        await db.rollback()
        return False


async def db_get_exp_sessions_for_user(
    db: AsyncSession,
    user_id: UUID,
) -> ExplanationSessionHistory | None:

    statement = select(ExplanationSession).where(
        ExplanationSession.user_id == user_id
    )

    result = await db.execute(statement)
    sessions = result.scalars().all()

    if not sessions:
        return None

    return ExplanationSessionHistory(
        sessions=[
            ExplanationSessionHistoryItem.model_validate(session)
            for session in sessions
        ]
    )


async def db_get_exp_session_by_id(
    db: AsyncSession,
    exp_session_id: UUID,
) -> ExplanationSessionResponse | None:

    statement = select(ExplanationSession).where(
        ExplanationSession.id == exp_session_id
    )

    result = await db.execute(statement)
    exp_session = result.scalar_one_or_none()

    if exp_session is None:
        return None

    explanations = await db_get_explanation(
        db,
        exp_session.id,
    )

    return ExplanationSessionResponse.model_validate(
        {
            **exp_session.__dict__,
            "explanations": explanations,
        }
    )
