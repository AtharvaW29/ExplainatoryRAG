from uuid import UUID

from fastapi import APIRouter, Depends, status
from neo4j import AsyncSession

from src.controllers.misconception_controller import MisconceptionController
from src.graph.database import get_graph_session
from src.schemas.misconception import (
    MisconceptionCreate,
    MisconceptionPatch,
    MisconceptionResponse,
)

router = APIRouter(
    prefix="/misconceptions",
    tags=["Misconceptions"],
)


@router.post(
    "/",
    response_model=MisconceptionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_misconception(
    payload: MisconceptionCreate,
    graph: AsyncSession = Depends(get_graph_session),
) -> MisconceptionResponse:
    """Creates a new misconception."""
    return await MisconceptionController.create_misconception(
        graph=graph, payload=payload
    )


@router.patch(
    "/{misconception_id}",
    response_model=MisconceptionResponse,
)
async def patch_misconception(
    misconception_id: UUID,
    payload: MisconceptionPatch,
    graph: AsyncSession = Depends(get_graph_session),
) -> MisconceptionResponse:
    """Updates an existing misconception."""
    return await MisconceptionController.patch_misconception(
        graph=graph, misconception_id=misconception_id, payload=payload
    )


@router.delete(
    "/{misconception_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_misconception(
    misconception_id: UUID,
    graph: AsyncSession = Depends(get_graph_session),
) -> None:
    """Deletes an existing misconception."""
    await MisconceptionController.delete_misconception(
        graph=graph, misconception_id=misconception_id
    )


@router.patch(
    "/{misconception_id}/attach-concepts",
    status_code=status.HTTP_200_OK,
    response_model=bool,
)
async def attach_misconception_to_concepts(
    misconception_id: UUID,
    concept_ids: list[UUID],
    graph: AsyncSession = Depends(get_graph_session),
) -> bool:
    """Attaches a misconception to multiple concepts."""
    return await MisconceptionController.attach_to_concepts(
        graph=graph, misconception_id=misconception_id, concept_ids=concept_ids
    )


@router.get(
    "/{misconception_id}",
    response_model=MisconceptionResponse,
)
async def get_misconception(
    misconception_id: UUID,
    graph: AsyncSession = Depends(get_graph_session),
) -> MisconceptionResponse:
    """Retrieves a specific misconception."""
    return await MisconceptionController.get_misconception(
        graph=graph, misconception_id=misconception_id
    )


@router.get(
    "/",
    response_model=list[MisconceptionResponse],
)
async def list_misconceptions(
    graph: AsyncSession = Depends(get_graph_session),
) -> list[MisconceptionResponse]:
    """Lists all misconceptions."""
    return await MisconceptionController.list_misconceptions(graph=graph)
