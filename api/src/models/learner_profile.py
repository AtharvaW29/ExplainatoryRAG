import uuid
from uuid import UUID

from sqlalchemy import (
    ARRAY,
    Column,
    DateTime,
    ForeignKey,
    String,
    select,
    text,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base
from src.schemas.learner_profile import (
    LearnerPreferencesResponse,
    LearnerProfileCreate,
    LearnerProfilePatch,
)


class LearnerProfile(Base):
    __tablename__ = "learner_profiles"

    id = Column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )

    user_id = Column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id"),
        unique=True,
        nullable=False,
    )

    academic_level = Column(String(50), nullable=True)
    institution = Column(String(50), nullable=True)
    major = Column(String(50), nullable=True)
    learning_style = Column(String(50), nullable=True)
    preferred_explanation_style = Column(String(100), nullable=True)
    preferred_difficulty = Column(String(50), nullable=True)
    language = Column(String(30), default="English")
    domain: Mapped[list[str]] = mapped_column(ARRAY(String(30)), default=list)

    created_at = Column(DateTime, server_default=text("NOW()"), nullable=False)
    updated_at = Column(DateTime, onupdate=text("NOW()"), nullable=True)


async def db_get_learnerprofile(
    db: AsyncSession, user_id: UUID
) -> LearnerProfile | None:
    statement = select(LearnerProfile).where(LearnerProfile.user_id == user_id)
    res = await db.execute(statement)
    return res.scalar_one_or_none()


async def db_create_learnerprofile(
    db: AsyncSession, profile_data: LearnerProfileCreate
) -> LearnerProfile | None:
    new_profile = LearnerProfile(**profile_data.model_dump())
    db.add(new_profile)
    await db.commit()
    await db.refresh(new_profile)
    return new_profile


async def db_patch_learnerprofile(
    db: AsyncSession, user_id: UUID, profile_data: LearnerProfilePatch
) -> LearnerProfile | None:

    try:
        statement = select(LearnerProfile).where(
            LearnerProfile.user_id == user_id
        )

        res = await db.execute(statement)

        profile = res.scalar_one_or_none()

        if not profile:
            return None

        for key, value in profile_data.model_dump(exclude_unset=True).items():
            setattr(profile, key, value)

        db.add(profile)

        await db.commit()

        await db.refresh(profile)

        return profile

    except Exception:
        await db.rollback()

        return None


async def db_get_learner_profile_preferences(
    db: AsyncSession, user_id: UUID
) -> LearnerPreferencesResponse | None:
    statement = select(LearnerProfile).where(LearnerProfile.user_id == user_id)
    res = await db.execute(statement)
    pref = res.scalar_one_or_none()
    if pref is None:
        return None
    return LearnerPreferencesResponse.model_validate(pref)
