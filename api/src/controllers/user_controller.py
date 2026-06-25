from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import db_create_user, db_get_user_by_id
from src.schemas.user import UserCreateSchema, UserSchema


class UserController:
    @staticmethod
    async def create_new_user(db: AsyncSession, payload: dict) -> UserSchema:
        validated_input = UserCreateSchema(**payload)
        db_user_obj = await db_create_user(db, validated_input)
        return UserSchema.model_validate(db_user_obj)

    @staticmethod
    async def fetch_user(db: AsyncSession, user_id: int) -> UserSchema | None:
        db_user_obj = await db_get_user_by_id(db, user_id)
        if not db_user_obj:
            return None
        return UserSchema.model_validate(db_user_obj)
