import uuid

from sqlalchemy import Column, ForeignKey, Text, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    source_id = Column(
        UUID(as_uuid=True), ForeignKey("knowledge_sources.id"), nullable=False
    )
    chunk_text = Column(Text)
    metadata_json = Column("metadata", JSONB)
