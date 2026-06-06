# L050 — ECB Data Portal (ex-SDW): euro-area depth, no auth, clean SDMX 2.1

**Loop**: 050 / 300
**Phase**: 1 — Open-source landscape survey (data sources)
**Date**: 2026-06-06
**Verdict**: **ADOPT-NOW** — third-priority multi-country adapter after WB and IMF, ahead of OECD-beyond-ORDRA. The euro area is a unit OPENGEM cannot half-ass.

---

## One-line take

The ECB Data Portal (formerly Statistical Data Warehouse) is one of the cleanest open central-bank APIs in existence — SDMX 2.1 REST, no auth, public domain, supports CSV/JSON/SDMX-ML, has explicit `updatedAfter` and `includeHistory` parameters that make incremental updates *and* basic vintage queries trivial. The migration from `sdw-wsrest.ecb.europa.eu` to `data-api.ecb.europa.eu` is done as of mid-2025, and the redirects retired October 2025 — so anything written against the old hostname today is dead code.

## What it is

- **Base URL**: `https://data-api.ecb.europa.eu/service/`
- **API style**: SDMX 2.1 RESTful, with SDMX-JSON 2.0 (a.k.a. SDMX 3.0 JSON) also supported on data queries.
- **Operating modes**: data retrieval (specific cell queries) + data discovery (metadata-driven crawl).
- **Auth**: none.
- **Rate limits**: not published. ECB-published "useful tips" page does not enumerate them. Community-observed: 2 RPS sustained is fine; 10+ RPS sees occasional 503s. House rule for OPENGEM: 1 RPS sustained, 6-deep burst.
- **License**: CC0 / public-domain-equivalent on the data layer. Attribution requested as a courtesy but not legally required. **GREEN — no friction.**
- **Update cadence**: most series update on their natural source cadence (daily FX, monthly money supply, quarterly euro-area accounts), and the API is fresh within minutes of release.

## Query grammar

```
protocol://wsEntryPoint/resource/flowRef/key?parameters
```

Concrete: `https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?startPeriod=2020-01-01&format=csvdata`

- **Series keys** are dot-separated dimensions. Omit a dimension to wildcard. `+` for OR. Example: `D.USD+JPY.EUR.SP00.A` returns both USD/EUR and JPY/EUR daily reference rates.
- **Date filters**: `startPeriod`, `endPeriod` in ISO-8601 or SDMX date forms.
- **Detail levels**: `detail=full|dataonly|serieskeysonly|nodata` — `dataonly` is the lean fetch.
- **Incremental updates**: `updatedAfter=2026-06-01T00:00:00Z` returns only series modified since a timestamp. This is **rare** in macro APIs and *critical* for our daily-fresh refresh loop.
- **Vintage queries (sort of)**: `includeHistory=true` returns the previous version of a series alongside the current. This is not a full revision triangle, but it gives us "what changed between today and last revision" for free.
- **Pagination**: not formally paginated; responses are server-side capped (community-tested at "very large" — easily 100k+ observations in one response).

## Dataflows that matter

| Dataflow | Code | Frequency | Cadence | Coverage | OPENGEM fit |
|---|---|---|---|---|---|
| **Exchange rates (reference)** | `EXR` | Daily | T+1d (14:15 CET fixing) | ~35 currencies vs EUR | **ADOPT-NOW** — the only open canonical daily EUR cross-rates |
| **Yield curves (AAA & all-EA)** | `YC` | Daily | T+1d | Euro area, ECB-fitted Svensson | **ADOPT-NOW** — euro-area sovereign yield curve |
| **Monetary aggregates** | `BSI` | Monthly | T+30d | Euro area + member states | **ADOPT-NOW** — M1/M2/M3, credit |
| **MFI interest rates** | `MIR` | Monthly | T+30d | Euro area + member states | **ADOPT-NOW** — bank lending/deposit rates |
| **Euro-area HICP** | `ICP` | Monthly | T+30d (flash T+10d) | Euro area + member states | **ADOPT-NOW** — inflation spine |
| **National accounts (ENA)** | `MNA` | Quarterly | T+90d | Euro area + member states | **ADOPT-NOW** — GDP, components |
| **Labour force statistics** | `LFSI` | Quarterly | T+90d | Euro area + member states | **ADOPT-NOW** — unemployment, participation |
| **Balance of payments** | `BPS` | Quarterly | T+90d | Euro area aggregate | ADOPT-BLOCK-II |
| **Securities issues** | `SEC` | Monthly | T+30d | Euro area, by issuer/currency | ADOPT-BLOCK-II |
| **Securities holdings (SHS)** | `SHS` | Quarterly | T+120d | EU/euro-area | ADOPT-BLOCK-II |
| **Survey of Professional Forecasters (SPF)** | `RTD` | Quarterly | T+45d | Euro area | **ADOPT-NOW** — third forecast comparator after WEO/EO |
| **Government finance** | `GFS` | Quarterly + Annual | T+90d / T+12mo | Euro area + member states | ADOPT-BLOCK-II |
| **Property prices** | `RPP` | Quarterly | T+150d | Euro area + members | ADOPT-BLOCK-II |
| **Bank lending survey** | `BLS` | Quarterly | T+30d | Euro area | ADOPT-BLOCK-II |
| **Composite Indicator of Systemic Stress (CISS)** | `CISS` | Daily | T+1d | Euro area + selected members | **ADOPT-NOW** — financial-stress proxy for sit-rep |

