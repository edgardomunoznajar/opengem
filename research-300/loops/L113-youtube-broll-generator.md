# L113 — YouTube B-Roll Generator from Forecast JSON: Static-Image / Animated-SVG Renderer for Video Creators

**Loop**: 113 / 300
**Phase**: 2 — Deep dive on top candidates
**Date**: 2026-06-06

---

## Thesis of this loop

L007 ranked YouTube embed as the **#1** ROI distribution channel for the volume cohort. The Damian persona (47k subscribers, daily videos, voracious chart-consumer) is the prototype. The L245 v1 embed handles the *web* surface; this loop handles the *video* surface — what we ship so that a macro YouTuber can drop OPENGEM data into a video edit without leaving their NLE (Final Cut, Premiere, Resolve, CapCut).

The mistake to avoid: thinking this is a "video player" problem. It is not. It is a *static asset* + *animated overlay asset* problem. A YouTuber's video editor accepts PNG, JPG, SVG, MOV with alpha, GIF, MP4. The format we ship determines whether OPENGEM can be a one-click drop-in or requires the creator to re-key the data into their tool of choice.

Verdict: **a `/broll` endpoint that accepts the same forecast/scenario/country query parameters as the dashboard and returns four asset families: (1) high-res still PNGs at 1080p/4K with broadcast-safe colors, (2) animated SVG overlays sized for lower-thirds, (3) MP4 with alpha channel for NLE compositing of chart-build-on animations, (4) Lottie JSON for After Effects users. The single underlying renderer (a server-side Satori + headless Chromium hybrid) drives all four. Every asset embeds the OPENGEM watermark — strippable only with a Studio-tier key.**

---

## The video creator's actual workflow

A typical YouTuber (Damian-class) producing a 12-minute macro explainer:

1. Writes a script outlining 5-7 charts.
2. For each chart, currently: opens Bloomberg/TradingEconomics/FRED in a browser, screenshots, drags into Premiere as a still, manually animates a Ken-Burns zoom on the screenshot, voices over.
3. Editing time per chart: ~10 minutes (find, screenshot, color-correct, animate).
4. Total chart-prep time: ~70 minutes per video.
5. Aesthetic ceiling: limited by screenshot quality and Ken-Burns animation.

The OPENGEM proposition: replace step 2 with "paste OPENGEM URL into NLE bin." Bring chart-prep time to ~5 minutes per video. Lift aesthetic ceiling because OPENGEM ships native broadcast-quality assets.

This is a 14x time savings per video. For a YouTuber doing 4 videos/week, that's 4 hours/week recovered. The willingness-to-pay for that time is meaningful — and even at $0 (free tier), the channel-traffic flywheel is enormous.

---

## Asset family 1: high-res still PNG

`GET /broll/still?kind=forecast&country=USA&indicator=cpi_yoy&theme=broadcast&w=3840&h=2160&format=png`

- 4K (3840×2160) by default; configurable down to 1080p (1920×1080) for legacy edits.
- Broadcast-safe color (NTSC/PAL gamut clamped — no super-saturated reds that vibrate on broadcast TV).
- Transparent background available via `bg=transparent` for overlay use.
- Watermark in lower-right corner, ~80px wide, 12% opacity by default. Stripped only with Studio-tier key + `data-key=`.
- Caption baked into image as native text using JetBrains Mono. Caption parameters: `caption`, `subcaption`, `vintage`.

Renderer: Satori + sharp. Satori turns React/JSX into SVG; sharp converts SVG to PNG at the requested resolution. The pipeline is the same as the L111 OG image generator, just at higher resolutions and broadcast color settings.

---

## Asset family 2: animated SVG overlay

`GET /broll/svg-animated?kind=forecast&country=USA&indicator=cpi_yoy&style=lower-third&duration=4s`

