# L201 — Hyperparameter Sweep Tracking

**Loop**: 201 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The decision

OPENGEM's L3 variants — DFM, ML-residual, large BVAR, TVP-VAR, MF-DFM — each have hyperparameters that are tuned via offline sweeps (BVAR prior tightness λ, ridge penalty α, factor count K, lag length p, learning rate, etc.). The tuning machinery must produce trial-level provenance compatible with L186 envelopes and L182 lineage.

Three candidate stacks: **Hydra + MLflow** (the de facto OSS standard), **DVC** (data + experiment versioning under git), and **a custom JSON-on-S3 layer** built on top of `opengem-vintage`. Pick one. Justify.

## The three candidates

### Candidate A — Hydra + MLflow

- **Hydra**: configuration composition (override + sweep) from YAML. Generates the cross-product of `λ ∈ {0.05, 0.10, 0.20}` × `K ∈ {4, 6, 8}` = 9 trial configs, with reproducible run dirs.
- **MLflow**: experiment-tracking server. Each trial logs params, metrics, artifacts. Has a web UI for browsing runs.
- **Status**: each is mature, widely used in ML platforms.

Pros:
- Industry standard; engineers know it.
- Web UI is good enough out-of-the-box.
- MLflow Tracking Server is OSS, self-hostable.

Cons:
- MLflow's data model is *opinionated* about runs and experiments; integrating with our existing `opengem-vintage` + lineage record requires a bridge layer.
- MLflow's artifact store is a separate S3 prefix; envelope replay needs to cross-reference.
- Hydra config composition is powerful but adds a new YAML schema layer on top of our existing `pyproject.toml`-defined pyproject metadata.
- MLflow's UI is functional but dated; less aligned with the dashboard's visual style.

### Candidate B — DVC

- **DVC** (Data Version Control): git-native experiment + data versioning. Trials are git branches; metrics + params live in git-tracked files (`metrics.json`, `params.yaml`); large artifacts pushed to S3 via DVC remote.
- **Status**: mature, widely used in academic / open-source ML.

Pros:
- Pure git workflow; no separate tracking server to host.
- Branch-per-trial is reviewable + diffable.
- DVC remote is just S3; aligns with our existing blob-store layout.
- No web UI to maintain; `dvc exp show` in CLI + GitHub PR view.

Cons:
- Sweep workflow is more manual: writing a 27-trial config matrix as 27 branches is awkward.
- DVC is best for "one experiment at a time with stable parent commit"; sweep semantics are bolted on.
- No web UI without DVC Studio (a SaaS).

### Candidate C — Custom JSON-on-S3

- Trials are JSON envelopes (`trial_envelope.v1`) written to S3 alongside the existing lineage records (L182). Each trial is a single envelope with `params`, `metrics`, `artifacts`, `parent_run`, `replay_command`.
- Sweep composition is a Python harness that emits N envelopes.
- Browsing UI is the OPENGEM dashboard itself: a /sweeps page rendering the JSONs.

Pros:
- Native integration with L186 envelope schema; trials inherit reproducibility.
- No separate service to operate.
- UI integrates with the dashboard's visual identity.

Cons:
- We have to build everything: sweep composition, comparison views, hyperparameter search algorithms (random / Bayes-opt / Optuna integration).
- No-batteries-included experience.
- One more thing to maintain.

## The pick: **Candidate A (Hydra + MLflow) with a thin L186 envelope bridge**

Reasoning, in order:

1. **The L3 sweeps are not exotic.** Standard cross-product + Bayesian search over 4-12 hyperparameters per variant. MLflow handles this without modification.
2. **MLflow's data model is close enough.** A MLflow `run` maps directly to an L186 envelope; a bridge layer (~200 LOC) writes envelopes on each MLflow run completion. Replay machinery is shared.
3. **Hydra's sweep composition is the cleanest among the three** for the way macro tuning is done — large grids with conditional branching ("if model=BVAR then sweep λ and lag_p, if model=ridge then sweep α and feature_set").
4. **Operational cost is low.** MLflow Tracking Server runs in a Docker container with PostgreSQL backend + S3 artifact store. We already have both. Add: one container, ~100 LOC of compose config, $0 incremental hosting.
5. **DVC's PR-per-trial workflow does not scale** to 200-trial Bayes-opt runs. Branches-as-trials is fine for 10 but rough at 100.
6. **Custom JSON-on-S3 is more code than I want to write and maintain.** The principle of "don't build what you can adopt" applies.

## The integration architecture

```
   sweep config (Hydra YAML)
              │
              ▼
   Hydra multirun launches K trials in parallel
              │
              ▼
   Each trial runs the L3 variant pipeline
              │
              ▼
   MLflow logs params + metrics + artifact paths
              │
              ▼
   On run complete: bridge writes L186 envelope
              │       (mlflow_run_id → envelope_id mapping table)
              ▼
   Envelope joined to OPENGEM vintage store
              │
              ▼
   Sweep results aggregated → leaderboard candidate, BMA weight input,
                              forecast.v1 component
```

## The Hydra sweep config

