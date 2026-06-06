# L017 — Awesome Quant: Top 25 Repos for OPENGEM (Macro-Filtered)

**Loop**: 017 / 300
**Phase**: 1 — Open-source landscape survey
**Date**: 2026-06-06

---

## Why this loop exists

[awesome-quant](https://github.com/wilsonfreitas/awesome-quant) (~26.6k stars, actively maintained June 2026) is the canonical curated list of quant-finance OSS. It's massive — hundreds of entries across Python / R / Julia / Rust / JS / Java. Most of it is **equity-microstructure** stuff that's the *wrong asset class* for OPENGEM (HFT engines, options pricers, broker SDKs, technical-indicator libs, equity backtest engines).

This loop filters awesome-quant down to **the 25 repos most relevant to OPENGEM's macro + geopolitics + forecasting + provenance mission**, with one opinionated sentence each on why. This is not a "best of awesome-quant" — it's "what to actually clone if you're building a macro dashboard tomorrow."

## The 25, ranked by integration priority

### Tier 1 — likely to be in OPENGEM's dependency tree

1. **[statsmodels](https://github.com/statsmodels/statsmodels)** — BSD-3. The unavoidable Python econometrics workhorse: DFM, VAR, BVAR-via-pymc, state-space, Kalman, ARIMA, regime-switching. *Every L3 macro model OPENGEM ships will lean on it.* See L035, L087.

2. **[Nixtla/neuralforecast](https://github.com/Nixtla/neuralforecast)** — Apache 2.0. 30+ deep models (NHITS, NBEATSx, TFT, PatchTST, TSMixer, iTransformer, TimeLLM) with a clean `.fit / .predict` API that mirrors statsforecast. *The right home for OPENGEM's L3 deep ensemble.* See L044, L088.

3. **[Nixtla/statsforecast](https://github.com/Nixtla/statsforecast)** — Apache 2.0. Lightning-fast classical models (AutoARIMA, AutoETS, Theta, ADIDA, IMAPA, CrostonClassic) parallelized across series. *The L1 backbone — fits a million series faster than R-forecast.*

4. **[Nixtla/hierarchicalforecast](https://github.com/Nixtla/hierarchicalforecast)** — Apache 2.0. Reconciliation for hierarchical forecasts (country → region → world, or G7 → G20 → all). *Solves OPENGEM's cross-country consistency problem natively.*

5. **[unit8co/darts](https://github.com/unit8co/darts)** — Apache 2.0. Sklearn-style time-series API with both stats and deep models, *and* a clean uncertainty-quantification story (quantile forecasts, conformal prediction). *Best fit for probabilistic forecast objects per L181, L207.*

6. **[pandas-datareader](https://github.com/pydata/pandas-datareader)** — BSD-3. Wraps FRED, OECD, World Bank, Eurostat, ENI in one consistent DataFrame API. *L046, L047, L048 ingestion will start here.*

7. **[dr-leo/pandaSDMX](https://github.com/dr-leo/pandaSDMX)** — Apache 2.0. The Python SDMX client — the protocol that ECB, IMF SDDS, OECD, UNSTATS, BIS, World Bank all speak. *L049 (BIS), L050 (ECB SDW) require this.*

8. **[fredapi / pystlouisfed](https://github.com/TomasKoutek/pystlouisfed)** — Apache 2.0. Direct typed FRED/ALFRED clients. ALFRED is the vintage-aware variant — *critical* for our backtest discipline (L185, L259).

9. **[simonw/datasette](https://github.com/simonw/datasette)** — Apache 2.0. Read-only SQLite-as-website. *L016 chose this for OPENGEM's `/data` raw-access surface — covered there.*

10. **[finos/perspective](https://github.com/finos/perspective)** — Apache 2.0. Streaming pivot grid in WASM. *L014 picks this for the indicator grid + leaderboard pages.*

### Tier 2 — high-probability inclusion in v2

11. **[tradingview/lightweight-charts](https://github.com/tradingview/lightweight-charts)** — Apache 2.0 + attribution. *L015 chose this for the forecast page bands + consensus overlay.*

12. **[ranaroussi/quantstats](https://github.com/ranaroussi/quantstats)** — Apache 2.0. Self-contained HTML tearsheets. *L013 flagged this as the right pattern for "cite-this-view" exports; we use it on internal eval scripts.*

13. **[awslabs/gluonts](https://github.com/awslabs/gluonts)** — Apache 2.0. Probabilistic time series (DeepAR, DeepState, Wavenet) with mature CRPS / log-score evaluators. *The right reference for L183 forecast scoring rules.*

14. **[Nixtla/mlforecast](https://github.com/Nixtla/mlforecast)** — Apache 2.0. ML models (LightGBM, XGBoost) as time-series forecasters with proper lag features and rolling validation. *Best L2 tabular layer in our forecast stack.*

15. **[bashtage/arch](https://github.com/bashtage/arch)** — BSD-3. GARCH/EGARCH/HAR families. Needed for L188 fan charts (vol-aware bands), L208 tail forecasts, L214 inflation regime classifier.

16. **[stan-dev/pystan](https://github.com/stan-dev/pystan)** / **[pymc-devs/pymc](https://github.com/pymc-devs/pymc)** — Apache 2.0 / BSD-3. Bayesian modeling for BVAR, state-space with priors, hierarchical pooling across countries. *L036, L087 architecture.*

17. **[man-group/dtale](https://github.com/man-group/dtale)** — LGPL-2.1. Pandas DataFrame inspector in the browser. Internal-only dev tool. *Useful for analysts inspecting vintage tables during pipeline debugging.*

### Tier 3 — patterns to study, probably not import

18. **[pyhf/pyhf](https://github.com/scikit-hep/pyhf)** — Apache 2.0. The CERN-particle-physics likelihood-model serialization spec. *Reference for how to publish a frozen, citable statistical model with full provenance — directly informs OPENGEM's model card design (L135, L172).*

19. **[OpenBB-finance/OpenBB](https://github.com/OpenBB-finance/OpenBB)** — AGPL-3.0. *L011 covered. Distribution channel, not substrate.*

20. **[microsoft/qlib](https://github.com/microsoft/qlib)** — MIT. *L012 covered. Wrong asset class, useful patterns.*

21. **[mlflow/mlflow](https://github.com/mlflow/mlflow)** — Apache 2.0. Experiment tracking + model registry. *L201 references this for hyperparameter sweep tracking; OSS alternative to W&B.*

22. **[great-expectations/great_expectations](https://github.com/great-expectations/great_expectations)** — Apache 2.0. Data-quality assertions. *Useful for ingestion contract tests (L186 reproducibility envelope).*

### Tier 4 — niche but worth pinning

23. **[domokane/FinancePy](https://github.com/domokane/FinancePy)** — Apache 2.0. Fixed-income + derivatives pricer. *Only relevant for L165 term-structure dashboard and L217 exchange-rate misalignment via FX-swap-implied rates.*

24. **[attack68/rateslib](https://github.com/attack68/rateslib)** — Apache 2.0. Modern rates / IRS / FX swap pricer. *Newer than FinancePy, cleaner API. Same use case.*

25. **[fast-aws-elastic-stack/exchange_calendars](https://github.com/gerrymanoim/exchange_calendars)** — Apache 2.0. Trading-hour and holiday calendars. *Boring but load-bearing for time-zone normalization across daily-frequency data.*

## Conspicuous omissions

Repos in awesome-quant that I **deliberately excluded** because they're wrong-asset-class for OPENGEM, despite their fame:

- `mementum/backtrader`, `polakowo/vectorbt`, `kernc/backtesting.py`, `quantopian/zipline` — equity backtesting, see L013.
- `ranaroussi/yfinance` — equity ticker data; *yes we'll use it occasionally for index proxies (L058), but it's not core*.
- `freqtrade/freqtrade`, `Jesse`, `nautilus_trader`, `rqalpha` — live trading bots.
- `quantopian/pyfolio` — deprecated equity tearsheets; QuantStats replaces.
- `tulip-php/tulipindicators`, `mrjbq7/ta-lib`, `bukosabino/ta`, `twopirllc/pandas-ta` — technical indicators, irrelevant to macro forecasting.
- `domokane/FinancePy`, `vollib/vollib`, `pyfin/pyfin` — derivatives pricers, only marginally relevant.
- `pmorissette/bt`, `pmorissette/ffn` — equity portfolio toolkit.
- `Asoaring/pebble`, `borisbanushev/stockpredictionai` — equity-only.

## Surprise of the loop

**The Nixtla suite (statsforecast + neuralforecast + mlforecast + hierarchicalforecast + statsforecast) is collectively the most undervalued asset in awesome-quant for macro work.** It's tagged primarily as a "time series" toolkit but the design — sklearn-style API, probabilistic outputs as first-class, hierarchical reconciliation built in, ~1M-series scaling — is *purpose-built* for the macro-panel-forecasting workload OPENGEM has. Picking Nixtla as the canonical forecast harness is probably the highest-leverage tooling decision in Phase 1.

A related surprise: **awesome-quant has no dedicated "macro forecasting" section.** Every entry that is macro-relevant has to be excavated from "Time Series" or "Data Sources." If we eventually publish OPENGEM's stack as a downstream awesome-list (`awesome-macro-forecasting`), that's a credibility play with near-zero cost.

## Cost-benefit summary

| Tier | Repos | Action | Effort |
|---|---|---|---|
| 1 (1–10) | 10 | Pin in `requirements.txt` from day 1 | ~1 dev-week to wire all |
| 2 (11–17) | 7 | Adopt as needed in Phase 2/3 | ~1 dev-week each |
| 3 (18–22) | 5 | Study patterns; do not depend | ~0.5 day each |
| 4 (23–25) | 3 | Optional, scenario-dependent | n/a |

## What this loop produced

- A 25-row priority list of awesome-quant entries filtered by macro relevance.
- Explicit exclusions of famous-but-wrong-asset-class repos.
- The Nixtla-as-forecast-substrate strategic call.
- A "publish `awesome-macro-forecasting`" distribution side-bet.

## What comes next

- **L018** — FinTabNet + financial document tools (PDF tables, Camelot, Tabula).
- **L020** — FinGPT / FinNLP / FinRL: LLM-for-finance toolkits.
- **L044** — Nixtla deep dive: skforecast, darts, neuralforecast.
- **L087** — Bayesian VAR Python stack consolidation.
- **L088** — neuralforecast for L3 layer (Phase 2).

## Related

- [[L001-vision-statement]] — "composable open-source substrate" demands a curated dependency tree.
- [[L011-openbb-terminal]] / [[L012-qlib]] / [[L013-backtrader-vectorbt-zipline]] — the "wrong asset class" repos this loop filters out.
- [[L014-finos-perspective]] / [[L015-lightweight-charts]] / [[L016-data-publishing-platforms]] — the viz/publishing complement.
- [[L044-nixtla-darts-neuralforecast]] — Phase 1 deep dive on the chosen forecast stack.
- [[L087-bayesian-var-stack]] — Phase 2 on the Bayesian half.
