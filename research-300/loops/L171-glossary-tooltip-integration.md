# L171 — Glossary Tooltip Integration

**Loop**: 171 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The thesis

A YouTuber lands on the OPENGEM dashboard and sees "CRPS 0.42" next to "PIT 0.71." If those acronyms don't unpack on hover, we lost the user. Macro is full of jargon; we make every term hoverable.

This is the bridge from "real analyst tool" to "anyone can use it."

## The mechanism

Every glossary-eligible term in the UI is wrapped with `<Glossary term="...">`. The component renders:
- A subtle dotted underline (text-decoration: dotted, color: text-tertiary)
- A `?` icon for the truly opaque acronyms (CRPS, SAAR, P50, etc.)
- On hover: a Tooltip (per L150) with definition + a "more →" link

Click "more →" routes to `/glossary#<term>`.

## The catalog (150 terms)

Organized by category. Each term has: definition (≤30 words), formula/example (optional), 1-2 sentence narrative, source reference.

### Forecasting / scoring

- **Nowcast** — A forecast for the current observation period before the official release.
- **CRPS** — Continuous Ranked Probability Score. Lower is better. Measures the entire forecast distribution against the observed value.
- **PIT** — Probability Integral Transform. A uniformly-distributed score; 0.5 means median-correct.
- **MAE** — Mean Absolute Error.
- **RMSE** — Root Mean Squared Error.
- **Brier score** — Probability forecast accuracy metric for binary outcomes. Lower is better.
- **P10, P50, P90** — 10th, 50th (median), 90th percentile of a forecast distribution.
- **Fan chart** — Forecast visualization showing probability bands around a central estimate.
- **Consensus** — Median forecast across a group of forecasters.
- **Vintage** — A specific historical version of a dataset or forecast.
- **Backtest** — Running a model on historical data to evaluate performance.
- **Calibration** — Whether forecast probabilities match observed frequencies.
- **In-sample / out-of-sample** — Data used to fit a model vs. data used to evaluate it.
- **Walk-forward** — A backtest strategy that refits the model at each time step.
- **Stacking** — Combining multiple forecasts using a meta-model.
- **Ensemble** — A collection of models whose outputs are combined.

### Macro indicators

- **GDP** — Gross Domestic Product.
- **CPI** — Consumer Price Index.
- **PPI** — Producer Price Index.
- **Core inflation** — Inflation excluding volatile components (typically food and energy).
- **Y/Y** — Year-over-year change.
- **M/M** — Month-over-month change.
- **Q/Q** — Quarter-over-quarter change.
- **SAAR** — Seasonally Adjusted Annual Rate.
- **NFP** — Non-Farm Payrolls (US monthly employment release).
- **NAIRU** — Non-Accelerating Inflation Rate of Unemployment.
- **PMI** — Purchasing Managers' Index. >50 expansion, <50 contraction.
- **GDPNow** — Atlanta Fed's GDP nowcasting model.
- **Output gap** — Difference between actual and potential GDP.
- **Potential GDP** — The maximum sustainable level of output.
- **Real / nominal** — Inflation-adjusted vs. unadjusted.
- **Recession** — Two consecutive quarters of negative GDP growth (informal); NBER official designation.
- **Stagflation** — Simultaneous high inflation and low growth.

### Yield curve

- **Yield curve** — Plot of bond yields against maturity.
- **Term spread** — Difference between long and short-maturity yields (e.g., 10Y - 2Y).
- **Inverted curve** — When short yields exceed long yields.
- **Steep curve** — When long yields significantly exceed short yields.
- **Forward rate** — Implied future spot rate from current yields.
- **OIS** — Overnight Index Swap. Reflects market expectations for the policy rate.
- **TIPS** — Treasury Inflation-Protected Securities.
- **Break-even** — TIPS-derived inflation expectation.
- **Real yield** — Yield adjusted for expected inflation.

### Monetary policy

- **Policy rate** — Central bank's primary interest rate.
- **FOMC** — Federal Open Market Committee (US Fed).
- **ECB** — European Central Bank.
- **BoE** — Bank of England.
- **BoJ** — Bank of Japan.
- **QE** — Quantitative Easing.
- **QT** — Quantitative Tightening.
- **Dot plot** — FOMC participants' rate projections chart.
- **SEP** — Summary of Economic Projections (FOMC).
- **Reaction function** — Rule describing how a central bank sets policy.
- **Taylor rule** — A common reaction function based on inflation and output gap.
- **Forward guidance** — Central bank communication about future policy.

### Geopolitics

- **GDELT** — Global Database of Events, Language, and Tone.
- **GKG** — Global Knowledge Graph (GDELT).
- **ACLED** — Armed Conflict Location & Event Data.
- **GPR** — Geopolitical Risk index (Caldara-Iacoviello).
- **Goldstein scale** — Conflict-cooperation score per event.
- **Tone** — Sentiment score for news text.
- **CAMEO** — Conflict and Mediation Event Observations (event taxonomy).
- **UCDP** — Uppsala Conflict Data Program.
- **V-Dem** — Varieties of Democracy.
- **Sanctions** — Restrictive measures imposed by one state on another.

### Trade & supply chain

- **GSCPI** — Global Supply Chain Pressure Index.
- **Comtrade** — UN trade statistics database.
- **BACI** — CEPII's bilateral trade dataset.
- **TEU** — Twenty-foot Equivalent Unit (container measure).
- **Choke point** — Geographic constraint on trade routes.
- **Hormuz / Malacca / Suez / Bab-el-Mandeb / Panama / Bosporus** — Major maritime chokes.
- **PortWatch** — IMF's port congestion dataset.
- **AIS** — Automatic Identification System (vessel tracking).
- **Trade balance** — Exports minus imports.
- **Current account** — Trade plus net factor income.

