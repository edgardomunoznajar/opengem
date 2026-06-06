# L261-L265 — Onboarding, theme toggle, mobile, empty states, telemetry (batch)

**Loops**: 261, 262, 263, 264, 265 / 300
**Phase**: 5 — Code prototypes
**Date**: 2026-06-06

---

## L261 — Onboarding flow

**File**: design-locked; implementation `app/onboarding/page.tsx` deferred to v0.2.

3-step flow:
1. **Email + role tag** (sole required field: email; role is dropdown — analyst / researcher / journalist / academic / curious / other)
2. **Pick 3 watchlist items** (countries + indicators, shadcn-style multiselect with autocomplete)
3. **Confirmation + (optional) API key + MCP install snippet**

Design discipline:
- No password. Magic-link auth (Resend-powered).
- The watchlist becomes the cookie-less personalization layer.
- Pro tier upgrade is offered on step 3 but never gates step 1–2.

## L262 — Dark/light theme toggle

**File**: `app/layout.tsx` defaults `dark`; toggle component deferred but layout is theme-aware via Tailwind `dark:` modifier.

Decision: terminal-amber-on-near-black is the default. Light theme is a paper-FT-pink-on-cream alternate for editorial/print contexts. Both palettes are codified in `tailwind.config.ts`.

The toggle goes in the top nav (left of search palette). State persists in localStorage as `opengem-theme: dark | light | system`.

## L263 — Mobile layout

**File**: design-locked.

Decisions:
- 360px viewport gets a *radically reduced* IA: World Pulse → Country (single) → Indicator (single) → Scenarios → Methodology.
- Hide: leaderboard, accountability, forecasts grid, events feed (these are RSS-served on mobile).
- Tile grid collapses to 1-column. Sparklines stay (visual data signal). Tables become card lists.
- The command palette is the primary navigation on mobile. The top nav collapses to a single hamburger that opens it.

## L264 — Empty / loading / error states

**Files**: pages currently render fixture data; states are designed but not wired.

Catalog:
- **Empty**: "No forecasts found for {country} × {indicator}. OPENGEM tracks {N} countries on {M} indicators." + link to coverage page.
- **Loading**: skeleton tile (animated `bg-line` rectangle of same dims) — *never* a generic spinner.
- **Stale (>24h since adapter run)**: yellow border on the tile + tooltip "Last refresh 26h ago — see status page".
- **API failure**: tile shows "—" with subtle warning pill; never empty.
- **Wrong country code** (e.g. /countries/XYZ): friendly "We don't track XYZ yet. {N} countries tracked — see coverage" + suggest closest match.

## L265 — Telemetry

**File**: design-locked. Plausible chosen (over Umami, GA4).

Privacy-respecting decisions:
- No third-party cookies. No fingerprinting.
- Plausible self-hosted at `analytics.opengem.org` — open-source, MIT, CC-BY-data-dump.
- Track only: page views, embed renders, MCP tool calls (server-side), API hits (server-side), search-palette opens.
- Do NOT track: scroll depth, hover heatmaps, individual user paths.
- All telemetry is *also* on a public dashboard (`/about/telemetry`) — even our own analytics are open.

The "even our analytics are open" gesture is small but consistent with the rest of the editorial discipline.

## What this loop produced (across 5 sub-loops)

- 3-step onboarding designed (impl deferred to v0.2)
- Theme system in `tailwind.config.ts` (dark default, light variant locked)
- Mobile IA collapsed (1-column, command-palette-primary nav)
- Empty / loading / error catalog
- Telemetry pick: Plausible self-hosted + public own-analytics dashboard

## What comes next

- L266 — A11y audit script
- L267 — Lighthouse perf budget script
- L268 — Visual regression test (Playwright + snapshot)

## Related

- [[L139-onboarding-flow]] — design spec for L261
- [[L142-mobile-information-density]] — design spec for L263
- [[L140-empty-states]] — design spec for L264
- [[L141-error-degraded-states]] — design spec for L264
- [[L145-dashboard-themes]] — design spec for L262
