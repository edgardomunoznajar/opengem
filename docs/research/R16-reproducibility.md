# R16 — Reproducibility Architecture

| Field | Value |
|---|---|
| Document ID | OG1-RES-016 |
| Revision | A (2026-05-24) |
| Date | 2026-05-24 |
| Status | **Cross-cutting design memo: provenance, hashing, bit-identical replay.** |
| Authority | StRS-003, FR-CFG-001, NFR-RPR-001 |

---

## 1. Why this exists

OPENGEM's claim to differentiation is **public accountability**. That claim is hollow unless any forecast OPENGEM has ever published can be **bit-identically reproduced** from its provenance triplet `(code_sha, vintage_hash, prior_hash, posterior_hash)`. This memo specifies the architecture that makes that work.

## 2. The hash quintuple

Every published forecast carries five hashes:

| Hash | Of what | When computed |
|---|---|---|
| `code_sha` | Git commit hash of OPENGEM repo + lockfile-pinned dependencies | At pipeline build time |
| `vintage_hash` | Content hash of the input data vintage used | At ingestion completion |
| `prior_hash` | Content hash of the prior set (Bayesian model priors as JSON-serialized blob) | At prior-loading |
| `posterior_hash` | Content hash of posterior samples / parameter estimates | At model fitting completion |
| `run_id` | Triplet of (code_sha, vintage_hash, posterior_hash) — short canonical reference | At run start |

Run-level immutability: once a forecast record is written with a `run_id`, it never changes. Corrections produce a *new* run with `superseded_by` pointer.

## 3. Storage

### 3.1 Code

- Single Git repository.
- Every release is a Git tag (semver).
- `code_sha` is the Git SHA at build time.
- Dependencies pinned in `uv.lock` (Python) and `pom.xml` (Java) — both committed.
- Container image digest stored alongside `code_sha`.

### 3.2 Data vintages

- Every source pull writes to `raw_observation` (Postgres hypertable).
- A `vintage_snapshot` row is written per pull batch with `vintage_hash = sha256(canonical_csv(rows))`.
- Canonicalization: rows sorted by (series_id, observed_at, vintage_at); deterministic CSV serialization.
- Vintage snapshots never overwritten — every release is a new snapshot.
- For backfilled historical vintages (from ORDRA / RTDSM / Dallas Fed): one-time ingestion writes per-vintage rows tagged with that vintage's release date.

### 3.3 Priors

- Stored as JSON blob in `prior_set` table.
- `prior_hash = sha256(json_canonical(prior_blob))`.
- Linked to the model variant and version that uses them.
- Changes in priors → new `prior_hash` → all downstream `posterior_hash` change → traceability.

### 3.4 Posteriors

- Stored in MinIO object store as parquet files.
- Object path: `posteriors/{model_variant}/{posterior_hash}.parquet`.
- `posterior_hash = sha256(canonical_parquet_bytes)`.
- Database row in `posterior` table with `(posterior_hash, model_variant, code_sha, prior_hash, vintage_hash, fit_time, fit_log)`.

### 3.5 Forecast records

```sql
CREATE TABLE forecast_run (
  run_id          TEXT PRIMARY KEY,    -- short canonical reference
  code_sha        TEXT NOT NULL,
  vintage_hash    TEXT NOT NULL,
  prior_hash      TEXT NOT NULL,
  posterior_hash  TEXT NOT NULL,
  started_at      TIMESTAMPTZ NOT NULL,
  completed_at    TIMESTAMPTZ NOT NULL,
  superseded_by   TEXT REFERENCES forecast_run(run_id)
);

CREATE TABLE forecast_point (
  run_id          TEXT REFERENCES forecast_run(run_id),
  country         TEXT NOT NULL,
  variable        TEXT NOT NULL,
  horizon_q       INTEGER NOT NULL,
  p10             NUMERIC,
  p25             NUMERIC,
  p50             NUMERIC,
  p75             NUMERIC,
  p90             NUMERIC,
  variant_weights JSONB,
  PRIMARY KEY (run_id, country, variable, horizon_q)
);
SELECT create_hypertable('forecast_point', 'run_id', if_not_exists => TRUE);
```

## 4. The replay-and-diff CI

NFR-RPR-001 requires bit-identical reproduction. Implementation:

1. Nightly CI job picks a random recent `run_id`.
2. Reconstructs: pulls `code_sha` → checks out repo → builds container.
3. Replays: feeds `vintage_hash` snapshot to the model pipeline.
4. Diffs: compares the new posterior parquet bytes to the stored parquet at `posterior_hash`.
5. Pass: bytes match exactly.
6. Fail: opens issue with reproducibility incident label `inc/repro`.

