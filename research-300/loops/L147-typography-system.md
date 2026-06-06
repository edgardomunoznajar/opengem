# L147 — Typography System

**Loop**: 147 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## Decision

**Stack: Inter (sans) + JetBrains Mono (code/numerics) + Source Serif 4 (editorial).**

All three are SIL OFL or Apache-2.0. All three are on Google Fonts and self-hostable. No legal exposure, no licensing reconsideration in five years.

## Why these three

### Inter (sans, primary UI)

- Designed by Rasmus Andersson for screen reading at small sizes — the exact OPENGEM problem.
- Variable font: one file, 100–900 weight, axis-tunable. ~120KB woff2.
- Tabular numerics built in (`font-feature-settings: "tnum"`) — critical for tables.
- Slashed-zero variant (`zero` feature) — disambiguates 0 from O in monetary fields.
- Used by every modern terminal-grade product (Linear, Vercel, Figma) — neutral, not derivative. Reads as "infrastructure," not "brand."

Rejected alternatives: System font stack (too inconsistent across OSes — Windows Segoe vs macOS SF will visibly differ at small sizes), IBM Plex Sans (slightly warmer, but less tabular-discipline), Helvetica/Arial (no tabular variant we can rely on), Geist (still maturing, Vercel-bound).

### JetBrains Mono (mono, numerics + code)

- Specifically designed for code, with ligatures we can disable per surface.
- Excellent at small sizes (14px); other monos blur.
- Same tabular discipline as Inter (built for parity).
- Apache-2.0.

Use cases: tickers, numeric grids, API code blocks, share-token IDs, vintage hashes.

Rejected: SF Mono (Apple-only), Menlo (only ships with macOS), IBM Plex Mono (heavier — fine, but JetBrains feels sharper in dark mode at 13px).

### Source Serif 4 (serif, editorial)

- For the "Why is this different from Bloomberg?" page (L174), methodology essays, the accountability ledger preamble, post-mortem write-ups. Anything that wants to read as *writing* and not *interface*.
- Variable font.
- OFL. Adobe-released, community-maintained.
- Has italic. Has small caps. Has discretionary ligatures we'll opt into for the editorial layout.

Rejected: Charter (too quirky), Lora (too consumer), EB Garamond (too bookish), Source Sans was the alternative non-serif but we already have Inter.

## Type scale

A modular scale with ratio **1.250 (major third)** — slightly tighter than the golden ratio. Tighter scales read as "dense terminal." Reference size: 14px (`text-base`).

| Token | px | rem | line-height | use |
|---|---|---|---|---|
| `text-xs` | 11 | 0.6875 | 1.4 | caption, label, axis tick |
| `text-sm` | 12 | 0.75 | 1.5 | secondary body, table cells |
| `text-base` | 14 | 0.875 | 1.55 | body, default |
| `text-md` | 16 | 1.0 | 1.5 | emphasis body |
| `text-lg` | 18 | 1.125 | 1.45 | subsection headers |
| `text-xl` | 22 | 1.375 | 1.35 | section headers |
| `text-2xl` | 28 | 1.75 | 1.3 | page titles |
| `text-3xl` | 36 | 2.25 | 1.2 | hero numbers (KPI tiles) |
| `text-4xl` | 48 | 3.0 | 1.1 | landing / marketing only |
| `text-mega` | 72 | 4.5 | 1.0 | single-number splash |

Note: base is **14px**, not 16px. This is the explicit terminal decision. Modern dashboards (Linear, Plaid, Stripe) all sit at 14px. The "16px for accessibility" rule applies to long-form reading; dashboards trade density for productivity.

## Weights

| Token | weight | use |
|---|---|---|
| `font-light` | 300 | hero numerics only |
| `font-normal` | 400 | body |
| `font-medium` | 500 | labels, table headers |
| `font-semibold` | 600 | section headers, button labels |
| `font-bold` | 700 | page titles, alert states |

No 800/900 — they look bolder than warranted on Inter at small sizes.

## Editorial scale (serif)

Source Serif appears only in the `<Editorial>` wrapper component. Inside it:

| Token | px | line-height |
|---|---|---|
| `editorial-body` | 17 | 1.65 |
| `editorial-lede` | 22 | 1.45 |
| `editorial-h1` | 36 | 1.2 |
| `editorial-h2` | 28 | 1.3 |
| `editorial-blockquote` | 19 italic | 1.55 |

Max measure: 68ch. Anything wider is illegible.

## Numerics

All numeric values in the UI use `font-variant-numeric: tabular-nums slashed-zero`. Set globally on `<table>`, `.number`, and the chart-overlay components.

For monetary or large numbers (GDP, market cap), use the `.numeric-hero` class which adds `letter-spacing: -0.02em` to tighten:

```
$28.6T   ← Inter, tabular, tight
```

Decimal alignment in tables: use a custom Tailwind utility that renders decimals at a fixed width via `inline-grid` with two columns. Never rely on visual alignment alone.

## Letter-spacing

| Use | tracking |
|---|---|
| Body | 0 (default) |
| Hero numerics | -0.02em |
| All-caps labels (e.g., "GDP YoY") | +0.05em |
| Small caption | +0.01em |

All-caps labels use `font-size: 11px; letter-spacing: 0.08em; font-weight: 500; text-transform: uppercase;` — the canonical "terminal label." Used heavily.

## Line length and rhythm

- Body paragraphs: max 75ch.
- Table cells: no constraint (overflow → ellipsis with tooltip).
- Tooltip body: max 320px wide (~45ch at 13px).
- Methodology pop-up: 2-column layout when viewport > 1024px, else single column at 60ch.

Vertical rhythm: 8px baseline grid. Every margin/padding is a multiple of 4px (allowing half-step) or 8px (preferred).

## Loading strategy

```html
<link rel="preload" as="font" href="/fonts/Inter.var.woff2" type="font/woff2" crossorigin>
<link rel="preload" as="font" href="/fonts/JetBrainsMono.var.woff2" type="font/woff2" crossorigin>
```

Source Serif is **not preloaded** — only routes that mount the `<Editorial>` wrapper pull it. Saves ~80KB on the home dashboard.

`font-display: swap` for sans/mono; `font-display: optional` for serif (we'd rather show fallback than block on editorial-only pages).

Fallback stack (FOUT-resistant):
```css
font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
font-family: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
font-family: "Source Serif 4", Georgia, "Times New Roman", serif;
```

## i18n note

Inter has excellent Latin + Cyrillic + Greek coverage. For Y2 internationalization (L118), we add Noto Sans variants per script. Locked stack now; revisit at L118.

## Hard rules

1. Never set a font-size in raw pixels in component code. Use Tailwind tokens.
2. Never set body line-height below 1.4.
3. Never mix Inter and a system fallback in the same render (preload or accept fallback throughout).
4. Numerics in any chart axis or table cell get tabular-nums. No exceptions.
5. Editorial serif only inside `<Editorial>`. Don't sprinkle it.
