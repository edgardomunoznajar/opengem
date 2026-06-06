---
loop: 121
phase: 3
title: Information Architecture — Top-Level Navigation
date: 2026-06-06
status: decided
---

# L121 — Information Architecture: Top-Level Navigation

**Loop**: 121 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The brief

Pick a top-level navigation for OPENGEM World Dashboard. Five to seven sections, no more. Each section name must be one word (max two) and unambiguous to a 30-second visitor. The navigation must be permanent (header bar), not contextual. It must sketch a URL convention that survives the next five years without renaming.

## The decision

**Six sections**, in this order, left to right:

```
[ OPENGEM ]    World    Countries    Indicators    Scenarios    Forecasts    Ledger        [ Search ⌘K ] [ Watchlist ] [ Sign in ]
```

URL convention:

```
/                                     → World (the home)
/c/{iso3}                             → Country page (e.g., /c/USA)
/c/{iso3}/{indicator-slug}            → Country × indicator drilldown
/i/{indicator-slug}                   → Indicator cross-country page
/i/{indicator-slug}/{iso3}            → Indicator × country drilldown
/s/{pack-id}                          → Scenario pack page
/s/{pack-id}/v/{vintage}              → Scenario at vintage
/f/{indicator}/{iso3}/{horizon}       → Forecast page
/f/{indicator}/{iso3}/{horizon}/v/{vintage}  → Forecast at vintage
/ledger                               → Track record + leaderboard root
/ledger/{indicator}/{horizon}         → Per-cell calibration page
/ledger/scoreboard                    → Forecaster leaderboard
/about                                → Governance, changelog, methodology root
/docs                                 → API + MCP docs
/pricing                              → Tiers
/embed/{type}/{id}                    → Embeddable variants
```

## Why six (and not five, and not seven)

The instinct is to chase five. Five is what Bloomberg's terminal command-line conventions feel like, and five is what dashboard surveys suggest as the perception ceiling. But OPENGEM has a load-bearing claim — "we publish our mistakes" — and that claim has no home if Ledger is collapsed into About or hidden behind Forecasts. The accountability is the brand. So Ledger gets its own permanent slot.

Seven is the next stop and gets tempting fast. The obvious seventh slots — Events, News, Maps, Compare — each can be tucked into the six without losing function. Events live as a stream inside World. Compare is a mode (keyboard-driven, command-bar invoked) that attaches to any pair of records. Maps are a view-mode toggle on Countries and Scenarios. So seven is unnecessary cost on the eye.

## Why these six names (and not the alternatives)

**World** beats Home / Dashboard / Today. "Home" tells you nothing about the product. "Dashboard" overpromises a single-pane-of-glass that the page can't deliver (any honest home screen is an editorial digest). "World" is what the page is — a 10-second readout of the world economy. It lands on the brand promise immediately.

**Countries** beats Geographies / Economies / Markets. "Markets" implies tradeable assets and would confuse the equities-curious. "Geographies" is bureaucratic. "Economies" is technically accurate but academic. Countries is what users type.

**Indicators** beats Series / Variables / Data. "Series" is the FRED word and is right but unfamiliar. "Variables" is the regression word. "Data" is so generic that it tells you nothing. Indicators is the OECD/IMF/World Bank word and the EconLit word — it imports a precise mental model of "named, time-stamped, comparable measures of the economy" without translation.

**Scenarios** is unchallenged. The product has scenario packs as a core concept (per the existing `opengem-scenarios` package), and the dashboard surfaces them as their own first-class object. Calling them "Models" would be misleading (models are the engines behind scenarios). Calling them "Risks" would narrow the meaning (some scenarios are upside).

**Forecasts** is unchallenged. The product publishes forecasts as first-class objects with vintages, bands, and track records. Calling this section "Predictions" or "Outlooks" would soften the commitment.

**Ledger** is the load-bearing choice. The alternatives are Accountability, Track Record, Calibration, Backtest, Scores. Each is more precise but more academic. "Ledger" is the right word because it imports the accounting metaphor — every forecast is an entry, dated, never rewritten, and the running balance is the calibration. It also reads as a verb-adjacent noun ("we ledger our forecasts") which is the active stance the brand wants. It signals open-book.

## What does NOT make the top nav

