# L156 — Annotation Layer

**Loop**: 156 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The thesis

Drawing on a chart is the single most "I'm a real analyst now" affordance OPENGEM can offer. Strategists do this on Bloomberg with PowerPoint shapes layered over screenshots. We bring it into the dashboard.

Annotations are first-class objects with their own URLs.

## The four annotation types

| Type | Looks like | Purpose |
|---|---|---|
| **Marker** | Vertical line + label at an x value | "Fed cut here" |
| **Region** | Shaded horizontal band over a date range | "Recession 2008–2009" |
| **Arrow** | Arrow from one (x,y) to another, with optional caption | "From here to here, fastest rise since the 70s" |
| **Text** | Free-floating annotation tied to (x,y) | "Note: methodology change in 2021" |

Four primitives, no more. We resisted "freehand pen" because it doesn't archive well and isn't legible at small sizes.

## The annotation editor

Triggered by:
- Toolbar pencil icon (L146 icon #43)
- Command palette → "Annotate"
- Keyboard shortcut: not assigned to keep the global map clean

Opens as a **drawer** (per L150 / L151) on the right side, with the chart still visible:

```
   ┌────────────────────────────────┐
   │  ✕  Annotate this view         │
   │  ──────────────────────────────  │
   │  Tools:                          │
   │   [Marker] [Region] [Arrow] [Text] │
   │                                  │
   │  Current annotation:             │
   │  ┌────────────────────────────┐  │
   │  │ Marker @ 2024-09-18        │  │
   │  │ Label: Fed cut 50bps        │  │
   │  │ Color: [info ▼]            │  │
   │  │ [Delete]                    │  │
   │  └────────────────────────────┘  │
   │                                  │
   │  All annotations on this view:   │
   │   • Marker · Fed cut 50bps       │
   │   • Region · COVID lockdown     │
   │   • Text · See methodology...    │
   │                                  │
   │  ───────────────────────────────  │
   │  Save & share         [Save]    │
   └────────────────────────────────┘
```

The chart remains live. Clicking on the chart while in the editor adds a primitive at that point. Esc exits the editor.

## Per-primitive UX

### Marker

- Click anywhere on x-axis → vertical line drops at that date
- Drag handle at top to reposition
- Label input appears
- Snap-to-data option: nearest known observation
- Color: pick from semantic (info, warn, good, bad, neutral)

### Region

- Click + drag horizontally → defines start/end of band
- Pre-defined bands available: NBER recession periods, official lockdown windows, BIS-defined crisis epochs
- Opacity locked at 12% so it doesn't bury the line

### Arrow

- Click for start point, click for end point
- Caption text input
- Style: straight, curved, or "angle" (right-angle elbow for connecting axes)
- Arrowhead: small filled triangle, matching label color

### Text

- Click anywhere to place
- Renders as a small text block with thin border
- Connects to nearest data point with a subtle leader line (toggle off)
- Max 120 characters per annotation — discipline

## Persistence model

Annotations are objects with this schema:

```json
{
  "id": "an-01j7k...",
  "view_url": "https://opengem.app/indicator/cpi-yoy?countries=usa",
  "vintage_pinned": "2026-06-04",
  "items": [
    {
      "type": "marker",
      "x": "2024-09-18",
      "label": "Fed cut 50bps",
      "color": "info"
    },
    {
      "type": "region",
      "x_start": "2020-02-15",
      "x_end": "2020-05-30",
      "label": "Lockdown",
      "color": "bad"
    }
  ],
  "author": "anon|<user-id>",
  "created_at": "2026-06-06T12:30:00Z",
  "title": "CPI under COVID and the September pivot",
  "description": "Free-text note"
}
```

Stored server-side keyed by ID. Anonymous users get a localStorage-backed draft; the server-persistence step requires login (free tier).

## URL contract

A view with annotations attached:

```
https://opengem.app/indicator/cpi-yoy?countries=usa&annotations=an-01j7k...
```

Or, for an anonymized share-token (L155):

```
https://opengem.app/v/b7k2m9pq3x
```

The share-token form is preferred when sharing — it's shorter and survives view-parameter changes.

Multiple annotation sets can be layered: `?annotations=an-...,an-...`. They render in order.

## Save & share flow

1. User finishes annotating.
2. Presses "Save & share" in the drawer.
3. Choose visibility:
   - **Anyone with the link** (default — share-token URL generated)
   - **Public catalog** (annotations appear in OPENGEM's public annotation index — opt-in, used by editorial contributors)
4. Optional: add title + description (encourages narrative).
5. URL is generated and copied.

A toast confirms: "Annotated view saved. Link in clipboard."

## Public annotation catalog (V2 feature mentioned for context)

V2 idea: a `/annotations` index where editorial contributors post insightful annotated views. Curated, not user-submitted slop. Powers the "Editorial picks of the week" section.

## Render contract

Annotations render as an SVG layer above the chart canvas, below the tooltip layer. They:
- Inherit theme (dark/light)
- Are responsive (rescale with the chart)
- Are interactive: click an annotation → tooltip with title/description/author
- Are accessible: each has `role="img"` and `aria-label`

## Edit / fork model

- An author can edit their own annotations.
- A viewer can "fork" any annotation: opens the editor pre-populated, save creates a new annotation ID.
- Forks track lineage: `forked_from: an-...`.

Like GitHub gists for charts.

## Vintage discipline

When an annotation is saved against a view at a specific vintage, the URL pins that vintage:

```
?vintage=2026-06-04&annotations=an-...
```

Otherwise, the data underneath the annotation could shift (e.g., GDP revision) and the user's commentary would become nonsensical. Default behavior: pin to the vintage at save-time. User can opt-out ("show on latest").

If unpinned and a future vintage breaks the annotation (e.g., the marker date is no longer in range), we render a degraded state: the annotation appears in the list with a "broken" warning, and the layer renders best-effort.

## Drawer-to-chart sync

Hovering an annotation in the drawer list highlights it on the chart. Clicking jumps to it (scroll into view). Drag handles on the chart update the values in the drawer in real time.

## Library

- Chart layer: D3 + custom SVG primitives. Recharts annotations are too rigid.
- Drag/drop: `@dnd-kit/core`.
- Editor state: Zustand store local to the editor scope.
- Persistence: API endpoint `POST /api/annotations` returning the ID.

## Limits

- 50 annotations per view max (sanity).
- 4 layers max combined (when stacking other users' annotations).
- 4MB JSON payload max per annotation set.

## Authentication

- Anonymous: localStorage draft only. Cannot share.
- Free tier: 100 saved annotations / month.
- Paid tier: unlimited + custom watermark on shared images + private annotation collections.

## What we will NOT build

- Real-time collaborative annotation (Google Docs-style). Too much complexity for the value. V3 maybe.
- Threaded comments on annotations. Tempting; ultimately becomes a moderation problem. V3.
- Anonymous public annotations. Always tied to an account to prevent spam. (Anonymous viewing fine.)
