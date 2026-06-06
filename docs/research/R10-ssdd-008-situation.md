# R10 — SSDD-008 Situation Subsystem Design

| Field | Value |
|---|---|
| Document ID | OG1-RES-010 |
| Revision | A (preliminary design 2026-05-24) |
| Date | 2026-05-24 |
| Status | **Preliminary design — feeds the LOOP_PLAN-v2 Iter 19a SSDD-008 realization.** |
| Authority | R06 §7, master-doc v2.0 §5.8 |

---

## 1. Purpose

The **Situation Subsystem** publishes information-surface forecasts that sit alongside (not inside) the macro forecast core. Per R06, two endpoints are in scope:

1. **Term-Spread Recession Probability** (`/v1/recession-probability`) — Bauer-Mertens-style 12-month-ahead recession indicator per Tier-V country.
2. **GPR Nowcast** (`/v1/gpr-nowcast`) — daily forecast of Caldara-Iacoviello Geopolitical Risk Index per country (44 countries), **build deferred** pending forecast-skill probe.

The subsystem is intentionally **lightweight**: each endpoint wraps a published, well-cited, transparent model rather than reinventing it. Its job is *operational availability* and *integration with the OPENGEM API/MCP surface*, not method development.

## 2. Inputs

| Endpoint | Required inputs | Source |
|---|---|---|
| Recession Probability | 10y and 3m sovereign yields per country | FRB H.15 (US); ECB SDW (EA); BoE (UK); national central banks via BIS or own portals; per-country adapter |
| Recession Probability (validation) | NBER-style recession dates per country | Per-country dating committees or OECD CLI-based proxy |
| GPR Nowcast | Caldara-Iacoviello historical GPR series + GDELT GKG country tones | matteoiacoviello.com + GDELT 2.0 |

## 3. Components

### 3.1 Term-Spread Engine

```
┌──────────────────────────────────────────────────────────┐
│  Term-Spread Engine                                       │
│                                                           │
│  ┌────────────┐  ┌────────────┐  ┌─────────────────────┐ │
│  │ Yield      │  │ Spread     │  │ Probit / Bauer-     │ │
│  │ Ingester   │─▶│ Computer   │─▶│ Mertens Estimator   │ │
│  │ (per cntry)│  │ (10y - 3m) │  │ (12m horizon)       │ │
│  └────────────┘  └────────────┘  └─────────┬───────────┘ │
│                                            │             │
│                                            ▼             │
│                                  ┌──────────────────┐    │
│                                  │ Recession-Prob   │    │
│                                  │ Hypertable +     │    │
│                                  │ Reliability Diag │    │
│                                  └──────────────────┘    │
└──────────────────────────────────────────────────────────┘
```

**Estimator**: Per-country probit regression of recession indicator on lagged term spread. Bauer-Mertens (2018) replication code adapted per country. Country-specific recession definition: NBER for US; OECD CLI peak-to-trough for others (or domestic dating committee where it exists).

**Update cadence**: Daily (recompute probability using current yield curve).

**Storage**: Hypertable `recession_prob` partitioned by country.

**API endpoint**:
```
GET /v1/recession-probability?country=US&as_of=2026-05-24
  → { "country": "US", "probability_12m": 0.18, "as_of": "2026-05-24",
      "model": "bauer_mertens_replication_v1.2", "term_spread_bp": 42,
      "country_specific_threshold_auc": 0.89 }
```

**MCP tool**: `recession_probability(country, as_of=None) → dict`.

**Model card**: One per country variant; includes AUC vs. recession history, calibration plot, last validation date.

### 3.2 GPR Nowcast Engine (deferred build)

```
┌────────────────────────────────────────────────────────────────┐
│  GPR Nowcast Engine (deferred build)                            │
│                                                                 │
│  ┌──────────────┐  ┌────────────┐  ┌──────────────────────┐    │
│  │ GDELT GKG    │  │ Per-country│  │ Lasso / GBM regressor│    │
│  │ daily tone   │─▶│ aggregator │─▶│ predicting GPR(t+1..t+90)│ │
│  │              │  │            │  └──────────┬───────────┘    │
│  └──────────────┘  └────────────┘             │                │
│                                                ▼                │
│  ┌──────────────┐                  ┌──────────────────┐         │
│  │ C-I GPR      │─── targets ────▶ │ gpr_nowcast      │         │
│  │ historical   │                  │ hypertable +     │         │
│  └──────────────┘                  │ skill report     │         │
│                                    └──────────────────┘         │
└────────────────────────────────────────────────────────────────┘
```

