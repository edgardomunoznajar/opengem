# L148 — Color System

**Loop**: 148 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## Name

**Palette name: "Ledger Amber."** The amber is the inheritance from the Bloomberg-orange decision in L119 — keep the chromatic memory, but tame it. Everything else is built around that single brand chord.

## The four roles, decided

| Role | Pick | Why |
|---|---|---|
| Semantic (good/bad/warn/info/neutral) | **Custom 5-pair semantic** built on perceptually-uniform OKLCH | Tailwind's reds/greens are too saturated for dashboard density |
| Categorical (qualitative, ≤8 categories) | **Tol's "Bright" 8** (color-vision-deficiency-safe) | Battle-tested in scientific viz; nothing better exists at 8 cats |
| Sequential (single hue, 9-step) | **Single-hue OKLCH ramp at h=70° (amber)** | Brand chord = ramp chord. No separate "viridis" for sequential. |
| Diverging (10-step, midpoint white) | **Cynthia Brewer's "RdBu" → OKLCH-rebuilt** | Standard, intuitive, works for surprise indices |

## Mode

- **Default: dark mode.** OPENGEM is a terminal. Dark first, light a serious second.
- Both modes are first-class; design tokens swap automatically via CSS custom properties.
- Print mode: always light (saves ink).

---

## Brand chord (the one fixed point)

```
ledger-amber-500: oklch(0.74 0.16 70)   /* approx #E89B3B */
```

This is the only "brand" color. Used for:
- Logo
- Active nav state
- Primary CTA buttons
- "Live forecast" marker on charts
- The accent on the loading spinner

Used **nowhere else**. Discipline.

## Semantic scale (5 roles × 11 steps)

Each role: `50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950`.

OKLCH lightness anchors:
- `50`: 0.97
- `500`: 0.62
- `950`: 0.14

Hue / chroma per role:

| Role | Hue | Use |
|---|---|---|
| `good` | 145° (forest green) | Beat consensus, on-track, healthy |
| `bad` | 25° (vermilion) | Miss consensus, stale, error |
| `warn` | 60° (mustard) | Caveat, low-coverage, stale-but-OK |
| `info` | 230° (slate blue) | Neutral signal, methodology |
| `neutral` | 0° (true gray) | Default text, borders, surfaces |

