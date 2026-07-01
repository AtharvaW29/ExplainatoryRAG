from uuid import UUID

from fastapi import APIRouter, Depends, status
from neo4j import AsyncSession

from src.controllers.graph_controller import GraphController
from src.graph.database import get_graph_session
from src.schemas.graph import (
    ConceptGraphResponse,
    ConceptNeighborhoodResponse,
    LearningPathResponse,
)

router = APIRouter(
    prefix="/graph",
    tags=["Graph"],
)


@router.get(
    "/concept-neighborhood/{concept_id}",
    response_model=ConceptNeighborhoodResponse,
    status_code=status.HTTP_200_OK,
)
async def get_concept_neighborhood(
    concept_id: UUID,
    graph: AsyncSession = Depends(get_graph_session),
) -> ConceptNeighborhoodResponse:
    """Returns the one-hop neighborhood of a concept."""
    return await GraphController.get_concept_neighborhood(
        graph=graph, concept_id=concept_id
    )


@router.get(
    "/expand-graph/{concept_id}",
    response_model=ConceptGraphResponse,
    status_code=status.HTTP_200_OK,
)
async def expand_graph(
    concept_id: UUID,
    graph: AsyncSession = Depends(get_graph_session),
) -> ConceptGraphResponse:
    """Expands the graph around a concept."""
    return await GraphController.expand_graph(
        graph=graph, concept_id=concept_id
    )


@router.get(
    "/learning-path/{concept_id}",
    response_model=LearningPathResponse,
    status_code=status.HTTP_200_OK,
)
async def get_learning_path(
    concept_id: UUID,
    graph: AsyncSession = Depends(get_graph_session),
) -> LearningPathResponse:
    """Returns the learning path for a concept."""
    return await GraphController.get_learning_path(
        graph=graph, concept_id=concept_id
    )