**Pre-build decision gate** (R06 §10):
- Run a probe over 5 years of GDELT GKG + historical GPR for 5 countries (US, UK, RU, IL, CN).
- Compute skill metric: nowcast RMSE vs. persistence (just predicting "GPR(t+1) = GPR(t)").
- **Build proceeds only if** the nowcast beats persistence by ≥10% RMSE in ≥3/5 probe countries.

If skill probe fails: defer indefinitely. The wrap on C-I's monthly index remains; no daily nowcast.

**API endpoint** (if built):
```
GET /v1/gpr-nowcast?country=US&horizon_days=30
  → { "country": "US", "horizon_days": 30, "gpr_nowcast": 87.2,
      "ci_p10": 62.0, "ci_p90": 121.5,
      "model": "gpr_nowcast_v0.1", "as_of": "2026-05-24" }
```

**MCP tool**: `gpr_nowcast(country, horizon_days)`.

## 4. Interactions with other subsystems

| Subsystem | How Situation interacts |
|---|---|
| Data Ingestion (SSDD-001) | Consumes yield curves and GDELT/GPR data; does not produce data itself except aggregated covariate panels |
| Curation (SSDD-002) | None direct |
| L1/L2/L3 model layers | None — Situation is independent of the forecast critical path |
| Forecast Service (SSDD-005 application) | Optional cross-link in API responses — a forecast response can include the country's current recession probability as context |
| Scenario Subsystem (SSDD-006) | Optional cross-link — recession-prob can be a "stress trigger" that auto-launches a canonical recession scenario via Scenario Subsystem |
| Backtest Subsystem (SSDD-007) | Independent V&V — Situation has its own backtest pipeline (rolling AUC for recession-prob, rolling RMSE for GPR nowcast) |
| Publication / Leaderboard | Recession-prob has its own leaderboard row per R01 §4 matrix; GPR nowcast has its own row if built |

## 5. State and storage

### 5.1 New tables

```sql
CREATE TABLE recession_prob (
  country     TEXT NOT NULL,
  as_of       DATE NOT NULL,
  prob_12m    NUMERIC(5,4) NOT NULL,
  term_spread_bp INTEGER,
  model_sha   TEXT NOT NULL,
  inputs_hash TEXT NOT NULL,
  PRIMARY KEY (country, as_of, model_sha)
);
SELECT create_hypertable('recession_prob', 'as_of');

CREATE TABLE gpr_nowcast (
  country     TEXT NOT NULL,
  as_of       DATE NOT NULL,
  horizon_days INTEGER NOT NULL,
  nowcast     NUMERIC,
  ci_p10      NUMERIC,
  ci_p90      NUMERIC,
  model_sha   TEXT NOT NULL,
  inputs_hash TEXT NOT NULL,
  PRIMARY KEY (country, as_of, horizon_days, model_sha)
);
SELECT create_hypertable('gpr_nowcast', 'as_of');
```

### 5.2 Retention

Forever for tagged releases; CI runs retained 90 days like other ephemeral artifacts.

## 6. V&V

Both endpoints are in the R01 §4 matrix:

| Endpoint | Bar |
|---|---|
| Recession-probability | AUC ≥ 0.85 vs. country-specific recession dates, ≥10 years OOS; not worse than 0.05 below Bauer-Mertens published model |
| GPR nowcast | Beat persistence by ≥10% RMSE on 30-day horizon, ≥3 years OOS, ≥3 of probe-set countries |

Both endpoints publish reliability diagrams (recession-prob) and PIT histograms (GPR nowcast if density is provided).

## 7. Failure modes

| Mode | Behavior |
|---|---|
| Yield-curve data outage in one country | Endpoint returns last-good with `data_completeness < 0.9` flag |
| Model-card validation fails | Endpoint serves but flags `under_review: true` |
| GDELT GKG outage | GPR nowcast endpoint returns 503 with retry-after |
| GPR target-history out of date | Nowcast still served; report `target_history_lag_months` |

## 8. Open probes

1. **GPR-nowcast skill probe** (gate to build the endpoint at all).
2. **Per-country recession-dating proxy** — for non-US countries without their own NBER-equivalent, what's the best free proxy? OECD CLI peak-to-trough is the candidate; verify it's defensible.
3. **Threshold calibration per country** for recession-probability — country-specific cutoffs that turn the probability into a binary call. Defer to model-card detail.

## 9. Bottom line

SSDD-008 Situation Subsystem is **two thin endpoints on top of two published, well-known indices**. Engineering cost is low. Forecast-power evidence is high (R06 §2 and §4). The subsystem adds visible product to OPENGEM beyond the macro core without expanding model maintenance burden materially.

---

*End of R10 Rev A.*
