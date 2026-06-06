# L105 — shadcn vs Tabler vs Mantine: Confirm the Pick, Pin the Vendor List

**Loop**: 105 / 300
**Phase**: 2 — Deep dive on top candidates
**Date**: 2026-06-06

---

## Thesis of this loop

L073 picked shadcn/ui as the base + Tremor for analytics components. This loop is the *vendor list* — the specific components OPENGEM copies in from each library at v1, and the *anti-list* — components we never want, because they would push us toward the generic-SaaS aesthetic that L008 differentiation explicitly rejects.

The companion question: should we add Tabler or Mantine to the mix? Both are component libraries that ship with more out-of-the-box analytics affordances than shadcn. The honest answer: **no.** Tabler is the wrong design language (it looks like a Bootstrap admin), and Mantine is the wrong distribution model (an npm package you import vs a copy-paste source you own). The shadcn philosophy — "own the source of every component, vendor it into your repo, customize at will" — is exactly the philosophy a one-developer Bloomberg-aspirational dashboard needs.

Verdict: **shadcn/ui as the only component library, with Tremor's analytics components copied in à la shadcn (the recently-released Tremor Raw lets us do exactly this). Skip Tabler entirely. Skip Mantine as a runtime dependency. Confirm: the 18 components below are vendored at v1; the 14 we explicitly never adopt are written down so we don't drift.**

---

## Why shadcn beats the others structurally

The four candidate libraries differ along *one* axis that matters more than feature lists: **who owns the source code**.

- **shadcn/ui**: the source lives in your repo. You ran `npx shadcn add button` and the button's TypeScript file is now committed under `components/ui/button.tsx`. You can edit it. The library is a stylistic recipe + a CLI, not a runtime dependency.

- **Mantine**: source lives in `node_modules/@mantine/core`. You import a `Button` and the rendered output comes from a versioned package. If you need to change the focus-ring color *globally* across all buttons, you do it via theme tokens or CSS overrides. You can't *edit* the component.

- **Tabler**: same as Mantine (npm-installed), but with a Bootstrap-flavored design system from a single designer (Codecalm). Beautiful for admin dashboards; wrong for OPENGEM's editorial-terminal aesthetic.

- **Tailwind UI** (paid): copy-pasteable like shadcn, but commercial license restricts redistribution and the design language is Vercel-marketing-flavored rather than terminal-flavored.

OPENGEM is staking its brand on a *specific* visual language: tabular numerics in JetBrains Mono, terminal-amber accent, narrow gutters, all-caps mono labels, square borders. shadcn's "you own the source" model is the only one that lets a one-developer team push every component to that aesthetic without forking the library.

---

## The vendor list (v1 — 18 components)

Each row is a component to run `npx shadcn add <name>` against, then post-process per the rules below.

| Component | Used for | Post-processing rules |
|---|---|---|
| `button` | Every CTA | Reduce border-radius from 6px to 2px; use mono font for ALL-CAPS labels. |
| `card` | Tile-grid layouts on home, country, indicator pages | Background `bg-elevated`, border `border-line`. |
| `dialog` | Methodology pop-ups, sharing UX | Default size: max-w-2xl; nest a `<details>` block for raw JSON. |
| `dropdown-menu` | Country/indicator selectors, share menu | Mono font for keyboard hint pills. |
| `popover` | Inline drilldown on chart points | Show vintage badge in the popover header. |
| `tabs` | Country page sections, scenario sections | Underline-style indicator, not pill-style. |
| `tooltip` | Number-with-mini-context, hover affordance | Mono font; `text-2xs`; appears with 200ms delay. |
| `command` | The command palette (already in repo) | Use `cmdk` directly; shadcn wraps it. |
| `input` | Search, embed code copy, watchlist add | Border `border-line`, focus ring `ring-brand-500`. |
| `label` | Form labels, field titles | All-caps, mono, `tracking-widest`. |
| `select` | Vintage selector, horizon selector | Mono font for option values. |
| `separator` | Section dividers | `bg-line`, `h-px`. |
| `skeleton` | Loading states for fetched data | Pulse animation with `pulse-fast` keyframe. |
| `switch` | Theme toggle, alert on/off | Brand-amber when on; `bg-line` when off. |
| `table` | Forecast tables, leaderboard, country comparison | Replaced ultimately by TanStack Table; shadcn table is for static use. |
| `toast` | Save confirmations, error notices | Bottom-right, auto-dismiss 4s. |
| `badge` | Vintage stamps, "TRIGGERED" flags, country flags | Mono font; sm/md/lg sizes. |
| `progress` | Long backtest jobs, embed generation | Brand-amber fill. |

Total time to vendor: ~3 hours, including the post-processing rules.

---

## Tremor components vendored à la shadcn (v1 — 9 components)

Tremor Raw (released late 2025) ships its components as shadcn-style copy-paste source rather than an npm dependency. We use this for the analytics-shaped components shadcn doesn't have.

