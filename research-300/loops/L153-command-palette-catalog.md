# L153 — Command Palette Catalog

**Loop**: 153 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The contract

The command palette (`mod + k`) is the single most important UI surface in OPENGEM. It's the place where:

- Users type a country, indicator, or scenario name and jump.
- Users invoke commands (save, share, export, alert).
- LLM agents inspect what's available.
- Keyboard shortcuts are discovered.

Every command appears here. If it doesn't, it doesn't exist as a first-class action.

## Anatomy

```
   ┌──────────────────────────────────────────────────┐
   │  ⌘K  Search countries, indicators, commands…     │
   │  ───────────────────────────────────────────────  │
   │                                                   │
   │  ▸ NAVIGATE                                       │
   │     United States                              ↵  │
   │     Germany                                    ↵  │
   │     Inflation (CPI, YoY)                       ↵  │
   │                                                   │
   │  ▸ ACTIONS                                        │
   │     Save current view                       ⌘S   │
   │     Copy permalink                       ⌘⇧L    │
   │     Share as image                            ↵  │
   │                                                   │
   │  ▸ JUMP                                           │
   │     Go to forecasts                          gf   │
   │     Go to leaderboard                        gl   │
   │                                                   │
   │  Esc to close ・ ↑↓ to move ・ ↵ to select         │
   └──────────────────────────────────────────────────┘
```

- Width: 640px, max-height: 480px, scrolls.
- Bg: `bg-elevated`. Heavy shadow.
- Categories collapsed by default if >5 items.
- Results ranked by fuzzy match + recency.
- Keyboard-first: focus enters the input on open. `↑/↓` navigates. `Enter` selects.

## The full command catalog

Eight categories. Roughly 80 commands.

### 1. Navigate (object lookup)

| Command | Synonyms | Action |
|---|---|---|
| Open country | jump to, go to, country, nation | Route to `/country/<iso>` |
| Open indicator | indicator, series | Route to `/indicator/<id>` |
| Open scenario | scenario, pack | Route to `/scenario/<id>` |
| Open forecast | forecast, prediction | Route to `/forecast/<id>` |
| Open methodology | method, methodology, how | Route to `/methodology/<id>` |
| Open news item | news, event, headline | Route to `/news/<id>` |
| Open vintage | vintage, snapshot, asof, as-of | Open vintage drawer |

These are auto-populated. The palette indexes all 220+ countries (ISO-3), ~600 indicators, ~40 scenario packs.

### 2. Jump (route shortcuts)

| Command | Synonyms | Chord |
|---|---|---|
| Go home | home, dashboard | `g h` |
| Go to countries | countries, world | `g c` |
| Go to indicators | indicators, series | `g i` |
| Go to scenarios | scenarios, packs | `g s` |
| Go to forecasts | forecasts, predictions | `g f` |
| Go to leaderboard | leaderboard, scores, rankings | `g l` |
| Go to accountability | accountability, ledger, mistakes | `g a` |
| Go to methodology | methodology, methods, how | `g m` |
| Go to watchlist | watchlist, saved, my | `g w` |
| Go to alerts | alerts, notifications | — |
| Go to API docs | api, docs, openapi | — |
| Go to MCP install | mcp, claude, chatgpt, integration | — |
| Go to pricing | pricing, plans, paid | — |
| Go to about | about, governance, changelog | — |

### 3. Actions on current view

| Command | Synonyms | Chord | Visible only on... |
|---|---|---|---|
| Save view to watchlist | save, bookmark, watchlist add | `⌘S` | Any view |
| Remove from watchlist | unsave, unbookmark | — | Saved view |
| Copy permalink | copy link, share link | `⌘⇧L` | Any view |
| Copy cite-this-view ID | cite, doi, citation | `⌘⇧C` | Any view |
| Share as image (PNG) | png, image, screenshot | — | Chart view |
| Share as GIF (animation) | gif, animation, sequence | — | Chart view |
| Share via oEmbed | embed, oembed | — | Chart view |
| Export to CSV | csv, download, export | — | Data view |
| Export to JSON | json, raw | — | Data view |
| Export to Excel | excel, xlsx | — | Data view |
| Open in notebook (Jupyter) | jupyter, ipynb, notebook, code | — | Data view |
| Open in DuckDB Cloud | duckdb, cloud | — | Data view |
| Print / PDF | print, pdf, tearsheet | — | Any view |
| Annotate | annotate, draw, mark | — | Chart view |
| Compare to… | compare, vs, versus | — | Any view |
| Watchlist add… | watch, follow | — | Country/indicator |
| Alert on… | alert, watch for, notify | — | Indicator |
| Open methodology | method, how | — | Forecast view |
| Open provenance | provenance, source, lineage | — | Any view |
| Toggle bands | bands, p10, p50, p90 | — | Forecast view |
| Toggle consensus overlay | consensus, weo, oecd | — | Forecast view |
| Toggle vintage marker | vintage marker | — | Forecast view |
| Time-machine to date… | rewind, time machine, as of | — | Any view |

