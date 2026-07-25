import { cookies } from "next/headers";
import { $SESSION_COOKIE } from "./constants";

export async function getSessionToken(): Promise<string | undefined> {
  const cookieStore = await cookies();
  return cookieStore.get($SESSION_COOKIE)?.value;
}
