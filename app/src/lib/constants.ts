function normalizeUrl(value: string | undefined): string {
  const raw = value?.toString().trim() ?? "";
  if (!raw) return "";
  const cleaned = raw.replace(/\/+$|\s+/g, "");
  if (/^https?:\/\//i.test(cleaned)) {
    return cleaned.replace(/\/+$/g, "");
  }
  if (/^[^/:]+(:\d+)?$/.test(cleaned)) {
    return `http://${cleaned}`;
  }
  return cleaned;
}

const rawApiUrl =
  process.env.NEXT_PUBLIC_API_URL;
const normalizedUrl = normalizeUrl(rawApiUrl);

if (!normalizedUrl) {
  throw new Error(
    "Missing or invalid API base URL. Set NEXT_PUBLIC_API_URL to an absolute URL."
  );
}

export const $API_URL = normalizedUrl;

export function buildApiUrl(path: string) {
  if (/^https?:\/\//i.test(path)) {
    return path;
  }

  const cleanedPath = path.startsWith("/") ? path : `/${path}`;
  return `${$API_URL}${cleanedPath}`;
}

export const $SESSION_COOKIE = "explainatory_session";

export const NAV_ITEMS = [
  { href: "/dashboard", label: "Overview" },
  { href: "/dashboard/sessions", label: "Sessions" },
  { href: "/dashboard/concepts", label: "Concepts" },
  { href: "/dashboard/graph", label: "Graph" },
  { href: "/dashboard/mastery", label: "Mastery" },
  { href: "/dashboard/misconceptions", label: "Misconceptions" },
  { href: "/dashboard/profile", label: "Profile" },
] as const;
