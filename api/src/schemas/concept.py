from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ConceptSchema(BaseModel):
    id: UUID
    user_id: UUID
    description: str

    model_config = ConfigDict(from_attributes=True)
