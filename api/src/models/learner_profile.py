import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class LearnerProfile(Base):
    __tablename__ = "learner_profiles"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )

    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False
    )

    academic_level = Column(String(50), nullable=True)
    learning_style = Column(String(50), nullable=True)
    preferred_explanation_style = Column(String(100), nullable=True)
    domain = Column(String(100), nullable=True)

    created_at = Column(DateTime, server_default=text("NOW()"), nullable=False)
    updated_at = Column(DateTime, onupdate=text("NOW()"), nullable=True)
