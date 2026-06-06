# R18 — First 90 Days Execution Plan

| Field | Value |
|---|---|
| Document ID | OG1-RES-018 |
| Revision | A (2026-05-24) |
| Date | 2026-05-24 |
| Status | **Tactical plan for the 90 days after rev C sign-off.** |
| Authority | R99, LOOP_PLAN v2, R13 §13 stress-test gate (a) |

---

## 1. Why this exists

R99 says "Option A: accept rebaseline; restart LOOP_PLAN; begin upstream-agency adapter work in parallel." That's a high-level intent. R18 makes it concrete: **what gets built in the first 90 days, in what order, with what gates between phases.**

The plan is deliberately scoped to be **achievable in 6–12 hours/week** of part-time effort.

## 2. Pre-condition

- R99 sign-off (Option A).
- Rev C CONOPS baselined.
- v2.0 master doc baselined.
- LOOP_PLAN v2 active.

## 3. Phase 0 — Setup (Week 0, ~4 hours)

### 3.1 Repository skeleton

```
opengem/
├── docs/                                  (exists)
├── src/
│   ├── opengem/
│   │   ├── adapters/                      ← Phase 1
│   │   │   ├── __init__.py
│   │   │   ├── bea.py
│   │   │   ├── bls.py
│   │   │   ├── frb_board.py
│   │   │   ├── treasury.py
│   │   │   └── census.py
│   │   ├── storage/                       ← Phase 1
│   │   ├── orchestration/                 ← Phase 2 (Dagster)
│   │   ├── models/                        ← Phase 3 (L3 + L2)
│   │   ├── api/                           ← Phase 4 (Spring Boot — Java)
│   │   └── mcp/                           ← Phase 5
│   └── tests/
├── data/
│   ├── raw/                               (vintage snapshots — gitignored)
│   ├── derived/                           (gitignored)
│   └── fixtures/                          (golden test data)
├── deploy/
│   ├── docker-compose.yml
│   └── Dockerfile.*
├── pyproject.toml                         (Python project)
├── pom.xml                                (Java/Spring project, later)
└── README.md
```

### 3.2 Tooling

- Python 3.12 + `uv` for dependency management
- Java 21 + Maven (later)
- Docker + Docker Compose
- PostgreSQL 16 + TimescaleDB extension
- Pre-commit hooks: ruff, mypy, pytest-cov
- GitHub Actions: CI on push (lint, type-check, test); golden-fixture validation

### 3.3 Database schema v0

Minimal tables to start:

```sql
CREATE TABLE source (
  source_id     TEXT PRIMARY KEY,    -- 'BEA', 'BLS', etc.
  name          TEXT NOT NULL,
  base_url      TEXT NOT NULL,
  retrieved_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE series_meta (
  series_id     TEXT PRIMARY KEY,    -- e.g., 'BEA.NIPA.T10101.L1' for real GDP
  source_id     TEXT REFERENCES source(source_id),
  description   TEXT,
  unit          TEXT,
  frequency     TEXT,
  country       TEXT,
  variable_kind TEXT                 -- 'gdp_real', 'cpi_headline', etc.
);

CREATE TABLE raw_observation (
  series_id     TEXT REFERENCES series_meta(series_id),
  observed_at   DATE NOT NULL,        -- reference period
  vintage_at    DATE NOT NULL,        -- release date
  value         NUMERIC,
  PRIMARY KEY (series_id, observed_at, vintage_at)
);
SELECT create_hypertable('raw_observation', 'vintage_at');

CREATE TABLE vintage_snapshot (
  vintage_hash  TEXT PRIMARY KEY,
  taken_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  source_id     TEXT REFERENCES source(source_id),
  manifest      JSONB                  -- list of series + counts
);
```

This is the v0 — sufficient for the first 90 days. SSDD-001 v2 will expand.

## 4. Phase 1 — US Adapter Cohort (Weeks 1–4, ~16 hours total)

### 4.1 Week 1: BEA NIPA adapter

