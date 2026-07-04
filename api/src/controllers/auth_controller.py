from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from src.models.user import db_create_user, db_get_user_by_email
from src.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from src.schemas.user import UserSchema


class AuthController:
    @staticmethod
    async def register(
        db: AsyncSession, payload: RegisterRequest
    ) -> UserSchema:
        existing = await db_get_user_by_email(db, payload.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        hashed_password = hash_password(payload.password)
        user = await db_create_user(
            db, payload.name, payload.email, hashed_password
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user",
            )
        return UserSchema.model_validate(user)

    @staticmethod
    async def login(db: AsyncSession, payload: LoginRequest) -> TokenResponse:
        user = await db_get_user_by_email(db, payload.email)
        if not user or not verify_password(
            payload.password, str(user.password_hash)
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = create_access_token(subject=str(user.id))
        return TokenResponse(access_token=token)
