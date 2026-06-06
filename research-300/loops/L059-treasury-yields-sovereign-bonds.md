# L059 — Treasury yields + foreign sovereign bonds: open the world curve

**Loop**: 059 / 300
**Phase**: 1 — Open-source landscape survey (data sources)
**Date**: 2026-06-06
**Verdict**: **ADOPT-NOW US Treasury DTYC + DTRYC + FRB H.15 (already in)**, **ADOPT-NOW BoE / Bundesbank / BoJ direct feeds for the G7 curve**, **ADOPT-BLOCK-II ECB YC for euro-area sovereign curve**, **CITE-ONLY Trading Economics / Investing.com aggregators**.

---

## One-line take

The US Treasury yield curve is the load-bearing macro series, and we already have FRB H.15 in OPENGEM. The next move is **Treasury's own DTYC + DTRYC** (par yield curve and real yield curve) for slightly different methodology, plus **direct ingest of BoE / Bundesbank / BoJ daily yield curves** to extend Block I coverage to the G7. The euro-area sovereign-yield panel comes free via the ECB Data Portal (L050). Aggregators (Trading Economics, Investing.com, worldgovernmentbonds.com) wrap these same sources with proprietary value-add — useful for cross-checking but not for ingestion.

## What we want yield-curve data for

- **US 2s/10s spread** — recession-probability load-bearing series (Bauer-Mertens) already in OPENGEM's term-spread model. We need the spread to actually be live.
- **Sovereign credit spread** (foreign 10y − US 10y) — sovereign-risk page.
- **Real yield curve** (TIPS / inflation-linked) — for the inflation-expectations narrative.
- **Yield curve animation across countries** — Bloomberg's terminal does this for $30k/seat; we do it for free.
- **Forward curves** — derive OIS-implied policy-rate paths to compare to OPENGEM's policy-rate forecast.

## US Treasury direct (DTYC + DTRYC + DTLT)

- **DTYC (Daily Treasury Par Yield Curve Rates)**: 1M, 2M, 3M, 4M, 6M, 1Y, 2Y, 3Y, 5Y, 7Y, 10Y, 20Y, 30Y par yields, daily.
- **DTRYC (Daily Treasury Par Real Yield Curve Rates)**: 5Y, 7Y, 10Y, 20Y, 30Y TIPS-derived real yields, daily.
- **DTLT (Daily Treasury Long-Term Rates)**: 30Y and Long-Term Composite.
- **Base URL**: `https://home.treasury.gov/resource-center/data-chart-center/interest-rates/...`
- **Machine access**: XML view at `home.treasury.gov/.../xmlview?data=daily_treasury_yield_curve&field_tdr_date_value={YYYY}` returns per-year XML. CSV view similarly via Treasury's interest-rate pages.
- **Cadence**: daily at ~3 PM ET, with the prior day's curve final.
- **History**: DTYC from 1990; DTRYC from 2003.
- **Auth**: none.
- **Rate limits**: undocumented; per-year file downloads are the right pattern, ~250 daily values per file, ~30 KB.
- **License**: U.S. federal government — **public domain (CC0)**. GREEN.
- **Vintage**: published values are official and never revised. Trivial.

## FRB H.15 (already in OPENGEM)

- Already in `opengem-data-frb`. Covers similar territory to Treasury DTYC with FRB's own constant-maturity methodology. Daily.
- **The DTYC and H.15 Treasury constant-maturity series mostly agree but use different smoothing techniques.** Both are worth ingesting for the cross-source comparison.

## ECB Data Portal — Yield Curves (YC dataflow)

- **Already in scope** via the L050 ECB Data Portal adapter.
- ECB-fitted Svensson zero-coupon yield curve, daily, for the euro area: AAA-rated only and All-euro-area, every basis point of maturity from 3M to 30Y.
- ECB also publishes 10y benchmark yields per member state on the EXR / interest-rate dataflows.

## Bundesbank Time Series Database (BBK)

