# L111 — Embeddable Widgets v2: iframe + Script SDK, with Live + Theme + Provenance Upgrades

**Loop**: 111 / 300
**Phase**: 2 — Deep dive on top candidates
**Date**: 2026-06-06

---

## Thesis of this loop

The L245 prototype shipped a working v1 embed: zero-dependency vanilla JS at `public/embed.js`, three sizes (square/banner/tall), three kinds (recession_prob/gpr_nowcast/forecast), inline SVG sparkline, vintage badge + OPENGEM brand link, fetches from `/v1/*` endpoints. It works. It does not yet earn the strategic role L007's distribution thesis assigns it — "embeds are the distribution multiplier." This loop specs v2.

The mistake to avoid: embed bloat. The temptation is to add charts, drilldowns, animations, and theming layers until the embed becomes "the dashboard, but smaller." That kills the load-anywhere promise and breaks the SDK's drop-in simplicity. The v2 upgrades are *conservative* — five additions plus one structural refactor — chosen because each unlocks a distribution surface the v1 doesn't.

Verdict: **v2 keeps the vanilla-JS, zero-dep shape, but adds (1) iframe-fallback mode for Substack/strict-CSP hosts, (2) SSE-backed "live tile" that streams updates via the L103 event stream, (3) host-side theme tokens, (4) a tier-keyed white-label option that strips the OPENGEM brand link (Studio tier and above), (5) Open Graph image generation per embed URL for Twitter unfurl. The structural refactor: split the single `embed.js` into a tiny loader + lazy-fetched render kernels, keeping the loader at ≤2KB to clear corporate-network filtering.**

---

## What v1 got right (don't break these)

The L245 embed established four invariants:

- **Zero external dependencies.** Single IIFE, ~3KB. Loads from one URL, runs everywhere.
- **Auto-mount on DOMContentLoaded** for elements with `data-opengem`. Programmatic remount available via `window.OPENGEM.mount(node)`.
- **Inline styles, no CSS leakage.** Host page CSS doesn't bleed in; embed CSS doesn't bleed out.
- **Vintage badge + brand link in every tile.** This is the brand-deal that justifies the data being free.

v2 preserves all four. No drift.

---

## Upgrade 1: iframe-fallback for strict-CSP hosts

Substack, some WordPress installs, GitHub READMEs, and most school-internal CMSes have strict Content-Security-Policy that blocks remote `<script>` tags. The v1 embed fails silently on these. v2 ships a parallel iframe path:

```html
<!-- v1 style — script SDK -->
<div data-opengem data-kind="recession_prob" data-country="USA" data-size="square"></div>
<script src="https://opengem.org/embed.js" defer></script>

<!-- v2 fallback — iframe -->
<iframe
  src="https://opengem.org/embed/iframe?kind=recession_prob&country=USA&size=square"
  width="200" height="200" frameborder="0" loading="lazy"
  title="USA recession probability — OPENGEM"
></iframe>
```

The iframe URL is *server-rendered* via the same React component that the script SDK uses client-side. Both paths produce identical visual output. The iframe is automatically the right shape for Substack, GitHub README via image-only fallback (using img+SVG), and any host that blocks third-party JS.

The iframe surface gets `X-Frame-Options: ALLOWALL` and an empty `Content-Security-Policy: frame-ancestors *;` — explicitly cross-origin-embeddable. A `referrer-policy: strict-origin-when-cross-origin` keeps the host URL semi-private.

---

## Upgrade 2: SSE-backed "live tile" mode

A new attribute, `data-live`, opts the tile into the L103 SSE stream. The tile self-updates as new vintages arrive without page refresh.

```html
<div data-opengem
     data-kind="forecast"
     data-country="USA" data-indicator="cpi_yoy"
     data-size="banner"
     data-live="true"></div>
```

Implementation in the embed SDK:

