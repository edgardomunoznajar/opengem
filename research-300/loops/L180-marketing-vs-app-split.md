# L180 — Marketing Site vs App Split

**Loop**: 180 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The decision

**The public dashboard IS the marketing site. Single front door. No `marketing.opengem.app` subdomain. No "marketing.html" landing pages.**

Reasoning, decisively:
1. OPENGEM's competitive thesis is "we publish our forecasts publicly." Hiding behind a marketing page contradicts the thesis.
2. Anyone arriving via a search for "US CPI forecast" should land on the actual forecast, not a "sign up to see the forecast" wall.
3. Conversion happens not from landing-page copy but from the user seeing the product *being good*.
4. Building two sites (marketing + app) doubles the work and creates content drift.

So: `opengem.app/` is the dashboard. The dashboard IS the marketing. The marketing IS the product.

## What this means concretely

### `opengem.app/` (the home)

When a visitor lands at the root with no specific page in mind, they see the world dashboard, populated with live data:
- Country cohort grid (L161)
- World pulse score
- Top-of-mind feed (L170)
- Recent accountability entries
- 4 hero KPI tiles (global GDP nowcast, world inflation nowcast, world recession-prob composite, world pulse)

There is no "Welcome to OPENGEM!" copy. The product is the welcome.

The only marketing-flavored elements:
- A 1-line subhead: "Open macro accountability ledger."
- A subtle "What is this?" link routing to `/different` (L174).
- A "Get an API key" CTA in the top-right (small, second-priority).

## The 5 navigational "doors"

A visitor's reason to arrive matters. We design five doors:

1. **The data door**: search results brought them to a specific page. `/country/usa`, `/indicator/cpi-yoy`. They land on the chart. No marketing.

2. **The brand door**: heard about OPENGEM, typed the URL. Lands at `/`. Sees the live dashboard. No splash.

3. **The dev door**: heard "OPENGEM has an MCP server." Lands at `/mcp` or `/api`. Sees install snippets. No upsell.

4. **The journalist door**: "I want to cite this." Lands at `/accountability` (often via Google for "open macro forecasts"). Sees the ledger.

5. **The buyer door**: "I'm considering paying for this." Lands at `/pricing`. Sees the tiers.

Every door is a real page. No landing page intermediate.

## The home page (more detail)

```
   ┌────────────────────────────────────────────────────┐
   │  OPENGEM                                  ⌘K  ⓘ ☰ │
   │  Open macro accountability ledger                    │
   │  ────────────────────────────────────────────────  │
   │                                                      │
   │  Hero tiles                                          │
   │  ┌────────┬────────┬────────┬────────┐              │
   │  │ World  │ World  │ World  │ World  │              │
   │  │ GDP    │ CPI    │ recess │ pulse  │              │
   │  │ +2.7%  │ +3.1%  │ 31%    │ -0.4   │              │
   │  └────────┴────────┴────────┴────────┘              │
   │                                                      │
   │  Cohort: [G7] [G20] [EU] [ASEAN] [BRICS] [OECD]     │
   │                                                      │
   │  ┌──────────────────────────────┬─────────────┐    │
   │  │                                 │             │    │
   │  │   [country card grid]            │  Top-of-    │    │
   │  │                                 │   mind      │    │
   │  │   USA  GER  FRA  ITA            │   feed      │    │
   │  │   JPN  GBR  CAN                 │             │    │
   │  │                                 │             │    │
   │  │                                 │             │    │
   │  └──────────────────────────────┴─────────────┘    │
   │                                                      │
   │  Recent accountability:                              │
   │   • OPENGEM beat consensus on May UK CPI (rank 1/4)  │
   │   • OPENGEM missed Q1 Japan GDP by 0.6pp             │
   │                                                      │
   │  What is this? →  · API key →  · Pricing →           │
   │                                                      │
   │  [footer]                                            │
   └────────────────────────────────────────────────────┘
```

## Why this works as marketing

A visitor sees:
- Real forecasts
- A real grid of countries
- Real numbers
- Real misses (the accountability section)
- Real entry points to API and pricing

There is no marketing page that could convey this better. The product is literally the demo.

## What we DO need to write (as content)

Even with no separate marketing site, we need:

1. **About page** (`/about`) — governance, team, history, manifesto
2. **Different page** (`/different`) — the L174 positioning page
3. **Methodology page** (`/methodology`) — the catalog of all model methodologies
4. **Pricing page** (`/pricing`) — tiers, FAQ
5. **API docs** (`/api`) — developer reference
6. **MCP install** (`/mcp`) — host-specific snippets

These are content. They are not "marketing pages." Users read them when they want to understand a specific dimension of the product.

## SEO strategy

Organic discovery → product page, not landing page.

| Query | Landing |
|---|---|
| "open Bloomberg alternative" | `/different` |
| "US CPI forecast" | `/indicator/cpi-yoy?countries=usa` |
| "what is the GDP nowcast" | `/indicator/gdp-nowcast?countries=usa` |
| "OPENGEM API" | `/api` |
| "OPENGEM MCP" | `/mcp` |
| "Bloomberg vs OPENGEM" | `/different` |
| "open macro forecasts" | `/` |

Each landing page is the *real product* for that query.

