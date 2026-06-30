from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.concept import (
    db_create_concept,
    db_delete_concept,
    db_get_all_concepts,
    db_get_concept,
    db_get_concept_by_name,
    db_patch_concept,
)
from src.schemas.concept import (
    ConceptCreate,
    ConceptPatch,
    ConceptResponse,
    ConceptSummary,
)


class ConceptController:
    @staticmethod
    async def get_concept(
        db: AsyncSession,
        concept_id: UUID,
    ) -> ConceptResponse:
        """
        Gets a concept with all its attributes
        """
        concept = await db_get_concept(db, concept_id)
        if concept is None:
            raise HTTPException(status_code=404, detail="Concept Not Found")
        return ConceptResponse.model_validate(concept)

    @staticmethod
    async def get_concept_by_name(
        db: AsyncSession, name: str
    ) -> ConceptResponse:
        """
        Gets Concept by name
        """
        concept = await db_get_concept_by_name(db, name)
        if concept is None:
            raise HTTPException(status_code=404, detail="Concept Not Found")
        return ConceptResponse.model_validate(concept)

    @staticmethod
    async def get_all_concepts(db: AsyncSession) -> list[ConceptSummary]:
        concepts = await db_get_all_concepts(db)
        if concepts is None:
            raise HTTPException(status_code=404, detail="Concepts Not Found")
        return [ConceptSummary.model_validate(concept) for concept in concepts]

    @staticmethod
    async def create_concept(
        db: AsyncSession, concept_data: dict
    ) -> ConceptResponse:
        validated = ConceptCreate(**concept_data)
        concept = await db_create_concept(db, validated)
        if concept is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request"
            )
        return ConceptResponse.model_validate(concept)

    @staticmethod
    async def patch_concept(
        db: AsyncSession, concept_id: UUID, concept_data: ConceptPatch
    ) -> ConceptPatch | None:

        concept_patch = await db_patch_concept(db, concept_id, concept_data)

        if concept_patch is None:
            raise HTTPException(status_code=400, detail="Bad Request")

        return ConceptPatch.model_validate(concept_patch)

    @staticmethod
    async def delete_concept(
        db: AsyncSession, concept_id: UUID, isdeleted: bool
    ) -> bool:

        success = await db_delete_concept(db, concept_id, isdeleted)
        if not success:
            raise HTTPException(status_code=404, detail="Concept not found")
        return success
