import Link from "next/link";

const TIERS = [
  {
    name: "Public",
    price: "Free",
    sub: "Forever, no signup",
    features: [
      "Full dashboard access — every page, every chart, every vintage",
      "RSS / Atom feeds for events + digest",
      "Embed widgets (with attribution)",
      "Public API: 60 requests/min/IP",
      "MCP server: 100 tool calls/day/IP",
      "Apache-2.0 SDK + CC-BY-4.0 data",
    ],
    cta: "It's already running.",
    href: "/",
    primary: false,
  },
  {
    name: "Pro",
    price: "$29/mo",
    sub: "or $290/yr",
    features: [
      "All Public features",
      "Public API: 1000 requests/min/key",
      "MCP server: 100k tool calls/day/key",
      "White-label embeds (attribution lifted)",
      "Forecast-revision webhooks",
      "Email alerts on scenario triggers",
      "PDF tearsheet exports",
    ],
    cta: "Start 14-day trial",
    href: "/checkout?plan=pro",
    primary: true,
  },
  {
    name: "Pro Team",
    price: "$149/mo",
    sub: "Up to 10 seats",
    features: [
      "All Pro features",
      "Public API: 10k requests/min/team",
      "MCP server: 1M tool calls/day/team",
      "Slack/Teams notifications integration",
      "SSO (SAML) seat invites",
      "Priority email support (24h)",
    ],
    cta: "Start 14-day trial",
    href: "/checkout?plan=team",
    primary: false,
  },
  {
    name: "Sovereign / Enterprise",
    price: "Talk to us",
    sub: "From $2k/mo",
    features: [
      "Dedicated MCP throughput SLA",
      "On-prem container deploy",
      "Custom adapter ingestion",
      "Calibration report subscription",
      "Audit-trail export (SOC2-friendly)",
      "Custom scenario pack co-development",
    ],
    cta: "Email sales",
    href: "mailto:sales@opengem.org",
    primary: false,
  },
];

export default function PricingPage() {
  return (
    <div className="space-y-6 max-w-6xl">
      <header className="border-b border-line pb-4">
        <h1 className="font-mono text-sm uppercase tracking-widest text-ink-muted">
          Pricing
        </h1>
        <p className="mt-2 text-base text-ink">
          Free forever for the substance — every forecast, every miss, every vintage.
          Pay for <em>velocity</em> (throughput, alerts, white-label) and <em>fit</em>
          (enterprise SLAs). Never for secrecy.
        </p>
      </header>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4">
        {TIERS.map((t) => (
          <div
            key={t.name}
            className={[
              "tile flex flex-col",
              t.primary && "border-brand-400 ring-1 ring-brand-400",
            ].filter(Boolean).join(" ")}
          >
            <div className="tile-h">{t.name}</div>
            <div className="mt-2 font-mono text-3xl text-ink">{t.price}</div>
            <div className="mt-1 text-2xs text-ink-subtle">{t.sub}</div>
            <ul className="mt-3 flex-1 space-y-2 text-sm text-ink-muted">
              {t.features.map((f) => (
                <li key={f} className="flex gap-2">
                  <span className="text-brand-400">▸</span>
                  <span>{f}</span>
                </li>
              ))}
            </ul>
            <Link
              href={t.href}
              className={[
                "mt-4 block rounded-sm border px-3 py-2 text-center text-sm",
                t.primary
                  ? "border-brand-400 bg-brand-400 text-bg hover:bg-brand-500"
                  : "border-line bg-bg-overlay hover:border-line-strong",
              ].join(" ")}
            >
              {t.cta}
            </Link>
          </div>
        ))}
      </div>

      <section className="rounded-sm border border-line bg-bg-elevated p-4 text-sm text-ink-muted">
        <h2 className="font-mono text-sm uppercase tracking-widest text-brand-400">
          What we will never charge for
        </h2>
        <ul className="mt-2 list-inside list-disc space-y-1">
          <li>The full forecast track record. Already free.</li>
          <li>Reading any historical vintage. Already free.</li>
          <li>Reading the miss log. Already free.</li>
          <li>Reading the methodology. Already free.</li>
          <li>Forking the entire codebase. Apache-2.0.</li>
          <li>Republishing derived metrics under CC-BY-4.0 attribution.</li>
        </ul>
        <p className="mt-3">
          The Pro tier exists because some users need 100x the throughput, branded
          embeds, or enterprise SLAs. Those needs are real — but they are needs of{" "}
          <em>scale and fit</em>, not <em>substance</em>. The data and the methodology
          stay free.
        </p>
      </section>

      <section className="text-2xs text-ink-subtle">
        Live API status on the public dashboard: 99.9% trailing 30-day uptime, P50
        response 35ms, P99 response 280ms. Numbers updated every 5 minutes from our
        Prometheus dump (also open).
      </section>
    </div>
  );
}
