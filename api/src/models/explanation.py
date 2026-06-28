import uuid

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Explanation(Base):
    __tablename__ = "explanations"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    session_id = Column(
        UUID(as_uuid=True),
        ForeignKey("explanation_sessions.id"),
        nullable=False,
    )
    model_name = Column(String(100))
    prompt = Column(Text)
    generated_explanation = Column(Text)
    difficulty_score = Column(Float)
    explanation_style = Column(String(50))
    token_count = Column(Integer)
    created_at = Column(DateTime, server_default=text("NOW()"))
