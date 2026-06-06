# L151 — Modal vs Inline Drilldown Rules

**Loop**: 151 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The rule, in one sentence

**Default to routing. Open a drawer when you need context. Open a modal only when you need confirmation.**

## The four drilldown patterns

| Pattern | URL changes? | Back-button works? | Use |
|---|---|---|---|
| **Inline expand** | No | n/a | Accordion-style detail row, in-place mini-chart upgrade |
| **Drawer** | Yes (hash) | Yes (back closes drawer) | Provenance, methodology preview, annotation, share menu |
| **Route (full page)** | Yes (path) | Yes | Country page → indicator page → forecast page |
| **Modal** | Maybe (query param) | Closes modal | Irreversible action confirmation, lightweight form |

## The decision tree

```
   User clicks a data point. What now?
   │
   ├── Is the user reading deeper into the same object?
   │       ├── In place is fine?         → Inline expand
   │       └── Needs more vertical room? → Drawer
   │
   ├── Is the user navigating to a related but distinct object?
   │       → Route (new page)
   │
   └── Is the user about to do something destructive or commit a choice?
           → Modal
```

## Bright lines

### Always route, never modal:

- "Compare 2" — has its own URL: `/compare?a=DEU.cpi&b=FRA.cpi`
- "See full methodology" — `/methodology/<scenario-pack>`
- "Open in notebook" — `/export/notebook/<view-id>`
- "Forecast leaderboard" — `/leaderboard`
- "Pricing" — `/pricing`
- Any page a user might want to bookmark, share, paste into a Substack, or screenshot for context.

If a user wants to send the link to a colleague, it has to be a route.

### Always drawer, never modal:

- Provenance (L132)
- Vintage time-machine (L173) — drawer with the date picker; route changes when the user commits
- Annotation editor (L156) — drawer with the drawing tools
- Cite-this-view (L158) — drawer with copy-to-clipboard variants
- Share menu (L155)
- Watchlist add/edit
- Filter panel (e.g., "show only G7")

Why a drawer and not a modal: drawers don't trap the eye. The chart stays visible behind. The user can reference the data while editing. Modals are jail.

### Always modal, never drawer:

- Confirm deletion of a saved view
- Confirm deletion of an alert
- Confirm "open paid checkout flow" (Stripe takes over after this)
- Sign-in step on a gated action
- Irreversible export ("this will email a 2GB CSV")

Modals are a hammer for "are you sure?" That's their only job.

### Sometimes modal, sometimes route:

- Sign-in/sign-up: route if part of onboarding flow (L139); modal if triggered by a "save this view" mid-task. The deciding question: was the user intending to log in, or were they intending to do X and login is a side-quest? If side-quest → modal so we can return them. If intent → route so they can bookmark.

## Why we avoid modals

1. **Modals hide context.** The user came to look at data; modal removes the data.
2. **Modals don't deep-link.** You can't paste a "URL with modal open" into Slack and have it open the modal.
3. **Modals trap focus.** Aggressive focus management feels carceral on touch.
4. **Modals stack badly.** Modal-over-modal is a confession that someone designed the wrong primitive.
5. **Mobile modals are sheets.** And sheets are drawers from the bottom. So just call it a drawer from day one.

Result: OPENGEM has ~6 modals total, all of them confirmation/auth, never UI-rich.

## Inline expand specifics

A row in a data table can expand inline to show a sparkline → mini-chart, or a table cell can show 3 nested cells. Use cases:
- Indicator row reveals a 30-day sparkline below the value
- Country row reveals the most-recent surprise scores
- Forecast row reveals diff-vs-WEO

Animation: 200ms ease-out height transition. No backgrounds change.

Constraint: an inline expand may not contain interactive controls that would re-expand or fetch additional layers. Stop nesting at depth 1. If you need depth 2, it's a route.

## Drawer-vs-route — the "context" test

The deciding question: **does the user need the previous page visible behind?**

- Yes → drawer. ("I want to see the chart while reading the methodology.")
- No → route. ("I'm going to the leaderboard. I don't need the previous chart.")

When in doubt, prefer route. Routes are more shareable, more SEO-friendly, and more aligned with OPENGEM's "everything is deep-linkable" thesis (L154).

## Drawer URL contract

Drawers update the URL hash:

```
/country/USA?indicator=CPI&vintage=2026-06-04#drawer=provenance
```

Closing the drawer removes `#drawer=...`. Refreshing the URL re-opens the drawer (so a shared URL with `#drawer=provenance` lands the user inside that drawer). Browser back-button closes the drawer (history entry).

## Modal URL contract

Modals do NOT update the URL by default — they are ephemeral. Exception: a "confirm checkout" modal during onboarding uses `?confirm=checkout` so that if the user refreshes mid-modal, they don't lose the step.

## Route transitions

Use Next.js' soft navigation for drilldown routes (country → indicator). The shell (top nav, sidebar) does not re-render. The body fades in over 100ms.

If the drilldown changes the shell (e.g., entering full-screen forecast view), use a hard navigation with a route group `(focus)` that swaps the shell layout.

## The "back button must work" rule

Every drilldown must respect browser back:
- Route → previous route restored.
- Drawer → drawer closes, chart restored.
- Inline expand → the row collapses.
- Modal → modal dismissed, no state change.

If any of these break the back button, redesign.

## Modal anatomy (the six we have)

```
   ┌──────────────────────────────────────────┐
   │  ✕  Delete saved view?                   │
   │  ───────────────────────────────────────  │
   │                                           │
   │  This will permanently remove             │
   │  "G7 CPI watchlist (May 2026)."           │
   │                                           │
   │  ┌──────────────────────────────────┐    │
   │  │  ☐ Don't ask again for this type │    │
   │  └──────────────────────────────────┘    │
   │                                           │
   │  ─────────────────────────────────────    │
   │              [ Cancel ]  [ Delete ]      │
   └──────────────────────────────────────────┘
      width: 420px (max)
      centered, dimmer-overlay behind
```

- Cancel always on the left, primary action on the right.
- Destructive primary action uses `bg-bad-500` (vermilion).
- Esc dismisses (cancels).
- Click outside dismisses (cancels).
- Tab order: heading → body → checkbox → cancel → primary.
- ARIA: `role="alertdialog"`, `aria-labelledby` heading, `aria-describedby` body.

## Implementation

- Routes: Next.js App Router
- Drawers: Radix Dialog with `data-side="right"` and a custom slide-in animation
- Modals: Radix AlertDialog
- Inline expand: native CSS grid with animated grid-row-height (no JS height calculation)

## The "small but loud" anti-pattern

Some teams use a modal to "be sure the user sees this." This is wrong. If the message matters, it's a banner, a toast, or a route landing-state. A modal that exists to be noticed is harassment.

OPENGEM's six modals are all "user just took action X, confirm it." Nothing else.
