---
loop: 140
phase: 3
title: Empty States — Catalog Across Every Page
date: 2026-06-06
status: decided
---

# L140 — Empty States: Catalog

**Loop**: 140 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The brief

Catalog every empty state on every page. Each empty state must serve three jobs:

1. **Explain** what the user is looking at (so they don't think the page is broken).
2. **Suggest** what they could do next (so they have a path forward).
3. **Match the voice** of OPENGEM (terse, dated, honest — never apologetic, never cute).

The catalog is the design contract. Every page in the spec has an entry; if a state isn't here, it shouldn't ship.

## Voice rules for empty states

- **Never say "Oops!"** No anthropomorphizing.
- **Never apologize.** Empty is a state, not a failure.
- **State the fact.** "No scenarios firing today" not "Looks like things are quiet!"
- **Offer ONE next step.** If there are two next steps, the empty state is doing too much.
- **Date things when they were last non-empty.** "No fires today. Last fire: 2 days ago."

## The catalog

### Home / World page

**State A — first-time visitor with no watchlist**

```
+----------------------------------------------------+
| 🌐 Welcome to OPENGEM World Dashboard               |
|                                                    |
| Today: 2026-06-06 06:00 UTC                        |
| 4 scenarios fired · GPR 132 · World CPI 4.1%       |
|                                                    |
| HEADLINE (everyone sees this)                      |
| "Trade-LATAM and Red-Sea packs fired; EZ           |
|  recession risk +3pp"                              |
|                                                    |
| STRIP (everyone sees this)                         |
| [6 headline numbers]                                |
|                                                    |
| YOUR PERSONALIZED VIEW (empty here)                |
|                                                    |
| You don't have a watchlist yet.                    |
|                                                    |
| Pick a preset to start:                            |
|   🌐 G7 Watch    🌐 G20 Watch    🌐 BRICS+         |
|   📊 Recession   📊 Inflation                       |
|                                                    |
| Or build your own → [open watchlist]               |
+----------------------------------------------------+
```

The page still shows the public global readout (headline + strip + global stream). The personalized half is empty with one CTA.

**State B — all scenarios calm, watchlist active**

```
| YOUR WATCHLIST                                     |
|                                                    |
| 🇺🇸 USA       GDP 2.4% ▼ · CPI 2.9% ▼ · RecProb 34%▲|
| 🇪🇺 EUR       GDP 0.6% ▲ · CPI 2.4% ▼ · RecProb 41%▲|
|                                                    |
| Today's scenarios for your watchlist               |
|                                                    |
| No scenarios firing today.                         |
| Last fire affecting your watchlist: 4 days ago,    |
| Trade-LATAM (affected EUR).                        |
|                                                    |
| [view full scenario list →]                         |
```

State the fact + reference the last-non-empty date.

**State C — system degradation (data adapter down)**

```
| ⚠️ One or more data adapters is degraded.           |
|                                                    |
| Affected: BLS (US CPI) — last refresh 11 hours ago |
| (normal: 6 hours)                                  |
|                                                    |
| The displayed values use the last successful       |
| vintage. Forecast bands include the staleness in   |
| their uncertainty.                                 |
|                                                    |
| [status page] [stale-data badge details →]         |
```

This isn't strictly empty, but degraded. Same voice rules: state the fact, ref status page.

### Country page

**Empty: country exists in roster but no data this vintage (e.g., a new addition)**

```
| 🇳🇬 NIGERIA                                          |
|                                                    |
| OPENGEM is in roster for Nigeria but does not yet  |
| have a published forecast for this vintage.       |
|                                                    |
| Coverage: indicators 5 of 12 (basic macro).       |
| Forecast horizons: 1Q only.                       |
| Forecasts at 4Q+ will be published when our model  |
| has ≥8 backtested quarters of in-sample fit.       |
|                                                    |
| [What does Tier-T mean? →]                          |
| [Roster status →]                                  |
| [Subscribe to first-publish notification]          |
```

This is the Tier-T (tracked but not vintage-correct) state. Honest about what is missing.

**Empty: indicator tab clicked but no data for country × indicator**

```
| 🇿🇼 ZIMBABWE · Inflation regime classifier           |
|                                                    |
| This indicator is not currently computed for ZWE.  |
| Inflation regime classification requires monthly  |
| CPI vintages going back ≥5 years; ZWE has 14      |
| months of usable vintages.                        |
|                                                    |
| When sufficient vintage depth is available, this   |
| page will be published with a methodology link.    |
|                                                    |
| Estimated availability: 2027-Q3                    |
|                                                    |
| [What is the inflation regime classifier? →]       |
```

Date the future availability.

### Indicator page

**Empty: indicator has no current vintage (paused source)**

```
| Indicator: Trade flows (UN Comtrade)                |
|                                                    |
| The UN Comtrade adapter is temporarily paused      |
| while we migrate to BACI 2026 vintage. Last        |
| successful refresh: 2026-05-12.                    |
|                                                    |
| Expected return: 2026-06-15.                       |
|                                                    |
| [adapter status →] [why we migrated →]              |
```

### Scenario page

**Empty: pack is dormant (has never fired in coverage window)**

```
| Pack: Yemen-Spillover                              |
|                                                    |
| Status: DORMANT — never fired in the backtest      |
| period (2010 to present).                          |
|                                                    |
| Current probability: 0.04                          |
| Trigger conditions: visible below.                 |
| Methodology: published.                            |
|                                                    |
| This pack is published as a watchable but not     |
| currently armed.                                   |
|                                                    |
| [view trigger conditions] [methodology] [history]  |
```

### Forecast page

**Empty: forecast for this vintage doesn't exist yet (upcoming publication)**

```
| Forecast: US CPI YoY 4Q ahead                       |
| Vintage: 2026-06-25 (scheduled)                    |
|                                                    |
| This vintage has not been published yet.          |
| Next publication: 2026-06-25 06:00 UTC.            |
|                                                    |
| Most recent published vintage: 2026-06-02.        |
|                                                    |
| [view 2026-06-02 forecast] [subscribe to publish] |
```

**Empty: forecast does not exist for this combination (no model)**

```
| Forecast: ZWE Inflation 5Y ahead                    |
|                                                    |
| OPENGEM does not currently publish 5Y-ahead         |
| forecasts for ZWE inflation.                       |
|                                                    |
| Reasons:                                            |
|   - ZWE inflation has fewer than 5 years of usable  |
|     vintage history.                              |
|   - L3 backtest does not pass V&V at 5Y for ZWE.   |
|                                                    |
| Closest published forecast: ZWE inflation 1Q.      |
| [view ZWE inflation 1Q]                             |
```

### Event stream page

**Empty: no events match filters**

```
| 0 events match your filters.                       |
|                                                    |
| Filters:                                           |
|   Region: Antarctica                                 |
|   Severity: high                                    |
|   Country: (any)                                    |
|                                                    |
| Loosen the filters:                                  |
|   [clear severity] [clear region] [reset all]      |
|                                                    |
| Last event from this scope: 2024-12-03 (1.5y ago) |
```

Always date the last-non-empty.

### Compare-2 page

**Empty: invalid pair (cross-type)**

```
| Cannot compare /c/USA with /s/trade-latam.         |
|                                                    |
| Compare-2 requires two records of the same type.   |
|                                                    |
| Country vs country: try /compare?a=USA&b=EUR        |
| Indicator vs indicator                              |
| Scenario vs scenario                                |
|                                                    |
| For cross-type relationships, view USA's affected   |
| scenarios at /c/USA.                                |
```

**Empty: comparing record vs itself**

```
| Compare-2 requires two different records.         |
|                                                    |
| Both sides are /c/USA. Pick a second side:         |
|   [country search]                                  |
|                                                    |
| Suggested: 🇪🇺 EUR · 🇨🇳 CHN · 🇬🇧 GBR              |
```

### Watchlist

**Empty: user just created an account, no items**

```
| Your watchlist is empty.                          |
|                                                    |
| Pick from a preset → (10 presets listed)           |
| Or build your own → [search]                       |
```

(Per L130 default state.)

### Alerts page

**Empty: no active alerts**

```
| No active alerts.                                  |
|                                                    |
| Alerts fire when a record crosses a threshold       |
| you set — e.g., "tell me when US CPI exceeds 4%."  |
|                                                    |
| [+ New alert]                                       |
|                                                    |
| Suggested: try alert on your watchlist items       |
|   [set alert on USA recession probability]         |
```

### Track-record page (ledger cell)

**Empty: insufficient vintages**

```
| /ledger/inflation-regime/4Q                         |
|                                                    |
| Insufficient vintages for a publishable track       |
| record. This cell requires ≥8 vintages to evaluate  |
| calibration; we have 3.                            |
|                                                    |
| First publishable evaluation: 2027-Q1               |
|                                                    |
| Until then, this cell is in V&V watch — the         |
| evaluation accumulates but is not published.       |
|                                                    |
| [V&V matrix overview →]                              |
```

### Leaderboard

**Empty: only OPENGEM has coverage**

```
| US CPI YoY · 1Q ahead leaderboard                   |
|                                                    |
| OPENGEM is the only publisher with regular         |
| coverage of this cell at this horizon.            |
|                                                    |
| Other forecasters considered:                       |
|   Cleveland Nowcast — published monthly, included.  |
|   WEO — does not publish at 1Q horizon.            |
|   OECD EO — does not publish at 1Q horizon.        |
|   FRB SEP — quarterly cadence, included.            |
|                                                    |
| Naive baselines (RW, AR(1)) are always included.   |
```

### Methodology page

**Empty: pack published without V&V evidence**

```
| ⚠️ NOT PUBLISHED FOR FORECAST USE — V&V evidence   |
|    insufficient.                                    |
|                                                    |
| Pack: Asteroid-Impact-Macro                        |
|                                                    |
| Methodology page is published for transparency,    |
| but the V&V evidence does not meet the rigor floor:|
|   - Sample size: n=0 historical fires.             |
|   - No baseline comparison possible.               |
|                                                    |
| This pack is a SPECULATIVE TEMPLATE. Probability   |
| outputs should not be used to inform action.       |
|                                                    |
| [why we publish unproven packs anyway →]            |
```

This is the load-bearing honest-failure empty state.

### API / MCP page (rate-limited)

```
| You've reached your free-tier limit (1000 req/day).|
|                                                    |
| Limit resets: 2026-06-07 00:00 UTC (in 7h 23m).   |
| Current cycle used: 1000 / 1000.                   |
|                                                    |
| For more throughput:                                |
|   [Upgrade to Pro: 100k req/day]                    |
|   [Or use the web dashboard]                        |
```

### Settings / Tokens

**Empty: no tokens created**

```
| You have no API tokens yet.                        |
|                                                    |
| Tokens authenticate your API and MCP requests.    |
| Anonymous access has a 1000 req/day cap; with a    |
| token you get the same cap, scoped to your account.|
|                                                    |
| [+ Create a token]                                  |
|                                                    |
| Tokens never expire; revoke at any time.           |
```

### Search (command bar)

**Empty: query matches nothing**

```
| > "foobar"                                           |
|                                                    |
| No results for "foobar".                           |
|                                                    |
| Try:                                                |
|   - A country name (e.g., "United States")         |
|   - An indicator (e.g., "CPI", "GDP")              |
|   - A scenario name (e.g., "trade-latam")          |
|                                                    |
| Or use a command: [> compare] [> watchlist] [> help]|
```

### Embed

**Empty: invalid embed config**

```
| Embed configuration error.                          |
|                                                    |
| Required parameters missing: kind, id, size.        |
|                                                    |
| See docs: /docs/embed                                |
```

(The embed page also has a degraded-state for stale data; see L141.)

## Voice consistency check

Across all empty states above, the voice is:
- Factual ("No scenarios firing today" not "Looks like things are calm!").
- Dated ("Last fire 4 days ago" not "It's been quiet recently").
- One CTA ("Pick a preset" not "Pick a preset, add an indicator, or browse all").
- Honest about why ("Insufficient vintages" not "Coming soon").

If a future page's empty state violates these, the design review rejects it.

## When NOT to render an empty state

Some pages should never render empty:
- World page: always has global headline + strip (even if user-side is empty).
- About / Docs / Pricing pages: always populated.
- Methodology pages: always populated (even for unpublished packs, the methodology renders).

If one of these renders empty, it is a system failure — show the degraded-state copy (L141), not the empty-state copy.

## What this loop produced

- Empty-state catalog across 14 page types (Home, Country, Indicator, Scenario, Forecast, Events, Compare, Watchlist, Alerts, Track record, Leaderboard, Methodology, API/MCP, Settings, Search, Embed).
- Voice rules: state the fact, date the last-non-empty, offer ONE next step, never apologize.
- Special-case empty states for: degraded data adapter (with stale-data flag), insufficient vintages (with future-availability date), V&V-failed packs (with "NOT PUBLISHED FOR FORECAST USE" stamp), rate limit reached.
- Three pages never render empty: World, About-family, Methodology (always show something).
- Design-review rejects voice-rule violations.

## What comes next

- **L141** designs the error / degraded-data states (related but distinct).
- **L264** prototypes empty / loading / error states in code.
- **L171** designs the glossary tooltip integration (links from empty-state explanations).

## Related

- [[L121-information-architecture]] — every page in the IA has an empty-state entry
- [[L122-home-screen]] — home page empty-state (no watchlist)
- [[L139-onboarding-flow]] — onboarding fills the empty watchlist
- [[L141-error-degraded-states]] — sibling concern
- [[L171-glossary-tooltip]] — links from empty-state explanations
