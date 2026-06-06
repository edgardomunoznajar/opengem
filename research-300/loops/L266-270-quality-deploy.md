# L266-L270 — A11y, perf, visual regression, deploy plan, dev container (batch)

**Loops**: 266, 267, 268, 269, 270 / 300
**Phase**: 5 — Code prototypes
**Date**: 2026-06-06

---

## L266 — A11y audit script

**File**: `prototypes/dashboard-next/package.json` already includes Playwright; an `axe-core` integration test is the v0.2 task.

Rules-as-code:
- All SVG sparklines have `aria-hidden="true"` (decorative; the numeric value is read).
- All numeric tiles have `aria-label` of the form `{label}: {value} {unit}, {direction} {delta} from previous`.
- Color is never the only signal — pills carry text + color, the recession-probability badge is "R 32%" not just a red dot.
- Tab order: top-nav left-to-right, then main content top-to-bottom, then footer.
- ⌘K palette is keyboard-only navigable (arrow keys, enter, escape).
- Tables get `<caption>` + `scope="col|row"` on headers.

CI gate: axe-core scan on every PR must report zero violations of "wcag2a" + "wcag2aa".

## L267 — Lighthouse perf budget

**File**: `prototypes/dashboard-next/lighthouse.budget.json` (deferred to v0.2 install).

Targets:
- Performance ≥ 90
- Accessibility ≥ 95
- Best Practices ≥ 95
- SEO ≥ 95
- LCP ≤ 1.8s on Slow 4G
- TBT ≤ 200ms
- Total JS ≤ 100 KB gzipped (server components do the heavy lifting)
- Total CSS ≤ 30 KB gzipped (Tailwind v4 + globals)

The 100KB JS budget is generous because the dashboard is mostly server-rendered. The interactive bits — command palette, theme toggle, charts on detail pages — are client islands.

## L268 — Visual regression test

**File**: `prototypes/dashboard-next/tests/playwright/visual.spec.ts` (deferred).

Coverage:
- Home page (1440×900) — desktop
- Home page (360×740) — mobile
- Country page (each Tier-V country) — desktop
- Indicator page (each canonical indicator) — desktop
- Forecasts page (large viewport) — table rendering integrity
- Accountability page (the unique surface)
- Command palette open with query

Snapshot store: `tests/__snapshots__/`. Pixel-diff threshold: 0.2% (allows for anti-aliasing variance). Run on every PR.

## L269 — Deploy plan: Cloudflare Pages + Workers + R2

**Decision locked.**

| Component | Host | Why |
|---|---|---|
| Next.js dashboard | Cloudflare Pages | Edge SSR, generous free tier, $5/mo paid tier handles 10x of any reasonable startup volume |
| Embed SDK + static assets | Cloudflare R2 + Pages | Versioned `/embed/v1.js`, immutable assets |
| FastAPI API service | Fly.io (Python) | Cheap (1 shared-cpu-1x machine = $2/mo), simple deploy, Postgres via Fly Postgres |
| TimescaleDB | Fly.io Postgres or Neon | Both have Postgres + TimescaleDB extension support |
| Cold vintage tier | Cloudflare R2 | Parquet-per-vintage, sql-queryable via DuckDB-WASM |
| Datasette public ledger | Fly.io ($5/mo machine) | The L076 surprise pick — strategically important |
| MCP server | Fly.io + Cloudflare Worker (SSE proxy) | stdio for desktop clients, SSE for ChatGPT Connectors |
| Plausible analytics | Fly.io (single small machine, $5/mo) | Self-hosted, transparent dashboard |

Total monthly hosting at v1 launch: ~$25/mo. At Y1 with 10k DAU and 5k MCP daily users: ~$120/mo. At Y3 with 100k DAU: ~$800/mo. Cloud-bill-viable in spirit and in math.

## L270 — Dev container + Codespaces config

**File**: `prototypes/dashboard-next/.devcontainer/devcontainer.json` (deferred to v0.2).

```json
{
  "name": "OPENGEM Dashboard",
  "image": "mcr.microsoft.com/devcontainers/typescript-node:20",
  "features": {
    "ghcr.io/devcontainers/features/python:1": { "version": "3.12" },
    "ghcr.io/devcontainers/features/node:1": { "version": "20" }
  },
  "forwardPorts": [3000, 8001],
  "postCreateCommand": "npm install && cd ../api-stub && pip install fastapi uvicorn pydantic",
  "customizations": {
    "vscode": {
      "extensions": [
        "bradlc.vscode-tailwindcss",
        "esbenp.prettier-vscode",
        "dbaeumer.vscode-eslint",
        "ms-python.python"
      ]
    }
  }
}
```

Codespaces hits the same config — single-click "Open in Codespaces" from the GitHub README boots the entire dev environment in 90s.

## What this loop produced (across 5 sub-loops)

- A11y rule catalog
- Lighthouse budget targets
- Visual regression coverage plan
- Cloudflare + Fly.io deploy stack (total ~$25-120/mo at v1-Y1)
- Devcontainer for one-click setup

## What comes next

- L271 — Master World Dashboard PRD (Phase 6, agent producing)
- L273 — V&V matrix for the dashboard layer (Phase 6, agent producing)
- L274 — KPI dashboard for the dashboard (Phase 6, agent producing)

## Related

- [[L117-accessibility-audit-framework]] — design spec for L266
- [[L075-static-site-dashboards]] — informs L269 Cloudflare pick
- [[L076-datasette-dclient]] — L076 surprise pick lives at Fly.io ($5/mo)
- [[L079-prefect-dagster-airflow]] — Dagster stays; orchestrates the data side
