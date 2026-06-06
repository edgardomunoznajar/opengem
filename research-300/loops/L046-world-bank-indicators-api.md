# L046 — World Bank Indicators API + WDI: the workhorse of multi-country macro

**Loop**: 046 / 300
**Phase**: 1 — Open-source landscape survey (data sources)
**Date**: 2026-06-06
**Verdict**: **ADOPT-NOW** — first non-US adapter to ship.

---

## One-line take

The World Bank Indicators API is the **closest thing to a universal macro covariate vending machine** on the open internet — 16,000 indicators, 200+ economies, no auth, no published rate limit, CC-BY-style license — and OPENGEM should treat it as the *default fallback* for any indicator a more-authoritative national source doesn't cover.

## What it is

- **Base URL**: `https://api.worldbank.org/v2/` (v1 fully sunset 2020-06-19).
- **Catalog scope**: World Bank docs say "nearly 16,000 time series indicators across 45+ databases." The headline database — **World Development Indicators (WDI)** — carries ~1,400 indicators with the broadest country panel.
- **Other databases of interest**: Global Financial Development (~110 series), International Debt Statistics, Doing Business (archival now), Human Capital Index, Worldwide Governance Indicators, Population estimates and projections (WPP-derived), Poverty and Inequality (PIP).
- **API styles**: REST returning JSON / XML / JSONP / JSON-stat. Sane URL grammar (`/country/{iso}/indicator/{code}?date={range}&format=json`).
- **Bulk downloads**: per-indicator and per-database ZIP files (CSV / XML / Excel) at `data.worldbank.org` — useful for backfill, but the API is fine for incremental updates.

## Authentication and rate limits

- **No auth**. No API key, no registration, no OAuth.
- **No documented rate limit** in the help-desk articles. Community lore: a single client running ~5 RPS on a residential IP has never been throttled; bursts above ~30 RPS occasionally see 429s with a polite `Retry-After`.
- **Reasonable house rule for OPENGEM**: cap our adapter at 2 RPS sustained, 8-deep burst. We will publish that as the contract so contributors don't accidentally DOS the freebie.

## URL grammar that matters

- `per_page` defaults to 50; in practice the server accepts at least `per_page=20000`, which is the documented WDI year span. **Always paginate explicitly** — the default has bitten every naive adapter that ever existed.
- Date forms: annual (`2000`), quarterly (`2013Q1`), monthly (`2012M01`), ranges with colon (`2000:2024`), and `YTD:2013`. WDI is annual; quarterly/monthly fields are honored where indicators carry sub-annual series (rare).
- **Multi-indicator queries**: up to 60 indicators per call via semicolon separation. This collapses what would be 60 round trips into one. Critical for keeping daily-fresh dashboards inside any rate budget.
- URL length cap: 4,000 chars total, 1,500 between slashes. The 60-indicator ceiling is the practical limit; longer codes break the per-slash cap.
- Country codes: ISO-2 (lowercase per docs; ISO-3 also accepted in practice). `all` returns the full panel.

## Rate-limit math for OPENGEM

Dashboard freshness target: WDI is annual, so "daily-fresh" really means *check-if-revised* once per day per indicator family.

- Useful subset (see below): ~150 indicators × 220 economies = 33,000 cells.
- With 60-indicator batching and 1 call per economy, ~3 calls per country, ~660 calls total per refresh.
- At 2 RPS that is ~5.5 minutes of wall clock. **Negligible.**
- Even a full WDI catalog scrape — 1,400 indicators × 220 countries ≈ 24 batched calls × 220 = 5,280 calls — completes in ~45 minutes at 2 RPS. Run weekly, not daily.

## Useful subset for OPENGEM (the ~150 that earn their slot)

Block I needs national-accounts spine, prices, labor, fiscal, external, money/credit, and a few human-development covariates for narrative context. Concretely:

