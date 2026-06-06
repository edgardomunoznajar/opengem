# L070 — TanStack Table + AG Grid + Glide Data Grid: Terminal-Grade Grid Pick

**Loop**: 070 / 300
**Phase**: 1 — Open-source landscape survey
**Date**: 2026-06-06

---

## Thesis of this loop

OPENGEM's Bloomberg-grade indicator grid is a load-bearing UI primitive. Three or four pages depend on it: the home screen (top-100 indicators), the country page (country × indicator matrix), the watchlist (user-curated rows), the forecast leaderboard (model × horizon × indicator scores).

The grid must:
- Render 200-2000 rows × 20-50 columns smoothly.
- Embed sparklines in cells.
- Sort, filter, group by any column.
- Support sticky headers and frozen columns.
- Theme to terminal-density (12-13px font, tight padding, monospace numerals).
- Be keyboard-navigable (j/k row, l/h column, / search).
- Export to CSV / clipboard.
- Be free.

Three candidates: **TanStack Table** (Tanner Linsley), **AG Grid** (AG Grid Ltd), **Glide Data Grid** (Glide Apps, originally for their no-code product).

Verdict: **TanStack Table for V1**, **AG Grid Community as fallback if TanStack ergonomics hurt**, **Glide for the rare canvas-rendered massive-row case**. Skip AG Grid Enterprise.

## TanStack Table (the headless winner)

- **License**: MIT.
- **Maintainer**: Tanner Linsley (Tanstack ecosystem — React Query, React Router, etc). Healthy.
- **Bundle**: ~15KB gzipped. By far the smallest.
- **Model**: *headless*. TanStack Table provides the *state machine* (row model, sort state, filter state, virtualization adapters) but emits no DOM. You write the JSX. This is what makes the bundle tiny and the theming infinite.
- **Pairing**: TanStack Virtual (~5KB) for row virtualization. Together: ~20KB for a full-featured virtualized grid.
- **Sparklines in cells**: trivial. Each cell is a JSX element you wrote; drop an Observable Plot `lineY` SVG in it.
- **Sort/filter/group**: built into the row model.
- **Sticky headers / frozen columns**: a CSS exercise on top of the JSX you wrote.
- **Keyboard nav**: not provided. You write it. ~50 lines of JS for j/k/l/h.
- **Export to CSV**: not provided. ~30 lines.

The cost of TanStack is *writing the JSX*. You build the table cells. That's also the *benefit* — you have terminal-grade density control, perfect alignment, custom sparkline integration, custom color rules.

For OPENGEM's needs, this is the right tradeoff. The grid is load-bearing UI; writing it explicitly is worth the 2-week investment vs trying to bend a black-box grid into OPENGEM-aesthetic.

## AG Grid Community (the all-in-one fallback)

- **License**: MIT for the Community edition. Enterprise edition is paid.
- **Maintainer**: AG Grid Ltd (UK company, commercial open source). Healthy, large team.
- **Bundle**: ~330KB gzipped (community), much more with enterprise modules. Big.
- **Model**: *opinionated*. You give it data + column definitions; it renders. You theme it through CSS variables.
- **Sparklines in cells**: built-in via `cellRenderer`, but the built-in sparkline component is enterprise-only. Community sparklines = bring your own renderer.
- **Sort/filter/group**: rich, mature. Multi-column sort, set-filter UI, row grouping.
- **Sticky headers / frozen columns / pinned rows**: built-in.
- **Keyboard nav**: built-in, comprehensive. j/k may need rebinding but the model is right.
- **Export to CSV**: built-in for community.
- **Virtualization**: built-in, just works.

What AG Grid Community gets *wrong* for OPENGEM:
- The 330KB bundle is a significant chunk of the per-page JS budget.
- The aesthetic is "data grid" — corporate, breathable. Tuning to terminal-density is CSS-heavy but possible.
- The mental model is "configure," not "compose." This is fine for a quick build, less fine when the requirement evolves.

What AG Grid Community gets *right*:
- Best-in-class out-of-the-box behavior. Day 1 you have a *good* grid.
- Best keyboard nav model.
- Best clipboard / copy-paste behavior.

The AG Grid Enterprise paywall trap is real: copy-paste *with* rich formatting, set filters, pivot, master-detail rows, sparklines as a component, are all enterprise-only ($1k+/seat/year). For a public open-source product, do not pay for these — replicate them in TanStack Table over a couple of weeks of focused work.

