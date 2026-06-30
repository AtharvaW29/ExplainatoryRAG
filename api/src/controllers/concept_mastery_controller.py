from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.concept_mastery import (
    db_get_all_mastery,
    db_get_mastery,
    db_upsert_mastery,
)
from src.schemas.concept_mastery import (
    ConceptMasteryCreate,
    ConceptMasteryResponse,
)


class ConceptMasteryController:
    @staticmethod
    async def create_or_update_mastery(
        db: AsyncSession,
        payload: dict,
    ) -> ConceptMasteryResponse:
        """
        Creates a new mastery record or updates an existing one.
        """

        validated_input = ConceptMasteryCreate(**payload)

        mastery = await db_upsert_mastery(
            db=db,
            mastery_data=validated_input,
        )

        return ConceptMasteryResponse.model_validate(mastery)

    @staticmethod
    async def fetch_mastery(
        db: AsyncSession,
        user_id: UUID,
        concept_id: UUID,
    ) -> ConceptMasteryResponse:
        """
        Fetch mastery for a specific concept.
        """

        mastery = await db_get_mastery(
            db=db,
            user_id=user_id,
            concept_id=concept_id,
        )

        if mastery is None:
            raise HTTPException(
                status_code=404,
                detail="Concept mastery not found.",
            )

        return ConceptMasteryResponse.model_validate(mastery)

    @staticmethod
    async def fetch_all_mastery(
        db: AsyncSession,
        user_id: UUID,
    ) -> list[ConceptMasteryResponse]:
        """
        Return every mastery record for the current user.
        """

        mastery_list = await db_get_all_mastery(
            db=db,
            user_id=user_id,
        )

        return [
            ConceptMasteryResponse.model_validate(mastery)
            for mastery in mastery_list
        ]
