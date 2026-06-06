# L273 — V&V Matrix for the Dashboard Layer

**Loop**: 273 / 300
**Phase**: 6 — Synthesis + launch
**Date**: 2026-06-06

---

## The thesis of this loop

The forecast V&V matrix lives at [[L194-coverage-page]] and covers calibration, coverage, CRPS, PIT, and the model-level evidence. This loop specifies the *dashboard* V&V matrix — the invariants the presentation layer must hold. Perf, accessibility, SEO, embed reliability, MCP round-trip, time-to-first-pixel. These are the dashboard-layer truths that get audited every release.

Dashboard V&V matters because the L008 promises are unverifiable if the dashboard is slow, inaccessible, or unparseable by search engines and LLMs. A vintage-stamped forecast is no use if the page that surfaces it lighthouse-fails. The promise lives or dies in the rendering layer.

This matrix becomes a CI gate. PRs that regress a budget block.

---

## The matrix

Seven invariant categories, each with budgets, measurement methods, ownership, and what-happens-on-failure.

### 1. Lighthouse performance budget

| Route | LCP (P75) | INP (P75) | CLS | Total bundle (gzipped) |
|---|---|---|---|---|
| `/` (home) | ≤ 1.5s | ≤ 100ms | ≤ 0.05 | ≤ 250kb |
| `/countries/[iso3]` | ≤ 1.5s | ≤ 150ms | ≤ 0.05 | ≤ 250kb |
| `/indicators/[id]` | ≤ 1.8s | ≤ 150ms | ≤ 0.05 | ≤ 300kb |
| `/forecasts/[c]/[i]/[h]` | ≤ 2.0s | ≤ 200ms | ≤ 0.05 | ≤ 400kb (charts) |
| `/scenarios/[slug]` | ≤ 1.8s | ≤ 150ms | ≤ 0.05 | ≤ 300kb |
| `/leaderboard` | ≤ 2.5s | ≤ 300ms | ≤ 0.10 | ≤ 800kb (Perspective wasm) |
| `/accountability` | ≤ 1.5s | ≤ 100ms | ≤ 0.05 | ≤ 250kb |
| `/embed/[id]` | ≤ 1.0s | ≤ 100ms | ≤ 0.05 | ≤ 150kb |

**Measurement.** Lighthouse CI runs on every PR + nightly on production. We use the median of five runs; we fail on P75 not P50 because tail latency is the user experience that compounds into churn.

**Ownership.** Frontend engineer. Failures are P0 within the sprint they appear.

**On failure.** PR is blocked. The blocking message includes a link to the perf-budget doc and the three biggest regressors. If a feature legitimately requires a budget increase, the PR amends the budget *first*, in a separate PR with explicit justification, before the feature lands.

### 2. Accessibility (a11y) score

| Invariant | Target |
|---|---|
| axe-core violations (critical + serious) | 0 |
| Lighthouse a11y score | ≥ 95 (all routes) |
| Keyboard navigation completeness | 100% (every interactive element reachable via Tab) |
| Color contrast | WCAG AA on all text; AAA on body text |
| Screen-reader smoke test | NVDA pass on home + country + forecast detail + accountability |
| Focus visible indicator | Always (no `outline: none` overrides) |
| Form labels | Every input has an associated label or `aria-label` |
| Heading hierarchy | Sequential (h1 → h2 → h3, no skipping levels) |

**Measurement.** axe-core in Playwright on every PR. Manual NVDA smoke test before each release. Color contrast is enforced by the design system (L148) — no ad-hoc colors permitted.

**Ownership.** Frontend engineer + monthly external a11y audit (eventually).

**On failure.** axe critical/serious violations block the PR. Lighthouse a11y < 95 blocks the PR. NVDA smoke-test failure blocks the release (not the PR).

### 3. SEO score

| Invariant | Target |
|---|---|
| Lighthouse SEO score | ≥ 95 (all routes) |
| `<title>` present and unique per route | 100% |
| `<meta name="description">` present and ≤ 160 chars | 100% |
| Canonical URL declared | 100% |
| Open Graph + Twitter Card meta | 100% (image, title, description) |
| JSON-LD schema markup | `Dataset`, `Observation`, `Article`, `Organization` on relevant routes |
| robots.txt + sitemap.xml | Live, sitemap auto-generated nightly |
| Mobile-friendly | Yes (PWA-style responsive) |
| Crawlable (no JS-blocking key content) | All canonical content is server-rendered |
| Internal link graph | Country ↔ indicator ↔ forecast ↔ methodology cross-linked |

**Measurement.** Lighthouse SEO on every PR. Sitemap diff tracked in CI. JSON-LD validates against schema.org's structured-data testing tool nightly.

