# L257-L259 — Vintage rewinder + track-record + accountability ledger (batch)

**Loops**: 257, 258, 259 / 300
**Phase**: 5 — Code prototypes
**Date**: 2026-06-06
**Artifacts**: in `prototypes/dashboard-next/app/`

---

This batch covers the three pages that, together, are OPENGEM's structural moat — "publishes its mistakes" as a working surface.

## L257 — Vintage rewinder

**File**: `app/vintage/page.tsx`

Index of recent vintages with date + label + counts (scenarios triggered, forecasts published) per vintage. URL grammar block:

```
/vintage/YYYY-MM-DD                                — vintage index for that day
/vintage/YYYY-MM-DD/countries/USA                  — country page at vintage
/vintage/YYYY-MM-DD/forecasts                      — all forecasts at vintage
/vintage/YYYY-MM-DD/scenarios                      — scenarios triggered at vintage
/diff/YYYY-MM-DD..today/forecasts/USA/gdp_yoy      — diff one forecast across vintages
```

Includes a "What rewinding does NOT do" block — important honesty: it shows what we *forecast*, not nowcasting-the-past with today's code.

**Why this matters**: vintage URLs are the foundation of the entire publication discipline. Without them, "publishes its mistakes" is rhetoric. With them, any miss is a literal diff between two URLs.

## L258 — Forecast diff prototype (deferred to v0.2)

**Status**: DESIGN-LOCKED.

Plan: `app/diff/[range]/[...path]/page.tsx` will render a forecast-revision view — multiple vintage points stacked as faint horizontal bars + the "revision arrow" connecting them. The L159 design loop has the precise visual.

## L259 — Track-record + Accountability ledger pages

**Files**: `app/track-record/[indicator]/page.tsx` + `app/accountability/page.tsx`

### Track-record page

Per-indicator scoring page. Overall tiles: CRPS (vs AR(1) % improvement), PIT, Hit rate, DM p-value. V&V matrix table — Country × Horizon with PASS/WARN/FAIL pill per cell. Calibration plot table — PIT bucket × Expected × Observed × Δ (color-coded by absolute deviation).

The page is *primary internal proof* — when an academic, journalist, or paid customer asks "show me the calibration", we link them here. It is *the page that doesn't exist anywhere else in the world* with this transparency level.

### Accountability ledger (the headline page)

Summary tiles: Published (14,283), Scored (11,902), Outside band (2,117 — 17.8% vs 20% target), Pending (264). Recent misses table — top 3 by magnitude with vintage, country, indicator, horizon, forecast value, actual, miss, why-paragraph, post-mortem link.

The "Publication discipline" block at the bottom restates the five rules: vintage permanence, miss-in-place, consensus side-by-side, reproducibility envelope, calibration as a target.

**Why this matters**: this is the *single most important page in the entire dashboard*. Every other surface (Pulse, Countries, Indicators, Forecasts, Scenarios) exists to feed this one. Every other dashboard in the world hides its misses. This one surfaces them with a counter.

## The design discipline these three pages enforce

1. **Permanence**: every forecast URL is permanent, even when the forecast was wrong. Editing in place is forbidden.
2. **Miss-in-place**: a miss does not move the forecast off its original URL. A post-mortem appears at the same URL.
3. **Consensus side-by-side**: the WEO / OECD EO / SEP overlay is on every forecast, so misses are seen in context.
4. **Reproducibility envelope**: git_sha + data_lockfile_hash + container_digest + generated_at — replay anytime.
5. **Calibration as a target**: the ≤20% out-of-band-at-80% target is published on the accountability page. When we drift above it, we say so on that page.

## Open ledger publication targets

| Frequency | Artifact |
|---|---|
| Daily | Pulse + situation indicators + new forecasts |
| Weekly | Updated leaderboard + miss-log entries for scored forecasts |
| Monthly | New scenario packs + retired pack post-mortems |
| Quarterly | Full V&V matrix update + calibration plot refresh |
| Annually | Multi-year track record summary + retro |

## What this loop produced

- Working `/vintage` rewinder index page
- Working `/track-record/[indicator]` page with V&V matrix + calibration plot
- Working `/accountability` ledger page with miss-log
- The publication discipline rules made concrete in UI

## What comes next

- L255 — Plotly Resampler embed for 1M-point series
- L256 — TanStack Table grid for indicator grid
- L258 — Forecast-diff visual prototype (deferred above)

## Related

- [[L008-differentiation]] — "publishes its mistakes" is the moat
- [[L132-provenance-vintage-drawer]] — design spec
- [[L133-forecast-leaderboard-page]] — sibling page
- [[L134-track-record-page]] — design spec for L259
- [[L173-vintage-time-machine]] — design spec for L257
- [[L175-accountability-page]] — design spec for the ledger page
- [[L182-forecast-vintage-lineage]] — the underlying mechanism
- [[L186-reproducibility-envelope]] — the implementation spec
- [[L298-postmortem-template]] — the template for individual miss writeups
