# L088 — neuralforecast (Nixtla) for L3 Layer: Design Fit + Model Menu

**Loop**: 088 / 300
**Phase**: 2 — Integration deep dive
**Date**: 2026-06-06
**Verdict**: **ADOPT-V2 (Block II experimental ensemble member, three-model menu, no hero-feature dependency)**

---

## What this loop answers

L044 graded the Nixtla stack: `statsforecast` + `mlforecast` + `hierarchicalforecast` are Tier-A workhorses; `neuralforecast` is Tier-B experimental. This Phase 2 loop opens `research-300/clones/neuralforecast/` and converts that grade into a concrete design fit: *what three neural models do we actually run, what does the integration look like, what's the success bar for promoting them from experiment to ensemble member?*

The answer: **three models** (NHITS for univariate baselines, DeepAR for probabilistic autoregressive, TFT for multivariate with covariates), **PyTorch Lightning under the hood**, **early-stopping + Conformal prediction for quantiles**, **GPU-optional but CPU-feasible**, and a **CRPS-beat-threshold of 5% over statsmodels DFM** as the promotion bar. Below it, we publish the experiment as evidence and move on. Above it, the model becomes a permanent L3 member.

## What the cloned repo contains

Inspecting `research-300/clones/neuralforecast/neuralforecast/`:

```
neuralforecast/
  __init__.py          # exports NeuralForecast + DistributedConfig
  core.py              # 115KB — the NeuralForecast orchestration class
  tsdataset.py         # PyTorch Dataset wrapper
  auto.py              # 88KB — hyperparameter-tuned variants (NHITS-Auto, etc.)
  utils.py             # 31KB — helpers
  common/              # base model classes + transforms
  losses/              # MSE, MAE, MAPE, Quantile, DeepAR distributional
  models/              # 39 models, one file per architecture
    nhits.py           # ★ univariate baseline
    nbeats.py / nbeatsx.py
    deepar.py          # ★ probabilistic autoregressive
    tft.py             # ★ multivariate w/ covariates
    patchtst.py
    itransformer.py
    timellm.py
    timexer.py
    ...
```

License: **Apache 2.0** (verified). 39 model files. The three I starred above are the L3 candidates; the rest are noted for posterity but not in scope for v1.

The package architecture is clean: each model is a `pl.LightningModule` (PyTorch Lightning). The `NeuralForecast` orchestrator handles cross-validation, hyperparameter tuning via Optuna (in `auto.py`), and the long/wide DataFrame I/O. There's no proprietary serving stack — once a model is fitted, you can serialize the `LightningModule` and serve it from any PyTorch runtime.

The fact that everything subclasses `pl.LightningModule` is a real win for OPENGEM: it means our Dagster jobs can use the standard `Trainer.fit()` API, our checkpoints are PyTorch-native, and our experiment tracking (Hydra + W&B-OSS-alt per L201) integrates without bespoke glue.

## The three-model menu — why these, not the others

### Model 1 — NHITS (Neural Hierarchical Interpolation for Time Series)

**Paper**: Challu et al., AAAI 2023.
**Architecture**: A stack of fully-connected blocks with multi-rate signal decomposition. Each block predicts a different frequency component; the residuals cascade through deeper blocks. Output: point + quantile forecasts via Conformal Prediction or quantile loss.
**Why pick it**: Best-in-class on M3/M4 competition for univariate forecasting. Strong reported performance on macro quarterly/monthly data when there's enough history. Fast — trains in minutes per series on CPU, seconds on GPU.
**OPENGEM role**: Per-country univariate baseline forecast for each indicator. Especially useful on countries where the DFM panel is too thin for full mixed-frequency estimation (smaller Tier-V economies in L086).
**Cost to integrate**: 1 dev-week wrapper + 1 dev-week hyperparameter grid + 1 dev-week V&V scoring = 3 dev-weeks.

### Model 2 — DeepAR (Salinas et al., 2017)

