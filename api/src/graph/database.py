import logging
import os
from collections.abc import AsyncGenerator

from dotenv import load_dotenv
from neo4j import AsyncDriver, AsyncGraphDatabase, AsyncSession

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

if not NEO4J_URI:
    raise ValueError("NEO4J_URI not configured.")

if not NEO4J_USERNAME:
    raise ValueError("NEO4J_USERNAME not configured.")

if not NEO4J_PASSWORD:
    raise ValueError("NEO4J_PASSWORD not configured.")


driver: AsyncDriver = AsyncGraphDatabase.driver(
    NEO4J_URI,
    auth=(
        NEO4J_USERNAME,
        NEO4J_PASSWORD,
    ),
)

logger = logging.getLogger("uvicorn.error")


async def get_graph_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for Neo4j sessions.
    """

    async with driver.session() as session:
        yield session
    logger.info("NEO4j Session Active!")


async def close_graph_driver():
    logger.info("NEO4j Session Closing")
    await driver.close()
