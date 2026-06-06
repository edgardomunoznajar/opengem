# L040 — IMF: GAS toolbox, Public Open Data API, DataMapper, WEO — open vs gated

**Loop**: 040 / 300
**Phase**: 1 — Open-source landscape survey (IMF)
**Date**: 2026-06-06
**OPENGEM adoption grade**: **B for IMF data adapters (SDMX 3.0 API + WEO), C for GAS, D for everything paywalled**

---

## TL;DR

Three things were collapsed into one loop. They are not the same:

1. **IMF GAS toolbox** — Generalized Autoregressive Score models, Ardia/Boudt/Catania. **R + MATLAB + Ox + Julia (ScoreDrivenModels.jl)**. Not specifically IMF; the "GAS" is a model class, not an IMF tool. The IMF connection is via Patrick Gruss / Filip Ćulibrk-era IMF working papers using GAS for volatility / quantile forecasting. **For OPENGEM: niche. C-grade.** Useful for one or two volatility-modeling experiments; not a backbone.

2. **IMF Public Open Data API** — the modernized SDMX 3.0 API at `https://api.imf.org/external/sdmx/3.0` plus legacy SDMX 2.1 at `https://sdmxcentral.imf.org/ws/public/sdmxapi/rest` plus the older DataMapper API at `https://www.imf.org/external/datamapper/api/v2`. **All public, no authentication.** WEO, IFS, BOP, DOTS, GFS, FAS, all the canonical IMF datasets. **B-grade adoption: build `opengem-data-imf` adapter for WEO + IFS + DOTS.**