- **Base URL**: `https://api.statistiken.bundesbank.de/rest/data/` (SDMX REST).
- **API style**: SDMX 2.1 REST. JSON + XML.
- **Auth**: none.
- **Rate limits**: undocumented; community-tested at "permissive."
- **Coverage**: German Bund yields (1M to 30Y) daily, plus a wide range of German + Eurosystem money/credit/banking series.
- **License**: Bundesbank Terms — free for use with attribution. GREEN.

## Bank of England Statistical Interactive Database

- **Base URL**: `https://www.bankofengland.co.uk/boeapps/database/`
- **API style**: query-built CSV download via a request URL with parameters; no formal REST API.
- **Coverage**: UK gilt yields (3M to 50Y) daily; instantaneous forward curves; nominal + real yield curves (fitted).
- **License**: BoE Terms — free for use. GREEN.
- **Methodology note**: BoE publishes its own **fitted nominal + real yield curves** as separate daily files (`yc-nominal-daily.xlsx`, `yc-real-daily.xlsx`). These are the macro reference for UK term structure.

## Bank of Japan / Japan MoF

- **Base URL (MoF)**: `https://www.mof.go.jp/english/policy/jgbs/reference/interest_rate/...` — JGB yields by maturity, daily CSV.
- **Base URL (BoJ)**: `https://www.boj.or.jp/en/statistics/` — broader market rates.
- **Coverage**: JGB 1Y, 2Y, 5Y, 10Y, 20Y, 30Y, 40Y daily.
- **License**: MoF + BoJ — free use with attribution. GREEN.

## Bank of Canada Valet API

- **Base URL**: `https://www.bankofcanada.ca/valet/`
- **API style**: REST. JSON/XML/CSV.
- **Auth**: none.
- **Rate limits**: undocumented; permissive.
- **Coverage**: Government of Canada benchmark bond yields, T-bill rates, real-return bond rates, daily.
- **License**: BoC Open Government — free use with attribution. GREEN.

## RBA (Reserve Bank of Australia) Statistical Tables

- **Base URL**: `https://www.rba.gov.au/statistics/tables/...`
- **API style**: static XLSX with daily updates.
- **Coverage**: Aussie government bond yields, repo rates, AUD bilaterals.
- **License**: RBA Terms — free use with attribution. GREEN.

## Swiss National Bank (SNB) Data Portal

- **Base URL**: `https://data.snb.ch/api/cube/`
- **API style**: REST.
- **Coverage**: Swiss Confederation bond yields, SARON, CHF rates.
- **License**: SNB Terms — free use. GREEN.

## Aggregators (Trading Economics, Investing.com, worldgovernmentbonds.com)

- These republish the above central-bank sources with proprietary value-add (consistent country naming, sector tagging, charting widgets).
- **No machine API at the free tier**; web scraping is a ToS risk.
- **Verdict for OPENGEM**: **CITE-ONLY**. Cross-check our direct-ingest values against worldgovernmentbonds.com manually as a QC step; do not ingest.

## Rate-limit math for OPENGEM

Per-country daily yield-curve ingest:
- **US Treasury DTYC + DTRYC**: 2 files/day.
- **FRB H.15**: already in.
- **ECB YC**: 1 SDMX call/day (already in L050 budget).
- **Bundesbank**: 1 SDMX call/day.
- **BoE**: 2 file downloads/day (nominal + real yield curve XLSX).
- **BoJ / MoF**: 1 CSV/day.
- **BoC Valet**: 1 call/day.
- **RBA**: 1 XLSX/day.
- **SNB**: 1 call/day.

**Total G7+CHF daily**: ~10 calls/day. **Trivial.**

Annual backfill: ~50 calls per country. ~500 calls total. Fits in minutes.

## The "world yield curve" page

A unique OPENGEM artifact opportunity: a single page showing **G7 + euro-area peripheries + EM-key benchmark 10y yields** as a heatmap, plus the per-country curve shape, with the 2s/10s spread highlighted. Add a "yield curve animation" feature showing the curve evolution by month — the kind of chart that's been Bloomberg-Terminal-exclusive for 25 years.