```yaml
# packages/opengem-l3/sweeps/bvar_2026_q3.yaml
defaults:
  - _self_
  - model: bvar_large
  - dataset: tier_v_core_2014_2025

hydra:
  mode: MULTIRUN
  sweeper:
    params:
      model.prior_tightness: 0.05, 0.10, 0.15, 0.20, 0.30
      model.lag_p: 1, 2, 4
      model.factor_count: 3, 5, 7
      sampler.seed: range(20260606, 20260616)   # 10 seeds for robustness

mlflow:
  experiment_name: bvar_2026_q3
  tracking_uri: https://mlflow.opengem.org
```

10 seeds × 5 priors × 3 lags × 3 factors = 450 trials, parallelised across the runners.

## The MLflow → L186 envelope bridge

```python
# packages/opengem-tracking/src/opengem_tracking/mlflow_bridge.py

def on_mlflow_run_complete(run_id: str) -> Envelope:
    """Convert an MLflow run into an L186 reproducibility envelope."""
    run = mlflow_client.get_run(run_id)
    envelope_id = f"env_trial_{run.info.run_id}"
    envelope = Envelope(
        envelope_id=envelope_id,
        data_lockfile=resolve_lockfile_for_dataset(run.data.params["dataset"]),
        code_commit=resolve_git_sha(run.data.tags["mlflow.source.git.commit"]),
        container=resolve_container_for_image(run.data.tags["mlflow.runName"]),
        weights=upload_trial_weights(run.info.artifact_uri),
        configuration=upload_trial_config(run.data.params),
    )
    write_envelope(envelope)
    return envelope
```

After each MLflow run completes, the bridge writes a full L186 envelope so the trial is replayable through the same `opengem replay` machinery as production forecasts. **The same replay command verifies a sweep trial.**

## Cost and scale

| Component | Cost | Notes |
|---|---|---|
| MLflow tracking server (Docker container) | $0 | Self-hosted on existing infrastructure |
| PostgreSQL for MLflow metadata | $0 | Existing RDS instance |
| S3 artifact storage | $1.5 / 1000 trials | 6 MB per trial × 1000 = 6 GB at $0.023/GB/mo |
| Hydra runtime | $0 | Python package, no service |
| Bridge layer | One-time engineering | ~200 LOC + tests |

Storage budget: ~2-3 TB / 5 years of sweep history under generous trial counts. Trivial against personal-scale infrastructure.

## Trial provenance schema

Each MLflow run logs:

| Field | Source |
|---|---|
| `params.{name}` | Hyperparameter being swept |
| `tags.git.commit` | Code SHA |
| `tags.container.digest` | Container digest (set by harness) |
| `tags.dataset.lockfile_sha256` | Data lockfile hash |
| `metrics.crps_mean`, `metrics.pit_ks_pvalue`, `metrics.crps_vs_ar1_winrate` | Backtest-engine outputs |
| `artifacts.weights.npz` | Model weights |
| `artifacts.predictions.parquet` | Per-vintage predictions for the trial |
| `tags.opengem.envelope_id` | Bridge-written L186 envelope ID |

## How sweeps feed production

Trials are *candidate* models. The selection rule:

1. Run the sweep.
2. Rank trials by primary V&V metric (e.g. CRPS-vs-AR(1) win-rate over the OOS window).
3. Top-K trials enter the BMA combiner (L189) as variant candidates.
4. BMA assigns weights via L189 rolling log-score procedure.
5. The production forecast is the combiner output.

This is the production-pull pattern: sweeps generate candidates, the combiner curates.

## Anti-pitfalls

1. **Survivor bias on hyperparameter selection.** Tuning on the OOS window contaminates the V&V signal. *Mitigation*: split the OOS window into a tuning subset (2014-2019) and a holdout (2020-2025); leaderboard scoring uses only the holdout.
2. **Storage bloat.** 200,000 trials over 5 years = ~1.2 TB. *Mitigation*: trials older than 12 months that are not currently in production are downsized to params + metrics only; artifacts deleted; envelope marked "archived, replayable via re-trial".
3. **Reproducibility-breaking refactors.** MLflow version upgrades occasionally break old runs. *Mitigation*: pin MLflow major version per epoch; document migration paths.

## What this loop produced

- Three candidate stacks compared.
- Pick: Hydra + MLflow with thin L186 envelope bridge.
- Justified on integration cleanness, ops cost, sweep semantics.
- Hydra sweep config sketch.
- MLflow → envelope bridge contract.
- Cost projection.
- Sweep-to-production feed pattern.
- Survivor-bias mitigation.

## What comes next

- **L202** — stacking as alternative combiner; sweep tracking enables stacking weight learning.
- **L204** — TVP-VAR sweeps.

## Related

- [[L186-reproducibility-envelope]] — envelope schema bridged.
- [[L182-forecast-vintage-lineage]] — lineage of each trial.
- [[L189-bma-combiner]] — sweep candidates feed combiner.
- [[L202-stacking]] — stacking weight learner uses sweep history.
- [[R14-l3-architecture]] — variants that get tuned.
