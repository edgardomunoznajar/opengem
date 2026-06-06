# L012 — Qlib (Microsoft): Deep Dive

**Loop**: 012 / 300
**Phase**: 1 — Open-source landscape survey
**Date**: 2026-06-06

---

## The repo at a glance

- **GitHub**: [github.com/microsoft/qlib](https://github.com/microsoft/qlib)
- **Stars**: ~44.1k, ~7k+ forks. Second-largest open-source quant repo on GitHub after OpenBB.
- **License**: **MIT**. No contamination risk. Friendly for Apache-2.0 redistribution.
- **Primary language**: Python (~95%) with Cython hotspots.
- **Last commit**: April 2026. Active, but the cadence has slowed since 2024 — Microsoft's quant research team appears to have shifted compute to the RD-Agent (linked from Qlib's README), an LLM-driven research automation system. Qlib itself is "mature, in selective-improvement mode," not "burning hot."
- **Homepage**: qlib.readthedocs.io

## What it actually is

Qlib is **an end-to-end equity-research and equity-execution stack**. The architecture has four layers:

1. **Data layer (`qlib.data`)** — a custom on-disk columnar binary format ("Qlib data format"), an `Expression Engine` for declaring features as DSL strings (`Ref($close,1)/$close - 1`), and a `Cache` system to memoize. The data layer is the *one piece* of Qlib that is genuinely reusable outside of equity.
2. **Model zoo (`qlib.contrib.model`)** — 20+ models: LightGBM, CatBoost, XGBoost, MLP, LSTM, GRU, ALSTM (attention-LSTM), Transformer, TabNet, TCN, GATS (Graph Attention Time Series), TFT (Temporal Fusion Transformer), HIST (HIerarchical Stock Trends), KRNN, AdaRNN, Sandwich, Double Ensemble. Some are deeply equity-specific (TRA, IGMTF, HIST — all built around stock-level cross-section); most are generic time-series learners that happen to be wired into Qlib's pipeline.
3. **Workflow (`qlib.workflow`)** — declarative YAML configs that wire dataset → model → record → analysis. Reproducible runs out of the box. Useful pattern even if we don't adopt the runtime.
4. **Strategy / Backtester (`qlib.backtest`)** — orderbook-aware execution simulator with TopkDropout-style portfolio construction. Pure equity. Nothing macro about it.

There is **no DSGE, no BVAR, no DFM, no nowcasting, no MIDAS** in Qlib's official model zoo. Cross-sectional pooling is everywhere (it's a stock-picking framework — that's the whole game), but cross-country pooling for macro variables is not a first-class concept.

## Suitability for OPENGEM macro use

Brutally: **0% as a substrate, 25% as a reference pattern, 60% on the data layer.**

### Where Qlib does NOT fit OPENGEM

- **Asset class mismatch.** Qlib's mental model is "N stocks × T daily bars × K features → predict next-period return → rank → portfolio." OPENGEM's mental model is "N countries × T monthly/quarterly releases × K indicators → predict T+h levels and bands with vintage provenance." The pipelines look superficially similar but they branch hard at the "rank vs forecast level with uncertainty" decision.
- **No probabilistic forecasts in the model zoo.** Qlib outputs point predictions. We need full distributions (P10/P50/P90 or P5/P25/P50/P75/P95 — see L188). Adapting any Qlib model to emit quantiles is non-trivial; their `Record` / `SignalRecord` abstractions assume scalar IC and rank-IC scoring.
- **No mixed-frequency handling.** GDP is quarterly, CPI is monthly, financial conditions index is daily, news tone is hourly. Qlib presupposes a single fundamental frequency per dataset. MIDAS / MF-DFM are not even discussed.
- **No vintage discipline.** Qlib stores "latest snapshot" with no native concept of as-of dates / publication vintages. OPENGEM's whole accountability thesis depends on vintaged storage. Bolting a vintage layer onto Qlib means rewriting half the data layer.

### Where Qlib *would* be useful — selectively

