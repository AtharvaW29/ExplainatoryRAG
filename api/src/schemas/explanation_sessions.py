from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.schemas.explanation import ExplanationCreate, ExplanationResponse


class ExplanationSessionCreate(BaseModel):
    user_id: UUID
    session_id: UUID
    topic: str = Field(..., max_length=255)

    explanations: list[ExplanationCreate]


class ExplanationSessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    topic: str

    created_at: datetime

    explanations: list[ExplanationResponse]


class ExplanationSessionHistoryItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    topic: str

    session_id: UUID

    created_at: datetime


class ExplanationSessionHistory(BaseModel):
    sessions: list[ExplanationSessionHistoryItem]


class ExplanationSessionPatch(BaseModel):
    id: UUID
    topic: Optional[str] = None
    explanation_id: Optional[list[UUID]] = None
    updated_at: Optional[datetime] = None
