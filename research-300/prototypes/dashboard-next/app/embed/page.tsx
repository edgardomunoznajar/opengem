import Link from "next/link";

const SIZES = [
  { name: "Square", w: 200, h: 200, kind: "recession_prob", country: "USA", desc: "Single indicator, big number + sparkline + vintage badge." },
  { name: "Banner", w: 600, h: 120, kind: "forecast", country: "DEU", indicator: "gdp_yoy", desc: "Row of 3 indicators. Good for newsletter mastheads." },
  { name: "Tall",  w: 300, h: 420, kind: "forecast", country: "CHN", indicator: "gdp_yoy", desc: "Full chart + consensus overlay + miss-log link." },
];

export default function EmbedPage() {
  return (
    <div className="space-y-6 max-w-4xl">
      <header className="border-b border-line pb-4">
        <h1 className="font-mono text-sm uppercase tracking-widest text-ink-muted">
          Embeds
        </h1>
        <p className="mt-2 text-base text-ink">
          Drop OPENGEM tiles into your blog, newsletter, or YouTube channel description.
          Three sizes. One script tag. Every embed includes a vintage badge — that's the deal.
        </p>
      </header>

      <section>
        <h2 className="mb-2 font-mono text-sm uppercase tracking-widest text-ink-muted">
          Quick start
        </h2>
        <pre className="overflow-x-auto rounded-sm border border-line bg-bg-elevated p-3 font-mono text-xs">
{`<div data-opengem
     data-kind="recession_prob"
     data-country="USA"
     data-size="square"></div>
<script src="https://opengem.org/embed.js" defer></script>`}
        </pre>
      </section>

      {SIZES.map((s) => (
        <section key={s.name}>
          <h2 className="mb-2 font-mono text-sm uppercase tracking-widest text-ink-muted">
            {s.name} — {s.w}×{s.h}
          </h2>
          <p className="mb-2 text-sm text-ink-muted">{s.desc}</p>
          <pre className="overflow-x-auto rounded-sm border border-line bg-bg-elevated p-3 font-mono text-xs">
{`<div data-opengem
     data-kind="${s.kind}"
     data-country="${s.country}"
${s.indicator ? `     data-indicator="${s.indicator}"\n` : ""}     data-size="${s.name.toLowerCase()}"></div>`}
          </pre>
        </section>
      ))}

      <section className="rounded-sm border border-line bg-bg-elevated p-4 text-sm text-ink-muted">
        <h2 className="font-mono text-sm uppercase tracking-widest text-brand-400">
          The embed contract
        </h2>
        <ul className="mt-2 list-inside list-disc space-y-1">
          <li>The vintage badge stays. No customization or hiding.</li>
          <li>The "OPENGEM" link stays. No removal.</li>
          <li>Numbers shown match the API at fetch time — no client-side derivation.</li>
          <li>If our API is unreachable, the tile shows a friendly "—" rather than guessing.</li>
          <li>Apache-2.0 — fork the SDK, white-label only on the Pro tier (which removes the brand link).</li>
        </ul>
      </section>

      <section>
        <Link href="/pricing" className="text-info underline">
          Pro embeds — branded, custom palette, SLA →
        </Link>
      </section>
    </div>
  );
}
