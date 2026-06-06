import { ForecastBandsChart } from "@/components/charts/ForecastBandsChart";
import Link from "next/link";
import { cn, fmt, isoToFlag } from "@/lib/utils";

// Stub forecast band history — in production, fetched from /v1/forecasts/{id}/history
const HISTORY = [
  { date: "2024-Q1", p10: 1.2, p50: 1.9, p90: 2.6, consensus: 2.1, actual: 1.6 },
  { date: "2024-Q2", p10: 1.4, p50: 2.0, p90: 2.7, consensus: 2.2, actual: 2.3 },
  { date: "2024-Q3", p10: 1.6, p50: 2.1, p90: 2.8, consensus: 2.3, actual: 2.8 }, // miss high
  { date: "2024-Q4", p10: 1.7, p50: 2.0, p90: 2.6, consensus: 2.2, actual: 2.5 },
  { date: "2025-Q1", p10: 1.6, p50: 1.9, p90: 2.4, consensus: 2.1, actual: 1.4 }, // miss low
  { date: "2025-Q2", p10: 1.5, p50: 1.8, p90: 2.3, consensus: 2.0, actual: 2.0 },
  { date: "2025-Q3", p10: 1.4, p50: 1.7, p90: 2.2, consensus: 1.9, actual: 1.8 },
  { date: "2025-Q4", p10: 1.5, p50: 1.8, p90: 2.2, consensus: 1.9, actual: 2.0 },
  { date: "2026-Q1", p10: 1.4, p50: 1.8, p90: 2.4 },
  { date: "2026-Q2", p10: 1.3, p50: 1.9, p90: 2.7 },
  { date: "2026-Q3", p10: 1.1, p50: 1.9, p90: 2.9 },
  { date: "2026-Q4", p10: 0.9, p50: 1.9, p90: 3.1 },
];

interface PageProps {
  params: Promise<{ id: string }>;
}

