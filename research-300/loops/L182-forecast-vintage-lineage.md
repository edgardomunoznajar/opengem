# L182 — Forecast Vintage Lineage

**Loop**: 182 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The lineage problem

A forecast emitted at 08:00 UTC on 2026-06-06 used some specific bundle of input data, processed by some specific revision of the OPENGEM code, running in some specific container image. Six months later, someone asks: *can I reproduce this exact forecast?* If the answer is "kind of", OPENGEM has lost the asymmetry that L001 promises.

This loop pins the lineage record that lets the answer be "yes, byte-identically, with one command."

## The trace pattern

```
  Vintage Inputs                Model Snapshot              Forecast Output
  (n series × vintage_at)  ──▶  (code SHA, container,  ──▶  (forecast.v1 JSON
                                 data lockfile, weights)     + density samples)
        │                              │                            │
        │                              │                            │
        └─────► vintage_lineage_id ◄───┴────────────────────────────┘
                (content-addressable, deterministic)
```

Every emitted forecast carries a `vintage_id` that uniquely identifies the lineage record. The lineage record is stored separately (in PostgreSQL `forecast_lineage` table + S3-backed Parquet blob store) and never mutated. Append-only.

## The lineage record schema

```json
{
  "schema": "opengem.forecast_lineage.v1",
  "vintage_id": "vint_2026-06-06T08:00:00Z_USA-quartet",
  "created_at": "2026-06-06T08:00:14Z",
  "forecast_ids_emitted": [
    "fcst_2026-06-06_USA_GDP_1Q_OPENGEM-L3-BMA_v3.2.1",
    "fcst_2026-06-06_USA_GDP_4Q_OPENGEM-L3-BMA_v3.2.1",
    "fcst_2026-06-06_USA_GDP_8Q_OPENGEM-L3-BMA_v3.2.1",
    "fcst_2026-06-06_USA_GDP_20Q_OPENGEM-L3-BMA_v3.2.1",
    "fcst_2026-06-06_USA_CPI_1Q_OPENGEM-L3-BMA_v3.2.1",
    "fcst_2026-06-06_USA_CPI_4Q_OPENGEM-L3-BMA_v3.2.1",
    "fcst_2026-06-06_USA_UR_4Q_OPENGEM-L3-BMA_v3.2.1",
    "fcst_2026-06-06_USA_POLRATE_4Q_OPENGEM-L3-BMA_v3.2.1"
  ],
  "input_vintages": [
    {
      "series_id": "BEA-T10101-A191RL",
      "label": "Real GDP, percent change from preceding period, SAAR",
      "frequency": "Q",
      "vintage_at": "2026-05-29T16:30:00Z",
      "vintage_source": "BEA NIPA T1.0.101",
      "last_observation_period": "2026-Q1",
      "n_revisions_since_first_release": 0,
      "blob_url": "s3://opengem-vintage/USA/BEA/T10101/A191RL/2026-05-29T163000Z.parquet",
      "sha256": "sha256:7a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b",
      "license": "U.S. Government work (public domain)"
    },
    {
      "series_id": "BLS-CPIAUCSL",
      "label": "CPI for All Urban Consumers: All Items",
      "frequency": "M",
      "vintage_at": "2026-06-05T12:30:00Z",
      "vintage_source": "BLS CU0000SA0",
      "last_observation_period": "2026-05",
      "n_revisions_since_first_release": 0,
      "blob_url": "s3://opengem-vintage/USA/BLS/CU0000SA0/2026-06-05T123000Z.parquet",
      "sha256": "sha256:8b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c",
      "license": "U.S. Government work (public domain)"
    },
    {
      "series_id": "FRB-H15-DGS10",
      "label": "10-Year Treasury Constant Maturity Rate",
      "frequency": "D",
      "vintage_at": "2026-06-06T07:15:00Z",
      "vintage_source": "FRB H.15",
      "last_observation_period": "2026-06-05",
      "blob_url": "s3://opengem-vintage/USA/FRB/H15/DGS10/2026-06-06T071500Z.parquet",
      "sha256": "sha256:9c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d",
      "license": "U.S. Government work (public domain)"
    }
  ],
  "model_snapshot": {
    "git_repo": "github.com/opengem/opengem-1",
    "git_sha": "9b3a4f7c8d1e2a5b6c7d8e9f0a1b2c3d4e5f6a7b",
    "git_tag": "v3.2.1",
    "git_dirty": false,
    "container_image": "ghcr.io/opengem/opengem-l3:3.2.1",
    "container_digest": "sha256:8e1d7a9c4b2f5e6d3a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1",
    "container_built_at": "2026-06-04T22:00:00Z",
    "data_lockfile": "sha256:1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b",
    "data_lockfile_url": "s3://opengem-lockfiles/2026-06-06T080000Z_USA-quartet.lock.json",
    "python_version": "3.13.2",
    "pip_freeze_url": "s3://opengem-lockfiles/2026-06-06T080000Z_USA-quartet.pip-freeze.txt",
    "r_packages_lockfile": "s3://opengem-lockfiles/2026-06-06T080000Z_USA-quartet.renv.lock",
    "model_weights_url": "s3://opengem-weights/L3-BMA-v3.2.1/USA/2026-06-06.npz",
    "model_weights_sha256": "sha256:2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c"
  },
  "execution_metadata": {
    "build_url": "https://github.com/opengem/opengem-1/actions/runs/8742193845",
    "runner": "self-hosted runner-ny-01",
    "host_os": "Ubuntu 24.04",
    "host_arch": "x86_64",
    "wall_clock_seconds": 87.3,
    "peak_memory_mb": 4128,
    "rng_seed": 20260606,
    "deterministic_mode": true
  },
  "replay_command": "opengem replay --vintage-id vint_2026-06-06T08:00:00Z_USA-quartet"
}
```

