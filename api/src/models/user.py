import uuid

from sqlalchemy import Boolean, Column, String, select, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from src.schemas.user import UserCreateSchema


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    name = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False)


async def db_get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    statement = select(User).where(User.id == user_id)
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
