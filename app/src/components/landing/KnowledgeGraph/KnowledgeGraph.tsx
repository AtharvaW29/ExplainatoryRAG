const nodes = [
  { label: "Calculus", type: "Concept" },
  { label: "Limits", type: "Prerequisite" },
  { label: "Derivatives", type: "Prerequisite" },
  { label: "Misconceptions", type: "Insight" },
];

export function KnowledgeGraph() {
  return (
    <section className="bg-slate-50 py-16 px-6 sm:px-8 lg:px-10">
      <div className="mx-auto max-w-7xl">
        <div className="grid gap-10 lg:grid-cols-[1.1fr_0.9fr] lg:items-center">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.24em] text-slate-500">Knowledge graph</p>
            <h2 className="mt-3 text-3xl font-semibold tracking-tight text-slate-950 sm:text-4xl">
              Explore relationships between concepts and misconceptions.
            </h2>
            <p className="mt-6 max-w-xl text-base leading-7 text-slate-600">
              The dashboard will surface connected topics and dependencies once retrieval and graph services are integrated.
            </p>
          </div>
          <div className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-sm">
            <div className="space-y-4">
              {nodes.map((node) => (
                <div key={node.label} className="flex items-center justify-between rounded-3xl border border-slate-200 bg-slate-100 px-5 py-4">
                  <div>
                    <p className="text-base font-semibold text-slate-900">{node.label}</p>
                    <p className="text-sm text-slate-600">{node.type}</p>
                  </div>
                  <div className="rounded-full bg-slate-900 px-3 py-1 text-xs font-semibold text-white">
                    {node.type}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
