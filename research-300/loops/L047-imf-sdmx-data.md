# L047 — IMF SDMX / IMF Data: the second-largest macro vending machine

**Loop**: 047 / 300
**Phase**: 1 — Open-source landscape survey (data sources)
**Date**: 2026-06-06
**Verdict**: **ADOPT-NOW (IFS + WEO + DOTS)**, ADOPT-BLOCK-II (BOP, COFER, FSI, FAS), CITE-ONLY (GFSR, FM, HPDD).

---

## One-line take

The IMF's data portal is the **only place** where you can pull a coherent, dimensionally-consistent panel of national-accounts, money/credit, fiscal, BOP, trade, and reserve-composition data across 190+ countries — but the 2024-2025 migration to SDMX 3.0 silently bricked every R / Python helper in the wild, and the adapter has to be written against the *new* API or it will rot inside a year.

## What it is

- **Portal**: `https://data.imf.org` (re-launched 2024-2025).
- **API base**: `https://api.imf.org/external/sdmx/3.0/` (SDMX 3.0; the legacy `dataservices.imf.org` SDMX 2.1 endpoint was deprecated late 2024 and broke in early 2025 — half the open-source IMF wrappers on PyPI/CRAN are now non-functional).
- **API style**: SDMX 3.0 REST. Default response is SDMX-ML (XML); `Accept: text/csv` or `Accept: application/json` flips formats.
- **Query grammar**: `/data/dataflow/{agency}/{dataflow}/{version}/{key}` — agency is `IMF.STA` or `IMF.RES`; key is dot-separated dimension values, `+` for OR, empty positions for wildcard.

## Datasets that matter (with cadence, license, fit)

| Dataset | Code | Frequency | Cadence | Coverage | OPENGEM fit |
|---|---|---|---|---|---|
| **World Economic Outlook** | `WEO` | Annual + 5y projections | April + October | 190 countries | **ADOPT-NOW** — the forecast benchmark we have to beat |
| **International Financial Statistics** | `IFS` | M / Q / A | Continuous | 190 countries | **ADOPT-NOW** — money, credit, FX, BOP, reserves |
| **Direction of Trade Statistics** | `DOT` | M / Q / A | Monthly w/ ~6w lag | 200 reporters × 200 partners | **ADOPT-NOW** — bilateral trade (see L052) |
| **Consumer Price Index** | `CPI` | Monthly | Monthly | 200 economies | **ADOPT-NOW** — multi-country inflation panel |
| **Balance of Payments** | `BOP` / `BOP_AGG` | Q (BOP), A (BOPSY) | Quarterly, BOPSY each Nov | 190 reporters | ADOPT-BLOCK-II |
| **Coordinated Direct Investment Survey** | `CDIS` | Annual | Q4 of year+1 | 110 reporters | CITE-ONLY |
| **Coordinated Portfolio Investment Survey** | `CPIS` | Semi-annual | Sept + March | 80 reporters | CITE-ONLY |
| **COFER (reserve currency composition)** | `COFER` | Quarterly | T+90d | Allocated + (post-2025Q3) full coverage | **ADOPT-NOW** — dollar dominance narrative anchor |
| **International Reserves & FX Liquidity** | `IRFCL` | Monthly | T+30d | 100+ economies | ADOPT-BLOCK-II |
| **Financial Access Survey** | `FAS` | Annual | Q3 | 180 economies | CITE-ONLY (financial inclusion; not macro-critical) |
| **Financial Soundness Indicators** | `FSI` | Quarterly | T+90d | 100 economies | ADOPT-BLOCK-II — capital adequacy, NPLs |
| **Government Finance Statistics** | `GFS` | Annual | Sept | 130 economies | ADOPT-BLOCK-II |
| **Fiscal Monitor (FM)** | `FM` | Semi-annual | April + Oct (with WEO) | 190 economies | CITE-ONLY |
| **Historical Public Debt Database** | `HPDD` | Annual | Irregular | 200 economies | CITE-ONLY |
| **Global Financial Stability Report data** | (no clean SDMX endpoint) | Semi-annual | April + Oct | Cross-country financial conditions | CITE-ONLY — the actual GFSR data is mostly PDF/CSV behind the publication; no SDMX flow |

## What's gated vs free

**Everything in the table is publicly accessible** — no token, no registration, no daily download quota documented. The SDMX 3.0 API is open. The Swagger explorer on `sdmxcentral.imf.org` sometimes asks for a beta-portal login, but that is for the *explorer UI*, not the underlying data endpoints — programmatic access without auth is fully supported.

Things that *are* gated (and therefore CITE-ONLY for OPENGEM):

- **WEO Country-staff projections (the country-by-country drafts before publication)** — internal only.
- **Article IV staff reports & datasets** — partially open as PDFs but not as machine-readable bulk.
- **IMF Direction of Trade quarterly forecast supplements** — internal.

## Rate limits, auth, etiquette

- **No documented rate limit.** Community observation: sustained 1–2 RPS is fine; 10+ RPS sees intermittent 503s.
- **No auth.** Same etiquette house rule as WDI: cap at 2 RPS, 8-deep burst.
- **Response sizes are big.** SDMX-ML is verbose; SDMX-JSON is leaner; CSV is leanest. Adapter should default to CSV.
- **Pagination**: SDMX 3.0 supports `?firstNObservations` / `?lastNObservations` / `?detail=...`. For full-history pulls, use `detail=full` once, then incremental via TIME_PERIOD constraints.

