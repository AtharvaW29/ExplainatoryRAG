export function Architecture() {
  return (
    <section className="bg-slate-50 py-16 px-6 sm:px-8 lg:px-10">
      <div className="mx-auto max-w-7xl">
        <div className="grid gap-10 lg:grid-cols-[0.9fr_1.1fr] lg:items-center">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.24em] text-slate-500">Architecture</p>
            <h2 className="mt-3 text-3xl font-semibold tracking-tight text-slate-950 sm:text-4xl">
              Mock-ready API architecture with clean separation for frontend and backend.
            </h2>
            <p className="mt-6 max-w-xl text-base leading-7 text-slate-600">
              The frontend is built to behave exactly as if the backend services already exist. Every feature is isolated so mock implementations can be swapped for real APIs later with minimal change.
            </p>
          </div>
          <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
            <ul className="space-y-4">
              {[
                "Feature modules with dedicated services",
                "Shared API wrapper for request handling",
                "UI-only components with state managed in hooks/services",
                "Replacing mocks requires only a configuration change",
              ].map((item) => (
                <li key={item} className="flex gap-3">
                  <span className="mt-1 h-2.5 w-2.5 rounded-full bg-indigo-500" />
                  <span className="text-sm leading-6 text-slate-700">{item}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
}
