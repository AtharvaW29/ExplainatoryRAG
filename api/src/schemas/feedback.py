from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class FeedbackCreate(BaseModel):
    explanation_id: UUID
    rating: Optional[int] = Field(
        None, ge=1, le=5
    )  # Limits scores from 1 to 5
    clarity_score: Optional[int] = Field(None, ge=1, le=5)
    usefulness_score: Optional[int] = Field(None, ge=1, le=5)
    correctness_score: Optional[int] = Field(None, ge=1, le=5)
    comments: Optional[str] = None


class FeedbackResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    explanation_id: UUID
    rating: Optional[int]
    clarity_score: Optional[int]
    usefulness_score: Optional[int]
    correctness_score: Optional[int]
    comments: Optional[str]
    created_at: datetime
