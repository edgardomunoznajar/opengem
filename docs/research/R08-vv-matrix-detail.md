# R08 — V&V Matrix: Detailed Specification

| Field | Value |
|---|---|
| Document ID | OG1-RES-008 |
| Revision | A (2026-05-24) |
| Date | 2026-05-24 |
| Status | **Detailed specification of the V&V matrix introduced in R01 §4.** |
| Authority | R01 §4, master-doc v2.0 §8.3 |

---

## 1. Why this exists

R01 §4 proposed a **matrix** replacing the single "beat AR(1) on 75%" gate from CONOPS rev B §8.3. This memo specifies the matrix completely: cells, metrics, benchmarks, statistical tests, vintage discipline, country-set scoping, and pass/fail thresholds. It's the bar OPENGEM must meet at IOC, v0.4, and FOC.

## 2. Matrix structure

Each cell is a tuple:

```
Cell = (Variable, Horizon, Country-Set, Metric, Benchmark, Threshold)
```

OPENGEM passes a cell when, evaluated on **vintage-correct out-of-sample data**, the metric clears the threshold against the benchmark on the country-set.

### 2.1 Variables

- **GDP-real** (annualized quarterly growth)
- **CPI-headline** (12-month inflation)
- **Unemployment rate** (level)
- **Policy rate** (level)
- **Recession indicator** (binary 12m-ahead)

### 2.2 Horizons

- **1Q** (one quarter ahead, ≈ 3 months)
- **4Q** (one year ahead)
- **8Q** (two years ahead)
- **20Q** (five years ahead)
- **12m** (specifically for recession-probability)

### 2.3 Country-sets

- **Tier-V Core** (~26 confirmed countries from R07 §3.1)
- **Tier-V Extended** (Core + post-1995 OECD entrants where ORDRA coverage exists)
- **Tier-V All** (Core + Extended + BRICS+ where coverage holds)
- **Tier-T** (tracked-only; **not part of V&V matrix** — published in dashboard with disclaimer only)

### 2.4 Metrics

- **CRPS** (Continuous Ranked Probability Score) — density-aware scoring; lower is better. Primary metric for density forecasts.
- **RMSE / MAE** — point-forecast accuracy. Secondary.
- **Log score** — density-aware; complements CRPS.
- **Diebold-Mariano (DM)** — pairwise predictive-accuracy test; we report p-values.
- **MCS membership** — Model Confidence Set inclusion at 90% confidence.
- **PIT KS-test** — Kolmogorov-Smirnov test for PIT uniformity at 5% level. Calibration of density.
- **AUC** — area under ROC curve for binary recession indicator.

## 3. The matrix (Block I, IOC bar)

| # | Variable | Horizon | Country-Set | Metric | Benchmark | Threshold (IOC) |
|---|---|---|---|---|---|---|
| C-01 | GDP-real | 1Q | Tier-V Core | CRPS | AR(1), RW | Beat both on ≥80% of countries |
| C-02 | GDP-real | 1Q | Tier-V Core | PIT KS@5% | own density | Pass on ≥80% of countries |
| C-03 | GDP-real | 4Q | Tier-V Core | DM p-value | WEO same-vintage | Not worse (p>0.05) on ≥50% of countries |
| C-04 | GDP-real | 4Q | Tier-V Core | DM p-value | OECD EO same-vintage | Not worse on ≥50% of countries |
| C-05 | GDP-real | 4Q | Tier-V Core | PIT KS@5% | own density | Pass on ≥70% of countries |
| C-06 | GDP-real | 8Q | Tier-V Core | DM p-value | WEO same-vintage | Not worse on ≥40% of countries |
| C-07 | GDP-real | 8Q | Tier-V Core | PIT KS@5% | own density | Pass on ≥60% of countries |
| C-08 | CPI-headline | 1Q | Tier-V Core | CRPS | AR(1) and last-12m-avg | Beat both on ≥65% of countries |
| C-09 | CPI-headline | 1Q | Tier-V Core | PIT KS@5% | own density | Pass on ≥60% of countries |
| C-10 | CPI-headline | 4Q | Tier-V Core | DM p-value | WEO same-vintage | Not worse on ≥40% of countries |
| C-11 | CPI-headline | 4Q | Tier-V Core | DM p-value | OECD EO same-vintage | Not worse on ≥40% of countries |
| C-12 | CPI-headline | 4Q | Tier-V Core | PIT KS@5% | own density | Pass on ≥50% of countries |
| C-13 | Unemployment | 1Q | Tier-V Core | CRPS | AR(1) | Beat on ≥75% of countries |
| C-14 | Unemployment | 4Q | Tier-V Core | DM p-value | WEO same-vintage | Not worse on ≥50% of countries |
| C-15 | Unemployment | 4Q | Tier-V Core | PIT KS@5% | own density | Pass on ≥60% of countries |
| C-16 | Policy rate | 1Q–4Q | Tier-V Core | DM p-value | Forward curve / OIS-implied | Not worse on ≥75% of countries |
| C-17 | Recession indicator | 12m | Tier-V Core | AUC | Bauer-Mertens replication | AUC ≥ 0.85 on US; not worse by 0.05 on others |

