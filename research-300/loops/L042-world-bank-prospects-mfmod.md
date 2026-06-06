# L042 — World Bank: MFMod / Prospects / Macro Poverty Outlook — APIs, code, dashboards

**Loop**: 042 / 300
**Phase**: 1 — Open-source landscape survey (World Bank)
**Date**: 2026-06-06
**OPENGEM adoption grade**: **A for data adoption (wbgapi + Data360 + GEP + MPO under CC-BY 4.0), B for MFMod-ModelFlow as scenario reference, C for direct model adoption**

---

## TL;DR

The World Bank's posture is **the gold standard for open macroeconomic data and the surprising near-gold standard for open macroeconomic models**:

1. **All World Bank data is CC-BY 4.0** (with attribution; commercial use allowed). This is **the most permissive license among major macroeconomic data providers** — strictly better than IMF, ECB, FRED, even most central banks.

2. **Data360** (`data360.worldbank.org`) is the new umbrella portal as of 2024–25. SDMX-compatible API, an MCP server for LLM access, third-party-app catalog. The Data360 API ramps up; the older Indicators API at `api.worldbank.org` still works and is still the workhorse for series-level access.

3. **`tgherzog/wbgapi`** (MIT, 175 stars) is the canonical Python client. Covers WDI, GEP (Global Economic Prospects), ICP, multiple databases. No API key required. Auto-chunks large requests. **Adopt as `opengem-data-wb` dependency.**

4. **`worldbank/MFMod-ModelFlow`** (CC0 public domain) is the World Bank's open-sourced macro-fiscal models, ported to the `ModelFlow` Python framework. Covers many developing countries. **First-of-its-kind from the World Bank** — they're explicitly bringing what was a commercial-grade IBM-style modeling system to the open-source world. Worth a deep look for Block II.

5. **Global Economic Prospects (GEP)** is the World Bank's forecast publication, twice-annually (Jan + June), with three-year detailed forecasts for ~150+ countries. Forecasts plus historical revisions are downloadable in the Data Catalog. **CC-BY 4.0.** This is **a free, full-coverage, vintaged alternative to IMF WEO** that we should add as a parallel consensus overlay on the dashboard.

6. **Macro Poverty Outlook (MPO)** is the country-by-country MPO publication for ~150 developing countries, twice-annually (Spring + Annual Meetings). Goes beyond WEO in covering poverty-rate forecasts, fiscal indicators, sectoral breakdowns. Downloadable via Data360.

The "Iceberg" reference in the queue was a typo / misremembered name; the actual World Bank suite is **GEP + MPO + MFMod + Data360**. None of them is called "Iceberg."

**The biggest win**: the World Bank's `wbgapi` + CC-BY 4.0 data combination gives OPENGEM **clean, redistributable, machine-readable forecast vintages** that we can use for the consensus overlay AND publish derived series of, with attribution and no licensing concerns. This is *the* dataset to lean on.

## wbgapi adapter detail

```python
import wbgapi as wb

# Default db=2 is WDI; explicitly switch for GEP
wb.db = 5  # Global Economic Prospects

# Real GDP growth forecasts for India, all available years
forecasts = wb.data.DataFrame(
    "NYGDPMKTPKDZ",  # Real GDP growth, %
    ["IND"],
    time=range(2020, 2030),
    db=5,
)
```

The package is MIT, 175 stars, maintained by Tim Herzog (World Bank Data team). Auto-chunks requests > 50 series. No API key. Adequate for our adapter pattern.

For `opengem-data-wb`, we wrap with:
- Vintage tagging (every GEP release date)
- Retry / backoff (already in `opengem-data-base`)
- Caching to `opengem-vintage` store
- Provenance stamping (DBcode, series, vintage)

Two weeks of effort to ship.

## Data360 — the new portal

Data360 launched 2024–25 as the unified World Bank data portal. Key elements:

