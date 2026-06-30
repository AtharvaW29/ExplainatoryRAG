import uuid
from uuid import UUID

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    UniqueConstraint,
    select,
    text,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base
from src.schemas.concept_mastery import (
    ConceptMasteryCreate,
    ConceptMasteryPatch,
)


class ConceptMastery(Base):
    __tablename__ = "concept_mastery"

    id = Column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )

    user_id = Column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )

    concept_id = Column(
        PG_UUID(as_uuid=True),
        ForeignKey("concepts.id"),
        nullable=False,
    )

    mastery_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    last_interaction = Column(
        DateTime(timezone=True),
        server_default=text("NOW()"),
        onupdate=text("NOW()"),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "concept_id",
            name="uq_user_concept_mastery",
        ),
        Index("idx_mastery_user", "user_id"),
        Index("idx_mastery_concept", "concept_id"),
    )


async def db_get_mastery(
    db: AsyncSession,
    user_id: UUID,
    concept_id: UUID,
) -> ConceptMastery | None:
    statement = select(ConceptMastery).where(
        ConceptMastery.user_id == user_id,
        ConceptMastery.concept_id == concept_id,
    )

    result = await db.execute(statement)
    return result.scalar_one_or_none()


async def db_get_all_mastery(
    db: AsyncSession,
    user_id: UUID,
) -> list[ConceptMastery]:

    statement = (
        select(ConceptMastery)
        .where(ConceptMastery.user_id == user_id)
        .order_by(
            ConceptMastery.mastery_score.desc(),
            ConceptMastery.last_interaction.desc(),
        )
    )

    result = await db.execute(statement)

    return list(result.scalars().all())


async def db_create_mastery(
    db: AsyncSession,
    mastery_data: ConceptMasteryCreate,
) -> ConceptMastery:

    mastery = ConceptMastery(**mastery_data.model_dump())

    db.add(mastery)

    await db.commit()

    await db.refresh(mastery)

    return mastery


async def db_update_mastery(
    db: AsyncSession,
    mastery: ConceptMastery,
    update_data: ConceptMasteryPatch,
) -> ConceptMastery:

    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(mastery, field, value)

    db.add(mastery)

    await db.commit()

    await db.refresh(mastery)

    return mastery


async def db_upsert_mastery(
    db: AsyncSession,
    mastery_data: ConceptMasteryCreate,
) -> ConceptMastery:

    mastery = await db_get_mastery(
        db=db,
        user_id=mastery_data.user_id,
        concept_id=mastery_data.concept_id,
    )
    if mastery:
        mastery.mastery_score = mastery_data.mastery_score
        mastery.confidence = mastery_data.confidence
        db.add(mastery)
        await db.commit()
        await db.refresh(mastery)
        return mastery
    mastery = ConceptMastery(**mastery_data.model_dump())
    db.add(mastery)
    await db.commit()
    await db.refresh(mastery)
    return mastery


async def db_delete_mastery(
    db: AsyncSession,
    user_id: UUID,
    concept_id: UUID,
) -> bool:

    mastery = await db_get_mastery(
        db,
        user_id,
        concept_id,
    )

    if mastery is None:
        return False

    await db.delete(mastery)

    await db.commit()

    return True
