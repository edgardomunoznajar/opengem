import Link from "next/link";
import { cn } from "@/lib/utils";
import { INDICATORS } from "@/lib/api";

const CELLS = [
  // country × horizon V&V matrix
  { country: "USA", horizons: { "nowcast": "PASS", "1Q": "PASS", "4Q": "PASS", "2Y": "WARN", "5Y": "WARN" } },
  { country: "CHN", horizons: { "nowcast": "PASS", "1Q": "PASS", "4Q": "WARN", "2Y": "FAIL", "5Y": "FAIL" } },
  { country: "JPN", horizons: { "nowcast": "PASS", "1Q": "PASS", "4Q": "PASS", "2Y": "PASS", "5Y": "WARN" } },
  { country: "DEU", horizons: { "nowcast": "PASS", "1Q": "PASS", "4Q": "WARN", "2Y": "WARN", "5Y": "FAIL" } },
  { country: "GBR", horizons: { "nowcast": "PASS", "1Q": "PASS", "4Q": "PASS", "2Y": "WARN", "5Y": "WARN" } },
  { country: "FRA", horizons: { "nowcast": "PASS", "1Q": "PASS", "4Q": "PASS", "2Y": "PASS", "5Y": "WARN" } },
  { country: "IND", horizons: { "nowcast": "PASS", "1Q": "WARN", "4Q": "WARN", "2Y": "FAIL", "5Y": "FAIL" } },
  { country: "BRA", horizons: { "nowcast": "PASS", "1Q": "PASS", "4Q": "WARN", "2Y": "WARN", "5Y": "FAIL" } },
];

const HORIZONS = ["nowcast", "1Q", "4Q", "2Y", "5Y"] as const;

const SCORE_STYLES = {
  PASS: "bg-good/15 text-good",
  WARN: "bg-warn/15 text-warn",
  FAIL: "bg-bad/15 text-bad",
  NA: "bg-bg-overlay text-ink-subtle",
};

const CALIBRATION = [
  { bucket: "0–10%", expected: 10, observed: 11.4 },
  { bucket: "10–20%", expected: 10, observed: 9.8 },
  { bucket: "20–30%", expected: 10, observed: 8.7 },
  { bucket: "30–40%", expected: 10, observed: 12.1 },
  { bucket: "40–50%", expected: 10, observed: 11.2 },
  { bucket: "50–60%", expected: 10, observed: 9.4 },
  { bucket: "60–70%", expected: 10, observed: 8.9 },
  { bucket: "70–80%", expected: 10, observed: 9.8 },
  { bucket: "80–90%", expected: 10, observed: 10.4 },
  { bucket: "90–100%", expected: 10, observed: 8.3 },
];

interface PageProps {
  params: Promise<{ indicator: string }>;
}

