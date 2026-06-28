import uuid

from sqlalchemy import Column, DateTime, Float, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    explanation_id = Column(
        UUID(as_uuid=True), ForeignKey("explanations.id"), nullable=False
    )
    metric_name = Column(String(100), nullable=False)
    score = Column(Float)
    metadata_json = Column("metadata", JSONB)
    created_at = Column(DateTime, server_default=text("NOW()"))
