# L052 — IMF DOTS vs UN Comtrade: when to use which

**Loop**: 052 / 300
**Phase**: 1 — Open-source landscape survey (data sources)
**Date**: 2026-06-06
**Verdict**: **ADOPT-NOW IMF DOTS as the headline bilateral-trade panel** alongside BACI. UN Comtrade remains the granular monthly nowcast source. The three together give OPENGEM a complete bilateral trade stack.

---

## One-line take

**DOTS = monthly bilateral trade by partner economy at the headline value level (no product detail), for 210 economies, with IMF-estimated values where official data are missing.** **Comtrade = monthly bilateral trade by partner economy *and HS6 product detail*, for ~170 reporters, with raw values and asymmetry gaps.** **BACI = annual bilateral trade at HS6 with mirror-flow reconciliation, for the cleanest cross-section panel.** For OPENGEM's main "trade and capital flows" page, we want **DOTS for the headline charts** (because it covers more countries, monthly, and is value-level which is what the dashboard wants), with **Comtrade-derived HS6 tiles** for drilldown and **BACI for the annual historical baseline**.

## The DOTS proposition

DOTS is the IMF Statistics Department's bilateral trade product. The official rebrand (as of 2025) is **"International Trade in Goods (by partner country) — IMTS, formerly DOTS"** in the IMF Data Portal. SDMX dataflow code in the new API: `IMTS` (or `DOT` in legacy paths).

- **Base URL**: via IMF SDMX 3.0 API at `https://api.imf.org/external/sdmx/3.0/data/dataflow/IMF.STA/IMTS/~/{key}`.
- **Coverage**: 210 economies (broadest of any open trade dataset).
- **Granularity**: bilateral, by partner economy, at the **headline goods value level** — no HS / SITC product detail. Just "country X's exports to country Y this month, in USD."
- **Frequency**: monthly + quarterly + annual.
- **Cadence**: T+85 days for the full monthly release (i.e., March 2026 data lands by mid-June 2026). 5+ days faster than the pre-2018 methodology.
- **Methodology**: For ~90% of monthly cells, DOTS uses **official monthly trade statistics reported directly to IMF**. For the remaining 10% (smaller economies, slower reporters), DOTS uses the **Cholette-Dagum (2006) regression-based benchmarking model** to estimate monthly bilateral flows consistent with annual official data. The IMF 2018 WP/18/16 documents this methodology.
- **Asymmetry handling**: **DOTS does NOT reconcile mirror-flow asymmetries.** Reporter-X-says-it-exported-$100 to Y and Y-says-it-imported-$110 from X both go into the DOTS panel as separately-published cells. Consumers have to choose which side they trust (typically the importer side because importers track tariffs and so collect more carefully).
- **License**: standard IMF data terms — GREEN with attribution + no-resale + non-endorsement.

## The decision table

| Use case | Right source | Why |
|---|---|---|
| "Monthly bilateral headline trade flow for the dashboard ticker" | **DOTS** | Monthly cadence, 210 economies, value level is what dashboards show, T+85d freshness |
| "HS6 product-level drilldown (e.g., semiconductors, oil, grain)" | **Comtrade** | Only source with HS6 granularity at monthly cadence |
| "Annual reconciled bilateral panel for backtesting" | **BACI** | Only source with proper mirror-flow reconciliation; clean and stable |
| "Recent sanctions-narrative: did trade collapse this quarter?" | **DOTS + Comtrade overlay** | DOTS gets you the value drop; Comtrade tells you which HS chapter dropped |
| "Long-run pre-2000 bilateral trade history" | **DOTS** | DOTS goes back to 1948 for many country pairs; Comtrade post-1962; BACI only post-1995 |
| "Trade in services (not goods)" | None of the above | Use the new CEPR bilateral trade-in-services database; DOTS/Comtrade/BACI are all goods-only |
| "World total exports / imports" | **DOTS aggregate** | DOTS publishes pre-aggregated world rollups; saves the consumer from summing |

## DOTS vs Comtrade — the asymmetric ranges

