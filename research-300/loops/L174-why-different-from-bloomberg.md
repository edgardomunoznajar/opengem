# L174 — "Why Is This Different from Bloomberg?" Page

**Loop**: 174 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The thesis

Every visitor in the first 30 seconds wonders: how is this different from Bloomberg / Reuters Eikon / Stratfor / TradingEconomics? We answer it on a dedicated editorial page. The page is positioned as content (not marketing), titled bluntly, written in plain prose.

It positions OPENGEM not as "a free Bloomberg" but as a *different artifact* — an open, vintaged, auditable substrate for an LLM-mediated future.

## URL

`/different`

(Brief, memorable, route-stable.)

Linked from:
- Footer (L178)
- Onboarding (L139)
- About page (L136)
- Pricing page (L138)

## The structure

```
   ┌────────────────────────────────────────────────┐
   │                                                  │
   │  Why is this different from Bloomberg?           │
   │                                                  │
   │  ────────────────────────────────────────────   │
   │                                                  │
   │  Five differences. Pick the one that matters     │
   │  to you and the rest will follow.                │
   │                                                  │
   │  1. The forecasts ship with their report card    │
   │  2. The methodology is open                      │
   │  3. The URL is the API                           │
   │  4. The track record is public                   │
   │  5. The data has a vintage                       │
   │                                                  │
   │  ────────────────────────────────────────────   │
   │                                                  │
   │  [Each section expanded below...]                │
   │                                                  │
   └────────────────────────────────────────────────┘
```

Uses the editorial typeface (Source Serif 4, per L147) — the page should *read*, not "interface."

## Section 1: The forecasts ship with their report card

Every forecast carries a calibration plot, a CRPS history, and a per-vintage track record. Public, vintaged, named.

```
   ┌────────────────────────────────────────────┐
   │  Demo: US CPI 4Q-ahead forecast, 24 months │
   │                                              │
   │  [Calibration plot + score history chart]   │
   │                                              │
   │  OPENGEM: CRPS 0.32, 13/24 vintages in-band │
   │  WEO:     CRPS 0.61, 7/24 vintages in-band  │
   │  Cleveland Fed: CRPS 0.41, 16/24 in-band    │
   └────────────────────────────────────────────┘
```

Bloomberg doesn't publish their consensus calibration. You can't tell from Bloomberg whether their consensus median is consistently biased. OPENGEM can answer that for OPENGEM and every other public forecaster we compare against.

## Section 2: The methodology is open

Each forecast links to:
- A methodology page (L172)
- A backtest
- A code commit
- A runnable notebook

You can clone the repo, run the model on your machine, get the same number. No professional has been able to do that with a Bloomberg forecast since the 1990s.

## Section 3: The URL is the API

Every chart has a URL. Every URL resolves to JSON. Every JSON is documented in OpenAPI. Every API endpoint is documented in MCP.

```
   GET /indicator/cpi-yoy?countries=usa
   → human view (HTML)

   GET /indicator/cpi-yoy?countries=usa
   Accept: application/json
   → JSON view

   GET /indicator/cpi-yoy?countries=usa
   Accept: text/csv
   → CSV

   Or via MCP:
   tool: indicator.get
   args: { id: "cpi-yoy", countries: ["usa"] }
   → same JSON
```

A Bloomberg chart can't be pasted into a Substack. An OPENGEM URL can. A Bloomberg dataset can't be queried by an LLM. An OPENGEM dataset can.

## Section 4: The track record is public

The accountability page (L175) shows every forecast OPENGEM has ever published. Every miss. Every revision. Every methodology change.

You can search for our worst calls. You can find our 95th-percentile misses. They're there.

Bloomberg's failure log is internal. OECD's WEO has multi-year-old methodology that you can find but no real-time calibration view. OPENGEM's failure log is `/accountability` and it's the page we'd never want to hide because we built the product to inhabit it.

## Section 5: The data has a vintage

Every number on OPENGEM is dated. Not "current" — dated. The vintage time machine (L173) lets you rewind to any past date and see what the dashboard showed then.

