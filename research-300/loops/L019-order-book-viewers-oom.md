# L019 — Open-Source Order-Book / Market-Data Viewers (OUT OF SCOPE)

**Loop**: 019 / 300
**Phase**: 1 — Open-source landscape survey
**Date**: 2026-06-06

---

## TL;DR

This loop is explicitly an **Out-Of-Manifest (OOM) bucket entry**. We surveyed the open-source order-book / depth-of-market / heatmap-visualizer landscape (Bookmap clones, OrderFlowMap, Elenchev/order-book-heatmap, Crypto Chassis ccapi, JuliaQuant DepthOfMarket.jl, etc.) and the answer is the same in every case: **this entire category is out of scope for OPENGEM v1, v2, and almost certainly v5.** This artifact exists so that future loops don't waste cycles re-litigating the question, and so that we have a *named, dated reason* for the rejection — fitting the broader L001 "publishes its decisions" thesis.

## The repos we looked at

| Repo | Stars | License | What it does | Status |
|---|---|---|---|---|
| [Elenchev/order-book-heatmap](https://github.com/Elenchev/order-book-heatmap) | ~500 | MIT | Browser-side Binance WS → D3 heatmap | "Short exploratory project" per author |
| [Azhagesan-dev/OrderFlowMap](https://github.com/Azhagesan-dev/OrderFlowMap) | ~200 | MIT | Bookmap clone, single-HTML, India NSE/MCX | New 2025-2026 |
| [crypto-chassis/ccapi](https://github.com/crypto-chassis/ccapi) | ~600 | Apache-2.0 | C++ unified crypto-market-data lib | Active |
| [openbookproject/openbook](https://github.com/openbookproject) | varies | mixed | Limit order book engine | Mostly research |
| [bookmap-com/bookmap-api-examples](https://github.com/Bookmap/Bookmap-API) | ~80 | MIT | Bookmap plugin SDK (commercial host) | Commercial |
| [JuliaQuant/DepthOfMarket.jl](https://github.com/JuliaQuant) | tiny | MIT | Julia order-book primitives | Stagnant |

There are many more (a couple dozen tutorial-quality repos on GitHub). None are mature, large, or financially sponsored enough to qualify as "OPENGEM should integrate this." The whole category is *tutorial-grade or commercial-shim-grade* — there is no Apache-2.0, well-funded, OpenBB-style flagship for order-book viz.

## Why this is the wrong category, explicitly

OPENGEM is a **macro-cadence accountability ledger** (L001). The *cadence* is daily-monthly-quarterly, not sub-second. The *unit of observation* is a country indicator or a forecast vintage, not a limit-order resting at a price level. The *thesis* is "publish your forecasts and miss-rates so the cartel can't hide theirs," not "trade better by reading microstructure liquidity."

Specifically:

1. **The data isn't free at the cadence we'd need.** Real depth-of-book (Level 2) data for the equity/futures markets people actually care about is paid: NASDAQ TotalView ~$70/month per user, CME MBO market-data ~$$, ICE TMC. Crypto Level 2 is free over Binance/Bybit WS — but crypto microstructure has nothing to say about *macro forecasts*. We'd be visualizing data that no OPENGEM persona (L003) cares about.

2. **The macro forecast horizon is 1Q-5Y.** Microstructure data is 1ms-1s. The gap is 11 orders of magnitude. There is no plausible feature-engineering story where "the EUR/USD order book at 14:32:18 today" improves "the 2027 Q3 euro-area CPI forecast." The macroprudential papers that try this (e.g. high-frequency identification of monetary shocks à la Gertler-Karadi) use specific windows around announcements — not continuous order-book observation, and they end up at daily-resolution series anyway.

3. **The persona overlap is zero.** Re-reading L003 personas: macro-curious YouTuber, geopolitics researcher, sovereign-fund LP, retail prosumer (interested in inflation/recession risk), journalist, hedge fund macro analyst. None of them care about real-time order books. The order-book audience is *intraday equity / futures / crypto traders* — a different cohort entirely, served by Bookmap / Quantower / Sierra Chart / TradingView paid tiers / Sweep / Goonie / Volfix.

4. **The brand collision is bad.** If OPENGEM ships an order-book heatmap, the immediate framing is "another Bloomberg-Lite trying to be Bloomberg-Trader." Our positioning is the *opposite*: macro-grade, accountability-first, "we publish our mistakes." A real-time tape view *dilutes* the brand thesis.

5. **The integration cost is real.** Even a "minimum viable order-book widget" requires: streaming WS infrastructure (Redis pub/sub or NATS), a canvas-rendering heatmap (none of our existing chart tools — Lightweight Charts L015, Perspective L014, Plotly — handle this idiom well; we'd need a custom layer or a fork of Elenchev's D3 code), Level 2 data licensing, and 24/7 uptime SLA on the streaming pipe. A 6-week build at minimum.

6. **The compliance footprint is unfun.** Once you publish order-book data, the lawyers get nervous about "is this a market data redistribution," and the exchanges' Level 2 license terms make any free public exposure a no-go. The free crypto angle survives, but as #1 noted, it's irrelevant.

## What about *cross-asset macro proxy* uses?

A reasonable counter-argument: "Couldn't OPENGEM use *some* market data — yield curves, FX, equity indices, commodity futures — as macro forecast inputs?"

Yes, **at daily close**, not at microstructure resolution. That's L057-L059 (yield curves, equity indices, FX) and L221 (energy/commodity). The data is end-of-day OHLC or daily close, from Stooq, Yahoo, FRB H.10, ECB SDW, IMF — *not* from an order book. The visualization is a line chart with bands (L015 territory) — *not* a heatmap of resting liquidity.

So the "use market data for macro" path is real, and already covered. The "visualize the order book" path is what's out of scope.

## What to do with the OOM bucket

This loop is itself the answer: **document the decision and move on.** The OOM bucket convention for OPENGEM:

- Each OOM artifact gets a loop number so it lands in the lineage like every other loop.
- The artifact names *what was rejected*, *the alternative considered*, *the explicit reasons*, and *the conditions under which the decision would be revisited*.
- It includes the search terms / repos surveyed so we don't re-pay the discovery cost.
- It's tagged `OUT OF SCOPE` in the frontmatter or first line.

The OOM bucket is part of the accountability discipline. L001 says "every methodology pop-up open" — that includes the *negative* methodology: "here's what we considered and rejected, here's why." We will accumulate a handful of these (probably 10-20 across the 300 loops); they make the design ledger more honest, not less.

### Conditions to revisit L019

We would revisit order-book / microstructure viewers if **any** of the following becomes true:

- OPENGEM's persona research (L003) surfaces a high-value cohort that *does* care about microstructure-as-macro-input — e.g. a high-frequency macro hedge fund running Gertler-Karadi-style shock identification at scale.
- A *macro-cadence* order-book signal becomes empirically useful — e.g. a paper shows that quarterly aggregates of Treasury auction depth materially improve recession nowcasts.
- We acquire / partner with a market-data vendor who can supply Level 2 under terms compatible with our CC-BY publication thesis.

None of these is foreseeable in 2026. Revisit no earlier than L300 retrospective, and only if surfaced organically.

## Surprise of the loop

**The open-source order-book viz space is shockingly thin.** Bookmap has been a category-defining commercial product for 15 years and the OSS world has never produced a credible replacement. The closest is a single-developer-side-project (Elenchev) that explicitly says "this was a short exploratory project." This tells you something about the market: the people who'd build this are already at trading firms with proprietary tools and no incentive to open-source. The community OSS quant world, by contrast, is dominated by *backtesting* and *strategy research* tooling (L013), not by trader-facing visualization. The asymmetry confirms that this category is *culturally* downstream from where OPENGEM wants to live.

## What this loop produced

- An explicit, dated OUT-OF-SCOPE call on order-book / microstructure viewers.
- Six concrete reasons for rejection.
- A specification of the OOM bucket convention for future loops.
- Three triggers under which to revisit the decision.

## What comes next

- **L020** — FinGPT / FinNLP / FinRL: the in-scope alternative for "AI on financial data."
- **L057** / **L058** / **L059** — daily-close market-data sources actually in scope (FX, equity indices, yields).
- **L221** — commodity prices at daily-or-coarser.
- A future OOM artifact (not numbered yet) likely on options/derivatives viz, same pattern.

## Related

- [[L001-vision-statement]] — "Not real-time intraday trading data" is now formally enforced here.
- [[L003-user-personas]] — the persona absence is the load-bearing argument.
- [[L013-backtrader-vectorbt-zipline]] — the category most likely to drift into this one; explicitly not letting that happen.
- [[L017-awesome-quant-roundup]] — order-book tools were excluded there too, for the same reason.
