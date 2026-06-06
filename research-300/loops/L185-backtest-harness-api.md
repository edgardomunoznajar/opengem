# L185 — Open Backtest Harness API

**Loop**: 185 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The decision

The OPENGEM backtest engine (R24) runs internally on a weekly cadence. **External researchers must be able to replay any backtest, propose alternative models, and submit results back to the public V&V matrix.** This loop specifies the public-facing harness: REST endpoints + Python client + Java client.

The point is asymmetry. Bloomberg never let academics run their black-box on a held-out window. OPENGEM does. That is the difference.

## API surface

### Versioning + base URL

- Public production: `https://api.opengem.org/v1/backtest/`
- Schema versioning via `Accept: application/vnd.opengem.backtest.v1+json` header; URL path mirror at `/v1/backtest/` as the wire fallback.
- Auth: none required for read endpoints; `OPENGEM_API_KEY` required for submission endpoints, rate limited at 100 jobs/day for free tier.

### REST endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/v1/backtest/cells` | Enumerate V&V matrix cells in scope this epoch. |
| GET | `/v1/backtest/cells/{cell_id}` | Fetch a single cell spec (variable, horizon, country set, scoring tuple, threshold). |
| GET | `/v1/backtest/results/{cell_id}/{model_id}` | Latest result for `(cell, model)`. |
| GET | `/v1/backtest/results/{cell_id}` | All models' results on a cell, ranked. |
| GET | `/v1/backtest/vintages` | List available vintage dates for replay. |
| GET | `/v1/backtest/vintages/{vintage_id}` | Lineage record (L182). |
| POST | `/v1/backtest/jobs` | Submit a backtest run. Returns `job_id`. |
| GET | `/v1/backtest/jobs/{job_id}` | Poll a job. |
| GET | `/v1/backtest/jobs/{job_id}/results` | Retrieve results when `state=succeeded`. |
| POST | `/v1/backtest/submissions` | Submit a third-party model's results for vetting. |
| GET | `/v1/backtest/leaderboard` | Current leaderboard (L184). |
| GET | `/v1/backtest/leaderboard/{epoch}` | Historical leaderboard at an epoch. |

### `GET /v1/backtest/cells/{cell_id}` response

```json
{
  "cell_id": "C-03",
  "variable": "GDP-real-yoy",
  "horizon_q": 4,
  "country_set": "Tier-V Core (26)",
  "evaluation_window": "2014-Q1..2025-Q4",
  "n_vintages": 48,
  "primary_metric": "crps",
  "calibration_test": "pit_ks",
  "comparison_test": "dm_hln",
  "benchmark": "IMF WEO",
  "threshold": {
    "type": "dm_not_worse",
    "operator": ">=",
    "value": 0.50,
    "explanation": "At ≥50% of Tier-V countries, OPENGEM is not statistically worse than IMF WEO at α=0.10 in the HLN-corrected DM test"
  },
  "model_card_url": "https://opengem.org/methodology/vv-matrix/C-03"
}
```

### `POST /v1/backtest/jobs` request

```json
{
  "schema": "opengem.backtest_job.v1",
  "name": "my-elastic-net-baseline-2026-06",
  "submitter_email": "researcher@uni.edu",
  "scope": {
    "cells": ["C-01", "C-03", "C-08", "C-10"],
    "countries": ["USA", "GBR", "DEU", "FRA"],
    "vintages": "all"
  },
  "model": {
    "source": "github",
    "repo": "github.com/some-academic/my-elastic-net",
    "git_sha": "a1b2c3d",
    "container_image": "ghcr.io/some-academic/elastic-net:0.1",
    "container_digest": "sha256:..."
  },
  "limits": {
    "max_wall_clock_seconds": 3600,
    "max_memory_gb": 8,
    "max_cpu_cores": 4
  },
  "metric_request": ["crps", "pit_ks", "mae", "dm_vs_opengem"],
  "notify_url": "https://hooks.example.com/job-done"
}
```

### `POST /v1/backtest/jobs` response

```json
{
  "job_id": "job_2026-06-06T08:00:00Z_my-elastic-net-baseline-2026-06",
  "state": "queued",
  "queue_position": 14,
  "estimated_start_at": "2026-06-06T09:30:00Z",
  "estimated_wall_clock_seconds": 1800,
  "limits_accepted": true,
  "links": {
    "self": "/v1/backtest/jobs/job_2026-06-06T...",
    "results": "/v1/backtest/jobs/job_2026-06-06T.../results",
    "logs": "/v1/backtest/jobs/job_2026-06-06T.../logs"
  }
}
```

The harness mounts the requested vintages in a sandboxed container, runs the submitter's model, and scores it against the cells' scoring tuples (L183). The submitter's container produces a `forecast.v1` JSON per vintage; the harness writes scores into a job-local `vv_results` view.

### Job sandboxing

- Container is run with `--network=none` (no internet egress), `--read-only` rootfs, mounted vintage data on a read-only volume, and a writable scratch volume.
- Resource limits enforced via cgroup constraints matching the `limits` block.
- Container is killed and the job marked `failed` if it exceeds wall-clock or memory.

This is the integrity guarantee: a third-party model cannot reach into OPENGEM's vintage store, cannot phone home, cannot exceed allocated compute. Its forecasts are the only output.

