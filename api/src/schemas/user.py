from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)


class UserCreateSchema(BaseModel):
    name: str
    email: str
