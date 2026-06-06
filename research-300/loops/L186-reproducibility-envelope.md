# L186 — Reproducibility Envelope

**Loop**: 186 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The decision

A *reproducibility envelope* is the minimal bundle of bytes such that anyone, anywhere, with the right runtime can produce the same forecast that OPENGEM published — byte-identical modulo timestamps. R16 sketched the hash quintuple; this loop pins the schema, the storage layout, and the verification command.

The envelope is the load-bearing artifact behind the accountability promise. Without it, "open" is a vibe; with it, "open" is a fact you can run on your laptop.

## The five bytes

The envelope's content is the union of five hashable artefacts:

1. **Data lockfile** — every input series with its `vintage_at` timestamp and SHA-256.
2. **Code commit** — `git_sha` of the model repository.
3. **Container digest** — `sha256:...` of the OCI image that ran the model.
4. **Weights / state file** — model parameters as a binary blob with its own hash.
5. **Configuration** — the resolved YAML/JSON config that drives the run (seed, n_draws, model variant, etc.).

A forecast's `provenance` block (L181) and `model_snapshot` block (L182) carry pointers to all five. The envelope *aggregates* them into one verifiable blob.

## Envelope schema

```json
{
  "schema": "opengem.reproducibility_envelope.v1",
  "envelope_id": "env_2026-06-06T08:00:00Z_USA-quartet-L3-BMA-v3.2.1",
  "envelope_sha256": "sha256:5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b",
  "produced_at": "2026-06-06T08:00:14Z",

  "data_lockfile": {
    "url": "s3://opengem-lockfiles/2026-06-06T080000Z_USA-quartet.lock.json",
    "sha256": "sha256:1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b",
    "summary": {
      "n_series": 14,
      "frequency_mix": ["A", "Q", "M", "D"],
      "earliest_observation": "1947-Q1",
      "latest_observation": "2026-06-05",
      "license_mix": ["public-domain", "CC-BY-4.0"]
    }
  },

  "code_commit": {
    "repo": "github.com/opengem/opengem-1",
    "git_sha": "9b3a4f7c8d1e2a5b6c7d8e9f0a1b2c3d4e5f6a7b",
    "git_tag": "v3.2.1",
    "git_dirty": false,
    "commit_signature_verified": true,
    "commit_author": "Edgardo Munoz <edgardo@opengem.org>",
    "commit_signed_by_key": "RSA4096/A1B2C3D4E5F6"
  },

  "container": {
    "registry": "ghcr.io",
    "image": "opengem/opengem-l3",
    "tag": "3.2.1",
    "digest": "sha256:8e1d7a9c4b2f5e6d3a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1",
    "built_at": "2026-06-04T22:00:00Z",
    "built_from_dockerfile_sha": "sha256:4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e",
    "base_image": "python:3.13.2-slim-bookworm",
    "size_bytes": 1437592583,
    "sbom_url": "s3://opengem-sboms/3.2.1.cyclonedx.json"
  },

  "weights": {
    "url": "s3://opengem-weights/L3-BMA-v3.2.1/USA/2026-06-06.npz",
    "sha256": "sha256:2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c",
    "size_bytes": 4882144,
    "format": "numpy_npz",
    "n_parameters": 12047,
    "produced_by_training_run": "train_2026-Q1_L3-BMA_USA"
  },

  "configuration": {
    "url": "s3://opengem-lockfiles/2026-06-06T080000Z_USA-quartet.config.json",
    "sha256": "sha256:3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d",
    "summary": {
      "model_variant": "L3-BMA",
      "n_monte_carlo_draws": 10000,
      "rng_seed": 20260606,
      "deterministic_mode": true,
      "bma_combiner": {
        "members": ["L3-DFM-v1.2", "L3-ML-RIDGE-v1.4", "L3-BVAR-LARGE-v2.0"],
        "weights": [0.41, 0.34, 0.25],
        "weighting_rule": "log-score-over-2014-2025-rolling"
      }
    }
  },

  "verification": {
    "method": "opengem replay --envelope-id env_2026-06-06T08:00:00Z_USA-quartet-L3-BMA-v3.2.1 --verify-bytes",
    "expected_forecast_ids": [
      "fcst_2026-06-06_USA_GDP_1Q_OPENGEM-L3-BMA_v3.2.1",
      "fcst_2026-06-06_USA_GDP_4Q_OPENGEM-L3-BMA_v3.2.1",
      "..."
    ],
    "expected_output_sha256_per_forecast": {
      "fcst_2026-06-06_USA_GDP_1Q_OPENGEM-L3-BMA_v3.2.1":
        "sha256:e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6"
    }
  }
}
```

## The data lockfile, drilled down

The data lockfile is its own JSON file (URL-referenced from the envelope):

