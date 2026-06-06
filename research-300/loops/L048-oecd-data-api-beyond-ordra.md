# L048 — OECD Data API + ORDRA: what to add beyond ORDRA

**Loop**: 048 / 300
**Phase**: 1 — Open-source landscape survey (data sources)
**Date**: 2026-06-06
**Verdict**: **ADOPT-NOW (EO + QNA + MEI core)**, ADOPT-BLOCK-II (KEI, BTS, CLI, STAN). ORDRA stays load-bearing for vintage; the OECD Data API stays load-bearing for current values + forecasts.

---

## One-line take

OPENGEM already uses ORDRA for vintage truth across 32 OECD economies — but ORDRA is **release-stamped, low-frequency, slow-to-update** for our daily-fresh dashboard target. The current `sdmx.oecd.org` data API is the right complement: it delivers the OECD Economic Outlook (EO) projections — the OECD's twice-yearly forecast that we have to beat — plus QNA, MEI, KEI, BTS, and CLI on a fresh-as-of-release cadence, with no auth, generous rate limits, and a clean SDMX 3.0 grammar.

## Where ORDRA stops and the OECD Data API starts

**ORDRA strengths (already in OPENGEM)**:
- Vintage-correct quarterly real-time matrix back to 1999.
- 32 economies (OECD + a handful of partners: BR, IN, ID, RU, ZA).
- ~130 series catalogue.
- Loadable as static archive — one `tar.gz` per vintage round.

