from uuid import UUID

from pydantic import BaseModel


class GraphNode(BaseModel):
    id: UUID
    label: str
    node_type: str
    metadata: dict | None = None


class GraphEdge(BaseModel):
    source: UUID
    target: UUID
    relationship: str
    weight: float | None = None
    confidence: float | None = None


class ConceptGraphResponse(BaseModel):
    nodes: list[GraphNode]
    edges: list[GraphEdge]


class LearningPathResponse(BaseModel):
    path: list[GraphNode]
    difficulty_score: float
    estimated_time: float
