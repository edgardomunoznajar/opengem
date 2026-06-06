---
loop: 144
phase: 3
title: Embed Widget Design — 3 Sizes
date: 2026-06-06
status: decided
---

# L144 — Embed Widget Design

**Loop**: 144 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The brief

Design 3 embed widget sizes (square, banner, tall). Spec the JS embed contract.

Embeds are OPENGEM's distribution superpower. The YouTuber pastes one line into Substack. The journalist pastes one line into a story. The NGO drops it into a research site. Every paste is a backlink, a credibility carrier, and a free SEO instrument.

The embed must:
- Load in <500ms on a cold cache.
- Render correctly inside iframe-blocking widget frameworks (Substack, Medium, Notion).
- Carry the OPENGEM brand consistently (no unbranded embeds).
- Update without manual refresh (latest vintage).
- Carry a stable URL to "open full view on OPENGEM."

## The three sizes

### Size 1 — Square (400 × 400 px)

The square is for sidebar placements, Substack mid-article, Twitter cards.

```
+----------------------------+
| OPENGEM 🌐  CPI YoY · US     |
+----------------------------+
|                            |
|  2.9% ▼0.2pp m/m            |
|                            |
|  ┌─ sparkline 12m ──┐      |
|  │  ▁▂▃▅▄▃▂▁▁▂▃▄▅   │      |
|  └────────────────────┘      |
|                            |
|  Forecast 4Q ahead:        |
|    P50  2.4%                |
|    band 1.4-3.5%            |
|                            |
|  Calibration                |
|    CRPS 0.84 (vs WEO 0.91) |
|                            |
+----------------------------+
| 2026-06-02 · opengem.world  |
+----------------------------+
```

Content includes:
- Header band: brand + record name.
- Big number with sparkline.
- Forecast P50 + band.
- Track-record line (CRPS comparison).
- Footer: vintage stamp + clickable URL.

The whole widget is clickable to the corresponding record page.

### Size 2 — Banner (728 × 240 px)

The banner is for top-of-article, hero, header strip. Wider than tall, designed for editorial placement.

```
+----------------------------------------------------------------+
| OPENGEM 🌐 · United States · CPI YoY                            |
+----------------------------------------------------------------+
|                                                                |
| 2.9%      ┌─ 12m sparkline ──────────┐    Forecast 4Q ahead  |
| YoY        │  ▁▂▃▅▄▃▂▁▁▂▃▄▅          │    P50    2.4%        |
| ▼0.2pp m/m │                          │    P10-90 1.4 - 3.5    |
| Vintage    │                          │    Cons.   2.8 (-0.4)  |
| 2026-06-02 └────────────────────────────┘    CRPS 0.84 / 0.91  |
|                                                                |
+----------------------------------------------------------------+
| Powered by OPENGEM · opengem.world/i/cpi-yoy/USA · CC-BY-4.0   |
+----------------------------------------------------------------+
```

Content in three columns:
- Left: big number + delta + vintage.
- Center: 12-month sparkline + forecast band (extends right of sparkline).
- Right: forecast P50, P10-P90, consensus delta, CRPS.

Clickable to the record page.

### Size 3 — Tall (300 × 600 px)

The tall is for sidebars, vertical placements, mobile-friendly insertion.

```
+----------------------------+
| OPENGEM 🌐  US · CPI YoY    |
+----------------------------+
|                            |
| 2.9% ▼ m/m                  |
| Vintage 2026-06-02          |
|                            |
| ┌─ Chart 12m + 4Q ──┐      |
| │                    │      |
| │  ▁▂▃▅▄▃▂▁ ╲~~~     │      |
| │            ─P50    │      |
| │           ▁P10-90  │      |
| │                    │      |
| └────────────────────┘      |
|                            |
| FORECAST 4Q                 |
|   P50    2.4                |
|   band   1.4 — 3.5          |
|                            |
| CONSENSUS                   |
|   WEO    2.8 (-0.4)         |
|   OECD   2.7 (-0.3)         |
|   FRB    2.6 (==)           |
|                            |
| TRACK RECORD                |
|   CRPS   0.84 (vs WEO 0.91)|
|   PIT    0.78 (pass)        |
|   Bias  -0.04               |
|                            |
| SCENARIOS AFFECTING         |
|   Trade-LATAM    P=0.62     |
|   Red-Sea-#4     P=0.78     |
|                            |
+----------------------------+
| 2026-06-02 · CC-BY-4.0      |
| opengem.world/i/cpi-yoy/USA |
+----------------------------+
```

Tall includes more depth: chart + forecast detail + consensus + track record + scenarios. It is the most editorial-rich variant.

## The JS embed contract

Embeds load via a single script tag plus a target div:

```html
<div id="opengem-embed" data-kind="indicator" data-id="cpi-yoy/USA"
     data-size="banner" data-theme="orange"></div>
<script src="https://cdn.opengem.world/embed/v1.js" defer></script>
```

The script reads:
- `data-kind`: one of `country`, `indicator`, `scenario`, `forecast`, `ledger-cell`.
- `data-id`: the slash-separated record ID.
- `data-size`: `square`, `banner`, or `tall`.
- `data-theme`: `orange` (default), `pink`, `blue` — per L145.
- `data-vintage` (optional): pin to a specific vintage.
- `data-locale` (optional): `en` default; `es`, `fr`, `de`, `ja`, `zh` for Block II+.

