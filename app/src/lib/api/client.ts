import { buildApiUrl } from "../constants";
import { getSessionToken } from "../session";

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
    public detail?: unknown,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

export async function apiFetch(
  path: string,
  init: RequestInit = {},
): Promise<Response> {
  const token = await getSessionToken();
  const headers = new Headers(init.headers);

  if (init.body && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }

  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  return fetch(buildApiUrl(path), {
    ...init,
    headers,
    cache: "no-store",
  });
}

export async function apiJson<T>(
  path: string,
  init?: RequestInit,
): Promise<T> {
  const response = await apiFetch(path, init);

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    const message =
      (error as { detail?: string }).detail ??
      (error as { message?: string }).message ??
      `Request failed (${response.status})`;
    throw new ApiError(response.status, message, error);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}

export async function apiJsonOrNull<T>(
  path: string,
  init?: RequestInit,
): Promise<T | null> {
  try {
    return await apiJson<T>(path, init);
  } catch (error) {
    if (error instanceof ApiError && error.status === 404) {
      return null;
    }
    throw error;
  }
}
