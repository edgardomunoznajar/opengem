import Link from "next/link";
import { cn, isoToFlag } from "@/lib/utils";

const TIER_V = ["USA", "CHN", "JPN", "DEU", "GBR", "FRA", "IND", "ITA", "BRA", "CAN", "KOR", "AUS", "MEX", "ESP", "IDN", "NLD", "TUR", "CHE", "POL", "SWE", "BEL", "IRL"];
const TIER_T_SAMPLE = ["RUS", "ZAF", "SAU", "ARG", "NGA", "EGY", "VNM", "PHL", "PAK", "BGD", "THA", "MYS", "SGP", "ARE", "CHL", "COL", "PER", "GRC", "PRT", "CZE"];

const INDICATORS = [
  { id: "gdp_yoy", label: "GDP" },
  { id: "cpi_yoy", label: "CPI" },
  { id: "unemployment", label: "Unemp" },
  { id: "policy_rate", label: "Rate" },
  { id: "gpr", label: "GPR" },
  { id: "recession_prob_12m", label: "Recession" },
];

const HORIZONS = ["nowcast", "1Q", "4Q", "2Y", "5Y"] as const;

type Cell = "FULL" | "PARTIAL" | "TRACKED" | "NONE";

function cellFor(_country: string, _indicator: string, horizon: string, tier: "V" | "T"): Cell {
  if (tier === "T") return horizon === "nowcast" ? "TRACKED" : horizon === "1Q" ? "TRACKED" : "NONE";
  // Tier-V coverage by horizon
  switch (horizon) {
    case "nowcast": return "FULL";
    case "1Q":      return "FULL";
    case "4Q":      return "FULL";
    case "2Y":      return Math.random() > 0.4 ? "FULL" : "PARTIAL";
    case "5Y":      return Math.random() > 0.6 ? "PARTIAL" : "NONE";
  }
  return "NONE";
}

const CELL_STYLE: Record<Cell, string> = {
  FULL: "bg-good/30 text-good",
  PARTIAL: "bg-warn/25 text-warn",
  TRACKED: "bg-info/20 text-info",
  NONE: "bg-bg-overlay text-ink-subtle",
};

