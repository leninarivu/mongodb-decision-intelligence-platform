const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export default function HealthPage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-950 px-6 py-12 text-slate-100">
      <section className="w-full max-w-2xl rounded-3xl border border-white/10 bg-white/[0.03] p-8 shadow-2xl">
        <p className="font-mono text-sm uppercase tracking-[0.28em] text-emerald-300">Frontend Health</p>
        <h1 className="mt-4 text-4xl font-semibold tracking-tight">Application shell is running.</h1>
        <dl className="mt-8 grid gap-4 sm:grid-cols-2">
          <div className="rounded-2xl bg-white/[0.06] p-4">
            <dt className="text-sm text-slate-400">Status</dt>
            <dd className="mt-2 font-mono text-emerald-300">ok</dd>
          </div>
          <div className="rounded-2xl bg-white/[0.06] p-4">
            <dt className="text-sm text-slate-400">API Base URL</dt>
            <dd className="mt-2 break-all font-mono text-emerald-300">{apiBaseUrl}</dd>
          </div>
        </dl>
      </section>
    </main>
  );
}