- **Events / News**. Event stream is the primary content of the World page (lower half) and is reachable from any Country or Scenario page via the "what just happened" rail. Adding Events as a top-level slot would imply the news feed is the product. It is not. The forecasts are the product; events are inputs.
- **Compare**. Compare-2 mode (L129) is a keyboard-invoked overlay, reachable from any record page via `c` keystroke or `/compare?a=...&b=...` URL. Compare is a verb on the navigation, not a noun in it.
- **Search**. Search lives as a permanent header element (`⌘K`), not a tab. The search bar IS the navigation for power users. L128 designs the command-bar fully.
- **About / Docs / Pricing**. These live as right-side footer-tier links in the header (less prominent), or in the footer itself. They are necessary but not part of the daily use loop.
- **My / Profile**. Watchlist is the only personalized surface and lives as a header pill (right side). Profile management lives behind `/settings` (one click from the avatar). No "My OPENGEM" tab.

## The URL convention in detail

The URL is a contract. Every record page must be linkable, addressable, citable, and survive a redesign. The short prefixes (`/c/`, `/i/`, `/s/`, `/f/`) optimize for two things: tweet length and analyst memory. A journalist citing OPENGEM in a story will copy `/c/USA` more readily than `/countries/united-states`. The short prefix also disambiguates: `/c/` cannot be confused with `/i/` even when typed in haste.

Vintage is always `/v/{YYYY-MM-DD}` appended to the canonical record URL. This means every chart, every forecast, every scenario can be addressed at the exact moment it was published. Vintage is OPENGEM's superpower; the URL must encode it cleanly.

The `/ledger` root is a first-class space. Inside it, the canonical address of an accountability cell is `/ledger/{indicator}/{horizon}` — for example `/ledger/cpi/4q`. This is the URL a hedge-fund LP will bookmark. It is the URL a press piece will cite when comparing OPENGEM's calibration against WEO.

The `/embed/` namespace is reserved. Embeds get their own URL space so we never accidentally regress the embed contract during an app-shell rewrite. L144 details the embed sizes; the URL space is here.

## Header behavior at scale

The header is fixed (always visible). On scroll, a secondary contextual breadcrumb slides in below it ("Countries › United States › Inflation") so deep pages stay locatable. On mobile (L142), Indicators / Scenarios / Forecasts collapse into a single Explore tab and the bottom-nav becomes World / Explore / Ledger / Search.

The header is dark by default (terminal-orange theme; see L145) with a thin orange underline on the active section. Hover reveals a flyout for the four data-heavy sections (World, Countries, Indicators, Scenarios) showing pinned items + recent items + "browse all." The flyout is what makes six sections feel like sixty.

## Why this survives Y0 → Y5

Block I ships /c/, /i/, /s/, /f/ for the Tier-V roster (~26 countries). Block II expands the country roster to 40+ without touching the IA. Block III adds API/MCP scale without touching the IA. Block IV adds public-goods dataset hosting without touching the IA — it slots under `/data` (a sub-section of Ledger or the About area, never the top nav). Block V (5-year retrospective) lives as a long-form post under `/about/retrospective`. None of these expansions require renaming a top-level slot.

## What this loop produced

- A six-slot top-level nav: World / Countries / Indicators / Scenarios / Forecasts / Ledger.
- A short-prefix URL convention (`/c/`, `/i/`, `/s/`, `/f/`) with `/v/{date}` for vintage.
- Explicit exclusions (Events, Compare, Search, About) with rationale for each.
- Mobile collapse rule (six → four bottom-nav).
- Header behavior on scroll and flyout pattern.

## What comes next

- **L122** designs the World (home) screen layout against seven candidates.
- **L123** designs the Country page against eight candidates.
- **L128** designs the command-bar that absorbs Compare and Search.
- **L142** designs the mobile-portrait IA reshape.
- **L154** locks the URL convention into a spec.

## Related

- [[L001-vision-statement]] — the brand promise that requires Ledger as a top-level slot
- [[L122-home-screen]] — World page populates the / route
- [[L128-search-command-bar]] — the ⌘K layer that absorbs Compare
- [[L142-mobile-information-density]] — six-slot nav collapses to four on portrait
- [[L154-url-convention]] — formalizes this URL contract
