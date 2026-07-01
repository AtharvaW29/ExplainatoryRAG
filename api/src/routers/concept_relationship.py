from uuid import UUID

from fastapi import APIRouter, Depends, status
from neo4j import AsyncSession

from src.controllers.concept_relationship_controller import (
    ConceptRelationshipController,
)
from src.graph.database import get_graph_session
from src.schemas.concept_relationship import (
    ConceptRelationshipCreate,
    ConceptRelationshipExists,
    ConceptRelationshipRemove,
    RelatedConceptResponse,
)

router = APIRouter(
    prefix="/concept-relationship", tags=["Concpet Relationships"]
)


@router.post(
    "/add-prerequisite",
    response_model=bool,
    status_code=status.HTTP_201_CREATED,
)
async def add_prerequisite_concept(
    concept_id: UUID,
    payload: ConceptRelationshipCreate,
    graph: AsyncSession = Depends(get_graph_session),
) -> bool:
    """Adds a Pre-Requisite Concept"""
    return await ConceptRelationshipController.add_prerequisite(
        graph=graph, concept_id=concept_id, payload=payload
    )


@router.post(
    "/add-related-concept",
    response_model=bool,
    status_code=status.HTTP_201_CREATED,
)
async def add_related_concept(
    concept_id: UUID,
    payload: ConceptRelationshipCreate,
    graph: AsyncSession = Depends(get_graph_session),
) -> bool:
    """Adds a related concept to the existing concept"""
    return await ConceptRelationshipController.add_related_concept(
        graph=graph, concept_id=concept_id, payload=payload
    )


@router.get(
    "/get-prerequisites",
    response_model=list[RelatedConceptResponse],
    status_code=status.HTTP_200_OK,
)
async def get_concept_prerequisites(
    concept_id: UUID, graph: AsyncSession = Depends(get_graph_session)
) -> list[RelatedConceptResponse] | None:
    """Gets Concept Pre-requisites for a Concept"""
    return await ConceptRelationshipController.get_prerequisites(
        concept_id=concept_id, graph=graph
    )


@router.get(
    "/get-related-concepts",
    response_model=list[RelatedConceptResponse],
    status_code=status.HTTP_200_OK,
)
async def get_related_concepts(
    concept_id: UUID, graph: AsyncSession = Depends(get_graph_session)
) -> list[RelatedConceptResponse] | None:
    """Gets Related Concepts"""
    return await ConceptRelationshipController.get_related_concepts(
        concept_id=concept_id, graph=graph
    )


@router.delete("/{source_concept_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_relationship(
    source_concept_id: UUID,
    payload: ConceptRelationshipRemove,
    graph: AsyncSession = Depends(get_graph_session),
) -> None:
    """
    Removes a Relationship If it Exists
    """
    await ConceptRelationshipController.remove_relationship(
        source_concept_id=source_concept_id, payload=payload, graph=graph
    )


@router.get("/", status_code=status.HTTP_200_OK, response_model=bool)
async def relationsship_exists(
    payload: ConceptRelationshipExists,
    graph: AsyncSession = Depends(get_graph_session),
) -> bool:
    """
    Checks if a given realtionship is valid or not
    """
    return await ConceptRelationshipController.relationship_exists(
        payload=payload, graph=graph
    )