**ORDRA weaknesses**:
- Vintage rounds are themselves released slowly (~once per quarter, not per OECD MEI revision).
- No projections (it's an observation archive).
- No high-frequency (monthly) MEI breakdown beyond the headline aggregates.
- Limited to the MEI series spine — no Economic Outlook, no Business Tendency Surveys, no CLI/composite indicators.

**OECD Data API fills exactly those gaps.**

## What the OECD Data API is

- **Base URL**: `https://sdmx.oecd.org/public/rest/`
- **API style**: SDMX 3.0 REST. Returns SDMX-ML, SDMX-JSON, or CSV (with `format=csvfilewithlabels` for human-readable labels).
- **Auth**: none. Anonymous queries only.
- **Rate limit**: published as "best-practices" doc; in practice: ~1,000,000 observations cap per response, ~1,000 char URL cap, undocumented per-IP per-minute cap (community-tested at ~30 RPM steady; throttles at sustained 1 RPS+). House rule: cap our adapter at 0.5 RPS, 4-deep burst. Slower than WB/IMF because OECD throttles harder.
- **License**: OECD Terms and Conditions — broadly equivalent to CC-BY for the data layer, with no-resale and no-implied-endorsement clauses. **GREEN with attribution + non-endorsement framing.**

## Datasets to add beyond ORDRA

| Dataflow | OECD code | Frequency | Cadence | Coverage | OPENGEM fit |
|---|---|---|---|---|---|
| **Economic Outlook** | `DSD_EO@DF_EO` (agency `OECD.ECO.MAD`) | Bi-annual + 2y projections | June + November | 50 economies (G20+) | **ADOPT-NOW** — the forecast benchmark alongside WEO |
| **Quarterly National Accounts** | `DSD_NASEC10@DF_TABLE14` etc. (`OECD.SDD.NAD`) | Quarterly | T+60d | OECD-38 | **ADOPT-NOW** — current values; complements ORDRA vintage |
| **Main Economic Indicators (MEI)** | `DSD_MEI@DF_MEI` | Monthly | T+30d | OECD-38 + 8 partners | **ADOPT-NOW** — high-freq labor / IP / retail / business surveys |
| **Key Economic Indicators (KEI)** | `DSD_KEI@DF_KEI` | Monthly/Q | T+30d | OECD-38 | ADOPT-BLOCK-II — KEI is a curated MEI subset; useful for dashboard tiles |
| **Composite Leading Indicators (CLI)** | `DSD_KEI@DF_CLI` | Monthly | T+45d | OECD-38 + China, India, Brazil, Russia, S Africa, Indonesia | **ADOPT-NOW** — turning-point detector, feeds recession-prob narrative |
| **Business Tendency Surveys (BTS)** | `DSD_KEI@DF_BTS` | Monthly | T+30d | OECD-38 | ADOPT-BLOCK-II — sentiment overlay |
| **Consumer Confidence (CCI)** | `DSD_KEI@DF_CCI` | Monthly | T+30d | OECD-38 | ADOPT-BLOCK-II |
| **Producer Price Index (PPI)** | `DSD_KEI@DF_PPI` | Monthly | T+30d | OECD-38 | ADOPT-BLOCK-II |
| **Unit Labour Costs** | `DSD_NAEU@DF_ULC` | Quarterly | T+90d | OECD-38 | ADOPT-BLOCK-II — competitiveness page |
| **STAN industrial structure** | `DSD_STAN@DF_STAN` | Annual | Sept | 38 economies × ISIC | CITE-ONLY (annual; low news value) |
| **Trade in Value Added (TiVA)** | `DSD_TIVA@DF_TIVA` | Annual (3y lag) | Nov | 76 economies | CITE-ONLY (slow; useful for L2 BGVAR scenario work only) |
| **Tax Revenue Statistics** | `DSD_REV@DF_REV` | Annual | Dec | OECD-38 | CITE-ONLY |
| **OECD.Stat fiscal monitoring (PDB)** | `DSD_PDB@DF_PDB` | Quarterly | T+90d | OECD-38 | ADOPT-BLOCK-II |

## The Economic Outlook (EO) is the real prize

For OPENGEM's "publish our mistakes, name our betters" thesis, **the OECD Economic Outlook is one of the two named comparators** (alongside IMF WEO).

- **Cadence**: two full releases per year (June + November), each containing 2-year projections for GDP, CPI, unemployment, fiscal balances, current account, policy rates across G20 + a few small advanced economies. Plus an "Interim" release in March + September with narrower country coverage and revised top-line.
- **Coverage**: ~50 economies — wider than ORDRA, less wide than WEO. EO is editorially deeper than WEO (each release reads as a committee-vetted scenario narrative).
- **Vintage archive**: every EO release is preserved at OECD.org as a downloadable Excel + PDF. The SDMX endpoint exposes only the latest — so OPENGEM must ingest the *archive* path separately, the same way we have to for WEO.
- **Comparator value**: OECD EO forecasts are public, dated, country-by-country. We can score every EO release after the fact and publish "OPENGEM vs OECD EO vs WEO" on the leaderboard page. Zero private data dependency.

## Rate-limit math for OPENGEM

Target: daily-fresh dashboard for OECD-38, with multi-week catch-up tolerance.

- MEI monthly sweep: ~38 countries × 50 pinned series. SDMX key allows 1 call per country (50-series batch), so ~38 calls/sweep. At 0.5 RPS, ~1.3 minutes. Run weekly.
- QNA quarterly: 38 countries × 20 series, 1 call per country, ~38 calls. Run monthly.
- CLI / BTS / CCI / PPI: each ~38 calls. Run monthly.
- EO: 2 SDMX-ML downloads/year + 2 Excel archive downloads/year (March + Sept interims). 4 calls total, batched.

Total monthly steady-state: ~150 calls. At 0.5 RPS that's 5 minutes. **Fits trivially even with OECD's tighter throttling.**

Backfill cost: full pinned-MEI history × 38 countries × 50 series with one-call-per-(country,series) worst case is ~1,900 calls. At 0.5 RPS: ~63 minutes. One-shot at adapter bootstrap.

## License & attribution

OECD requires attribution and a no-implied-endorsement clause. Our adapter will emit per-cell strings like:

> "Source: OECD Main Economic Indicators (MEI), retrieved via OECD SDMX API on 2026-06-06. Not an OECD product."

This is identical to our planned IMF attribution pattern. License classification: **GREEN with attribution + non-endorsement**.

## Vintage truth — how ORDRA + the live API compose

The two together give OPENGEM the cleanest open vintage architecture available outside ALFRED:

1. **ORDRA** = vintage observation matrix back to 1999. The truth as it was *believed* at the time of each MEI release round.
2. **Live OECD Data API** = current revised values. The truth as it is *believed today*.
3. **EO archive** = forecast vintage matrix back to 1990s. The truth the OECD *projected* at the time.

OPENGEM stores all three in the vintage store with distinct namespaces:
- `oecd.ordra.{round}.{indicator}.{country}` for vintage observations
- `oecd.api.live.{indicator}.{country}` for current revised values
- `oecd.eo.{release}.{indicator}.{country}.{horizon}` for forecasts

This composition gives backtesting infrastructure that does not exist anywhere else for OECD economies as a clean machine-readable set.

## Fit-for-OPENGEM verdict

- **ADOPT-NOW** (Block I): EO archive ingest, QNA, MEI core, CLI.
- **ADOPT-BLOCK-II**: KEI, BTS, CCI, PPI, ULC, PDB.
- **CITE-ONLY**: STAN, TiVA, REV.
- **SKIP**: nothing on this list is truly skippable; everything is cheap to add when needed.

**Adapter design notes**:

- Extend `opengem-data-ordra` into a new package `opengem-data-oecd` covering the live + EO surface. ORDRA stays as a sub-module within it (or remains its own package and the new one depends on shared SDMX helpers — leaning toward the latter for clean publishability).
- Hardcode `https://sdmx.oecd.org/public/rest/` base URL.
- CSV with labels by default.
- EO archive ingest: walk `oecd.org/en/publications/oecd-economic-outlook_16097408.html` once per June + Nov + March + Sept release for the Excel ZIP. Manual confirmation step is fine because cadence is twice/4x per year.
- Provenance: every Observation records `source=oecd`, `dataflow=...`, `release_id=...`, `vintage_round=...` (for ORDRA observations), `non_endorsement=true`.

## Trap log

- **Response cap of 1M observations** sounds large but is easy to blow with a careless `?detail=full` over a multi-decade MEI sweep with no country filter. Always filter on `REF_AREA`.
- **URL length cap of 1,000 chars**. Long dimension keys (especially with `+` joining many country codes) hit this fast. Adapter must chunk.
- **OECD throttles harder than IMF/WB.** 30 RPM sustained is the soft ceiling. Don't try to be clever.
- **EO interim releases (March + Sept) have narrow coverage** — only G7 + euro area + a few. Don't expect a full 50-country panel from interims.
- **Dataflow URLs are agency-prefixed** (`OECD.ECO.MAD`, `OECD.SDD.NAD`, etc.). Hardcoded clients written against the old `stats.oecd.org` interface will silently 404.
- **The old `stats.oecd.org` endpoint is deprecated as of late 2024.** Some R/Python wrappers (e.g., `OECD` CRAN package) still target it and need rewriting.

## Related

- [[L046]] — World Bank Indicators
- [[L047]] — IMF SDMX
- [[L050]] — ECB SDW (similar SDMX 3.0 surface for euro-area depth)
- [[R02]] (existing) — Tier-V coverage; ORDRA is the seed
