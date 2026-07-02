from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel

ConceptType = Literal[
    "concept",
    "misconception",
    "question",
    "resource",
    "prerequisite",
    "related",
    "prerequisite_of",
    "related_to",
    "misconception_of",
    "misconception_related_to",
]


class ConceptRelationshipCreate(BaseModel):
    target_concept_id: UUID


class ConceptRelationshipResponse(BaseModel):
    source_concept_id: UUID
    target_concept_id: UUID
    relationship: str


class ConceptRelationshipExists(BaseModel):
    source_concept_id: UUID
    target_concept_id: UUID
    relationship: str


class ConceptRelationshipRemove(BaseModel):
    target_concept_id: UUID
    relationship: str


class RelatedConceptResponse(BaseModel):
    id: UUID
    name: str
    description: str | None
    difficulty: float | None
    domain: str | None


class ConceptNodeCreate(BaseModel):
    id: UUID
    name: str
    concepttype: ConceptType = "concept"
    description: Optional[str] = None
    difficulty: Optional[float] = None
    domain: Optional[str] = None
