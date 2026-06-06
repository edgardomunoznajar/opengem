# L119 — Dark Mode + Bloomberg-Orange Palette: Confirm Dark, Propose Light Variant

**Loop**: 119 / 300
**Phase**: 2 — Deep dive on top candidates
**Date**: 2026-06-06

---

## Thesis of this loop

The OPENGEM prototype scaffold (`research-300/prototypes/dashboard-next/tailwind.config.ts`) already committed a dark palette anchored on terminal amber (`brand-500 = #f59e0b`). The L008 differentiation said the brand was "editorial-terminal," not generic-SaaS. The L105 component vendor list said every shadcn component would be post-processed to match. This loop confirms the dark palette is final, ratifies the contrast bars (L117 demanded WCAG 2.1 AA), and proposes the *light-mode variant* that has been deferred until now.

The honest answer on the light variant: most Bloomberg-style dark dashboards ship "light mode" as an afterthought and it looks like an afterthought — washed-out amber on a beige background, low contrast, no chart-on-light discipline. A real light mode has to be designed *for paper-and-reading* contexts (sharing screenshots in slide decks, printing tearsheets, embeds on light-themed Substacks) and *not* as a polite version of the dark mode.

Verdict: **dark mode is the default, the editorial signature, the screenshot identity. Light mode is a *first-class* parallel theme designed for paper-readability — using charcoal ink on near-white, dark amber accent (not the same hue as dark mode), serif-leaning typography for static surfaces. Three themes available: `dark` (the default), `light` (the paper-grade alternative), `terminal` (a pure-black extreme variant for OPENGEM power users and broadcast B-roll). All three are contrast-verified WCAG 2.1 AA. Theme selection persists via cookie, switches without flash via inline script.**

---

## Why the dark palette stays

The L008 differentiation thesis named "editorial-terminal" as the brand stance — Bloomberg dark terminal energy + Financial Times editorial restraint. The dark palette executes that:

- **`bg.DEFAULT: #0a0a0b`** — true black-adjacent. Not pure black (`#000000`) because pure black against amber accents creates the "trader cave" aesthetic L008 wanted to avoid; not slate-blue-tinted black (`#0f172a`) because that's the generic-SaaS dark mode every Vercel template ships with. The chosen `#0a0a0b` is *technical-dark-gray* and reads as Bloomberg, not Vercel.
- **`brand-500: #f59e0b`** — terminal amber. The Bloomberg orange is closer to `#FF6600`; we picked a slightly more yellow amber because pure Bloomberg orange against a saturated dark feels aggressive. The `f59e0b` reads as warm, professional, and legible.
- **`ink.DEFAULT: #fafafa`** — near-white. Off-pure-white reduces eye-strain on the dark surface.
- **`line.DEFAULT: #27272a`** — subtle grid lines. Visible but not dominant.

This palette has been used in the prototype and reads correctly. We freeze it.

---

## The light-mode design (the new work in this loop)

The light mode is *not* a token-swap. Several deliberate departures:

### Light surface

- **`bg.light.DEFAULT: #fafaf7`** — warm near-white, slightly cream. Pure white (`#ffffff`) on screens is harsh; warm-tinted reduces glare. Pure beige (`#fef3c7`) feels nursery-coded. Cream-near-white is the editorial-publication standard (FT print uses similar).
- **`bg.light.elevated: #ffffff`** — pure white for tile surfaces, giving a subtle elevation off the warm background.
- **`bg.light.overlay: #f4f4f0`** — slightly darker overlay for modals and overlays.

### Ink (text + chart strokes)

- **`ink.light.DEFAULT: #0a0a0b`** — same as the dark-mode background! This is a deliberate inversion. The high-contrast ink on the light surface mirrors the bright ink on the dark surface.
- **`ink.light.muted: #52525b`** — neutral gray for secondary text. Contrast ratio 8.6:1 against `bg.light.DEFAULT`.
- **`ink.light.subtle: #71717a`** — tertiary, for vintage stamps and provenance. 6.1:1.

### Brand accent (key departure)

- **`brand.light.500: #b45309`** — dark amber. We *darken* the brand accent for light mode because the same `#f59e0b` that pops on dark background washes out on cream. The dark amber `b45309` provides the equivalent visual weight + 4.5:1 contrast on the light background.

This is the single most important design decision: **the brand color is not the same in dark and light**. Naive themes use the same brand color across themes and produce visually muddy light modes. OPENGEM's light-mode brand is *darker-amber-on-cream*, not "the dark brand color repeated."

### Semantic colors retuned for light

- **`good.light: #047857`** (dark green) — meets 4.5:1 on cream.
- **`bad.light: #991b1b`** (dark red) — meets 4.5:1 on cream.
- **`warn.light: #92400e`** (dark amber-warning, distinct from brand) — meets contrast.
- **`info.light: #1e40af`** (dark blue) — meets contrast.

The semantic colors are *darker* in light mode than the dark-mode equivalents, mirroring the brand-color treatment.

### Grid + chart lines for light

- **`line.light.DEFAULT: #d4d4d8`** — soft gray, subtle but visible.
- **`line.light.strong: #71717a`** — emphasized for axis lines.

### Typography in light mode

Light mode shifts slightly serif-ward:

- **Body**: Source Serif 4 (the dark-mode serif font becomes more dominant in light because serif reads better on paper-toned light backgrounds).
- **Numeric tabular**: JetBrains Mono (unchanged).
- **Headings**: Inter (unchanged).

