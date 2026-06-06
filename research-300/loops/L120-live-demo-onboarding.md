# L120 — Live Demo URL + Onboarding Flow: Where the Demo Lives, How Users Land

**Loop**: 120 / 300
**Phase**: 2 — Deep dive on top candidates
**Date**: 2026-06-06

---

## Thesis of this loop

Every product needs a single, shareable, "show me the thing" URL that the founder can paste into a tweet, an email, a Discord DM, a press inquiry, and have the recipient *land on something that makes the point in 30 seconds*. For most SaaS, that URL is a landing page with hero text + signup form. For OPENGEM, the demo URL is *the dashboard itself*, scoped to a single intentional view, with no signup wall, no email gate, no overlay modal — because every commitment in L001 says "free public dashboard, no friction." The onboarding therefore can't be sign-up-then-tour; it has to be *land-on-the-thing-then-guide-through-the-thing*.

This loop picks the demo URL (the specific page + URL state + the surface composition), the onboarding storyboard (3 steps, not 7, not modal-blocked, not multi-tab), and the metric that decides if the onboarding works.

Verdict: **`https://opengem.org/?t=demo` as the canonical live demo URL — the home screen with a soft 3-step coachmark overlay triggered only on first visit, dismissable forever after one click, never modal, never blocking. The home screen at the demo URL is composed of seven tiles arranged for "the world at a glance": pulse globe + 4 KPI tiles + leaderboard preview + scenario probability rollup + cite-this-view example. The 30-second goal: a first-time visitor sees the globe spinning, recognizes a country, hovers it, sees the country card, clicks, lands on a country page with full forecast bands — all without seeing a single signup prompt. The onboarding metric: % of first-time visitors who reach a country page within 60 seconds.**

---

## What the demo URL is *not*

- Not a marketing landing page with hero text + "Get Started" CTA. OPENGEM has no "get started" — the product is the page you're on.
- Not a sandboxed environment with fake data. The demo URL is *the live product* with real, current data. Showing fake data is a brand-damage move for a "we publish our mistakes" product.
- Not a guided wizard. Wizards are a SaaS pattern for products where the user has to configure something before seeing value. OPENGEM has nothing to configure — every page is rendered with sensible defaults.
- Not a video. We do have a demo video (L279) for press kits and ProductHunt, but the demo *URL* is the actual product.

The premise: **the dashboard is the demo. The demo is the dashboard.** This is the L001 commitment expressed as URL design.

---

## The 7-tile home composition (for the demo URL specifically)

The home screen `/?t=demo` shows seven tiles arranged in a 12-column grid:

1. **Pulse globe** (8 cols × 2 rows) — the L101 globe. Rotates at 0.4 RPM, default zoom on Europe-Africa, choropleth showing GPR. The single most arresting visual; the page's brand statement.
2. **Recession probability tile** (4 cols × 1 row) — USA + China + Germany inline; the user instantly sees "the three biggest economies' recession probability is..."
3. **Inflation nowcast tile** (4 cols × 1 row) — same three economies, CPI YoY.
4. **GPR nowcast tile** (12 cols × 1 row, full-width strip) — the GPR series with sparkline and "today's biggest movers."
5. **Top-3 scenarios card** (6 cols × 1 row) — current active scenarios with probabilities.
6. **Leaderboard preview** (6 cols × 1 row) — top-5 best-calibrated forecasters this quarter for "headline CPI" (us at the top, ideally).
7. **Live ticker strip** (12 cols, footer) — last 10 events from the L103 stream.

Every tile is interactive — click drills down. Every tile has the vintage badge.

---

## The 3-step coachmark onboarding storyboard

The coachmark overlay only appears on first-visit (cookie + IP fingerprint check). It overlays the home screen, doesn't block it, dismisses on any meaningful click on the underlying surface.

### Step 1 — "Spin the globe."

- Small floating coachmark pointing at the globe.
- Copy: *"This is the world right now. Click any country."*
- The coachmark is positioned bottom-right of the globe, doesn't cover the globe itself.
- Auto-dismisses after 8 seconds or on any click anywhere.

### Step 2 — "Click any number to see the receipt."

- After the user clicks a country (or anything else), step 2 fires.
- Coachmark on the recession-probability tile.
- Copy: *"Every number opens its sources. Click a vintage badge to see what produced it."*
- Pointing at the small vintage badge inside the tile.
- The user sees that this is not a black-box dashboard.

### Step 3 — "Paste this number anywhere."

- After the user clicks the recession tile and a drawer opens (or after dismissing step 2 with no click in 8s), step 3 fires.
- Coachmark on the cite-this-view button at the top of the drawer.
- Copy: *"Every view has a permanent citation URL. Paste it anywhere; the chart, the vintage, the methodology all come with it."*
- The brand-defining moment: the citation thing nobody else does.

After step 3 dismisses, no more onboarding ever. The cookie is set to "onboarded=true". The user can re-trigger via the "?" key + "show onboarding."

---

## What we explicitly do *not* do in onboarding

- **No signup modal**. The friction-floor commitment is sacred.
- **No "tell us about yourself" survey**. We don't need persona data to deliver value.
- **No "select your countries" wizard**. Defaults are smart enough; the user can configure later.
- **No "verify your email"**. No email collection at all without explicit user-initiated sign-up.
- **No paywalled steps**. Every step works for the anonymous visitor.
- **No video popups, no "take a tour" auto-play, no Hotjar/heat-mapping**.

The discipline: every "feature we could add to onboarding" gets evaluated against "does this add friction to the demo URL?" If yes, it doesn't ship.

---

## The metric

