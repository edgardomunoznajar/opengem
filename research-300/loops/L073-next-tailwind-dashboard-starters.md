# L073 — Next.js + Tailwind Dashboard Starter Kits: shadcn vs Tremor vs Refine vs Tailwind UI

**Loop**: 073 / 300
**Phase**: 1 — Open-source landscape survey
**Date**: 2026-06-06

---

## Thesis of this loop

The OPENGEM public dashboard's interactive surface lives in Next.js. That decision is implicit in everything Phase 0 said about SEO, embeddability, terminal-feel, custom React components, and SSR. The question this loop answers is: *which Next.js + Tailwind starter / component library does OPENGEM lean on*?

The four serious candidates:

- **shadcn/ui** (the bring-your-own-components library popularized by Vercel's design head circa 2023, now ubiquitous in 2026): MIT-licensed copy-paste components.
- **Tremor** (Vercel-acquired late 2024, specifically the analytics-dashboard component library): Apache 2.0, purpose-built for analytics UIs.
- **Refine** (the React meta-framework for data-heavy admin panels): MIT, with paid enterprise tier.
- **Tailwind UI** (the original commercial Tailwind component set, $299 one-time license): closed for redistribution but you can use components in your projects.

Verdict: **shadcn/ui as the base + Tremor for the chart/KPI components**. Refine is the wrong shape (admin-panel framework, not a public dashboard). Tailwind UI is worth the $299 for design references but not the foundation.

## Why shadcn/ui as the base

shadcn/ui is not a *library* in the npm-install sense. It is a *copy-paste registry* of Radix-UI-primitive-based components styled with Tailwind. You run `npx shadcn add button card dropdown` and it copies the source code into your project, where you own it forever. The model has four enormous advantages for OPENGEM:

1. **You own the components.** Bloomberg-orange theming is editing the source, not fighting a black-box. Terminal density is changing a `className`, not a config object. Every breaking change in Tailwind v4 or Radix v2 is a `pnpm update` in your repo, not a vendored breaking dependency.

2. **MIT license, no per-seat / no commercial gate.** Free forever, embeddable in OPENGEM's open-source-and-CC-BY product.

3. **Tiny effective bundle.** You only ship the components you use. A typical OPENGEM page imports `Card`, `Button`, `Input`, `Dropdown`, `Tooltip` — ~15KB gzipped of component code on top of Radix primitives.

4. **2026 ubiquity is a moat.** Every Cursor / Claude Code / GPT prompt about React UI assumes shadcn. AI-assisted dev productivity is materially higher in shadcn than in any alternative. The downstream effect is real: a one-person team ships 2× faster with shadcn because the LLMs are well-trained on it.

The shadcn ecosystem in 2026 includes shadcn-themes (drop-in dark mode + brand palettes), shadcn charts (a thin Recharts wrapper that *might* be useful for simple cases but Observable Plot likely wins), and a sprawling templates registry. The OPENGEM home screen starts as a fork of the "shadcn dashboard" template, then gets aggressively un-shadcn-ified into terminal-density.

## Why Tremor for the analytics-specific components

Tremor is a React component library *specifically* for analytics dashboards. Apache 2.0, Vercel-owned (acquired late 2024 — meaning long-term roadmap is stable). Key components OPENGEM wants:

- `<Card>` and `<Metric>` for KPI tiles.
- `<AreaChart>` and `<LineChart>` for simple time-series (Recharts-backed).
- `<DonutChart>` and `<BarChart>` for composition decompositions.
- `<DateRangePicker>` for vintage selection.
- `<TabGroup>`, `<Tab>`, `<TabPanels>` for forecast/realized/methodology tabs.
- `<Table>` for simple tabular views (defer to AG-Grid / TanStack Table from L070 for the heavy ones).
- `<Callout>` for methodology annotations.

The Tremor charts are not the workhorse — Observable Plot wins line/area, Lightweight Charts wins the forecast view, AG-Grid/TanStack wins tables (L069, L070, L072). Tremor's value is the *non-chart components*: well-designed KPI cards, date pickers, callouts, tab groups, badges, deltas. These are exactly the parts of an analytics UI that are tedious to build well from primitives.

Tremor pairs well with shadcn — both are Tailwind-native, both ship typed React components, both can coexist in the same project. The mental model: shadcn for the base UI grammar (buttons, inputs, dropdowns), Tremor for analytics-specific compositions (KPI strips, callouts, delta indicators), Observable Plot / Lightweight Charts for the charts themselves.

## Why Refine is the wrong shape

Refine is a meta-framework for *internal admin panels*: CRUD interfaces, data tables, forms, auth-gated dashboards. It generates resource pages from your data models. For an internal ops tool against a Postgres DB, Refine can save weeks.

OPENGEM's public dashboard is the opposite of an admin panel:
- It's read-only (no forms).
- It's anon-public (no auth flow).
- It's content-first (SEO, OG cards, RSS).
- It's heavily designed (custom layouts per page).
- It's not CRUD against any DB — it's published static + interactive views on top of a vintage store.

Refine's affordances actively work against this. **SKIP** for the public dashboard. **EVALUATE-LATER** for the internal forecast-vintage-management admin tool (L132 vintage drawer admin) — but Dash (L062) likely wins that too.

## Why Tailwind UI is *almost* but not quite

Tailwind UI is the *original* paid Tailwind component library by Adam Wathan and team. $299 lifetime license, ~500+ components, polished design.

Pros for OPENGEM:
- Highest-quality design references in the ecosystem.
- Specific "Application UI" subset (sidebar layouts, modals, tabs, dropdowns) is a goldmine of patterns.
- The $299 is trivially recouped in 2 hours of saved design work.

Cons for OPENGEM:
- License *forbids redistribution* of the components. OPENGEM is open-source. We can't ship Tailwind UI components in the OPENGEM open repo.
- shadcn already covers the same affordances under a permissive license.

The right play: **buy Tailwind UI for $299** as a *design reference library* used during the OPENGEM design phase. Translate the patterns into shadcn-equivalent components inside the OPENGEM repo. Ship those (MIT) into the open repo. The Tailwind UI license is not violated — the *patterns* (CSS layouts, color discipline, spacing) are not copyrightable, only the source files are licensed.

## Cost summary

| Tool | License | Cost | Use in OPENGEM | Ramp |
|---|---|---|---|---|
| shadcn/ui | MIT | $0 | Base component foundation | 1 week first page |
| Tremor | Apache 2.0 | $0 | KPI cards, dates, callouts, deltas | 2 days |
| Tailwind UI | Commercial reference | $299 one-time | Design pattern theft | 1 day |
| Refine | MIT | $0 (skipped) | (skipped) | (skipped) |

## Implementation outline

Y1 OPENGEM dashboard architecture:
- **Next.js 15+** with App Router, server components, SSR.
- **Tailwind v4+** for styling.
- **shadcn/ui** for base components (button, card, dropdown, dialog, tooltip).
- **Tremor** for KPI cards, date pickers, deltas, callouts, badges.
- **Observable Plot** for the workhorse charts (line/area/sparkline/bar/heatmap/scatter).
- **Lightweight Charts** for the forecast page hero chart.
- **TanStack Table + TanStack Virtual** for grids.
- **globe.gl + react-globe.gl** for the geopolitical pulse 3D globe.
- **D3-geo + topojson** for 2D maps.

The public dashboard is *Next.js*. The static long-tail (per-country, per-indicator explainer pages) is *Observable Framework* (L066). The two coexist — the Next.js app links into the Observable static site for the long tail, and vice versa.

## Hosting cost

- **Vercel free tier**: covers Y1 traffic comfortably. The hobby plan supports ~100GB bandwidth/mo.
- **Vercel Pro**: $20/mo when needed.
- **Self-hosted on Cloudflare Pages**: $0/mo, unlimited bandwidth.
- **Self-hosted on Fly.io**: ~$15-30/mo for a small Next.js app.
- Edge functions and ISR (incremental static regeneration) for the dynamic pages: ~$0-50/mo depending on usage.

Practical floor: **$0/mo on Cloudflare Pages**.

## Ramp-up

- Week 1: Next.js app with shadcn + Tremor wired up, home page mockup, dark theme.
- Week 2: Country page template + indicator page template.
- Week 3: Forecast page template with Lightweight Charts integration.
- Week 4: Grid views with TanStack Table.
- Week 5: globe.gl integration for the geopolitical pulse page.
- Week 6: Polish, OG cards, RSS, mobile.

A 6-week Y1 v1 dashboard build for one focused developer.

## Verdict

- **shadcn/ui**: **ADOPT-V1** for base components.
- **Tremor**: **ADOPT-V1** for analytics-specific components.
- **Tailwind UI**: **ADOPT-V1** ($299) as design reference only.
- **Refine**: **SKIP** for public dashboard.

## What comes next

- **L074** evaluates SvelteKit / Solid / Astro / Qwik alternatives to Next.js.
- **L105** is the Phase 2 design-system pass on shadcn/Tremor/Mantine.

## Related

- [[L066-observable-framework]] — sister-stack for the static long-tail
- [[L069-d3-vega-plotly]] — chart library that lives inside Next.js components
- [[L070-tanstack-aggrid-glide]] — grid library
- [[L105-tabler-mantine-shadcn]] — Phase 2 design system pass
