import { FeatureCard } from "../feature-card";

const featureCards = [
  {
    title: "Guided explanations",
    description:
      "Turn complex topics into step-by-step explanations that feel like tutoring, not a search result.",
    icon: "✦",
  },
  {
    title: "Concept graph insight",
    description:
      "Explore prerequisite relationships and misconceptions in a connected view that helps learners understand the whole map.",
    icon: "◎",
  },
  {
    title: "Progress-aware feedback",
    description:
      "Track mastery, collect human feedback, and refine the experience over time with a dependable learning loop.",
    icon: "↺",
  },
];

export function FeatureGrid() {
  return (
    <section className="bg-white py-16 px-6 sm:px-8 lg:px-10">
      <div className="mx-auto max-w-7xl">
        <div className="max-w-2xl">
          <p className="text-sm font-semibold uppercase tracking-[0.24em] text-slate-500">Capabilities</p>
          <h2 className="mt-3 text-3xl font-semibold tracking-tight text-slate-950 sm:text-4xl">
            Everything learners need, arranged around real understanding.
          </h2>
        </div>
        <div className="mt-10 grid gap-6 md:grid-cols-3">
          {featureCards.map((feature) => (
            <FeatureCard key={feature.title} {...feature} />
          ))}
        </div>
      </div>
    </section>
  );
}
