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


def build_database_url() -> str:
    configured_url = os.getenv("app_DB_URL")
    if configured_url:
        return configured_url

    user = os.getenv("app_DB_USER", "postgres")
    password = os.getenv("app_DB_PASSWORD", "")
    host = os.getenv("app_DB_HOST", "localhost")
    port = os.getenv("app_DB_PORT", "5432")
    db_name = os.getenv("app_DB", "postgres")

    return (
        "postgresql+asyncpg://"
        f"{quote_plus(user)}:{quote_plus(password)}@{host}:{port}/{db_name}"
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