3. **IMF Data Mapper** — the user-facing dashboard at `data.imf.org`. Not for OPENGEM adoption directly (it's a UI), but a useful reference for "which IMF series get cherry-picked for storytelling" — gives us the canonical 50-100 series IMF curates.

The key thing to understand about IMF "open" is that **the data is essentially public and free, but the *licenses* and *terms* are confusing and sometimes contradict the spirit of "open."** WEO data has a copyright notice ("© IMF, all rights reserved") on its disclaimer page, yet at the same time IMF distributes WEO Excel files that any researcher can download and freely use for non-commercial / commercial work alike. The practical answer is: WEO is fine to use, cite IMF, do not redistribute the dataset *as the IMF dataset* (you can redistribute extracts, derived series, etc.).

## What's actually open

| Asset | API endpoint | License posture | OPENGEM use |
|---|---|---|---|
| WEO (World Economic Outlook) | downloadable Excel + `data.imf.org/en/datasets/IMF.RES:WEO` | "© IMF" but free for use with attribution | Forecast leaderboard overlay (L190) |
| IFS (International Financial Statistics) | SDMX 3.0 API | same | Cross-country monetary + balance-of-payments | 
| BOP (Balance of Payments) | SDMX 3.0 API | same | Sovereign risk page (L216) |
| DOTS (Direction of Trade Statistics) | SDMX 3.0 API | same | Trade flows (L052) |
| FAS (Financial Access Survey) | SDMX 3.0 API | same | EM coverage |
| GFS (Government Finance Statistics) | SDMX 3.0 API | same | Fiscal sustainability |
| FSI (Financial Soundness Indicators) | SDMX 3.0 API | same | Banking-sector risk |
| PortWatch | dedicated API | CC-licensed implicit | Already in scope as L055 (shipping) |
| **Article IV reports** | PDF | © IMF | Cite only, not data |
| **Internal forecasts (Greenbook equivalent)** | not public | gated | Not available |

The most-cited IMF series for macro forecasting:

- WEO `NGDP_RPCH` — Real GDP growth, % change.
- WEO `PCPIPCH` — Inflation, average CPI.
- WEO `LUR` — Unemployment rate.
- WEO `GGXWDG_NGDP` — General government gross debt as % of GDP.
- WEO `BCA_NGDPD` — Current account balance as % of GDP.
- IFS `ENDE_XDC_USD_RATE` — Period-end exchange rate.
- IFS `FPOLM_PA` — Central bank policy rate.

These ~7 series plus the country roster give us about 80% of the WEO/IFS surface area for our purposes. **A focused `opengem-data-imf` package can ship in 2 weeks** with WEO + IFS + DOTS coverage at OECD-26 + BRICS+ resolution.

## The API landscape — three APIs, one IMF

The IMF data team in 2024–2025 launched a new SDMX 3.0 API (`https://api.imf.org/external/sdmx/3.0`). This is the **forward path**. They keep the SDMX 2.1 API alive at sdmxcentral.imf.org and the DataMapper API at imf.org/external/datamapper. Both legacy endpoints work today; the IMF Help Desk recommends migrating to SDMX 3.0.

For OPENGEM:

- **Use SDMX 3.0 as the primary adapter.** It's modern, well-documented, JSON-friendly.
- **Use the DataMapper API as a discovery aid.** It exposes the curated catalog of country / indicator / region / group lists that the IMF themselves use for storytelling. Very useful for our "indicator-card grid" UI work (L162).
- **Avoid SDMX 2.1.** Legacy; not the long-term path.

Best-in-class Python clients:

- `sdmx1` on PyPI — Python implementation of SDMX 2.1 + 3.0, Apache-2.0, well-maintained. **Adopt.**
- `pandasdmx` — older SDMX 2.1 client, Apache-2.0. Active but less full-featured than `sdmx1`.
- `imfapi` (R, via Teal-Insights / econdataverse) — R-specific. Useful for our reference / replication work, not adopt.
- `imf.data` (R) — older R wrapper, deprecated in favor of `imfapi`.
- Hand-rolled HTTP client — for our adapter pattern (per `opengem-data-base`), we wrap `sdmx1` with our retry-and-vintage hooks.

## GAS toolbox — what it actually is

Generalized Autoregressive Score models (Creal-Koopman-Lucas 2013) are a class of **observation-driven models** where the time-varying parameters are updated using the score of the conditional density. They are the natural successor to GARCH for volatility modeling, extended to copulas, location-scale, and quantile dynamics.

The "GAS toolbox":

- **R: `GAS` package** by Ardia, Boudt, Catania (JSS 2019, `LeopoldoCatania/GAS` on GitHub). Multivariate, GAS-copula support, well-tested.
- **R: `gasmodel` package** (Holub, 2024, JOSS-published). Newer; more flexible spec; broad distribution coverage.
- **MATLAB**: original Creal-Koopman-Lucas implementation.
- **Julia: ScoreDrivenModels.jl** (Saavedra, Bodin, 2020). Active.
- **Ox**: legacy academic.
- **Python**: no canonical maintained library. Some scattered notebook implementations.

The "IMF" connection here is weak: IMF working papers (Patton, Ziegel, Chen, etc.) use GAS for financial-stability volatility modeling. There is no "IMF GAS toolbox" as such.

For OPENGEM:

- **Where GAS could be useful**: modeling time-varying volatility of GDP growth, sovereign-CDS spreads, exchange-rate fluctuations. Quantile / fan-chart forecasting (L208 left-tail GDP).
- **But**: we're not doing volatility-modeling at scale in Block I. Block II might use a single GAS model for the recession-probability tile (L213) to complement Bauer-Mertens.
- **Path**: if needed, use R `GAS` via rpy2, or implement a thin Python wrapper over the published math (Creal-Koopman-Lucas 2013 is concise — ~3 weeks to a Python re-implementation if motivated).

**Grade C**. Cite, don't adopt as backbone. Maybe a one-off Block III experiment.

## Data adapter detail

`opengem-data-imf` adapter spec:

```python
from opengem_data_base import Adapter, RetryConfig
import sdmx1

class IMFAdapter(Adapter):
    """Pulls WEO + IFS + DOTS via SDMX 3.0 with vintage tagging."""

    def __init__(self):
        self.client = sdmx1.Client(
            "https://api.imf.org/external/sdmx/3.0",
            retry_config=RetryConfig(
                attempts=5, backoff_factor=2,
                retry_on=(429, 502, 503, 504),
            ),
        )

    def fetch_weo_series(
        self, series_code: str, country: str,
        vintage_quarter: Optional[str] = None
    ) -> VintageSnapshot:
        ...

    def fetch_ifs(self, series, country, freq="M"):
        ...

    def fetch_dots(self, exporter, importer, freq="M"):
        ...
```

Vintage handling: IMF publishes WEO twice a year (April + October). We tag each `VintageSnapshot` with the release date. ALFRED-style "as-of" queries become natural.

## What is NOT open at IMF

- **Article IV reports beyond the public PDF**: detailed projection databases are usually internal.
- **MAC DSF / LIC DSF results beyond the published spreadsheets** — debt-sustainability runs are sometimes private until the country agrees to publish.
- **WEO database vintages**: the IMF publishes only the *current* WEO. Historical WEO vintages are *technically* available but require digging through old PDFs and Excel files. There is no clean WEO vintage API. **This is a real friction for our V&V matrix** — comparing OPENGEM forecasts to "what the IMF said as of last October" requires us to maintain our own archive of WEO Excel snapshots.
- **In-house monitoring datasets** (e.g. country-specific risk dashboards).

## License posture

The IMF distinguishes between **data** and **publications**:

- **Data is broadly permissive.** Free use with attribution. Suitable for redistribution as derived series.
- **Publications are © IMF.** Cannot redistribute as-is. Citation only.

For OPENGEM, the practical posture:

- Our `opengem-data-imf` adapter cites IMF in every retrieved series's provenance.
- Our model cards cite WEO / IFS as upstream data.
- We do **not** redistribute the WEO Excel files verbatim.
- We **do** redistribute our derived forecast series with attribution like "fitted to WEO data via OPENGEM model X, vintage Y."

This is the same posture every research user takes with WEO data. Low risk.

## Risks

1. **SDMX 3.0 API stability.** New API, still evolving. The IMF Data Help Desk has been responsive to bug reports. Mitigation: pin a `sdmx1` version; test the endpoint regularly; have a fallback to SDMX 2.1.

2. **WEO vintage archive.** No clean API for historical vintages. Mitigation: write a one-time script that pulls every WEO Excel since 2010 from imf.org/external/pubs/ft/weo and converts to our `VintageSnapshot` format. Maintain manually going forward (2x/year).

3. **License interpretation drift.** The IMF could tighten their data terms at any time (as FRED did in 2024). Mitigation: keep our own ALFRED-like archive of vintaged downloads; don't rely on live API queries for backtesting.

4. **PortWatch API stability.** Separate concern; tracked via L055.

5. **DataMapper deprecation.** The DataMapper API is older. IMF may sunset it once SDMX 3.0 covers all of DataMapper's curated catalog. Mitigation: use it lightly, only for catalog discovery.

## Verdict

- **B-grade for IMF data adoption.** Build `opengem-data-imf` with SDMX 3.0 backbone covering WEO + IFS + DOTS + BOP. Use `sdmx1` Python library. Tag every fetch with vintage. License-friendly with attribution.
- **C-grade for GAS toolbox.** Cite, don't adopt as backbone. R `GAS` or `gasmodel` via rpy2 if a specific scenario calls for it.
- **D-grade for everything gated.** Article IV detailed projections, internal Greenbook-equivalent — not for us.

## Citations

- IMF Data API: https://data.imf.org/en/Resource-Pages/IMF-API
- IMF SDMX 3.0 base: `https://api.imf.org/external/sdmx/3.0`
- WEO database: https://data.imf.org/en/datasets/IMF.RES:WEO
- WEO disclaimer: https://www.imf.org/en/publications/weo/weo-database/disclaimer
- `sdmx1`: https://sdmx1.readthedocs.io/
- `pandasdmx`: https://pandasdmx.readthedocs.io/
- Ardia, Boudt, Catania. "Generalized Autoregressive Score Models in R: The GAS Package." *Journal of Statistical Software* 88(6), 2019.
- Creal, Koopman, Lucas. "Generalized Autoregressive Score Models with Applications." *Journal of Applied Econometrics* 28(5), 2013.
- ScoreDrivenModels.jl: arXiv:2008.05506
- imfapi (R, econdataverse): https://github.com/Teal-Insights/r-imfapi

## Related

- [[L042]] — World Bank (parallel data-source story)
- [[L043]] — ECB SPF (parallel survey-data story)
- [[L047]] — IMF SDMX detailed endpoints (next-level adapter detail)
- [[L052]] — IMF DOTS (trade flows)
- [[L055]] — IMF PortWatch (shipping)
- [[L208]] — Tail forecasts (where GAS could maybe fit)
- R09 — FRED-substitution map (IMF complement upstream)
