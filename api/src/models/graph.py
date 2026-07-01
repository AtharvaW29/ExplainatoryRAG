from typing import Any
from uuid import UUID

from neo4j import AsyncSession


async def db_get_concept_neighborhood(
    graph: AsyncSession, concept_id: UUID, depth: int = 2
) -> dict[str, Any] | None:
    """
    Returns the one-hop neighborhood of a concept.

    Includes:
    - prerequisite concepts
    - related concepts
    - misconceptions
    """

    query = """
    MATCH (c:Concept {id:$concept_id})

    OPTIONAL MATCH
        (pre:Concept)-[:PREREQUISITE_OF]->(c)

    OPTIONAL MATCH
        (c)-[:RELATED_TO]->(rel:Concept)

    OPTIONAL MATCH
        (mis:Misconception)-[:CAUSES_CONFUSION_WITH]->(c)

    RETURN

    c{
        .id,
        .name,
        .description,
        .difficulty,
        .domain
    } AS concept,

    collect(DISTINCT pre{
        .id,
        .name
    }) AS prerequisites,

    collect(DISTINCT rel{
        .id,
        .name
    }) AS related,

    collect(DISTINCT mis{
        .id,
        .title
    }) AS misconceptions
    """
    depth = max(1, min(depth, 5))
    result = await graph.run(
        query,
        concept_id=str(concept_id),
        depth=depth,
    )

    record = await result.single()

    if record is None:
        return None

    return dict(record)


async def db_expand_graph(
    graph: AsyncSession,
    concept_id: UUID,
    depth: int = 2,
) -> list[dict[str, Any]]:
    """
    Expands the graph around a concept.

    Traverses prerequisite and related relationships.
    """
    depth = max(1, min(depth, 5))
    query = """
    MATCH p=(c:Concept {id:$concept_id})
        -[:PREREQUISITE_OF|RELATED_TO*1..$depth]-
        (neighbor)

    RETURN p
    """

    result = await graph.run(
        query,
        concept_id=str(concept_id),
        depth=depth,
    )

    return await result.data()


async def db_get_learning_path(
    graph: AsyncSession,
    concept_id: UUID,
) -> list[dict[str, Any]]:
    """
    Returns a topological learning path
    leading to the requested concept.
    """

    query = """
    MATCH path=
        (start:Concept)
        -[:PREREQUISITE_OF*]->
        (target:Concept {id:$concept_id})

    WITH nodes(path) AS concepts

    UNWIND concepts AS concept

    RETURN DISTINCT

        concept.id AS id,
        concept.name AS name,
        concept.description AS description,
        concept.difficulty AS difficulty,
        concept.domain AS domain
    """

    result = await graph.run(
        query,
        concept_id=str(concept_id),
    )

    records: list[dict[str, Any]] = await result.data()

    return records
