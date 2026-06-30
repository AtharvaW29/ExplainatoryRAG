from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ConceptCreate(BaseModel):
    name: str
    description: Optional[str] = None
    difficulty: Optional[str] = None
    domain: Optional[str] = None


class ConceptPatch(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    difficulty: Optional[str] = None
    domain: Optional[str] = None


class ConceptResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    description: Optional[str]
    difficulty: Optional[str]
    domain: Optional[str]
    isactive: bool
    created_at: datetime


class ConceptSummary(BaseModel):
    """
    Lightweight schema for dropdowns, search results,
    and mastery APIs.
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    difficulty: Optional[str]
