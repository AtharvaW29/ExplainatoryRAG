export function Pipeline() {
  const steps = [
    {
      title: "Prepare knowledge sources",
      description:
        "Capture the topic, source documents, and learner goals in a single, reusable model.",
    },
    {
      title: "Retrieve meaningful context",
      description:
        "Simulate semantic search and contextual lookup so explanation generation stays grounded.",
    },
    {
      title: "Generate with clarity",
      description:
        "Produce repeatable explanations and surface supporting reasoning for every learner interaction.",
    },
  ];

  return (
    <section className="bg-white py-16 px-6 sm:px-8 lg:px-10">
      <div className="mx-auto max-w-7xl">
        <div className="grid gap-10 lg:grid-cols-[0.9fr_1.1fr] lg:items-center">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.24em] text-slate-500">Pipeline</p>
            <h2 className="mt-3 text-3xl font-semibold tracking-tight text-slate-950 sm:text-4xl">
              A frontend-ready research pipeline for explanations.
            </h2>
            <p className="mt-6 max-w-xl text-base leading-7 text-slate-600">
              Every step is designed so mock implementations behave like real backend services, making it easy to swap in real retrieval, embeddings, and LLM calls later.
            </p>
          </div>
          <div className="grid gap-4">
            {steps.map((step) => (
              <div key={step.title} className="rounded-3xl border border-slate-200 bg-slate-50 p-6 shadow-sm">
                <p className="text-sm font-semibold text-slate-900">{step.title}</p>
                <p className="mt-3 text-sm leading-6 text-slate-600">{step.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