This is buildable from the adapters above, with no paid data, in one prototype week.

## Vintage truth

Yield-curve values are observed market data, finalized at end-of-day. **No revisions.** Vintage is trivial for headline rates.

Fitted curves (BoE Svensson, ECB Svensson, NSS spline) are recomputed when methodology changes. Adapter should record `curve_methodology=svensson|nss|par|...` per Observation.

## Fit-for-OPENGEM verdict

- **ADOPT-NOW**: US Treasury DTYC + DTRYC (extends `opengem-data-treasury`); Bundesbank / BoE / BoJ-MoF / BoC / SNB / RBA direct (new package `opengem-data-rates-foreign`).
- **ADOPT-BLOCK-II**: emerging-market sovereign curves via national central-bank sources (China, India, Brazil, South Africa, Turkey, Mexico).
- **CITE-ONLY**: aggregators (Trading Economics, Investing.com, worldgovernmentbonds.com).
- **SKIP**: paid bond-data feeds (Refinitiv, Bloomberg, ICE Data).

**Adapter design notes**:

- Extend `opengem-data-treasury` to add `fetch_dtyc(year)`, `fetch_dtryc(year)`, `fetch_dtlt(year)`.
- New package `opengem-data-rates-foreign` with submodules:
  - `BundesbankAdapter` — SDMX REST.
  - `BoEAdapter` — XLSX file downloads.
  - `BoJ_MoFAdapter` — CSV file downloads.
  - `BoCValetAdapter` — REST/JSON.
  - `SNBAdapter` — REST.
  - `RBAAdapter` — XLSX file downloads.
- Provenance: every Observation records `source=treasury|frb|ecb|bundesbank|boe|boj|boc|snb|rba`, `maturity_tenor=...`, `curve_methodology=...`.

## Trap log

- **DTYC and H.15 don't perfectly agree** — different constant-maturity smoothing. The difference is typically <1 bp but adapter should preserve both, not pick one.
- **BoE publishes nominal + real curves** as separate files. Adapter must distinguish; some methodologies put "real curve" in the same XLSX as a different sheet.
- **BoJ JGB yields use different maturity conventions** (1Y, 2Y, 5Y, 10Y, 20Y, 30Y, 40Y) — no 30M/3M/6M short end at the same granularity as DTYC.
- **Euro-area peripheries (Italy, Spain, France, Portugal, Greece)** — yield-curve series come from each national central bank or treasury, not from a single ECB dataflow. We need per-country sources for the spread page.
- **Bond yields are denominated in local currency**; for cross-country comparison the "FX-adjusted" view requires explicit FX conversion. Don't conflate.
- **Federal Reserve "10-Year Treasury Constant Maturity Minus 2-Year Treasury Constant Maturity" (T10Y2Y) is the FRED-served spread series**; our adapter computes it locally from DTYC.
- **Trading Economics and Investing.com both scrape central-bank sources without explicit license**; using them as data sources for OPENGEM would mean stacking license risk on top of license risk. Always go to the central-bank originals.

## What this enables on the dashboard

- **Recession-prob tile**: 2s10s spread live, with Bauer-Mertens probability.
- **Sovereign-risk page**: 10y spread vs US for every G20 country, with credit rating overlay.
- **Yield curve page**: animated curve across time, per country.
- **Real yield page**: TIPS-derived real curve and breakeven inflation expectations.
- **Term-premium estimates**: derive from the same data using ACM or Kim-Wright methodology.

All from free open sources. All with public methodology. **Exactly the "open as a moat" thesis.**

## Related

- [[R09]] (existing) — FRED-substitution; H.15 mapped
- [[L057]] — FX free APIs
- [[L049]] — BIS Statistics (debt securities + CBPOL complement)
- [[L050]] — ECB Data Portal (YC dataflow)
