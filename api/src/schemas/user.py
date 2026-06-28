from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    id: UUID
    name: str
    email: str
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)


class UserCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    email: str
