import { getScenarios } from "@/lib/api";
import { isoToFlag, cn } from "@/lib/utils";
import Link from "next/link";
import { notFound } from "next/navigation";

interface PageProps {
  params: Promise<{ slug: string }>;
}

export default async function ScenarioPage({ params }: PageProps) {
  const { slug } = await params;
  const scenarios = await getScenarios();
  const s = scenarios.find((x) => x.slug === slug);
  if (!s) notFound();

  return (
    <div className="space-y-6">
      <header className="border-b border-line pb-4">
        <div className="flex items-center gap-3">
          <span
            className={cn(
              "pill text-base",
              s.probability > 0.5 && "pill-bad",
              s.probability > 0.25 && s.probability <= 0.5 && "pill-warn",
              s.probability <= 0.25 && "pill-good"
            )}
          >
            P {(s.probability * 100).toFixed(0)}%
          </span>
          <h1 className="text-2xl text-ink">{s.name}</h1>
        </div>
        <p className="mt-2 text-ink-muted">{s.description}</p>
        <div className="mt-3 text-2xs text-ink-subtle">
          Triggered {new Date(s.triggered_at).toLocaleString()}
          {" · "}
          <Link href={s.methodology_url} className="underline hover:text-ink">methodology</Link>
        </div>
      </header>

      <section className="grid grid-cols-1 gap-4 md:grid-cols-3">
        <div className="tile md:col-span-2">
          <div className="tile-h mb-1">Trigger conditions</div>
          <div className="font-mono text-sm text-ink-muted whitespace-pre-wrap">
            {s.trigger_summary}
          </div>
        </div>
        <div className="tile">
          <div className="tile-h mb-1">Probability</div>
          <div className="num text-3xl text-ink">{(s.probability * 100).toFixed(0)}%</div>
          <div className="mt-1 text-2xs text-ink-subtle">
            Bayesian rollup over triggered conditions
          </div>
        </div>
      </section>

      <section>
        <h2 className="mb-2 font-mono text-sm uppercase tracking-widest text-ink-muted">
          Affected countries
        </h2>
        <div className="flex flex-wrap gap-2">
          {s.affected_countries.map((c) => (
            <Link
              key={c}
              href={`/countries/${c}`}
              className="rounded-sm border border-line bg-bg-elevated px-3 py-2 text-sm hover:border-line-strong"
            >
              <span className="mr-1">{isoToFlag(c)}</span>
              <span className="font-mono">{c}</span>
            </Link>
          ))}
        </div>
      </section>

      <section>
        <h2 className="mb-2 font-mono text-sm uppercase tracking-widest text-ink-muted">
          Affected indicators
        </h2>
        <div className="flex flex-wrap gap-2">
          {s.affected_indicators.map((i) => (
            <Link
              key={i}
              href={`/indicators/${i}`}
              className="pill-info text-sm"
            >
              {i}
            </Link>
          ))}
        </div>
      </section>

      {s.narrative_block && (
        <section className="rounded-sm border border-line bg-bg-elevated p-4">
          <div className="tile-h mb-2">Narrative</div>
          <div className="font-serif text-base leading-relaxed text-ink">
            {s.narrative_block}
          </div>
        </section>
      )}
    </div>
  );
}
