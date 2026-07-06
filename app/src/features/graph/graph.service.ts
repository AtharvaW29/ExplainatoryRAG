import { apiJson } from "@/lib/api";
import type {
  ConceptGraph,
  ConceptNeighborhood,
  LearningPath,
  UUID,
} from "@/types/api";

export async function getConceptNeighborhood(
  conceptId: UUID,
): Promise<ConceptNeighborhood> {
  return apiJson<ConceptNeighborhood>(
    `/graph/concept-neighborhood/${conceptId}`,
  );
}

export async function expandGraph(conceptId: UUID): Promise<ConceptGraph> {
  return apiJson<ConceptGraph>(`/graph/expand-graph/${conceptId}`);
}

export async function getLearningPath(
  conceptId: UUID,
): Promise<LearningPath> {
  return apiJson<LearningPath>(`/graph/learning-path/${conceptId}`);
}
