from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class UserSchema(BaseModel):
    id: UUID
    name: str
    email: str
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)


class UserCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[UUID] = Field(default_factory=uuid4)
    name: str
    email: str


class UserPatchSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None
