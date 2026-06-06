# L056 — Commodity prices: WB Pink Sheet + IMF PCPS as the GREEN spine

**Loop**: 056 / 300
**Phase**: 1 — Open-source landscape survey (data sources)
**Date**: 2026-06-06
**Verdict**: **ADOPT-NOW World Bank Pink Sheet + IMF PCPS** as the headline commodity-price layer. **CITE-ONLY BCOM / CRB / S&P GSCI** indices (proprietary; we publish the components, not the index licensed name). **SKIP LME** for Block I.

---

## One-line take

The two best open commodity-price datasets in existence — the **World Bank Pink Sheet** and the **IMF Primary Commodity Price System (PCPS)** — are both monthly, both GREEN-licensed, both cover all major energy / metals / soft-commodity prices, and **partially overlap but don't perfectly agree** because they use different reference-price methodologies. OPENGEM should ingest both, publish both side-by-side, and let users see the methodology delta — exactly the "publish your sources, name your disagreements" pattern.

## Two products, same use case, complementary

| Aspect | World Bank Pink Sheet | IMF PCPS |
|---|---|---|
| Update cadence | Monthly, first week | Monthly, first full week |
| Coverage | ~70 commodities + a handful of weighted indices | ~70 commodities + ~100 price indices |
| Reference price methodology | Trade-weighted spot at named hub (e.g., Henry Hub for natgas, Dubai/Brent/WTI for oil) | Mixed: spot, futures, indicator prices; documented per commodity |
| File formats | Excel (.xlsx historical), PDF (monthly bulletin) | SDMX API (live), Excel historical |
| Series naming | World Bank short codes (e.g., `iCRUDE_BRENT`) | IMF commodity codes |
| Vintage | Historical Excel preserves prior releases | SDMX serves latest revised |
| License | World Bank Terms — CC-BY-style on the data layer; **GREEN with attribution** | IMF Terms — **GREEN with attribution + non-endorsement** |
| History | 1960-current (annual), 1979-current (monthly for most series) | 1992-current |

## World Bank Pink Sheet

- **File URLs**:
  - `https://thedocs.worldbank.org/.../CMO-Historical-Data-Monthly.xlsx` — monthly historical, every commodity, back to 1960 annual / 1979 monthly.
  - `https://thedocs.worldbank.org/.../CMO-Historical-Data-Annual.xlsx` — annual.
  - `https://thedocs.worldbank.org/.../CMO-Pink-Sheet-{Month}-{Year}.pdf` — the named monthly publication.
- **Update cadence**: monthly, first week. April + October editions also serve as the inputs to the World Bank's Commodity Markets Outlook (CMO).
- **API style**: no live API. Static Excel files at version-stamped URLs. The hash in the URL path changes per release year — needs a small URL-discovery scraper run monthly.
- **Auth**: none.
- **Rate limits**: none (file download).
- **Commodities covered**: energy (crude oil — Brent + Dubai + WTI, natural gas — US + EU + Japan, coal, propane), agriculture (wheat, maize, rice, soybeans, sugar, coffee, cocoa, palm oil, cotton, rubber, tobacco), metals (aluminum, copper, zinc, nickel, lead, tin, iron ore, gold, silver, platinum), fertilizers (urea, DAP, phosphate rock, potash).
- **License**: World Bank Open Data Terms — **CC-BY-style, GREEN**.
- **History depth**: deepest of any free commodity dataset. The Excel sheets carry annual data back to 1960 for many commodities.

## IMF PCPS (Primary Commodity Price System)

- **API endpoint**: SDMX 3.0 via `https://api.imf.org/external/sdmx/3.0/data/dataflow/IMF.RES/PCPS/~/{key}` (rides the same adapter as L047).
- **Update cadence**: monthly, first full week.
- **Coverage**: ~68 individual commodities + ~100 weighted price indices (PCPS index, energy index, food index, agricultural raw materials index, metals index, fuel index, beverages index, etc.). Currently weighted by global import share with 5-year rebasing.
- **Series resolution**: monthly + quarterly + annual since 1992.
- **License**: **IMF terms — GREEN with attribution + non-endorsement**.
- **History depth**: shallower than Pink Sheet (1992 vs 1960) but with the weighted-index family that Pink Sheet doesn't provide.

## CRB / BCOM / S&P GSCI / Rogers (proprietary commodity indices)

These are **proprietary financial-industry products**. Index methodology is published (BCOM uses 24 commodity futures, 6 sectors, world-production + liquidity weights; CRB uses 19 commodity futures). The *values* of the indices are licensed by FTSE-Russell (for CRB) and Bloomberg (for BCOM).

For OPENGEM:
- We do **NOT** publish CRB / BCOM values directly. License-incompatible.
- We **MAY** publish the **components** (the 19 or 24 commodity futures prices that go into the index) from public sources. The component prices themselves are public.
- We **MAY** publish an OPENGEM-branded weighted commodity index using the public methodology weights, as long as we don't call it CRB or BCOM.

