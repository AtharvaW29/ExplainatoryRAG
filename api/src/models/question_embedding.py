from pgvector.sqlalchemy import Vector  # type: ignore
from sqlalchemy import Column, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class QuestionEmbedding(Base):
    __tablename__ = "question_embeddings"

    session_id = Column(
        UUID(as_uuid=True),
        ForeignKey("explanation_sessions.id", ondelete="CASCADE"),
        primary_key=True,
    )

    embedding = Column(Vector(1536), nullable=False)

    __table_args__ = Index(
        "idx_question_embedding",
        embedding,
        postgresql_using="ivfflat",
        postgresql_ops={"embedding": "vector_cosine_ops"},
    )
