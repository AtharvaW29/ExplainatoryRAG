from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.sqltypes import UUID

from src.models.learner_profile import (
    db_create_learnerprofile,
    db_get_learnerprofile,
    db_patch_learnerprofile,
)
from src.schemas.learner_profile import (
    LearnerPreferencesResponse,
    LearnerProfileCreate,
    LearnerProfilePatch,
    LearnerProfileResponse,
)


class LearnerProfileController:
    @staticmethod
    async def create_profile(
        db: AsyncSession, payload: dict
    ) -> LearnerProfileResponse:

        validated = LearnerProfileCreate(**payload)

        profile = await db_create_learnerprofile(db, validated)

        return LearnerProfileResponse.model_validate(profile)

    @staticmethod
    async def fetch_profile(
        db: AsyncSession, user_id: UUID
    ) -> LearnerProfileResponse:

        profile = await db_get_learnerprofile(db, user_id)

        if not profile:
            raise HTTPException(404, "Profile not found")

        return LearnerProfileResponse.model_validate(profile)

    @staticmethod
    async def patch_profile(
        db: AsyncSession, user_id: UUID, payload: LearnerProfilePatch
    ) -> LearnerProfileResponse:

        profile = await db_patch_learnerprofile(db, user_id, payload)

        if not profile:
            raise HTTPException(404, "Profile not found")

        return LearnerProfileResponse.model_validate(profile)

    @staticmethod
    async def fetch_preferences(
        db: AsyncSession, user_id: UUID
    ) -> LearnerPreferencesResponse:

        profile = await db_get_learnerprofile(db, user_id)

        if not profile:
            raise HTTPException(404, "Profile not found")

        return LearnerPreferencesResponse.model_validate(profile)
