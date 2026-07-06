import { apiJson } from "@/lib/api";
import type {
  ConceptNodeCreate,
  ConceptRelationshipCreate,
  RelatedConcept,
  UUID,
} from "@/types/api";

export async function addConceptNode(
  payload: ConceptNodeCreate,
): Promise<boolean> {
  return apiJson<boolean>("/concept-relationship/add-concept", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function addPrerequisite(
  conceptId: UUID,
  targetConceptId: UUID,
): Promise<boolean> {
  const body: ConceptRelationshipCreate = {
    target_concept_id: targetConceptId,
  };
  return apiJson<boolean>(
    `/concept-relationship/add-prerequisite?concept_id=${conceptId}`,
    { method: "POST", body: JSON.stringify(body) },
  );
}

export async function addRelatedConcept(
  conceptId: UUID,
  targetConceptId: UUID,
): Promise<boolean> {
  const body: ConceptRelationshipCreate = {
    target_concept_id: targetConceptId,
  };
  return apiJson<boolean>(
    `/concept-relationship/add-related-concept?concept_id=${conceptId}`,
    { method: "POST", body: JSON.stringify(body) },
  );
}

export async function getPrerequisites(
  conceptId: UUID,
): Promise<RelatedConcept[]> {
  return apiJson<RelatedConcept[]>(
    `/concept-relationship/get-prerequisites?concept_id=${conceptId}`,
  );
}

export async function getRelatedConcepts(
  conceptId: UUID,
): Promise<RelatedConcept[]> {
  return apiJson<RelatedConcept[]>(
    `/concept-relationship/get-related-concepts?concept_id=${conceptId}`,
  );
}