Implementation note: reproducibility depends on:
- Deterministic random seeds per variant.
- Stable BLAS / threading config (set in container env vars).
- Stable Postgres ORDER BY in any query that feeds the model.
- Deterministic JSON serialization (Python: `sort_keys=True`).

Any non-determinism is a bug — flagged and fixed, not ignored.

## 5. Public surface

Provenance is exposed at the API:

```
GET /v1/forecast?country=US&horizon=1Q
  → { ..., "run_id": "20260524-q2-2026-vintage", "code_sha": "abc123...",
      "vintage_hash": "def456...", "model_card_url": "..." }

GET /v1/runs/{run_id}
  → full provenance triplet + model-card metadata + supersedes pointer
```

Every forecast on the dashboard links to its `/v1/runs/{run_id}` provenance page.

## 6. Model cards

A model card per model-variant per code version per release:

```yaml
# model_cards/v1_dfm/2026-q2.yaml
model_variant: v1_dfm
code_sha: abc123...
release_tag: v0.4.1
prior_hash: 'sha256:...'
posterior_hash: 'sha256:...'
last_validated: 2026-05-01
training_window: '2004Q1..2026Q1'
known_biases:
  - 'Underestimates inflation tails during regime shifts'
  - 'PIT non-uniform in 2009Q3..2010Q1'
v_v_table:
  C-01: PASS (0.83 win rate vs RW on Tier-V Core)
  C-02: PASS (PIT KS 82%)
  C-03: PASS (DM not worse than WEO on 58%)
  C-05: MARGINAL (PIT KS 68%, threshold 70%)
```

Model cards are themselves version-pinned and published on the dashboard.

## 7. Vintage discipline reproducibility

The hardest reproducibility test: can we, on October 1, 2027, re-run OPENGEM's October 1, 2026, forecast and get bit-identical numbers?

**Yes**, because:
- The October 2026 release of (e.g.) BEA's NIPA Q3 advance estimate was archived as a `vintage_snapshot` on that date.
- The L3 code at the October 2026 release tag is checked out.
- The priors at the October 2026 `prior_hash` are loaded.
- The pipeline runs deterministically.
- Output bytes match the stored posterior parquet exactly.

**Exception cases**:
- If the source agency *restates* a previously-published value (rare for BEA/BLS; commonplace for some emerging-market stat agencies), we keep both vintages. The 2026 run uses the 2026 vintage; the restatement appears as a separate row.
- If we *re-archive* a historical vintage from a third-party source (e.g., Dallas Fed back-fill), we record the original-source release date as `vintage_at` and the re-archive ingestion time as a separate audit column.

## 8. Storage cost

Vintage snapshots are append-only forever (StRS-010). Estimate:

- ~50 series × ~80 countries × monthly = 4k observations / month.
- Average row size: ~200 bytes.
- 4k × 200 bytes × 12 months × 10 years = ~10 GB.
- Posterior parquet files: ~50 MB per model variant per re-fit × 4 variants × 12 months × 10 years = ~24 GB.
- **Total < 100 GB over 10 years.** Negligible.

## 9. Verification tooling

Provide a CLI for auditors:

```bash
opengem verify <run_id>
# downloads code at code_sha, vintage at vintage_hash, replays, diffs
# exit 0 if bit-identical; exit 1 + diff report otherwise
```

This is the "anyone can verify our claim" surface. Eventually published as a public Docker image.

## 10. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Non-determinism in dependencies (e.g., BLAS thread ordering) | Pin env vars (`OPENBLAS_NUM_THREADS=1`, etc.); test in CI |
| Postgres query result ordering | Always `ORDER BY` explicitly in pipeline queries |
| Floating-point summation order | Use Kahan summation where critical; document tolerance windows |
| Vintage snapshot corruption | Checksums + immutable storage; quarterly integrity audit |
| Posterior parquet drift across pandas / pyarrow versions | Pin those versions; CI validates parquet bytes match across pinned versions |

## 11. Bottom line

Reproducibility is **not a feature; it's a constraint**. Every other architectural choice in OPENGEM bends to make bit-identical replay possible. The replay-and-diff CI is the load-bearing test that this discipline survives normal development.

OPENGEM's claim "every forecast we've ever published can be reproduced" is the foundation of its credibility — and it's mechanically verifiable, not aspirational.

---

*End of R16 Rev A.*
