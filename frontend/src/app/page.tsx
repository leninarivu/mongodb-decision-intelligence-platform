import { ArrowRight, Database, ShieldCheck, Workflow } from "lucide-react";

import { Button } from "@/components/ui/button";

const capabilities = [
  {
    title: "Decision Workspace",
    description: "Placeholder surface for future workflows, models, and evaluation tools.",
    icon: Workflow,
  },
  {
    title: "MongoDB Foundation",
    description: "Backend wiring includes async MongoDB connectivity and health checks.",
    icon: Database,
  },
  {
    title: "Production Baseline",
    description: "Docker, CI, type checks, linting, and explicit environment configuration.",
    icon: ShieldCheck,
  },
];

export default function Home() {
  return (
    <main className="min-h-screen bg-[radial-gradient(circle_at_top_left,_rgba(16,185,129,0.16),_transparent_34rem),linear-gradient(180deg,_#f8fafc_0%,_#eef2f7_100%)] px-6 py-8 text-slate-950 sm:px-10">
      <section className="mx-auto flex max-w-6xl flex-col gap-12 rounded-[2rem] border border-white/70 bg-white/80 p-8 shadow-2xl shadow-slate-200/70 backdrop-blur md:p-12">
        <nav className="flex items-center justify-between gap-4">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.28em] text-emerald-700">
              MongoDB DIP
            </p>
            <h1 className="mt-2 text-2xl font-semibold tracking-tight sm:text-3xl">
              Decision Intelligence Platform
            </h1>
          </div>
          <Button asChild>
            <a href="/health">
              Health
              <ArrowRight className="h-4 w-4" />
            </a>
          </Button>
        </nav>

        <div className="grid gap-10 lg:grid-cols-[1.1fr_0.9fr] lg:items-end">
          <div className="space-y-6">
            <p className="max-w-3xl text-5xl font-semibold leading-tight tracking-[-0.04em] text-slate-950 sm:text-6xl lg:text-7xl">
              A clean platform shell for decisions, data, and intelligence.
            </p>
            <p className="max-w-2xl text-lg leading-8 text-slate-600">
              This scaffold is ready for product teams to add authenticated workflows,
              API domains, and MongoDB-backed features without reworking the foundation.
            </p>
          </div>

          <div className="rounded-3xl border border-slate-200 bg-slate-950 p-6 text-slate-100 shadow-xl">
            <p className="font-mono text-sm text-emerald-300">system.status</p>
            <div className="mt-6 space-y-4 font-mono text-sm">
              <div className="flex items-center justify-between border-b border-white/10 pb-3">
                <span>frontend</span>
                <span className="text-emerald-300">ready</span>
              </div>
              <div className="flex items-center justify-between border-b border-white/10 pb-3">
                <span>backend</span>
                <span className="text-emerald-300">/health</span>
              </div>
              <div className="flex items-center justify-between">
                <span>database</span>
                <span className="text-emerald-300">mongodb</span>
              </div>
            </div>
          </div>
        </div>

        <div className="grid gap-4 md:grid-cols-3">
          {capabilities.map((item) => {
            const Icon = item.icon;

            return (
              <article key={item.title} className="rounded-3xl border border-slate-200 bg-white p-6">
                <Icon className="h-6 w-6 text-emerald-700" />
                <h2 className="mt-5 text-xl font-semibold tracking-tight">{item.title}</h2>
                <p className="mt-3 leading-7 text-slate-600">{item.description}</p>
              </article>
            );
          })}
        </div>
      </section>
    </main>
  );
}
