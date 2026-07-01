from uuid import UUID

from neo4j import AsyncSession

from src.schemas.graph import (
    ConceptDetail,
    ConceptGraphResponse,
    ConceptNeighborhoodResponse,
    GraphEdge,
    GraphNode,
    LearningPathResponse,
)


async def db_get_concept_neighborhood(
    graph: AsyncSession, concept_id: UUID
) -> ConceptNeighborhoodResponse | None:
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
    result = await graph.run(
        query,
        concept_id=str(concept_id),
    )

    record = await result.single()

    if record is None:
        return None

    return ConceptNeighborhoodResponse(**record)


async def db_expand_graph(
    graph: AsyncSession,
    concept_id: UUID,
) -> ConceptGraphResponse:
    """
    Expands the graph around a concept.

    Traverses prerequisite and related relationships.
    """
    query = """
    MATCH p=(c:Concept {id:$concept_id})
        -[:PREREQUISITE_OF|RELATED_TO*1..$depth]-
        (neighbor)

    RETURN p
    """

    result = await graph.run(
        query,
        concept_id=str(concept_id),
    )
    nodes_map = {}
    edges_list = []
    seen_edges = set()

    async for record in result:
        path = record["p"]

        # Extract Nodes
        for node in path.nodes:
            node_id = node.get("id")
            if node_id and node_id not in nodes_map:
                nodes_map[node_id] = GraphNode(
                    id=UUID(node_id),
                    label=node.get("name", "Unknown Concept"),
                    node_type=list(node.labels)[0]
                    if node.labels
                    else "Concept",
                    metadata=dict(node),
                )

        # Extract Edges
        for rel in path.relationships:
            start_id = rel.start_node.get("id")
            end_id = rel.end_node.get("id")

            if not start_id or not end_id:
                continue

            edge_signature = (start_id, end_id, rel.type)
            if edge_signature not in seen_edges:
                seen_edges.add(edge_signature)
                edges_list.append(
                    GraphEdge(
                        source=UUID(start_id),
                        target=UUID(end_id),
                        relationship=rel.type,
                        weight=rel.get("weight"),
                        confidence=rel.get("confidence"),
                    )
                )

    return ConceptGraphResponse(
        nodes=list(nodes_map.values()), edges=edges_list
    )


async def db_get_learning_path(
    graph: AsyncSession,
    concept_id: UUID,
) -> LearningPathResponse | None:
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

    records = await result.data()

    path_nodes = [ConceptDetail(**record) for record in records]

    calculated_difficulty = sum((n.difficulty or 0.0) for n in path_nodes)
    calculated_time = len(path_nodes) * 15.0

    return LearningPathResponse(
        path=path_nodes,
        difficulty_score=calculated_difficulty,
        estimated_time=calculated_time,
    )
