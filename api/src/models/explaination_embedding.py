from pgvector.sqlalchemy import Vector  # type: ignore
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from src.database import Base


class ExplainationEmbedding(Base):
    __tablename__ = "explaination_embeddings"

    session_id = Column(
        UUID(as_uuid=True),
        ForeignKey("explanations.id", ondelete="CASCADE"),
        primary_key=True,
    )

    embedding = Column(Vector(1536), nullable=False)