| Component | Used for | Rules |
|---|---|---|
| `BarChart` | Comparison bars, indicator distributions | Bloomberg-amber primary, semantic colors for compare-2 |
| `LineChart` | Sparkline alt for slower-than-realtime data | Mostly replaced by lightweight-charts for forecast pages |
| `AreaChart` | Forecast bands | Used for the P10-P90 band visual |
| `DonutChart` | Scenario probability rollup | Single-direction donut, not full pie |
| `Tracker` | Forecast hit/miss visual on leaderboard | Green for hit, red for miss |
| `Metric` (KPI) | Top-of-page metric tiles | Mono font, large numeric, sparkline below |
| `ProgressBar` | Calibration plot bars | Replaces shadcn `progress` for analytics use |
| `Legend` | Multi-series chart legends | Mono font; tabular layout |
| `Callout` | Annotation/methodology notes inline | Border-left amber accent |

---

## The anti-list (14 components we explicitly never adopt)

Writing the anti-list down is the discipline. Each of these would push OPENGEM toward a generic-SaaS aesthetic and away from terminal-editorial.

1. **Sidebar with collapsible group icons** — the standard SaaS admin sidebar. OPENGEM's nav is a top bar with a command palette. No sidebar.
2. **Avatar grouping for collaboration** — there is no collaboration; OPENGEM is a publishing surface, not a workspace.
3. **Stepper / wizard** — every flow is one-shot, not multi-step. Onboarding (L120) is three tiles, not a stepper.
4. **Tag input with chips** — overweight UX for a single-input field; we use plain text with delimiters.
5. **Date range picker with calendar grids** — vintage selector is mono-font ISO dates; no calendar grid.
6. **Carousel** — never. Carousels are SEO-hostile and accessibility-hostile.
7. **Confetti / celebration animations** — anti-editorial. OPENGEM is sober.
8. **Drawer / off-canvas sidebars** — covered by `dialog` + popover; an extra primitive is bloat.
9. **Toggle group** — `tabs` covers this; redundant.
10. **Hover card** (the "GitHub user preview" pattern) — too playful for macro data.
11. **Accordion** — disclosure is `<details>` (native HTML); accordions add unneeded JS.
12. **Resizable panels** — we ship fixed layouts; resizing is a Pro-tier feature at most, not v1.
13. **Sheet** — same as drawer.
14. **Pagination with page numbers** — infinite scroll for event streams; "load more" button for tables. No page-number bar.

---

## Why not Tabler

Tabler is a 5-year-old Bootstrap-based admin template. It is beautiful. It has thousands of pre-designed pages. It would let a contractor ship an OPENGEM-shaped admin in three days.

We reject it because:

- The design language is "modern admin," which carries a "I am a SaaS product" semantic. OPENGEM's brand position requires "I am an editorial macro publication." The visual delta matters.
- Adopting Tabler means importing Bootstrap-flavored CSS + Tabler's design tokens. Migrating away from that is a multi-month project. The cost of escape is high; the cost of avoidance is zero.
- Tabler doesn't have an asset graph for OPENGEM's specific surfaces (forecast bands, vintage timelines, scenario rollups). We'd be using ~30% of its components and writing the other 70% from scratch.

---

## Why not Mantine as a runtime dependency

Mantine is excellent. The Mantine Hooks alone are a strong piece of work; the form library is the cleanest in the React ecosystem. But:

- Importing Mantine = locking in a runtime CSS-in-JS engine (`emotion`). OPENGEM's CSS is Tailwind. Mixing the two leads to specificity wars and bundle bloat.
- The Mantine theme is global; per-component overrides are tedious. shadcn's "edit the source" model is more direct.
- The cost of adoption is *runtime*: a Mantine button is rendered through Mantine's reconciler, not as raw HTML. For OPENGEM's per-route bundle budget (15KB, L104), Mantine's footprint is too large.

We *do* steal individual Mantine hook ideas (`useDebouncedValue`, `useClickOutside`) and reimplement them ourselves. The hooks are a few dozen lines each; copy-paste is fine.

---

## Next-step: the install script

```bash
#!/usr/bin/env bash
# scripts/vendor-components.sh — run once at scaffold time
set -e
cd prototypes/dashboard-next
npx shadcn@latest init \
  --base-color zinc \
  --css-variables \
  --tailwind-config tailwind.config.ts \
  --components ./components/ui

# v1 vendor list
for c in button card dialog dropdown-menu popover tabs tooltip command \
         input label select separator skeleton switch table toast badge progress; do
  npx shadcn@latest add "$c" --yes --overwrite
done

# Tremor Raw — vendored from upstream
npx @tremor/raw@latest add bar-chart line-chart area-chart donut-chart \
  tracker metric progress-bar legend callout
```

---

## What this loop produced

- Confirmed shadcn/ui as the only library; Tremor Raw as the analytics overlay.
- An 18-component vendor list with post-processing rules.
- A 9-component Tremor list with analytics-specific rules.
- A 14-component anti-list to prevent generic-SaaS drift.
- The rationale for skipping Tabler (wrong design language) and Mantine (wrong distribution model).
- An install script ready for the scaffold.

## What comes next

- **L119** — color system applies the Bloomberg-orange palette to these components.
- **L146** — iconography system pairs lucide-react with this component vendor.
- **L147** — typography rules use the component post-processing principles.

## Related

- [[L073-next-tailwind-dashboard-starters]] — shadcn vs Tremor vs Refine evaluation
- [[L008-differentiation]] — the editorial-terminal aesthetic that drives anti-list
- [[L119-dark-mode-bloomberg-orange]] — palette applied to vendored components
- [[L146-iconography-system]] — icon library pairing
- [[L147-typography-system]] — type rules used in post-processing