## Vintage truth (the load-bearing question)

The IMF runs three different vintage models depending on the dataset:

1. **WEO vintage archive** — official: every April + October release is preserved as a downloadable database snapshot, plus a separate "Historical WEO Forecasts Database" Excel file at `imf.org/external/pubs/ft/weo/data/WEOhistorical.xlsx`. Vintages back to 1990 for major series, sparser for small economies. **This is the gold standard for forecast backtesting in OPENGEM**: every WEO publication is a *signed, dated forecast we can score after the fact*. Combine with our own L3 leaderboard, and we get an automatic "OPENGEM vs WEO" comparison without any private data dependency.

2. **IFS, CPI, DOTS, BOP** — the SDMX endpoint serves *current revised* values. Historical vintages are not exposed by API. Reconstruction is possible via the IMF's monthly STA bulletins (PDF-era) but is high-cost. **Practical compromise**: cache OPENGEM's IFS pull weekly and treat each cache as the "as-of" vintage. This gives us a forward-only vintage triangle starting at OPENGEM ingest time — better than nothing, worse than ALFRED.

3. **GFS, FSI, FM** — annual or semi-annual revisions baked into the headline release; no separate vintage archive.

## Rate-limit math for OPENGEM

Daily-fresh dashboard target across the IMF surface:

- IFS pinned series: ~80 series × 190 countries × monthly frequency = 15,200 cells, but a single SDMX request can return a country-cross-section in one call. Estimate ~190 calls for IFS sweep.
- CPI monthly: ~190 country-rollups in 1 call (well-formed SDMX key handles this), so ~1 call per refresh.
- DOTS monthly: ~200 reporter × 200 partner is huge — but a single SDMX call can do `M.{reporter}.{indicator}.{partners}` returning thousands of cells. Estimate ~200 calls for full DOTS sweep.
- WEO: snapshot, 2 calls per year (April + October).

Total daily steady-state: ~30 calls (light: only what changed today). Total catch-up after a 2-week outage: ~500 calls. At 2 RPS, that's 4 minutes. Fits trivially.

## License

IMF data terms: "freely available... attribution required... no resale of the unmodified data... derived works must not imply IMF endorsement." This is **GREEN with attribution + no-resale + non-endorsement** — OPENGEM's CC-BY-4.0 stance is compatible if we ship explicit per-cell attribution strings (which we already plan to) and avoid "IMF says..." brand framing on derived charts.

## Fit-for-OPENGEM verdict

- **ADOPT-NOW**: `IFS`, `WEO`, `DOT`, `CPI`, `COFER` — these are the load-bearing five for a credible Block I world dashboard.
- **ADOPT-BLOCK-II**: `BOP`, `BOP_AGG`, `IRFCL`, `FSI`, `GFS` — second-wave for sovereign-risk and financial-conditions pages.
- **CITE-ONLY**: `FAS`, `FM`, `HPDD`, `CDIS`, `CPIS`, GFSR — data is fine but not on our core indicator spine.

**Adapter design notes**:

- Single Python package `opengem-data-imf` covering the SDMX 3.0 surface. One client class with per-dataflow fetchers (`fetch_weo`, `fetch_ifs`, `fetch_dot`, `fetch_cpi`, `fetch_cofer`).
- Hardcode `https://api.imf.org/external/sdmx/3.0/` as base URL. Do **not** use `dataservices.imf.org` (dead path).
- CSV-by-default with `Accept: text/csv`.
- Cache the WEO Excel ZIPs from the publications page once per April/October and ingest them as a separate `fetch_weo_archive(release="2026-04")` path (the SDMX endpoint serves only the latest WEO).
- Provenance: every Observation records `source=imf`, `dataflow=...`, `release_id=...`, `imf_attribution_string=...`.

## Trap log

- **SDMX 2.1 endpoint is dead.** Half the open-source IMF clients on PyPI/CRAN call `dataservices.imf.org` and now return nothing. We must write against 3.0 from day 1 — and pin the API version in the adapter signature.
- **Version wildcard**: use `~` (tilde) for latest, **not** `*`. The asterisk is a known foot-gun that returns 4xx.
- **COFER "unallocated" disappeared in 2025Q3** with retroactive revisions back to 2000Q1. Long-run COFER charts re-rendered against the new endpoint will silently change shape. We must record that the 2025Q3 revision changed the historical baseline, not just the latest reading.
- **WEO is a forecast, not an observation**. Treat WEO values as ForecastObjects in the OPENGEM type system, not Observations. Ingestion should write to a separate vintage namespace.
- **Country codes**: IMF uses a mix of ISO-3 and IMF country codes (`111` for US, `534` for India). The codelist is fetchable via SDMX `/codelist/IMF/CL_AREA/~/`. Adapter should pre-fetch and cache.

## Related

- [[L046]] — World Bank Indicators (complementary multi-country layer)
- [[L048]] — OECD beyond ORDRA
- [[L052]] — IMF DOTS vs UN Comtrade (depth comparison)
- [[R12]] (existing) — reference systems; WEO is the comparator
