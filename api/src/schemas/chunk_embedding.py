from typing import List
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ChunkEmbeddingCreate(BaseModel):
    chunk_id: UUID
    embedding: List[float] = Field(..., min_length=1536, max_length=1536)


class ChunkEmbeddingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    chunk_id: UUID
    embedding: List[float]
