import Link from "next/link";
import { notFound } from "next/navigation";

const TOPICS: Record<string, { title: string; body: string; sources: string[] }> = {
  "scoring": {
    title: "Forecast scoring methodology",
    body: `Every published forecast is scored against truth using CRPS as the canonical proper scoring rule, with auxiliary metrics PIT (calibration), MAE, RMSE, hit-rate (within 80% band), and Diebold-Mariano p-value vs an AR(1) baseline and a random-walk baseline.

CRPS penalizes both point error and band misspecification — wide, vague bands are not free. A model that produces P10-P90 of [-∞, +∞] has perfect calibration at every PIT bucket but a CRPS that is unbounded large. That is the right tradeoff for a model card: be confident, but be calibrated, or be honest about not knowing.

The 17-cell V&V matrix (country × horizon for the canonical 6 indicators) is the publication gate. A model variant that fails ≥4 of its critical cells does not get publish status until it is post-mortemed in writing.`,
    sources: ["Gneiting & Raftery 2007", "Diebold & Mariano 1995", "OPENGEM R08 V&V matrix"],
  },
  "recession-prob-us": {
    title: "US recession probability methodology",
    body: `OPENGEM publishes a Bauer-Mertens-style term-spread probit, fit on monthly H.15 data with the 10-year minus 3-month spread as the canonical predictor and a labor-market surprise as the secondary input.

The output is a 12-month-ahead conditional probability of NBER-dated recession start. Calibration against post-1985 history holds at PIT 0.78 (target ≥0.75).

We do not regress on additional ad-hoc predictors during regime changes — that is a backtest-overfitting trap. If the model misses, the post-mortem reports the miss; we do not retro-fit predictors to make it look like we wouldn't have missed.`,
    sources: ["Bauer & Mertens (Fed) 2018", "Estrella & Mishkin 1998", "FRB H.15 daily series"],
  },
  "gpr-nowcast": {
    title: "Geopolitical Risk (GPR) nowcast methodology",
    body: `OPENGEM extends the Caldara-Iacoviello GPR family with: (a) daily-cadence GPR-D from a Cline Center Global News Index features subset, (b) per-country GPR-C heatmap rolled from POLECAT PLOVER-coded event aggregates with Goldstein-Scale weighting, (c) category breakdowns (military, war, terror) attributed to subindices.

The nowcast uses our own composite indicator constructed from POLECAT (CC0) + GDELT GKG (free with attribution) + UCDP (CC-BY-4.0). This avoids any dependency on Iacoviello's monthly drop or on Factiva-equivalent paid corpora. The composite is back-tested against the original GPR over 1985-2024 with R² ≥ 0.92.`,
    sources: ["Caldara & Iacoviello (Fed) 2022", "Cline Center POLECAT", "GDELT GKG 2.0", "UCDP datasets"],
  },
  "l3-dfm-bma-v0-4": {
    title: "L3 model card — DFM + BMA combiner (v0.4)",
    body: `L3 is OPENGEM's workhorse forecast layer: a 6-factor Dynamic Factor Mixed-Frequency model (Bok et al. NY Fed framework, native in statsmodels) combined via Bayesian Model Averaging with two BVAR variants (Minnesota prior, sum-of-coefficients prior) and a small neural ensemble (Nixtla neuralforecast: NHITS + NBEATSx).

BMA weights are computed on a rolling 24-month CRPS, re-normalized to keep total weight = 1. No single component is allowed weight ≥0.6 (defensive against over-concentration).

Training set: vintage-correct upstream-agency releases for Tier-V economies, BEA NIPA + BLS CPI/payrolls + FRB H.15 + Treasury FiscalData + Census M3 + OECD ORDRA + BIS CBPOL.`,
    sources: ["Bok et al. (NY Fed) 2017", "statsmodels.tsa.statespace.DynamicFactorMQ", "Nixtla neuralforecast", "Litterman 1986 (Minnesota prior)"],
  },
};

interface PageProps {
  params: Promise<{ topic: string }>;
}

export default async function MethodologyTopicPage({ params }: PageProps) {
  const { topic } = await params;
  const t = TOPICS[topic];
  if (!t) notFound();

  return (
    <div className="space-y-6 max-w-3xl">
      <header className="border-b border-line pb-4">
        <div className="font-mono text-2xs uppercase tracking-wider text-ink-subtle">METHODOLOGY</div>
        <h1 className="text-2xl text-ink">{t.title}</h1>
      </header>

      <section>
        <p className="whitespace-pre-line font-serif text-base leading-relaxed text-ink-muted">
          {t.body}
        </p>
      </section>

      <section className="rounded-sm border border-line bg-bg-elevated p-4">
        <h2 className="font-mono text-sm uppercase tracking-widest text-brand-400 mb-2">
          References
        </h2>
        <ul className="space-y-1 text-sm text-ink-muted">
          {t.sources.map((s) => <li key={s}>· {s}</li>)}
        </ul>
      </section>

      <section className="flex gap-3 text-2xs">
        <Link href="/methodology" className="pill-info">methodology index</Link>
        <Link href="/accountability" className="pill-info">accountability ledger</Link>
        <Link href="https://github.com/opengem/opengem" className="pill-info">replication code</Link>
      </section>
    </div>
  );
}