- API key signup (free, 1 day approval)
- Implement `adapters/bea.py`: `pull_series(series_id) -> list[Observation]`
- Series in scope: real GDP, nominal GDP, GDP deflator, GDI, PCE deflator, government spending, private investment, NX components
- Vintage handling: snapshot at release; store with `vintage_at = today_utc()`
- Tests: golden fixtures for one quarter of historical data

### 4.2 Week 2: BLS adapter

- API key signup
- Implement `adapters/bls.py`
- Series in scope: CPI (CUUR0000SA0, CUSR0000SA0L1E), unemployment (LNS14000000), nonfarm payrolls (CES0000000001), JOLTS openings
- Same pattern as BEA

### 4.3 Week 3: FRB Board adapter

- DataDownload Programs no auth
- Implement `adapters/frb_board.py` for H.15 (rates), G.17 (IP), H.6 (M2)
- Series: DGS10, DGS2, DGS3MO, FEDFUNDS, DFEDTARU/L, INDPRO, CAPUTL, M2SL

### 4.4 Week 4: Treasury + Census adapters

- Treasury FiscalData (no auth) — daily yield curve as redundancy
- Census M3 + MRTS — inventory-to-sales, retail sales
- Series: yield curve, debt to the penny, M3 inventory, MRTS retail

### 4.5 Phase 1 exit criteria

- All 5 adapters compile, type-check, lint clean.
- Each adapter has ≥1 integration test against a golden fixture.
- Each adapter successfully pulls one historical quarter of representative data without error.
- `raw_observation` table populated with ≥1000 series-period-vintage tuples.

## 5. Phase 2 — Orchestration + Storage (Weeks 5–6, ~8 hours total)

### 5.1 Dagster setup

- Install Dagster (Python)
- Define one asset graph: `us_macro_panel` → depends on `bea_assets`, `bls_assets`, `frb_assets`, `treasury_assets`, `census_assets`
- Each adapter exposes its own asset partition (per series)
- Schedule: daily 06:00 UTC

### 5.2 Vintage snapshot mechanism

- After every successful adapter run, compute `vintage_hash` over the set of (series_id, observed_at, value) tuples written that run
- Store in `vintage_snapshot` with manifest
- Verify reproducibility: re-run adapter on same release date → same `vintage_hash`

### 5.3 Phase 2 exit criteria

- Dagster UI runs locally; full asset graph green.
- One full daily-orchestration run completes successfully.
- Vintage hashes are deterministic across re-runs.

## 6. Phase 3 — L3 MVP probe (Weeks 7–10, ~16 hours)

**This is the critical gate from R13 §13 stress-test (a).** If L3-as-workhorse doesn't show meaningful skill on US data alone, the entire rescope is invalid.

### 6.1 Scope of L3 MVP

- One country (US).
- One variable (real GDP quarterly growth).
- Two horizons (1Q and 4Q).
- L3 variants:
  - Univariate AR(2) (sanity baseline)
  - Mixed-frequency DFM (Banbura-Giannone-Reichlin Minnesota natural-conjugate)
  - DFM + LightGBM residual
  - BMA over the three

### 6.2 Implementation

- Use `statsmodels` for DFM (or implement simple state-space if needed)
- `lightgbm` for residual ML
- Small BMA combiner using rolling-window log scores

### 6.3 Evaluation

- Pseudo-real-time backtest 2014Q1–most recent (using vintages from Phase 1 ingestion + ALFRED queries for backfill where allowed)
- Cells from V&V matrix (R08 §3):
  - C-01 (GDP 1Q vs. AR(1)/RW by CRPS): target ≥80% win on US
  - C-02 (GDP 1Q PIT KS): target pass
  - C-03 (GDP 4Q vs. WEO same-vintage): target not worse on US

### 6.4 Phase 3 decision gate

| Result | Action |
|---|---|
| US clears C-01, C-02, C-03 | Validate L3-as-workhorse. Proceed to Phase 4. |
| US clears 2 of 3 | Investigate failure mode; iterate L3 variants; re-test. |
| US clears 0–1 of 3 | **Halt.** Revisit rev C architecture; possibly fall back to "more layers" or different combiner. R99 verdict may need revisiting. |

## 7. Phase 4 — Read API skeleton (Weeks 11–12, ~8 hours)

