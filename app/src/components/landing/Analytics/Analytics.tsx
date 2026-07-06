const metrics = [
  { label: "Sessions started", value: "16" },
  { label: "Concepts tracked", value: "42" },
  { label: "Feedback responses", value: "8" },
];

export function Analytics() {
  return (
    <section className="bg-slate-950 py-16 px-6 text-white sm:px-8 lg:px-10">
      <div className="mx-auto max-w-7xl">
        <div className="grid gap-10 lg:grid-cols-[0.95fr_1.05fr] lg:items-center">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.24em] text-emerald-300">Insights</p>
            <h2 className="mt-3 text-3xl font-semibold tracking-tight text-white sm:text-4xl">
              Measure progress and learning momentum.
            </h2>
            <p className="mt-6 max-w-xl text-base leading-7 text-slate-300">
              Use mocked analytics now while preserving the ability to plug in real learner data and evaluation metrics later.
            </p>
          </div>
          <div className="grid gap-4 sm:grid-cols-3">
            {metrics.map((metric) => (
              <div key={metric.label} className="rounded-3xl bg-white/10 p-6">
                <p className="text-3xl font-semibold text-white">{metric.value}</p>
                <p className="mt-2 text-sm text-slate-300">{metric.label}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