The script:
1. Detects all `#opengem-embed` divs on the page.
2. Constructs the iframe URL: `https://opengem.world/embed/{kind}/{size}?id={id}&theme={theme}&vintage={vintage}`.
3. Injects the iframe sized to the requested dimensions.
4. Sets `loading="lazy"` and `sandbox="allow-scripts allow-same-origin allow-popups"`.

The iframe is the rendered widget. The host page does not need anything beyond the script tag.

### Why iframe (and not direct DOM injection)

- **Style isolation.** OPENGEM's CSS does not leak into the host page; the host's CSS does not break the widget.
- **Update independence.** When OPENGEM ships a new widget version, all live embeds inherit the update without host action.
- **Trust isolation.** The widget renders as a sandboxed third-party context; no risk of cookie or fingerprint leakage.
- **Embedded analytics.** OPENGEM can count widget views without injecting tracking into the host.

The trade-off is that the widget cannot inherit the host page's typography or color scheme. We accept this: OPENGEM-branded embeds are the brand promise.

## Static fallback

Some hosts (Substack, Medium, Notion) block iframes by default or only support oembed. For these, we provide a static-image fallback:

```html
<a href="https://opengem.world/i/cpi-yoy/USA">
  <img src="https://opengem.world/embed/img/indicator/banner/cpi-yoy_USA.png"
       alt="OPENGEM: US CPI YoY" width="728" height="240">
</a>
```

The static PNG is rendered server-side at the current vintage and is updated daily. Hosts that block iframes get the static image; the link target opens the live OPENGEM page.

The Substack workflow is the test case: paste one line, get an embed-quality static image automatically.

## oEmbed support

OPENGEM publishes an oEmbed endpoint:
- `https://opengem.world/oembed?url={record-url}&maxwidth=...&maxheight=...`

Returns an oEmbed JSON response with rich embedding details. Substack, Twitter, WordPress, and oEmbed-aware platforms can call this endpoint to render embeds automatically when a user pastes an OPENGEM URL.

## Widget builder UI

`/embed/builder` is a small tool where a user can:
1. Pick a record (country, indicator, scenario, forecast, ledger cell).
2. Pick a size.
3. Pick a theme.
4. Pick a vintage (default: live).
5. Preview the embed.
6. Copy the embed code (JS, iframe-only, oEmbed link, static-image markdown).

The builder is the "give me a code snippet" UX. It is fast and copyable.

## Branding and white-label

- **Free tier embeds**: include OPENGEM wordmark and footer URL.
- **Pro tier**: same as free; embed quota raised to 1000 page-views per day per record.
- **Team tier (white-label)**: can hide OPENGEM wordmark, replace with their own. The bottom footer link still mentions "data: OPENGEM" in 8pt gray for attribution compliance with CC-BY-4.0.

## Vintage pinning

By default, embeds render the *latest* vintage of the record. A pinned-vintage embed (via `data-vintage`) renders that specific vintage forever — useful for citing a forecast at a specific moment in a published piece.

Pinned-vintage embeds get a "vintage 2026-06-02" stamp in the footer that does not auto-update.

## Update cadence

Live embeds update:
- On page load (cache-busted via a per-vintage URL).
- Per record vintage cadence (daily for most indicators, intra-day for events).

The widget script has a small `data-refresh-on-interval` flag (default: false) — if true, the widget polls every 5 minutes and re-renders on a new vintage. Off by default to avoid wasted bandwidth.

## Performance

The script bundle is ≤8KB gzipped. The iframe payload (HTML + CSS + chart libraries) is ≤45KB gzipped. First Contentful Paint for the embed: <300ms after the iframe loads.

Charts inside embeds use Lightweight Charts (≤45KB) — small, fast, sharp. No Plotly. No D3 modules. The chart subset rendered inside embeds is a minimal sparkline + band fan.

## Analytics

OPENGEM collects per-embed view counts (anonymously) for product analytics:
- Total embed loads.
- Per-record popularity.
- Per-host-domain popularity (only if PostMessage announces it — opt-in by the host).

No cookies. No user identifiers. The widget honors Do Not Track.

## What this loop produced

- Three embed sizes: square (400x400), banner (728x240), tall (300x600).
- JS embed contract: single script + data-attribute div.
- Iframe-based rendering for style/trust isolation.
- Static-image fallback for iframe-blocked hosts.
- oEmbed endpoint for platform auto-embedding.
- /embed/builder UI for code generation.
- Free tier embeds branded; Team tier white-label with attribution preserved.
- Vintage pinning supported.
- Default live (auto-update on load); optional 5-minute polling.
- Script bundle ≤8KB; iframe payload ≤45KB; FCP <300ms.
- Anonymous per-embed analytics with no cookies.

## What comes next

- **L111** integrates: embeddable widgets (iframe + script SDK).
- **L245** prototypes the 3-size embed widget.
- **L155** designs the sharing UX (oEmbed is one share path).

## Related

- [[L121-information-architecture]] — /embed URL space
- [[L132-provenance-drawer]] — vintage stamp from drawer
- [[L138-pricing-page]] — Team tier white-label
- [[L142-mobile-information-density]] — tall embed works well in mobile-portrait contexts
- [[L145-dashboard-themes]] — theme parameter
- [[L155-sharing-ux]] — oEmbed is one share path
- [[L245-embed-widget-prototype]] — code prototype