- **Search across all WB datasets** (WDI, GEP, MPO, ICP, ASPIRE, education, etc.).
- **Dataset-level API** (`data360.worldbank.org/en/api`) with SDMX-compatible endpoints.
- **OpenAPI specs** at `worldbank/open-api-specs` on GitHub.
- **Data360 MCP server** at `worldbank/data360-mcp` — gives LLM agents structured access to indicators. Could be the model for how we ship our own MCP server!
- **5 focus areas** (Digital, Infrastructure, People, Planet, Prosperity) for thematic discovery.

For OPENGEM:
- Use the Indicators API at `api.worldbank.org` for series-level retrieval (the wbgapi backbone).
- Use the Data360 API for dataset-level discovery and for series we can't find in WDI.
- Read the Data360 MCP server code as inspiration for our own MCP server (L250).

## MFMod-ModelFlow — the open-sourced macro models

`worldbank/MFMod-ModelFlow`:

| Field | Value |
|---|---|
| License | **CC0-1.0 (public domain)** — the most permissive license possible |
| Language | Jupyter Notebook 78%, HTML 22% |
| Built on | `ModelFlow` open-source Python package (Goumilevski) |
| Coverage | Macro-structural models for developing countries (MFMod framework) |
| Maturity | 15 GitHub stars, 20 commits — small but real |

What it is: the World Bank's **Macroeconomic and Fiscal Model (MFMod)** framework, implemented in the `ModelFlow` Python package. MFMod is the central macro-modeling tool the WB has used for ~decade across its developing-country country teams. Each country team historically maintained its own MFMod variant. The open-sourcing initiative wraps these into Python and ships them with manuals.

For OPENGEM:

- **Pros**: CC0 license, Python-native, real models from a serious institution, developing-country coverage that complements our Tier-V US/euro-area bias.
- **Cons**: small footprint (15 stars suggests low usage outside the WB), Jupyter-notebook-first means it's not a clean library yet, `ModelFlow` itself is a smaller dependency we'd need to add.
- **Action**: explore in Block II. If MFMod has a reasonable wrapped model for, e.g., India / Brazil / Indonesia, we have a free macro-fiscal model for those countries we don't currently cover.

**Grade B**: not a backbone, but a real candidate for filling Tier-T (tracked-only) gaps with structural model output.

## Global Economic Prospects (GEP)

GEP is the World Bank's twice-annual flagship forecast publication. As of Jan 2026:

- **Coverage**: ~150+ countries, three-year point forecasts (current year + next 2) plus long-term scenarios.
- **Format**: PDF + downloadable Excel/CSV via Data Catalog + DataBank + Data360.
- **License**: CC-BY 4.0 — copy, modify, distribute, commercial use, only obligation is attribution.
- **Coverage variables**: real GDP growth, current account balance, gross fixed investment, government debt, current account balance, exchange rates (limited).
- **Vintage**: each release (January + June each year) is a distinct vintage. The Data Catalog preserves them.

For OPENGEM:
- **A-grade data adoption**. Use GEP forecasts as a parallel consensus overlay alongside IMF WEO on every country page (per L190).
- Pull vintages programmatically; tag each forecast with its release date.
- Include in V&V matrix as one of the named "consensus" benchmarks per the rev-C CONOPS (where "GDP-4Q not statistically worse than WEO/OECD EO" was the criterion — we expand "WEO/OECD EO" to "WEO/OECD EO/WB GEP").

## Macro Poverty Outlook (MPO)

MPO is the WB's country-by-country brief, twice-annually (Spring + Annual Meetings). Each country gets a 2-page note + forecasts for 3 years out:

- **Real GDP growth + components**
- **Inflation**
- **Fiscal indicators** (revenue, expenditure, deficit, debt)
- **Current account**
- **Poverty headcount ratio**
- **Sector-specific narratives**

The dataset (Data360 dataset `WB_MPO`) is downloadable, CC-BY 4.0.

