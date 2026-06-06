import Link from "next/link";
import { cn } from "@/lib/utils";

const PUBLISHED = 14_283;
const SCORED = 11_902;
const MISSED = 2_117;
const PENDING = 264;

const RECENT_MISSES = [
  {
    vintage: "2025-Q2",
    country: "USA",
    indicator: "gdp_yoy",
    horizon: "4Q",
    forecast: 1.4,
    actual: 2.6,
    miss: 1.2,
    rmse_rank: 47,
    why: "Persistent Q1-2025 revisions pushed GDP surprise outside our 80% band; component DFM under-weighted services consumption.",
    postmortem: "/postmortem/usa-gdp-2025q2",
  },
  {
    vintage: "2025-Q1",
    country: "DEU",
    indicator: "cpi_yoy",
    horizon: "1Q",
    forecast: 2.1,
    actual: 1.4,
    miss: -0.7,
    rmse_rank: 92,
    why: "Energy passthrough faded faster than expected; food-component model lagged dataflow.",
    postmortem: "/postmortem/deu-cpi-2025q1",
  },
  {
    vintage: "2024-Q4",
    country: "JPN",
    indicator: "policy_rate",
    horizon: "2Q",
    forecast: 0.5,
    actual: 0.25,
    miss: -0.25,
    rmse_rank: 18,
    why: "BoJ tightening path priors were too aggressive given persistent wage softness.",
    postmortem: "/postmortem/jpn-policy-2024q4",
  },
];

export default function AccountabilityPage() {
  return (
    <div className="space-y-6">
      <header className="border-b border-line pb-4">
        <h1 className="font-mono text-sm uppercase tracking-widest text-ink-muted">
          Accountability ledger
        </h1>
        <p className="mt-2 text-base text-ink">
          Every forecast OPENGEM has ever published. Scored against truth at horizon.
          Misses are not retracted — they are post-mortemed in place. This is the page
          that doesn't exist anywhere else.
        </p>
      </header>

      <section className="grid grid-cols-2 gap-3 md:grid-cols-4">
        <div className="tile">
          <div className="tile-h">Forecasts published</div>
          <div className="tile-v">{PUBLISHED.toLocaleString()}</div>
          <div className="mt-1 text-2xs text-ink-subtle">since 2024-Q1</div>
        </div>
        <div className="tile">
          <div className="tile-h">Scored</div>
          <div className="tile-v">{SCORED.toLocaleString()}</div>
          <div className="mt-1 text-2xs text-good">
            {((SCORED / PUBLISHED) * 100).toFixed(1)}% of publishable
          </div>
        </div>
        <div className="tile">
          <div className="tile-h">Outside band (miss)</div>
          <div className="tile-v">{MISSED.toLocaleString()}</div>
          <div className="mt-1 text-2xs text-bad">
            {((MISSED / SCORED) * 100).toFixed(1)}% (target: ≤20%)
          </div>
        </div>
        <div className="tile">
          <div className="tile-h">Pending scoring</div>
          <div className="tile-v">{PENDING.toLocaleString()}</div>
          <div className="mt-1 text-2xs text-ink-subtle">awaiting truth print</div>
        </div>
      </section>

      <section>
        <h2 className="mb-2 font-mono text-sm uppercase tracking-widest text-ink-muted">
          Recent misses — top 3 by magnitude
        </h2>
        <div className="overflow-x-auto rounded-sm border border-line bg-bg-elevated">
          <table className="min-w-full text-sm">
            <thead className="border-b border-line text-2xs uppercase tracking-wide text-ink-subtle">
              <tr>
                <th className="px-3 py-2 text-left">Vintage</th>
                <th className="px-3 py-2 text-left">Country</th>
                <th className="px-3 py-2 text-left">Indicator</th>
                <th className="px-3 py-2 text-left">H</th>
                <th className="px-3 py-2 text-right">Forecast</th>
                <th className="px-3 py-2 text-right">Actual</th>
                <th className="px-3 py-2 text-right">Miss</th>
                <th className="px-3 py-2 text-left">Why</th>
                <th className="px-3 py-2 text-left">Post-mortem</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-line">
              {RECENT_MISSES.map((m) => (
                <tr key={`${m.country}-${m.vintage}-${m.indicator}`} className="hover:bg-bg-overlay align-top">
                  <td className="px-3 py-2 font-mono text-2xs text-ink-muted">{m.vintage}</td>
                  <td className="px-3 py-2 font-mono">{m.country}</td>
                  <td className="px-3 py-2 font-mono text-2xs">{m.indicator}</td>
                  <td className="px-3 py-2 font-mono text-2xs">{m.horizon}</td>
                  <td className="px-3 py-2 text-right num text-ink-muted">{m.forecast.toFixed(1)}%</td>
                  <td className="px-3 py-2 text-right num text-ink">{m.actual.toFixed(1)}%</td>
                  <td className={cn("px-3 py-2 text-right num", m.miss > 0 ? "text-good" : "text-bad")}>
                    {m.miss > 0 ? "+" : ""}{m.miss.toFixed(1)}
                  </td>
                  <td className="px-3 py-2 text-2xs text-ink-muted max-w-md">{m.why}</td>
                  <td className="px-3 py-2 text-2xs">
                    <Link href={m.postmortem} className="text-info underline">read</Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="mt-2 text-2xs text-ink-subtle">
          Every miss above has its own URL. The URL was assigned <em>before</em> we knew
          we'd miss. That's the promise.
        </div>
      </section>

      <section className="rounded-sm border border-line bg-bg-elevated p-4">
        <h2 className="font-mono text-sm uppercase tracking-widest text-brand-400">
          The publication discipline
        </h2>
        <ul className="mt-2 space-y-2 font-serif text-base leading-relaxed text-ink-muted">
          <li>
            <strong className="text-ink">Vintage permanence.</strong> Every published
            forecast is permanent. No silent retract, no edit-in-place. If we change
            method, we publish a new vintage with a forward link.
          </li>
          <li>
            <strong className="text-ink">Miss-in-place.</strong> A missed forecast doesn't
            leave the page it was on. A post-mortem appears below it.
          </li>
          <li>
            <strong className="text-ink">Consensus side-by-side.</strong> Every forecast
            shows WEO, OECD EO, FRB SEP, ECB SPF where available — so a miss is visible
            in context.
          </li>
          <li>
            <strong className="text-ink">Reproducibility envelope.</strong> Git SHA,
            data lockfile hash, container digest, generated-at timestamp. Anyone can
            replay any vintage.
          </li>
          <li>
            <strong className="text-ink">Calibration is a target.</strong> The ledger
            commits to ≤20% out-of-band rate at the 80% band. When it drifts above,
            we say so on this page.
          </li>
        </ul>
      </section>
    </div>
  );
}
