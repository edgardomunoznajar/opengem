---
loop: 128
phase: 3
title: Universal Search / Command-Bar UX
date: 2026-06-06
status: decided
---

# L128 — Universal Search / Command-Bar UX

**Loop**: 128 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The brief

Design the keyboard-driven search and command bar. The terminal-feel power-user surface. The thing that distinguishes OPENGEM from a navigation-only dashboard. List all commands.

## The opening move

The command bar opens with `⌘K` (Mac) or `Ctrl-K` (everywhere else). It also opens by clicking the search icon in the header. Once open, it captures keyboard focus and intercepts every keystroke until dismissed (Escape or click-outside).

The bar lives as a centered modal at top-third of the viewport. Width: 720px on desktop, full-screen on mobile. Background: dimmed overlay (rgba 0,0,0,0.6) over the page underneath.

```
+------+------------------------------------------------------+
|  ⌘K  |  > search countries, indicators, scenarios...        |
+------+------------------------------------------------------+
|  COUNTRIES (fuzzy: "uni stat" → United States)              |
|    🇺🇸 United States                                          |
|    🇰🇼 United Arab Emirates                                  |
|    🇬🇧 United Kingdom                                        |
+-------------------------------------------------------------+
|  INDICATORS                                                  |
|    CPI YoY                                                  |
|    Unemployment rate                                        |
+-------------------------------------------------------------+
|  SCENARIOS                                                  |
|    Trade-LATAM (fired today)                                |
+-------------------------------------------------------------+
|  COMMANDS                                                   |
|    > compare USA EZ                                          |
|    > rewind 2024-09                                          |
+-------------------------------------------------------------+
| ↑↓ navigate · ↵ open · Tab cycle category · Esc dismiss     |
+-------------------------------------------------------------+
```

## Modes

The bar has three modes, switched implicitly by the first character of the query:

1. **Search mode** (default, alpha character): query is a fuzzy-search across countries, indicators, scenarios, forecasts, events. Results group by category.
2. **Command mode** (`>` first character): query is parsed as a command. Autocomplete suggests command names. Tab autofills.
3. **URL mode** (`/` first character): query is interpreted as a URL fragment for direct navigation. E.g., `/c/USA/cpi` → navigate to that page.

## The fuzzy search ranking

Fuzzy match uses a typo-tolerant trigram + scored ranking:
- Exact-prefix match: +100
- Exact word boundary match: +50
- Trigram overlap: +1 per overlap
- Category boost: countries (+20), scenarios fired today (+30), watchlist items (+10)
- Recent visit boost: +15 if visited in last 7 days
- Penalty for length differential vs query: -1 per char

Top 5 per category, max 4 categories visible. Press Tab to cycle to "more in this category" view.

## The command catalog

Commands are the power-user surface. Each command has a slash-style autocomplete name, optional positional args, and optional flags.

### Navigation commands

- `> go {country|indicator|scenario|forecast}` — navigate to a record. E.g., `> go USA` → /c/USA.
- `> home` — return to /.
- `> back` — browser back.
- `> recent` — show last 10 pages visited.
- `> watchlist` — open watchlist drawer.

### Comparison commands

- `> compare {a} {b}` — open Compare-2 view (L129). E.g., `> compare USA EZ`.
- `> compare {indicator} {a} {b}` — comparison locked to one indicator. E.g., `> compare cpi USA EZ`.
- `> diff {forecast} {vintage1} {vintage2}` — show forecast revision diff. E.g., `> diff cpi/USA/4Q 2026-03-02 2026-06-02`.

### Vintage commands

- `> rewind {date}` — set the global vintage to {date}. All open charts re-render at that vintage.
- `> rewind {step}` — relative step backward. E.g., `> rewind -1m` (one month earlier).
- `> latest` — reset global vintage to latest available.
- `> play [speed]` — animate vintage rewind across all charts.

### Watchlist commands

- `> watch {record}` — add to watchlist. E.g., `> watch USA`, `> watch trade-latam`.
- `> unwatch {record}` — remove.
- `> watchlist clear` — empty.
- `> watchlist share` — generate share URL for current watchlist.
- `> watchlist load {url|name}` — load a shared or named watchlist.
- `> watchlist new {name}` — start a fresh named watchlist.

### Alert commands

- `> alert {record} {condition}` — set an alert. E.g., `> alert cpi/USA gt 4%`.
- `> alerts` — open alerts page.
- `> mute {alert-id}` — temporarily mute.

### Scenario commands

- `> trigger {pack-id}` — manually simulate trigger (premium tier only; sandboxed counterfactual).
- `> packs` — list all scenario packs.
- `> packs fired` — list packs fired today.
- `> packs armed` — list packs armed (close to firing) today.

### Export / cite commands

- `> cite {url|current}` — generate a citation block (BibTeX, plain text, DOI-style).
- `> export {format}` — export current view. Formats: png, svg, csv, json, pdf.
- `> embed {size}` — generate embed code. Sizes: square, banner, tall.
- `> notebook` — export current view as Jupyter notebook.

### Subscription commands

- `> subscribe {topic}` — subscribe to a topic via email/RSS. E.g., `> subscribe scenarios:fired`.
- `> unsubscribe {topic}` — opposite.
- `> rss` — show RSS catalog.

### API commands

- `> api {record}` — show API endpoint for the current record.
- `> mcp install` — show one-click MCP server install for ChatGPT/Claude/Gemini.
- `> token` — manage API tokens (logged-in only).

### Settings commands

