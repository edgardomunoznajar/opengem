import Link from "next/link";

const LEADERBOARD = [
  { rank: 1, model: "opengem-l3-dfm-bma-v0.4", indicator: "gdp_yoy", horizon: "4Q", crps: 0.42, pit: 0.78, hitRate: 0.61, n: 96, last: "2026-06-06" },
  { rank: 2, model: "WEO Apr-2026", indicator: "gdp_yoy", horizon: "4Q", crps: 0.48, pit: 0.71, hitRate: 0.58, n: 96, last: "2026-04-15" },
  { rank: 3, model: "OECD EO Mar-2026", indicator: "gdp_yoy", horizon: "4Q", crps: 0.51, pit: 0.69, hitRate: 0.56, n: 96, last: "2026-03-10" },
  { rank: 4, model: "RW (random-walk)", indicator: "gdp_yoy", horizon: "4Q", crps: 0.65, pit: 0.55, hitRate: 0.50, n: 96, last: "—" },
  { rank: 5, model: "AR(1)", indicator: "gdp_yoy", horizon: "4Q", crps: 0.62, pit: 0.58, hitRate: 0.51, n: 96, last: "—" },
];

export default function LeaderboardPage() {
  return (
    <div className="space-y-4">
      <header className="border-b border-line pb-4">
        <h1 className="font-mono text-sm uppercase tracking-widest text-ink-muted">
          Forecast leaderboard — GDP YoY, 4Q
        </h1>
        <p className="mt-2 text-sm text-ink-muted">
          Ranked by CRPS over the Tier-V backtest sample (96 country-quarters,
          2020-Q1 → 2025-Q4). Random-walk and AR(1) included as floor baselines.
          {" "}
          <Link className="underline hover:text-ink" href="/methodology/scoring">
            scoring methodology
          </Link>
        </p>
      </header>
      <div className="overflow-x-auto rounded-sm border border-line bg-bg-elevated">
        <table className="min-w-full text-sm">
          <thead className="border-b border-line text-2xs uppercase tracking-wide text-ink-subtle">
            <tr>
              <th className="px-3 py-2 text-right">#</th>
              <th className="px-3 py-2 text-left">Model</th>
              <th className="px-3 py-2 text-left">Horizon</th>
              <th className="px-3 py-2 text-right">CRPS ↓</th>
              <th className="px-3 py-2 text-right">PIT</th>
              <th className="px-3 py-2 text-right">Hit-rate</th>
              <th className="px-3 py-2 text-right">N</th>
              <th className="px-3 py-2 text-left">Last vintage</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-line">
            {LEADERBOARD.map((row) => (
              <tr key={row.model} className="hover:bg-bg-overlay">
                <td className="px-3 py-2 text-right num text-ink-muted">{row.rank}</td>
                <td className="px-3 py-2">
                  <span className="font-mono text-sm">{row.model}</span>
                </td>
                <td className="px-3 py-2 font-mono text-2xs text-ink-muted">{row.horizon}</td>
                <td className="px-3 py-2 text-right num text-ink">{row.crps.toFixed(2)}</td>
                <td className="px-3 py-2 text-right num text-ink-muted">{row.pit.toFixed(2)}</td>
                <td className="px-3 py-2 text-right num text-ink-muted">{(row.hitRate * 100).toFixed(0)}%</td>
                <td className="px-3 py-2 text-right num text-ink-subtle">{row.n}</td>
                <td className="px-3 py-2 font-mono text-2xs text-ink-subtle">{row.last}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="text-2xs text-ink-subtle">
        ↓ Lower CRPS is better. Diebold-Mariano p-values vs RW baseline available on the
        {" "}
        <Link href="/track-record/gdp_yoy" className="underline hover:text-ink">track record page</Link>.
      </div>
    </div>
  );
}
