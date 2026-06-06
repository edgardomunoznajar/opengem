import { getCountry } from "@/lib/api";
import { IndicatorTile } from "@/components/tiles/IndicatorTile";
import { fmt, isoToFlag, cn } from "@/lib/utils";
import Link from "next/link";
import { notFound } from "next/navigation";

interface PageProps {
  params: Promise<{ iso3: string }>;
}

export default async function CountryPage({ params }: PageProps) {
  const { iso3 } = await params;
  const country = await getCountry(iso3.toUpperCase());
  if (!country.name || country.name === iso3.toUpperCase()) {
    // Allow unknown ISOs to render with a degraded state rather than 404 outright.
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <header className="flex items-baseline justify-between gap-4 border-b border-line pb-4">
        <div className="flex items-baseline gap-4">
          <span className="text-3xl">{isoToFlag(country.iso3)}</span>
          <div>
            <div className="font-mono text-2xs uppercase tracking-wider text-ink-subtle">
              {country.iso3}
            </div>
            <h1 className="text-2xl text-ink">{country.name}</h1>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Link href={`/countries/${iso3}/methodology`} className="pill-info">methodology</Link>
          <Link href={`/countries/${iso3}/track-record`} className="pill-info">track record</Link>
          <Link href={`/countries/${iso3}/vintage`} className="pill-info">vintage</Link>
        </div>
      </header>

      {/* Situation tiles */}
      <section>
        <h2 className="mb-2 font-mono text-sm uppercase tracking-widest text-ink-muted">
          Situation
        </h2>
        <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
          {country.situation.map((s, i) => (
            <IndicatorTile
              key={`${s.kind}-${i}`}
              label={s.kind}
              value={s.kind === "recession_prob" ? s.value * 100 : s.value}
              unit={s.kind === "recession_prob" ? "%" : undefined}
              delta={s.delta}
              spark={s.spark}
              asOf={s.as_of}
            />
          ))}
        </div>
      </section>

      {/* Forecasts */}
      <section>
        <h2 className="mb-2 font-mono text-sm uppercase tracking-widest text-ink-muted">
          Forecasts
        </h2>
        <div className="overflow-x-auto rounded-sm border border-line bg-bg-elevated">
          <table className="min-w-full text-sm">
            <thead className="border-b border-line text-2xs uppercase tracking-wide text-ink-subtle">
              <tr>
                <th className="px-3 py-2 text-left">Indicator</th>
                <th className="px-3 py-2 text-left">Horizon</th>
                <th className="px-3 py-2 text-right">OPENGEM (P50)</th>
                <th className="px-3 py-2 text-right">Band P10–P90</th>
                <th className="px-3 py-2 text-right">WEO</th>
                <th className="px-3 py-2 text-right">OECD EO</th>
                <th className="px-3 py-2 text-left">Model</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-line">
              {country.forecasts.map((f) => (
                <tr key={`${f.indicator}-${f.horizon}`} className="hover:bg-bg-overlay">
                  <td className="px-3 py-2 font-mono">{f.indicator}</td>
                  <td className="px-3 py-2 font-mono text-2xs text-ink-muted">{f.horizon}</td>
                  <td className="px-3 py-2 text-right num text-ink">{fmt(f.point, "%")}</td>
                  <td className="px-3 py-2 text-right num text-ink-muted">
                    {fmt(f.bands.p10, "%")} – {fmt(f.bands.p90, "%")}
                  </td>
                  <td className="px-3 py-2 text-right num text-ink-subtle">{fmt(f.consensus_overlay?.weo, "%")}</td>
                  <td className="px-3 py-2 text-right num text-ink-subtle">{fmt(f.consensus_overlay?.oecd_eo, "%")}</td>
                  <td className="px-3 py-2 text-2xs">
                    <Link href={f.model_card_url} className="text-info hover:underline">
                      {f.model_id}
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* Methodology drawer prompt */}
      <section className="rounded-sm border border-line bg-bg-elevated p-4 text-2xs text-ink-muted">
        <span className="font-mono uppercase tracking-widest text-brand-400 mr-2">
          Provenance
        </span>
        Every number above is vintage-stamped. Click any indicator to open its lineage drawer —
        upstream agency endpoint, retrieval timestamp, model snapshot, container digest.
      </section>
    </div>
  );
}
