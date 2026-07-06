import Link from "next/link";

export function Hero() {
  return (
    <section className="mx-auto max-w-7xl px-6 py-16 sm:px-8 lg:px-10">
      <div className="grid gap-12 lg:grid-cols-[1.2fr_0.8fr] lg:items-center">
        <div>
          <p className="mb-4 inline-flex rounded-full border border-slate-200 bg-slate-100 px-4 py-2 text-xs font-semibold uppercase tracking-[0.3em] text-slate-700">
            ExplainatoryRAG
          </p>
          <h1 className="max-w-3xl text-4xl font-semibold tracking-tight text-slate-950 sm:text-5xl">
            A research-grade learning workspace built around explanations, concept graphs, and feedback.
          </h1>
          <p className="mt-6 max-w-2xl text-lg leading-8 text-slate-600">
            Start with a clear learning path, explore concept relationships, and track mastery through a mock-ready frontend that is designed for future real backend integration.
          </p>
          <div className="mt-8 flex flex-col gap-3 sm:flex-row">
            <Link
              href="/dashboard"
              className="inline-flex items-center justify-center rounded-full bg-slate-900 px-6 py-3 text-sm font-semibold text-white transition hover:bg-slate-700"
            >
              Open dashboard
            </Link>
            <Link
              href="/login"
              className="inline-flex items-center justify-center rounded-full border border-slate-300 bg-white px-6 py-3 text-sm font-semibold text-slate-800 transition hover:border-slate-400"
            >
              Sign in
            </Link>
          </div>
        </div>

        <div className="rounded-[2rem] border border-slate-200 bg-slate-950 p-8 text-white shadow-xl ring-1 ring-slate-900/5 sm:p-10">
          <div className="flex items-center justify-between rounded-3xl bg-slate-800/90 p-5">
            <div>
              <p className="text-sm uppercase tracking-[0.28em] text-slate-400">Session preview</p>
              <p className="mt-3 text-xl font-semibold">Session analytics</p>
            </div>
            <span className="rounded-full bg-emerald-100 px-3 py-1 text-sm font-semibold text-emerald-900">
              Beta
            </span>
          </div>
          <div className="mt-8 space-y-5">
            <div className="rounded-3xl bg-slate-900/80 p-5">
              <p className="text-sm uppercase tracking-[0.2em] text-slate-500">Topic</p>
              <p className="mt-2 text-lg font-semibold text-white">Neural networks</p>
            </div>
            <div className="grid gap-4 sm:grid-cols-2">
              <div className="rounded-3xl bg-slate-900/80 p-5">
                <p className="text-sm uppercase tracking-[0.2em] text-slate-500">Clarity</p>
                <p className="mt-2 text-3xl font-semibold text-white">92%</p>
              </div>
              <div className="rounded-3xl bg-slate-900/80 p-5">
                <p className="text-sm uppercase tracking-[0.2em] text-slate-500">Feedback</p>
                <p className="mt-2 text-3xl font-semibold text-white">4.8 / 5</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
