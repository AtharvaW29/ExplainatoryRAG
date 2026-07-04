import uuid
from uuid import UUID

from sqlalchemy import Column, DateTime, ForeignKey, String, select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class ExplanationSession(Base):
    __tablename__ = "explanation_sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    topic: Mapped[str] = mapped_column(String(255))
    created_at = Column(
        DateTime(timezone=True), server_default=text("NOW()"), nullable=False
    )


async def db_create_session(
    db: AsyncSession, user_id: UUID, topic: str
) -> ExplanationSession:
    new_session = ExplanationSession(user_id=user_id, topic=topic)
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    return new_session


async def db_get_sessions_for_user(
    db: AsyncSession, user_id: UUID
) -> list[ExplanationSession]:
    statement = select(ExplanationSession).where(
        ExplanationSession.user_id == user_id
    )
    res = await db.execute(statement)
    return list(res.scalars().all())
