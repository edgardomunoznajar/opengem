# L150 — Tooltip / Overlay Patterns

**Loop**: 150 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The four overlay tiers, decided

| Tier | Trigger | Dismiss | Body width | Persists across page | Stacks? |
|---|---|---|---|---|---|
| **Hint** | hover ≥250ms | mouseleave / scroll | ≤200px | no | no |
| **Tooltip** | hover ≥150ms OR focus | mouseleave / esc | ≤320px | no | no |
| **Popover** | click | click outside / esc | ≤480px | no | yes (1 deep) |
| **Drawer** | click | close button / esc / route-change | full vertical, 480px wide | yes | no |

Anything more elaborate than a drawer is a route. See L151 for modal vs route decisions.

---

## Hint

Use for: keyboard-shortcut labels on icons, "you can click this" affordance reveals, definitions of jargon in axis labels.

Visual:
```
   ┌────────────────────┐
   │  Source: FRED       │
   └────────▼───────────┘
```
- bg: `bg-elevated`
- border: 1px `border-subtle`
- text: `text-xs` `text-secondary`
- padding: 4px 8px
- shadow: none
- max-width: 200px
- delay: 250ms in, 0ms out
- offset from element: 6px
- always single-line; if multi-line is needed, it's a Tooltip not a Hint.

Implementation: Radix UI `<Tooltip>` primitive with our `Hint` wrapper.

## Tooltip

Use for: chart data-point hovers, glossary terms (L171), badge value disambiguation, button helper text.

Visual:
```
   ┌──────────────────────────────────┐
   │  Inflation, Y/Y                  │
   │  3.4%  (▲ +0.4pp vs prev)        │
   │  ─────────────────────────────   │
   │  Source: FRED CPIAUCSL           │
   │  As of 2026-05-30                │
   └────────────▼─────────────────────┘
```
- bg: `bg-elevated`
- border: 1px `border-default`
- text: `text-sm`
- padding: 8px 12px
- shadow: subtle
- max-width: 320px
- delay: 150ms in, 100ms out (grace period for moving cursor between adjacent points)
- offset: 8px

Required content for any data-point tooltip:
1. Indicator name
2. Value (tabular nums)
3. Diff vs previous obs (badge inline)
4. Source attribution
5. As-of date / vintage

Tooltips render via React portal to avoid clipping. Position via Floating-UI: prefer top, then right, then bottom, then left.

## Popover

Use for: methodology pop-up (L172), share menu, vintage selector micro-UI, watchlist add, filter mini-panel.

Visual:
```
   ┌──────────────────────────────────────────┐
   │  Methodology: NY Fed-style DFM           │
   │  ───────────────────────────────────────  │
   │                                           │
   │  This forecast uses a dynamic factor      │
   │  model on 24 monthly indicators...        │
   │                                           │
   │  [ See full methodology → ]               │
   │                                           │
   │  Last refreshed: 2026-06-04 14:30 UTC     │
   └───────────────▼──────────────────────────┘
```

- bg: `bg-elevated`
- border: 1px `border-default`
- shadow: medium
- padding: 16px 20px
- max-width: 480px
- close button: top-right `x` (24px hit-target)
- has heading row, body, optional footer with one CTA

A popover MUST have at least one navigable interactive element. If it only displays text, it's a tooltip.

Click outside or `Esc` to dismiss. Tabbing out also dismisses (focus management — Radix Popover handles).

**Popover stacking**: only one popover open at a time. Clicking a trigger when another popover is open closes the first. There is no nested popover behavior; if you need that, it's a drawer.

## Drawer

Use for: provenance / vintage drawer (L132), annotation editor (L156), full methodology view (L172 has both the popover preview and the drawer expansion), cite-this-view (L158), filter panel, advanced settings.

Visual:
```
   ┌────────────────────────────┐
   │  ✕  Provenance              │
   │  ───────────────────────────  │
   │                             │
   │  Vintage: 2026-06-04         │
   │  Model: combiner v4.2        │
   │  ...                         │
   │                             │
   │  [Download manifest]         │
   │                             │
   └────────────────────────────┘
       width: 480px (desktop)
       full-width on mobile
       slides in from right
```

- bg: `bg-surface`
- border-left: 1px `border-default`
- shadow: heavy
- close: top-left `x` (not top-right — left because it's near the slide-out edge)
- a drawer has a heading row, scrollable body, sticky footer with primary action
- Esc dismisses
- Clicking outside dismisses ONLY IF no unsaved state; otherwise asks for confirmation
- A drawer is reflected in the URL hash (`#drawer=provenance`) so it deep-links

A drawer can host its own tooltips and popovers (children of the drawer follow the rules).

---

## Hover, click, persistent — the three behaviors

| Behavior | Maps to | Used for |
|---|---|---|
| **Hover** | Hint, Tooltip | Read-only inspection |
| **Click** | Popover, Drawer | Interaction or extended reading |
| **Persistent** | Drawer | Multi-step workflows or comparison reference |

The rule: **if the user needs to read it twice, it's not a tooltip.** Tooltips are for the cursor-passing-through moment. Popovers and drawers are for "let me actually look at this."

Persistent reasoning: the drawer is the only overlay that survives a chart click on the underlying canvas. Everything else dismisses on outside-click.

## Mobile / touch

- Hint: absent (no hover). The Hint content moves to a long-press tooltip.
- Tooltip: triggered by tap. Dismissed by tapping outside.
- Popover: identical to desktop.
- Drawer: slides from bottom (sheet pattern), not right.

Long-press tooltip on touch screens shows after 500ms. Vibrates 10ms to confirm. The tooltip persists until tapped-away.

## Accessibility

- All triggers have `aria-describedby` linking to the tooltip body for screen readers.
- All popovers and drawers trap focus.
- All overlays close on `Esc`.
- All overlays announce open/close to assistive tech via Radix's built-in roles.
- Tooltips never contain only icon content — the trigger element itself carries the semantic text.

## Performance budget

- Tooltips must mount in <8ms. No data fetching on tooltip — preload at component render or lazy-fetch with placeholder skeleton.
- Popovers may fetch on open (<300ms typical, show skeleton beyond 150ms).
- Drawers may fetch on open; show skeleton if >100ms; show progress if >500ms.

## Position resolution

Use Floating-UI's `computePosition` for all overlays. Try-order:
1. `bottom-start` for popovers attached to header items
2. `top` for tooltips on chart points
3. `right` for sidebar items
4. Fallback through the cardinal directions

If no position fits the viewport, switch to a bottom sheet on mobile sizes or modal-style centered on desktop.

## The "no surprise" rule

Overlays must never appear without user intent. No "tooltip after a 2-second pause," no "guided tour pop-up on first visit" (that's an onboarding pattern, handled in L139), no notifications that look like tooltips. The user always took an action (hover, click, focus) immediately before the overlay appeared.

## What's NOT an overlay

- Inline expansion (accordion): part of layout, not overlay.
- Toast notifications: handled separately (page-level stack, dismissable, see L141 for error toasts).
- Modal dialogs: avoided — see L151. Only for irreversible confirmations.
- Banner alerts (e.g., "stale data"): part of layout, sticks to top of section.

---

## Library

Stack:
- Radix UI primitives (`Tooltip`, `Popover`, `Dialog` for drawer)
- Floating-UI for position math (Radix uses it internally)
- Framer Motion for the slide-in animation on drawers (200ms ease-out)
- All wrapped in OPENGEM-styled components: `<Hint>`, `<Tooltip>`, `<Popover>`, `<Drawer>`

No third-party "tooltip libraries" beyond Radix. We control the visual contract.
