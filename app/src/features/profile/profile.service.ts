import { apiJson, apiJsonOrNull } from "@/lib/api";
import type {
  LearnerPreferences,
  LearnerProfile,
  LearnerProfileCreate,
  LearnerProfilePatch,
  UUID,
} from "@/types/api";

export async function getProfile(userId: UUID): Promise<LearnerProfile | null> {
  return apiJsonOrNull<LearnerProfile>(`/learner_profile/${userId}`);
}

export async function getPreferences(
  userId: UUID,
): Promise<LearnerPreferences | null> {
  return apiJsonOrNull<LearnerPreferences>(
    `/learner_profile/${userId}/preferences`,
  );
}

export async function createProfile(
  payload: LearnerProfileCreate,
): Promise<LearnerProfile> {
  return apiJson<LearnerProfile>("/learner_profile", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function updateProfile(
  userId: UUID,
  payload: LearnerProfilePatch,
): Promise<LearnerProfile> {
  return apiJson<LearnerProfile>(`/learner_profile/${userId}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}
