from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.controllers.user_controller import UserController
from src.database import get_db
from src.schemas.user import UserCreateSchema, UserSchema

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/", response_model=UserSchema, status_code=status.HTTP_201_CREATED
)
async def create_user(
    payload: UserCreateSchema, db: AsyncSession = Depends(get_db)
):
    return await UserController.create_new_user(db, payload.model_dump())


@router.get("/{user_id}", response_model=UserSchema)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await UserController.fetch_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
