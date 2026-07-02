import logging
from pathlib import Path

from neo4j import AsyncDriver

from src.graph.database import driver

GRAPH_ROOT = Path(__file__).resolve().parent.parent
CYPHER_DIR = GRAPH_ROOT / "cypher"

CONSTRAINT_FILE = CYPHER_DIR / "constraints.cypher"
INDEX_FILE = CYPHER_DIR / "indexes.cypher"

logger = logging.getLogger("uvicorn.error")


async def execute_cypher_file(
    driver: AsyncDriver,
    file_path: Path,
) -> None:
    """
    Executes every Cypher statement contained in a .cypher file.

    Statements are separated by ';'.
    """

    if not file_path.exists():
        raise FileNotFoundError(f"Cypher file not found: {file_path}")

    cypher = file_path.read_text(encoding="utf-8")

    statements = [stmt.strip() for stmt in cypher.split(";") if stmt.strip()]

    async with driver.session() as session:
        for statement in statements:
            await session.run(statement)

    logger.info(
        f"[Neo4j] Executed {len(statements)} statements from {file_path.name}"
    )


async def verify_connection(
    driver: AsyncDriver,
) -> None:
    """
    Ensures Neo4j is reachable before executing any scripts.
    """

    await driver.verify_connectivity()

    logger.info("[Neo4j] Connection verified.")


async def initialize_graph() -> None:
    """
    Initializes Neo4j.
    """

    try:
        logger.info("[Neo4j] Initializing graph...")

        await verify_connection(driver)

        await execute_cypher_file(
            driver,
            CONSTRAINT_FILE,
        )

        await execute_cypher_file(
            driver,
            INDEX_FILE,
        )

        logger.info("[Neo4j] Graph initialization completed successfully.")

    except Exception as e:
        logger.error(f"[Neo4j] Error occurred while initializing graph: {e}")
