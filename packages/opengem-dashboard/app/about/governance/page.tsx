import Link from "next/link";

export default function GovernancePage() {
  return (
    <div className="space-y-8 max-w-3xl">
      <header className="border-b border-line pb-4">
        <h1 className="font-mono text-sm uppercase tracking-widest text-ink-muted">
          Governance
        </h1>
        <p className="mt-2 text-base text-ink">
          The editorial values and decision discipline OPENGEM publishes against.
        </p>
      </header>

      <section>
        <h2 className="text-xl text-ink mb-2">The five commitments</h2>
        <ol className="space-y-3 font-serif text-base leading-relaxed text-ink-muted list-decimal pl-5">
          <li>
            <strong className="text-ink">Vintage permanence.</strong> Every published
            forecast is permanent. No silent retract, no edit-in-place. If we change method,
            we publish a new vintage with a forward link.
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
            data-lockfile hash, container digest, generated-at timestamp. Anyone can
            replay any vintage.
          </li>
          <li>
            <strong className="text-ink">Calibration is a target.</strong> The ledger
            commits to ≤20% out-of-band rate at the 80% band. When it drifts above,
            we say so on the{" "}
            <Link href="/accountability" className="underline hover:text-ink">accountability page</Link>.
          </li>
        </ol>
      </section>

      <section>
        <h2 className="text-xl text-ink mb-2">Sponsorship policy</h2>
        <p className="font-serif text-base leading-relaxed text-ink-muted">
          OPENGEM does not accept sponsorship that creates an editorial dependency on the
          sponsor. We will accept underwriting that funds engineering capacity for
          publicly-disclosed work items, on the condition that:
        </p>
        <ul className="mt-3 space-y-1 font-serif text-base text-ink-muted list-disc pl-5">
          <li>The work item is on the public roadmap.</li>
          <li>The sponsor's identity is published.</li>
          <li>The sponsor has no editorial review.</li>
          <li>OPENGEM retains the right to publish negative findings about the sponsor.</li>
        </ul>
      </section>

      <section>
        <h2 className="text-xl text-ink mb-2">Anti-personas</h2>
        <p className="font-serif text-base leading-relaxed text-ink-muted">
          OPENGEM is not built for, and will not preferentially serve:
        </p>
        <ul className="mt-3 space-y-1 font-serif text-base text-ink-muted list-disc pl-5">
          <li>Day-trading or intraday market-data consumers (wrong cadence).</li>
          <li>Securities-advice generation (we publish numbers, not recommendations).</li>
          <li>Nation-state intelligence buyers (we do not target individuals or entities).</li>
          <li>Military command-and-control systems (we provide a public signal, not a kill chain).</li>
        </ul>
        <p className="mt-3 font-serif text-base leading-relaxed text-ink-muted">
          The dashboard is open; the data is open. If our work nonetheless ends up
          informing a use we object to, our recourse is editorial transparency, not
          legal restraint.
        </p>
      </section>

      <section>
        <h2 className="text-xl text-ink mb-2">Funding</h2>
        <p className="font-serif text-base leading-relaxed text-ink-muted">
          OPENGEM is self-funded by{" "}
          <Link href="/pricing" className="underline hover:text-ink">paid tier revenue</Link>{" "}
          (Pro, Pro Team, Sovereign). Free tier substance is paid for by Pro tier velocity.
          We do not seek venture funding, do not have institutional investors, and do not
          plan to take equity from any party that would acquire editorial control.
        </p>
      </section>

      <section>
        <h2 className="text-xl text-ink mb-2">Contact</h2>
        <p className="font-serif text-base leading-relaxed text-ink-muted">
          Editorial / corrections / disputes: hello@opengem.org<br />
          Sales / enterprise: sales@opengem.org<br />
          Security: security@opengem.org<br />
          GPG: published on the{" "}
          <Link href="https://github.com/opengem/opengem/blob/main/SECURITY.md" className="underline hover:text-ink">
            SECURITY.md
          </Link>{" "}
          page of the repository.
        </p>
      </section>
    </div>
  );
}