**Paper**: Salinas, Flunkert, Gasthaus 2017, the canonical probabilistic autoregressive model.
**Architecture**: Encoder-decoder LSTM/GRU with parametric distributional output (Negative Binomial for count data, Student-T or Gaussian for continuous). Native probabilistic forecasting via the distributional head — no separate Conformal step needed.
**Why pick it**: First-class probabilistic forecasting (the OPENGEM accountability bar). Handles cross-series global pooling natively — train one model on US + EU + UK + Japan + Korea + Canada, get a global model that exploits cross-country structure.
**OPENGEM role**: Probabilistic forecaster with cross-country pooling. The natural complement to single-country statsmodels DFM and PyMC BVAR.
**Cost to integrate**: 1 dev-week wrapper + 1 dev-week pooling-strategy tuning + 1 dev-week V&V = 3 dev-weeks.

### Model 3 — TFT (Temporal Fusion Transformer)

**Paper**: Lim et al. 2021.
**Architecture**: Attention-based encoder-decoder with explicit variable-selection networks, static / time-varying / known-future covariate handling, interpretable attention weights.
**Why pick it**: Native covariate handling — we feed GDELT-derived tone, GPR-T threats, OpenSanctions exposure, financial conditions index as time-varying covariates and the model decides their relevance. The variable-selection weights produce a *built-in feature attribution*, which lands directly in the L132 vintage drawer.
**OPENGEM role**: Multivariate forecaster with rich covariates. The model we point at when a user asks "what features moved this forecast?"
**Cost to integrate**: 2 dev-weeks wrapper + 2 dev-weeks covariate pipeline + 1 dev-week interpretability surface = 5 dev-weeks.

## Why these three, not 36 others

The other 36 models in `neuralforecast/models/` fall into four buckets:

1. **Transformer variants** (Informer, Autoformer, FedFormer, PatchTST, iTransformer, TimeXer, TimeMixer, vanilla Transformer, Timesnet, Softs). Methodologically interesting; empirically inconsistent on macro data. We pick TFT because the *covariate handling* is unique, not because it's the best Transformer.
2. **NBEATS family** (NBEATS, NBEATSx, NHITS, DLinear, NLinear). NHITS dominates the family on most published benchmarks; we pick that one.
3. **RNN/CNN baselines** (LSTM, GRU, RNN, DilatedRNN, TCN, BiTCN, RMok). Older architectures; outperformed by NHITS/DeepAR/TFT on macro panels. Skip.
4. **Specialist** (TimeLLM, KAN, STEMGNN, HINT). Too narrow or too speculative for v1.

Adding a model to the L3 ensemble has a real maintenance cost (V&V scoring, methodology card, BMA weight integration). Three is the right number to start.

## How the integration looks

```python
# packages/opengem-l3-neural/src/opengem_l3_neural/forecaster.py
from neuralforecast import NeuralForecast
from neuralforecast.models import NHITS, DeepAR, TFT
from neuralforecast.losses.pytorch import DistributionLoss, QuantileLoss

class NeuralL3Forecaster:
    """Wraps NHITS + DeepAR + TFT as three independent ensemble members."""

    def __init__(self, country_panel: PanelSpec, horizon: int = 4):
        self.panel = country_panel
        self.horizon = horizon
        self.models = self._build_models()

    def _build_models(self):
        return [
            NHITS(
                h=self.horizon,
                input_size=24,
                loss=QuantileLoss(quantiles=[0.1, 0.25, 0.5, 0.75, 0.9]),
                max_steps=2000,
                early_stop_patience_steps=50,
                random_seed=42,
            ),
            DeepAR(
                h=self.horizon,
                input_size=24,
                loss=DistributionLoss(distribution="StudentT", level=[10, 25, 50, 75, 90]),
                max_steps=2000,
                early_stop_patience_steps=50,
                random_seed=42,
            ),
            TFT(
                h=self.horizon,
                input_size=24,
                hist_exog_list=self.panel.historical_features,
                futr_exog_list=self.panel.known_future_features,
                stat_exog_list=self.panel.static_features,
                loss=QuantileLoss(quantiles=[0.1, 0.25, 0.5, 0.75, 0.9]),
                max_steps=2000,
                early_stop_patience_steps=50,
                random_seed=42,
            ),
        ]

    def fit(self, df: pd.DataFrame):
        """df in Nixtla long format: unique_id, ds, y, + covariates."""
        for model in self.models:
            nf = NeuralForecast(models=[model], freq="Q")
            nf.fit(df=df)
            self._write_checkpoint(model.__class__.__name__, nf)

    def predict(self, df_future: pd.DataFrame) -> dict[str, ForecastDist]:
        """Returns one ForecastDist per model."""
        out = {}
        for model_name, nf in self._load_checkpoints():
            preds = nf.predict(df_future)
            out[model_name] = self._to_forecast_dist(preds)
        return out
```

