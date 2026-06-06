# L079 — Prefect / Dagster / Airflow / Temporal for Orchestration: Stay With Dagster Or Switch?

**Loop**: 079 / 300
**Phase**: 1 — Open-source landscape survey
**Date**: 2026-06-06

---

## Thesis of this loop

OPENGEM already has `deploy/dagster` in the repo, signaling a Dagster-first orchestration choice. The question this loop honestly tests: *is that still the right choice in mid-2026 against the post-2024 generation of orchestrators?*

Spoiler: **yes**. Stay with Dagster. The asset-based model fits OPENGEM's vintage-store discipline like a glove — Dagster's first-class "data asset" abstraction is *exactly* the abstraction OPENGEM needs for "every series, every forecast, every vintage is a versioned addressable thing." Switching to anything else surrenders this affordance.

Verdict: **ADOPT-V1 Dagster**. **SKIP Airflow** (too heavy, asset model worse). **SKIP Prefect** (lighter but no asset model — partial regression). **EVALUATE-LATER Temporal** only for the API/webhook side (not the data pipeline side).

## Dagster: why the asset model wins for OPENGEM

Dagster's central abstraction is the **asset**: a named, typed, versioned data thing produced by a function. The asset graph is the *forward-pointing* equivalent of a database schema: you declare what assets exist, what produces them, and Dagster does the dependency resolution.

For OPENGEM specifically, the assets map cleanly:

- `cpi_raw_brazil` — the raw CPI series for Brazil from the IBGE source.
- `cpi_cleaned_brazil` — after dedup, vintage tagging, methodology stamping.
- `cpi_forecast_v$VINTAGE_brazil_horizon_3m` — a forecast asset.
- `cpi_realized_brazil_2026_q1` — the realized value (fills in when the data arrives).
- `cpi_vv_score_brazil_v$VINTAGE` — the V&V score asset that depends on both forecast and realized.

The asset graph captures the *forecast-cartel-killer* business logic: which inputs produced which forecast, which forecast was scored against which realization, what was the methodology vintage. This is the same lineage Bloomberg, Macrobond, and IMF can not publish because their pricing depends on opacity. OPENGEM publishes it because Dagster's asset graph is the lineage, ready to be exposed.

Other Dagster strengths for OPENGEM:
- **Software-defined assets, versioned.** Asset materializations are versioned (code version + data version). The "what produced this number" answer is in Dagster, queryable.
- **Partitions** are first-class. Time-partitioned assets (a forecast for each daily vintage) are the asset model's native shape.
- **IO managers** abstract storage. A single config swap shifts an asset's storage from Postgres to Parquet on S3 to Iceberg without touching the asset's producing code.
- **Dagster Cloud / OSS**: Apache 2.0 OSS. Dagster Cloud (paid) is a hosted control plane. OSS covers everything OPENGEM needs.
- **Reasonable scheduling.** Cron + event-driven + manual.

The cost of Dagster: it has a steeper learning curve than Prefect, more concepts (assets, partitions, IO managers, ops, jobs, schedules, sensors, resources). For a one-person team this is real friction. But OPENGEM's data model *requires* the concepts Dagster makes first-class; the friction is the friction of the problem, not the framework.

## Airflow: too heavy, wrong abstraction

- **License**: Apache 2.0.
- **Strengths**: 100% market share in enterprise data pipelines, biggest community, every integration exists, battle-tested.
- **Weaknesses for OPENGEM**:
  - Task-based mental model, not asset-based. The lineage is implicit in the DAG, not first-class.
  - Operational overhead: scheduler, web server, executor, metadata DB. The minimum operating cost is real (~$50-200/mo for self-hosted, $500+/mo for MWAA/Astronomer managed).
  - The "Airflow is heavy" complaint is *not* a developer-experience thing — it's a real operational thing. Reasonable Airflow shops have a platform engineer; OPENGEM is one person.
- **SKIP**. Wrong fit.

## Prefect: lighter, but no asset model

- **License**: Apache 2.0.
- **Strengths**: Python-native `@flow` and `@task` decorators with minimal ceremony. Lightest learning curve of the four. Cloud control plane (Prefect Cloud) is generous in the free tier.
- **Weaknesses for OPENGEM**:
  - Task/flow model, not asset model. To express "the forecast for Brazil CPI 2026-Q2 as of vintage 2026-06-06 depends on the realized CPI through 2026-05 and the methodology v3.1," you write a flow; the dependency is procedural. Dagster expresses this as an asset graph declaratively.
  - Lineage is weaker. Prefect 3 has improved this but the abstraction is task-events, not assets.
  - "Flows" are convenient for one-shot scripts; the vintage-discipline OPENGEM needs benefits from Dagster's stricter model.
