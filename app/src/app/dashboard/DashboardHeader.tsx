import { LogoutButton } from "@/components/dashboard";

export function DashboardHeader() {
  return (
    <div className="flex flex-col gap-6 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm sm:flex-row sm:items-center sm:justify-between">
      <div>
        <p className="text-sm font-semibold uppercase tracking-[0.24em] text-slate-500">Dashboard</p>
        <h1 className="mt-3 text-3xl font-semibold text-slate-950">Welcome back</h1>
        <p className="mt-2 text-sm text-slate-600">Your explanation sessions and learning progress are waiting.</p>
      </div>
      <LogoutButton />
    </div>
  );
}
