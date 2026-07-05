from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class RetrievalMetadataSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    source_count: int
    retrieved_chunks: int
    average_similarity: Optional[float] = None


class ExplanationCreate(BaseModel):
    prompt: Optional[str] = None

    generated_explanation: Optional[str] = None
    difficulty_score: Optional[float] = None

    explanation_style: Optional[str] = Field(None, max_length=50)
    token_count: Optional[int] = Field(None, ge=0)

    llm_provider: str
    llm_model: Optional[str] = None

    generation_time_ms: Optional[float] = None
    retrieval: Optional[RetrievalMetadataSchema] = None


class ExplanationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    exp_session_id: UUID

    prompt: Optional[str]

    generated_explanation: Optional[str]
    difficulty_score: Optional[float]

    explanation_style: Optional[str]
    token_count: Optional[int]

    llm_provider: str

    llm_model: Optional[str] = None

    generation_time_ms: Optional[int]
    retrieval: Optional[RetrievalMetadataSchema] = None

    created_at: datetime


class ExplanationPatch(BaseModel):
    prompt: Optional[str]

    generated_explanation: Optional[str]
    difficulty_score: Optional[float] = None

    token_count: Optional[int] = None
    generation_time_ms: Optional[float] = None

    updated_at: datetime
