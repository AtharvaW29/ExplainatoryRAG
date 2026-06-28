from pgvector.sqlalchemy import Vector  # type: ignore
from sqlalchemy import Column, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class ChunkEmbedding(Base):
    __tablename__ = "chunk_embeddings"

    chunk_id = Column(
        UUID(as_uuid=True),
        ForeignKey("document_chunks.id", ondelete="CASCADE"),
        primary_key=True,
    )

    embedding = Column(Vector(1536), nullable=False)
    __table_args__ = (
        Index(
            "idx_chunk_embedding",
            embedding,
            postgresql_using="ivfflat",
            postgresql_ops={"embedding": "vector_cosine_ops"},
            # Optional: ivfflat recommends choosing lists based on your table size
            # postgresql_with={"lists": 100}
        ),
    )
