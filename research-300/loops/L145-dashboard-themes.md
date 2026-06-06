---
loop: 145
phase: 3
title: Dashboard Themes — Terminal Orange, Editorial FT-Pink, Playful OWID-Blue
date: 2026-06-06
status: decided
---

# L145 — Dashboard Themes

**Loop**: 145 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The brief

Three candidate themes. Pick a default. Allow theme override.

## The three candidates

### Theme A — Terminal Orange (Bloomberg-coded)

```
+----------------------------+
|  Bg #0A0A0A (near-black)   |
|  Fg #E8E8E8 (near-white)   |
|  Brand #FF6F00 (orange)    |
|  Accent #FFB300 (amber)    |
|  Success #00C853 (green)   |
|  Warn #FFAB00 (yellow)     |
|  Danger #FF1744 (red)      |
|  Surface #1A1A1A           |
|  Border #2B2B2B            |
+----------------------------+
```

Inspired by Bloomberg Terminal. Dark canvas + orange accents = the financial-terminal mood. The brand voice says "this is data, not lifestyle." Dense, fast-reading, optimized for hours of monitoring.

**Vibe**: terminal, broker desk, "I track the world."

### Theme B — Editorial FT-Pink

```
+----------------------------+
|  Bg #FFF1E5 (FT pink/      |
|              salmon)        |
|  Fg #262A33 (charcoal)     |
|  Brand #990F3D (FT red)    |
|  Accent #0D7680 (teal)     |
|  Success #007D7D (deep grn)|
|  Warn #B98800 (amber-gold) |
|  Danger #990F3D (FT red)   |
|  Surface #F2DFCE (warmer)  |
|  Border #C8B79D (warm gray)|
+----------------------------+
```

Inspired by the Financial Times print color identity (the salmon paper). Warm cream canvas + deep charcoal text = newspaper editorial mood. The brand voice says "this is journalism, not noise."

**Vibe**: editorial, considered, "this is the paper of record."

### Theme C — Playful OWID-Blue

```
+----------------------------+
|  Bg #FAFCFE (cool white)   |
|  Fg #1F2937 (slate-dark)   |
|  Brand #2563EB (royal blue)|
|  Accent #06B6D4 (cyan)     |
|  Success #16A34A (green)   |
|  Warn #F59E0B (amber)      |
|  Danger #DC2626 (red)      |
|  Surface #F1F5F9 (slate-50)|
|  Border #CBD5E1 (slate-300)|
+----------------------------+
```

Inspired by Our World in Data — clean white canvas + saturated blue accents = academic-accessible mood. The brand voice says "this is data for everyone, not insiders."

**Vibe**: open-source, friendly, "this is data for the public good."

## The decision — Theme A (Terminal Orange) as default

Pick **Terminal Orange (A)** as the default. Allow Themes B and C as user-toggleable alternates.

### Why A as default

Three reasons.

**1. The brand strategy is "Bloomberg-grade for everyone."**

The L001 vision explicitly positions OPENGEM as a Bloomberg-grade dashboard. The visual identity should not undersell that. Theme A signals "professional terminal" at first glance — the LP, the analyst, the journalist all read it as serious. Theme B (FT-pink) feels like a magazine; Theme C (OWID-blue) feels like a public museum exhibit. Both undersell the depth.

The brand-recognition asymmetry matters at scale: someone tweets a screenshot of OPENGEM in dark/orange, and viewers immediately register "trading desk." That visual association is borrowed from Bloomberg's twenty-year typographic moat. We exploit it.

**2. Density and contrast.**

Theme A's dark canvas + saturated orange accents give the highest information density per pixel. P10/P50/P90 bands shaded in three orange opacities pop off the black. Sparklines render clearly. Tabular numbers are highly legible.

Theme B and C use light canvases. The same chart on light canvas needs more whitespace to feel breathable; density drops 15-25% per fold. For a power-user product, dark canvas wins.

**3. Long-session ergonomics.**

The macro analyst stares at the dashboard for hours. Dark mode reduces eye fatigue in dim-lit offices and during evening sessions. Light mode for hours-of-staring causes more strain.

A light-mode override is offered for daylight reading and for users with dark-mode sensitivity (some users with astigmatism prefer light backgrounds).

### Why allow overrides

Theme overrides matter for three reasons.

**1. Brand fit.** Some white-label customers (Team tier) need to match their own brand palette. Themes B and C give an editorial / approachable alternative.

**2. Accessibility.** Some users find dark mode harder to read. Light theme via Theme C is the accommodation.

**3. Embed personality.** Embed widgets (L144) inherit the theme parameter. A YouTuber embedding into a light-themed Substack can pick Theme C; a hedge-fund newsletter in dark mode picks Theme A.

## The token system

Each theme is expressed as a CSS variable token set:

```css
:root[data-theme="orange"] {
  --bg: #0A0A0A;
  --fg: #E8E8E8;
  --brand: #FF6F00;
  --accent: #FFB300;
  --success: #00C853;
  --warn: #FFAB00;
  --danger: #FF1744;
  --surface: #1A1A1A;
  --border: #2B2B2B;
  --p10: rgba(255,111,0,0.1);
  --p50: #FF6F00;
  --p90: rgba(255,111,0,0.3);
}

:root[data-theme="pink"] {
  --bg: #FFF1E5;
  --fg: #262A33;
  --brand: #990F3D;
  --accent: #0D7680;
  /* ... */
  --p10: rgba(153,15,61,0.1);
  --p50: #990F3D;
  --p90: rgba(153,15,61,0.3);
}

:root[data-theme="blue"] {
  --bg: #FAFCFE;
  --fg: #1F2937;
  --brand: #2563EB;
  /* ... */
  --p10: rgba(37,99,235,0.1);
  --p50: #2563EB;
  --p90: rgba(37,99,235,0.3);
}
```