### 7.1 Spring Boot scaffold

- `pom.xml` with Java 21, Spring Boot 3.x, Lombok, jdbcTemplate
- Two endpoints minimal:
  - `GET /v1/forecast?country=US&variable=gdp_real&horizon=1Q`
  - `GET /v1/runs/{run_id}` (provenance)
- JSON output matching ICD-002 v2 draft

### 7.2 Hand-shake with Python L3

- L3 outputs forecasts to `forecast_point` table (Postgres)
- Spring Boot read API queries that table
- No gRPC needed at v0; just shared DB

### 7.3 Phase 4 exit criteria

- API serves a forecast for US GDP at 1Q and 4Q
- Provenance roundtrip works (`code_sha + vintage_hash + run_id`)
- p95 latency ≤ 500ms (very easy for read-only)

## 8. Phase 5 — Reflection + Decide v0.4 Scope (Week 13, ~4 hours)

End of Day 90. Look at:

- Did L3 MVP pass the gate? If no → revisit architecture, possibly halt.
- Adapter cohort quality: schema drift seen? Outages handled? Tests still passing?
- Time spent: was 6–12 hr/week sustainable? If not, scope-staging needs refinement.
- Next 90 days planning: per LOOP_PLAN v2, target Iter 12 (SSDD-001 v2 with full adapter spec) and start v0.4 work (L2 BGVAR via R adapter; first Tier-V Core country beyond US; Situation Subsystem stub).

### 8.1 v0.4 candidate scope (post-Day-90)

If Phase 3 gate passes:
- Add Tier-V Core countries: CA, UK, DE (these have rich ORDRA + EABCN + national vintage data)
- BGVAR R-adapter via subprocess
- Situation Subsystem term-spread endpoint (US only first)
- Backtest service per V&V matrix
- Public dashboard (Vercel) read-only

## 9. Total time budget

| Phase | Weeks | Hours |
|---|---|---|
| Phase 0 | 1 | 4 |
| Phase 1 | 4 | 16 |
| Phase 2 | 2 | 8 |
| Phase 3 | 4 | 16 |
| Phase 4 | 2 | 8 |
| Phase 5 | 1 | 4 |
| **Total** | **13 weeks** | **56 hours** |

**Average**: ~4.3 hours/week. Achievable at 6–12 hr/week budget with ample slack.

## 10. Risks specific to first 90 days

| Risk | Mitigation |
|---|---|
| BEA / BLS API quirks burn more time than planned | Time-box each adapter to 4 hours; if blocked, move to next and revisit |
| L3 MVP fails the gate | Cleanly accepted — gate is there to surface this before more investment |
| Database schema iteration | Use Alembic migrations from Day 1 to make schema evolution painless |
| Distraction from other 5 active projects | Phase boundaries are explicit pickup-and-put-down points |
| Time underestimated | The 56-hour total has ~30% slack vs. a 6 hr/week × 13 week = 78 hour budget |

## 11. Definition of done for Day 90

- [ ] Five US-agency adapters working
- [ ] Postgres + TimescaleDB schema deployed locally
- [ ] Vintage snapshots reproducible (same hash on re-run)
- [ ] Dagster orchestration green daily
- [ ] L3 MVP forecasting US GDP 1Q and 4Q (whether or not it passes the V&V cells)
- [ ] Spring Boot read API serving forecasts with provenance
- [ ] Phase 3 gate decision documented: continue / iterate / halt
- [ ] Updated LOOP_PLAN v2 reflecting actual progress vs. plan
- [ ] Day-90 retrospective memo (`R200-day-90-retro.md` template)

## 12. Bottom line

The first 90 days are deliberately **boring**: 5 adapter modules, 1 orchestration setup, 1 L3 MVP, 1 API skeleton. The most important deliverable is the **Phase 3 gate decision** — does L3 actually work as the workhorse on real US vintage data? If yes, OPENGEM proceeds. If no, R99 is invalidated and we revisit.

This is the smallest feasible end-to-end slice that tests the rev C architecture's load-bearing premise. Anything more ambitious in the first 90 days is overconfidence.

---

*End of R18 Rev A.*