**Ownership.** Frontend engineer + content lead.

**On failure.** Lighthouse SEO < 95 blocks the PR. Missing JSON-LD on a page that should have it blocks the PR. Sitemap drift triggers a P1 alert.

### 4. Embed-in-the-wild test

The embed widget is the highest-leverage distribution surface — every chart Damian pastes into a YouTube video, every chart Marcus pastes into an FT column, every chart Lin pastes into a Substack post. If the embed breaks in the wild, we don't find out from a CI test; we find out from a user complaint days later.

**Invariants.**

| Host | Iframe works | Script SDK works | Static PNG fallback works |
|---|---|---|---|
| Substack | Y | Y | Y |
| Ghost | Y | Y | Y |
| WordPress (self-hosted) | Y | Y | Y |
| WordPress.com | Y | (no script allowed) | Y |
| Medium | (iframe limits) | (no script) | Y |
| Reddit | (no iframe in posts) | (no script) | Y |
| Notion | Y | (no script) | Y |
| Bluesky | (no iframe) | (no script) | Y (with og:image fallback) |
| LinkedIn article | (no iframe) | (no script) | Y |
| Twitter / X | (no iframe) | (no script) | Y (via Twitter Card meta) |
| Beehiiv | Y | Y | Y |

**Measurement.** Synthetic embed tests run weekly against canary pages we maintain on each host. A custom Playwright harness loads the host, scrolls to the embed, and asserts the chart rendered. If a host changes its CSP and breaks our embed, we get an alert.

**Ownership.** Frontend engineer + distribution lead.

