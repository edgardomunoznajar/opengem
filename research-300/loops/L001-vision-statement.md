# L001 — Vision Statement: OPENGEM World Dashboard

**Loop**: 001 / 300
**Phase**: 0 — Strategic framing
**Date**: 2026-06-06

---

## One-sentence pitch

**OPENGEM is the public macro-accountability ledger for the world economy — a Bloomberg-grade dashboard for everyone, where every forecast is open, every number is dated, and every miss is named.**

## Twelve-word version

A world dashboard that publishes its mistakes so the incumbents cannot hide theirs.

## The asymmetry, restated

The forecasting cartel — IMF WEO, OECD EO, Bloomberg Economics, Goldman GIR, JPM Macro, the buy-side desks, the Stratfor-grade newsletters — produce *priced* forecasts. Their track records are private. Their margins depend on opacity. They cannot publish their full calibration without exposing why the customer is paying.

OPENGEM has no margins to protect. So it can publish:

- Every vintage of every forecast it has ever made (provenance-stamped).
- Every backtest, with every cell of the V&V matrix open.
- Every model card, with every assumption named.
- Every miss, with a post-mortem in the same place the original was published.

That is the asymmetry. **"A system that publishes its mistakes is harder to discredit than a system that hides them."**

## Three things the dashboard MUST be

1. **A live, terminal-grade view of the world economy** — country pages, indicator pages, scenario pages, forecast pages, with bands, with consensus overlays, with one-click drilldown into the underlying data.

2. **A public accountability ledger** — every forecast vintaged, every backtest scored, every miss named, every methodology pop-up open. The numbers come with their own report card attached.

3. **A composable open-source substrate** — Apache-2.0 code, CC-BY-4.0 data, model cards, an MCP server, RSS feeds, embeddable widgets. Anyone can fork, mirror, derive, embed.

## Three things the dashboard MUST NOT be

1. **Not real-time intraday trading data.** This is macro, not micro. Daily / weekly / monthly cadence, not sub-second. We do not chase Bloomberg's market data feed.

2. **Not a black-box "AI forecast."** Every forecast is a named model with a named methodology and a track record. Generative narrative on top of grounded numbers, never instead of them.

3. **Not a private newsletter.** No "premium" forecasts behind a paywall. Paid tier is for *velocity* (alerts, API throughput, MCP throughput) and *fit* (white-label embeds, branded tearsheets), never for *secrecy*.

## The three-cohort thesis

| Cohort | Need | OPENGEM's bet |
|---|---|---|
| **Macro-curious prosumer** (YouTuber, blogger, Substack-er, Reddit commenter) | "Numbers I can paste and cite" | Free public dashboard + JSON-block-per-chart + RSS + embeddable widget |
| **Pro researcher** (analyst, journalist, NGO, gov staffer) | "Numbers with provenance + lineage I can defend" | Open vintage store, forecast leaderboard, methodology pop-ups, cite-this-view, API |
| **Forecast LP** (sovereign fund, family office, hedge fund) | "An open benchmark to negotiate vendor contracts against" | Paid tier: API throughput, MCP throughput, white-label embeds, calibration reports |

The first cohort drives top-of-funnel volume. The third cohort drives revenue. The middle cohort is the credibility anchor.

## Why now (six tailwinds)

1. **LLMs commoditize narrative**, so the moat shifts from "we write good prose" to "we publish good numbers with provenance the LLM can chew on."
2. **MCP is real**: an open server lets any LLM chat (ChatGPT, Claude, Gemini, Mistral, local) ground itself in OPENGEM forecasts without OPENGEM having to build a chat product.
3. **Open-source dashboard stack is mature**: Next.js + Tailwind + Lightweight Charts + Plotly + Kepler.gl + Observable + Datasette = production-grade UI built by one developer.
4. **Public data is denser than ever**: FRED, World Bank, IMF SDMX, OECD ORDRA, BIS, GDELT, ACLED, PortWatch, IEA — coverage that was sovereign-only twenty years ago is now an HTTP GET.
5. **The cartel is brittle**: Bloomberg's terminal-per-seat model and Stratfor's editorial cadence are both vulnerable to a free, open, machine-readable substrate that LLMs route through.
6. **Trust is bleeding out of legacy forecasters** (post-COVID, post-2022 recession-that-wasn't, post-LLM-eats-research) — and a brand built on "we publish our mistakes" reads as a credible counter.

## What success looks like in three horizons

| Horizon | Test |
|---|---|
| **30 days from v1 launch** | One non-Edgardo human (the YouTuber friend) uses the dashboard daily and pastes its JSON into their workflow at least 5x. |
| **12 months from v1 launch** | 100 weekly active humans on the public dashboard; 5 paying customers on the API/MCP tier; 1 academic citation of the open ledger. |
| **5 years from v1 launch** | OPENGEM forecast tracking is referenced in a press piece *next to* WEO and OECD EO as a benchmark to compare incumbents against. The track record is impossible to dispute because it's been public the whole time. |

## What this loop produced

- One-sentence and twelve-word pitches.
- Three musts + three must-nots.
- Three-cohort thesis with the funnel logic.
- Six "why now" tailwinds.
- Three success horizons.

## What comes next

- **L002** maps the competitive landscape (Bloomberg, Stratfor, OWID, TradingEconomics, Macrobond, OECD Data).
- **L003** drafts six personas in depth.
- **L004** decomposes 25 atomic JTBDs across persona × horizon.
- **L005** proposes three candidate north-star metrics.

## Related

- [[R100-vision]] — original 5-year arc (this loop sharpens it to dashboard-product framing)
- [[R99-synthesis]] — the rebaseline that makes the V&V matrix tractable
- [[OG1-CONOPS-001-revC]] — operational concept this dashboard surfaces