### 4. Search (typed)

When a user types a free-text query, results blend across:
- Country names (exact + fuzzy)
- Indicator names + tickers (CPI, GDP, U6, RPI, etc.)
- Scenario names
- Methodology terms (DFM, BVAR, GDPNow)
- News headlines (last 7 days)
- Glossary terms

Ranking: BM25 on name + synonyms, boosted by recency for news.

### 5. Settings & preferences

| Command | Synonyms | Chord |
|---|---|---|
| Toggle theme | dark, light, theme | `⌘D` |
| Toggle sidebar | sidebar, hide | `⌘B` |
| Toggle dense mode | density, dense, compact | — |
| Change locale | language, locale, i18n | — |
| Change number format | number, locale, format | — |
| Change vintage default | default vintage | — |
| Sign in | login, sign-in | — |
| Sign out | logout, sign-out | — |
| Open settings | settings, preferences | `⌘,` |

### 6. Developer / power

| Command | Synonyms |
|---|---|
| Copy JSON of this view | json, raw, debug |
| Show API request for this view | api, request, curl |
| Open OpenAPI spec | openapi, swagger, schema |
| Show telemetry event | event, telemetry, debug |
| Toggle debug overlay | debug, dev |
| Show CDN cache state | cache, cdn |
| Show data freshness | freshness, asof |

### 7. Help

| Command | Synonyms |
|---|---|
| Show keyboard shortcuts | keys, shortcuts, hotkeys |
| Show changelog | what's new, changelog, updates |
| Contact support | support, help, contact |
| Report data issue | bug, issue, problem |
| Suggest indicator | suggest, request |

### 8. Meta (palette commands)

| Command | Synonyms |
|---|---|
| Clear recents | clear, reset |
| Toggle command palette pinned | pin, persistent |
| Open command palette pre-filled | actions on view (`.` shortcut) |

## Synonym matrix (design rule)

Every command has at least 3 synonyms in the index. We tested with:
- Bloomberg-trained users (they type "CPI YOY")
- Stratfor-trained users (they type "geopolitical risk")
- Reddit users (they type "inflation USA")
- LLM-mediated queries (they type "what is the latest US CPI")

The index normalizes to lowercase, strips punctuation, expands acronyms (`CPI` → `consumer price index, inflation`), and supports country code aliases (`US`, `USA`, `United States`, `America`).

## Ranking

Per query:
- 60% weight on string match (BM25 over name + synonyms)
- 20% on recency (commands used in last 7 days)
- 15% on context (commands relevant to current view)
- 5% on global frequency

If no query, show "Recent" + "Suggested for this view" (~10 items total).

## "."  variant — actions-on-this-view

Pressing `.` opens the palette filtered to actions relevant to the current view. The same palette, but with the "Navigate" category collapsed and "Actions on current view" expanded. Saves a typing step.

## Empty state

When no results match: a friendly fallback.

```
  No results for "qatar inflation 2024".
  Did you mean:
   • Qatar CPI (indicator)
   • Open in Compare: QAT × WLD inflation
  Or just open the country: [Qatar →]
```

## Library

Choice: **cmdk** (by Paco Coursey, used by Vercel, Linear, RaycastWeb).

- React, headless, lean.
- Keyboard-first.
- Composable categories.
- Compatible with Radix Dialog.

Wrap as `<CommandPalette>` with OPENGEM theming.

## Indexing strategy

- Static commands compiled into a JS bundle at build time (`commands.gen.ts`).
- Dynamic objects (countries, indicators, scenarios) fetched lazily from `/api/index` on first open, then cached in IndexedDB.
- News items fetched on `mod+k` open (with skeleton state).
- Re-index daily via a background revalidation pass.

Bundle size budget: 25KB gzipped for the static palette index. Dynamic index loads to ~120KB.

## MCP exposure

The MCP server (L108) exposes a `palette.list` tool returning the catalog as structured JSON. LLM agents can pick a command and invoke it by ID. This is how agents drive OPENGEM in chat contexts.