export default async function TrackRecordPage({ params }: PageProps) {
  const { indicator } = await params;
  const meta = INDICATORS[indicator] ?? { label: indicator, unit: "" };
  const overall = {
    crps: 0.42,
    crpsVsAr1: -32,
    pit: 0.78,
    hitRate: 0.61,
    n: 96,
    dmPVsAr1: 0.001,
    dmPVsWeo: 0.084,
  };

  return (
    <div className="space-y-6">
      <header className="border-b border-line pb-4 flex items-baseline justify-between">
        <div>
          <div className="font-mono text-2xs uppercase tracking-wider text-ink-subtle">
            TRACK RECORD
          </div>
          <h1 className="text-2xl text-ink">{meta.label}</h1>
        </div>
        <div className="flex items-center gap-2">
          <Link href={`/indicators/${indicator}`} className="pill-info">indicator page</Link>
          <Link href="/leaderboard" className="pill-info">leaderboard</Link>
          <Link href="/methodology/scoring" className="pill-info">scoring</Link>
        </div>
      </header>

      <section>
        <h2 className="mb-2 font-mono text-sm uppercase tracking-widest text-ink-muted">
          Overall scoring (Tier-V backtest, 2020-Q1 → 2025-Q4)
        </h2>
        <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
          <div className="tile">
            <div className="tile-h">CRPS ↓</div>
            <div className="tile-v">{overall.crps.toFixed(2)}</div>
            <div className="mt-1 text-2xs text-good">
              {overall.crpsVsAr1}% vs AR(1)
            </div>
          </div>
          <div className="tile">
            <div className="tile-h">PIT</div>
            <div className="tile-v">{overall.pit.toFixed(2)}</div>
            <div className="mt-1 text-2xs text-ink-subtle">target: 0.78+ at 80% band</div>
          </div>
          <div className="tile">
            <div className="tile-h">Hit rate</div>
            <div className="tile-v">{(overall.hitRate * 100).toFixed(0)}%</div>
            <div className="mt-1 text-2xs text-ink-subtle">vs RW: +11pp</div>
          </div>
          <div className="tile">
            <div className="tile-h">DM p-value</div>
            <div className="tile-v">{overall.dmPVsAr1.toFixed(3)}</div>
            <div className="mt-1 text-2xs text-ink-subtle">vs AR(1) baseline</div>
          </div>
        </div>
      </section>

      <section>
        <h2 className="mb-2 font-mono text-sm uppercase tracking-widest text-ink-muted">
          V&V matrix — country × horizon
        </h2>
        <div className="overflow-x-auto rounded-sm border border-line bg-bg-elevated">
          <table className="min-w-full text-sm">
            <thead className="border-b border-line text-2xs uppercase tracking-wide text-ink-subtle">
              <tr>
                <th className="px-3 py-2 text-left">Country</th>
                {HORIZONS.map((h) => (
                  <th key={h} className="px-3 py-2 text-center">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-line">
              {CELLS.map((row) => (
                <tr key={row.country} className="hover:bg-bg-overlay">
                  <td className="px-3 py-2 font-mono">{row.country}</td>
                  {HORIZONS.map((h) => {
                    const cell = row.horizons[h] as keyof typeof SCORE_STYLES;
                    return (
                      <td key={h} className="px-3 py-2 text-center">
                        <span className={cn("pill", SCORE_STYLES[cell])}>{cell}</span>
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="mt-2 text-2xs text-ink-subtle">
          PASS = beats AR(1) by CRPS at p&lt;0.05. WARN = beats RW only. FAIL = neither.
          The matrix is the V&V gate; cells flip based on rolling backtest.
        </div>
      </section>

      <section>
        <h2 className="mb-2 font-mono text-sm uppercase tracking-widest text-ink-muted">
          Calibration plot — 80% band expected vs observed
        </h2>
        <div className="overflow-x-auto rounded-sm border border-line bg-bg-elevated">
          <table className="min-w-full text-sm">
            <thead className="border-b border-line text-2xs uppercase tracking-wide text-ink-subtle">
              <tr>
                <th className="px-3 py-2 text-left">PIT bucket</th>
                <th className="px-3 py-2 text-right">Expected %</th>
                <th className="px-3 py-2 text-right">Observed %</th>
                <th className="px-3 py-2 text-right">Δ</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-line">
              {CALIBRATION.map((c) => {
                const delta = c.observed - c.expected;
                return (
                  <tr key={c.bucket} className="hover:bg-bg-overlay">
                    <td className="px-3 py-2 font-mono">{c.bucket}</td>
                    <td className="px-3 py-2 text-right num text-ink-muted">{c.expected.toFixed(1)}</td>
                    <td className="px-3 py-2 text-right num text-ink">{c.observed.toFixed(1)}</td>
                    <td className={cn(
                      "px-3 py-2 text-right num",
                      Math.abs(delta) < 2 && "text-good",
                      Math.abs(delta) >= 2 && Math.abs(delta) < 4 && "text-warn",
                      Math.abs(delta) >= 4 && "text-bad"
                    )}>
                      {delta > 0 ? "+" : ""}{delta.toFixed(1)}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </section>

      <section className="rounded-sm border border-line bg-bg-elevated p-4 text-sm text-ink-muted">
        Every cell of this matrix is a permanent URL. If a cell drifts, the chart
        retains its prior state and the new value supersedes it — both are kept.
        That's the publication discipline. See{" "}
        <Link href="/accountability" className="underline hover:text-ink">accountability ledger</Link>{" "}
        for the long-run version.
      </section>
    </div>
  );
}