```json
{
  "schema": "opengem.data_lockfile.v1",
  "lockfile_id": "2026-06-06T080000Z_USA-quartet",
  "series": [
    {
      "series_id": "BEA-T10101-A191RL",
      "vintage_at": "2026-05-29T16:30:00Z",
      "blob_url": "s3://opengem-vintage/USA/BEA/T10101/A191RL/2026-05-29T163000Z.parquet",
      "sha256": "sha256:7a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b",
      "n_observations": 318,
      "license": "public-domain",
      "license_attribution_required": false
    },
    {"series_id": "BLS-CPIAUCSL", "vintage_at": "...", "blob_url": "...", "sha256": "..."},
    {"series_id": "FRB-H15-DGS10", "vintage_at": "...", "blob_url": "...", "sha256": "..."}
  ],
  "manifest_sha256": "sha256:1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b"
}
```

`manifest_sha256` is the SHA-256 of the canonicalised JSON (sorted keys, no whitespace) — this is the hash that appears in the envelope's `data_lockfile.sha256` field.

## The envelope hash itself

`envelope_sha256` is computed as SHA-256 of the canonicalised envelope JSON *with the `envelope_sha256` field set to a placeholder*. The placeholder convention: hash the JSON with `envelope_sha256: ""`, then write the hash back into the field.

This is the same trick Docker uses for image digests. The reader can verify the envelope hasn't been tampered with by re-canonicalising and re-hashing.

## Storage and discovery

Envelopes live in two stores:

1. **Hot store** (PostgreSQL `reproducibility_envelopes` table): all envelope JSON for the last 90 days, indexed by `envelope_id`, `forecast_id_emitted`, `vintage_id`, `git_sha`, `container_digest`.
2. **Cold store** (S3 with object-lock + WORM, 10-year retention): all envelope JSON forever, organised under `s3://opengem-envelopes/{YYYY}/{MM}/{envelope_id}.json`.

The dashboard's lineage browser (L182) pulls the envelope JSON when the user clicks "view envelope" on any forecast.

## Verification command

```bash
opengem replay --envelope-id env_2026-06-06T08:00:00Z_USA-quartet-L3-BMA-v3.2.1 \
               --verify-bytes \
               --output ./replay-output/
```

What this does, step by step:

1. Fetch envelope JSON from `https://api.opengem.org/v1/envelopes/{envelope_id}`. Verify `envelope_sha256` matches re-computed hash.
2. Fetch data lockfile JSON, verify hash.
3. For each series in lockfile: download Parquet blob, verify SHA-256. Halt on mismatch.
4. Pull container image at recorded digest (`docker pull ghcr.io/opengem/opengem-l3@sha256:...`).
5. Verify container digest matches.
6. Download weights blob, verify SHA-256.
7. Mount inputs into container's `/data`, weights into `/weights`, config into `/config.json`.
8. Run `docker run --network=none --read-only ... ghcr.io/opengem/opengem-l3@sha256:... opengem-l3 forecast --config /config.json`.
9. Capture stdout (the emitted `forecast.v1` JSONs).
10. For each expected forecast, SHA-256 the emitted JSON (after canonicalisation, replacing `released_at` with the original value). Compare to `expected_output_sha256_per_forecast`.
11. Exit 0 if all match; exit 1 with diff otherwise.

The whole verification on a single envelope (one country, 8 forecasts) takes ~2 minutes wall-clock on a 4-core/8 GB laptop. The container is the heavy lift; the rest is download + SHA + compare.

## Replay-and-diff CI

A nightly CI job picks a random recent envelope from the public archive and runs the verification. Failures are paged loud. This is the *self-audit*: OPENGEM verifies its own reproducibility every night. If it ever fails, that failure becomes a public incident report (L200).

## Backward replay across major code versions

A v3.2.1 envelope is replayable with the v3.2.1 container. A v4.0 release does not invalidate the envelope; it just runs in a different container. We commit to:

- Pulling container images from `ghcr.io/opengem/*` for at least 5 years.
- Maintaining a `opengem-archive-images` mirror on a separate registry as fallback.
- Documenting any breaking dependency change in `RELEASE-NOTES.md` so that historical envelopes flag a "may not replay on current host architecture" warning.

## What's deliberately not in the envelope

- **Live LLM narrative output** (L198). The narrative pipeline is non-deterministic (LLM sampling) and downstream of the forecast. The forecast is reproducible; the narrative is documented but not byte-replayable.
- **Front-end build artefacts** (Next.js bundle, etc.). These are display layer; the underlying JSON is what's reproducible.
- **Human-edited methodology pages** (model cards). These are versioned in git but are not part of the runtime envelope.

## What this loop produced

- `reproducibility_envelope.v1` schema.
- Data lockfile schema.
- Envelope hashing convention.
- Hot + cold storage layout.
- 11-step `opengem replay --verify-bytes` contract.
- Replay-and-diff CI commitment.

## What comes next

- **L201** — hyperparameter sweep tracking referencing this envelope structure for each trial.
- **L185** — backtest harness API consumes envelopes for third-party replay.

## Related

- [[L181-forecast-object-schema]] — provenance block in forecast.v1.
- [[L182-forecast-vintage-lineage]] — lineage record this envelopes.
- [[R16-reproducibility]] — hash quintuple background.
- [[R24-backtest-engine]] — backtest replays use this same machinery.
- [[L200-failure-log]] — verification failures get posted here.