```js
function startLiveStream(node, params) {
  const url = new URL("https://opengem.org/v1/events", location.href);
  if (params.country) url.searchParams.set("countries", params.country);
  if (params.indicator) url.searchParams.set("indicators", params.indicator);
  const es = new EventSource(url.toString());
  es.onmessage = (m) => {
    const ev = JSON.parse(m.data);
    if (ev.kind === "indicator_update" || ev.kind === "forecast_revision") {
      renderTile(node, ev.payload, params.size, params.label, ev.vintage_id);
    }
  };
  es.onerror = () => setTimeout(() => startLiveStream(node, params), 5000);
}
```

EventSource auto-reconnects with `Last-Event-ID` so the embed catches up after a network hiccup. The cost on the server side: ~5KB/hour per live tile from heartbeats and updates — negligible.

The default for v2 stays `data-live="false"`. Host pages opt in explicitly because some hosts (newsletter archives) don't want live updates.

---

## Upgrade 3: host-side theme tokens

v1 was dark-only. v2 ships `data-theme="dark|light|terminal|editorial"` plus per-tile color overrides via `data-color-bg`, `data-color-ink`, `data-color-accent`. The four named themes ship from the SDK with curated palettes:

- `dark` — the v1 default, dark surface, amber accent (matches L119 main app palette).
- `light` — light surface, charcoal ink, dark amber accent (the L119 light variant).
- `terminal` — pure-black background, Bloomberg-amber, JetBrains Mono throughout.
- `editorial` — off-white background, near-black serif headlines for newsletter-style hosts.

Custom themes are achievable via `data-color-*` overrides which set CSS variables on the rendered tile.

---

## Upgrade 4: tier-keyed white-label

A new attribute, `data-key`, opts into the paid white-label mode. The SDK includes a tiny JWT-verify step (using the public key shipped with the SDK; verification ~10ms client-side):

```html
<div data-opengem
     data-key="og_sk_studio_abc..."
     data-kind="forecast" data-country="USA" data-indicator="cpi_yoy"></div>
<script src="https://opengem.org/embed.js" defer></script>
```

The SDK verifies the JWT, reads the `tier` claim, and:

- **Studio tier+** removes the OPENGEM brand link from the corner. The vintage badge stays (it's the data contract, not the brand).
- **Newsroom tier+** allows `data-logo-url` so the host's logo appears in the corner instead.
- **Institutional tier+** allows `data-domain` to override the link target to a custom subdomain.

A key that doesn't verify or has expired gracefully degrades to the free-tier rendering (brand link visible) rather than failing — the embed *never* breaks.

---

## Upgrade 5: Open Graph image per embed URL

Every embed URL gets a paired `og-image` URL that returns a 1200×630 PNG suitable for Twitter/LinkedIn/Discord/Slack unfurl. The server-side image is the same React component rendered to PNG via `@vercel/og` (Satori under the hood).

```
GET  https://opengem.org/embed/og?kind=forecast&country=USA&indicator=cpi_yoy&size=banner
→ image/png 1200×630 (24-hour cached)
```

A `<meta property="og:image">` tag is emitted whenever an OPENGEM URL is embedded in a parent page; this drives social-share previews.

This is the single largest brand-amplification mechanism in v2 — every time someone tweets an OPENGEM embed URL, the Twitter card shows the tile with the OPENGEM watermark. The cost is ~$10/mo of Cloudflare Image rendering quota at v1 scale.

---

## Structural refactor: loader + lazy render kernels

v1's single 3KB file is fine. As v2 adds features (theme, live, white-label, fallback), naive expansion would hit 12-15KB. We instead split:

- **`embed.js` (the loader, ≤2KB)** — DOM scanner, requestIdleCallback dispatcher, dynamic `<script>` load of the kernel based on the tile's `data-kind`.
- **`embed-render-tile.js` (~5KB)** — the tile renderer for static tiles.
- **`embed-render-live.js` (~3KB)** — the SSE-streaming renderer.
- **`embed-render-themed.js` (~2KB)** — the theme-tokens applier.

The loader fingerprints each kernel URL by content hash so kernels are immutable-cacheable forever at CDN edge. A page with three static tiles loads only `embed.js` + `embed-render-tile.js` — total ~7KB. A page with a live tile additionally loads `embed-render-live.js` (~3KB more). Pages without embeds load nothing.

---

## Production-readiness deltas from L245's checklist

L245 had a six-item production-readiness checklist. v2 closes four of them and defers two:

- **Tag-level CSP-safe inline styles** — closed. v2 emits styles via JS `Object.assign(node.style, ...)` rather than inline `<style>` tags, so strict `style-src 'none'` hosts still render.
- **Subresource Integrity hash published in docs** — closed. The `/embed` page (L245's `app/embed/page.tsx`) now ships SRI hashes per kernel URL.
- **CDN: Cloudflare R2 + Workers cache** — closed in deployment plan (L269 follow-up).
- **Versioned URL: `/embed/v1.js`** — closed. Loader is at `/embed/v2.js`; old `/embed.js` redirects to `/embed/v1.js` (frozen) for backward compatibility.
- **Click-through analytics** — DEFERRED. Privacy-respecting embed analytics is a Y1.5 conversation; meanwhile we use server-side request logs.
- **Open-graph cards** — closed as Upgrade 5 above.

---

## Next-step: the v2 loader skeleton

```js
// public/embed/v2.js — loader (≤2KB target)
(function () {
  const ORIGIN = "https://opengem.org";
  const KERNEL_VERSION = "2.0.0";

  const KERNELS = {
    static: `${ORIGIN}/embed/render-tile-${KERNEL_VERSION}.js`,
    live: `${ORIGIN}/embed/render-live-${KERNEL_VERSION}.js`,
  };

  const loadedKernels = new Map();
  function loadKernel(name) {
    if (loadedKernels.has(name)) return loadedKernels.get(name);
    const p = new Promise((resolve, reject) => {
      const s = document.createElement("script");
      s.src = KERNELS[name];
      s.async = true;
      s.crossOrigin = "anonymous";
      s.onload = () => resolve(window.OPENGEM[name]);
      s.onerror = reject;
      document.head.appendChild(s);
    });
    loadedKernels.set(name, p);
    return p;
  }

  function dispatch(node) {
    const live = node.dataset.live === "true";
    const kernel = live ? "live" : "static";
    loadKernel(kernel).then((render) => render(node));
  }

  function init() {
    document.querySelectorAll("[data-opengem]").forEach((node) => {
      if ("requestIdleCallback" in window) {
        requestIdleCallback(() => dispatch(node));
      } else {
        setTimeout(() => dispatch(node), 0);
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  window.OPENGEM = window.OPENGEM || {};
  window.OPENGEM.mount = (node) => dispatch(node);
  window.OPENGEM.init = init;
})();
```

---

## What this loop produced

- Verdict: v2 keeps v1 invariants, adds five upgrades + one structural refactor.
- iframe-fallback mode for strict-CSP hosts.
- SSE-backed live tile mode using L103's stream.
- Theme tokens with four named themes and per-color overrides.
- Tier-keyed white-label via JWT.
- OG image per embed URL for social unfurl.
- Loader/kernel split keeping the loader ≤2KB.
- A working v2 loader skeleton.

## What comes next

- **L155** — sharing UX (gif/png/link/oembed) builds on the same render pipeline.
- **L144** — embed widget design (Phase 3) refines the visual.
- **L245** — v1 prototype that this loop upgrades.

## Related

- [[L007-distribution-thesis]] — embeds are the distribution multiplier
- [[L103-fastapi-websocket]] — the SSE stream powering live tile
- [[L119-dark-mode-bloomberg-orange]] — the four named themes
- [[L245-embed-widget]] — the v1 prototype
- [[L155-sharing-ux]] — shares use the OG image generator