## Python client

```python
# packages/opengem-client/src/opengem/backtest.py

from opengem import BacktestClient

client = BacktestClient(api_key=os.environ["OPENGEM_API_KEY"])

# List cells in scope
cells = client.list_cells()
for cell in cells:
    print(cell.cell_id, cell.variable, cell.horizon_q)

# Submit a backtest job
job = client.submit_job(
    name="my-elastic-net-baseline-2026-06",
    cells=["C-01", "C-03"],
    countries=["USA", "GBR", "DEU"],
    model_repo="github.com/some-academic/my-elastic-net",
    git_sha="a1b2c3d",
    container_image="ghcr.io/some-academic/elastic-net:0.1",
    container_digest="sha256:...",
    max_wall_clock_seconds=1800,
    max_memory_gb=8,
)

# Poll until done
job.wait()  # blocks; raises BacktestJobError on failure

# Retrieve results
results = job.results()
for cell_id, score in results.items():
    print(cell_id, score.crps, score.pit_ks_pvalue, score.dm_vs_opengem_pvalue)

# Compare against the live leaderboard
leaderboard = client.leaderboard()
my_rank = leaderboard.where_would("my-elastic-net-baseline-2026-06", results)
print(f"This model would rank #{my_rank} on the SSS aggregate.")
```

The client wraps the REST endpoints, handles retries via `tenacity`, surfaces typed errors (`BacktestJobError`, `RateLimitError`, `InvalidScopeError`), and ships as `pip install opengem-backtest-client`.

## Java client

```java
// io.opengem.backtest:opengem-backtest-client:1.0.0

OpengemClient client = OpengemClient.builder()
    .apiKey(System.getenv("OPENGEM_API_KEY"))
    .build();

List<Cell> cells = client.backtest().listCells();
for (Cell cell : cells) {
    System.out.printf("%s %s horizon=%dQ%n",
        cell.getCellId(), cell.getVariable(), cell.getHorizonQ());
}

JobRequest request = JobRequest.builder()
    .name("my-elastic-net-baseline-2026-06")
    .cells(List.of("C-01", "C-03"))
    .countries(List.of("USA", "GBR", "DEU"))
    .modelRepo("github.com/some-academic/my-elastic-net")
    .gitSha("a1b2c3d")
    .containerImage("ghcr.io/some-academic/elastic-net:0.1")
    .containerDigest("sha256:...")
    .maxWallClockSeconds(1800)
    .maxMemoryGb(8)
    .build();

Job job = client.backtest().submitJob(request);
job.waitForCompletion(Duration.ofMinutes(30));

Results results = job.results();
results.forEach((cellId, score) ->
    System.out.printf("%s: CRPS=%.4f, PIT-KS p=%.3f%n",
        cellId, score.getCrps(), score.getPitKsPvalue())
);
```

The Java client mirrors the Python client API one-for-one, distributed via Maven Central as `io.opengem.backtest:opengem-backtest-client:1.0.0`.

## Submission flow (third-party scoring)

```
1. Author writes a model: container that reads a vintage Parquet directory + writes forecast.v1 JSON.
2. Author publishes the container at a public registry (ghcr.io / quay.io / docker.io).
3. Author submits via POST /v1/backtest/jobs with the container digest.
4. Harness runs the container against the requested cells × vintages.
5. Results computed by the engine; written to a job-private table.
6. Author can choose to:
   a. Keep results private (only the author sees them).
   b. Publish to the public leaderboard via POST /v1/backtest/submissions, which gates on:
      - Container digest pinned (no mutable tags)
      - Code SHA points at a public commit
      - License declared
      - Methodology page URL provided
      - OPENGEM maintainer signs off (manual review, ~weekly cadence)
```

After approval, the third-party model joins the leaderboard with full provenance.

## Rate limits and pricing

| Tier | Submissions/day | Wall-clock budget/day | Cost |
|---|---|---|---|
| Free | 5 | 30 minutes | $0 |
| Academic | 50 | 6 hours | $0 (verified .edu/.ac email) |
| Pro | 500 | 30 hours | $99/mo |
| Institutional | unlimited | dedicated runner | contact |

## Observability

The harness publishes Prometheus metrics at `/metrics`:

- `opengem_backtest_jobs_queued_total{state}`
- `opengem_backtest_jobs_duration_seconds{cell_id, model_id}`
- `opengem_backtest_jobs_failed_total{reason}`
- `opengem_backtest_vintage_archive_bytes`

These power the public health dashboard and the SLO alerts.

## What this loop produced

- REST endpoint catalogue.
- Job submission request/response examples.
- Sandboxing contract.
- Python client API.
- Java client API.
- Submission-to-leaderboard flow.
- Tier pricing.

## What comes next

- **L186** — reproducibility envelope defining what the container must produce.
- **L201** — hyperparameter sweep tracking inside the harness.

## Related

- [[R24-backtest-engine]] — internal engine this exposes.
- [[L181-forecast-object-schema]] — forecast.v1 the container must emit.
- [[L182-forecast-vintage-lineage]] — vintages this serves.
- [[L186-reproducibility-envelope]] — envelope rules.
- [[L184-leaderboard-ranking]] — leaderboard this feeds.
