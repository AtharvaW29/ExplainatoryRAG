from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class LearnerProfileCreate(BaseModel):
    user_id: UUID
    academic_level: Optional[str] = None
    learning_style: Optional[str] = None
    preferred_explanation_style: Optional[str] = None
    domain: Optional[str] = None


class LearnerProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    academic_level: Optional[str]
    learning_style: Optional[str]
    preferred_explanation_style: Optional[str]
    domain: Optional[str]
    created_at: datetime
    updated_at: datetime
