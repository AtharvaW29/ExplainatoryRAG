from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class KnowledgeSourceCreate(BaseModel):
    source_name: Optional[str] = None
    source_type: Optional[str] = Field(None, max_length=50)


class KnowledgeSourceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    source_name: Optional[str]
    source_type: Optional[str]
    uploaded_at: datetime
