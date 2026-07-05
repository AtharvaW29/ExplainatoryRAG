import os
from collections.abc import AsyncGenerator
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

load_dotenv()


class Base(DeclarativeBase):
    pass


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def build_database_url() -> str:
    user = _require_env("app_DB_USER")
    password = _require_env("app_DB_PASSWORD")
    host = _require_env("app_DB_HOST")
    port = _require_env("app_DB_PORT")
    db_name = _require_env("app_DB")

    return (
        "postgresql+asyncpg://"
        f"{quote_plus(user)}:{quote_plus(password)}"
        f"@{host}:{port}/{db_name}"
    )


DATABASE_URL = build_database_url()
if not DATABASE_URL:
    raise ValueError("Database URL Not Found!")

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, autocommit=False, autoflush=False, expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