### 3.1 FOC bar

FOC requires the IOC matrix **PLUS**:

- All thresholds raised by 5 percentage points (e.g., C-01 from 80% to 85%).
- Country-set widens from Tier-V Core to **Tier-V Core + Extended** (~35 countries).
- MCS membership: OPENGEM models in MCS at 90% on ≥50% of {country, variable, horizon} cells.
- 20Q horizon cells added for GDP and CPI (against AR(1) — at 5y, no judgmental benchmark applies cleanly).

## 4. Statistical methodology

### 4.1 Vintage discipline

- All evaluations use **the data vintage that was available at the time the forecast was made**.
- WEO and OECD EO benchmarks: same-vintage. We compare OPENGEM's October-2024-issued 4Q-ahead forecast to WEO October 2024's same-horizon forecast.
- Forward curve: use closing rates on the OPENGEM forecast date.
- No revised-final data ever used for either OPENGEM or benchmark forecasts in V&V.

### 4.2 Out-of-sample window

- Minimum **8 quarters** of OOS for DM tests (statistical power requirement).
- IOC evaluation window: rolling origin from 2014-Q1 to most-recent-vintage minus 2 years.
- FOC evaluation window: rolling origin from 2010-Q1 to most-recent-vintage minus 2 years.

### 4.3 Diebold-Mariano variants

- Use **Harvey-Leybourne-Newbold small-sample correction** of DM (HLN-DM).
- Two-sided test at α=0.05.

### 4.4 PIT testing

- Kolmogorov-Smirnov at α=0.05 against U[0,1].
- Anderson-Darling as secondary check (more sensitive to tails).
- Hong-Li test for *independence* of PITs (catches serial-correlation density-mis-specification).
- A cell "passes" PIT if KS passes; AD and Hong-Li are reported but not gate.

### 4.5 Model Confidence Set

- Hansen-Lunde-Nason MCS at 90% confidence.
- Stationary bootstrap with block length tuned per country.
- Report membership cell by cell.

## 5. Reproducibility requirements

For every cell in the matrix:

- **Computation code** is open and version-pinned with `code_sha`.
- **Benchmark data** is archived locally per source (WEO, OECD EO releases).
- **Test outcomes** are stored in a `vv_results` table per (cell, evaluation_window, run_id).
- **Reliability diagrams, PIT histograms, DM forest plots** are auto-generated per cell per release.

## 6. Failure modes and re-baseline triggers

| Trigger | Action |
|---|---|
| ≥3 cells fail at IOC | Block IOC sign-off; iterate L3 architecture |
| 1–2 cells fail at IOC | Document as known limitation; proceed with explicit acknowledgement in model cards |
| ≥5 cells fail at FOC | Sunset the v1.0 framing; re-baseline as "verifiable infrastructure" not "operational parity" |

## 7. Reporting cadence

- **Daily**: nowcast cells refresh.
- **Quarterly**: full V&V matrix re-evaluated after new vintages land.
- **Weekly**: leaderboard refresh per FR-PUB-001.
- **Per release**: model cards include the latest V&V table per cell.

## 8. New tables for V&V tracking

```sql
CREATE TABLE vv_results (
  cell_id        TEXT NOT NULL,           -- e.g., "C-01"
  evaluation_run TEXT NOT NULL,           -- run_id
  variable       TEXT NOT NULL,
  horizon        TEXT NOT NULL,
  country_set    TEXT NOT NULL,
  metric         TEXT NOT NULL,
  benchmark      TEXT NOT NULL,
  threshold      JSONB NOT NULL,
  observed_value JSONB NOT NULL,
  passed         BOOLEAN NOT NULL,
  evaluated_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  PRIMARY KEY (cell_id, evaluation_run)
);
```

## 9. Open probes

1. **WEO same-vintage availability** — confirm IMF makes full WEO release PDFs/Excels downloadable historically. Verify at SRR.
2. **OECD EO same-vintage availability** — same.
3. **Forward-curve historical archive** — FRB H.15 has it for US; per-country availability via BIS or central bank. Adapter pulls verified per Tier-V country.
4. **Country-specific recession dating** for non-US — OECD CLI peak-to-trough proxy validated at SRR.

## 10. Bottom line

V&V is no longer a single number. It's **17 cells at IOC, ~25 at FOC**, each with its own threshold and benchmark. OPENGEM is honestly evaluated where the literature says evaluation is meaningful, and is not let off the hook by an easy aggregate metric.

---

*End of R08 Rev A.*