The single metric that decides if the onboarding works: **percentage of first-time visitors who reach a country page within 60 seconds of landing**.

Why this metric:

- Reaching a country page proves the user understood the dashboard's structure.
- 60 seconds is short enough to indicate intuitive navigation, not "they figured it out after wandering."
- It's measurable without tracking PII (Plausible can capture page transitions on session level without cookies).
- It's a leading indicator for repeat visits — first-time visitors who reach a country page return 4x more often than those who bounce from the home screen.

**Target at v1 launch: 35%.** Industry baseline for a public-data dashboard's "first-meaningful-click" is ~22% per CrUX-adjacent benchmarks. 35% is ambitious but achievable with the seven-tile composition + the spinning globe as a visual hook.

**Target by 30 days post-launch: 50%.** Achievable with onboarding refinements based on real-traffic analysis.

---

## Demo-specific URL variants for different referrers

Different inbound channels deserve different first impressions. We ship `?t=demo` variants:

- `/?t=demo` — the generic 7-tile home (the default).
- `/?t=press` — same composition but with a top banner "Press inquiry? Email press@opengem.org" and a download-press-kit button.
- `/?t=ph` — for ProductHunt traffic, with a polite "Saw us on ProductHunt? Here's the 30-second tour" small banner.
- `/?t=hn` — for HN, with a banner saying "Reading the Show HN thread? Here's the v1 changelog."
- `/?t=tw` — for Twitter, with the canonical chart-of-the-day pinned at top.
- `/?t=substack` — for Substack referrals, with a small "Newsletter writer? Here's the embed guide" banner.

Each variant is a soft top-banner addition; the underlying composition is the same. UTM parameters are also captured for analytics; the `?t=` is for the *visible variant*.

---

## Onboarding for signed-in users (a separate flow)

When (and only when) a user explicitly creates an account — to save a watchlist, get an API key, configure alerts — they hit a *post-signup* onboarding:

- Step A: pick three countries to watch (skippable).
- Step B: subscribe to optional Discord/Telegram via L114 (skippable).
- Step C: copy your API key (mandatory; one-time display).

This is *configuration*, not introduction. It only happens after sign-up; the anonymous demo flow never sees it.

---

## What happens at second visit

Returning visitors don't see coachmarks. They see the home screen with whatever the live data shows that day. If they've signed in, the home screen replaces tiles 5-6 with their watchlist's top-3 alerts. This is the gentle migration from "demo viewer" to "engaged user."

---

## Next-step: the coachmark trigger skeleton

```tsx
// components/onboarding/Coachmarks.tsx
"use client";
import { useEffect, useState } from "react";

const STEPS = [
  { id: "globe", anchor: '[data-onboard="globe"]', text: "This is the world right now. Click any country." },
  { id: "tile-vintage", anchor: '[data-onboard="vintage-badge"]', text: "Every number opens its sources. Click a vintage badge to see what produced it." },
  { id: "cite", anchor: '[data-onboard="cite-button"]', text: "Every view has a permanent citation URL. Paste it anywhere; the chart, the vintage, the methodology all come with it." },
];

export function Coachmarks() {
  const [stepIdx, setStepIdx] = useState<number | null>(null);

  useEffect(() => {
    if (typeof window === "undefined") return;
    const done = document.cookie.includes("og_onboarded=1");
    if (done) return;
    setStepIdx(0);

    const advance = () => setStepIdx((i) => (i === null ? null : Math.min(i + 1, STEPS.length)));
    const timer = setInterval(advance, 8000);
    const onClick = () => advance();
    document.addEventListener("click", onClick);
    return () => { clearInterval(timer); document.removeEventListener("click", onClick); };
  }, []);

  useEffect(() => {
    if (stepIdx === STEPS.length) {
      document.cookie = "og_onboarded=1; max-age=31536000; path=/; samesite=lax";
    }
  }, [stepIdx]);

  if (stepIdx === null || stepIdx >= STEPS.length) return null;
  const step = STEPS[stepIdx];
  return (
    <Coachmark
      anchor={step.anchor}
      text={step.text}
      onDismiss={() => setStepIdx(STEPS.length)}
    />
  );
}
```

```tsx
// components/onboarding/Coachmark.tsx — a small floating pill
export function Coachmark({ anchor, text, onDismiss }: Props) {
  // Position absolutely near the anchor element via getBoundingClientRect.
  // Render a small amber-bordered tooltip with the text + ✕ button.
  // Auto-position to avoid covering the anchor.
  return (
    <div role="dialog" aria-label="Tip" className="coachmark">
      <span>{text}</span>
      <button onClick={onDismiss} aria-label="Dismiss">×</button>
    </div>
  );
}
```

---

## What this loop produced

- The canonical demo URL (`/?t=demo`) and its 7-tile composition.
- A 3-step coachmark storyboard that never blocks the underlying surface.
- An explicit "what we never ship in onboarding" list.
- A single success metric: 35% → 50% reach-country-page-in-60-seconds.
- Six referrer-specific banner variants.
- A separate post-signup configuration flow for accounts.
- A working coachmark trigger skeleton.

## What comes next

- **L122** — home screen layout candidates evaluate this composition.
- **L139** — onboarding flow (Phase 3 design) refines this storyboard.
- **L261** — onboarding flow prototype (Phase 5).

## Related

- [[L122-home-screen]] — home layout candidates evaluation
- [[L139-onboarding-flow]] — Phase 3 design surface
- [[L261-onboarding-flow-prototype]] — Phase 5 implementation
- [[L001-vision-statement]] — no-signup-wall commitment
- [[L101-globe-gl-3d-pattern]] — the globe is the demo's visual hook
