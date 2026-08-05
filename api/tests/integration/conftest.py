import os
import subprocess
import sys
from collections.abc import AsyncGenerator, Generator
from pathlib import Path
from typing import Any, Iterator, Protocol
from urllib.parse import quote_plus

import psycopg2
import pytest
import pytest_asyncio
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from psycopg2 import sql
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from starlette.testclient import WebSocketTestSession

API_ROOT = Path(__file__).resolve().parents[2]
print(API_ROOT)
load_dotenv(API_ROOT / ".env")

# os.environ.setdefault("app_DB_USER", "user")
# os.environ.setdefault("app_DB_PASSWORD", "password")
# os.environ.setdefault("app_DB_HOST", "127.0.0.1")
# os.environ.setdefault("app_DB_PORT", "5432")
# os.environ.setdefault("app_DB", "explainatory_rag_test")
os.environ.setdefault(
    "JWT_SECRET_KEY",
    "integration-test-secret-key-that-is-not-used-outside-tests",
)
# os.environ.setdefault("NEO4J_URI", "bolt://127.0.0.1:7687")
# os.environ.setdefault("NEO4J_USERNAME", "neo4j")
# os.environ.setdefault("NEO4J_PASSWORD", "test-password")


from src.database import get_db  # noqa: E402
from src.main import app  # noqa: E402


def _database_name() -> str:
    return os.environ["app_DB_TEST"]


def _ensure_test_database_name(database_name: str) -> None:
    if "test" not in database_name.casefold():
        raise RuntimeError(
            "Integration tests refuse to modify a database whose name does "
            "not contain 'test'."
        )


def _admin_connection():
    return psycopg2.connect(
        dbname="postgres",
        user=os.environ["app_DB_USER"],
        password=os.environ["app_DB_PASSWORD"],
        host=os.environ["app_DB_HOST"],
        port=os.environ["app_DB_PORT"],
    )


def recreate_database(database_name: str) -> None:
    """Recreate one explicitly named disposable test database."""

    _ensure_test_database_name(database_name)

    connection = _admin_connection()
    try:
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                sql.SQL("DROP DATABASE IF EXISTS {} WITH (FORCE)").format(
                    sql.Identifier(database_name)
                )
            )
            cursor.execute(
                sql.SQL("CREATE DATABASE {}").format(
                    sql.Identifier(database_name)
                )
            )
    finally:
        connection.close()


def drop_database(database_name: str) -> None:
    _ensure_test_database_name(database_name)

    connection = _admin_connection()
    try:
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                sql.SQL("DROP DATABASE IF EXISTS {} WITH (FORCE)").format(
                    sql.Identifier(database_name)
                )
            )
    finally:
        connection.close()


