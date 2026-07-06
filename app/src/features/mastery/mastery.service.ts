import { apiJson } from "@/lib/api";
import type {
  ConceptMastery,
  ConceptMasteryCreate,
  UUID,
} from "@/types/api";

export async function listMastery(userId: UUID): Promise<ConceptMastery[]> {
  return apiJson<ConceptMastery[]>(`/mastery?user_id=${userId}`);
}

export async function getMastery(
  conceptId: UUID,
  userId: UUID,
): Promise<ConceptMastery | null> {
  try {
    return await apiJson<ConceptMastery>(
      `/mastery/${conceptId}?user_id=${userId}`,
    );
  } catch {
    return null;
  }
}

export async function upsertMastery(
  payload: ConceptMasteryCreate,
): Promise<ConceptMastery> {
  return apiJson<ConceptMastery>("/mastery", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}
