from typing import List
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ExplainationEmbeddingCreate(BaseModel):
    session_id: UUID
    embedding: List[float] = Field(..., min_length=1536, max_length=1536)


class ExplainationEmbeddingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    session_id: UUID
    embedding: List[float]
