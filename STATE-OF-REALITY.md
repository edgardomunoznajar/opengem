# OPENGEM — State of Reality

**What this is**: an evidence-based audit of what in the OPENGEM v2.0 tree is
*real and verified* versus *partial*, *stub*, or *fabricated*. Produced under
Goal A ("Green, Honest, Baselined"). Every status here was checked by running
code in this environment, not by reading READMEs.

**Date**: 2026-06-06
**Branch**: `goal-a-green-baselined`
**How verified**: `uv sync --all-packages` → `ruff check .` → `pytest` →
per-package import smoke test → surface build attempts. Commands are
reproducible from a fresh checkout.

---

## Headline numbers (measured, not claimed)

| Metric | Value | How |
|---|---|---|
| Python packages (workspace members) | **21** | `uv sync --all-packages` installs all editable |
| Packages that import cleanly | **20 / 21** | import smoke test; only `opengem-mcp` fails |
| Test cases passing | **267 / 267** | `pytest` (245 at Goal A baseline; +22 from Goal B's panel + backtest) |
| Python workspace packages | **23** | 21 at baseline + `opengem-panel` + `opengem-backtest` (Goal B) |
| Lint | **clean** | `ruff check .` passes (shipped code; research-300 excluded) |
| CI | **authored + locally validated** | `.github/workflows/ci.yml`; no git remote yet → not run on GitHub |

### The README's "183 tests" claim — reconciled

`README.md` claims ~183 tests. **Actual is 245 passing.** The claim *undercounts*
— it is stale, not inflated. The suite is larger and healthier than advertised.
The earlier worry ("183 might be aspirational") was wrong in the optimistic
direction.

### What "245 green" does NOT cover (important caveat)

The green suite is real but **not total coverage**:
- `opengem-mcp` contributes **0 tests and does not import** — it is never
  exercised by the suite. "245 green" says nothing about it.
- `opengem-api` (FastAPI stub) and `opengem-dashboard` (Next.js) have **0 Python
  tests**; they are outside the pytest workspace.
- The packaged adapter tests use **mocked HTTP**. The *production* BEA/BLS/FRB
  adapters still have not run against their live upstreams (Goal B sourced real
  data via FRED discovery instead — see below).

---

## Update — Goal B (2026-06-06): first real, scored forecast

The biggest Goal-A gap ("everything is mocked; no real data has flowed") is now
**partially closed**. Two new packages turn the stack from *mocked-green* to a
real, accountable forecast:

- **opengem-panel** — curation slice: vintage observations → dense quarterly
  panel (yoy transforms). Closes the `fit_us_gdp` wiring gap (it called a
  nonexistent `store.load_panel`).
- **opengem-backtest** — CRPS/MAE/PIT metrics, AR(1) + random-walk baselines,
  rolling-origin replay, leaderboard, CLI.

**First real US forecast** (`scripts/first_us_forecast.py`, real FRED data, 261
quarters 1960Q2–2026Q1; result in `docs/first-us-forecast.json`):

| | DFM | AR(1) | RW |
|---|---|---|---|
| GDP yoy 1Q — mean CRPS | **1.380** ✅ | 1.553 | 1.717 |
| GDP yoy 1Q — median CRPS (cap-free) | **0.398** ✅ | 0.405 | 0.428 |
| GDP yoy 1Q — MAE | **1.716** ✅ | 1.743 | 1.918 |

The L3 DFM **beats AR(1) and RW on GDP-1Q by CRPS** — the V&V matrix's headline
bar — corroborated by the cap-free median. Honest mix elsewhere (AR(1) wins
CPI-1Q; DFM wins the 4Q horizons on median). Live forecast: **US GDP yoy 2026Q2
= 2.67% [0.87, 4.47]**, CPI yoy = 2.74% [1.80, 3.69].

**Honest caveats on this result:**
- **Single-vintage backtest.** Actuals are the latest-vintage values, not the
  values knowable at each origin. True vintage-correct replay (replaying the
  store at each origin's own vintage) is the next SSDD-007 step.
- **SE guard.** A numerical cap (SE ≤ 6× in-sample std) prevents the DFM's EM
  fit from emitting a non-credible variance at the COVID outlier; without it the
  mean CRPS is dominated by ~1 blown-up origin. The cap never binds the
  baselines (their variance is inherently bounded), and the median CRPS needs no
  cap and agrees — so the win is not a cap artifact.
- **FRED = discovery only.** Raw data stays in a gitignored local store; the
  production path is still the (mocked, unrun-live) BEA/BLS/FRB adapters.

This updates the L3 / Backtest rows below from "stub/partial" toward real.

---

## Per-package reality (the 21 Python members)

Legend: **real** = working logic + meaningful tests; **partial** = real core,
incomplete vs its design role; **stub** = scaffold/placeholder; **broken** =
present but does not import/run.

| Package | Imports | Tests | Status | Notes |
|---|---|---|---|---|
| opengem-types | ✅ | 32 | **real** | Conditional/Basis/Observation/Vintage/Forecast/Scenario with genuine validation. Added `GDP_YOY`/`CPI_YOY` (see fixes). |
| opengem-vintage | ✅ | 6 | **real** | SQLite store: real DDL, atomic batches, deterministic hash, vintage-as-of queries. *PostgresVintageStore not implemented* (SQLite only). |
| opengem-data-base | ✅ | 13 | **real** | Adapter ABC, exponential-backoff retry w/ jitter, typed catalog, error hierarchy. |
| opengem-data-bea | ✅ | 12 | **real** (mocked) | NIPA adapter; tested against mocked BEA JSON. Never hit live BEA. |
| opengem-data-bls | ✅ | 12 | **real** (mocked) | CPI adapter; mocked. |
| opengem-data-frb | ✅ | 9 | **real** (mocked) | H.15 CSV adapter; mocked. |
| opengem-data-treasury | ✅ | 6 | **real** (mocked) | mocked. |
| opengem-data-census | ✅ | 9 | **real** (mocked) | mocked. |
| opengem-data-ordra | ✅ | 15 | **real** (mocked) | OECD ORDRA vintage adapter; mocked. |
| opengem-data-bis | ✅ | 9 | **real** (mocked) | mocked. |
| opengem-data-gscpi | ✅ | 5 | **real** (mocked) | mocked. |
| opengem-data-gpr | ✅ | 5 | **real** (mocked) | mocked. |
| opengem-data-polecat | ✅ | 8 | **real** (mocked) | Uses ISO-3 country codes in metadata (see latent issue). |
| opengem-scenarios | ✅ | 15 | **real** | Scenario library, invocation, serialization. L1/L2 propagation not wired (design defers it). |
| opengem-recession-prob | ✅ | 11 | **real** | Bauer-Mertens term-spread probit w/ IRLS fitter. |
| opengem-event-detector | ✅ | 9 | **partial** | Rule engine real; live market/news feed integration absent. |
| opengem-digest | ✅ | 7 | **partial** | Renders JSON+markdown; daily cron / real data wiring absent. |
| opengem-narrative | ✅ | 12 | **real** | Enforces the EPISTEMIC.md `Conditional[T]` contract in code (forbidden-phrase / required-marker checks). |
| opengem-l3-dfm | ✅ | 16 | **partial** | Genuinely wraps statsmodels `DynamicFactorMQ`; integration fit passes. Only the DFM variant — no ML-residual, no large-BVAR, no BMA combiner (SSDD-005a). |
| opengem-datasette | ✅ | 9 | **partial** | Snapshot/CLI present; no deployed instance. |
| **opengem-mcp** | ❌ | **0** | **broken stub** | See below — does not import. |

### opengem-mcp — broken stub (the one fabrication-class package)

`import opengem_mcp` **fails**. Concrete defects:
- `console_scripts` declares `opengem-mcp = "opengem_mcp.server:main"` but
  **`server.py` does not exist** in the package.
- `tools/__init__.py` triggers a **circular import** and imports an undefined
  name `cite_this_view`, so even importing the package errors out.
- **0 tests** — the green suite never touches it.

The 7 tool modules + client + envelope are scaffolded, but the package is not
runnable. Per the v2.0 design the MCP server is a deferred capability; this is
left as-is (building it is feature work, out of Goal A's scope) and flagged here
so "245 green" is not mistaken for "MCP works."

### opengem-api & opengem-dashboard (non-workspace surface)

| Surface | Status | Evidence |
|---|---|---|
| opengem-api | **prototype stub** | Bare `main.py`, no `pyproject.toml`. Syntactically valid (`py_compile` OK), 9 FastAPI routes declared. Needs `fastapi` (not a workspace dep). Its own docstring says "NOT the production API." Excluded from the uv workspace. |
| opengem-dashboard | **real (builds)** | Next.js 15 / React 19, ~24 routes. `npm install` + `npm run build` **succeed** — after 3 real fixes (below). Only 1 TypeScript error existed in the entire app. |

**Dashboard fixes to make `npm run build` pass** (all committed):
1. Nested-quote JS syntax error in `app/methodology/page.tsx` (`"What "publishes…" means"`) — broke the build outright. Switched outer quotes to single.
2. **Tailwind v4/v3 mismatch**: `package.json` pinned `tailwindcss@^4.0.0`, but the PostCSS config, `tailwind.config.ts`, and `globals.css` (`@tailwind base;`) are all v3. The pin was the lone outlier → pinned to `^3.4.17`.
3. One TypeScript type error in `IndicatorTile.tsx` (the `href ? Link : "div"` union-spread). Refactored to an explicit `href ? <Link> : <div>` branch.

---

## Design subsystem → implementation status

Mapping the v2.0 master-doc / CONOPS rev C architecture to what exists in code.

| Subsystem (design) | Status | Reality |
|---|---|---|
| Data Ingestion (SSDD-001) | **partial** | 11 upstream adapters built + mocked-tested; OECD/ECB/IMF/WB/Comtrade designed-not-built; no live ingest run. |
| Vintage Store (§7) | **partial** | SQLite real; Postgres/TimescaleDB schema designed, not implemented; never loaded with real Tier-V data. |
| Data Curation & Feature (SSDD-002) | **stub** | No package. Frequency harmonization / seasonal adj / trade-weights unbuilt. |
| L1 — US semi-structural core (SSDD-003) | **stub** | No package. Deferred per design (satellite, not IOC critical path). |
| L2 — Bayesian GVAR / R BGVAR (SSDD-004) | **stub** | No package, no R process-adapter. |
| L3 — Workhorse (SSDD-005) | **partial** | DFM variant only (opengem-l3-dfm). ML-residual + large-BVAR + **BMA combiner (SSDD-005a) unbuilt**. |
| Scenario (SSDD-006) | **partial** | Library + invocation real; L1+L2 propagation not connected. |
| Backtest & Publication (SSDD-007) | **stub** | No package. **Therefore the 17-cell V&V matrix cannot be evaluated yet.** |
| Situation (SSDD-008, new) | **partial** | recession-probability real; GPR-nowcast endpoint deferred (skill-probe gate). |
| Public REST API | **stub→drift** | Design says Spring Boot (Java 21); reality is a FastAPI `main.py` stub. Architectural drift with no ADR. |
| MCP Server | **broken stub** | Does not import (see above). |
| Orchestration (Dagster) | **stub** | No Dagster code/config. |
| Narrative / EPISTEMIC contract | **real** | Contract is live code, tested. |
| V&V matrix (17 cells) | **design-only** | Frozen in docs; no test harness exists. |

---

## What I changed to reach green (the fixes — full disclosure)

These were **real cross-package contract defects**, not cosmetic. All are
committed individually; details in git log.

1. **`Variable` enum was missing growth targets.** `DensityForecast.variable`
   is typed `Variable`, but l3-dfm forecasts `gdp_yoy`/`cpi_yoy` — codes the
   canonical enum didn't define. Added `GDP_YOY` / `CPI_YOY` (growth is a
   first-class forecast target; the whole V&V matrix is about growth rates).
2. **l3-dfm used an invented ISO-3 country contract.** `DFMConfig` required
   `"USA"` and *rejected* `"US"`, but `DensityForecast.country` is the canonical
   ISO-2 `Country` enum — so l3-dfm literally could not build a valid record.
   Conformed l3-dfm to ISO-2.
3. **Time-dependent integration test.** `test_vertical_slice` relied on
   `date.today()` for vintage stamping and broke once the calendar passed its
   hard-coded as-of date. The vintage store was correct; pinned the test's
   `vintage_at` deterministically.
4. **Bootstrap.** No package had ever been installed (hence 33 collection
   errors). Added uv workspace excludes for non-Python members, missing
   `[tool.uv.sources]`, a `dev` group, committed `uv.lock`.
5. **Lint.** Shipped code was never linted (1754 ruff errors repo-wide, but
   ~1600 were in `research-300/` scratch). Scoped ruff to shipped code; fixed
   140 → 0 in `packages/` + `tests/`.

**No source *logic* was broken** — the failures were a missing bootstrap plus
two cross-package vocabulary mismatches. The agent-built core is substantially
real.

---

## Latent issues (not breakage today, but real risk)

1. **Country code split: ISO-2 vs ISO-3.** Forecasts/types use ISO-2 (`US`);
   event-data (polecat) and datasette snapshots store ISO-3 (`USA`) in
   free-form metadata. They don't collide now (metadata is untyped) but **any
   future join of event data to forecasts by country will mismatch.** Needs a
   normalization decision before SSDD-002.
2. **Spring Boot → FastAPI drift** with no ADR. The physical-deployment design
   (`og-app-01` = "Spring API") and the code disagree.
3. **MCP broken** (above) — the stated v0.5 monetization lever does not run.
4. **No live-data path proven.** Every adapter is mocked; upstream schema/auth/
   rate-limit reality is undiscovered until a real pull is attempted.
5. **PostgresVintageStore unimplemented** — production storage path is SQLite-only.

---

## Governance: research-300 vs LOOP_PLAN v2 (the two-track fracture)

- The **design track** (`LOOP_PLAN-v2.md`) is a 27-iteration *document
  decomposition* plan. Iter 00 done; **Iter 02–27 all unchecked.** Its
  pre-condition (program-owner sign-off on R99 + CONOPS rev C + master-doc v2.0)
  was never recorded — no `SIGNOFF.md`, no tag.
- The **build track** (`research-300/`, 300 loops, completed 2026-06-06)
  produced the 23 packages — i.e. it **overtook the design track and built
  implementation before the design decomposition or sign-off happened.**
- The two were never reconciled. The packages implement *some* of the v2.0
  architecture (adapters, L3-DFM, recession-prob, narrative, scenarios) and
  skip the rest (L1, L2, backtest, BMA, orchestration).

This audit + the Goal-A baseline commit + `SIGNOFF.md` close that gap: the
build is now captured in git, verified green, and the rebaseline decision is
recorded.

---

*Generated by Goal A. Reproduce any claim: `uv sync --all-packages && uv run ruff check . && uv run pytest`.*