- `> theme {orange|pink|blue}` — switch theme (L145).
- `> dark` / `> light` — toggle color mode within current theme.
- `> dense` / `> roomy` — toggle data density.
- `> shortcuts` — show keyboard shortcut cheatsheet.
- `> help` — open command bar help.

### Admin / power-user commands

- `> ledger {indicator}/{horizon}` — jump to a track-record cell.
- `> leaderboard {indicator}/{horizon}` — open forecaster leaderboard.
- `> backtest {record}` — open backtest harness for a record.
- `> replay {forecast-id}` — trigger replay-and-diff CI job.

### Discovery commands

- `> packs:fired-today` — instant filter.
- `> revisions:large-today` — forecasts that moved >0.1pp.
- `> events:high-severity-24h` — high-impact events.
- `> watchlist:movers` — watchlist items that moved today.

## Keyboard shortcuts (global, outside the bar)

The bar opens with `⌘K`/`Ctrl-K`. Beyond that, every page binds a small set of shortcuts:

- `?` — open shortcut cheatsheet.
- `g w` — go to World (/) (vim-style chord).
- `g c` — go to Countries.
- `g i` — go to Indicators.
- `g s` — go to Scenarios.
- `g f` — go to Forecasts.
- `g l` — go to Ledger.
- `c` — open Compare-2.
- `w` — toggle current record on watchlist.
- `a` — open alerts dialog for current record.
- `m` — toggle methodology drawer.
- `v` — toggle vintage rewind controls.
- `t` — toggle theme.
- `?` — shortcut cheatsheet.
- `e` — export current view.
- `/` — focus search (alternative to ⌘K, vim-style).
- `j` / `k` — next / previous item in any list (vim).

These bindings are remappable in `/settings/shortcuts` (L152 designs the remapping UI).

## URL-mode navigation

Typing `/` as the first character flips to URL mode. The bar autocompletes path segments. Useful for keyboard navigation:

- `/c/USA` → United States page.
- `/i/cpi/USA` → CPI for the United States.
- `/s/trade-latam` → scenario page.
- `/f/cpi-yoy/USA/4Q` → forecast page.
- `/v/2024-09-15` → set global vintage.

Tab autocomplete steps through valid path segments using the catalog.

## Empty state

When the bar opens with no query, show a curated empty state:

```
+------------------------------------------------------+
| ⌘K · what's on your mind?                            |
+------------------------------------------------------+
|  RECENT (last 7 days)                                |
|    /c/USA       2 hours ago                          |
|    /i/cpi-yoy   yesterday                            |
|    /s/trade-latam   yesterday                        |
+------------------------------------------------------+
|  WATCHLIST                                          |
|    🇺🇸 USA                                            |
|    🇪🇺 EUR                                            |
|    CPI YoY                                          |
|    Trade-LATAM                                      |
+------------------------------------------------------+
|  TRY                                                 |
|    > compare USA EZ                                  |
|    > rewind 2024-09                                  |
|    > packs:fired-today                               |
|    > help                                            |
+------------------------------------------------------+
```

## Search across what

The fuzzy search indexes:
- All countries (ISO 3166 + common names + autonyms + previous names).
- All indicators (canonical name + abbreviations + EconLit synonyms).
- All scenario packs (name + tagline + common triggers).
- All forecasts (computed from indicator × country × horizon).
- All events (last 90 days, by headline + entity tags).
- All Ledger cells (per-indicator-per-horizon track records).

Index size at Block I: ~26 countries × 50 indicators × 5 horizons + ~20 scenario packs + ~10k events + ~26 × 50 × 5 ledger cells = ~17,000 documents. Trivially fast as a client-side fuse.js or fzf-like index (≤200KB gzipped).

By Block II (40+ countries) and Block IV (public-data-as-standard, full coverage): ~100,000 documents. Switch to server-side typesense or meilisearch.

## Accessibility

The bar is fully keyboard-navigable. Screen-reader announcements:
- "Command bar open. Type to search. Up/down arrow to navigate. Enter to select. Tab to cycle category. Escape to dismiss."

Results have ARIA roles (combobox + listbox + option). The active result is announced as the user navigates.

## What this loop produced

- Command bar opens with `⌘K`/`Ctrl-K` and is the keyboard-first surface.
- Three modes by first character: search (alpha), command (`>`), URL (`/`).
- Full command catalog (~50 commands across 8 categories: navigation, compare, vintage, watchlist, alerts, scenarios, export, subscription, API, settings, admin, discovery).
- Global keyboard shortcut binding (vim-style chords for go-to navigation).
- Fuzzy search ranking: trigram + boosts (category, scenarios-fired-today, watchlist, recent visits).
- Empty state shows recent + watchlist + suggested commands.
- Index size estimate at Block I (~17k docs, client-side) → Block IV (~100k docs, server-side).
- Accessibility: ARIA combobox + screen-reader announcements.

## What comes next

- **L129** designs Compare-2 mode (invoked via `> compare`).
- **L130** designs Watchlist UX (invoked via `> watch`).
- **L131** designs Alerts UX (invoked via `> alert`).
- **L152** designs keyboard shortcut remapping.
- **L153** designs the command palette catalog page (`> help` lands here).

## Related

- [[L121-information-architecture]] — search lives in the header
- [[L129-compare-2-mode]] — invoked via command bar
- [[L130-watchlist-ux]] — invoked via command bar
- [[L131-alerts-ux]] — invoked via command bar
- [[L152-keyboard-shortcuts]] — global shortcuts catalog
- [[L153-command-palette-catalog]] — long-form command reference