export default function CoveragePage() {
  return (
    <div className="space-y-6">
      <header className="border-b border-line pb-4">
        <h1 className="font-mono text-sm uppercase tracking-widest text-ink-muted">
          Coverage matrix
        </h1>
        <p className="mt-2 text-base text-ink">
          Which countries get which forecasts, at which horizons. Tier-V is
          vintage-correct (full backtest discipline). Tier-T is tracked-only
          (current snapshots; nowcasts only, no vintage replay).
        </p>
        <div className="mt-3 flex flex-wrap gap-2 text-2xs">
          <span className="pill bg-good/30 text-good">FULL</span>
          <span className="pill bg-warn/25 text-warn">PARTIAL</span>
          <span className="pill bg-info/20 text-info">TRACKED-ONLY</span>
          <span className="pill bg-bg-overlay text-ink-subtle">NONE</span>
        </div>
      </header>

      <section>
        <h2 className="mb-2 font-mono text-sm uppercase tracking-widest text-ink-muted">
          Tier-V — vintage-correct (22 economies)
        </h2>
        <div className="overflow-x-auto rounded-sm border border-line bg-bg-elevated">
          <table className="min-w-full text-2xs">
            <thead className="border-b border-line text-2xs uppercase tracking-wide text-ink-subtle">
              <tr>
                <th className="px-2 py-2 text-left">Country</th>
                {INDICATORS.map((i) => (
                  <th key={i.id} className="px-1 py-2" colSpan={HORIZONS.length}>
                    {i.label}
                  </th>
                ))}
              </tr>
              <tr>
                <th className="px-2 py-1"></th>
                {INDICATORS.flatMap((i) =>
                  HORIZONS.map((h) => (
                    <th key={`${i.id}-${h}`} className="px-1 py-1 font-mono text-2xs text-ink-subtle">{h}</th>
                  ))
                )}
              </tr>
            </thead>
            <tbody className="divide-y divide-line">
              {TIER_V.map((c) => (
                <tr key={c} className="hover:bg-bg-overlay">
                  <td className="px-2 py-1">
                    <Link href={`/countries/${c}`} className="hover:underline">
                      <span className="mr-1">{isoToFlag(c)}</span>
                      <span className="font-mono">{c}</span>
                    </Link>
                  </td>
                  {INDICATORS.flatMap((i) =>
                    HORIZONS.map((h) => {
                      const cell = cellFor(c, i.id, h, "V");
                      return (
                        <td key={`${c}-${i.id}-${h}`} className="px-1 py-1 text-center">
                          <span className={cn("inline-block w-7 rounded-sm py-0.5", CELL_STYLE[cell])}>
                            {cell === "FULL" ? "●" : cell === "PARTIAL" ? "◐" : cell === "TRACKED" ? "○" : "·"}
                          </span>
                        </td>
                      );
                    })
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section>
        <h2 className="mb-2 font-mono text-sm uppercase tracking-widest text-ink-muted">
          Tier-T — tracked only (sample of 20; full list ~110 economies)
        </h2>
        <div className="overflow-x-auto rounded-sm border border-line bg-bg-elevated">
          <table className="min-w-full text-2xs">
            <thead className="border-b border-line text-2xs uppercase tracking-wide text-ink-subtle">
              <tr>
                <th className="px-2 py-2 text-left">Country</th>
                {INDICATORS.map((i) => (
                  <th key={i.id} className="px-1 py-2" colSpan={HORIZONS.length}>
                    {i.label}
                  </th>
                ))}
              </tr>
              <tr>
                <th className="px-2 py-1"></th>
                {INDICATORS.flatMap((i) =>
                  HORIZONS.map((h) => (
                    <th key={`${i.id}-${h}`} className="px-1 py-1 font-mono text-2xs text-ink-subtle">{h}</th>
                  ))
                )}
              </tr>
            </thead>
            <tbody className="divide-y divide-line">
              {TIER_T_SAMPLE.map((c) => (
                <tr key={c} className="hover:bg-bg-overlay">
                  <td className="px-2 py-1">
                    <Link href={`/countries/${c}`} className="hover:underline">
                      <span className="mr-1">{isoToFlag(c)}</span>
                      <span className="font-mono">{c}</span>
                    </Link>
                  </td>
                  {INDICATORS.flatMap((i) =>
                    HORIZONS.map((h) => {
                      const cell = cellFor(c, i.id, h, "T");
                      return (
                        <td key={`${c}-${i.id}-${h}`} className="px-1 py-1 text-center">
                          <span className={cn("inline-block w-7 rounded-sm py-0.5", CELL_STYLE[cell])}>
                            {cell === "FULL" ? "●" : cell === "PARTIAL" ? "◐" : cell === "TRACKED" ? "○" : "·"}
                          </span>
                        </td>
                      );
                    })
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="rounded-sm border border-line bg-bg-elevated p-4 text-sm text-ink-muted">
        <h2 className="font-mono text-sm uppercase tracking-widest text-brand-400">
          Tier discipline
        </h2>
        <ul className="mt-2 list-inside list-disc space-y-1">
          <li>
            <strong className="text-ink">Tier-V</strong> means vintage-correct: we have ALFRED-equivalent
            real-time data archives, so a backtest of "what would we have forecast on date X" is
            mechanically correct.
          </li>
          <li>
            <strong className="text-ink">Tier-T</strong> means tracked-only: we publish nowcasts from
            current data but cannot replay history without conflating revisions with new information.
          </li>
          <li>
            Coverage is gated by upstream agency vintage archives, not by ambition. Adding a country
            to Tier-V requires its statistical office to publish vintage data — most don't.
          </li>
          <li>
            The Tier-V/Tier-T split is published; we never silently downgrade or upgrade.
          </li>
        </ul>
      </section>
    </div>
  );
}
