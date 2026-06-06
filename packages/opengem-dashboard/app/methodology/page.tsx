import Link from "next/link";

const SECTIONS = [
  {
    h: "What we forecast",
    body: `Tier-V (vintage-correct) covers ~22-35 economies with full vintage backtest discipline. Tier-T (tracked-only) covers ~110 additional economies with current-snapshot data but no vintage replay. The forecast critical path is the L3 workhorse: a dynamic factor model + Bayesian VAR + ML ensemble combined by BMA. L1 is a US-only narrative satellite. L2 is an annual BGVAR spillover layer.`,
  },
  {
    h: "How we score",
    body: `Every forecast is scored against truth using CRPS, log-score, PIT, MAE, RMSE, and hit-rate. Diebold-Mariano tests compare against an AR(1) baseline. The leaderboard is sorted by CRPS, with PIT calibration shown as a secondary column. A 17-cell V&V matrix (country × indicator × horizon) is the publication gate.`,
  },
  {
    h: 'What "publishes its mistakes" means',
    body: `Every forecast vintage is permanent. When a forecast misses, a post-mortem appears at the same URL, dated, signed, and linked to the original forecast. The miss-log is paginated and searchable. There is no quiet retract.`,
  },
  {
    h: "What we don't claim",
    body: `OPENGEM does not claim higher accuracy than the cartel at internal verification — it claims higher transparency. Where the V&V matrix shows we lose to consensus, that cell is published as "loses to consensus on X% of countries" rather than buried.`,
  },
  {
    h: "Reproducibility envelope",
    body: `Every forecast object carries: git_sha (the code at the time), data_lockfile_hash (the input data), container_digest (the runtime), generated_at (the moment). Anyone can replay a vintage by checking out that git_sha, restoring the data lockfile, and running the container.`,
  },
];

export default function MethodologyPage() {
  return (
    <div className="space-y-8 max-w-3xl">
      <header className="border-b border-line pb-4">
        <h1 className="font-mono text-sm uppercase tracking-widest text-ink-muted">
          Methodology
        </h1>
        <p className="mt-2 text-base text-ink">
          What OPENGEM forecasts, how, and what we are honest about not being able to do.
        </p>
      </header>

      {SECTIONS.map((s) => (
        <section key={s.h}>
          <h2 className="mb-2 text-xl text-ink">{s.h}</h2>
          <p className="font-serif text-base leading-relaxed text-ink-muted">{s.body}</p>
        </section>
      ))}

      <section className="rounded-sm border border-line bg-bg-elevated p-4 text-sm text-ink-muted">
        Deep design dossier:{" "}
        <Link href="https://github.com/opengem/opengem/tree/main/docs/design" className="underline hover:text-ink">
          docs/design
        </Link>
        {" · "}
        Research memos:{" "}
        <Link href="https://github.com/opengem/opengem/tree/main/docs/research" className="underline hover:text-ink">
          docs/research
        </Link>
      </section>
    </div>
  );
}
