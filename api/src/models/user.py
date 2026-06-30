import uuid
from uuid import UUID

from sqlalchemy import Boolean, Column, String, select, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Base
from src.schemas.user import UserCreateSchema, UserPatchSchema


class User(Base):
    __tablename__ = "users"

    id = Column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    name = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False)


async def db_get_user_by_email(
    db: AsyncSession, user_email: str
) -> User | None:
    statement = select(User).where(User.email == user_email)
    res = await db.execute(statement)
    return res.scalar_one_or_none()


async def db_create_user(
    db: AsyncSession, user_data: UserCreateSchema
) -> User:
    new_user = User(**user_data.model_dump())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def db_patch_user(
    db: AsyncSession, user_id: UUID, user_data: UserPatchSchema
) -> User | None:
    try:
        statement = select(User).where(User.id == user_id)
        res = await db.execute(statement)
        user = res.scalar_one_or_none()
        if not user:
            return None
        for k, v in user_data.model_dump(exclude_unset=True).items():
            setattr(user, k, v)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    except Exception:
        await db.rollback()
        return None