That's about ~80 lines of glue code for the three models. The lift is real but proportionate.

## CPU vs GPU footprint

For OPENGEM's scale (~130 country-indicator forecasts per horizon, ~25-year quarterly histories):

- **NHITS**: trains in ~3 minutes per series on CPU. Total nightly retrain: ~6.5 hours. Tractable.
- **DeepAR**: with cross-country pooling (one model per indicator, all countries), trains in ~30 minutes per indicator on CPU. Total nightly: ~6 hours. Tractable.
- **TFT**: heavier — ~60 minutes per indicator with full covariates on CPU. Total nightly: ~12 hours. Tight.

CPU-only is feasible for v1. The full nightly job runs in ~24 hours; we schedule the retrain weekly, not daily. Inference (point forecast for a deployed model) is sub-second on CPU.

For Block II we evaluate a single GPU node (~$0.50-1/hour spot pricing on Cloud Run / EC2 / Hetzner). Cuts retrain time by 5-10x. We add the GPU node when L3 promotion is confirmed.

## The promotion bar — 5% CRPS improvement

A neural model promotes from experimental to permanent L3 ensemble member if and only if it beats the statsmodels DFM baseline by ≥5% on CRPS (Continuous Ranked Probability Score) averaged across the Tier-V country-indicator backtests over the last 5 years. The threshold:

- Less than 5%: insufficient signal. We publish the comparison as a track-record-page entry, retire the model from production scoring, and add a "model card" entry explaining why.
- 5% to 15%: medium signal. Add to L3 with conservative BMA weight (capped at 15%).
- 15%+: high signal. Add to L3 with empirically-derived BMA weight.

This bar is intentionally aggressive. Deep-learning forecasting in macro has been mixed at best. A 5% CRPS gain over a calibrated DFM is real progress, not noise.

## Why Block II, not Block I

Block I is the v1 launch (Phase 6 of the 300-loop schedule). It must ship with calibrated baselines. The L3 layer in Block I is:

- statsmodels DFM (L086)
- statsmodels VAR (L087 Tier 1)
- PyMC BVAR Minnesota (L087 Tier 2)
- statsforecast baselines (L044 — AutoARIMA, AutoETS, Theta, RW, SeasonalNaive)
- BMA combiner with empirical weights from backtest

Block II (post-launch, months 4-9 post-v1) adds:

- PyMC BVAR-SV (L087 Tier 3)
- PyMC hier-BVAR (L087 Tier 4)
- **neuralforecast NHITS** (this loop)
- **neuralforecast DeepAR** (this loop)
- **neuralforecast TFT** (this loop)
- mlforecast LightGBM (L044)

The reason neural forecasters land in Block II rather than Block I: their training pipelines have higher operational risk (NUTS-equivalent failure modes, GPU spot interruptions, longer feedback loops on bad runs). For v1 we want the simplest possible reproducible spine. Neural is the upgrade.

## The interpretability surface

TFT exposes attention weights and variable-selection weights for every prediction. Hidden behind the L132 provenance drawer: a "feature importance" panel showing which historical features and which covariates the model weighted highest for this specific forecast.

