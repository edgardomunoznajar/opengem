import Link from "next/link";

const VINTAGE_DATES = [
  { date: "2026-06-06", label: "Today", scenarios: 4, forecasts: 142, badge: "current" },
  { date: "2026-05-30", label: "1 week ago", scenarios: 3, forecasts: 138, badge: null },
  { date: "2026-05-01", label: "1 month ago", scenarios: 5, forecasts: 124, badge: null },
  { date: "2026-03-01", label: "Q1 close", scenarios: 6, forecasts: 118, badge: "quarterly" },
  { date: "2026-01-01", label: "Y2026 open", scenarios: 8, forecasts: 102, badge: "annual" },
  { date: "2025-09-01", label: "Pre-Q4-rally", scenarios: 4, forecasts: 96, badge: null },
  { date: "2024-09-01", label: "Pre-2024-election", scenarios: 7, forecasts: 84, badge: "notable" },
  { date: "2024-03-01", label: "Q1 2024", scenarios: 5, forecasts: 71, badge: null },
];

export default function VintagePage() {
  return (
    <div className="space-y-6">
      <header className="border-b border-line pb-4">
        <h1 className="font-mono text-sm uppercase tracking-widest text-ink-muted">
          Vintage time machine
        </h1>
        <p className="mt-2 text-base text-ink">
          Rewind to any past vintage and see exactly what OPENGEM forecast that day.
          Every page in this app supports vintage-scoped URLs — the dashboard becomes
          a public time-series of forecasts, not a snapshot.
        </p>
      </header>

      <section>
        <h2 className="mb-2 font-mono text-sm uppercase tracking-widest text-ink-muted">
          Recent vintages
        </h2>
        <div className="grid grid-cols-1 gap-3 md:grid-cols-2 lg:grid-cols-4">
          {VINTAGE_DATES.map((v) => (
            <Link
              key={v.date}
              href={`/vintage/${v.date}`}
              className="tile group block hover:border-line-strong"
            >
              <div className="flex items-baseline justify-between">
                <div className="font-mono text-sm text-ink">{v.date}</div>
                {v.badge && <span className="pill-info">{v.badge}</span>}
              </div>
              <div className="mt-1 text-2xs text-ink-muted">{v.label}</div>
              <div className="mt-3 grid grid-cols-2 gap-2">
                <div>
                  <div className="text-2xs uppercase tracking-wide text-ink-subtle">Scenarios</div>
                  <div className="num text-base text-ink">{v.scenarios}</div>
                </div>
                <div>
                  <div className="text-2xs uppercase tracking-wide text-ink-subtle">Forecasts</div>
                  <div className="num text-base text-ink">{v.forecasts}</div>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </section>

      <section className="rounded-sm border border-line bg-bg-elevated p-4">
        <h2 className="font-mono text-sm uppercase tracking-widest text-brand-400">
          URL grammar
        </h2>
        <div className="mt-2 font-mono text-sm text-ink-muted space-y-1">
          <div><code className="text-brand-400">/vintage/YYYY-MM-DD</code> — vintage index for that day</div>
          <div><code className="text-brand-400">/vintage/YYYY-MM-DD/countries/USA</code> — country page at vintage</div>
          <div><code className="text-brand-400">/vintage/YYYY-MM-DD/forecasts</code> — all forecasts published at vintage</div>
          <div><code className="text-brand-400">/vintage/YYYY-MM-DD/scenarios</code> — scenarios triggered at vintage</div>
          <div><code className="text-brand-400">/diff/YYYY-MM-DD..today/forecasts/USA/gdp_yoy</code> — diff one forecast across vintages</div>
        </div>
        <p className="mt-3 text-sm text-ink-muted">
          The vintage-scoped URL is the foundation of everything in OPENGEM. It's how we
          can credibly say "publishes its mistakes" — a miss is a diff between
          <code className="text-brand-400 px-1">forecast(vintage=X, scoring_period=Y)</code> and
          <code className="text-brand-400 px-1">truth(period=Y, source=upstream-agency)</code>,
          and both halves are public URLs.
        </p>
      </section>

      <section className="rounded-sm border border-line bg-bg-elevated p-4 text-sm text-ink-muted">
        <h2 className="font-mono text-sm uppercase tracking-widest text-brand-400">
          What rewinding does NOT do
        </h2>
        <ul className="mt-2 list-inside list-disc space-y-1">
          <li>It does not show what <em>truth</em> was that day — it shows what OPENGEM <em>forecast</em>.</li>
          <li>It does not run the model on today's code against past data ("nowcasting the past"). It surfaces the literal forecast object that was generated.</li>
          <li>Methodology changes since the vintage are documented but not retroactively applied.</li>
        </ul>
      </section>
    </div>
  );
}
