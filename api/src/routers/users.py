from uuid import UUID  # type: ignore

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.controllers.user_controller import UserController
from src.database import get_db
from src.schemas.user import UserPatchSchema, UserSchema

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_email}", response_model=UserSchema)
async def get_user(user_email: str, db: AsyncSession = Depends(get_db)):
    user = await UserController.fetch_user(db, user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=UserPatchSchema)
async def patch_user(
    user_id: UUID, payload: UserPatchSchema, db: AsyncSession = Depends(get_db)
):
    return await UserController.patch_user(db, user_id, payload)
