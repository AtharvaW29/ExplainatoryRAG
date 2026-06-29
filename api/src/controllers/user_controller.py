from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.sqltypes import UUID

from src.models.user import db_create_user, db_get_user_by_email, db_patch_user
from src.schemas.user import UserCreateSchema, UserPatchSchema, UserSchema


class UserController:
    @staticmethod
    async def create_new_user(db: AsyncSession, payload: dict) -> UserSchema:
        validated_input = UserCreateSchema(**payload)
        db_user_obj = await db_create_user(db, validated_input)
        return UserSchema.model_validate(db_user_obj)

    @staticmethod
    async def fetch_user(
        db: AsyncSession, user_email: str
    ) -> UserSchema | None:
        db_user_obj = await db_get_user_by_email(db, user_email)
        if not db_user_obj:
            return None
        return UserSchema.model_validate(db_user_obj)

    @staticmethod
    async def patch_user(
        db: AsyncSession, user_id: UUID, payload: UserPatchSchema
    ) -> UserSchema | None:
        db_user_obj = await db_patch_user(db, user_id, payload)

        if not db_user_obj:
            raise HTTPException(status_code=404, detail="User not found")
        return UserSchema.model_validate(db_user_obj)