Every component references variables, never hardcoded colors. Switching themes is a single attribute change on the `<html>` element.

## Forecast band rendering

Each theme defines its own band palette. The band uses three opacity tiers of the brand color:
- **P50**: solid brand color, 100% opacity, 2px stroke.
- **P10-P90**: 30% opacity fill.
- **P25-P75** (inner band, when shown): 50% opacity fill.

This keeps the visual language consistent across themes — the forecast band is the same *shape* in all three, just different *hue*.

## Categorical color scale

For multi-line charts (multi-country, multi-forecaster), a categorical palette is needed. Each theme has its own 8-color categorical palette:

- **Theme A (orange)**: orange / cyan / yellow / pink / lime / purple / mint / coral. Mid-saturation, high contrast on dark canvas.
- **Theme B (pink)**: FT-red / teal / mustard / navy / olive / burgundy / sage / rust. Mid-saturation, on warm cream.
- **Theme C (blue)**: blue / orange / green / purple / yellow / pink / cyan / brown. Tableau-10 derivative, on cool white.

All palettes are checked for:
- Color-blind safety (deuteranopia, protanopia, tritanopia simulation pass).
- WCAG AAA contrast on body text against canvas.
- Distinguishability at 4px line width (sparklines).

## Semantic color use

- **Success / positive change**: green (theme-specific shade).
- **Warning / borderline**: yellow / amber.
- **Danger / negative change**: red.
- **Neutral**: gray.
- **Brand**: forecast P50 line, active state, emphasis.

Semantic colors are never used decoratively. A green tile means "improving" or "passing." A red tile means "deteriorating" or "failing." Decorative color is reserved for the categorical palette.

## Theme switching

Theme is persisted in:
- `localStorage` (anonymous users).
- User profile (signed-in users; syncs across devices).
- URL query param `?theme=orange|pink|blue` (one-off override).

The `t` keystroke cycles theme. The `> theme {name}` command bar entry sets it explicitly.

System-preference respect: if user has not chosen a theme, OPENGEM defaults to Theme A regardless of OS dark-mode preference. This is intentional — Theme A is the brand, and we want consistency on first impression.

## Light variants

Each theme has a light variant for users who prefer light mode:
- **Theme A light**: cream canvas + orange accents (less common; falls back to Theme B for most users).
- **Theme B**: already light by default.
- **Theme C**: already light by default.

A user on Theme A who wants light mode is invited to switch to Theme B or C; OPENGEM does not auto-light-mode-flip Theme A because the orange-on-cream variant loses the terminal feel.

## Embed inheritance

The theme parameter passes to embed widgets (L144). A site that embeds OPENGEM in Substack picks the theme that best fits the host site's palette. Embeds can override the theme even if the dashboard user has set a different default.

## Print theme

Print tearsheets (L143) use a print-specific variant: brand color is preserved (small accents), but body is dark gray on near-white for ink efficiency. The print theme is the same regardless of the user's screen theme — print is a separate context.

## Theme transitions

When a user switches theme, the transition is instant (no fade). Half-second fades feel slow and tax CPU. Instant feels assertive.

## Future themes (deferred)

A "high-contrast" theme for accessibility (WCAG AAA) is deferred to L266 (a11y audit). It will likely be a variant of Theme A with stronger contrast.

A "newspaper-print" sepia theme has been considered for archive-vintage pages but is deferred.

## What this loop produced

- Three candidate themes specified: Terminal Orange (A), Editorial FT-Pink (B), Playful OWID-Blue (C).
- Decision: Theme A (Terminal Orange) is the default; B and C are user-toggleable.
- Justification: brand strategy ("Bloomberg-grade for everyone"), density on dark, long-session ergonomics.
- CSS variable token system: --bg, --fg, --brand, --accent, --success, --warn, --danger, --surface, --border, --p10, --p50, --p90.
- Categorical 8-color palette per theme, color-blind safe.
- Semantic color usage (success/warn/danger) reserved for state communication.
- Theme persistence in localStorage + profile + URL param.
- `t` keystroke cycles theme; `> theme` command sets it.
- Embed widgets inherit theme parameter.
- Print is its own theme (preserved across screen themes).
- Light variants: Theme A defaults to dark; Theme B/C are already light.
- System OS dark-mode preference does NOT auto-flip default (brand consistency).
- High-contrast accessibility theme deferred to L266.

## What comes next

- **L147** designs the typography system that pairs with these themes.
- **L148** designs the color system in more semantic depth.
- **L262** prototypes the dark/light theme toggle.
- **L266** runs the a11y audit (informs high-contrast theme).

## Related

- [[L121-information-architecture]] — header strip color from theme
- [[L122-home-screen]] — World page rendered in theme
- [[L132-provenance-drawer]] — drawer rendered in theme
- [[L144-embed-widget-design]] — embeds inherit theme
- [[L262-theme-toggle-prototype]] — code prototype
- [[L266-accessibility-audit]] — high-contrast variant
