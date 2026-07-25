export function formatDate(iso: string): string {
  return new Intl.DateTimeFormat("en-US", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(iso));
}

export function formatPercent(value: number): string {
  return `${Math.round(value * 100)}%`;
}

export function formatScore(value: number | null | undefined): string {
  if (value == null) return "—";
  return value.toFixed(2);
}
