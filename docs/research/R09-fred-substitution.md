# R09 — FRED-Substitution Map (US data layer)

| Field | Value |
|---|---|
| Document ID | OG1-RES-009 |
| Revision | A (2026-05-24) |
| Date | 2026-05-24 |
| Status | **Implementation-ready specification for replacing FRED dependencies with upstream US agencies.** |
| Authority | R05 §3, ADR-010 |

---

## 1. Why this exists

R05 found that **FRED's 2024 ToS prohibits caching, archiving, and ML training** on FRED Content. ALFRED (St. Louis Fed) inherits the same restrictions. OPENGEM's design requires persistent, archived, vintage-correct US macro data. Therefore the US data path cannot route through FRED.

This memo enumerates the **upstream US agency replacements** for every category of US series OPENGEM needs.

## 2. The substitution map

### 2.1 National Income and Product Accounts (NIPA) — BEA

**Source**: Bureau of Economic Analysis (BEA).
**API**: REST, JSON/XML, API key required (free).
**Endpoint**: `https://apps.bea.gov/api/data`.
**DataSetName**: `NIPA` (and `NIUnderlyingDetail`).
**Auth**: 36-character key from [BEA API signup](https://apps.bea.gov/api/signup/).
**Frequency**: Quarterly and annual.
**Vintage handling**: BEA publishes "frozen" vintage values per release. OPENGEM ingests on release dates and archives per-vintage.
**Documentation**: [BEA API User Guide (April 2026)](https://apps.bea.gov/api/_pdf/bea_web_service_api_user_guide.pdf).

**Series covered**:
- Real GDP (annualized chained dollars)
- Nominal GDP
- GDP price deflator
- GDP components (C, I, G, NX) and subcomponents
- GDI (gross domestic income)
- Personal income, disposable income
- Corporate profits

**Python client**: `beaapi` ([us-bea/beaapi on GitHub](https://github.com/us-bea/beaapi)).

### 2.2 Prices and Labor — BLS

**Source**: Bureau of Labor Statistics (BLS).
**API**: REST, JSON, v2 supports up to 50 series/request and 20 years/request with free registered key.
**Endpoint**: `https://api.bls.gov/publicAPI/v2/timeseries/data`.
**Auth**: Free key from [BLS Developers page](https://www.bls.gov/developers/home.htm).
**Rate limit**: Daily query limit; v2 unlocks higher tier.

**Series covered**:
- CPI (CUUR series): headline, core, regional, item-specific
- PPI (WPU series)
- Unemployment rate (LNS series, CPS-based)
- Nonfarm payroll employment (CES survey, monthly)
- Average hourly earnings, hours worked
- JOLTS (job openings)
- Productivity

**Documentation**: [BLS API v2 signatures](https://www.bls.gov/developers/api_signature_v2.htm); [Python access guide](https://www.bls.gov/developers/api_python.htm).

### 2.3 Monetary and rates — Federal Reserve Board

**Source**: Board of Governors of the Federal Reserve System.
**API**: DataDownload Program (DDP) — XML/CSV bulk downloads + REST query API.
**Endpoint**: `https://www.federalreserve.gov/datadownload/Output.aspx` (with package codes).
**Auth**: None (some endpoints require token; most are public).
**Rate limit**: Effectively bulk.

**Series covered**:
- H.15 — Selected Interest Rates (Treasury yields all maturities, federal funds, OIS rates, prime, swap rates)
- H.6 — Money Stock (M1, M2)
- H.8 — Banking Assets and Liabilities
- G.17 — Industrial Production and Capacity Utilization
- Z.1 — Financial Accounts of the United States
- Z.7 — Financial Stability Reports data

**Documentation**: [Federal Reserve Data Download Programs](https://www.federalreserve.gov/datadownload/).

### 2.4 Treasury and fiscal — US Treasury (FiscalData)

**Source**: U.S. Department of the Treasury.
**API**: REST, JSON/CSV.
**Endpoint**: `https://api.fiscaldata.treasury.gov/services/api/fiscal_service/`.
**Auth**: None.
**Rate limit**: Generous; no key required.

**Series covered**:
- Daily Treasury yield curve rates (alternative to H.15 if needed for redundancy)
- Monthly Treasury statement (federal receipts, outlays, deficit)
- Debt to the penny
- TIC capital flow data (via separate endpoints)

**Documentation**: [FiscalData API documentation](https://fiscaldata.treasury.gov/api-documentation/).

### 2.5 Trade and Census — US Census Bureau

**Source**: U.S. Census Bureau.
**API**: REST, JSON.
**Endpoint**: `https://api.census.gov/data/`.
**Auth**: Optional key for higher rate limit.

**Series covered**:
- M3 — Manufacturers' Shipments, Inventories, and Orders (inventory-to-sales ratio, durable goods orders)
- International Trade in Goods and Services (FT900) — alternative to BEA's trade module
- Retail Sales (Monthly Retail Trade Survey)
- Housing Starts (joint with HUD)

**Documentation**: [Census APIs](https://www.census.gov/data/developers.html).

### 2.6 Senior Loan Officer and other Fed surveys

Federal Reserve Board's H.7 and senior-loan-officer surveys available via the same DDP.

## 3. Series-level substitution table (the operational mapping)

This is the table OPENGEM's ingestion code will be built from. Every FRED series identifier OPENGEM was going to use maps to one upstream call.

| FRED series ID (NOT used) | Upstream source | Endpoint / DataSet | Frequency | Notes |
|---|---|---|---|---|
| GDPC1 (Real GDP) | BEA NIPA | Table T10101 line 1 | Q | Annualized chained dollars |
| GDPDEF | BEA NIPA | Table T10104 | Q | GDP deflator |
| GDP | BEA NIPA | T10105 line 1 | Q | Nominal GDP |
| PCEPI | BEA NIPA | T20804 | M/Q | PCE price index |
| CPIAUCSL | BLS CPI | CUUR0000SA0 (NSA) / CUSR0000SA0 (SA) | M | Headline CPI |
| CPILFESL | BLS CPI | CUSR0000SA0L1E | M | Core CPI |
| UNRATE | BLS LNS | LNS14000000 | M | Unemployment rate, CPS |
| PAYEMS | BLS CES | CES0000000001 | M | Total nonfarm payrolls |
| INDPRO | FRB Board G.17 | INDPRO from DDP | M | Industrial production |
| TCU | FRB Board G.17 | CAPUTL.B50001.S | M | Capacity utilization |
| FEDFUNDS | FRB Board H.15 | FEDFUNDS / DFEDTAR{U,L} | D/M | Fed funds target |
| GS10 | FRB Board H.15 | DGS10 | D | 10-year Treasury yield |
| GS2 | FRB Board H.15 | DGS2 | D | 2-year Treasury yield |
| GS3M | FRB Board H.15 | DGS3MO | D | 3-month Treasury bill |
| M2SL | FRB Board H.6 | M2 | M | M2 money stock |
| HOUST | Census/HUD | New Residential Construction | M | Housing starts |
| RETAIL (MRTSSM44000) | Census MRTS | MRTS | M | Retail sales |
| ISRATIO | Census M3 | M3-derived | M | Inventory-to-sales |

(Full list of ~50 series to be detailed in SSDD-001 v2.)

## 4. Ingestion architecture implication

The ingestion subsystem is **a polyglot adapter cohort**, not a single FRED-API client:

```
Source                  Adapter            Vintage handling
─────────────────────────────────────────────────────────────────
BEA (NIPA)              beaapi (Python)    Snapshot per NIPA release
BLS (CPI/UNRATE/...)    requests +         Snapshot per release calendar
                         API key
FRB H.15 / G.17 / H.6   DDP downloader     Snapshot per release calendar
Treasury (FiscalData)   requests           Snapshot per business day
Census (M3/MRTS)        requests +         Snapshot per release calendar
                         API key
─────────────────────────────────────────────────────────────────
All write to: opengem.raw_observations
              opengem.vintage_snapshots
```

**Implication**: Five adapter modules at IOC, each with its own retry/backoff and release-calendar awareness. Heavier than the FRED-as-single-source design, but the upside is **persistent, ToS-compliant, vintage-correct US data** that nothing in 2024+ FRED ToS forbids.

## 5. Release calendars

The adapter cohort must align with each agency's release schedule. Indicative cadence:

| Source | Release rhythm |
|---|---|
| BEA NIPA | ~Last Thursday of month following quarter end (advance), revised at 2-month and 3-month marks |
| BLS CPI | ~Mid-month for prior month |
| BLS CES (payrolls) | First Friday of each month |
| FRB H.15 | Daily (rates) |
| FRB G.17 | ~Mid-month for prior month |
| FRB H.6 (M2) | Weekly |
| Treasury FiscalData | Daily for most, monthly for MTS |
| Census M3 / MRTS | Mid-month |

OPENGEM's Dagster orchestrator schedules each adapter at the expected release time + a small jitter; failure-mode reverts to next-day re-check.

## 6. Costs

All upstream agency APIs are free. API keys are free (where required). No premium tiers needed.

**Engineering cost** is the only real cost: ~1–2 weeks of adapter development for the five-agency cohort, plus integration tests with golden fixtures.

## 7. Risk and mitigations

| Risk | Mitigation |
|---|---|
| Per-agency schema drift | Schema validation gate on each adapter; pinned-snapshot fallback |
| Agency API outage | Each adapter independent; degrade per-agency, not whole-US |
| API key rotation | Stored in vault; per-agency key, not shared |
| Release-calendar slip | Adapter polls until success or escalation after N tries |

## 8. ToS posture — explicit

OPENGEM, under this design:

- **Does not** call FRED API for persistent series ingestion.
- **May** call FRED for series-ID discovery and human-readable browsing (i.e., users on the OPENGEM team navigating FRED to identify which BEA / BLS / FRB series corresponds to an observation of interest). This is read-only and ephemeral; no caching.
- **Does not** call ALFRED for archived vintages. Philadelphia Fed RTDSM is the US vintage source.
- Documents this posture in `POL-01` (rev C CONOPS §5.2).

## 9. Bottom line

The FRED-substitution map is **operationally fully specified**. OPENGEM Block I implements five upstream-agency adapters, all free, all permissive, all aligned with vintage discipline. The 1–2 weeks of extra engineering at IOC buys ToS-compliance, source-of-truth alignment, and removes a single-vendor dependency from the US data path forever.

---

*End of R09 Rev A.*
