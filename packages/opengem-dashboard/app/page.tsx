import { getSituation, getForecasts, getScenarios, COUNTRY_NAMES } from "@/lib/api";
import { IndicatorTile } from "@/components/tiles/IndicatorTile";
import { CountryCard } from "@/components/tiles/CountryCard";
import Link from "next/link";
import { fmt } from "@/lib/utils";

const SITUATION_LABELS: Record<string, string> = {
  recession_prob: "US recession (12m)",
  gpr_nowcast: "Geopolitical risk",
  gscpi: "Supply chain pressure",
  fci: "US financial conditions",
  inflation_nowcast: "US inflation (nowcast)",
  gdp_nowcast: "US GDP (nowcast)",
};

const TIER_V = [
  "USA", "CHN", "JPN", "DEU", "GBR", "FRA", "IND", "ITA",
  "BRA", "CAN", "KOR", "AUS", "MEX", "ESP", "IDN", "NLD",
  "TUR", "CHE", "POL", "SWE", "BEL", "IRL",
];

export default async function Home() {
  const [situation, forecasts, scenarios] = await Promise.all([
    getSituation(),
    getForecasts(),
    getScenarios(),
  ]);

  return (
    <div className="space-y-6">
      {/* Hero strip — situation indicators */}
      <section>
        <div className="mb-2 flex items-baseline justify-between">
          <h1 className="font-mono text-sm uppercase tracking-widest text-ink-muted">
            World Pulse
          </h1>
          <div className="text-2xs text-ink-subtle">
            Updated{" "}
            <span className="num text-ink-muted">{situation[0]?.as_of}</span>{" "}
            ·{" "}
            <Link href="/accountability" className="underline hover:text-ink">
              accountability ledger
            </Link>
          </div>
        </div>
        <div className="grid grid-cols-2 gap-3 md:grid-cols-3 lg:grid-cols-6">
          {situation.map((s, i) => (
            <IndicatorTile
              key={`${s.kind}-${s.country ?? "G"}-${i}`}
              label={SITUATION_LABELS[s.kind] ?? s.kind}
              value={
                s.kind === "recession_prob" ? s.value * 100 : s.value
              }
              unit={
                s.kind === "recession_prob" ||
                s.kind === "inflation_nowcast" ||
                s.kind === "gdp_nowcast"
                  ? "%"
                  : undefined
              }
              delta={s.delta}
              spark={s.spark}
              asOf={s.as_of}
              href={`/indicators/${s.kind}`}
            />
          ))}
        </div>
      </section>

      {/* Active scenarios row */}
      <section>
        <div className="mb-2 flex items-baseline justify-between">
          <h2 className="font-mono text-sm uppercase tracking-widest text-ink-muted">
            Active scenarios
          </h2>
          <Link href="/scenarios" className="text-2xs text-ink-subtle hover:text-ink underline">
            all {scenarios.length} →
          </Link>
        </div>
        <div className="grid grid-cols-1 gap-3 md:grid-cols-2 lg:grid-cols-4">
          {scenarios.map((s) => (
            <Link
              key={s.slug}
              href={`/scenarios/${s.slug}`}
              className="tile group block hover:border-line-strong"
            >
              <div className="flex items-baseline justify-between">
                <div className="tile-h">P {(s.probability * 100).toFixed(0)}%</div>
                <div className="text-2xs text-ink-subtle">
                  {s.affected_countries.length} countries
                </div>
              </div>
              <div className="mt-1 text-sm text-ink">{s.name}</div>
              <div className="mt-1 text-2xs text-ink-muted line-clamp-2">
                {s.description}
              </div>
              <div className="mt-2 flex flex-wrap gap-1">
                {s.affected_countries.slice(0, 5).map((c) => (
                  <span key={c} className="pill-info">{c}</span>
                ))}
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* Forecast strip */}
      <section>
        <div className="mb-2 flex items-baseline justify-between">
          <h2 className="font-mono text-sm uppercase tracking-widest text-ink-muted">
            Forecast strip — 4Q ahead
          </h2>
          <Link href="/forecasts" className="text-2xs text-ink-subtle hover:text-ink underline">
            all forecasts →
          </Link>
        </div>
        <div className="overflow-x-auto rounded-sm border border-line bg-bg-elevated">
          <table className="min-w-full text-sm">
            <thead className="border-b border-line text-2xs uppercase tracking-wide text-ink-subtle">
              <tr>
                <th className="px-3 py-2 text-left">Country</th>
                <th className="px-3 py-2 text-left">Indicator</th>
                <th className="px-3 py-2 text-right">OPENGEM</th>
                <th className="px-3 py-2 text-right">P10</th>
                <th className="px-3 py-2 text-right">P90</th>
                <th className="px-3 py-2 text-right">WEO</th>
                <th className="px-3 py-2 text-right">OECD</th>
                <th className="px-3 py-2 text-left">Badges</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-line">
              {forecasts.map((f) => (
                <tr key={`${f.country}-${f.indicator}`} className="hover:bg-bg-overlay">
                  <td className="px-3 py-2 font-mono text-2xs">{f.country}</td>
                  <td className="px-3 py-2">{f.indicator}</td>
                  <td className="px-3 py-2 text-right num">{fmt(f.point, "%")}</td>
                  <td className="px-3 py-2 text-right num text-ink-muted">{fmt(f.bands.p10, "%")}</td>
                  <td className="px-3 py-2 text-right num text-ink-muted">{fmt(f.bands.p90, "%")}</td>
                  <td className="px-3 py-2 text-right num text-ink-subtle">{fmt(f.consensus_overlay?.weo, "%")}</td>
                  <td className="px-3 py-2 text-right num text-ink-subtle">{fmt(f.consensus_overlay?.oecd_eo, "%")}</td>
                  <td className="px-3 py-2">
                    <div className="flex flex-wrap gap-1">
                      {f.badges?.slice(0, 2).map((b) => (
                        <span key={b} className="pill-info">{b}</span>
                      ))}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* Country grid (Tier-V) */}
      <section>
        <div className="mb-2 flex items-baseline justify-between">
          <h2 className="font-mono text-sm uppercase tracking-widest text-ink-muted">
            Countries — Tier-V coverage
          </h2>
          <Link href="/countries" className="text-2xs text-ink-subtle hover:text-ink underline">
            all countries →
          </Link>
        </div>
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {TIER_V.slice(0, 8).map((iso3, idx) => (
            <CountryCard
              key={iso3}
              iso3={iso3}
              name={COUNTRY_NAMES[iso3] ?? iso3}
              recessionProb={[0.32, 0.18, 0.21, 0.38, 0.41, 0.27, 0.22, 0.25][idx]}
              gpr={[143, 91, 72, 102, 88, 76, 64, 81][idx]}
              metrics={[
                { label: "GDP", value: [1.9, 4.3, 1.1, 0.7, 0.9, 1.2, 7.0, 0.5][idx], unit: "%", delta: -0.1, spark: [2.4, 2.2, 2.1, 2.0, 1.9, 1.9] },
                { label: "CPI", value: [2.5, 1.2, 2.8, 2.1, 3.0, 2.3, 4.6, 1.8][idx], unit: "%", delta: -0.2, spark: [3.2, 3.0, 2.9, 2.7, 2.6, 2.5] },
                { label: "Unemp", value: [4.1, 5.2, 2.6, 5.8, 4.5, 7.3, 7.8, 8.1][idx], unit: "%", delta: 0.0, spark: [4.1, 4.1, 4.1, 4.1, 4.1, 4.1] },
              ]}
            />
          ))}
        </div>
      </section>
    </div>
  );
}
