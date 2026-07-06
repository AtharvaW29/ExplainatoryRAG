import { DashboardHeader } from "./DashboardHeader";
import { OverviewCard, SessionList } from "@/components/dashboard";
import { listSessions } from "@/features/sessions";

export default async function DashboardPage() {
  const history = await listSessions();

  return (
    <main className="min-h-screen bg-slate-50 px-6 py-10 sm:px-8 lg:px-10">
      <div className="mx-auto max-w-7xl space-y-8">
        <DashboardHeader />

        <section className="grid gap-6 lg:grid-cols-3">
          <OverviewCard
            title="Active sessions"
            value={String(history.sessions.length)}
            detail="Topics you have started exploring."
          />
          <OverviewCard
            title="Recent activity"
            value="Live"
            detail="Your workspace is ready for guided explanations."
          />
          <OverviewCard
            title="Next milestone"
            value="Review"
            detail="Track concept mastery and misconception insights."
          />
        </section>

        <section className="space-y-6">
          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <p className="text-sm font-semibold uppercase tracking-[0.26em] text-slate-500">Explanation sessions</p>
                <p className="mt-2 text-sm text-slate-600">
                  Sessions are loaded from the session service. A real backend will provide full history and detail.
                </p>
              </div>
            </div>
            <div className="mt-6">
              <SessionList sessions={history.sessions} />
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
