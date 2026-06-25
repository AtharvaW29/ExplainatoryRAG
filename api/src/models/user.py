from sqlalchemy import Boolean, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.schemas.user import UserCreateSchema


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


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