## Glide Data Grid (the canvas-rendered specialist)

- **License**: MIT.
- **Maintainer**: Glide Apps. Mostly built for their own product; Glide Apps maintains it actively.
- **Bundle**: ~120KB gzipped.
- **Model**: HTML5 canvas-rendered. Like the JavaScript table on a TradingView or Notion-database-view — the cells are pixels, not DOM elements.
- **Specialty**: massive grids. 100k+ rows is fine. The DOM-based grids (TanStack, AG Grid) start to stutter past 10k rows of visible viewport even with virtualization; Glide doesn't.
- **Drawback**: because cells are pixels, custom JSX in cells is awkward. Sparklines require canvas drawing, not SVG composition.
- **Drawback**: accessibility is harder (canvas is opaque to screen readers without explicit ARIA wiring).

For OPENGEM specifically, Glide is the *third* option for a specific use case: the forecast leaderboard at full scale (every model × every horizon × every indicator × every country = ~100k rows). At that scale, Glide is genuinely the best tool. But the leaderboard's V1 fits in 2k rows easily, so TanStack handles it.

## The decision matrix for OPENGEM

| Use | First pick | Second pick |
|---|---|---|
| Home top-100 indicators grid (~100 rows × 12 cols) | TanStack Table | AG Grid Community |
| Country page indicator matrix (~50 × 8) | TanStack Table | AG Grid Community |
| Watchlist (~20 × 8) | TanStack Table | AG Grid Community |
| Forecast leaderboard V1 (~2k × 15) | TanStack Table | AG Grid Community |
| Forecast leaderboard Y2 (~100k × 15) | Glide Data Grid | AG Grid Enterprise *(if budget)* |
| V&V matrix (~indicator × horizon × model, ~500 × 30) | TanStack Table with cell-color render | AG Grid Community |

## Cost (license + ramp + hosting)

- **TanStack Table**: $0 license. 1-2 weeks for the *first* grid (write the JSX patterns); 2 days per additional grid (templated). Bundle adds ~25KB per page.
- **AG Grid Community**: $0 license. 2 days for the first grid (configure column defs); 1 day per additional grid. Bundle adds ~330KB per page.
- **AG Grid Enterprise**: ~$995-1495/dev seat/year. *Reject.* The features behind the paywall (pivot, set-filter, sparklines, master-detail) are all replicable in TanStack in 2-4 weeks.
- **Glide Data Grid**: $0 license. 1 week for a working grid; awkward custom-cell story. Bundle adds ~120KB.

## Embedded sparkline pattern (the load-bearing implementation detail)

A sparkline-in-cell looks like:

```jsx
<td>
  {row.original.last_12_months.length > 0 && (
    <Plot
      width={80}
      height={20}
      x={null}
      y={null}
      marks={[Plot.lineY(row.original.last_12_months)]}
    />
  )}
</td>
```

With TanStack Table this is *natural* — it's just JSX. With AG Grid Community it requires a `cellRenderer` component that mounts a sub-React-tree per cell, and the perf cost of 100×12=1200 cell-mounts is non-trivial. AG Grid Enterprise handles this with its native sparkline component but you're paying for it. TanStack wins this affordance cleanly.

## Verdict

- **TanStack Table + TanStack Virtual + Observable Plot for cell sparklines**: **ADOPT-V1** for all OPENGEM grids in Y1.
- **AG Grid Community**: **EVALUATE-LATER** as a fallback if TanStack ergonomics produce too much custom code. Likely never invoked.
- **AG Grid Enterprise**: **SKIP** forever. The paywall items are buildable in OSS.
- **Glide Data Grid**: **EVALUATE-LATER** for the 100k-row forecast leaderboard in Y2-Y3.

## Cost summary

| Tool | Cost | Ramp |
|---|---|---|
| TanStack Table + Virtual | $0 | 1-2 weeks first grid, 2 days each subsequent |
| AG Grid Community | $0 | 2 days |
| AG Grid Enterprise | (skipped) | (skipped) |
| Glide Data Grid (Y2+) | $0 | 1 week |

## What comes next

- **L071** picks the 3D geo viz library.
- **L099** is the Phase 2 implementation deep dive on TanStack Table for Pro-grade grids.

## Related

- [[L069-d3-vega-plotly]] — Observable Plot for in-cell sparklines
- [[L099-tanstack-table-pro-grids]] — Phase 2 deep dive
- [[L073-next-tailwind-dashboard-starters]] — Tremor / shadcn host the grid components
