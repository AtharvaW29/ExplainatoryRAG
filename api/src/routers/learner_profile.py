from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.controllers.learner_profile_controller import LearnerProfileController
from src.database import get_db
from src.schemas.learner_profile import (
    LearnerPreferencesResponse,
    LearnerProfileCreate,
    LearnerProfilePatch,
    LearnerProfileResponse,
)

router = APIRouter(prefix="/learner_profile", tags=["Learner Profile"])


@router.post(
    "",
    response_model=LearnerProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_learner_profile(
    payload: LearnerProfileCreate, db: AsyncSession = Depends(get_db)
):
    return await LearnerProfileController.create_profile(
        db, payload.model_dump()
    )


@router.get("/{user_id}", response_model=LearnerProfileResponse)
async def fetch_learner_profile(
    user_id: UUID, db: AsyncSession = Depends(get_db)
):
    profile = await LearnerProfileController.fetch_profile(db, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile Not Found")
    return profile


@router.patch("/{user_id}", response_model=LearnerProfileResponse)
async def patch_profile(
    user_id: UUID,
    payload: LearnerProfilePatch,
    db: AsyncSession = Depends(get_db),
):
    return await LearnerProfileController.patch_profile(db, user_id, payload)


@router.get(
    "/{user_id}/preferences", response_model=LearnerPreferencesResponse
)
async def fetch_profile_preferences(
    user_id: UUID, db: AsyncSession = Depends(get_db)
):
    pref = await LearnerProfileController.fetch_preferences(db, user_id)
    if not pref:
        raise HTTPException(status_code=404, detail="No Preferences Found")
    return pref
