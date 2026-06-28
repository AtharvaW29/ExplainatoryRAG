from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ExplanationSessionCreate(BaseModel):
    user_id: UUID
    topic: str = Field(..., max_length=255)


class ExplanationSessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    topic: str
    created_at: datetime
