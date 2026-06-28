from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ExplanationCreate(BaseModel):
    session_id: UUID
    model_name: Optional[str] = Field(None, max_length=100)
    prompt: Optional[str] = None
    generated_explanation: Optional[str] = None
    difficulty_score: Optional[float] = None
    explanation_style: Optional[str] = Field(None, max_length=50)
    token_count: Optional[int] = Field(None, ge=0)


class ExplanationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    session_id: UUID
    model_name: Optional[str]
    prompt: Optional[str]
    generated_explanation: Optional[str]
    difficulty_score: Optional[float]
    explanation_style: Optional[str]
    token_count: Optional[int]
    created_at: datetime