export default async function ForecastDetailPage({ params }: PageProps) {
  const { id } = await params;
  // Stub — in production decode the id into (vintage_id, country, indicator, horizon)
  const meta = {
    country: "USA",
    indicator: "gdp_yoy",
    horizon: "4Q",
    vintage_id: "2026-06-06-1200Z",
    model_id: "opengem-l3-dfm-bma-v0.4",
    model_card_url: "/methodology/l3-dfm-bma-v0-4",
  };

  return (
    <div className="space-y-6">
      <header className="border-b border-line pb-4">
        <div className="flex items-baseline gap-3">
          <span className="text-2xl">{isoToFlag(meta.country)}</span>
          <Link href={`/countries/${meta.country}`} className="font-mono text-2xs uppercase tracking-wider text-ink-muted hover:text-ink">
            {meta.country}
          </Link>
          <Link href={`/indicators/${meta.indicator}`} className="text-2xl text-ink hover:underline">
            GDP Growth (YoY)
          </Link>
          <span className="font-mono text-sm text-ink-muted">· {meta.horizon}</span>
        </div>
        <div className="mt-2 flex items-center gap-3 text-2xs text-ink-subtle">
          <span className="font-mono">vintage {meta.vintage_id}</span>
          <span>·</span>
          <Link href={meta.model_card_url} className="underline hover:text-ink font-mono">{meta.model_id}</Link>
        </div>
      </header>

      {/* Chart */}
      <section className="rounded-sm border border-line bg-bg-elevated p-4">
        <ForecastBandsChart points={HISTORY} unit="%" />
        <div className="mt-2 flex items-center justify-between text-2xs text-ink-subtle">
          <span>
            Backtest history (2024-Q1 → 2025-Q4) + current vintage forecast (2026-Q1 → 2026-Q4)
          </span>
          <Link href={`/track-record/${meta.indicator}`} className="underline hover:text-ink">
            calibration plot →
          </Link>
        </div>
      </section>

      {/* Summary stats */}
      <section className="grid grid-cols-2 gap-3 md:grid-cols-4">
        <div className="tile">
          <div className="tile-h">P50 — 4Q ahead</div>
          <div className="tile-v">{fmt(HISTORY[HISTORY.length - 1].p50, "%")}</div>
        </div>
        <div className="tile">
          <div className="tile-h">P10–P90 band</div>
          <div className="tile-v">
            {fmt(HISTORY[HISTORY.length - 1].p10, "%")}–{fmt(HISTORY[HISTORY.length - 1].p90, "%")}
          </div>
        </div>
        <div className="tile">
          <div className="tile-h">Misses in history</div>
          <div className="tile-v">2 / 8</div>
          <div className="mt-1 text-2xs text-bad">25% out-of-band</div>
        </div>
        <div className="tile">
          <div className="tile-h">CRPS vs AR(1)</div>
          <div className="tile-v">−32%</div>
          <div className="mt-1 text-2xs text-good">DM p = 0.001</div>
        </div>
      </section>

      {/* Vintage table */}
      <section>
        <h2 className="mb-2 font-mono text-sm uppercase tracking-widest text-ink-muted">
          Quarterly vintage table
        </h2>
        <div className="overflow-x-auto rounded-sm border border-line bg-bg-elevated">
          <table className="min-w-full text-sm">
            <thead className="border-b border-line text-2xs uppercase tracking-wide text-ink-subtle">
              <tr>
                <th className="px-3 py-2 text-left">Period</th>
                <th className="px-3 py-2 text-right">P10</th>
                <th className="px-3 py-2 text-right">P50</th>
                <th className="px-3 py-2 text-right">P90</th>
                <th className="px-3 py-2 text-right">Consensus</th>
                <th className="px-3 py-2 text-right">Actual</th>
                <th className="px-3 py-2 text-left">Result</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-line">
              {HISTORY.map((row) => {
                const inside = row.actual !== undefined && row.actual >= row.p10 && row.actual <= row.p90;
                const future = row.actual === undefined;
                return (
                  <tr key={row.date} className="hover:bg-bg-overlay">
                    <td className="px-3 py-2 font-mono">{row.date}</td>
                    <td className="px-3 py-2 text-right num text-ink-muted">{fmt(row.p10, "%")}</td>
                    <td className="px-3 py-2 text-right num text-ink">{fmt(row.p50, "%")}</td>
                    <td className="px-3 py-2 text-right num text-ink-muted">{fmt(row.p90, "%")}</td>
                    <td className="px-3 py-2 text-right num text-ink-subtle">{fmt(row.consensus, "%")}</td>
                    <td className="px-3 py-2 text-right num text-ink">{fmt(row.actual, "%")}</td>
                    <td className="px-3 py-2">
                      {future ? (
                        <span className="pill-info">pending</span>
                      ) : inside ? (
                        <span className="pill-good">hit (in 80% band)</span>
                      ) : (
                        <span className="pill-bad">miss · <Link href="/postmortem" className="underline">post-mortem</Link></span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </section>

      {/* Provenance drawer */}
      <section className="rounded-sm border border-line bg-bg-elevated p-4 text-sm text-ink-muted">
        <h2 className="font-mono text-sm uppercase tracking-widest text-brand-400 mb-2">
          Provenance
        </h2>
        <ul className="space-y-1">
          <li><code className="text-brand-400">vintage_id</code>: {meta.vintage_id}</li>
          <li><code className="text-brand-400">model_id</code>: {meta.model_id}</li>
          <li><code className="text-brand-400">git_sha</code>: a1b2c3d4 (<Link href="https://github.com/opengem/opengem/tree/a1b2c3d4" className="underline">browse</Link>)</li>
          <li><code className="text-brand-400">data_lockfile_hash</code>: sha256:deadbeef</li>
          <li><code className="text-brand-400">container_digest</code>: sha256:cafebabe</li>
          <li><code className="text-brand-400">generated_at</code>: 2026-06-06T12:00:00Z</li>
        </ul>
        <p className="mt-3">
          Anyone with the four fields above can replay this exact forecast bit-for-bit. That's the
          reproducibility envelope.
        </p>
      </section>
    </div>
  );
}