| Family | WDI codes (sample) | Why we want it |
|---|---|---|
| National accounts | `NY.GDP.MKTP.CD`, `NY.GDP.MKTP.KD.ZG`, `NY.GDP.PCAP.CD`, `NE.CON.PRVT.ZS`, `NE.EXP.GNFS.ZS`, `NE.IMP.GNFS.ZS` | The GDP spine for every Tier-T country that has no Tier-V vintage archive. |
| Prices | `FP.CPI.TOTL.ZG`, `FP.CPI.TOTL` | Cross-country inflation panel (annual; monthly via national sources). |
| Labor | `SL.UEM.TOTL.ZS`, `SL.TLF.ACTI.ZS`, `SL.EMP.WORK.ZS` | Unemployment + participation for places where ILO LFS is the only game. |
| Fiscal | `GC.DOD.TOTL.GD.ZS`, `GC.TAX.TOTL.GD.ZS`, `GC.NLD.TOTL.GD.ZS` | Debt-to-GDP, primary balance proxies. |
| External | `BN.CAB.XOKA.GD.ZS`, `BX.KLT.DINV.WD.GD.ZS`, `NY.GNS.ICTR.ZS` | CA balance, FDI, savings. |
| Money/credit | `FS.AST.PRVT.GD.ZS`, `FM.LBL.BMNY.GD.ZS`, `FR.INR.RINR` | Private credit, broad money, real rate. |
| Demographics | `SP.POP.TOTL`, `SP.POP.GROW`, `SP.URB.TOTL.IN.ZS` | Long-run denominator for everything. |
| Energy | `EG.USE.PCAP.KG.OE`, `EG.ELC.RNEW.ZS` | Energy intensity & renewable share for climate-macro overlays. |
| Trade composition | `TX.VAL.MRCH.CD.WT`, `TG.VAL.TOTL.GD.ZS` | Goods trade for sanctions/scenario work. |

Estimated final shortlist: 120–180 codes. Treat this as a `wdi_pinned_codes.yaml` in the adapter and let the dashboard derive everything else lazily.

## Vintage truth — the trap

The headline use of WDI in OPENGEM is **Tier-T (tracked-only) coverage** — places where we cannot defend a true real-time vintage archive. WDI itself does maintain a **WDI Database Archives** at DataBank, with historical releases back to 1989 (the print-edition era). Three subtleties:

1. The archive is **release-stamped**, not revision-triangle. Each annual release replaces the previous one wholesale, so we can reconstruct *what the world thought GDP-2010 was, as of WDI-2015* — but not *as of any non-release date*.
2. **Series codes are reused across base-year changes**. `NY.GDP.MKTP.KD` (real GDP, current base year) has silently shifted base years across 1987 → 1995 → 2000 → 2005 → 2010 → 2015. A naive cross-vintage diff conflates revision and rebasing. Adapter must record the base-year metadata each vintage carries.
3. **Discontinued indicators** persist in the archive. The current WDI metadata is the only metadata that comes back from the live API — so the archive is a separate ingestion path, not "ask the same API with a date in the past."

For OPENGEM this means: WDI ingestion has **two adapters** — live (`api.worldbank.org/v2`) for current values, and an archive ingestor that walks DataBank ZIPs once per WDI release (April + Sept-ish). The archive ingest is the seed for any "WDI-2015 thought GDP-2010 was X" reconstructions, and is the right denominator for backtesting against published WEO forecasts (which were drafted against contemporaneous WDI).

## License

The World Bank Open Data license is **CC-BY-4.0** for most data (some series carry IMF or partner-org restrictions; metadata flag `licensetype` exposes this per indicator). For OPENGEM's CC-BY-4.0 stance, this is a clean GREEN with an attribution-string-per-cell obligation we already plan to ship in the provenance schema.

## Fit-for-OPENGEM verdict — **ADOPT-NOW**

- Closes the multi-country coverage gap that ORDRA leaves open (ORDRA stops short of low-income economies; WDI does not).
- Backfills Tier-T countries where vintage archives don't exist.
- Zero auth complexity, license is GREEN, rate-limit math is trivial.
- Should be the **fourth multi-country adapter** after ORDRA / BIS / IMF SDMX.

**Adapter design notes**:

- One Python package `opengem-data-wb` (mirrors `opengem-data-ordra` layout).
- Pinned indicator catalog in `wb_catalog.yaml` (~150 codes), regenerated quarterly via a curation script.
- Two fetch paths: `fetch_live(indicator, country, date_range)` and `fetch_archive(release, indicator)` (the latter reads DataBank ZIPs from a mirror we control, since they aren't directly URL-stable).
- Provenance: every Observation records `source=wb`, `database=wdi`, `release_id=YYYY-MM`, `indicator=...`, `licensetype=...`.

## Trap log

- **Base-year drift on `NY.GDP.MKTP.KD`** — adapter must capture base-year metadata each vintage.
- **`per_page` default 50** — silent truncation if you forget.
- **Mixed licenses** — some series are IMF-sourced and carry IMF redistribution clauses even though the World Bank serves them. Check `licensetype` on every indicator.
- **Discontinued indicators** — archive ingest is a separate path.
- **Country aggregates** mix with country rows in the default response — filter on the `region.id` to exclude `WLD`, `EAS`, etc., when you want sovereigns only.

## Related

- [[L047]] — IMF SDMX (parallel coverage; complementary)
- [[L048]] — OECD endpoints beyond ORDRA
- [[R02]] (existing) — vintage coverage; WDI archive is the Tier-T seed
- [[R09]] (existing) — FRED-substitution; WDI is the multi-country analog
