# L099 — TanStack Table for Pro-grade grids

**Loop**: 099 / 300
**Phase**: 2 — Deep dives
**Date**: 2026-06-06
**Verdict**: ADOPT-V1

---

## The decision

OPENGEM uses TanStack Table (formerly react-table) for every Pro-grade grid: forecasts list, leaderboard, accountability ledger miss table, coverage matrix, scenario index, indicator cross-country grid.

Rejected alternatives:
- **AG Grid Community** — full-featured, but its commercial license is invasive for the kind of derivative use OPENGEM enables (republishing data implies users may run AG Grid commercially against OPENGEM data; we don't want to be that vector).
- **Glide Data Grid** — excellent for spreadsheet-like editing; OPENGEM is read-only, so the editing capabilities are dead weight.
- **MUI DataGrid** — bundle weight, opinionated styling, expensive Pro tier.

TanStack Table is **headless** — it manages state + sorting + filtering + grouping but renders nothing. We provide the DOM, which means our terminal-density Tailwind table cells stay first-class.

## Composition pattern

```tsx
import {
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  flexRender,
} from "@tanstack/react-table";

const columns = useMemo<ColumnDef<Forecast>[]>(() => [
  {
    header: "Country",
    accessorKey: "country",
    cell: ({ getValue }) => (
      <Link href={`/countries/${getValue()}`}>
        <span>{isoToFlag(getValue() as string)}</span>
        <span className="font-mono text-2xs">{getValue() as string}</span>
      </Link>
    ),
  },
  { header: "Indicator", accessorKey: "indicator" },
  {
    header: "P50",
    accessorKey: "point",
    cell: ({ getValue }) => <span className="num">{fmt(getValue() as number, "%")}</span>,
    enableSorting: true,
  },
  // ...
], []);

const table = useReactTable({
  data: forecasts,
  columns,
  getCoreRowModel: getCoreRowModel(),
  getSortedRowModel: getSortedRowModel(),
  getFilteredRowModel: getFilteredRowModel(),
  getPaginationRowModel: getPaginationRowModel(),
});
```

## Features we use at v1

- **Sorting** (click column header) — universal
- **Filtering** (per-column predicate) — on every column
- **Pagination** OR virtualization (see below)
- **Column visibility toggle** — the gear icon in column headers
- **Column ordering** (drag) — Pro-grade affordance for power users
- **Row selection** — for the "compare these" workflow
- **Sticky headers** — long forecast lists keep column headers fixed

## Virtualization decision

For the all-forecasts page (14k forecasts at v1 release, ~250k at Y1), pagination at 50/page is the fallback. For the power-user "show me everything" view, swap to **TanStack Virtual** (sibling library, ~3 KB):

```tsx
import { useVirtualizer } from "@tanstack/react-virtual";

const virtualizer = useVirtualizer({
  count: rows.length,
  getScrollElement: () => parentRef.current,
  estimateSize: () => 32,  // tile row height in px
  overscan: 12,
});
```

Renders only ~30 rows in DOM at a time, regardless of total. Hits 60fps with 100k rows on a 2018-era laptop.

## Server-side vs client-side

| Surface | Strategy | Why |
|---|---|---|
| Country page forecast table (~20 rows) | client-side | tiny, no need |
| Indicator page cross-country (~22 rows) | client-side | same |
| All-forecasts page (~14k rows v1) | server-side filtering, client-side sort/page | typical use is filter-down then browse |
| Leaderboard (~30 rows per cell) | client-side | small per cell |
| Accountability ledger miss table (~2k rows) | server-side pagination | grows unbounded |
| Coverage matrix (~22 × 6 × 5 = 660 cells) | client-side | static grid |

The `/api/forecasts.json?country=USA&indicator=gdp_yoy&horizon=4Q` endpoint takes the same filter params TanStack uses client-side; we pass through to the FastAPI service which delegates to TimescaleDB.

## Accessibility

- `<table>` semantic element (not divs) — TanStack accommodates either; we use the semantic version per L266 a11y rules.
- `<caption>` element on every table identifying it (often `aria-hidden`-screen-reader-only).
- Sort buttons in column headers use `aria-sort="ascending|descending|none"`.
- Virtualized rows announce row count via `aria-rowcount` on the table and `aria-rowindex` on each row.

## Performance budget

- The `/forecasts` page must render TTFB ≤ 200ms at the edge, LCP ≤ 1.5s.
- TanStack Table contributes ~10 KB gzipped. Acceptable.
- TanStack Virtual contributes ~3 KB gzipped. Acceptable.

## What this loop produced

- TanStack Table picked over AG Grid / MUI / Glide
- Composition pattern with per-cell renderers
- Virtualization pick (TanStack Virtual) for >1k rows
- Server-side filtering threshold (~14k rows triggers SSR delegation)
- A11y conformance plan

## What comes next

- L100 — Plotly Resampler for million-point series (sibling decision)

## Related

- [[L070-tanstack-aggrid-glide]] — the survey
- [[L256-tanstack-table-grids]] (in Phase 5 batch) — the implementation note
- [[L266-270-quality-deploy]] — a11y conformance baked in
