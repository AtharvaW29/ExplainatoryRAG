import uuid

from sqlalchemy import Column, DateTime, String, Text, text
from sqlalchemy.dialects.postgresql import UUID

from src.database import Base


class KnowledgeSource(Base):
    __tablename__ = "knowledge_sources"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    source_name = Column(Text)
    source_type = Column(String(50))
    uploaded_at = Column(DateTime, server_default=text("NOW()"))
