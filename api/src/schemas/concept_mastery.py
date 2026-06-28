from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ConceptMasteryCreate(BaseModel):
    user_id: UUID
    concept_id: UUID
    mastery_score: float = Field(..., ge=0.0, le=1.0)
    confidence: float = Field(..., ge=0.0, le=1.0)


class ConceptMasteryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    concept_id: UUID
    mastery_score: float
    confidence: float
    last_interaction: datetime
