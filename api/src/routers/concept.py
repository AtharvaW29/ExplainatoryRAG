from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.controllers.concept_controller import ConceptController
from src.database import get_db
from src.schemas.concept import (
    ConceptCreate,
    ConceptPatch,
    ConceptResponse,
    ConceptSummary,
)

router = APIRouter(
    prefix="/concept",
    tags=["Concepts"],
)


@router.post(
    "",
    response_model=ConceptResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_concept(
    payload: ConceptCreate, db: AsyncSession = Depends(get_db)
):
    """
    Create a Concept
    """
    return await ConceptController.create_concept(
        db=db, concept_data=payload.model_dump()
    )


@router.patch(
    "/{concept_id}",
    response_model=ConceptPatch,
    status_code=status.HTTP_201_CREATED,
)
async def patch_concept(
    concept_id: UUID,
    payload: ConceptPatch,
    db: AsyncSession = Depends(get_db),
):
    """
    Patch a Concept
    """
    return await ConceptController.patch_concept(
        db=db, concept_id=concept_id, concept_data=payload
    )


@router.get(
    "/{concept_id}",
    response_model=ConceptResponse,
    status_code=status.HTTP_200_OK,
)
async def get_concept(concept_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Get Concept Details
    """
    return await ConceptController.get_concept(db=db, concept_id=concept_id)


@router.get(
    "/{concept_name}",
    response_model=ConceptResponse,
    status_code=status.HTTP_200_OK,
)
async def get_concept_by_name(
    concept_name: str, db: AsyncSession = Depends(get_db)
):
    """
    Get Concept Details
    """
    return await ConceptController.get_concept_by_name(
        db=db, name=concept_name
    )


@router.get(
    "", response_model=list[ConceptSummary], status_code=status.HTTP_200_OK
)
async def list_concepts(db: AsyncSession = Depends(get_db)):
    """
    List every concept
    """
    return await ConceptController.get_all_concepts(db=db)


@router.delete(
    "/{concept_id}",
)
async def delete_concept(
    isdeleted: bool, concept_id: UUID, db: AsyncSession = Depends(get_db)
):
    await ConceptController.delete_concept(db, concept_id, isdeleted=isdeleted)
    return status.HTTP_204_NO_CONTENT
