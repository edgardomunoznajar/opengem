# L051 — UN Comtrade + CEPII BACI: bilateral trade at HS6, two paths in

**Loop**: 051 / 300
**Phase**: 1 — Open-source landscape survey (data sources)
**Date**: 2026-06-06
**Verdict**: **ADOPT-NOW BACI** (annual HS6 panel, ready-cleaned, free, GREEN license), **ADOPT-BLOCK-II UN Comtrade** (live monthly cadence, free tier marginal, Premium gated).

---

## One-line take

For OPENGEM the right move is to **eat the BACI annual snapshot as the baseline bilateral-trade panel** (CEPII has done the data-cleaning we don't want to redo), and **only call live UN Comtrade for current-year monthly nowcasts** where the BACI lag (12–18 months) is too long. The two together give us a HS6-by-exporter-by-importer-by-year panel back to 1995 — the global trade panel everyone wants but nobody has open.

## Two products, one data lineage

UN Comtrade is the **raw filing**. Every customs office of every reporting country posts its bilateral trade data to the UN. The UN publishes it. The data is famously dirty: reporter and partner numbers disagree by 10–30% on most country-pairs; missing reporters create asymmetric panels; the HS classification rebases every 5 years.

CEPII's **BACI** is the *reconciled, cleaned, harmonized* derivative. BACI takes Comtrade's mirror flows, applies a reconciliation algorithm (gravity-based, weight transport-cost asymmetries to reconstruct the implied true flow), and ships an annual CSV-per-year for every HS revision (1992 / 1996 / 2002 / 2007 / 2012 / 2017 / 2022).

For OPENGEM the data-engineering judgment is clean: **use BACI for everything except current-year nowcasting.**

## UN Comtrade (the raw source)

- **Base URL**: `https://comtradeapi.un.org/` (the new Comtrade Plus API; older `comtrade.un.org` legacy interface is being phased out).
- **API style**: REST. JSON responses.
- **Auth**: requires registration + free subscription key (`Ocp-Apim-Subscription-Key` header). Free tier exists; Premium tiers gated by paid subscription via `shop.un.org/databases`.
- **Rate limits (free tier)**: 500 calls per day with a registered key; up to 100,000 records per call (i.e., per HS6 × reporter × partner × year combination, returns up to 100k rows). Preview functions (no key) limited to 500 records.
- **Rate limits (premium)**: ~5 calls/sec per user, no daily cap. Async batch up to 2.5M records per batch.
- **Premium pricing**: not publicly listed on the developer portal; quotes via `subscriptions@un.org`. Past public references put institutional site licenses at **mid-four to low-five-figures per year** (USD). Individual research subscriptions are notably cheaper but still gated.
- **Data coverage**: 200+ reporters × 200+ partners × 5,400 HS6 codes × monthly (since ~2010 for most reporters; annual back to 1962 for the OG dataset).
- **Update cadence**: monthly, with new monthly observations posting irregularly (3–12 weeks after reference period depending on reporter).
- **License**: UN Comtrade data licensed under the UN's specific terms; non-commercial use generally permitted, commercial redistribution prohibited without licensing. **YELLOW — usable in OPENGEM's free-tier dashboard but cannot be re-exported as a bulk dataset for download.**

## CEPII BACI (the cleaned derivative)

- **Base URL**: `https://www.cepii.fr/DATA_DOWNLOAD/baci/data/` (file URLs follow `BACI_HS{revision}_Y{year}_V{YYYYMM}.csv` pattern, zipped per HS-revision-and-release).
- **API style**: static CSV files (no API; bulk only).
- **Auth**: free registration to download; no API key per call.
- **Rate limits**: none (it's static file download).
- **Update cadence**: **annual**, released in January (2025 release covered 2023 trade data; 2026 release in Jan covered 2024).
- **Coverage**: bilateral trade at HS6 by reporter × partner × HS6 × year. **Strictly positive flows only** (zero or NA flows not stored). Values in thousands USD, quantities in metric tons.
- **History**: from 1995 (HS92 revision) through latest release minus 18 months. Each HS revision starts in its base year (HS22 from 2022 forward, etc.).
- **License**: **Etalab Open Licence 2.0** — equivalent to CC-BY 2.0 / Open Government Licence. **GREEN — fully redistributable with attribution.**

## Coverage delta

The biggest functional difference: **BACI is reconciled (the trade-asymmetry problem is solved), Comtrade is raw**. For any OPENGEM chart that says "China exports to US in 2023 were $X", BACI gives a single defensible number, Comtrade gives you two (US-as-reporter and China-as-reporter) that don't agree.

Second difference: **BACI is annual, Comtrade is monthly**. For nowcasting and event-detection (sanctions hit → trade flow collapse, port closure → import surge somewhere else), the monthly cadence matters; annual is too lagged.

Third: **license**. BACI is GREEN and re-exportable. Comtrade is YELLOW and binding.

## Rate-limit math for OPENGEM

**BACI** (no rate limit math required; static download):
- Initial bulk: 7 HS revisions × ~30 yearly files each, ~250 MB compressed total. One-shot at adapter bootstrap, then 1 release/year refresh.
- Daily steady-state: 0 calls.

**UN Comtrade** (free tier, 500 calls/day):
- Daily nowcast target: current-year monthly trade for top-30 reporters × top-30 partners on top-50 HS chapters. One call per (reporter, year-to-date, period=this month, frequency=M) returns up to 100k rows (more than enough for ~50 HS chapter × 30 partners ≈ 1,500 rows).
- Daily ceiling at 30 reporter calls: 30 calls/day. Well under the 500/day limit.
- Monthly steady-state: 30 calls × 30 days = 900 calls/month. Under the per-day cap.
- Backfill: not needed — BACI handles history.

The combination fits the free Comtrade tier comfortably.

## Vintage truth

Trade data has a peculiar revision pattern: monthly figures get heavily revised in the first 6 months, lightly revised for years, occasionally revised in big retrospective reclassifications (e.g., HS classification rebase).

- **BACI** stamps its release version (`V202601` etc.) in the filename, giving us a clean cross-release vintage triangle. We ingest each annual BACI release as its own vintage.
- **UN Comtrade** does not version-stamp. The recommended OPENGEM pattern: snapshot each monthly nowcast call into the vintage store keyed by retrieval date.

## Fit-for-OPENGEM verdict

- **ADOPT-NOW**: BACI annual ingest. This is the baseline bilateral trade panel for the dashboard. Lightweight, GREEN, reconciled.
- **ADOPT-BLOCK-II**: UN Comtrade monthly nowcast on a curated top-30 × top-30 × top-50 HS chapter slice. Lives on free tier. Adds 6–18 month freshness over BACI.
- **CITE-ONLY**: Comtrade Premium bulk subscription. Track the pricing in case a sovereign-fund-LP customer demands current-month full-resolution; until then, free tier + BACI baseline is sufficient.
- **SKIP**: nothing.

**Adapter design notes**:

- New package `opengem-data-trade` covering both sources behind a single API.
- `fetch_baci_panel(year, hs_revision)` — downloads from CEPII URL pattern, caches to local CSV-Parquet.
- `fetch_comtrade_monthly(reporter, period, frequency="M")` — calls `comtradeapi.un.org/data/v1/get/{reporter}/{period}/HS` with the subscription key.
- `subscription_key` ingested from `OPENGEM_COMTRADE_KEY` env var; adapter degrades gracefully (Comtrade nowcast disabled, BACI baseline still works) when key is absent.
- Each Observation records `source=baci` or `source=comtrade`, `release_version=V202601` (BACI) or `retrieved_at=...` (Comtrade).

## License trap

**Critical:** the UN Comtrade license prohibits redistributing the *raw data* as a downloadable bulk. OPENGEM can serve Comtrade-derived **charts, aggregates, and dashboard cells**, but cannot publish a "download Comtrade as parquet" button on our `/data` Datasette mount.

BACI is GREEN — we can serve the raw BACI files via Datasette without restriction (with attribution).

The clean pattern: **Datasette `/data` mount exposes BACI raw** + **API endpoints expose Comtrade-derived aggregates** but **no raw Comtrade dump**. Adapter must enforce this at the database-view layer.

## Trap log

- **HS revision rebasing** — every 5 years the HS classification changes. A naive cross-decade time series at HS6 has gaps. BACI provides per-revision files; OPENGEM should treat HS17 series and HS22 series as separate logical channels, with a curated mapping for chart-level aggregation.
- **Mirror-flow asymmetry** — for any direct UN Comtrade pull, US-says-it-exported-X and China-says-it-imported-Y disagree by 5–30%. We must label which reporter is the source in every cell.
- **BACI excludes zero flows** — "Russia exported pasta to USA in 2023 = NA" doesn't mean zero, it means the row wasn't in the file. For sanctions narratives this matters: a flow that *went to zero* is invisible in BACI; we have to infer from prior years' presence and current absence.
- **Comtrade "Plus" vs legacy endpoint** — the old `comtrade.un.org/api/get` endpoint still works but is sunsetting. New adapter must target `comtradeapi.un.org/data/v1/get/...`.
- **Top-30 partner cap on free tier** — Comtrade limits free-tier responses to top-30 partners. If you want the long-tail (small island exporters), you need Premium.

## Related

- [[L046]] — World Bank Indicators (WITS sits on top of Comtrade; lower-resolution)
- [[L047]] — IMF DOTS (same data, different reconciliation; see L052)
- [[L052]] — IMF DOTS vs Comtrade comparison
- [[R06]] (existing) — wider information surface
