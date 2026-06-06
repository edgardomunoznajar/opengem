import Link from "next/link";

export default function AboutPage() {
  return (
    <div className="space-y-8 max-w-3xl">
      <header className="border-b border-line pb-4">
        <h1 className="font-mono text-sm uppercase tracking-widest text-ink-muted">
          About OPENGEM
        </h1>
      </header>

      <section>
        <h2 className="text-xl text-ink mb-2">What this is</h2>
        <p className="font-serif text-base leading-relaxed text-ink-muted">
          OPENGEM (Open Geopolitical-Economic Modeling) is a public macro-accountability
          ledger for the world economy — a Bloomberg-grade dashboard for everyone,
          where every forecast is open, every number is dated, every miss is named.
        </p>
        <p className="mt-3 font-serif text-base leading-relaxed text-ink-muted">
          It is an open-source alternative to Stratfor, NiGEM, Oxford GEM, and the
          forecasting cartel at the IMF and OECD — not by claiming to be more accurate
          (we don't), but by being structurally honest about what we got wrong, when, and why.
        </p>
      </section>

      <section>
        <h2 className="text-xl text-ink mb-2">The asymmetry</h2>
        <p className="font-serif text-base leading-relaxed text-ink-muted">
          The forecasting incumbents — IMF WEO, OECD EO, Bloomberg Economics, Goldman GIR,
          JPM Macro — produce <em>priced</em> forecasts. Their track records are private.
          Their margins depend on opacity. They cannot publish their full calibration
          without exposing why the customer is paying.
        </p>
        <p className="mt-3 font-serif text-base leading-relaxed text-ink-muted">
          OPENGEM has no margins to protect. So it can publish every vintage of every
          forecast it has ever made, every backtest with every cell of the V&amp;V matrix
          open, every model card with every assumption named, and every miss with a
          post-mortem in the same place the original was published.
        </p>
        <p className="mt-3 font-serif text-base leading-relaxed text-ink-muted">
          That asymmetry is the moat. A system that publishes its mistakes is harder to
          discredit than a system that hides them.
        </p>
      </section>

      <section>
        <h2 className="text-xl text-ink mb-2">Who built this</h2>
        <p className="font-serif text-base leading-relaxed text-ink-muted">
          OPENGEM is a single-developer project by Edgardo Muñoz Najar — a guerrilla
          developer following the thesis that consumer-grade open-source tools can
          replace legacy SaaS at fractional cost. OPENGEM is part of the oblique suite
          (anvil, weaver, oracle, thinker, seer, plan).
        </p>
        <p className="mt-3 font-serif text-base leading-relaxed text-ink-muted">
          Apache-2.0 code, CC-BY-4.0 data. All forecasts, all backtests, all methodology
          public. Contributions welcome on{" "}
          <Link href="https://github.com/opengem/opengem" className="underline hover:text-ink">
            GitHub
          </Link>.
        </p>
      </section>

      <section>
        <h2 className="text-xl text-ink mb-2">Quick links</h2>
        <ul className="space-y-2 text-sm">
          <li><Link href="/methodology" className="underline hover:text-ink">Methodology</Link> — how forecasts are built and scored</li>
          <li><Link href="/accountability" className="underline hover:text-ink">Accountability ledger</Link> — every forecast, every miss</li>
          <li><Link href="/about/governance" className="underline hover:text-ink">Governance</Link> — editorial values + decision discipline</li>
          <li><Link href="/about/changelog" className="underline hover:text-ink">Changelog</Link> — what's changed, when, why</li>
          <li><Link href="/mcp" className="underline hover:text-ink">MCP server</Link> — for LLM grounding workflows</li>
          <li><Link href="/api" className="underline hover:text-ink">API</Link> — for analyst pipelines</li>
        </ul>
      </section>
    </div>
  );
}
