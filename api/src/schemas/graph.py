from uuid import UUID

from pydantic import BaseModel, Field


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


# Query models
class EntityReference(BaseModel):
    id: UUID
    name: str | None = None
    title: str | None = None


class ConceptDetail(BaseModel):
    id: UUID
    name: str
    description: str | None = None
    difficulty: float | None = None
    domain: str | None = None


class ConceptNeighborhoodResponse(BaseModel):
    concept: ConceptDetail
    prerequisites: list[EntityReference] = Field(default_factory=list)
    related: list[EntityReference] = Field(default_factory=list)
    misconceptions: list[EntityReference] = Field(default_factory=list)


# Aggregated models
class LearningPathResponse(BaseModel):
    path: list[ConceptDetail]
    difficulty_score: float = 0.0
    estimated_time: float = 0.0
