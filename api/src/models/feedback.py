import uuid

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Text,
    select,
    text,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base
from src.schemas.feedback import (
    FeedbackCreate,
    FeedbackPatch,
    FeedbackResponse,
)


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
        nullable=False,
    )
    explanation_id = Column(
        PG_UUID(as_uuid=True), ForeignKey("explanations.id"), nullable=False
    )
    rating: Mapped[int] = mapped_column(Integer, nullable=True, default=0)
    clarity_score: Mapped[int] = mapped_column(
        Integer, nullable=True, default=0
    )
    usefulness_score: Mapped[int] = mapped_column(
        Integer, nullable=True, default=0
    )
    correctness_score: Mapped[int] = mapped_column(
        Integer, nullable=True, default=0
    )
    comments: Mapped[str] = mapped_column(Text, nullable=True, default=0)
    created_at = Column(DateTime, server_default=text("NOW()"), nullable=False)


async def db_create_feedback(
    db: AsyncSession, payload: FeedbackCreate
) -> bool:

    f = Feedback(**payload.model_dump())
    db.add(f)
    await db.commit()
    await db.refresh(f)
    return f.id is not None


async def db_get_feedback(
    db: AsyncSession, explanation_id: PG_UUID
) -> FeedbackResponse | None:

    statement = select(Feedback).where(
        Feedback.explanation_id == explanation_id
    )
    result = await db.execute(statement)
    if result is None:
        return
    return FeedbackResponse.model_validate(result.scalar_one_or_none())


async def db_patch_feedback(
    db: AsyncSession, explanation_id: PG_UUID, payload: FeedbackPatch
) -> bool:
    statement = select(Feedback).where(
        Feedback.explanation_id == explanation_id
    )
    result = await db.execute(statement)
    if result is None:
        return False
    feedback = result.scalar_one_or_none()

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(feedback, field, value)

    await db.commit()
    await db.refresh(feedback)
    return True
