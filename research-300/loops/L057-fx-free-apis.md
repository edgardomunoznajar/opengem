# L057 — FX free APIs: ECB Eurofxref + FRB H.10 + BIS EER are the entire stack

**Loop**: 057 / 300
**Phase**: 1 — Open-source landscape survey (data sources)
**Date**: 2026-06-06
**Verdict**: **ADOPT-NOW ECB Eurofxref + BIS EER + FRB H.10 (already in)**. **CITE-ONLY exchangerate.host / similar resellers**. **SKIP paid forex feeds** for Block I.

---

## One-line take

For OPENGEM's purposes — daily macroeconomic-cadence FX, not real-time intraday forex trading — **three free official sources cover everything**: ECB Eurofxref for daily EUR cross-rates, BIS EER for trade-weighted effective exchange rates, and FRB H.10 (already in OPENGEM's adapter roster) for USD bilaterals. The third-party "free FX API" market (exchangerate.host, ExchangeRate-API, exchangeratesapi.io, fixer.io) is **mostly an ECB-feed reseller layer with usage-meter and freemium funnels**, valuable only when you want JSON+convenience and not at OPENGEM's volume.

## What FX OPENGEM actually needs

| Use case | Right source | Why |
|---|---|---|
| Headline daily EUR cross-rates (~35 currencies vs EUR) | **ECB Eurofxref XML / SDMX** | Official, fresh-T+0 14:15 CET, free, public-domain |
| Daily USD bilaterals (G10 + emerging) | **FRB H.10** (already in OPENGEM) | Already in `opengem-data-frb` |
| Trade-weighted effective exchange rates (NEER + REER) | **BIS EER bulk** | 64 economies daily, 26 economies back to 1983, official |
| Long-run monthly historical FX panel | **IMF IFS** + **World Bank WDI** | When BIS EER doesn't cover a country |
| Real-time intraday forex (sub-minute) | NOT NEEDED | OPENGEM is daily-cadence, not intraday |

That's it. Three GREEN sources cover 100% of OPENGEM's FX surface.

## ECB Eurofxref — the workhorse

- **Daily file**: `https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml` — current day's reference rates, 1 EUR → ~35 currencies.
- **90-day historical**: `https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml` — last 90 trading days.
- **Full historical**: `https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.xml` — 1999-current daily series for all rates.
- **Also**: CSV equivalents at parallel paths (`.csv` instead of `.xml`).
- **API style**: static XML/CSV files updated at 14:15 CET on TARGET days.
- **Auth**: none.
- **Rate limits**: none documented; 1 download/day of the daily file + 1/year of the full historical is the right pattern.
- **Coverage**: 1 EUR vs USD, JPY, BGN, CZK, DKK, GBP, HUF, PLN, RON, SEK, CHF, ISK, NOK, HRK (until 2023), TRY, AUD, BRL, CAD, CNY, HKD, IDR, ILS, INR, KRW, MXN, MYR, NZD, PHP, SGD, THB, ZAR — ~33 currencies. Cross-rates derivable by dividing.
- **License**: **CC0 / public domain equivalent** — ECB explicitly allows free use with no attribution required.
- **Vintage**: each daily file is the official fixing for that day; never retroactively revised. Vintage history is trivial.

## BIS EER — trade-weighted indices

- **Bulk download** (preferred): `https://data.bis.org/topics/EER/data` — daily ZIP, monthly ZIP. Sub-10MB.
- **REST**: per-economy URLs like `https://data.bis.org/topics/EER/BIS,WS_EER,1.0/M.R.B.US` (monthly Real Broad EER for US).
- **Cadence**: daily nominal series updated mid-week; monthly series updated mid-month.
- **Coverage**: 64 economies, Broad basket (since 1996 daily / 1994 monthly), Narrow basket (since 1983 daily / 1964 monthly, narrower 26-27 economies).
- **Series types**:
  - Nominal Broad (`N.B.{cc}`) — N for nominal, B for broad.
  - Real Broad (`R.B.{cc}`) — CPI-deflated.
  - Nominal Narrow (`N.N.{cc}`).
  - Real Narrow (`R.N.{cc}`).
- **Auth**: none.
- **License**: BIS Terms — **GREEN with attribution + non-redistribution-of-bulk**.
- **Weight rebasing**: trade weights re-estimated every 3 years; this causes apparent retroactive revisions of REER even when underlying FX didn't move.

## FRB H.10 (already in OPENGEM)

- Already adapter-ed in `opengem-data-frb` per the existing roster.
- Daily, ~25 currencies vs USD, public-domain.
- One trap: H.10 historically published a "Broad" and "Major" trade-weighted USD index alongside bilaterals. Those parallel BIS's REER but with US-Fed methodology. Worth ingesting both for the cross-source comparison feature.

## The third-party "free FX API" market (exchangerate.host etc.)

These services proliferate in the API-discovery indexes. Most are thin wrappers around the ECB Eurofxref feed plus light value-add (JSON formatting, time-series endpoints, convenience math). Pricing tiers are designed around tight free quotas to push to paid:

| Service | Free tier | Paid tiers |
|---|---|---|
| exchangerate.host | **100 requests/month** (daily updates) | $14.99/mo basic (10k req), $59.99/mo pro (100k req), $99.99/mo business (500k req, 60-sec updates) |
| ExchangeRate-API | 1,500 requests/month (daily updates) | $9/mo (100k), $19/mo (500k), $59/mo (1.5M) |
| exchangeratesapi.io (apilayer) | 100 requests/month | $9.99–$99.99/mo tiers |
| fixer.io | 100 requests/month | similar tier ladder |
| openexchangerates.org | 1,000 requests/month | $12-$300/mo |

**For OPENGEM the free tiers are useless** (100 requests/month is one call per ~7 hours; we need daily polling for fresh-dashboard semantics + ad-hoc dashboard reads). The paid tiers are unnecessary because we have ECB Eurofxref + BIS + FRB H.10 free and at fully professional quality.

**Verdict on resellers: SKIP** for Block I. CITE-ONLY if a user-facing widget needs a single-call convenience endpoint, in which case route to ECB Eurofxref directly.

## Rate-limit math for OPENGEM

- **ECB Eurofxref daily**: 1 XML download/day = 1 call/day. Trivial.
- **ECB Eurofxref historical**: 1 download per year (or on adapter bootstrap). Trivial.
- **BIS EER daily ZIP**: 1 download/day. ~5 MB.
- **BIS EER monthly ZIP**: 1 download/month.
- **FRB H.10**: daily CSV, already wrapped in `opengem-data-frb`.

Daily steady-state: **3 file fetches**. Total FX adapter cost: **<5 calls/day**. Fastest adapter in the stack alongside shipping.

## Vintage truth

FX series are observed market data with weights/indices methodologies. Revisions are:

- **ECB Eurofxref**: zero — daily fixings are final. Trivial vintage.
- **BIS EER**: weights rebase every 3 years, which retroactively recomputes REER. Adapter must snapshot the weight vintage in addition to the value vintage. The BIS publishes its weight vintage explicitly per release.
- **FRB H.10**: similar — Broad/Major index weights update periodically.

Adapter records `weight_vintage_year` for any index series.

## Fit-for-OPENGEM verdict

- **ADOPT-NOW**: ECB Eurofxref (new ingest), BIS EER (rolls into the existing BIS adapter via L049), FRB H.10 (already in).
- **ADOPT-BLOCK-II**: nothing new — FX surface is covered.
- **CITE-ONLY**: exchangerate.host etc. (mention as a "if you want JSON convenience" option in docs).
- **SKIP**: paid forex feeds, intraday FX, Refinitiv/Bloomberg.

**Adapter design notes**:

- Extend `opengem-data-ecb` (from L050) with `fetch_eurofxref(daily|hist|hist-90d)` that reads the XML/CSV files directly. (Note: the SDMX `EXR` dataflow covers similar territory but the static Eurofxref files are leaner.)
- BIS EER ingest rides on the extended `opengem-data-bis` package (L049).
- FRB H.10 is already done.
- Each Observation records `source=ecb|bis|frb`, `series=...`, `weight_vintage=...` (where applicable).

## What's deliberately not covered

OPENGEM does **not** publish:

- Intraday tick or sub-daily FX.
- Forward points / FX swaps / NDF curves (paid markets-data territory; if needed for a sovereign-fund LP, that's an API tier upsell).
- Options-implied volatility surfaces.
- Carry-trade or FX-momentum factor indices (build our own from public bilaterals if needed).

This is on-brand: OPENGEM is daily macro, not real-time markets.

## The "ECB vs FRB vs BIS for the same currency" comparison

Another candidate "publish-your-disagreement" chart: for USD/EUR over a year, show ECB Eurofxref daily fix, FRB H.10 daily fix, and a reverse-derived BIS-broad-implied rate. The three usually agree to 4 decimal places; occasional small divergences (1-2 basis points) are the difference between fixing methodologies. This is the kind of detail Bloomberg's terminal will never show users because it would invite questions; OPENGEM should embrace it.

## Trap log

- **ECB Eurofxref does not include EUR/EUR** (obviously) and does not directly give USD-base cross-rates. Cross-rates require trivial arithmetic but a naive consumer expecting USD-base will be confused.
- **HRK (Croatian kuna) was retired** January 2023 when Croatia joined the euro. Adapter must handle currency lifecycle.
- **BIS EER weight rebasing is silent**. Without recording the weight vintage, time-series visualizations will show apparent jumps that aren't real value changes.
- **Free-tier 100 req/month from resellers is not "free FX data"** — it's a marketing funnel. Don't depend on it.
- **TARGET2 holiday calendar**: ECB Eurofxref doesn't publish on TARGET2 holidays; FRB H.10 doesn't publish on US federal holidays. Their calendars differ. Adapter must merge calendars carefully.
- **FRB H.10 has been "discontinued" in print form** but the underlying data still publishes daily via FRB's CSV; legacy clients pointed at the print archive will fail.

## Related

- [[L049]] — BIS Statistics warehouse (EER lives here)
- [[L050]] — ECB Data Portal (EXR SDMX is the heavy version of Eurofxref)
- [[L059]] — Treasury yield curves (FRB H.15 is the rates cousin)
- [[R09]] (existing) — FRED-substitution; FRB H.10 already mapped
