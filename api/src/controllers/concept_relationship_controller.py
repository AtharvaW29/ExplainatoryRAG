from uuid import UUID

from fastapi import HTTPException, status
from neo4j import AsyncSession

from src.models.concept_relationship import (
    db_add_concept,
    db_add_prerequisite,
    db_add_related_concept,
    db_get_prerequisites,
    db_get_related_concepts,
    db_relationship_exists,
    db_remove_relationship,
)
from src.schemas.concept_relationship import (
    ConceptNodeCreate,
    ConceptRelationshipCreate,
    ConceptRelationshipExists,
    ConceptRelationshipRemove,
    RelatedConceptResponse,
)


class ConceptRelationshipController:
    @staticmethod
    async def add_concept(
        graph: AsyncSession,
        payload: ConceptNodeCreate,
    ) -> bool:
        success = await db_add_concept(graph=graph, payload=payload)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Unable to create concept.",
            )

        return True

    @staticmethod
    async def add_prerequisite(
        graph: AsyncSession,
        concept_id: UUID,
        payload: ConceptRelationshipCreate,
    ) -> bool:
        success = await db_add_prerequisite(
            graph=graph,
            concept_id=concept_id,
            target_concept_id=payload.target_concept_id,
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Unable to create prerequisite relationship.",
            )

        return True

    @staticmethod
    async def add_related_concept(
        graph: AsyncSession,
        concept_id: UUID,
        payload: ConceptRelationshipCreate,
    ) -> bool:

        success = await db_add_related_concept(
            graph=graph,
            concept_id=concept_id,
            target_concept_id=payload.target_concept_id,
        )

        if not success:
            raise HTTPException(
                status_code=404,
                detail="Unable to create related relationship.",
            )

        return True

    @staticmethod
    async def get_prerequisites(
        graph: AsyncSession,
        concept_id: UUID,
    ) -> list[RelatedConceptResponse] | None:

        concepts = await db_get_prerequisites(
            graph=graph,
            concept_id=concept_id,
        )
        if not concepts:
            raise HTTPException(
                status_code=404,
                detail="No Related Concepts Found",
            )
        return [RelatedConceptResponse.model_validate(c) for c in concepts]

    @staticmethod
    async def get_related_concepts(
        graph: AsyncSession,
        concept_id: UUID,
    ) -> list[RelatedConceptResponse] | None:

        concepts = await db_get_related_concepts(
            graph=graph,
            concept_id=concept_id,
        )

        if not concepts:
            raise HTTPException(
                status_code=404,
                detail="No Related Concepts Found",
            )

        return [RelatedConceptResponse.model_validate(c) for c in concepts]

    @staticmethod
    async def remove_relationship(
        graph: AsyncSession,
        source_concept_id: UUID,
        payload: ConceptRelationshipRemove,
    ) -> bool:

        success = await db_remove_relationship(
            graph=graph, source_concept_id=source_concept_id, payload=payload
        )

        if not success:
            raise HTTPException(
                status_code=404,
                detail="Relationship not found.",
            )

        return True

    @staticmethod
    async def relationship_exists(
        graph: AsyncSession, payload: ConceptRelationshipExists
    ) -> bool:
        return await db_relationship_exists(graph=graph, paylod=payload)
