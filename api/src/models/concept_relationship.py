import re
from typing import Any
from uuid import UUID

from neo4j import AsyncSession

from src.schemas.concept_relationship import (
    ConceptNodeCreate,
    ConceptRelationshipExists,
    ConceptRelationshipRemove,
    RelatedConceptResponse,
)

RELATIONSHIP_REGEX = re.compile(r"^[a-zA-Z0-9_]+$")


async def db_add_concept(
    graph: AsyncSession,
    payload: ConceptNodeCreate,
) -> bool:
    query = """
    CREATE (c:Concept {
        id: $id,
        name: $name,
        description: $description,
        difficulty: $difficulty,
        domain: $domain,
        type: $type
    })
    RETURN c.id AS id
    """
    result = await graph.run(
        query,
        id=str(payload.id),
        name=payload.name,
        description=payload.description,
        difficulty=float(payload.difficulty)
        if payload.difficulty is not None
        else None,
        domain=payload.domain,
        type=payload.concepttype,
    )
    record = await result.single()
    return record is not None


async def db_relationship_exists(
    graph: AsyncSession, paylod: ConceptRelationshipExists
) -> bool:
    if not RELATIONSHIP_REGEX.match(paylod.relationship):
        raise ValueError(f"Invalid relationship type: {paylod.relationship}")

    query = f"""
    MATCH (source:Concept {{id: $source_id}})
          -[r:{paylod.relationship}]->
          (target:Concept {{id: $target_id}})
    RETURN COUNT(r) > 0 AS exists
    """
    res = await graph.run(
        query,
        source_id=str(paylod.source_concept_id),
        target_id=str(paylod.target_concept_id),
    )
    record = await res.single()
    if record is None:
        return False
    return bool(record["exists"])


async def db_add_prerequisite(
    graph: AsyncSession,
    concept_id: UUID,
    target_concept_id: UUID,
) -> bool:
    query = """
    MATCH (concept:Concept {id: $concept_id})
    MATCH (target:Concept {id: $target_id})

    MERGE (target)-[:PREREQUISITE_OF]->(concept)

    RETURN concept.id
    """
    res = await graph.run(
        query, concept_id=str(concept_id), target_id=str(target_concept_id)
    )

    record = await res.single()
    return record is not None


async def db_add_related_concept(
    graph: AsyncSession,
    concept_id: UUID,
    target_concept_id: UUID,
) -> bool:
    query = """
    MATCH (a:Concept {id: $concept_id})
    MATCH (b:Concept {id: $target_id})

    MERGE (a)-[:RELATED_TO]->(b)
    MERGE (b)-[:RELATED_TO]->(a)

    RETURN a.id
    """
    res = await graph.run(
        query, concept_id=str(concept_id), target_id=str(target_concept_id)
    )

    record = await res.single()
    return record is not None


async def db_get_prerequisites(
    graph: AsyncSession,
    concept_id: UUID,
) -> list[RelatedConceptResponse]:
    """Returns all prerequisite concepts."""
    query = """
    MATCH (prerequisite:Concept)
          -[:PREREQUISITE_OF]->
          (concept:Concept {id: $concept_id})

    RETURN
        prerequisite.id AS id,
        prerequisite.name AS name,
        prerequisite.description AS description,
        prerequisite.difficulty AS difficulty,
        prerequisite.domain AS domain

    ORDER BY prerequisite.name
    """
    result = await graph.run(
        query,
        concept_id=str(concept_id),
    )

    records: list[dict[str, Any]] = await result.data()
    return [RelatedConceptResponse.model_validate(c) for c in records]


async def db_get_related_concepts(
    graph: AsyncSession,
    concept_id: UUID,
) -> list[RelatedConceptResponse]:
    """Returns all concepts related to a concept."""
    query = """
    MATCH (concept:Concept {id: $concept_id})
          -[:RELATED_TO]->
          (related:Concept)

    RETURN
        related.id AS id,
        related.name AS name,
        related.description AS description,
        related.difficulty AS difficulty,
        related.domain AS domain

    ORDER BY related.name
    """
    result = await graph.run(
        query,
        concept_id=str(concept_id),
    )
    records: list[dict[str, Any]] = await result.data()
    return [RelatedConceptResponse.model_validate(c) for c in records]


async def db_remove_relationship(
    graph: AsyncSession,
    source_concept_id: UUID,
    payload: ConceptRelationshipRemove,
) -> bool:
    """Deletes a relationship between two concepts."""
    if not RELATIONSHIP_REGEX.match(payload.relationship):
        raise ValueError(f"Invalid relationship type: {payload.relationship}")
    query = f"""
    MATCH (a:Concept {{id: $source_id}})
          -[r:{payload.relationship}]->
          (b:Concept {{id: $target_id}})

    DELETE r

    RETURN COUNT(*) AS deleted
    """
    result = await graph.run(
        query,
        source_id=str(source_concept_id),
        target_id=str(payload.target_concept_id),
    )

    record = await result.single()
    if record is None:
        return False

    return int(record["deleted"]) > 0