The right product call: build an `OPENGEM-Commodity-Index` derived from World Bank Pink Sheet weights or our own methodology, and document the methodology openly. This is on-brand for OPENGEM's "open methodology" thesis. CRB / BCOM go in the comparator overlay only.

## LME (London Metal Exchange)

- **What it offers**: official LME settlement prices for aluminum, copper, zinc, nickel, lead, tin, plus more recently cobalt, lithium.
- **License**: LME settlement prices are licensed by LME's commercial arm. **The 30-minute-delayed prices are available free; real-time prices require LME data subscription.**
- **For OPENGEM**: World Bank Pink Sheet already publishes monthly LME-derived prices in the "metals" section under WB's own attribution. **SKIP direct LME ingest for Block I; the Pink Sheet is sufficient.**

## Other relevant free sources

- **EIA petroleum weekly** (L053) for high-frequency crude/gasoline/distillate.
- **CME settlement** futures prices via the CME's data services (delayed quotes free).
- **USDA NASS** for US agricultural commodity prices, planted acres, production estimates.
- **FAO FAOSTAT** for agricultural production by country (annual; not prices).
- **Kitco / Goldhub / silverinstitute** for precious metals (some free).

## Rate-limit math for OPENGEM

**WB Pink Sheet**:
- 2 Excel downloads + 1 PDF per month. URL-discovery scrape on the World Bank docs site once per month.
- Total: 4 HTTP calls/month. Trivial.

**IMF PCPS** (rides existing IMF SDMX adapter):
- 1 SDMX call per month for all commodities × all frequencies. Trivial.

**Total commodity adapter cost**: <10 calls/month.

## Vintage truth

- **Pink Sheet**: each monthly Excel release replaces the prior; no native vintage archive at version-stamped URLs. Adapter snapshots each pull.
- **IMF PCPS**: same forward-only pattern via SDMX.

Where commodities differ from macro data: revisions are **rare** because price series are observed market prices, not estimated. Methodology changes (new reference contract, switch from Brent to Dubai weighting) happen, but the historical values themselves rarely move. **Commodity vintage is therefore cheaper to maintain than macro vintage.**

## Fit-for-OPENGEM verdict

- **ADOPT-NOW**: WB Pink Sheet + IMF PCPS — both monthly, both GREEN.
- **ADOPT-BLOCK-II**: USDA NASS for US ag detail, FAO FAOSTAT for global production.
- **CITE-ONLY**: BCOM, CRB, S&P GSCI (proprietary; cite as comparators).
- **SKIP**: LME direct, paid Argus / Platts / Fastmarkets, Bloomberg commodity terminal.

**Adapter design notes**:

- New package `opengem-data-commodities`.
- Submodule 1: `WBPinkSheetAdapter` — monthly URL-discovery scraper hits `thedocs.worldbank.org/en/doc/all?qterm=pink+sheet` to find the current release ZIP, downloads + parses the Excel.
- Submodule 2: `IMFPCPSAdapter` — extends `opengem-data-imf` SDMX client with `fetch_pcps(commodity, frequency)`.
- Each Observation records `source=wb_pink_sheet|imf_pcps`, `release_id=...`, `methodology=...`.

## The methodology-delta product feature

A unique OPENGEM artifact: a chart that shows **Brent crude price per month** from both sources overlaid. The lines mostly agree but diverge by ~1-2% in some months (different averaging windows, holiday calendars, currency conversions). This is exactly the kind of "publish your sources, show the disagreement" pattern that builds OPENGEM's credibility brand.

For commodities where the two sources use *different reference prices* (e.g., WB uses spot Brent FOB, IMF uses average of Brent + Dubai + WTI for "crude oil"), the divergence is structural. The chart tooltip should explain why, citing both methodology documents.

## Trap log

- **Pink Sheet URL hash changes per year** — the path `0050012026` etc. is a per-year unique identifier. Adapter must discover the current path each year.
- **WB Pink Sheet Excel column structure occasionally changes** when commodities get added or methodology updates. Validation step required.
- **IMF PCPS commodity codes ≠ WB commodity codes**. Adapter must maintain a crosswalk for the cross-source comparison.
- **Quoting convention varies by commodity** — oil in $/barrel, gas in $/MMBtu (US) vs $/MWh (EU) vs $/MMBtu (Asia), metals in $/MT vs $/lb, grains in $/MT. Adapter should normalize at the column-name layer, not the values layer (preserve original units in the Observation, expose a normalized view).
- **CRB and BCOM are NOT free to redistribute.** Even citing the index value requires a licensed source. Show methodology and components freely; cite the index value with a "data from Bloomberg/FTSE" footnote and link only.
- **LME official prices have a 30-min delay before becoming free**, and even then redistribution rules apply. Don't ingest LME directly.
- **Some Pink Sheet series are LME-sourced, some are WB-collected.** Adapter should preserve the source provenance per commodity, not just per dataset.

## Related

- [[L053]] — Energy (oil, gas dominate Pink Sheet)
- [[L055]] — Shipping (chokepoint closures move oil and grain)
- [[L054]] — Climate (drought drives soft commodities)
- [[R06]] (existing) — wider information surface