This is the *only* L3 ensemble member that produces native feature attribution. statsmodels DFM has news decomposition (which is different — it attributes to *releases*, not features). PyMC BVAR has impulse-response functions. neuralforecast TFT has per-prediction feature importance.

The "publishes its mistakes" promise rhymes with this: when a forecast misses, the TFT attribution shows what the model thought mattered, and the L200 post-mortem can compare that to what *actually* mattered.

## Risks

1. **Reproducibility under PyTorch nondeterminism.** PyTorch with multi-threading is non-deterministic by default. Mitigation: pin `torch.use_deterministic_algorithms(True)`, set `num_workers=0` for the DataLoader, fix random seeds in `LightningModule`. Accept the ~2x slowdown.

2. **PyTorch Lightning API churn.** Lightning 2.x has had several breaking releases. Mitigation: pin minor versions; quarterly upgrade cycle synced with neuralforecast's own release cadence.

3. **Hyperparameter overfit.** Auto-tuning via Optuna on small panels overfits. Mitigation: use Nixtla's published defaults from the M-competition; reserve a true holdout (the last 4 years) that Optuna never sees.

4. **Macro-data shortness.** ~100 quarterly observations per Tier-V country is on the short side for deep learning. Mitigation: cross-country pooling in DeepAR; aggressive regularization; honest reporting when a model can't beat the DFM baseline.

5. **The 5% promotion bar is harsh.** Some models might genuinely add ensemble value (diversification) even without beating DFM individually. Mitigation: track BMA-weight-implied performance separately; revisit the bar if backtest evidence supports BMA-only promotion.

## Cost summary

| Task | Cost |
|---|---|
| NHITS wrapper + hyperparameter grid + V&V | 3 dev-weeks |
| DeepAR wrapper + pooling-strategy tuning + V&V | 3 dev-weeks |
| TFT wrapper + covariate pipeline + interpretability | 5 dev-weeks |
| L3 BMA combiner integration | 1 dev-week |
| Track-record page entries for each model | 0.5 dev-week each = 1.5 weeks |
| Promotion-bar test harness | 1 dev-week |
| **Total `opengem-l3-neural` v0.1.0** | **~14 dev-weeks (~3.5 months)** |

Comparable to the BVAR stack (L087). Justifies its place in the Block II roadmap.

## What this loop produced

- Three-model menu (NHITS, DeepAR, TFT) with explicit rationale for each.
- Explicit rejection of the other 36 neuralforecast models for v1.
- CPU-vs-GPU operational envelope (CPU OK for v1, GPU for Block II promotion).
- 5% CRPS promotion bar over statsmodels DFM.
- Interpretability story: TFT attention weights → L132 provenance drawer.
- ~14 dev-week total cost.

## What comes next

- **L087** — Bayesian VAR sibling (already published).
- **L189** — BMA combiner: how the neural members weight in.
- **L201** — Hydra + MLflow sweep tracking: how we manage the hyperparameter search.
- **L207** — Density forecast aggregation across heterogeneous output formats.

## Related

- [[L044-nixtla-stack]] — Phase 1 Nixtla survey.
- [[L086-nyfed-nowcasting-reuse-vs-rewrite]] — DFM sibling.
- [[L087-bayesian-var-python-consolidation]] — BVAR sibling.
- [[L132-provenance-drawer]] — interpretability surface.
- [[L189-bma-combiner]] — downstream combiner.
- [[L201-hyperparameter-sweep-tracking]] — sweep infra.
- [[L207-density-forecast-aggregation]] — aggregation rules.
- inspected source: `/mnt/bigdata/home/edgardo/projectsd/opengem/research-300/clones/neuralforecast/neuralforecast/models/{nhits,deepar,tft}.py` (file existence + signatures).
- inspected source: `/mnt/bigdata/home/edgardo/projectsd/opengem/research-300/clones/neuralforecast/LICENSE` (Apache 2.0).
