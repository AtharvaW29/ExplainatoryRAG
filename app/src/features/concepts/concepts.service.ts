import { apiJson } from "@/lib/api";
import type {
  Concept,
  ConceptCreate,
  ConceptPatch,
  ConceptSummary,
  UUID,
} from "@/types/api";

export async function listConcepts(): Promise<ConceptSummary[]> {
  return apiJson<ConceptSummary[]>("/concept");
}

export async function getConcept(conceptId: UUID): Promise<Concept> {
  return apiJson<Concept>(`/concept/${conceptId}`);
}

export async function getConceptByName(name: string): Promise<Concept> {
  return apiJson<Concept>(`/concept/name/${encodeURIComponent(name)}`);
}

export async function createConcept(payload: ConceptCreate): Promise<Concept> {
  return apiJson<Concept>("/concept", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function updateConcept(
  conceptId: UUID,
  payload: ConceptPatch,
): Promise<ConceptPatch> {
  return apiJson<ConceptPatch>(`/concept/${conceptId}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export async function deleteConcept(
  conceptId: UUID,
  isDeleted = true,
): Promise<void> {
  await apiJson<void>(`/concept/${conceptId}?isdeleted=${isDeleted}`, {
    method: "DELETE",
  });
}