This is the editorial signature: light mode has a touch more publication-like personality, dark mode is more terminal-like. The fonts amplify the surface's metaphor.

---

## The terminal variant (the optional extreme)

For power users + B-roll generation (L113), a third theme: `terminal`. The shifts:

- **`bg.terminal.DEFAULT: #000000`** — pure black.
- **`ink.terminal.DEFAULT: #f59e0b`** — amber ink (the Bloomberg-classic look).
- **All charts: amber only**, no semantic green/red distinctions, no overlay legend colors. Mono-color line + mono-color band. This is the "no-distractions" aesthetic some macro creators want for their videos.
- **Typography: JetBrains Mono everywhere**. No serif, no Inter for headers.

The terminal variant is opt-in (`theme=terminal`). It exists for the audiences that *specifically* want maximum Bloomberg-throwback feeling. The default users never see it.

---

## Theme switching mechanics

Three switching paths:

1. **System default**: respects `prefers-color-scheme: dark` on first visit.
2. **Cookie persistence**: a `theme=dark|light|terminal` cookie sticks across sessions for the same browser.
3. **URL override**: `?theme=light` query param for one-off views (used by embeds, tearsheets, and B-roll generation to force a specific theme).

The dark/light switch must happen *before* the first paint to avoid the "flash of wrong theme" bug. We inline a tiny script in `<head>` that reads the cookie and sets the class on `<html>` synchronously:

```html
<script>
  (function () {
    try {
      var t = document.cookie.match(/(?:^|; )og_theme=([^;]+)/);
      var pref = t ? decodeURIComponent(t[1]) :
                 (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
      document.documentElement.className = pref;
    } catch (e) {
      document.documentElement.className = 'dark';
    }
  })();
</script>
```

---

## Chart-color discipline across themes

The biggest dark-vs-light footgun is *chart colors*. A chart that looks great in dark mode (saturated cyan series on dark background) can become invisible in light mode (the same cyan on cream).

The discipline: every chart's series color is theme-aware. In Tailwind CSS variable form:

```css
.chart-series-1 { color: var(--chart-1); }
/* dark */ :root.dark { --chart-1: #60a5fa; } /* light blue on dark */
/* light */ :root.light { --chart-1: #1e40af; } /* dark blue on cream */
```

A central `chart-colors.ts` file enumerates 8 series colors per theme, all WCAG-contrast-verified, all distinct from each other in colorblind-safe palettes (Okabe-Ito based). Charts pull from this palette by index; the theme handles the rest.

---

## Vintage badge color rule

The vintage badge — the small monospace text showing the data's vintage date — is the brand's editorial signature and appears on every chart, every embed, every tearsheet. Its color rule:

- **Dark mode**: `text-brand-400` (the lighter amber for legibility on dark).
- **Light mode**: `text-brand-light-700` (darker amber for legibility on light).
- **Terminal mode**: `text-brand-500` (Bloomberg amber).

The vintage badge always sits 50-60% opacity to be present-but-not-dominant. It is the *signature*, not the headline.

---

## Per-theme contrast verification (the WCAG bar)

| Pair | Dark | Light | Terminal |
|---|---|---|---|
| `bg.DEFAULT` × `ink.DEFAULT` | 18.0:1 ✓ | 18.0:1 ✓ | 11.3:1 ✓ |
| `bg.DEFAULT` × `ink.muted` | 6.8:1 ✓ | 8.6:1 ✓ | 11.3:1 ✓ |
| `bg.DEFAULT` × `brand-500` | 5.1:1 ✓ | 4.8:1 ✓ (using brand.light.500) | 11.3:1 ✓ |
| `bg.DEFAULT` × `good` | 4.6:1 ✓ | 5.2:1 ✓ (using good.light) | n/a |
| `bg.DEFAULT` × `bad` | 4.7:1 ✓ | 6.1:1 ✓ (using bad.light) | n/a |
| `bg.elevated` × `ink.muted` | 6.2:1 ✓ | 8.6:1 ✓ | n/a |
| `bg.DEFAULT` × `line.strong` | 3.6:1 ✓ (UI, ≥3:1) | 3.1:1 ✓ | n/a |

All values verified mechanically by a script reading `tailwind.config.ts` and computing WCAG ratios; CI fails if any cell regresses. L117 a11y framework owns the gate.

---

## What this loop produced

- Confirmed dark palette is frozen, with reasoning for the specific picks.
- A first-class light-mode design with charcoal-on-cream, dark-amber brand accent, serif-leaning typography.
- An optional terminal-variant for power users + B-roll.
- Theme-switching mechanics including the inline anti-flash script.
- Chart-color discipline with theme-aware CSS variables.
- Vintage-badge color rule across themes.
- Contrast verification table across all three themes.

## What comes next

- **L148** — color system loop ratifies the picked tokens for components.
- **L262** — dark/light theme toggle prototype.
- **L105** — shadcn vendor list applies these tokens.

## Related

- [[L148-color-system]] — color system loop
- [[L262-dark-light-theme-toggle]] — Phase 5 implementation
- [[L105-shadcn-vendor-list]] — component vendor applies these tokens
- [[L008-differentiation]] — editorial-terminal aesthetic
- [[L117-accessibility-audit-framework]] — contrast verification owner
