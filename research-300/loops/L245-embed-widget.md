# L245 — Embed widget prototype (3 sizes)

**Loop**: 245 / 300
**Phase**: 5 — Code prototypes
**Date**: 2026-06-06
**Artifact**: `prototypes/dashboard-next/public/embed.js` + `app/embed/page.tsx`

---

## What was built

A zero-dependency vanilla JS embed SDK (`public/embed.js`) plus an `/embed` documentation page showing the three canonical sizes (square 200×200, banner 600×120, tall 300×420).

## Why this matters

The embed is the **distribution multiplier**. Every macro blogger, every YouTuber's video description, every Substack post that drops an OPENGEM tile becomes a one-way attribution link back to OPENGEM. The "vintage badge stays" + "OPENGEM link stays" clauses are not legalese — they are the deal in exchange for the data being free.

## The deal (the embed contract)

```
You get: Up-to-date data, vintage-stamped, free, Apache-2.0 SDK.
We get:  Vintage badge stays. Brand link stays. Numbers match API at fetch time.
Pro:     White-label option lifts the brand-link constraint ($/month).
```

This is OurWorldInData's playbook, applied to macro. OWID's grafiken embeds appear in thousands of blogs, papers, and news pieces, and every one is a discovery vector. OPENGEM does the same — but with forecasts and machine-checkable vintages, not just static charts.

## SDK architecture

- Single file, single IIFE, zero dependencies. ~3 KB minified.
- Auto-mounts on DOMContentLoaded by looking for `[data-opengem]` elements.
- Renders a self-contained `<div>` with inline styles (no CSS leakage into host page).
- Fetches `/v1/{recession-probability|gpr-nowcast|forecasts}` based on `data-kind`.
- Renders sparkline inline via SVG (no canvas, no chart lib dep).
- Falls back to "—" if API unreachable (no broken layouts).
- Exposes `window.OPENGEM.mount(node)` for programmatic remount.

## Customization API (host can set)

| Data attribute | Values | Default |
|---|---|---|
| `data-kind` | `recession_prob`, `gpr_nowcast`, `forecast` | `forecast` |
| `data-country` | ISO-3 | `USA` |
| `data-indicator` | `gdp_yoy`, `cpi_yoy`, … | `gdp_yoy` |
| `data-size` | `square`, `banner`, `tall` | `square` |
| `data-theme` | (Pro) `light`, `dark`, custom | `dark` |

## Production readiness checklist

- [ ] Tag-level CSP-safe inline styles (no inline JS execution)
- [ ] Subresource Integrity hash published in docs
- [ ] CDN: Cloudflare R2 + Workers cache
- [ ] Versioned URL: `/embed/v1.js` so we can roll forward without breaking existing embeds
- [ ] Click-through analytics (privacy-preserving — pixel + IP-prefix hash)
- [ ] Open-graph cards for Twitter/X (server-side rendered tile screenshots)

## What this loop produced

- Working `public/embed.js` with 3 size renderers
- Documentation page at `/embed` with copy-paste snippets
- The embed contract (the deal) written out

## What comes next

- L247 — RSS / Atom feed generator (companion distribution mechanism)
- L248 — JSON-LD injection for SEO (companion)
- L155 — Sharing UX: gif / png / link / oembed (the manual share path)

## Related

- [[L144-embed-widget-design]] — the spec this implements
- [[L007-distribution-thesis]] — embeds are tactic 1 of 6
- [[L138-pricing-page]] — Pro embed is a paid SKU
- [[L008-differentiation]] — vintage badge is the editorial signature
