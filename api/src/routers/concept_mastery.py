from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.controllers.concept_mastery_controller import (
    ConceptMasteryController,
)
from src.database import get_db
from src.schemas.concept_mastery import (
    ConceptMasteryCreate,
    ConceptMasteryResponse,
)

router = APIRouter(
    prefix="/mastery",
    tags=["Concept Mastery"],
)


@router.post(
    "",
    response_model=ConceptMasteryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_or_update_mastery(
    payload: ConceptMasteryCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Create or update a user's mastery score for a concept.
    """
    return await ConceptMasteryController.create_or_update_mastery(
        db=db,
        payload=payload.model_dump(),
    )


@router.get(
    "/{concept_id}",
    response_model=ConceptMasteryResponse,
)
async def get_mastery(
    concept_id: UUID,
    user_id: UUID = Query(..., description="User ID"),
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieve mastery for a specific concept.
    """
    return await ConceptMasteryController.fetch_mastery(
        db=db,
        user_id=user_id,
        concept_id=concept_id,
    )


@router.get(
    "",
    response_model=list[ConceptMasteryResponse],
)
async def list_mastery(
    user_id: UUID = Query(..., description="User ID"),
    db: AsyncSession = Depends(get_db),
):
    """
    List every concept mastery record for the user.
    """
    return await ConceptMasteryController.fetch_all_mastery(
        db=db,
        user_id=user_id,
    )