- **The Qlib data format is genuinely fast.** Binary columnar, memory-mappable, lazy. If we end up with billions of cells (vintage × country × indicator × release date × forecast horizon), the format is worth studying — though DuckDB + Parquet now dominates this niche and we should use that (see L077, L094).
- **The expression engine is elegant.** `Ref($cpi, -3) - $cpi` as a feature spec is the right ergonomic level for analysts. We may borrow the *idea* (a typed DSL over our vintage panel) without adopting the runtime.
- **The model zoo's deep-learning baselines are well-tested.** If we ever wire neuralforecast / Nixtla into L3 (see L044, L088), we'll want to cross-reference Qlib's PyTorch implementations for ALSTM / Transformer hyperparameter defaults. They've already done the gridsearch we'd otherwise repeat.
- **The workflow YAML pattern is good.** Declarative pipeline configs that survive reruns are exactly what we'd want for our 5-year forecast leaderboard reproducibility (see L186). Don't adopt qlib's exact YAML schema; do steal the idea.

## "How a macro DFM/BVAR could borrow from Qlib"

Concretely:

| Qlib piece | Stolen for OPENGEM as |
|---|---|
| `qlib.data.expression` DSL | A feature-engineering DSL over our `(country, indicator, vintage)` panel |
| `qlib.workflow` YAML run config | Per-forecast run manifest (model + data slice + vintage cut + seed) |
| `qlib.contrib.model.pytorch_transformer` defaults | Starting hyperparameters for any deep L3 model we add |
| `qlib.contrib.report` HTML render | Pattern for forecast post-mortems (we'd skin it differently) |

What we **don't steal**: the data store (use DuckDB + Parquet), the backtester (build our own evaluator around CRPS/log-score per L183), the strategy layer (irrelevant), the equity-specific models (TRA, HIST, IGMTF — leave them in their box).

## RD-Agent: the surprise

The Qlib README explicitly forwards readers to RD-Agent — Microsoft's LLM-driven *automated research process* for quant. This is the strategic signal: Microsoft is no longer investing in Qlib as a *human-research-supporting platform*; they're investing in *LLM-driven hypothesis generation that uses Qlib as a substrate*. The framing matters for OPENGEM. If we publish forecasts with full provenance, RD-Agent-style systems can ingest us, score themselves against us, and we get the same upstream-of-LLM positioning OpenBB is going for. Worth watching, not yet worth integrating.

## Cost-benefit if we integrate

| Action | Cost (dev-weeks) | Benefit |
|---|---|---|
| Adopt Qlib as backend data layer | 6–10 + ongoing | Net negative — wrong shape for macro vintages |
| Steal expression-DSL pattern | 1 | Cleaner feature configs for analysts |
| Steal workflow-YAML pattern | 0.5 | Reproducible run manifests |
| Borrow hyperparameter defaults from PyTorch model zoo | 0.2 | Faster L3 model warm-start |
| Submit OPENGEM as Qlib data provider | 2 + AGPL-free since Qlib is MIT | Marginal — Qlib users want equity, not macro |

**Recommendation**: don't integrate. Borrow patterns. Revisit if Microsoft pivots Qlib toward macro (no signal of that in 2026).

## What this loop produced

- Layer-by-layer architecture (data / models / workflow / backtest).
- Concrete reasons Qlib's equity-tilted abstractions don't fit OPENGEM macro.
- Explicit list of patterns worth stealing (DSL, YAML workflow, PyTorch defaults).
- Strategic read on RD-Agent as Qlib's actual future.

## What comes next

- **L013** — Backtrader / VectorBT / Zipline-reloaded: similar non-fit but with chart export wins.
- **L044** — Nixtla / neuralforecast / darts: the actual ML-econ stack we'll build on.
- **L087** — Bayesian VAR Python stack consolidation: the macro-native side of Qlib's "model zoo" question.
- **L088** — neuralforecast for L3 layer: where Qlib's hyperparameter defaults transfer.

## Related

- [[L001-vision-statement]] — vintage discipline + accountability ledger is why Qlib's "latest snapshot" data store doesn't fit.
- [[L011-openbb-terminal]] — different AGPL-vs-MIT story, but same "famous OSS finance repo that does the wrong asset class" pattern.
- [[L088-neuralforecast-l3]] — where Qlib's PyTorch defaults actually transfer.
