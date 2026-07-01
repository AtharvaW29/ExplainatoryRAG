from uuid import UUID

from pydantic import BaseModel


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
    difficulty: str | None
    domain: str | None
