from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class LearnerProfileCreate(BaseModel):
    user_id: UUID

    academic_level: Optional[str] = None
    institution: Optional[str] = None
    major: Optional[str] = None

    learning_style: Optional[str] = None
    preferred_explanation_style: Optional[str] = None
    preferred_difficulty: Optional[str] = None

    domain: List[str] = []
    language: str = "English"


class LearnerProfilePatch(BaseModel):
    academic_level: Optional[str] = None
    institution: Optional[str] = None
    major: Optional[str] = None

    learning_style: Optional[str] = None
    preferred_explanation_style: Optional[str] = None
    preferred_difficulty: Optional[str] = None

    domain: Optional[List[str]] = None
    language: Optional[str] = None


class LearnerPreferencesResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    learning_style: Optional[str]
    preferred_explanation_style: Optional[str]
    preferred_difficulty: Optional[str]
    domain: List[str]
    language: str


class LearnerProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID

    academic_level: Optional[str]
    institution: Optional[str]
    major: Optional[str]

    learning_style: Optional[str]
    preferred_explanation_style: Optional[str]
    preferred_difficulty: Optional[str]

    domain: List[str]

    language: str

    created_at: datetime
    updated_at: Optional[datetime]