- SVG with embedded SMIL or CSS animation timeline.
- Three preset styles: `lower-third` (slides in from left, holds, slides out), `corner-card` (fades in, breathes, fades out), `full-screen-callout` (zooms in, holds, zooms out).
- Duration configurable 2s–10s.
- File size ~30-60KB depending on style.

NLE compatibility: SVG isn't universally accepted by NLEs (Premiere accepts via plugins, Final Cut doesn't natively). For NLEs that don't accept SVG, we serve the same animation as MP4-with-alpha or PNG sequence.

---

## Asset family 3: MP4 with alpha channel

`GET /broll/mp4-alpha?kind=forecast&country=USA&indicator=cpi_yoy&style=lower-third&duration=4s&fps=30&res=1080p`

- ProRes 4444 with alpha — the broadcast standard for compositing.
- Alternative: WebM with VP9 alpha for web-native edits.
- Renderer: server-side Puppeteer + chrome-headless-shell records the SVG animation at the requested fps, then ffmpeg muxes with the alpha channel.

Cost: this is the heaviest asset family — a 4-second 1080p ProRes file is ~80MB and takes ~3 seconds to render. We cap free-tier requests at 10 per day per IP; Studio tier gets 100/day; cached aggressively at edge.

For free tier, the *first* request renders synchronously; subsequent identical requests serve from cache. The cache hit rate at YouTube-channel scale should be high (a popular MP4 generated once and served thousands of times).

---

## Asset family 4: Lottie JSON for After Effects

`GET /broll/lottie?kind=forecast&country=USA&indicator=cpi_yoy&style=lower-third`

- Bodymovin-format JSON, ~10KB.
- Animator-friendly: After Effects users can edit timing, colors, fonts, layer composition after import.
- Renderer: a hand-built React-Lottie compiler that takes the same JSX as Satori and produces the Bodymovin structure.

Lottie is the most-powerful surface for advanced editors but the least common — maybe 15% of YouTube macro creators use After Effects. Worth shipping for the high-end users who *do* edit Lottie; not worth optimizing for everyone.

---

## The `/broll` discovery surface

A discovery page at `/broll` shows:

- Big "drop-in" demo: an animated GIF of the lower-third being dragged into Premiere with the OPENGEM URL.
- Three preset categories — Today's data, Most-shared, Custom — each with copy-paste URLs and file downloads.
- A "Generate from URL" tool: paste any OPENGEM chart URL, get back four download buttons (PNG / animated SVG / MP4-alpha / Lottie).
- A direct-publish flow for the YouTube partnership program (L007 tactic 1 of channel #3): partners' channels get a personalized broll page at `/broll/p/{slug}` with pre-rendered weekly assets.

---

## The watermark contract

Every asset includes the OPENGEM watermark in the lower-right corner. The watermark is:

- **80px wide on 1080p** (proportional on other resolutions).
- **12% opacity** — visible but not distracting.
- **The text "OPENGEM.ORG" + a tiny vintage badge** showing the data's vintage date.
- **Strippable only with a valid Studio-tier or higher API key**, passed as `data-key=...` query param.

This is the analog of the L111 embed brand-link contract. The watermark is the brand-recognition driver — viewers who see "OPENGEM.ORG" in 100 macro videos eventually wonder what it is, search, land on the dashboard.

Why not make the watermark stripper-by-default? Because the YouTube channel is paying us in attribution, not in money. If we strip the watermark for free, we get neither.

---

## Privacy and creator credit

The optional `?credit=Damian+Macro` param adds a "via Damian Macro" line under the OPENGEM watermark, in 50% opacity. This is the *creator credit* mechanism — a YouTuber building a recurring partnership with OPENGEM gets their channel name surfaced in the brand stack as a thank-you. Tiny detail; high signaling value to the partner.

---

## The YouTube content-engine partnership (L007 tactic 1)

L007 named 10 mid-tier macro YouTubers as the partnership cohort. Each one gets:

- A `/broll/p/{slug}` page with daily fresh assets — today's recession-prob, today's GPR, today's surprise index — auto-regenerated at 06:00 ET.
- A `/feeds/c/{their-country-of-focus}.rss` feed for their reading.
- An editorial credit on the OPENGEM blog (drives backlinks).
- A custom branded chart template — their channel logo in the watermark stack (creator credit, see above).
- A free Studio tier credit ($99/mo equivalent) for embed white-labeling on their own sites.

In return: commitment to use OPENGEM assets in at least one video per week with on-screen attribution.

This is *not* a paid sponsorship. It's a barter — assets-for-attribution. The asymmetry: an OPENGEM weekly asset costs us $0 to produce (we already generate it for the dashboard); the channel's 47k-subscriber attribution costs them ~0 effort (they were going to make the video anyway).

---

## Cost economics

The expensive operations are the MP4-with-alpha renders (~3 seconds CPU + ~80MB R2 storage per file). At free-tier scale (estimated 1000 MP4 generations/day after Y1 ramp), cost is ~$30/mo of Cloudflare Workers + R2. Cached files serve from edge at <50ms.

If a viral video drives 100k MP4 requests for one asset, the asset is cached at edge and serves all 100k from there — origin cost is ~$0 for the long tail.

---

## Next-step: the still PNG endpoint skeleton

```typescript
// app/broll/still/route.ts — Next.js Route Handler
import { ImageResponse } from "next/og";
import { fetchForecast } from "@/lib/forecast";

export const runtime = "edge";

export async function GET(request: Request) {
  const url = new URL(request.url);
  const country = url.searchParams.get("country") ?? "USA";
  const indicator = url.searchParams.get("indicator") ?? "cpi_yoy";
  const width = parseInt(url.searchParams.get("w") ?? "3840");
  const height = parseInt(url.searchParams.get("h") ?? "2160");
  const data = await fetchForecast({ country, indicator });
  const isWhiteLabel = verifyStudioKey(url.searchParams.get("key"));

  return new ImageResponse(
    (
      <div style={{ width, height, background: "#0a0a0b",
                    color: "#fafafa", padding: 120,
                    display: "flex", flexDirection: "column" }}>
        <div style={{ fontSize: 60, color: "#a1a1aa", textTransform: "uppercase" }}>
          {country} — {indicator}
        </div>
        <div style={{ fontSize: 240, color: "#f59e0b", fontFamily: "JetBrains Mono" }}>
          {data.point.toFixed(2)}%
        </div>
        <ChartBands data={data} width={width - 240} height={height - 600} />
        <div style={{ position: "absolute", bottom: 80, right: 80,
                      opacity: 0.12, fontSize: 36, display: isWhiteLabel ? "none" : "flex" }}>
          OPENGEM.ORG · vintage {data.vintage_id}
        </div>
      </div>
    ),
    { width, height, headers: { "Cache-Control": "public, max-age=86400, s-maxage=86400" } },
  );
}
```

---

## What this loop produced

- A four-asset-family spec: still PNG, animated SVG, MP4-alpha, Lottie.
- The `/broll` discovery surface and the per-partner `/broll/p/{slug}` pages.
- The watermark contract — strippable only with Studio-tier key.
- The 10-partner YouTube content-engine partnership structure.
- A still-PNG endpoint skeleton using next/og.
- Cost economics showing free-tier viability at ~$30/mo.

## What comes next

- **L295** — YouTube content engine plan at scale (Phase 6).
- **L246** — print-tearsheet prototype reuses the still-PNG renderer.
- **L116** — print-grade SVG tearsheets share the same renderer pipeline.

## Related

- [[L007-distribution-thesis]] — YouTube is channel #1 for volume cohort
- [[L111-embed-widgets-v2]] — shared OG image generator pipeline
- [[L116-print-grade-svg-tearsheets]] — same renderer for print
- [[L295-youtube-content-engine]] — Phase 6 execution plan
- [[L101-globe-gl-3d-pattern]] — the pulse globe is one of the broll-able surfaces
