from uuid import UUID

from fastapi import HTTPException
from neo4j import AsyncSession

from src.models.graph import (
    db_expand_graph,
    db_get_concept_neighborhood,
    db_get_learning_path,
)
from src.schemas.graph import (
    ConceptGraphResponse,
    LearningPathResponse,
)


class GraphController:
    @staticmethod
    async def get_concept_neighborhood(
        graph: AsyncSession,
        concept_id: UUID,
        depth: int = 2,
    ) -> ConceptGraphResponse:

        neighborhood = await db_get_concept_neighborhood(
            graph,
            concept_id,
            depth,
        )

        if neighborhood is None:
            raise HTTPException(
                404,
                "Concept not found.",
            )

        return ConceptGraphResponse.model_validate(neighborhood)

    @staticmethod
    async def expand_graph(
        graph: AsyncSession,
        concept_id: UUID,
        hops: int = 3,
    ) -> ConceptGraphResponse:

        result = await db_expand_graph(
            graph,
            concept_id,
            hops,
        )

        return ConceptGraphResponse.model_validate(result)

    @staticmethod
    async def get_learning_path(
        graph: AsyncSession,
        concept_id: UUID,
    ) -> LearningPathResponse:

        path = await db_get_learning_path(
            graph,
            concept_id,
        )

        if path is None:
            raise HTTPException(
                404,
                "No learning path found.",
            )

        return LearningPathResponse.model_validate(path)