def run_alembic(
    *arguments: str,
    database_name: str | None = None,
) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()

    if database_name is not None:
        _ensure_test_database_name(database_name)

        environment["app_DB_TEST"] = database_name
        environment["ALEMBIC_DATABASE_URL"] = _async_database_url(
            database_name
        )

    command = [
        sys.executable,
        "-m",
        "alembic",
        *arguments,
    ]

    result = subprocess.run(
        command,
        cwd=API_ROOT,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(
            "\nAlembic command failed.\n"
            f"Command: {' '.join(command)}\n"
            f"Working directory: {API_ROOT}\n"
            f"Test database: {database_name or '<not overridden>'}\n"
            f"Exit code: {result.returncode}\n"
            "\n"
            "----- Alembic stdout -----\n"
            f"{result.stdout.strip() or '<empty>'}\n"
            "\n"
            "----- Alembic stderr -----\n"
            f"{result.stderr.strip() or '<empty>'}\n"
        )

    return result


def _truncate_application_tables(database_name: str) -> None:
    connection = psycopg2.connect(
        dbname=database_name,
        user=os.environ["app_DB_USER"],
        password=os.environ["app_DB_PASSWORD"],
        host=os.environ["app_DB_HOST"],
        port=os.environ["app_DB_PORT"],
    )

    try:
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT tablename
                FROM pg_tables
                WHERE schemaname = 'public'
                  AND tablename <> 'alembic_version'
                """
            )
            table_names = [row[0] for row in cursor.fetchall()]

            if table_names:
                identifiers = sql.SQL(", ").join(
                    sql.Identifier(table_name) for table_name in table_names
                )
                cursor.execute(
                    sql.SQL(
                        "TRUNCATE TABLE {} RESTART IDENTITY CASCADE"
                    ).format(identifiers)
                )
    finally:
        connection.close()


def _async_database_url(database_name: str) -> str:
    return (
        "postgresql+asyncpg://"
        f"{quote_plus(os.environ['app_DB_USER'])}:"
        f"{quote_plus(os.environ['app_DB_PASSWORD'])}"
        f"@{os.environ['app_DB_HOST']}:{os.environ['app_DB_PORT']}"
        f"/{database_name}"
    )


def dispose_test_database_connections() -> None:
    """Dispose of all connections to the test database.

    This is necessary before dropping the database, as PostgreSQL does not
    allow dropping a database with active connections.
    """
    database_name = _database_name()
    _ensure_test_database_name(database_name)

    connection = _admin_connection()
    try:
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                sql.SQL(
                    """
                    SELECT pg_terminate_backend(pid)
                    FROM pg_stat_activity
                    WHERE datname = %s
                      AND pid <> pg_backend_pid()
                    """
                ),
                (database_name,),
            )
    finally:
        connection.close()


@pytest.fixture(scope="session")
def migrated_test_database() -> Iterator[str]:
    database_name = "explainatory_rag_test"

    recreate_database(database_name)

    try:
        run_alembic(
            "upgrade",
            "head",
            database_name=database_name,
        )
        yield database_name
    finally:
        dispose_test_database_connections()
        drop_database(database_name)


@pytest.fixture(autouse=True)
def clean_database(
    migrated_test_database: str,
) -> Generator[None, None, None]:
    _truncate_application_tables(migrated_test_database)
    yield
    _truncate_application_tables(migrated_test_database)


@pytest_asyncio.fixture
async def session_factory(
    migrated_test_database: str,
) -> AsyncGenerator[async_sessionmaker[AsyncSession], None]:
    engine = create_async_engine(
        _async_database_url(migrated_test_database),
        pool_pre_ping=True,
    )
    factory = async_sessionmaker(
        engine,
        expire_on_commit=False,
        autoflush=False,
    )

    yield factory
    await engine.dispose()


@pytest_asyncio.fixture
async def client(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        async with session_factory() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app, raise_app_exceptions=True)
    async with AsyncClient(
        transport=transport,
        base_url="http://localhost:8001",
    ) as test_client:
        yield test_client

    app.dependency_overrides.clear()


class UserFactory(Protocol):
    async def __call__(
        self,
        name: str,
        email: str,
        password: str = "Password123!",
    ) -> dict[str, Any]: ...


@pytest.fixture
def user_factory(client: AsyncClient) -> UserFactory:
    async def create_user(
        name: str,
        email: str,
        password: str = "Password123!",
    ) -> dict[str, Any]:
        registration = await client.post(
            "/auth/register",
            json={
                "name": name,
                "email": email,
                "password": password,
            },
        )
        assert registration.status_code == 201, registration.text

        login = await client.post(
            "/auth/login",
            json={"email": email, "password": password},
        )
        assert login.status_code == 200, login.text

        return {
            "user": registration.json(),
            "token": login.json()["access_token"],
            "headers": {
                "Authorization": (f"Bearer {login.json()['access_token']}")
            },
        }

    return create_user


@pytest.fixture
def websocket_client(
    session_factory: async_sessionmaker[AsyncSession],
) -> Generator[TestClient, None, None]:
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        async with session_factory() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()


@pytest.fixture
def chat_websocket(
    websocket_client: TestClient,
) -> Generator[WebSocketTestSession, None, None]:
    with websocket_client.websocket_connect(
        "/explanation-sessions/start_exp_session",
        subprotocols=["llm-chat.v1"],
    ) as websocket:
        yield websocket
