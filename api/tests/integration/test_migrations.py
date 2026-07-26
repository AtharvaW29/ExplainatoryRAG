import os

import pytest

from .conftest import drop_database, recreate_database, run_alembic


@pytest.mark.migration
def test_clean_database_migration_round_trip() -> None:
    database_name = str(os.getenv("app_DB_TEST_MIGRATION"))

    recreate_database(database_name)

    try:
        run_alembic("upgrade", "head", database_name=database_name)
        run_alembic(
            "current",
            "--check-heads",
            database_name=database_name,
        )
        first_check = run_alembic(
            "check",
            database_name=database_name,
        )
        assert "No new upgrade operations detected" in (
            first_check.stdout + first_check.stderr
        )

        run_alembic("downgrade", "base", database_name=database_name)
        run_alembic("upgrade", "head", database_name=database_name)

        second_check = run_alembic(
            "check",
            database_name=database_name,
        )
        assert "No new upgrade operations detected" in (
            second_check.stdout + second_check.stderr
        )
    finally:
        drop_database(database_name)
