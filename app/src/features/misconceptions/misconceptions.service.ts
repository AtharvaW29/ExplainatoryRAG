import { apiJson } from "@/lib/api";
import type {
  Misconception,
  MisconceptionCreate,
  MisconceptionPatch,
  UUID,
} from "@/types/api";

export async function listMisconceptions(): Promise<Misconception[]> {
  return apiJson<Misconception[]>("/misconceptions/");
}

export async function getMisconception(
  misconceptionId: UUID,
): Promise<Misconception> {
  return apiJson<Misconception>(`/misconceptions/${misconceptionId}`);
}

export async function createMisconception(
  payload: MisconceptionCreate,
): Promise<Misconception> {
  return apiJson<Misconception>("/misconceptions/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function updateMisconception(
  misconceptionId: UUID,
  payload: MisconceptionPatch,
): Promise<Misconception> {
  return apiJson<Misconception>(`/misconceptions/${misconceptionId}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export async function deleteMisconception(
  misconceptionId: UUID,
): Promise<void> {
  await apiJson<void>(`/misconceptions/${misconceptionId}`, {
    method: "DELETE",
  });
}

export async function attachConcepts(
  misconceptionId: UUID,
  conceptIds: UUID[],
): Promise<boolean> {
  const params = conceptIds
    .map((id) => `concept_ids=${encodeURIComponent(id)}`)
    .join("&");
  return apiJson<boolean>(
    `/misconceptions/${misconceptionId}/attach-concepts?${params}`,
    { method: "PATCH" },
  );
}
