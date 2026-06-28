import uuid

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class ConceptMastery(Base):
    __tablename__ = "concept_mastery"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )

    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False
    )

    concept_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False
    )

    mastery_score = Column(Float, default=0.0, nullable=False)

    confidence = Column(Float)

    last_interaction = Column(
        DateTime, server_default=text("NOW()"), onupdate=text("NOW()")
    )

    __table_args__ = (
        UniqueConstraint("user_id", "concept_id", name="_user_concept_uc"),
    )
