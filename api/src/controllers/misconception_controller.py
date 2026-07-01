from uuid import UUID

from fastapi import HTTPException, status
from neo4j import AsyncSession

from src.models.misconception import (
    db_attach_misconception_to_concepts,
    db_create_misconception,
    db_delete_misconception,
    db_get_misconception,
    db_list_misconceptions,
    db_patch_misconception,
)
from src.schemas.misconception import (
    MisconceptionCreate,
    MisconceptionPatch,
    MisconceptionResponse,
)


class MisconceptionController:
    @staticmethod
    async def create_misconception(
        graph: AsyncSession,
        payload: MisconceptionCreate,
    ) -> MisconceptionResponse:

        misconception = await db_create_misconception(
            graph,
            payload,
        )

        if misconception is None:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Unable to create misconception.",
            )

        return MisconceptionResponse.model_validate(misconception)

    @staticmethod
    async def patch_misconception(
        graph: AsyncSession,
        misconception_id: UUID,
        payload: MisconceptionPatch,
    ) -> MisconceptionResponse:

        misconception = await db_patch_misconception(
            graph,
            misconception_id,
            payload,
        )

        if misconception is None:
            raise HTTPException(
                404,
                "Misconception not found.",
            )

        return MisconceptionResponse.model_validate(misconception)

    @staticmethod
    async def delete_misconception(
        graph: AsyncSession,
        misconception_id: UUID,
    ) -> bool:

        success = await db_delete_misconception(
            graph,
            misconception_id,
        )

        if not success:
            raise HTTPException(
                404,
                "Misconception not found.",
            )

        return True

    @staticmethod
    async def attach_to_concepts(
        graph: AsyncSession,
        misconception_id: UUID,
        concept_ids: list[UUID],
    ) -> bool:

        success = await db_attach_misconception_to_concepts(
            graph,
            misconception_id,
            concept_ids,
        )

        if not success:
            raise HTTPException(
                400,
                "Unable to attach misconception.",
            )

        return True

    @staticmethod
    async def get_misconception(
        graph: AsyncSession,
        misconception_id: UUID,
    ) -> MisconceptionResponse:

        misconception = await db_get_misconception(
            graph,
            misconception_id,
        )

        if misconception is None:
            raise HTTPException(
                404,
                "Misconception not found.",
            )

        return MisconceptionResponse.model_validate(misconception)

    @staticmethod
    async def list_misconceptions(
        graph: AsyncSession,
    ) -> list[MisconceptionResponse]:

        misconceptions = await db_list_misconceptions(
            graph,
        )

        return [
            MisconceptionResponse.model_validate(m) for m in misconceptions
        ]