## How a reader replays the forecast

The contract is one command:

```bash
opengem replay --vintage-id vint_2026-06-06T08:00:00Z_USA-quartet \
               --verify-bytes \
               --output ./replay-output/
```

What it does:

1. Resolves the `vintage_id` to the lineage record JSON.
2. Pulls the container image at the recorded digest (`docker pull ghcr.io/opengem/opengem-l3@sha256:8e1d7a9c...`). If the image is missing, errors loud.
3. Downloads each input vintage Parquet from the recorded blob URLs. Verifies SHA-256 on each. Any mismatch is a fatal abort.
4. Downloads the data lockfile JSON, verifies hash.
5. Mounts inputs into the container, invokes `opengem-l3 forecast --lockfile /lockfile.json --seed 20260606 --deterministic`.
6. Captures stdout/stderr and the emitted `forecast.v1` JSONs.
7. Compares each emitted JSON to the originally-published JSON (fetched from the public ledger). With `--verify-bytes`, requires byte-identical match modulo `released_at` timestamp.
8. Exits 0 with a green check; or exits nonzero with a side-by-side diff.

When step 7 produces an exact match, the reader has proven that the OPENGEM forecast they read on 2026-06-06 was the consequence of (a) those specific inputs, (b) that specific code, (c) that specific container, (d) those specific weights — and nothing else.

## Why content-addressable

The `vintage_id` format is deterministic: `vint_{released_at}_{country}-{indicator-set}`. The lineage record itself, once written, is hashed and that hash becomes a Merkle root referenced from the public ledger. Tampering with a historical lineage record changes its hash; the ledger entry no longer validates.

The blob store (`s3://opengem-vintage/`) is configured with object lock + WORM retention. Once written, vintages cannot be deleted or modified for 10 years. This is the legal teeth behind the lineage promise.

## What if an input source disappears

A vintage record points at the blob in OPENGEM's own immutable archive, *not* at the upstream agency's URL. If BEA goes offline tomorrow, the vintage we already captured is still in our blob store. The lineage record carries the agency URL as metadata (`vintage_source`) for citation purposes, not for retrieval.

This is the load-bearing reason the FRED-substitution mandate (R05 / ADR-010) matters: we own the cache, so we can reproduce.

## Lineage retention policy

- **Tier-V (vintage-correct) forecasts**: lineage retained forever. WORM-locked for 10 years; thereafter still kept on cold storage indefinitely.
- **Tier-T (tracked-only) forecasts**: lineage retained for 5 years rolling. Tier-T forecasts cannot serve as primary research evidence anyway; they exist to grow into Tier-V.
- **Dev / preview forecasts**: lineage retained for 90 days, never WORM-locked, prefixed `dev-` and barred from any public dashboard surface.

## The lineage browser UI

The dashboard exposes `/forecasts/{forecast_id}/lineage` as a clickable visual:

```
forecast: USA GDP 4Q-ahead, 2026-06-06
└── vint_2026-06-06T08:00:00Z_USA-quartet
    ├── inputs (3 series)
    │   ├── BEA-T10101-A191RL @ 2026-05-29T16:30:00Z [view bytes] [view source link]
    │   ├── BLS-CPIAUCSL      @ 2026-06-05T12:30:00Z [view bytes] [view source link]
    │   └── FRB-H15-DGS10     @ 2026-06-06T07:15:00Z [view bytes] [view source link]
    ├── model snapshot
    │   ├── code: github.com/opengem/opengem-1 @ 9b3a4f7c [view diff]
    │   ├── container: ghcr.io/opengem/opengem-l3 @ sha256:8e1d7a9c [pull]
    │   └── lockfile: 2026-06-06T080000Z_USA-quartet.lock.json [download]
    └── replay
        └── opengem replay --vintage-id ... [copy command]
```

This is rendered from the lineage record JSON directly. No additional API calls.

## What this loop produced

- `forecast_lineage.v1` JSON schema with worked example.
- One-command replay contract.
- Content-addressable lineage IDs.
- Retention policy by tier.
- Browser UI sketch.

## What comes next

- **L186** — full reproducibility envelope (this lineage record is its instantiation).
- **L192** — per-vintage revisions: how successive lineages chain into a forecast history.

## Related

- [[L181-forecast-object-schema]] — forecast object that references this lineage.
- [[L186-reproducibility-envelope]] — envelope spec.
- [[L192-forecast-revisions]] — successive vintages.
- [[R16-reproducibility]] — hash quintuple architecture.
- [[R24-backtest-engine]] — backtest replays use this same lineage mechanism.