**On failure.** Host-level breakage is a P1 (we fix or document the limitation within 5 business days). Static-PNG fallback failure is a P0 (it's the universal fallback).

### 5. MCP tool round-trip latency

The MCP server is how LLMs ground in OPENGEM. If it's slow, the LLM-grounding experience is bad and the passive-distribution flywheel stalls.

**Invariants.**

| Tool | P50 | P95 | P99 |
|---|---|---|---|
| `get_forecast` | ≤ 200ms | ≤ 800ms | ≤ 1500ms |
| `compare_forecasts` | ≤ 400ms | ≤ 1500ms | ≤ 3000ms |
| `list_scenarios` | ≤ 150ms | ≤ 500ms | ≤ 1000ms |
| `get_recession_probability` | ≤ 200ms | ≤ 800ms | ≤ 1500ms |
| `get_gpr_nowcast` | ≤ 150ms | ≤ 500ms | ≤ 1000ms |
| `rewind_vintage` | ≤ 400ms | ≤ 1500ms | ≤ 3000ms |
| `get_leaderboard` | ≤ 500ms | ≤ 2000ms | ≤ 4000ms |
| `list_misses` | ≤ 200ms | ≤ 800ms | ≤ 1500ms |

**Measurement.** Cloudflare Workers RUM telemetry. Synthetic MCP tool calls from three geo-distributed regions (us-east, eu-west, ap-southeast) every minute. P95 over rolling 24h window.

**Ownership.** Backend engineer + SRE rotation (founder for now).

**On failure.** P95 breach for 1 hour triggers a P2 alert. P95 breach for 6 hours or P99 breach for 1 hour triggers P1. Cause analysis published in the changelog within 7 days for any sustained breach.

### 6. Time-to-first-pixel (TTFP) by route

Lighthouse LCP is a good single number, but for our information-density-first UX, the time the user sees *something useful* (a sparkline, a number, a country flag) matters more than the time the page is fully loaded. We measure TTFP separately.

**Invariants.**

| Route | TTFP (P75) | Definition |
|---|---|---|
| `/` | ≤ 800ms | First indicator tile fully rendered with value + sparkline + delta |
| `/countries/[iso3]` | ≤ 800ms | Country header + first situation tile rendered |
| `/indicators/[id]` | ≤ 1000ms | Cross-country sparkline grid rendered |
| `/forecasts/...` | ≤ 1200ms | Bands chart rendered with at least 3 quantile lines |
| `/scenarios/[slug]` | ≤ 800ms | Scenario header + probability pill rendered |
| `/leaderboard` | ≤ 2000ms | Skeleton grid rendered; data fill within 4000ms |
| `/accountability` | ≤ 800ms | Four-tile scoreboard rendered with values |
| `/embed/[id]` | ≤ 500ms | Chart rendered |

**Measurement.** Custom RUM beacons fire on the first paint of the named element. Sampled at 1% of real user sessions; aggregated in Plausible/Umami-compatible custom-event store.

**Ownership.** Frontend engineer.

**On failure.** TTFP breach is a P2 alert. We treat TTFP as a leading indicator of Lighthouse perf regression — if TTFP drifts, Lighthouse usually follows in the next release.

### 7. Provenance + cite-this-view integrity

Every chart must resolve to its source. Every cite-this-view URL must resolve permanently. These are not perf invariants; they are *promise* invariants that need automated verification.

**Invariants.**

| Invariant | Target | Measurement |
|---|---|---|
| Every chart has a methodology pop-up link | 100% | Playwright assertion across all routes |
| Every data point's hover surfaces its source citation | 100% | Playwright assertion on key routes |
| Every cite-this-view URL resolves with HTTP 200 + chart render | 99.99% | Synthetic test against a sampled cite-URL set, daily |
| Every cite-this-view URL renders the chart *as it was at vintage time*, not as-of-now | 100% | Property-based test: render at vintage T, compare to snapshot from T |
| Forecast detail pages link to vintage history | 100% | Playwright assertion |
| Every miss in `/accountability` has a working post-mortem link | 100% | Daily link-checker job |
| RSS feeds parse correctly per the W3C feed validator | 100% | Nightly validator |
| OpenGraph image renders correctly per the Facebook debugger | 100% | Nightly check on top 1000 URLs |

**Measurement.** Mix of unit tests (in CI), Playwright (in CI + nightly on prod), and synthetic monitors (continuous). The promise-invariants are the *brand* tests; they take precedence over performance tests if the two conflict.

**Ownership.** Backend + frontend + content lead jointly. Failure on any invariant in this category is a P0 — the brand depends on these.

**On failure.** Any P0 promise-invariant failure halts the release pipeline. A documented incident is published on the changelog page within 48 hours describing what broke, why, and what we changed.

---

## How V&V is run

| Cadence | What runs | Where |
|---|---|---|
| Every PR | Lighthouse CI (sampled routes), axe-core, JSON-LD validator, unit tests, type-check | GitHub Actions |
| Nightly | Full Lighthouse sweep (all routes × 5 runs), embed-in-the-wild synthetic, MCP synthetic from 3 geos, cite-URL sampler, RSS validator | GitHub Actions + Cloudflare Cron |
| Weekly | Full embed-in-the-wild against all 11 hosts, full a11y NVDA smoke test (manual), promise-invariant property tests | Engineer rotation |
| Quarterly | External a11y audit (Y2+), external pen test on MCP, external SEO audit | Vendor-contracted |

Telemetry feeds an internal `/internal/vv` page that the team reads weekly. Public-facing V&V status (not the full numbers, but pass/fail per category) is published on the `/about/vv` page, refreshed daily.

---

## V&V vs the L008 five promises

Each V&V category maps to one or more of the five promises from [[L008-differentiation]]:

- **Promise 1 (publish every forecast)** → Provenance + cite-this-view integrity (Category 7)
- **Promise 2 (name every miss)** → Accountability ledger link-checker (Category 7)
- **Promise 3 (open methodology)** → Methodology pop-up coverage (Category 7)
- **Promise 4 (cite every number)** → Hover-source-citation coverage (Category 7)
- **Promise 5 (embed everything)** → Embed-in-the-wild (Category 4) + MCP latency (Category 5)

Perf + a11y + SEO + TTFP (Categories 1, 2, 3, 6) are the *delivery* invariants — they ensure the promises actually reach the user. The provenance + cite invariants (Category 7) are the *truth* invariants — they ensure the promises hold.

A perfect V&V score means OPENGEM is structurally honest. A failing V&V is the brand crumbling. The matrix is therefore *the* brand-defense apparatus.

---

## What this loop produced

- Seven V&V invariant categories with budgets, measurement, ownership, and on-failure actions.
- Mapping from V&V categories to L008 five-promise invariants.
- Cadence schedule for CI, nightly, weekly, quarterly runs.
- A `/about/vv` public page surfacing daily V&V status.

## What comes next

- **L274** — KPI dashboard (meta) referencing V&V status as a quality input.
- **L266** (Phase 5) — a11y audit script that operationalizes Category 2.
- **L267** (Phase 5) — Lighthouse perf budget script that operationalizes Category 1.
- **L268** (Phase 5) — Playwright visual regression tests that overlap with Categories 2, 4, 7.

## Related

- [[L008-differentiation]] — the five promises the V&V matrix defends
- [[L194-coverage-page]] — the forecast-level V&V (this loop is the dashboard companion)
- [[L271-master-prd]] — Section 11 references this matrix
- [[L266-a11y-audit-script]] / [[L267-lighthouse-budget]] / [[L268-visual-regression]] — Phase 5 prototype scripts
