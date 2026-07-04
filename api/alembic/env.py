import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context
from src.database import DATABASE_URL, Base

# Import all application models so Alembic/autogenerate can discover them.

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

if DATABASE_URL:
    config.set_main_option("sqlalchemy.url", DATABASE_URL.replace("%", "%%"))

# Alembic needs the shared metadata from your declarative base.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode using the async engine."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def do_run_migrations(sync_connection) -> None:
    context.configure(
        connection=sync_connection,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