- **DOTS coverage exceeds Comtrade coverage** at the country count (210 vs ~170 reporters). DOTS uses IMF's broader country reporting universe + estimates for non-reporters.
- **Comtrade coverage exceeds DOTS coverage** at the product detail (5,400 HS6 codes vs 0).
- **DOTS freshness exceeds Comtrade freshness** for many slow reporters (DOTS estimates fill the gap with Cholette-Dagum benchmarking; Comtrade just shows NA until the reporter files).
- **Comtrade revision stability exceeds DOTS revision stability** for recent months — DOTS estimates revise as the underlying official data come in; Comtrade just shows the official data the reporter filed.

## DOTS rate-limit math for OPENGEM

This rides on the same `opengem-data-imf` adapter as L047, so the call budget is already accounted for there. Specifically:

- **DOTS monthly headline sweep**: 1 SDMX call per reporter (or 1 wildcarded call returning all 210 reporters × all 210 partners for a given month if the response cap permits). Estimate 5–10 calls per month at the wildcarded level, ~210 calls per month at the per-reporter level.
- **DOTS annual rollup**: 1 call per year for the whole world panel.

Total monthly steady-state cost: <10 calls if we use wildcarding aggressively. At 2 RPS budget that's seconds.

## Vintage truth

DOTS revisions are heavy in the first 3–6 months as official monthly reports come in and replace Cholette-Dagum estimates. The IMF doesn't expose a vintage archive — the SDMX endpoint serves only the latest.

OPENGEM compromise: snapshot the DOTS panel into our vintage store on each refresh, keyed by retrieval date. This gives us a forward-only vintage triangle starting at adapter bootstrap. Combined with BACI's release-stamped annual snapshots, we get a defensible "what did we think 2024 bilateral trade was, as of 2024-12 vs 2025-06 vs 2026-01" timeline for any country pair.

## Fit-for-OPENGEM verdict

- **ADOPT-NOW**: DOTS / IMTS via the existing `opengem-data-imf` SDMX adapter. Top-level bilateral-trade panel; default chart source.
- **ADOPT-BLOCK-II**: nothing new — DOTS subsumes the headline use case.
- **CITE-ONLY**: nothing.
- **SKIP**: nothing.

**Adapter design notes**:

- Add `fetch_dots(reporter, partner, period, frequency)` to `opengem-data-imf` (the IMF SDMX adapter from L047).
- Use the new `IMTS` dataflow code; do not hardcode legacy `DOT`.
- Default chart: dashboard shows the monthly DOTS bilateral value series with a `methodology=cholette_dagum_estimated|official_reported` flag so the user can see when they're looking at an estimate vs a hard report.
- Provenance: every Observation records `source=imf`, `dataflow=IMTS`, `methodology_flag=...`, `imf_attribution=...`.

## The "three-source coherence" page

A unique OPENGEM artifact opportunity: a per-country-pair page that **shows DOTS / Comtrade / BACI side-by-side** for the same flow, highlights the asymmetries (DOTS reporter-says vs partner-says; Comtrade raw asymmetry; BACI reconciled value), and lets the user understand the data lineage. This is the "publish your sources, name your disagreements" pattern applied to trade data. No other open dashboard does this.

This is a Block I product item worth flagging — it differentiates OPENGEM from the "DOTS chart only" patterns of OECD Data Explorer or World Bank WITS.

## Trap log

- **DOTS is value-only, not volume or product**. Charts that say "the US imported X tons of steel from Korea this month" cannot come from DOTS — that requires Comtrade.
- **DOTS estimates carry an OBS_STATUS flag** in the SDMX response. Adapter must surface this; consumers downstream must show it on the chart.
- **The "IMTS" rebrand from "DOTS" happened mid-2024** and the legacy DOT dataflow still works but is being phased out. Pin against `IMTS` going forward.
- **DOTS world rollups can double-count** if you naively sum reporter exports + partner imports. Use the IMF's published aggregates, not your own sum.
- **Old DOTS Yearbook PDFs (pre-2000)** have data not in the SDMX endpoint. For deep historical work, ingestion needs to walk the PDF archives — not a Block I item.
- **DOT and IMTS are not 1:1 schema-compatible**. IMTS adds explicit OBS_STATUS dimensions and renames a few attributes. Adapter must handle the schema diff or downstream pivots will silently lose flags.

## Related

- [[L047]] — IMF SDMX (DOTS lives on this adapter)
- [[L051]] — UN Comtrade + BACI (the complementary HS6 sources)
- [[L055]] — Shipping (PortWatch correlates with DOTS at the headline level)
- [[R06]] (existing) — wider information surface
