# L155 — Sharing UX

**Loop**: 155 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The thesis

OPENGEM is a publishing engine disguised as a dashboard. Every view should be shareable in the format most native to where it's going. We don't make users figure out the right format — we pick for them based on page type.

## The four share formats

| Format | Best for | Bandwidth | Persistence |
|---|---|---|---|
| **Link (URL)** | Twitter, Slack, Substack body, email | Tiny | Live (resolves current data) |
| **PNG** | Reddit, Discord, presentation slides, news article | Medium | Snapshot (frozen) |
| **GIF (or animated WebP)** | Twitter video, blog hero, demonstration of revision | Larger | Snapshot sequence |
| **oEmbed** | Substack, Notion, WordPress, Medium | Live | Live (re-renders) |

## The primary per page type

| Page type | Primary share | Secondary | Tertiary |
|---|---|---|---|
| Country page | Link | PNG | oEmbed |
| Indicator page | oEmbed | Link | PNG |
| Scenario page | Link | PNG | (no GIF — too complex) |
| Forecast page | PNG | Link | oEmbed |
| Forecast diff (vintage-over-vintage) | **GIF** | PNG | Link |
| Leaderboard | Link | PNG of top-10 | — |
| Accountability ledger entry | Link | PNG | — |
| News / event | Link | (none) | — |
| Compare-2 | PNG | Link | oEmbed |
| Watchlist view | Link (private) | — | — |

Reasoning per page type below.

### Country page → Link primary

A country page is a dashboard tour. Users share it for the URL, knowing the reader will explore. PNG is secondary for "I want to point at the latest CPI print."

### Indicator page → oEmbed primary

An indicator page is the answer to "what is inflation in country X right now." It belongs embedded in a Substack post. The embedded chart updates daily. oEmbed wins.

### Scenario page → Link primary

Scenarios are narrative-heavy. The link delivers the full experience. PNG of the scenario tree is the secondary — useful in slide decks. No GIF — scenario trees don't animate well.

### Forecast page → PNG primary

A forecast snapshot is a statement made at a moment. PNG with the vintage stamp burned in is the share-format. Link is secondary (the live view updates, which is sometimes not what the sharer intends).

### Forecast diff → GIF primary

"How my recession-prob forecast has evolved over the last 12 weeks" is a story. Animation tells it. GIF of 12 frames at 1.5s each, looping, with the vintage date burning in each frame.

This is the format Bloomberg can't replicate (their charts are static). It's an asymmetric weapon.

### Leaderboard → Link primary

Live scoreboard. Sharing a frozen PNG misrepresents the standings. Live link only.

## Share menu UX

Triggered by `mod + shift + l` (copy link), the share icon button in the toolbar, or the command palette ("share").

Renders as a popover:

```
   ┌──────────────────────────────────┐
   │  Share this view                 │
   │  ──────────────────────────────  │
   │                                  │
   │  Recommended: Copy link          │
   │                                  │
   │  ┌────────────────────────────┐ │
   │  │ https://opengem.app/...    │ │
   │  └────────────────────────────┘ │
   │  [ Copy ]                        │
   │                                  │
   │  Other formats:                  │
   │   • Save as PNG                  │
   │   • Embed code (oEmbed)          │
   │   • Animated diff (GIF)          │
   │   • Cite this view  →            │
   │   • Open in notebook  →          │
   │                                  │
   │  Audience:                       │
   │   ◉ Public (default)             │
   │   ○ Unlisted (share-token)       │
   │                                  │
   └──────────────────────────────────┘
```

