# L146 — Iconography System

**Loop**: 146 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## Decision

**Pick: Lucide Icons (the maintained fork of Feather Icons) as the primary family.**

Reasons, decisively:

1. **License**: ISC. Trivial. No attribution friction for embeds.
2. **Library size**: ~1,400 glyphs covering 99% of dashboard needs. Tabler has more (4,000+), but we don't need them; we need a smaller, opinionated set so designers stop bikeshedding.
3. **Stroke style**: 2px stroke at 24px nominal — reads as "instrument," not "brand." Bloomberg terminals are 1px hairlines; we go 2px because the modern HiDPI screen wants more weight. Feather's 1.5px is too thin on dark mode.
4. **Lucide vs Tabler**: Tabler has duplicate variants (filled + outline) which seduces inconsistency. Lucide is outline-only. Discipline.
5. **Tree-shakeable**: each icon is a separate React component. `lucide-react` is the canonical binding. Zero runtime overhead for unused icons.
6. **MCP angle**: when an LLM agent renders an OPENGEM-embedded view, it can reference icon names by string and the dashboard resolves them. Lucide's names are stable.

Rejected alternatives: Heroicons (too marketing-y), Phosphor (too playful, weighted strokes feel "consumer"), Tabler (too many, dilutes the visual language), Bootstrap Icons (dated), custom (we are one developer; don't bikeshed).

## Sizing scale

| Slot | Size | Stroke | Use |
|---|---|---|---|
| `icon-xs` | 12px | 1.5px | inline with caption text |
| `icon-sm` | 16px | 1.75px | inline with body / table cell |
| `icon-md` | 20px | 2px | toolbar buttons, tab headers |
| `icon-lg` | 24px | 2px | section headers, empty-state nudges |
| `icon-xl` | 32px | 2.5px | hero placements, splash empty states |
| `icon-2xl` | 48px | 3px | onboarding illustrations |

Stroke linecap: `round`. Stroke linejoin: `round`. (Lucide default.)

Color: inherits `currentColor`. Never bake hex.

## The 60-icon catalog

OPENGEM uses exactly these. If a designer needs a 61st, they file a ticket and we negotiate.

### Navigation (8)
| # | Lucide name | Used for |
|---|---|---|
| 1 | `house` | Home |
| 2 | `globe` | World / countries index |
| 3 | `line-chart` | Indicators index |
| 4 | `git-branch` | Scenarios index |
| 5 | `crystal-ball` (custom — Lucide has no exact match; use `sparkles`) | Forecasts index |
| 6 | `newspaper` | News / events |
| 7 | `book-open` | Methodology / docs |
| 8 | `settings` | Settings |

### Indicator types (10)
| # | Name | Indicator |
|---|---|---|
| 9 | `trending-up` | GDP |
| 10 | `flame` | CPI (inflation) |
| 11 | `briefcase` | Unemployment |
| 12 | `landmark` | Policy rate |
| 13 | `package` | Trade / exports |
| 14 | `coins` | Reserves |
| 15 | `factory` | Industrial production |
| 16 | `home` | Housing |
| 17 | `ship` | Shipping / supply chain |
| 18 | `zap` | Energy |

### Data semantics (10)
| # | Name | Meaning |
|---|---|---|
| 19 | `arrow-up-right` | Surprised positive / beat |
| 20 | `arrow-down-right` | Surprised negative / miss |
| 21 | `arrow-right` | In line with consensus |
| 22 | `circle-dot` | Latest vintage marker |
| 23 | `history` | Vintage / time-machine |
| 24 | `git-compare-arrows` | Compare 2 |
| 25 | `target` | Forecast / point estimate |
| 26 | `waves` | Confidence band / fan |
| 27 | `alert-triangle` | Warning / methodology caveat |
| 28 | `info` | Info / methodology pop-up trigger |

### Geopolitics (8)
| # | Name | Use |
|---|---|---|
| 29 | `swords` | Conflict |
| 30 | `handshake` | Alliance / deal |
| 31 | `gavel` | Sanctions / policy |
| 32 | `flag` | Country flag wrapper |
| 33 | `vote` | Election |
| 34 | `radio-tower` | News pulse |
| 35 | `siren` | High-alert event |
| 36 | `map-pin` | Geo-point |

### Actions (10)
| # | Name | Action |
|---|---|---|
| 37 | `search` | Search / command palette |
| 38 | `share-2` | Share view |
| 39 | `download` | Export (PNG/CSV/PDF/Notebook) |
| 40 | `link` | Copy permalink / cite-this-view |
| 41 | `bookmark` | Watchlist add |
| 42 | `bell` | Alerts |
| 43 | `pencil` | Annotate |
| 44 | `eye` | View as / preview |
| 45 | `code` | Open JSON / open in notebook |
| 46 | `external-link` | Outbound source link |

### State / status (8)
| # | Name | Meaning |
|---|---|---|
| 47 | `check-circle-2` | Confirmed / on-track |
| 48 | `x-circle` | Failed / discontinued series |
| 49 | `clock` | Stale data |
| 50 | `loader-2` | Loading (spinner role) |
| 51 | `wifi-off` | Adapter down |
| 52 | `circle-help` | Glossary tooltip trigger |
| 53 | `lock` | Auth-gated / paid feature |
| 54 | `gauge` | Calibration / scoring |

### Editorial / brand (6)
| # | Name | Use |
|---|---|---|
| 55 | `scroll-text` | Ledger / accountability page |
| 56 | `microscope` | Methodology page |
| 57 | `library` | Citation / references |
| 58 | `feather` | Annotation / writer view |
| 59 | `binary` | Raw data / API |
| 60 | `plug` | MCP / integrations |

## Custom additions (deferred)

If we need anything Lucide lacks (e.g., a true "crystal ball"), we add a one-off SVG to `/lib/icons/custom/*.tsx` matching Lucide's API: `<Icon size strokeWidth className>`. Custom icons must be reviewed by Edgardo. No drift.

## Rendering contract

```tsx
import { TrendingUp } from "lucide-react"

<TrendingUp size={20} strokeWidth={2} className="text-good-500" aria-hidden />
```

- `aria-hidden` by default; meaningful icons get an explicit `aria-label`.
- Icons paired with text never need a label.
- Icons standing alone (icon-only buttons) MUST have `aria-label` and a tooltip (see L150).

## Storybook / iconpicker

A single page at `/_design/icons` lists all 60 with names, sizes, and copy-to-clipboard JSX. This is the source of truth.

## Update policy

Lucide ships releases monthly. Pin a minor version (`^0.X`). Upgrade quarterly. Never silently swap a glyph.