For OPENGEM:
- **Particularly useful for our Tier-T (tracked-only) countries** where vintage data is sparse but published forecasts exist.
- Adds poverty-rate forecasts, which IMF WEO does not cover. This is a unique data layer.
- Sector-specific narratives are useful for the L1 narrative satellite work.

**B-grade data adoption**. Pull MPO via the API, surface on developing-country pages.

## Open-Code-Lite Picks

Beyond MFMod, the World Bank GitHub org publishes:

- `worldbank/open-api-specs` — OpenAPI specs for their APIs. Reference for adapter work.
- `worldbank/data360-mcp` — reference MCP server. **Read for inspiration for L250.**
- Various single-purpose data analysis repos (poverty maps, development indicators dashboards, climate-economic links).

None of these are forecasting backbones, but they're useful for adapter design.

## License compatibility

- CC-BY 4.0 (data): drop-in compatible with our CC-BY 4.0 data layer per OPENGEM's licensing scheme (Apache-2.0 code, CC-BY-4.0 data + docs + model cards). Cite the World Bank in series provenance. Done.
- CC0-1.0 (MFMod): most permissive. Drop-in.
- MIT (wbgapi): drop-in for code.

No license blocker anywhere.

## Risks

1. **Data360 API in beta.** Endpoints may change. Mitigation: maintain wbgapi-based adapter as the stable path; layer Data360 calls for discovery only.

2. **wbgapi bus factor.** One maintainer (tgherzog). Has been stable, but watch. Mitigation: snapshot known-good version; PR backwards-compat fixes if needed.

3. **GEP vintage preservation.** The Data Catalog preserves vintages but the workflow to extract a specific vintage as of a specific release date is manual. Mitigation: write a one-time GEP-vintage-scraper for our archive; maintain forward.

4. **MFMod-ModelFlow stability.** Small footprint; might not be maintained as developers transition. Mitigation: vendor if we adopt; treat as research code; not a critical path.

5. **MPO release timing** vs WEO release timing. The two publications come out at the same Spring/Annual meetings. Easy mistake: confuse vintages or double-count. Mitigation: clear vintage stamps with explicit release date + publication name in provenance.

## Verdict

- **Grade A** for the World Bank **data** layer (`wbgapi` + CC-BY 4.0 datasets + GEP + MPO + Data360). The most permissive macroeconomic data licensing in the world. We adopt without reservation.
- **Grade B** for `MFMod-ModelFlow` as a Block II Tier-T model-fill option for developing countries.
- **Grade A** for the conceptual pattern of "open data + open code + permissive license" — the World Bank shows what's possible.

The single most important takeaway: **GEP is the right second consensus benchmark** alongside IMF WEO on every country page.

## Citations

- World Bank Open Data: https://data.worldbank.org/
- Data360: https://data360.worldbank.org/
- wbgapi (Tim Herzog): https://github.com/tgherzog/wbgapi
- WBGAPI blog announcement: https://blogs.worldbank.org/en/opendata/introducing-wbgapi-new-python-package-accessing-world-bank-data
- MFMod-ModelFlow: https://github.com/worldbank/MFMod-ModelFlow
- Data360 MCP: https://github.com/worldbank/data360-mcp
- WB licensing: https://datacatalog.worldbank.org/public-licenses
- Global Economic Prospects: https://www.worldbank.org/en/publication/global-economic-prospects
- Macro Poverty Outlook: https://www.worldbank.org/en/publication/macro-poverty-outlook
- ModelFlow Python (parent framework): see Goumilevski 2023 IMF WP

## Related

- [[L040]] — IMF (parallel data adapter)
- [[L046]] — World Bank Indicators API detail
- [[L050]] — ECB SDW (parallel)
- [[L190]] — Consensus comparison (WEO + OECD + WB GEP overlay)
- [[L250]] — MCP server prototype (look at Data360 MCP for patterns)
- R09 — FRED-substitution map (WB joins the upstream-agency list)
