import { apiJson, apiJsonOrNull } from "@/lib/api";
import type { User } from "@/types/api";

export async function getCurrentUser(): Promise<User> {
  return apiJson<User>("/auth/me");
}
