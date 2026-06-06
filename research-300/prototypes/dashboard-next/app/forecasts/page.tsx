import { getForecasts, INDICATORS, COUNTRY_NAMES } from "@/lib/api";
import { fmt, isoToFlag, cn } from "@/lib/utils";
import Link from "next/link";

export default async function ForecastsIndex() {
  const forecasts = await getForecasts();

  return (
    <div className="space-y-4">
      <header className="border-b border-line pb-4 flex items-baseline justify-between">
        <div>
          <h1 className="font-mono text-sm uppercase tracking-widest text-ink-muted">
            All forecasts — current vintage
          </h1>
          <p className="mt-2 text-sm text-ink-muted">
            Every published forecast object. Each row links to the vintage
            timeline + model card + miss log. Use the URL grammar
            <span className="font-mono"> /vintage/YYYY-MM-DD/forecasts </span>
            to time-travel.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Link href="/leaderboard" className="pill-info">leaderboard</Link>
          <a href="/api/forecasts.json" className="pill-info">JSON</a>
          <a href="/api/forecasts.csv" className="pill-info">CSV</a>
        </div>
      </header>
      <div className="overflow-x-auto rounded-sm border border-line bg-bg-elevated">
        <table className="min-w-full text-sm">
          <thead className="border-b border-line text-2xs uppercase tracking-wide text-ink-subtle">
            <tr>
              <th className="px-3 py-2 text-left">Country</th>
              <th className="px-3 py-2 text-left">Indicator</th>
              <th className="px-3 py-2 text-left">Horizon</th>
              <th className="px-3 py-2 text-right">OPENGEM (P50)</th>
              <th className="px-3 py-2 text-right">P10</th>
              <th className="px-3 py-2 text-right">P90</th>
              <th className="px-3 py-2 text-right">vs WEO</th>
              <th className="px-3 py-2 text-left">Badges</th>
              <th className="px-3 py-2 text-left">Model</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-line">
            {forecasts.map((f) => {
              const unit = INDICATORS[f.indicator]?.unit ?? "";
              const weoDiff = f.consensus_overlay?.weo !== undefined
                ? f.point - f.consensus_overlay.weo : undefined;
              return (
                <tr key={`${f.country}-${f.indicator}-${f.horizon}`} className="hover:bg-bg-overlay">
                  <td className="px-3 py-2">
                    <Link href={`/countries/${f.country}`} className="hover:underline">
                      <span className="mr-1">{isoToFlag(f.country)}</span>
                      <span className="font-mono text-2xs">{f.country}</span>
                    </Link>
                  </td>
                  <td className="px-3 py-2">
                    <Link href={`/indicators/${f.indicator}`} className="hover:underline font-mono text-2xs">
                      {f.indicator}
                    </Link>
                  </td>
                  <td className="px-3 py-2 font-mono text-2xs text-ink-muted">{f.horizon}</td>
                  <td className="px-3 py-2 text-right num text-ink">{fmt(f.point, unit)}</td>
                  <td className="px-3 py-2 text-right num text-ink-muted">{fmt(f.bands.p10, unit)}</td>
                  <td className="px-3 py-2 text-right num text-ink-muted">{fmt(f.bands.p90, unit)}</td>
                  <td className={cn(
                    "px-3 py-2 text-right num",
                    weoDiff === undefined && "text-ink-subtle",
                    weoDiff !== undefined && weoDiff > 0 && "text-good",
                    weoDiff !== undefined && weoDiff < 0 && "text-bad"
                  )}>
                    {weoDiff === undefined ? "—" : (weoDiff > 0 ? "+" : "") + weoDiff.toFixed(1)}
                  </td>
                  <td className="px-3 py-2">
                    <div className="flex flex-wrap gap-1">
                      {f.badges?.slice(0, 2).map((b) => (
                        <span key={b} className="pill-info">{b}</span>
                      ))}
                    </div>
                  </td>
                  <td className="px-3 py-2 text-2xs">
                    <Link href={f.model_card_url} className="text-info hover:underline font-mono">
                      {f.model_id}
                    </Link>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
