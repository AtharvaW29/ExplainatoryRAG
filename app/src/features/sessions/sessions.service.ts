import { apiJson, apiJsonOrNull } from "@/lib/api";
import type {
  ExplanationSession,
  ExplanationSessionCreate,
  ExplanationSessionHistory,
  UUID,
} from "@/types/api";

export async function listSessions(): Promise<ExplanationSessionHistory> {
  const history = await apiJsonOrNull<ExplanationSessionHistory>(
    "/explanation_sessions",
  );
  return history ?? { sessions: [] };
}

export async function getSession(
  sessionId: UUID,
): Promise<ExplanationSession | null> {
  return apiJsonOrNull<ExplanationSession>(
    `/explanation_sessions/${sessionId}`,
  );
}

export async function createSession(
  payload: ExplanationSessionCreate,
): Promise<boolean> {
  return apiJson<boolean>("/explanation_sessions", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}