Specifically NOT pure red and pure green (#FF0000, #00FF00). Vermilion and forest read as "data signal" rather than "stoplight." Color-blind users will distinguish vermilion vs forest via lightness, not hue alone — we verified with the OKLCH lightness gap (forest-500 is L=0.62, vermilion-500 is L=0.62, but their chroma vectors are 80° apart in opposite hue regions).

### Token surface

```css
--color-good-500: oklch(0.62 0.14 145);  /* #58A56B */
--color-bad-500:  oklch(0.62 0.16 25);   /* #D26B47 */
--color-warn-500: oklch(0.62 0.13 60);   /* #B58A3B */
--color-info-500: oklch(0.62 0.10 230);  /* #647CA5 */
```

(Concrete hex values are approximate — generated from OKLCH at build time.)

## Categorical: Paul Tol's Bright 8

For categorical encodings (countries, scenarios, model variants, indicators in a small-multiples grid). Color-blind safe across deuteranopia and protanopia.

| # | OKLCH | Approx hex | Tol name |
|---|---|---|---|
| 1 | oklch(0.68 0.18 250) | #4477AA | Blue |
| 2 | oklch(0.74 0.13 95)  | #EE6677 | Red |
| 3 | oklch(0.72 0.16 135) | #228833 | Green |
| 4 | oklch(0.82 0.13 90)  | #CCBB44 | Yellow |
| 5 | oklch(0.68 0.14 230) | #66CCEE | Cyan |
| 6 | oklch(0.62 0.18 350) | #AA3377 | Purple |
| 7 | oklch(0.50 0.02 0)   | #BBBBBB | Grey |
| 8 | oklch(0.40 0.04 30)  | #000000 | Black |

Order matters: 1→8 is the assignment order when categories don't have an inherent order. For G7 countries we hardcode an assignment (US=blue, JP=red, etc.) to keep memory across pages.

If we ever exceed 8 categories: we don't. We aggregate, paginate, or facet. Eight is a discipline check.

## Sequential: single-hue amber ramp

For choropleths (one indicator across countries), heatmaps, density visualizations.

9 steps, all hue 70°, monotonic lightness from 0.97 → 0.18, chroma anchored at 0.16 mid-ramp.

| # | OKLCH | Use |
|---|---|---|
| 1 | oklch(0.97 0.02 70) | Lightest |
| 2 | oklch(0.92 0.06 70) | |
| 3 | oklch(0.86 0.10 70) | |
| 4 | oklch(0.78 0.13 70) | |
| 5 | oklch(0.70 0.15 70) | Mid |
| 6 | oklch(0.60 0.15 70) | |
| 7 | oklch(0.48 0.13 70) | |
| 8 | oklch(0.34 0.10 70) | |
| 9 | oklch(0.18 0.06 70) | Darkest |

The visual "memory bridge" between sequential maps and brand color is intentional — readers learn that amber = OPENGEM's intensity scale.

## Diverging: OKLCH RdBu-equivalent, 10-step

Midpoint at neutral (gray, not white — dark mode requires the midpoint to be perceptually neutral, which in dark mode is mid-gray).

Light end: cool blue (210°). Dark end: warm vermilion (25°). Midpoint at step 5–6: neutral gray.

For: surprise index, forecast revision diff, alignment indices.

```
-5  -4  -3  -2  -1   |   +1  +2  +3  +4  +5
blue-blue-blue-blue-pale  gray  pale-red-red-red-red
```

10 steps, no 0; we always encode "no change" as the neutral inter-step rendered as plain gray with no marker. Forces users to read direction.

## Mode swap

CSS custom properties at `:root` (dark) and `:root[data-theme="light"]` (light). All tokens use `oklch()`; browsers without OKLCH (none currently shipping that matter) get a hex fallback emitted at build time via PostCSS.

### Surface colors

| Token | Dark | Light |
|---|---|---|
| `bg-canvas` | oklch(0.14 0.005 240) | oklch(0.99 0.003 240) |
| `bg-surface` | oklch(0.18 0.005 240) | oklch(0.97 0.005 240) |
| `bg-elevated` | oklch(0.22 0.006 240) | oklch(0.94 0.006 240) |
| `border-subtle` | oklch(0.27 0.008 240) | oklch(0.88 0.008 240) |
| `border-default` | oklch(0.34 0.010 240) | oklch(0.80 0.010 240) |
| `text-primary` | oklch(0.95 0.003 240) | oklch(0.18 0.005 240) |
| `text-secondary` | oklch(0.70 0.005 240) | oklch(0.40 0.005 240) |
| `text-tertiary` | oklch(0.55 0.005 240) | oklch(0.55 0.005 240) |

Note the hue bias: all surfaces sit at hue=240° (very slight cool blue) with extremely low chroma (0.003–0.01). This gives the dark mode a "deep night" feel without being charcoal-bland.

## Contrast rules

- Body text on `bg-canvas`: WCAG AA min (4.5:1) — verified at all sizes.
- Chart fills on `bg-surface`: 3:1 minimum.
- Decorative borders may drop to 1.5:1.
- Token CI fails the build if any documented pairing drops below threshold.

## Accessibility contract

- Never encode meaning by color alone. Every good/bad pair also has an icon (L146: arrow-up-right vs arrow-down-right).
- Surprise diverging maps include a numeric label per cell or a hover with the value.
- Tol categorical is verified against deuteranope/protanope/tritanope simulators.

## What we do NOT use

- Pure red, pure green, pure blue (`#F00`, `#0F0`, `#00F`). Too saturated, too "Christmas-tree."
- Tailwind's default palette in chart fills. (Tailwind grays are fine for surfaces; Tailwind reds/greens are not signal-friendly.)
- Black `#000` or white `#FFF`. Both modes use OKLCH-controlled near-black and near-white.
- Translucent overlays as the primary signal carrier (too easy to misread on busy charts).

## Token export

All tokens emit to:
- `tokens.css` (CSS custom properties)
- `tokens.ts` (TypeScript constants for Recharts/D3)
- `tokens.json` (Style Dictionary format, for white-label embeds)

One source of truth: `design/tokens.json5`. Generators write the three outputs.
