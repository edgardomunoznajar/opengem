import { getForecasts, INDICATORS, COUNTRY_NAMES } from "@/lib/api";
import { fmt, isoToFlag, cn } from "@/lib/utils";
import Link from "next/link";

interface PageProps {
  params: Promise<{ id: string }>;
}

export default async function IndicatorPage({ params }: PageProps) {
  const { id } = await params;
  const forecasts = await getForecasts({ indicator: id });
  const meta = INDICATORS[id] ?? { label: id, unit: "" };

  return (
    <div className="space-y-6">
      <header className="border-b border-line pb-4">
        <div className="font-mono text-2xs uppercase tracking-wider text-ink-subtle">
          INDICATOR
        </div>
        <h1 className="text-2xl text-ink">{meta.label}</h1>
        <div className="mt-2 flex items-center gap-3 text-2xs text-ink-subtle">
          <span className="font-mono">{id}</span>
          <span>·</span>
          <Link href={`/methodology/${id}`} className="underline hover:text-ink">methodology</Link>
          <span>·</span>
          <Link href={`/track-record/${id}`} className="underline hover:text-ink">track record</Link>
        </div>
      </header>

      <section>
        <h2 className="mb-2 font-mono text-sm uppercase tracking-widest text-ink-muted">
          Cross-country forecasts — 4Q ahead
        </h2>
        <div className="overflow-x-auto rounded-sm border border-line bg-bg-elevated">
          <table className="min-w-full text-sm">
            <thead className="border-b border-line text-2xs uppercase tracking-wide text-ink-subtle">
              <tr>
                <th className="px-3 py-2 text-left">Country</th>
                <th className="px-3 py-2 text-right">OPENGEM (P50)</th>
                <th className="px-3 py-2 text-right">P10</th>
                <th className="px-3 py-2 text-right">P90</th>
                <th className="px-3 py-2 text-right">vs WEO</th>
                <th className="px-3 py-2 text-right">vs OECD</th>
                <th className="px-3 py-2 text-left">Vintage</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-line">
              {forecasts.map((f) => {
                const weoDiff =
                  f.consensus_overlay?.weo !== undefined
                    ? f.point - f.consensus_overlay.weo
                    : undefined;
                const oecdDiff =
                  f.consensus_overlay?.oecd_eo !== undefined
                    ? f.point - f.consensus_overlay.oecd_eo
                    : undefined;
                return (
                  <tr key={f.country} className="hover:bg-bg-overlay">
                    <td className="px-3 py-2">
                      <Link href={`/countries/${f.country}`} className="hover:underline">
                        <span className="mr-1">{isoToFlag(f.country)}</span>
                        <span className="font-mono text-2xs">{f.country}</span>
                        <span className="ml-2">{COUNTRY_NAMES[f.country] ?? f.country}</span>
                      </Link>
                    </td>
                    <td className="px-3 py-2 text-right num text-ink">{fmt(f.point, meta.unit)}</td>
                    <td className="px-3 py-2 text-right num text-ink-muted">{fmt(f.bands.p10, meta.unit)}</td>
                    <td className="px-3 py-2 text-right num text-ink-muted">{fmt(f.bands.p90, meta.unit)}</td>
                    <td className={cn(
                      "px-3 py-2 text-right num",
                      weoDiff === undefined && "text-ink-subtle",
                      weoDiff !== undefined && weoDiff > 0 && "text-good",
                      weoDiff !== undefined && weoDiff < 0 && "text-bad"
                    )}>
                      {weoDiff === undefined ? "—" : (weoDiff > 0 ? "+" : "") + weoDiff.toFixed(1)}
                    </td>
                    <td className={cn(
                      "px-3 py-2 text-right num",
                      oecdDiff === undefined && "text-ink-subtle",
                      oecdDiff !== undefined && oecdDiff > 0 && "text-good",
                      oecdDiff !== undefined && oecdDiff < 0 && "text-bad"
                    )}>
                      {oecdDiff === undefined ? "—" : (oecdDiff > 0 ? "+" : "") + oecdDiff.toFixed(1)}
                    </td>
                    <td className="px-3 py-2 font-mono text-2xs text-ink-subtle">{f.vintage_id}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
