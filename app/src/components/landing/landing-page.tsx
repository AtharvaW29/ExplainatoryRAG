import { Navbar } from "./Navbar";
import { Hero } from "./Hero";
import { FeatureGrid } from "./FeatureGrid";
import { Architecture } from "./Architecture";
import { Pipeline } from "./Pipeline";
import { Analytics } from "./Analytics";
import { KnowledgeGraph } from "./KnowledgeGraph";
import { CTA } from "./CTA";
import { Footer } from "./Footer";

export function LandingPage() {
  return (
    <main className="min-h-screen bg-slate-50 text-slate-900">
      <Navbar />
      <Hero />
      <FeatureGrid />
      <Architecture />
      <Pipeline />
      <KnowledgeGraph />
      <Analytics />
      <CTA />
      <Footer />
    </main>
  );
}
