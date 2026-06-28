from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class EvaluationCreate(BaseModel):
    explanation_id: UUID
    metric_name: str = Field(..., max_length=100)
    score: Optional[float] = None
    metadata_json: Optional[Dict[str, Any]] = Field(
        default=None, alias="metadata"
    )

    model_config = ConfigDict(populate_by_name=True)


class EvaluationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: UUID
    explanation_id: UUID
    metric_name: str
    score: Optional[float]
    metadata_json: Optional[Dict[str, Any]] = Field(..., alias="metadata")
    created_at: datetime
