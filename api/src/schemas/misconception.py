from uuid import UUID

from pydantic import BaseModel


class MisconceptionCreate(BaseModel):
    name: str
    user_id: UUID
    title: str
    explanation: str
    concept_ids: list[UUID]
    frequency: float | None = None


class MisconceptionPatch(BaseModel):
    name: str | None = None
    title: str | None = None
    explanation: str | None = None
    frequency: float | None = None
    concept_ids: list[UUID] | None = None


class MisconceptionResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    explanation: str
    concept_ids: list[UUID]
    frequency: float | None = None
    created_at: str
