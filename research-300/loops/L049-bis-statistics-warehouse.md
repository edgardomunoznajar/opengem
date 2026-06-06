# L049 — BIS Statistics warehouse: the cross-border banking & credit telescope

**Loop**: 049 / 300
**Phase**: 1 — Open-source landscape survey (data sources)
**Date**: 2026-06-06
**Verdict**: **ADOPT-NOW (LBS, CBS, EER, CREDIT_GAPS via bulk)**, ADOPT-BLOCK-II (debt securities, DSR, RPP), CITE-ONLY (Triennial Survey, payments).

---

## One-line take

OPENGEM already uses BIS CBPOL — that's the smallest, cleanest BIS dataset. The other twenty-three datasets behind `data.bis.org` are the **only open machine-readable lens on cross-border banking, global liquidity, effective exchange rates, and the BIS credit-to-GDP gap** — the load-bearing variables for any honest sovereign-risk and financial-conditions page. We should ingest via **bulk SDMX zips** rather than the live REST API: BIS data updates monthly/quarterly, the zips are small, and bulk is the BIS's blessed path.

## What it is now (post-2024 re-platform)

The BIS data portal was re-launched as `data.bis.org` in 2023–2024, replacing the older `stats.bis.org` interface. The SDMX REST API is documented at `stats.bis.org/api-doc/v2/` and uses SDMX 2.1.

- **API base**: `https://stats.bis.org/api/v2/` (SDMX 2.1 REST)
- **Bulk downloads**: `https://data.bis.org/bulkdownload` — full topic ZIPs in CSV or SDMX (Compact / Generic) format
- **Auth**: none
- **Rate limits**: no documented per-IP cap; bulk download is the recommended path for big sweeps. Community lore: REST endpoint comfortably handles 1 RPS sustained; bulk ZIPs are tens-of-MB and update mostly monthly.
- **License**: BIS "Terms of permitted use" — academic / research / non-commercial freely redistributable with attribution; commercial use of derived works permitted but BIS branding cannot be implied. **GREEN with attribution + non-commercial-redistribution-of-unmodified-data restriction.**

## Datasets that matter