## Why ECB is "third priority" not "later"

OPENGEM's existing roster (BEA/BLS/FRB/Treasury/Census + ORDRA + BIS + GSCPI + GPR) gives strong US coverage and shallow non-US coverage. The euro area is 14% of world GDP and the second-most-cited macro economy. **No ECB ingest = no defensible euro-area dashboard.** ORDRA covers macroeconomic aggregates for euro-area members at monthly/quarterly cadence but at MEI's coarse granularity. ECB Data Portal goes deeper:

- HICP at the component breakdown (ICP) — not in MEI's headline-only roster.
- MFI lending rates (MIR) — not in MEI at all.
- ECB SPF — the third forecast comparator (after WEO + EO), giving OPENGEM a public forecast triplet to score against on euro-area aggregates.
- Yield curves (YC) — the ECB's own zero-coupon AAA curve, used in every euro-area policy paper.
- CISS — a single daily financial-stress index.

These are the indicators a sovereign-fund LP browsing the euro-area page expects to find. Skipping them is a credibility hit.

## Rate-limit math for OPENGEM

Daily-fresh target across the euro area:

- **Daily series (EXR + YC + CISS)**: 3 wildcarded calls returning ~100 series total per call. 3 calls at 1 RPS = trivial.
- **Monthly series (ICP + BSI + MIR + headline HICP flash)**: 4 calls per month, each wildcarded across euro-area + ~20 members. 4 calls, trivial.
- **Quarterly series (MNA + LFSI + BPS + GFS + RPP + BLS)**: 6 calls per quarter. Trivial.
- **SPF**: 1 call per quarter.

Daily steady-state: **3 calls**. Monthly: **3 + 4 = 7**. Quarterly: **3 + 4 + 7 = 14**.

`updatedAfter` is the magic ingredient: a daily refresh job can do one call with `updatedAfter=yesterday` per dataflow and only get the cells that changed. **The entire euro-area ingest costs <10 calls/day.** Fastest adapter in the OPENGEM stack.

Backfill: full history sweep across all adopted dataflows is ~50 calls, fits inside 1 minute at 1 RPS.

## Vintage truth

The ECB API supports `includeHistory=true`, which returns the immediately preceding version of each series cell. This is **better than IFS or WDI** (which give only current revised) but **worse than ALFRED** (which gives a full revision triangle).

Practical OPENGEM compromise:

- Adapter calls each dataflow with `includeHistory=true` on each refresh.
- Each Observation pair (current + previous) lands in the vintage store as two rows.
- Over time this accumulates a *coarse* vintage triangle — not as rich as a full ALFRED replay, but the only open central-bank vintage source other than ALFRED.

## Fit-for-OPENGEM verdict

- **ADOPT-NOW** (Block I): EXR, YC, BSI, MIR, ICP, MNA, LFSI, SPF, CISS.
- **ADOPT-BLOCK-II**: BPS, SEC, SHS, GFS, RPP, BLS.
- **CITE-ONLY**: nothing on the ECB surface is CITE-ONLY; everything is either adopted or not yet evaluated.
- **SKIP**: nothing.

**Adapter design notes**:

- New package `opengem-data-ecb` paralleling `opengem-data-ordra`.
- Base client class with one method per pinned dataflow.
- Default to CSV-data response for ingestion speed.
- Standard refresh: per-dataflow `updatedAfter` + `includeHistory` daily; the response is a delta with previous-versions, write both vintages.
- Provenance: every Observation records `source=ecb`, `dataflow=...`, `flowRef=...`, `key=...`, `prev_version_observed=true|false`.

## Trap log

- **Old hostname `sdw-wsrest.ecb.europa.eu` is dead** as of October 2025 (redirects retired). Anything in the wild written against it is broken. Adapter must hardcode `data-api.ecb.europa.eu`.
- **Key vs flowRef confusion**: `flowRef` is the dataflow ID (e.g., `EXR`); `key` is the dot-separated dimension tuple. Many tutorials conflate the two.
- **Empty dimension positions are wildcards**, but you need the right number of dots. EXR has 5 dimensions: `D..EUR.SP00.A` (wildcards currency).
- **The SDMX-JSON 2.0 format is "SDMX 3.0 JSON" branding**. Confusing in docs.
- **Euro-area aggregate vs member-state series**: the aggregate has its own REF_AREA code (`U2` for euro area, evolves with enlargement; `U2_19` for the 19-member EA). Cross-vintage analyses need to be aware that "euro area" is not a fixed object.
- **Flash HICP releases at T+10d are revised** at the final T+30d release. Adapter should distinguish flash vs final via the `OBS_STATUS` attribute.

## Related

- [[L046]] — World Bank Indicators
- [[L047]] — IMF SDMX
- [[L048]] — OECD beyond ORDRA
- [[L057]] — FX free APIs (ECB EXR is the GREEN-est option)