This is mundane data hygiene that the industry has somehow abandoned. Bloomberg shows you the latest, and the latest changes when revisions land. You can never reproduce an analysis from last Thursday because the data underneath has shifted. OPENGEM solves this by treating every number as a vintaged artifact, indefinitely.

---

## What OPENGEM is NOT

The page closes with what we're not:

```
   ┌────────────────────────────────────────────┐
   │  What OPENGEM is NOT                         │
   │                                              │
   │  Not real-time intraday market data.         │
   │     This is macro. Daily, weekly, monthly.   │
   │                                              │
   │  Not a black-box "AI forecast."              │
   │     Every forecast is a named model with     │
   │     a named methodology and a track record.  │
   │                                              │
   │  Not a private newsletter.                   │
   │     Free tier is the full forecast set.      │
   │     Paid tier is for velocity (API, MCP,     │
   │     alerts) and fit (white-label embeds).    │
   │                                              │
   │  Not a replacement for your terminal — yet.  │
   │     If you trade fixed income on the 1s, you │
   │     need Bloomberg or Refinitiv.             │
   │     If you make decisions on macro themes,   │
   │     OPENGEM is the open substrate.            │
   │                                              │
   └────────────────────────────────────────────┘
```

## Comparison table

A clean table to anchor the differences:

```
                       Bloomberg    Stratfor   OPENGEM
   ─────────────────────────────────────────────────
   Cost                ~$25K/y      ~$4K/y      free + paid
   Public URL          no           no          yes
   Open methodology    no           partial     yes (every chart)
   Vintage time machine no          no          yes
   Open API            no           no          yes (Apache-2.0)
   MCP support         no           no          yes (first-party)
   Public track record no           no          yes
   Cite-able           no           no          yes (DOIs)
   Notebook export     no           no          yes
   Embeddable widgets  no           no          yes (free)
   ─────────────────────────────────────────────────
```

## Section: when to keep Bloomberg

Honesty:

```
   Keep Bloomberg if:
    - You execute trades and need their messaging
    - Your firm requires Bloomberg compliance integrations
    - You need real-time fixed-income market data
    - You need the chat (IB)
   
   Keep Stratfor if:
    - You want curated geopolitical narrative
    - You don't have time to build your own brief
   
   Use OPENGEM alongside, when:
    - You want to cite a number in writing
    - You want to embed a chart in a Substack
    - You want an LLM to ground itself in real data
    - You want a forecast with a track record
    - You want methodology you can audit
   
   Use OPENGEM instead of consensus forecasts when:
    - You want vintaged forecasts you can replay
    - You want scoring against actuals
    - You want open math
```

## Editorial tone

Not aggressive. Not "the Bloomberg moat is dying." Confident, plain, accurate. The page should read as if a senior researcher wrote it for a colleague.

No marketing words. No "revolutionary," no "disruptive," no "AI-powered."

## The page footer

```
   ────────────────────────────────────────────────
   Last reviewed: 2026-06-06
   We update this page when the comparison shifts.
   See the diff in our changelog: /about/changelog
```

The page itself is vintaged. Per the "publish your mistakes" thesis, we may eventually need to acknowledge if a comparison becomes obsolete.

## Implementation

- Static MDX page with embedded charts
- The demo calibration plot is a live OPENGEM forecast, vintaged to publication date
- Comparison table is a markdown table
- Linked from the home page, about page, footer, onboarding

## SEO

Page targets the literal query "OPENGEM vs Bloomberg" and "open Bloomberg alternative." Schema.org structured data for `Article`.

## Anti-patterns avoided

- "We're better than Bloomberg" claim. We're *different*; we don't claim superiority on Bloomberg's home turf.
- Bullet lists of marketing features. The page is prose.
- Hidden "but you need paid tier" caveats. Free tier is the demonstration; paid is the upgrade path.

## The asymmetric move

A page titled "Why is this different from Bloomberg?" exists nowhere in macro. Every incumbent pretends they don't have a comparator. We make the comparison explicit, fair, and updated.

The page is our *positioning artifact* — what we point at when journalists, investors, and prospects ask.
