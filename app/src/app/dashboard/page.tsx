import { StartNewSessionButton } from "@/components/chat";
import { OverviewCard, SessionList } from "@/components/dashboard";
import { listSessions } from "@/features/sessions";
import { DashboardHeader } from "./DashboardHeader";

export default async function DashboardPage() {
  const history = await listSessions();

  return (
    <main className="min-h-dvh px-4 py-8 sm:px-6 lg:px-8 lg:py-10">
      <div className="mx-auto max-w-7xl space-y-8">
        <DashboardHeader />

        <section
          aria-label="Dashboard overview"
          className="grid gap-4 md:grid-cols-2 lg:grid-cols-3 lg:gap-6"
        >
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

        <section aria-labelledby="sessions-heading">
          <div className="overflow-hidden rounded-3xl border border-zinc-200/70 bg-zinc-50 shadow-sm dark:border-zinc-800/70 dark:bg-[#171717]">
            <div className="flex flex-col gap-5 border-b border-zinc-200/70 p-6 dark:border-zinc-800/70 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <h2
                  id="sessions-heading"
                  className="text-sm font-semibold uppercase tracking-[0.22em] text-zinc-500 dark:text-zinc-400"
                >
                  Explanation sessions
                </h2>

                <p className="mt-2 max-w-2xl text-sm leading-6 text-zinc-600 dark:text-zinc-400">
                  Sessions are loaded from the session service. A real backend
                  will provide full history and detail.
                </p>
              </div>

              <div className="shrink-0">
                <StartNewSessionButton />
              </div>
            </div>

            <div className="p-4 sm:p-6">
              <SessionList sessions={history.sessions} />
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