- **Verdict**: **SKIP** as primary. If OPENGEM wasn't already on Dagster, Prefect would be a viable choice — but it's a downgrade from Dagster's asset model. Don't switch backwards.

## Temporal: a different shape entirely

- **License**: MIT (Temporal core), with a managed cloud offering.
- **Model**: durable workflows. Stateful long-running functions that survive crashes. Not a data pipeline tool — a workflow tool for application logic (sagas, business workflows, ML training orchestration with checkpointing).
- **Strengths**: bulletproof reliability for long-running stateful operations. Best-in-class for "this workflow takes 3 days and must survive worker restarts."
- **Weaknesses for OPENGEM data pipelines**: wrong shape. Temporal doesn't think in terms of assets or DAGs; it thinks in terms of imperatively-coded workflows.

**Where Temporal *could* belong in OPENGEM**: the *API-side* long-running workflows — for example, "process this large customer export," "run this 3-hour custom backtest the user requested," "rebuild the vintage tree after a methodology version bump." These are imperative workflows that fit Temporal but don't fit Dagster's asset model.

For now, Y1 OPENGEM has no such workflows. **EVALUATE-LATER**.

## Cost / hosting reality

- **Dagster OSS self-hosted**: 2-vCPU box runs the daemon + webserver + Postgres metadata. Hetzner CX21 = ~$8/mo. Add Cloud Storage for IO manager backing = ~$5/mo. Total: ~$15/mo.
- **Dagster OSS on Cloud Run**: ~$30-60/mo with a Postgres backend.
- **Dagster Cloud Hybrid** (control plane in Dagster, compute in your infra): starts at $400/mo. Adds nice things like a hosted UI, asset catalog, branch deployments, alerting. *Probably not worth the cost for Y1 OPENGEM*.
- **Dagster Cloud Serverless**: pay-per-compute, ~$100-300/mo at OPENGEM's scale. Considered but the hybrid pricing is more predictable.

Practical floor: **$15/mo for Dagster OSS on Hetzner**. Through Y1, this is the right plan.

## Ramp-up (already partially done)

Per the prompt, OPENGEM already uses Dagster (`deploy/dagster/`). Even if the deploy is mostly skeleton today, the choice has been ratified. The ramp from here:

- Week 1: convert ingestion adapters to assets.
- Week 2: convert forecast generation to assets, partitioned by vintage.
- Week 3: convert V&V scoring to assets with explicit upstream/downstream relations.
- Week 4: schedule + sensor wiring for "rebuild this asset when its upstream changes."

A 1-month commitment to get the asset graph genuinely productive.

## Specific anti-patterns to avoid

- **Don't mix orchestrators.** Adding Prefect "for one quick thing" and keeping Dagster for everything else doubles operational cost and confuses lineage.
- **Don't use Dagster for *application* workflows.** When the API needs to run a long workflow for a logged-in user, that's Temporal or a custom Celery worker — not a Dagster asset.
- **Don't tightly couple Dagster to a single execution backend.** Use IO managers to abstract storage. The Y2-Y3 migration to Iceberg (L078) is smooth if assets are storage-agnostic.

## Verdict

- **Dagster OSS** as the OPENGEM orchestrator: **ADOPT-V1**. Stay. $15/mo. Asset model is the right abstraction.
- **Dagster Cloud**: **EVALUATE-LATER** at Y2-Y3 when an alerting/UI/branch-deploys story justifies $400/mo.
- **Airflow**: **SKIP** forever.
- **Prefect**: **SKIP**. Downgrade from Dagster's asset model.
- **Temporal**: **EVALUATE-LATER** only for application-layer long-running workflows (custom backtests, large exports).

## Cost summary

| Tool | Cost | Use | Ramp |
|---|---|---|---|
| Dagster OSS self-host | $15/mo | All data pipelines | 1 month |
| Dagster Cloud Hybrid | $400/mo (skipped) | (skipped Y1) | n/a |
| Temporal Cloud | ~$200/mo (skipped) | (skipped Y1) | n/a |

## What comes next

- **L080** evaluates Monte Carlo / scenario-tree libs.
- **L097** is the Phase 2 deep dive on fully exploiting Dagster's existing in-repo setup.

## Related

- [[L078-iceberg-delta-parquet]] — IO managers abstract storage; Dagster handles migration smoothly
- [[L097-dagster-fully-exploit]] — Phase 2 deep dive
- [[L102-asynq-celery-arq]] — application-tier task queue choices (Temporal alternative)