| Dataset | Code (bulk-zip name) | Frequency | Cadence | Coverage | OPENGEM fit |
|---|---|---|---|---|---|
| **Central bank policy rates** | `WS_CBPOL` | Daily | T+1d | 45 central banks | **ALREADY IN** (opengem-data-bis) |
| **Locational banking statistics** | `WS_LBS_D_PUB` | Quarterly | T+150d | 47 reporting countries × 200+ counterparties | **ADOPT-NOW** — cross-border bank claims by reporter × counterparty × currency × instrument |
| **Consolidated banking statistics** | `WS_CBS_PUB` | Quarterly | T+150d | 31 reporters × 200+ counterparties | **ADOPT-NOW** — bank exposure by nationality (CBPOL's nationality-perspective sibling) |
| **Effective exchange rates** | `WS_EER` | Daily + Monthly | T+1d | Broad (64 economies, 1994+); Narrow (27, 1964+) | **ADOPT-NOW** — REER + NEER, the only open daily series with this country breadth |
| **Credit-to-GDP gaps** | `WS_CREDIT_GAP` | Quarterly | T+90d | 44 economies, from 1961 | **ADOPT-NOW** — one-sided HP-filter trend; BIS-canonical early-warning signal |
| **Credit to non-financial sector** | `WS_TC` | Quarterly | T+90d | 44 economies | **ADOPT-NOW** — total / households / NFCs / government in local currency, USD, PPP-USD, % GDP |
| **Debt service ratios (DSR)** | `WS_DSR` | Quarterly | T+90d | 32 economies | ADOPT-BLOCK-II — financial-stress proxy |
| **Debt securities statistics (DSS)** | `WS_DEBT_SEC` | Quarterly | T+90d | Issuer × currency × maturity | ADOPT-BLOCK-II — cross-border bond market plumbing |
| **International debt securities** | `WS_INTL_DEBT_SEC` | Quarterly | T+90d | Subset of DSS, by nationality | ADOPT-BLOCK-II |
| **Residential property prices (RPP)** | `WS_LONG_CPI`/`WS_RPP` | Quarterly | T+120d | 60 economies, long history | ADOPT-BLOCK-II — housing market page |
| **Commercial property prices** | `WS_CPP` | Quarterly | T+120d | 22 economies | ADOPT-BLOCK-II |
| **Consumer prices (BIS CPI panel)** | `WS_LONG_CPI` | Monthly | T+30d | 60 economies, very long history | ADOPT-BLOCK-II — alternative to IFS CPI for historical depth |
| **Triennial survey (FX + derivatives)** | `WS_OTC_DERIV2` | Tri-annual | Dec of survey year | Global | CITE-ONLY (low news cadence) |
| **Exchange-traded derivatives** | `WS_XTD_DERIV` | Quarterly | T+90d | Global | CITE-ONLY |
| **OTC derivatives** | `WS_OTC_DERIV2` | Semi-annual | T+150d | Global | CITE-ONLY |
| **Central bank total assets** | `WS_CBTA` | Monthly | T+30d | 33 central banks | ADOPT-BLOCK-II — balance-sheet narrative |
| **Payment system statistics (CPMI)** | `WS_CPMI_DEVICET` etc. | Annual | T+12mo | CPMI member economies | CITE-ONLY |

## Bulk download is the right pattern

Three reasons to favor bulk over REST for everything except CBPOL:

1. **Update cadence matches.** LBS/CBS update once a quarter. EER is daily but the daily ZIP is tiny (~few MB). There's no business reason to hammer the REST API.
2. **The data is multi-dimensional and big.** A single REST call for LBS-by-counterparty-by-currency-by-instrument can return tens of thousands of cells. The bulk SDMX-Compact ZIP is more bandwidth-efficient.
3. **The BIS Terms of Use endorse bulk.** "Bulk downloads" is its own portal section, not a fallback.

For CBPOL we'd keep the REST path because it's daily and we already have it working. Everything else: bulk.

## Rate-limit math for OPENGEM

Daily-fresh target across the full adopted BIS surface:

- **CBPOL (REST, already in)**: 45 series × 1 daily call ≈ 1 batched call per refresh. Sub-second.
- **EER bulk ZIP**: 1 download per day (daily file), ~5 MB. Trivial.
- **LBS / CBS / Credit / Credit-Gap / DSR bulk ZIPs**: 1 download per quarter, each 20–80 MB. ~5 downloads/quarter total. Run on the BIS release calendar (we'd subscribe to the BIS statistical-release ICS feed).
- **CPI / RPP / CPP / CBTA**: monthly or quarterly ZIPs. ~10 downloads/month total.

Daily steady-state: ~2 small calls. Monthly: ~10 ZIP downloads. Total daily wall clock: <1 minute. **Cheaper than any other macro adapter.**

Backfill at adapter bootstrap: all historical ZIPs in one parallel sweep, ~250 MB total, ~10 minutes on a reasonable connection.

## What the BIS uniquely gives us

This is the only place to get, on the open internet:

1. **Cross-border bank claims by reporter × counterparty × currency** — the variable that drives 80% of sovereign-stress narratives (LBS).
2. **Bank exposures by nationality of parent** — the variable that drives international-bank contagion narratives (CBS).
3. **REER / NEER for 64 economies, daily** — the only open daily REER panel with this breadth. The OECD has REER but with shorter history and fewer countries.
4. **Credit-to-GDP gap, BIS canonical formula** — the early-warning indicator that the BIS itself publishes and that virtually every central bank cites. Open replication of this would be possible, but using the BIS-canonical series eliminates a calibration debate.
5. **Long-run CPI panel back to ~1870** — for any "in real terms" or "in historical perspective" claim.

No other source has any one of these. Bloomberg has 3 of 5 behind a $30k/seat paywall.

## Vintage truth

BIS releases revisions on the standard quarterly cadence — older quarters get restated as more reporters file. The bulk ZIPs are *replacement* snapshots, not vintage triangles. To build a vintage history, OPENGEM must:

- Archive each bulk ZIP at ingest time, stamped with retrieval date.
- Treat each archived ZIP as a vintage. We'd accumulate a forward-only vintage stack starting at OPENGEM ingest.

This is the same compromise we take with IFS. No worse than the open-data state of the art.

## Fit-for-OPENGEM verdict

- **ADOPT-NOW** (extends existing `opengem-data-bis`): LBS, CBS, EER, CREDIT_GAPS, TC (total credit).
- **ADOPT-BLOCK-II**: DSR, DSS, INTL_DEBT_SEC, RPP, CPP, BIS CPI, CBTA.
- **CITE-ONLY**: Triennial Survey, XTD_DERIV, OTC_DERIV2, CPMI payments.
- **SKIP**: nothing.

**Adapter design notes**:

- Extend `opengem-data-bis` (currently CBPOL-only) to a multi-dataset package.
- Add `fetch_bulk(topic, format="csv")` method that pulls the ZIP from `https://data.bis.org/static/bulk/{TOPIC}_csv_*.zip` (the BIS bulk URL pattern is stable per topic).
- Keep `fetch_cbpol` via REST as is.
- Each ingest emits Observations with `source=bis`, `topic=...`, `release_id=YYYY-Qn` (or YYYY-Mn for monthly), `bis_attribution=...`.
- Subscribe to BIS release calendar ICS feed (`bis.org/statistics/calendar.htm`) for triggering ingests.

## Trap log

- **The `stats.bis.org` (old) and `data.bis.org` (new) hostnames coexist** during the transition. New code should target `data.bis.org` for the portal and `stats.bis.org/api/v2/` for the SDMX REST. Some 2022-era community wrappers hit the old paths and silently 404.
- **LBS is reporter-perspective; CBS is nationality-perspective.** Don't conflate. A bank with a UK subsidiary lending to Brazil shows up in UK-reporter LBS *and* in (say) US-nationality CBS if it's a US parent. We need both for any sovereign-risk narrative.
- **Credit-to-GDP gap uses one-sided HP filter** with the BIS's specific lambda. Don't try to "improve" it by computing your own — the BIS series is the policy benchmark, even if academics dislike HP.
- **Bulk ZIPs sometimes change structure** between releases when BIS adds dimensions. Adapter must validate against the SDMX Data Structure Definition each ingest.
- **Some series are reporter-redacted** (confidential bilateral cells). Those return as missing in the ZIPs, not zero. Don't infer "no exposure" from missing.
- **EER weights are revised every 3 years.** This causes apparent retroactive revisions even when the underlying FX data didn't change. Adapter should record the EER weight vintage.

## Related

- [[L046]] — World Bank Indicators
- [[L047]] — IMF SDMX (BOP overlap with BIS LBS for cross-border claims)
- [[L057]] — FX (EER vs ECB Eurofxref vs FRB H.10)
- [[R06]] (existing) — wider information surface