- The primary format is highlighted for the current page type.
- Other formats are one click away.
- "Audience" lets the user choose between a vanilla URL (public, indexed) and a share-token URL (unlisted — works but won't appear in search).

## Image generation

PNG and GIF are server-rendered:

- Endpoint: `GET /share/png?path=<encoded-url>&w=1200&h=630`
- Returns PNG (OG-image dimensions by default; configurable).
- Implementation: Vercel `@vercel/og` or Satori for the lightweight path; for charts requiring full Recharts/D3, Playwright Worker rendering a hidden Chrome instance.
- Caching: keyed on canonical URL + vintage. TTL = until the next vintage. Then regenerated lazily.

For GIF:
- Endpoint: `GET /share/gif?path=<encoded-url>&frames=<N>&interval=<ms>`
- N frames at the N most-recent vintages.
- Server stitches PNG frames into a GIF via `ffmpeg`.
- Cached aggressively. TTL = same as data vintage.

Image specs:
- PNG default: 1200×630 (Twitter card / OG image).
- PNG alternative: 1920×1080 (high-resolution).
- GIF: 800×450 at 2 frames/sec, max 30 frames.

All images carry:
- OPENGEM logotype in bottom-right
- "As of <date>" stamp
- Source attribution

## oEmbed

OPENGEM is an oEmbed provider. Endpoint:

```
GET /oembed?url=https://opengem.app/indicator/cpi-yoy&maxwidth=600&format=json
```

Returns:

```json
{
  "version": "1.0",
  "type": "rich",
  "provider_name": "OPENGEM",
  "provider_url": "https://opengem.app",
  "title": "US CPI YoY — OPENGEM",
  "html": "<iframe src='https://opengem.app/indicator/cpi-yoy?embed=1' width='600' height='400' allowtransparency></iframe>",
  "width": 600,
  "height": 400
}
```

Discovery: every page has

```html
<link rel="alternate" type="application/json+oembed" href="https://opengem.app/oembed?url=...">
```

Substack, Medium, Notion, WordPress all autoload via this discovery link.

## Embed iframe

The `?embed=1` route serves a stripped-down version:
- No nav
- No footer
- 16:9 default aspect
- Vintage stamp visible
- Bottom-right: "via OPENGEM" link
- Light + dark mode auto-detect via `prefers-color-scheme`
- Sandboxed: no JS from parent, no cross-origin reads
- Mobile-responsive

Embed retains keyboard nav inside its sandbox. Click → opens full view in new tab.

## Open Graph & Twitter cards

Every page emits:

```html
<meta property="og:type" content="article">
<meta property="og:title" content="…">
<meta property="og:description" content="…">
<meta property="og:image" content="/share/png?path=…">
<meta property="og:url" content="https://opengem.app/…">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="/share/png?path=…">
```

OG image generation is on-demand, cached. The image generator picks the right view: country page → top-3 KPIs; indicator page → the chart; forecast → chart with vintage stamp.

## Share-token (unlisted)

For a privately-shared annotated view:
- User clicks "Share → Unlisted"
- We persist the view object (URL + annotations + watchlist state) keyed by a base32 nanoid
- Token URL: `https://opengem.app/v/b7k2m9pq3x`
- These URLs do NOT appear in sitemaps, do NOT have OG images, do NOT get indexed
- Resolve to the canonical URL but with annotation layer attached

Tokens are unguessable but not access-controlled — anyone with the URL can view. If the user wants real privacy, they save to their watchlist (login required).

## Copy-paste delight

When the user clicks "Copy link," we:
1. Copy the URL to clipboard
2. Show a toast: "Link copied. Includes vintage 2026-06-04."
3. If the user navigates away within 10s, persist the toast across nav so they see the confirmation.

Small, but signals competence.

## Anti-patterns

- No share buttons for "Facebook" / "LinkedIn" / "Pinterest" by default. Users who want those use OS share APIs (which we expose via `navigator.share` on supporting platforms).
- No tracking parameters appended to copied URLs. We rely on canonical URLs + Plausible event capture on visit.
- No QR codes by default. Available as a "more" option for conference-deck users.

## Telemetry

We track:
- Format used (link / png / gif / oembed / qr)
- Page type at time of share
- Whether the share included a vintage param or used the latest

This feeds back into the per-page-type primary mapping above. If oEmbed for indicator pages turns out to be rare, we promote PNG.

## What we will build later

- "Share as tweet" with pre-composed text (V2)
- Substack auto-embed integration via API (V2, see L112)
- Slack unfurl (V2 — Slack hits the OG endpoint for now)
- Discord embed bot (V2)
- Custom watermarks for paid tier (V2 — white-label tearsheets)