### Financial / FX

- **REER** — Real Effective Exchange Rate.
- **NEER** — Nominal Effective Exchange Rate.
- **DXY** — US Dollar Index.
- **PPP** — Purchasing Power Parity.
- **Carry trade** — Borrowing low-yield, lending high-yield.
- **Reserve currency** — Currency held by central banks for reserves.
- **CDS** — Credit Default Swap.
- **Sovereign rating** — Credit rating of a country's debt.
- **Bps / Basis point** — 1/100 of a percentage point.
- **FX intervention** — Central bank action in currency markets.

### Modeling

- **DFM** — Dynamic Factor Model.
- **BVAR** — Bayesian Vector Autoregression.
- **MIDAS** — Mixed-Data Sampling regression.
- **VAR** — Vector Autoregression.
- **DSGE** — Dynamic Stochastic General Equilibrium.
- **HMM** — Hidden Markov Model.
- **State-space model** — A class of models with latent dynamics.
- **Kalman filter** — Algorithm for state-space inference.
- **Bayesian model averaging** — Combining models weighted by posterior probability.
- **Shrinkage** — Regularization that pulls estimates toward a prior.
- **Hyperparameter** — A parameter of a model that isn't learned from data.

### Sentiment / news

- **Sentiment score** — Numerical representation of text tone.
- **Topic model** — A method to discover themes in text.
- **News tone** — Aggregated sentiment over a corpus of news.
- **Event extraction** — Identifying events from unstructured text.

### Open data / API

- **SDMX** — Statistical Data and Metadata eXchange.
- **REST API** — Architectural style for web services.
- **MCP** — Model Context Protocol.
- **Provenance** — Origin and history of data.
- **Lineage** — The chain of transformations from source to derived data.
- **Catalog** — A registry of available datasets.

### Misc

- **Quartile / decile / percentile** — Distribution positions.
- **Z-score** — Standardized score (number of standard deviations from mean).
- **Confidence interval** — Range capturing the true value with a stated probability.
- **EMA** — Exponentially-weighted Moving Average.
- **Half-life** — Time for an EMA to decay by half.
- **Heteroskedasticity** — Non-constant variance.
- **Cointegration** — Two series sharing a common stochastic trend.
- **Stationarity** — Statistical properties don't change over time.
- **Lag / lead** — Earlier / later in time relative to a reference point.

## The catalog as a page

`/glossary`:

```
   Glossary
   ──────────────────────────────────
   [Search]   [Filter by category ▼]

   A
     ACLED — Armed Conflict Location & Event Data...
     AIS — Automatic Identification System...
   B
     Backtest — Running a model on historical data...
     ...
```

Each entry is anchored: `/glossary#crps` deep-links.

Each entry has:
- Definition
- Formula (where applicable, rendered LaTeX-style via KaTeX)
- 2-sentence narrative
- "Used in" — links to pages that use this term
- "Related terms" — links to siblings

## The integration

Every page renders text via React components. Glossary-eligible terms are wrapped:

```tsx
<p>OPENGEM scored a <Glossary term="crps">CRPS</Glossary> of 0.42 on...</p>
```

The `<Glossary>` component:
- Renders the text with a dotted underline
- On hover (after 300ms): tooltip with definition + "more →" link
- On focus (keyboard): same
- Click: opens the glossary page anchored at the term

Bundle: the glossary data is embedded as a JSON manifest at build time (~25KB gzipped — small enough to inline).

## Auto-detection (V2)

V1: terms must be manually wrapped. Discipline.

V2: a build-time linter scans text content and auto-wraps known terms. Authors can opt out per-term with a comment.

## Translation strategy

Glossary entries are translated per language (when i18n lands per L118). Each term has a `translations` field.

For V1: English only.

## Authoring contract

Adding a glossary term requires:
1. PR to `glossary/terms.json5`
2. Definition under 30 words
3. At least one usage site identified
4. Optional formula in LaTeX

A linter checks for term collisions and orphaned entries.

## MCP exposure

The MCP server exposes `glossary.lookup(term)` returning the definition + narrative. LLM agents can use this to ground their explanations.

## "Explain like I'm 5" mode

A toggle in the user settings: "Plain language tooltips." When enabled, the `<Glossary>` component renders the narrative instead of the definition. Useful for the prosumer cohort (L003).

V2 — V1 ships the definition only.

## Performance

- All term lookups are local (catalog in browser memory)
- Tooltips mount in <8ms
- No fetches on hover

## Anti-patterns avoided

- Every word linked. Visual noise. We wrap only the genuinely opaque terms.
- Inline definitions in parentheses. Doesn't scale; clutters body text.
- Modal on click. Too aggressive — the hover should answer 95% of questions.
- Auto-tooltip on first scroll. Annoying.

## The asymmetric move

Bloomberg's glossary is paywalled. Wikipedia's is community-curated but unreliable. OPENGEM's glossary is:
- Open (CC-BY-4.0)
- Curated by people who know
- Integrated into the surfaces where the term appears
- Available via MCP for LLM agents
- Cite-able (each term has a permanent URL)

The asymmetric weapon is: when a journalist needs to define "PIT" in an article, they can paste the OPENGEM glossary URL.
