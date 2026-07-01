import uuid
from typing import Any
from uuid import UUID

from neo4j import AsyncSession

from src.schemas.misconception import (
    MisconceptionCreate,
    MisconceptionPatch,
    MisconceptionResponse,
)


async def db_create_misconception(
    graph: AsyncSession,
    payload: MisconceptionCreate,
) -> MisconceptionResponse:
    """
    Creates a Misconception node.

    Returns the created node.
    """

    query = """
    CREATE (m:Misconception {
        id: $id,
        user_id: $user_id,
        title: $title,
        explanation: $explanation,
        frequency: $frequency
        concept_ids: $concept_ids
    })

    RETURN
        m.id AS id,
        m.user_id AS user_id,
        m.title AS title,
        m.explanation AS explanation,
        m.frequency AS frequency
        m.concept_ids AS concept_ids
    """

    result = await graph.run(
        query,
        id=str(uuid.uuid4()),
        user_id=str(payload.user_id),
        title=payload.title,
        explanation=payload.explanation,
        frequency=payload.frequency,
        concept_ids=[str(i) for i in payload.concept_ids],
    )

    record = await result.single()

    if record is None:
        raise RuntimeError("Failed to create misconception.")

    return MisconceptionResponse.model_validate(record)


async def db_attach_misconception_to_concepts(
    graph: AsyncSession,
    misconception_id: UUID,
    concept_ids: list[UUID],
) -> bool:
    """
    Creates

    (Misconception)-[:CAUSES_CONFUSION_WITH]->(Concept)

    relationships.
    """

    query = """
    MATCH (m:Misconception {id: $misconception_id})

    UNWIND $concept_ids AS cid

    MATCH (c:Concept {id: cid})

    MERGE (m)-[:CAUSES_CONFUSION_WITH]->(c)

    RETURN COUNT(c) AS attached
    """

    result = await graph.run(
        query,
        misconception_id=str(misconception_id),
        concept_ids=[str(i) for i in concept_ids],
    )

    record = await result.single()

    if record is None:
        return False

    return int(record["attached"]) > 0


async def db_get_misconception(
    graph: AsyncSession,
    misconception_id: UUID,
) -> MisconceptionResponse | None:
    """
    Returns a misconception along with the concepts
    it is attached to.
    """

    query = """
    MATCH (m:Misconception {id: $misconception_id})

    OPTIONAL MATCH
        (m)-[:CAUSES_CONFUSION_WITH]->
        (c:Concept)

    RETURN
        m.id AS id,
        m.title AS title,
        m.explanation AS explanation,
        m.frequency AS frequency,

        collect({
            id: c.id,
            name: c.name
        }) AS concepts
    """

    result = await graph.run(
        query,
        misconception_id=str(misconception_id),
    )

    record = await result.single()

    if record is None:
        return None

    return MisconceptionResponse.model_validate(record)


async def db_list_misconceptions(
    graph: AsyncSession,
) -> list[MisconceptionResponse]:
    """
    Returns every misconception in the graph.
    """

    query = """
    MATCH (m:Misconception)

    RETURN
        m.id AS id,
        m.title AS title,
        m.explanation AS explanation,
        m.frequency AS frequency

    ORDER BY m.title
    """

    result = await graph.run(query)

    records: list[dict[str, Any]] = await result.data()

    return [MisconceptionResponse.model_validate(record) for record in records]


async def db_patch_misconception(
    graph: AsyncSession,
    misconception_id: UUID,
    misconception_data: MisconceptionPatch,
) -> MisconceptionResponse | None:
    """
    Updates only the supplied fields of a Misconception node.
    """

    if not misconception_data:
        return await db_get_misconception(graph, misconception_id)

    update_dict = misconception_data.model_dump(exclude_unset=True)
    set_clause = ", ".join(
        f"m.{field} = ${field}" for field in update_dict.keys()
    )

    query = f"""
    MATCH (m:Misconception {{id: $misconception_id}})

    SET {set_clause}

    RETURN
        m.id AS id,
        m.user_id AS user_id,
        m.title AS title,
        m.explanation AS explanation,
        m.concept_ids AS concept_ids,
        m.frequency AS frequency,
        m.created_at AS created_at
    """

    params = {
        "misconception_id": str(misconception_id),
        **update_dict,
    }

    result = await graph.run(query, **params)

    record = await result.single()

    if record is None:
        return None

    return MisconceptionResponse.model_validate(record.data())


async def db_delete_misconception(
    graph: AsyncSession,
    misconception_id: UUID,
) -> bool:
    """
    Deletes a misconception node and all of its relationships.
    """

    query = """
    MATCH (m:Misconception {id: $misconception_id})

    WITH m, COUNT(m) AS exists

    DETACH DELETE m

    RETURN exists
    """

    result = await graph.run(
        query,
        misconception_id=str(misconception_id),
    )

    record = await result.single()

    if record is None:
        return False

    return int(record["exists"]) > 0


async def db_remove_misconception_from_concept(
    graph: AsyncSession,
    misconception_id: UUID,
    concept_id: UUID,
) -> bool:
    """
    Removes the CAUSES_CONFUSION_WITH relationship between
    a misconception and a concept.
    """

    query = """
    MATCH
        (m:Misconception {id: $misconception_id})
        -[r:CAUSES_CONFUSION_WITH]->
        (c:Concept {id: $concept_id})

    DELETE r

    RETURN COUNT(*) AS deleted
    """

    result = await graph.run(
        query,
        misconception_id=str(misconception_id),
        concept_id=str(concept_id),
    )

    record = await result.single()

    if record is None:
        return False

    return int(record["deleted"]) > 0


async def db_misconception_exists(
    graph: AsyncSession,
    misconception_id: UUID,
) -> bool:
    """
    Returns whether a misconception exists.
    """

    query = """
    MATCH (m:Misconception {id: $misconception_id})

    RETURN COUNT(m) > 0 AS exists
    """

    result = await graph.run(
        query,
        misconception_id=str(misconception_id),
    )

    record = await result.single()

    if record is None:
        return False

    return bool(record["exists"])
