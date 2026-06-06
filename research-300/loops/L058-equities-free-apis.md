# L058 — Equities free: Stooq for indices, yfinance with eyes open, Alpaca free for US, Polygon as the structural fallback

**Loop**: 058 / 300
**Phase**: 1 — Open-source landscape survey (data sources)
**Date**: 2026-06-06
**Verdict**: **ADOPT-NOW Stooq** for daily world equity indices, **ADOPT-BLOCK-II Alpaca free tier** for US equities and daily bars, **CITE-ONLY yfinance** for ad-hoc enrichment, **SKIP Polygon free**, **SKIP all paid feeds** until a sovereign-fund LP customer demands them.

---

## One-line take

The "free equity data API" landscape is a graveyard littered with ToS violations and shut-down services (Yahoo's no-API stance + the August 2024 IEX Cloud shutdown were the load-bearing events). For OPENGEM's daily macro use case — **headline equity indices to overlay on macro charts, not stock-picking infrastructure** — **Stooq + Alpaca free tier + the LSEG / SIX bilaterals via local indices** is enough. Anything beyond that is markets-data territory we're not pretending to compete in.

## What equity data OPENGEM actually needs

OPENGEM's friend-the-YouTuber and the "macro pulse" page want:

- **Headline indices** (S&P 500, NASDAQ, Russell 2000, FTSE 100, Stoxx 600, Nikkei 225, Hang Seng, Shanghai Composite, Sensex, KOSPI, Bovespa, IPC, RTSI, ASX 200, TSX) daily close + intraday for the ticker tape.
- **Sector indices** (S&P 500 sectors at minimum) for the "what's working" narrative.
- **Volatility indices** (VIX, V2X) for the risk-on/risk-off narrative.
- **Country ETFs** as a fallback for headline markets where we can't get the national index directly (EEM, EWZ, EWJ, MCHI, etc.).

We do NOT need:
- Per-stock pricing for OPENGEM's macro stance.
- Real-time NBBO or order-book.
- Options chains, Greeks, IV surfaces.

## Stooq — the surprise winner

- **Base URL**: `https://stooq.com/q/?s={ticker}&i={interval}` for current quotes; `https://stooq.com/db/h/` for historical CSV bulk downloads.
- **Coverage**: world equity indices, ETFs, stocks across multiple regions, plus bonds, forex, cryptocurrencies, commodities. Daily/hourly/5-minute intervals.
- **API style**: URL-based CSV download. No formal API — direct file URLs return CSVs. Bulk historical downloads via region+frequency pages, with CAPTCHA on the bulk pages.
- **Auth**: none.
- **Rate limits**: undocumented; community-tested at "polite" — sub-1 RPS, single-CSV-per-URL queries.
- **License**: Stooq's footer mentions "Terms of service" but the terms permit free non-commercial use of the data. **YELLOW** — commercial redistribution unclear. For OPENGEM's free public dashboard, fine. For our paid tier or bulk export, ambiguous — would need email clarification from Stooq.
- **Vintage**: Stooq doesn't expose vintage; daily values are observed and final.

For OPENGEM's headline-index overlay use case, Stooq covers the world ETFs and indices that yfinance covers, in CSV, without the ToS gray.

## yfinance (Yahoo Finance reverse-engineered)

- **Reality**: Yahoo Finance has **no official API**. `yfinance` (the Python library) reverse-engineers Yahoo's internal endpoints.
- **Status**: Yahoo periodically tightens throttling; the library breaks for days at a time; rate-limit error 429 is common. Yahoo Developer API ToS technically prohibits scraping for commercial use.
- **Verdict for OPENGEM**: **CITE-ONLY** — acknowledge as a thing analysts use; do not depend on it as a production data source. Adapter, if we build one, should be marked "best-effort, may break without notice."

## Alpaca free tier

- **Free tier includes**: IEX-exchange-only real-time equity data + indicative options feed. Paper trading. Full historical via API.
- **What's behind paywall ($99/mo Algo Trader Plus)**: full SIP feed (consolidated NBBO from all US exchanges).
- **Auth**: free API key per registered account.
- **Rate limits**: Free tier — 200 requests/minute for the data API. Paper trading account at no cost.
- **License**: Alpaca data is licensed; redistribution requires Alpaca terms acceptance. Per-Observation use in a dashboard is fine. **YELLOW for bulk redistribution; GREEN for displayed values.**
- **Coverage**: US equities only. No international.

For OPENGEM's US equity tile, **Alpaca free tier + IEX-only is sufficient** for the daily-close use case. The IEX-only limitation is irrelevant at daily cadence.

## Polygon free tier

- **Free tier**: **5 calls per minute**. Practically useless for any dashboard refresh.
- **Paid**: $199/month+.
- **Verdict**: **SKIP for Block I and Block II**. The free tier doesn't support real production use; paid tiers are markets-data spend we don't need.

## IEX Cloud (the cautionary tale)

- **Status**: **shut down August 31, 2024**. Acquired by IEXSD; product retired.
- **OPENGEM lesson**: any free equity data source can vanish overnight. Build adapters with **swappable backends**, not hardcoded to a single vendor.

## Alpha Vantage

- **Free tier**: 25 requests/day. Useless.
- **Premium**: $49.99-$249.99/month.
- **Verdict**: SKIP.

## Tiingo

- **Free tier**: limited.
- **Paid**: $10/month for personal use. Reasonable price point.
- **Verdict**: CITE-ONLY for Block I; consider for Block II if Stooq attribution becomes a problem.

## FMP (Financial Modeling Prep)

- **Free tier**: 250 requests/day.
- **Paid**: $19/month entry.
- **Verdict**: CITE-ONLY for Block I.

## Country index → ETF substitution table

Where we can't get a national index directly, country ETFs provide a reasonable proxy at NYSE-listed prices:

| Index we want | Free source | ETF fallback (Stooq or Alpaca) |
|---|---|---|
| S&P 500 (^SPX) | Stooq `^SPX` or Alpaca SPY | SPY |
| Nikkei 225 (^N225) | Stooq | EWJ |
| Hang Seng (^HSI) | Stooq | EWH / 2800.HK |
| Shanghai Composite (^SSEC) | Stooq | MCHI / FXI |
| FTSE 100 (^FTSE) | Stooq | EWU |
| Stoxx 600 (^STOXX) | Stooq | FEZ |
| Bovespa (^BVSP) | Stooq | EWZ |
| Sensex (^BSESN) | Stooq | INDA |
| KOSPI | Stooq | EWY |

ETF fallback values lag the underlying by 6-8 hours when the foreign market is closed (NY trading hours don't overlap with Asia), but for OPENGEM's daily macro purposes that's acceptable.

## Rate-limit math for OPENGEM

**Stooq**:
- 15 headline indices × 1 daily close + 5 sector indices + VIX + V2X = ~25 CSV downloads/day at 1 per URL.
- 1 monthly bulk historical refresh.
- Total: ~25 calls/day at sub-1 RPS = 30 seconds wall-clock.

**Alpaca free tier**:
- Optional US-equity overlay: ~10 calls/day for daily bars. Well under 200 req/min.

**Total equity adapter budget**: ~35 calls/day. Negligible.

## Vintage truth

Equity prices are observed market data with finality. No revisions. Vintage is trivial.

The exception: dividend/split adjustments — adjusted-close series are recomputed when corporate actions happen. Adapter should ingest both adjusted-close and unadjusted-close, distinguish in provenance.

## Fit-for-OPENGEM verdict

- **ADOPT-NOW**: Stooq for daily world index closes + VIX/V2X.
- **ADOPT-BLOCK-II**: Alpaca free tier for US equities overlay; potentially Tiingo if Stooq attribution becomes a problem.
- **CITE-ONLY**: yfinance (mention as an option for power users); FMP; Alpha Vantage paid.
- **SKIP**: Polygon (free tier too tight), IEX Cloud (dead), all paid feeds for Block I.

**Adapter design notes**:

- New package `opengem-data-equities`.
- Submodule 1: `StooqAdapter` — pulls CSV from the URL pattern, parses, caches. Polite throttle. Handles CAPTCHA gracefully (degrades to per-symbol pulls without CAPTCHA, falls back to manual cache refresh).
- Submodule 2: `AlpacaAdapter` (Block II) — wraps the Alpaca API key.
- License flag on every Observation: Stooq sources flagged `redistribution_restricted=true`, Alpaca sources flagged `display_only=true`.

## Trap log

- **yfinance is a known-fragile dependency**. Any production adapter that builds on it should declare so explicitly and ship with a "this may break without notice" disclaimer.
- **Stooq's commercial-redistribution terms are unclear** — for OPENGEM's free public dashboard, we're probably fine; for the paid API tier we'd need to email Stooq for permission.
- **IEX Cloud's August 2024 shutdown** is the cautionary tale: any free vendor can disappear. Adapters must be swappable.
- **Alpaca free tier IEX-only feed has lower coverage** than the full SIP feed during periods when IEX market share is low. For US equity daily close, this is rarely a problem (closing-cross prices broadly agree across venues); for intraday, large differences.
- **Index name conventions vary**: Yahoo uses `^GSPC` for S&P 500; Stooq uses `^SPX`. Adapter must maintain a cross-vendor ticker dictionary.
- **VIX is published by Cboe**, not by Yahoo or Stooq directly. Both vendors mirror; Cboe's free historical CSV at `cdn.cboe.com/api/global/delayed_quotes/charts/historical_data/...` is the authoritative source.
- **Stooq CAPTCHAs the bulk download pages** but not individual symbol URLs. Adapter should prefer per-symbol patterns for incremental updates and fall back to manual cache for bulk historical refreshes.
- **Daily close at "market close" varies by venue**: S&P close is 4:00 ET, Nikkei is 15:00 JST, Bovespa is 17:00 BRT. Adapter must capture the local-time close and convert to UTC.

## What this enables on the dashboard

- **Macro pulse tile**: live index ticker, 24h delta, week delta, year delta. The Bloomberg-aesthetic header row.
- **Country page overlay**: equity index as a covariate on the country page (e.g., Bovespa overlay on Brazil GDP nowcast).
- **Risk-on/risk-off tile**: VIX/V2X levels with regime classifier.
- **Sector rotation map**: S&P 500 sector breadth visualization.

None of this is markets-data territory. All of it is macro-context territory. **That's the right ceiling for OPENGEM's equity ambition in Block I.**

## Related

- [[L056]] — Commodity prices (commodity ETFs sometimes overlap)
- [[L059]] — Treasury yield curves (rates equity correlation)
- [[L057]] — FX (equity-FX correlation page)
