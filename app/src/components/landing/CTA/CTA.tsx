import Link from "next/link";

export function CTA() {
  return (
    <section className="bg-slate-950 py-16 px-6 text-white sm:px-8 lg:px-10">
      <div className="mx-auto flex max-w-7xl flex-col gap-6 rounded-[2rem] border border-slate-800 bg-slate-900/95 p-10 shadow-2xl">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.3em] text-emerald-300">Ready to explore</p>
          <h2 className="mt-3 text-3xl font-semibold tracking-tight text-white sm:text-4xl">
            Start building explanations and verify your learning journey.
          </h2>
        </div>
        <div className="flex flex-col gap-3 sm:flex-row">
          <Link
            href="/dashboard"
            className="inline-flex items-center justify-center rounded-full bg-white px-6 py-3 text-sm font-semibold text-slate-950 transition hover:bg-slate-100"
          >
            Go to dashboard
          </Link>
          <Link
            href="/login"
            className="inline-flex items-center justify-center rounded-full border border-slate-700 bg-slate-900 px-6 py-3 text-sm font-semibold text-white transition hover:bg-slate-800"
          >
            Sign in
          </Link>
        </div>
      </div>
    </section>
  );
}
