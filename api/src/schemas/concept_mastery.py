from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ConceptMasteryCreate(BaseModel):
    """
    Used by POST /api/v1/mastery
    Creates a mastery record if one doesn't exist,
    otherwise updates the existing record.
    """

    user_id: UUID
    concept_id: UUID

    mastery_score: float = Field(
        ..., ge=0.0, le=1.0, description="Current estimated mastery (0-1)"
    )

    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Confidence of mastery estimate (0-1)"
    )


class ConceptMasteryPatch(BaseModel):
    """
    Internal update schema.
    Allows partial updates.
    """

    mastery_score: Optional[float] = Field(None, ge=0.0, le=1.0)

    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)


class ConceptMasteryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

    user_id: UUID
    concept_id: UUID

    mastery_score: float
    confidence: float

    last_interaction: datetime


class ConceptMasteryListResponse(BaseModel):
    """
    Returned by
    GET /api/v1/mastery
    """

    model_config = ConfigDict(from_attributes=True)

    concept_id: UUID

    mastery_score: float

    confidence: float

    last_interaction: datetime
