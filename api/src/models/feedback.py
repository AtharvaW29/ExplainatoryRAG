import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    explanation_id = Column(
        UUID(as_uuid=True), ForeignKey("explanations.id"), nullable=False
    )
    rating = Column(Integer)
    clarity_score = Column(Integer)
    usefulness_score = Column(Integer)
    correctness_score = Column(Integer)
    comments = Column(Text)
    created_at = Column(DateTime, server_default=text("NOW()"))
