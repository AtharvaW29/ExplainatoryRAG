import type { ExplanationSessionHistoryItem } from "@/types/api";

interface SessionListProps {
  sessions: ExplanationSessionHistoryItem[];
}

export function SessionList({ sessions }: SessionListProps) {
  if (sessions.length === 0) {
    return (
      <div className="rounded-3xl border border-dashed border-slate-300 bg-slate-50 p-8 text-center text-slate-600">
        <p className="text-sm font-semibold">No explanation sessions yet</p>
        <p className="mt-2 text-sm">Start a new topic to track your reasoning and feedback journey.</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {sessions.map((session) => (
        <div
          key={session.id}
          className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm"
        >
          <p className="text-base font-semibold text-slate-900">{session.topic}</p>
          <p className="mt-2 text-sm text-slate-600">Created at {new Date(session.created_at).toLocaleString()}</p>
        </div>
      ))}
    </div>
  );
}
