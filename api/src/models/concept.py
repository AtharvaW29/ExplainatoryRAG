import uuid
from uuid import UUID

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Index,
    String,
    Text,
    select,
    text,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base
from src.schemas.concept import (
    ConceptCreate,
    ConceptPatch,
)


class Concept(Base):
    __tablename__ = "concepts"

    id = Column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True,
    )

    description = Column(
        Text,
        nullable=True,
    )

    difficulty = Column(
        String(30),
        nullable=True,
    )

    domain = Column(
        String(50),
        nullable=True,
    )

    isactive: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=text("NOW()"),
        nullable=False,
    )

    __table_args__ = (
        Index("idx_concept_name", "name"),
        Index("idx_concept_domain", "domain"),
    )


async def db_get_concept(
    db: AsyncSession,
    concept_id: UUID,
) -> Concept | None:
    statement = select(Concept).where(Concept.id == concept_id)

    result = await db.execute(statement)

    return result.scalar_one_or_none()


async def db_get_concept_by_name(
    db: AsyncSession,
    name: str,
) -> Concept | None:
    statement = select(Concept).where(
        (Concept.name == name) & Concept.isactive
    )

    result = await db.execute(statement)

    return result.scalar_one_or_none()


async def db_get_all_concepts(
    db: AsyncSession,
) -> list[Concept]:

    statement = (
        select(Concept).where(Concept.isactive).order_by(Concept.name.asc())
    )

    result = await db.execute(statement)

    return list(result.scalars().all())


async def db_create_concept(
    db: AsyncSession,
    concept_data: ConceptCreate,
) -> Concept:

    concept = Concept(**concept_data.model_dump())

    db.add(concept)

    await db.commit()

    await db.refresh(concept)

    return concept


async def db_patch_concept(
    db: AsyncSession,
    concept_id: UUID,
    concept_data: ConceptPatch,
) -> Concept | None:

    concept = await db_get_concept(
        db,
        concept_id,
    )

    if concept is None:
        return None

    for field, value in concept_data.model_dump(exclude_unset=True).items():
        setattr(concept, field, value)

    db.add(concept)

    await db.commit()

    await db.refresh(concept)

    return concept


async def db_delete_concept(
    db: AsyncSession, concept_id: UUID, isdeleted: bool
) -> bool:

    concept = await db_get_concept(
        db,
        concept_id,
    )

    if concept is None:
        return False

    concept.isactive = not isdeleted
    try:
        db.add(concept)
        await db.commit()
        return True
    except Exception:
        await db.rollback()
        return False
