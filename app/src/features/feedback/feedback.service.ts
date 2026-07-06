import { apiJson, apiJsonOrNull } from "@/lib/api";
import type { Feedback, FeedbackCreate, FeedbackPatch, UUID } from "@/types/api";

export async function getFeedback(
  explanationId: UUID,
): Promise<Feedback | null> {
  return apiJsonOrNull<Feedback>(`/feedback/${explanationId}`);
}

export async function createFeedback(
  payload: FeedbackCreate,
): Promise<boolean> {
  return apiJson<boolean>("/feedback", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function updateFeedback(
  explanationId: UUID,
  payload: FeedbackPatch,
): Promise<boolean> {
  return apiJson<boolean>(`/feedback/${explanationId}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}
