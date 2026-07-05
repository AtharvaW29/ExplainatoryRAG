import uuid
from typing import cast

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    select,
    text,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base
from src.schemas.explanation import (
    ExplanationCreate,
    ExplanationResponse,
    RetrievalMetadataSchema,
)


class RetrievalMetaData(Base):
    __tablename__ = "retrieval_metatdata"

    id = Column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
        nullable=False,
    )
    explanation_id = Column(
        PG_UUID(as_uuid=True), ForeignKey("explanations.id"), nullable=False
    )
    source_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    retrieved_chunks: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    average_similarity: Mapped[float] = mapped_column(
        Float, nullable=True, default=0.0
    )


class Explanation(Base):
    __tablename__ = "explanations"

    id = Column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    exp_session_id = Column(
        PG_UUID(as_uuid=True),
        ForeignKey("explanation_sessions.id"),
        nullable=False,
    )

    prompt: Mapped[str] = mapped_column(Text, nullable=False)

    generated_explanation: Mapped[str] = mapped_column(Text, nullable=True)
    difficulty_score: Mapped[float] = mapped_column(Float, nullable=True)

    explanation_style: Mapped[str] = mapped_column(String(100), nullable=True)
    token_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )

    llm_provider: Mapped[str] = mapped_column(String(50), nullable=False)
    llm_model: Mapped[str] = mapped_column(String(50), nullable=True)

    generation_time_ms: Mapped[float] = mapped_column(
        Float, default=0.0, nullable=False
    )

    created_at = Column(DateTime, server_default=text("NOW()"), nullable=False)
    updated_at = Column(DateTime, nullable=True)


async def db_create_explanation(
    db: AsyncSession, payload: ExplanationCreate, exp_session_id: uuid.UUID
) -> bool:
    metadata = payload.retrieval
    filtered_data = payload.model_dump(exclude={"retrieval"})
    filtered_data["exp_session_id"] = exp_session_id
    explanation = Explanation(**filtered_data)

    db.add(explanation)
    await db.flush()

    if metadata is not None:
        metadata_dict = metadata.model_dump()
        metadata_dict["explanation_id"] = explanation.id
        return await db_create_retrieval_metadata(db, metadata_dict)
    return True


async def db_create_retrieval_metadata(
    db: AsyncSession, payload: dict
) -> bool:
    rmd = RetrievalMetaData(**payload)
    db.add(rmd)
    await db.flush()
    return rmd.id is not None


async def db_get_explanation(
    db: AsyncSession,
    exp_session_id: uuid.UUID,
) -> list[ExplanationResponse]:

    statement = select(Explanation).where(
        Explanation.exp_session_id == exp_session_id
    )

    result = await db.execute(statement)
    explanations = result.scalars().all()

    response = []

    for explanation in explanations:
        metadata = await db_metadata_by_exp(db, cast(PG_UUID, explanation.id))

        response.append(
            ExplanationResponse.model_validate(
                {
                    **explanation.__dict__,
                    "retrieval": metadata,
                }
            )
        )

    return response


async def db_metadata_by_exp(
    db: AsyncSession,
    explanation_id: PG_UUID,
) -> RetrievalMetadataSchema | None:

    statement = select(RetrievalMetaData).where(
        RetrievalMetaData.explanation_id == explanation_id
    )

    result = await db.execute(statement)
    metadata = result.scalar_one_or_none()

    if metadata is None:
        return None

    return RetrievalMetadataSchema.model_validate(metadata)
