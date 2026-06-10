# OPENGEM — Open Geopolitical-Economic Modeling

[![CI](https://github.com/edgardomunoznajar/opengem/actions/workflows/ci.yml/badge.svg)](https://github.com/edgardomunoznajar/opengem/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

**Status**: Block I — v2.0 baseline accepted (see [SIGNOFF.md](SIGNOFF.md)). **23 Python packages, 267 tests passing, ruff-clean, CI green.** First **real, scored** US forecast is live: the L3 DFM beats AR(1) and random-walk on GDP-1Q by CRPS on real 1960–2026 data ([docs/first-us-forecast.json](docs/first-us-forecast.json)). For the honest real-vs-stub breakdown, read **[STATE-OF-REALITY.md](STATE-OF-REALITY.md)** — not the per-package counts below, which are approximate.

## Public forecast track record

This project's product is an **accountable, ex-ante forecast record** — dated
density forecasts committed publicly *before* the official data they predict
is released, scored against named baselines, with misses kept up forever.
The record and its fixed rules live in [`forecasts/`](forecasts/README.md).

Current open forecasts (published 2026-06-06):

| Target | Period | p50 | [p10, p90] | Resolves |
|---|---|---|---|---|
| US GDP yoy | 2026Q2 | **2.67%** | [0.87, 4.47] | ~2026-07-30 |
| US CPI yoy | 2026Q2 | **2.74%** | [1.80, 3.69] | ~2026-07-14 |

At publication, the model beat both baselines on the headline backtest cell
(GDP-1Q mean CRPS: DFM 1.380 < AR(1) 1.553 < RW 1.717; 24 rolling origins on
real 1960–2026 data), with an honest mix on the other cells — details in
[`forecasts/README.md`](forecasts/README.md).

## What this is

An open-source, model-grounded, reproducibly-tracked **scenario engine** for
geopolitical-economic analysis. The headline product is a daily digest that
gets pasted into ChatGPT for analyst-grade prose — producing video-ready
content for an international-politics YouTuber whose competitive baseline is
"ChatGPT and nothing else." The longer arc is an open alternative to Stratfor /
NiGEM / Oxford GEM, validated through that one alpha user before going broader.

## Architectural imperative

Every package is **independently publishable**. Clean contracts at boundaries
(`opengem-types` is the shared vocabulary). Each package has its own
`pyproject.toml`, README, tests, can be lifted out and PyPI'd without churn.

## Package roster

### Foundation
- **opengem-types** ✅ — canonical typed dataclasses (Observation, VintageSnapshot, ScenarioSpec, RunProvenance, …) — 28 tests
- **opengem-vintage** ✅ — vintage-correct storage primitives (TimescaleDB + SQLite + in-memory) — 6 tests
- **opengem-data-base** ✅ — Adapter ABC + retry/backoff + error taxonomy — 13 tests

### US upstream-agency adapters (FRED-substitution per ADR-010)
- **opengem-data-bea** ✅ — Bureau of Economic Analysis (NIPA) — 15 tests
- **opengem-data-bls** ✅ — Bureau of Labor Statistics (CPI, payrolls, unemployment) — 12 tests
- **opengem-data-frb** ✅ — Federal Reserve Board (H.15, G.17, H.6) — 9 tests
- **opengem-data-treasury** ✅ — Treasury FiscalData — 6 tests
- **opengem-data-census** ✅ — Census M3 / MRTS — 9 tests

### Multi-country adapters
- **opengem-data-ordra** ✅ — OECD ORDRA SDMX (~130-series catalog auto-generated) — 15 tests
- **opengem-data-bis** ✅ — BIS CBPOL policy rates (45 central banks) — 9 tests

### Information surface
- **opengem-data-gscpi** ✅ — NY Fed Global Supply Chain Pressure Index — 5 tests
- **opengem-data-gpr** ✅ — Caldara-Iacoviello Geopolitical Risk Index (global + 45 country indexes) — 5 tests

### Scenario + Situation engine
- **opengem-scenarios** ✅ — Canonical library (10 packs) + invocation + JSON serialization — 15 tests
- **opengem-recession-prob** ✅ — Bauer-Mertens term-spread probit (with IRLS fitter) — 10 tests
- **opengem-event-detector** ✅ — Market + news event detectors + rule engine → pack triggers — 9 tests

### Friend-facing output
- **opengem-digest** ✅ — Daily JSON + markdown digest renderer — 6 tests
- **opengem-narrative** ✅ — ChatGPT system prompts + JSON contract for analyst-grade prose — 6 tests

### Integration tests
- **tests/integration/** ✅ — vertical slice + Stratfor-grade end-to-end demo — 5 tests

**Total (verified 2026-06-06): 21 Python packages, 245 tests, all green** (+ l3-dfm, datasette, mcp [stub], data-polecat, and the dashboard/api surfaces not listed above). Per-package counts in this section are approximate and predate the last build — see [STATE-OF-REALITY.md](STATE-OF-REALITY.md) for measured values.**

## The friend's morning workflow

1. Overnight: data adapters refresh, event detector scans news + markets, rule engine fires scenario packs.
2. Morning: friend opens `docs/example-digest.md` (or a similar live file).
3. Skim situation indicators, events, triggered scenarios.
4. Pick a scenario, copy the JSON block.
5. Paste into ChatGPT with the OPENGEM system prompt from `opengem-narrative`.
6. Get a 3-paragraph video segment grounded in real model output.

See `docs/example-digest.md` for a rendered example with 4 scenarios triggered
on a morning of high geopolitical tension.

## Architecture

```
                 ┌──────────────── Data adapters ─────────────────┐
                 │ BEA · BLS · FRB · Treasury · Census · ORDRA · │
                 │ BIS · GSCPI · GPR · (ECB · IMF · WB pending)  │
                 └─────────────────────┬─────────────────────────┘
                                       ▼
                              opengem-vintage
                       (TimescaleDB / SQLite store)
                                       │
        ┌──────────────────────────────┴───────────────────────────────┐
        ▼                                                              ▼
   opengem-recession-prob                                opengem-event-detector
   (Bauer-Mertens probit)                          (market thresholds + news rules)
        │                                                              │
        │                                                              ▼
        │                                                opengem-scenarios
        │                                       (10 canonical packs + library)
        │                                                              │
        │                                                              ▼
        │                                                  RuleEngine triggers
        │                                                ScenarioInvocations
        ▼                                                              ▼
                  ┌──────────────── opengem-digest ───────────────┐
                  │  JSON + markdown daily digest                 │
                  └──────────────────────┬────────────────────────┘
                                         ▼
                              opengem-narrative
                  (ChatGPT system prompt + NarrativeRequest JSON)
                                         ▼
                                friend's ChatGPT
                                         ▼
                            analyst-grade YouTube segment
```

## Running the test suite

```bash
uv sync --all-packages   # install all workspace members editable + dev tools
uv run ruff check .      # lint
uv run pytest            # 245 tests, incl. the statsmodels DFM integration fit
```

## Design dossier

The pre-PDR research round produced 28 memos + CONOPS rev C + master design doc v2.0 + LOOP_PLAN v2 — all in `docs/`. As of 2026-06-06 the rebaseline is **accepted** ([SIGNOFF.md](SIGNOFF.md)): the rev C CONOPS, master-doc v2.0, and LOOP_PLAN v2 are promoted to baseline (rev B / v1 remain in git history). Start with [MORNING-BRIEFING.md](MORNING-BRIEFING.md).

## License

Apache-2.0 (code) / CC-BY-4.0 (docs, data, model cards).