JSON-LD structured data per page (per L107) ensures Google Knowledge Graph indexes us correctly.

## The "Get started" CTA

A small persistent banner for first-time visitors:

```
   ┌──────────────────────────────────────────┐
   │  New here? See what makes OPENGEM         │
   │  different from Bloomberg.   [Tour →]     │
   │                              [Dismiss ×]  │
   └──────────────────────────────────────────┘
```

Dismisses on click. Persists in localStorage. Not aggressive.

## The 60-second tour

Click "Tour →" → opens a guided 60-second walkthrough overlay:

1. "This is the world dashboard."
2. "Click any country to drill in."
3. "Every forecast is vintaged."
4. "The methodology is open."
5. "The track record is public."
6. "Use it via MCP from ChatGPT or Claude."
7. "API is free for prosumers, paid for high-volume."

7 cards, each ~5 seconds of reading.

Implementation: a tour library (Driver.js or custom). Cancellable. Doesn't block interaction.

## Pricing page (`/pricing`)

Separate from the home page but as plain as possible:

```
   Pricing
   ─────────────────────────────────────
   Free            Pro $99/mo     Throughput $499/mo    Enterprise
   ────────       ────────       ──────────────       ──────────
   - Dashboard    - All of free   - All of pro         - SOC 2
   - 200 req/min  - 1k req/min    - 10k req/min        - Custom
   - 5k req/day   - 50k/day       - 1M/day             - SLA
   - All embeds   - White-label   - Throughput         - Contract
   - All feeds    - Alerts        - Webhooks           - DPA
```

A small FAQ. A pre-filled email link for Enterprise inquiries.

No urgency-marketing. No "limited time" tier. No "save 20% annual." We charge for value, not for psychological pressure.

## About page (`/about`)

Plain. Maintainer name, contact, governance:

```
   OPENGEM is built by Edgardo Muñoz in collaboration
   with [TBD contributors].

   The project's governance is:
    - Edgardo is the BDFL for V1 (years 1-3).
    - From V2 onward, a 3-person steering committee.
    - Methodology decisions are open to comment via GitHub.

   Code: github.com/opengem
   Data: data.opengem.app (CC-BY-4.0)
   Contact: hello@opengem.app
```

Plus changelog, roadmap, press kit.

## Press kit (`/about/press`)

Logo + brand assets + screenshots + 1-paragraph "what is OPENGEM" + contact. The basics.

## Onboarding flow

When a user lands and is not logged in:
- They see the dashboard with full data (no walls)
- A small persistent "Get API key" CTA in the top-right
- The first-visit banner with the "Tour →" link
- Optional sign-up at any time for personalization

When a user signs up:
- 3-step flow per L139
- Lands on their personalized home

We never gate the dashboard behind sign-up. That's the thesis.

## Conversion funnel

The funnel is implicit:

1. Anonymous user → sees value in the dashboard
2. Some users → want to save a view or watchlist → sign up for free account
3. Some signed-up users → hit free-tier rate limit on API → upgrade to Pro
4. Some Pro users → embed in their workflow → upgrade to Throughput
5. Some Throughput users → need SLAs → become Enterprise

No surprise gates. No fake urgency.

## Implementation

- Single Next.js app
- Single Tailwind theme
- Public + auth-gated routes in the same app
- `/api/*` and `/mcp/*` are part of the same app
- One repo, one deploy

No `marketing/` subdirectory, no separate Webflow site, no Wix landing pages.

## The "should we hide methodology" question

We won't. The methodology pages, the accountability page, and the data pages are all public and indexed. We never hide the substance behind "for paid users only."

The only thing paid: rate, alerting, white-label, webhooks, support.

## Comparison: how other dashboards do it

- **Bloomberg**: bloomberg.com is marketing; the terminal is the product. We don't accept this.
- **Stratfor**: stratfor.com is marketing + editorial preview; the data is paywalled. We don't accept this.
- **TradingEconomics**: tradingeconomics.com is the product + marketing as one. Closer to our model — but they ad-pollute.
- **OurWorldInData**: ourworldindata.org is the product with no marketing layer. Our model.
- **FRED**: fred.stlouisfed.org is product + minimal marketing. Our model.

We're in the OWID / FRED tradition: product = marketing.

## The asymmetric move

Every $25K/seat terminal hides behind a marketing-and-sales gate. OPENGEM's front door is the product. A journalist Googling "US CPI" finds OPENGEM's CPI page on the first page of results and pastes the URL into their article without ever signing up.

That's the distribution moat. No sales team needed. The product *is* the funnel.

## Mobile

The home dashboard is mobile-responsive. Cohort grid stacks. Feed appears below. Same content. No separate mobile landing page.

## Internationalization (V2)

When i18n lands (L118):
- Locale via URL: `/?lang=es`, `/?lang=de`, `/?lang=ja`
- Same pages, translated copy
- Numbers/dates localized
- No separate locale-specific marketing site

Single domain. Single product. Many locales.

## What we won't ever build

- A "request a demo" form. The product IS the demo.
- A "free trial" of paid tier. Free tier exists permanently.
- A "Coming soon!" splash for future features. Either it's shipped or it's not.
- A logo carousel of "trusted by." Real users will appear in case studies (per L292/L293), not as logos on the home page.
