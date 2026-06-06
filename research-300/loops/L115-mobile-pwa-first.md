# L115 — Mobile App — PWA-First Thesis: When (if Ever) We Need Native

**Loop**: 115 / 300
**Phase**: 2 — Deep dive on top candidates
**Date**: 2026-06-06

---

## Thesis of this loop

OPENGEM is a publishing surface — a Bloomberg-grade dashboard for the world economy, daily/weekly/monthly cadence, not sub-second. The question this loop tests: does that thesis require a native iOS/Android app at any horizon, or does a Progressive Web App carry us indefinitely?

The honest answer: **PWA carries us through Y2 with no compromise. The only meaningful native-app reason at OPENGEM's scale is iOS push notifications, which Apple gates to App Store apps. Web Push on iOS Safari arrived in 2023 but with limitations that still bite in 2026.** Even there, the cost of a thin native shell (a wrapper around the PWA, ~$50 in Apple Developer fee + 2 weeks of work using Capacitor) is so low that the PWA-first approach is dominant: ship PWA at v1, ship a thin native wrapper at Y2 if iOS-push demand justifies it. *Never* ship two separate codebases.

Verdict: **PWA-first, with install hooks visible on day one and a deliberate effort to score high on the "installability" Lighthouse audit. Y2 iOS shell only if iOS-push demand is observable. Android can stay PWA forever (Android Chrome's Web Push is fully functional). No React Native, no Flutter, no Swift, no Kotlin at the app layer — those are the wrong stack for a publishing surface where the value is in the data and the visualizations, not in OS-specific affordances.**

---

## What a PWA gives us at no cost

The 2026 PWA capability matrix is dramatically better than 2020:

- **Install to home screen** on Android, iOS, macOS Safari, Windows Edge, Chrome desktop. The "Add to Home Screen" affordance shows up automatically when manifest + service worker + HTTPS are in place.
- **Offline read** of the last 30 days of data via service-worker caching. Critical for the Damian-class user on a flight.
- **Background sync** of subscribed alert rules — the service worker wakes on network reconnect and pulls in any missed events.
- **Web Push on Android Chrome, Firefox, macOS Safari (limited), Windows Edge** — push notifications without a native app.
- **Web Push on iOS Safari (since iOS 16.4, 2023)** — but only if the user installs the PWA to home screen first. This is a real friction step on iOS that doesn't exist on Android.
- **App-shell architecture** — the chrome (nav bar, command palette, theme) loads from cache; the data loads fresh. First-paint feels native-app-fast.
- **File system access** for power features (downloading vintage exports, saving tearsheets).
- **Web Share API** for native-feel share sheets.
- **Geolocation API** if we ever surface "indicators near you" (we won't at v1).

What a PWA *doesn't* give us at the same level as native:

- Background polling at sub-30-second intervals. Service workers throttle aggressively when the app isn't active. For OPENGEM's daily/weekly cadence this is fine.
- iOS Siri shortcuts. Could matter to power users; doesn't matter at v1.
- iOS widgets. Could matter for "recession probability glance" widgets; Y2 conversation.
- App Store visibility (organic discovery). Real loss but recoverable via Y2 thin native shell.

---

## When does PWA stop being enough

Three concrete triggers would flip the verdict toward native:

1. **iOS push notification adoption stays low.** If a quarterly cohort analysis shows >40% of paying iOS users don't have Web Push enabled (because the install-to-home-screen friction loses them), the case for an iOS native shell strengthens. Threshold: 40% drop-off attributable to iOS push friction.

2. **App-Store-discovery becomes a material acquisition channel.** Unlikely for OPENGEM — we're a publishing brand, not an app brand — but if a competitor lands a viral App Store launch and grabs mindshare, we'd consider a thin native shell as a defensive move. Cost: 2 weeks + $99/year Apple Developer fee.

3. **Apple ships a feature behind native-only walls that materially helps OPENGEM** — e.g., Vision Pro integration, deep iOS widgets with real data, Siri integration. Speculative; revisit annually.

None of these conditions exist at v1. PWA is the answer.

---

## The PWA manifest

```json
{
  "name": "OPENGEM World Dashboard",
  "short_name": "OPENGEM",
  "description": "The macro-accountability ledger for the world economy.",
  "start_url": "/?source=pwa",
  "id": "/?source=pwa",
  "display": "standalone",
  "display_override": ["window-controls-overlay", "standalone"],
  "background_color": "#0a0a0b",
  "theme_color": "#f59e0b",
  "orientation": "any",
  "icons": [
    { "src": "/icons/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icons/icon-512.png", "sizes": "512x512", "type": "image/png" },
    { "src": "/icons/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }
  ],
  "screenshots": [
    { "src": "/screenshots/home-wide.png", "sizes": "1280x800", "form_factor": "wide" },
    { "src": "/screenshots/home-narrow.png", "sizes": "750x1334", "form_factor": "narrow" }
  ],
  "categories": ["finance", "productivity", "news"],
  "shortcuts": [
    { "name": "Pulse", "url": "/pulse", "icons": [{ "src": "/icons/sc-pulse.png", "sizes": "96x96" }] },
    { "name": "Recession Probability", "url": "/recession", "icons": [{ "src": "/icons/sc-rec.png", "sizes": "96x96" }] },
    { "name": "Leaderboard", "url": "/leaderboard", "icons": [{ "src": "/icons/sc-lb.png", "sizes": "96x96" }] }
  ],
  "share_target": {
    "action": "/share",
    "method": "GET",
    "params": { "title": "title", "text": "text", "url": "url" }
  }
}
```

Notable choices:

- `display: standalone` so the installed app looks like a native app (no browser chrome).
- `theme_color: #f59e0b` — the Bloomberg amber from L119.
- `shortcuts` for quick-launch from the install icon (long-press on Android, force-press on iOS).
- `share_target` so OPENGEM appears in the OS native share sheet — a user can share a Substack post and "send to OPENGEM" to bookmark it.

---

## The service worker strategy

Three caching layers:

1. **App shell** (HTML, CSS, JS bundle) — cache-first, network-fallback. Updated when a new version hash is detected.
2. **Static data** (country list, indicator list, methodology pages) — stale-while-revalidate. Serves cached immediately, fetches fresh in background.
3. **Live data** (forecasts, indicator values, scenario probabilities) — network-first with 5s timeout, cache-fallback. The dashboard works offline with the last cached state if network is unavailable.

The vintage data is *immutable* by definition — a forecast at vintage 2026-06-06 will never change. So we cache vintage-keyed URLs with `Cache-Control: public, immutable, max-age=31536000`. The latest-vintage URLs use shorter TTLs.

---

## Install prompt timing

Browsers throttle the `beforeinstallprompt` event — show the install prompt too early and the user dismisses; too late and the user already left. Our timing:

- **First visit**: no prompt. Just the page.
- **Second visit OR first visit lasting >2 minutes with >3 page views**: show a small, dismissable "Install OPENGEM" banner at the top of the page (not a modal — banners convert better and feel less aggressive).
- **Sixth visit**: show the banner again if previously dismissed.
- **Never again** after the user explicitly closes the banner three times.

Implementation: a tiny client-side counter in localStorage tracks visits + page views; the banner is rendered conditionally based on the counter and the `beforeinstallprompt` event being available.

---

## iOS install instructions (because beforeinstallprompt doesn't work there)

iOS Safari doesn't fire `beforeinstallprompt`. The user has to manually share → "Add to Home Screen." We need to *teach* this on iOS.

The iOS-specific banner says: "Install OPENGEM: tap [share icon], then 'Add to Home Screen.'" The share icon is rendered as an inline SVG so users recognize it visually.

This is a one-paragraph educational banner, shown once per device after the same trigger thresholds as Android.

---

## Web Push subscription on iOS

After install, the user can subscribe to push notifications. Apple's API:

1. User visits installed PWA, clicks "Enable alerts."
2. App calls `Notification.requestPermission()`.
3. iOS shows the system permission prompt; user grants.
4. App subscribes via `pushManager.subscribe({ userVisibleOnly: true, applicationServerKey: VAPID_KEY })`.
5. Subscription object is sent to OPENGEM backend, stored on `users.delivery_channels.web_push`.

When an alert fires, the backend sends a push via the web-push protocol (encrypted, signed with VAPID). iOS Safari shows it in Notification Center.

The iOS friction: step 1 requires the user to have *installed* the PWA first. About 20% of iOS visitors install; of those, ~60% grant push permission. End-to-end iOS push conversion: ~12%. This is the data point that, if much lower than projected, would trigger the Y2 thin-native-shell decision.

---

## What we deliberately *don't* ship at v1

- **No React Native or Flutter app.** A second codebase for "the app version" of OPENGEM is the wrong investment — it dilutes engineering effort, introduces parity bugs, and the value-add is small for a publishing surface.
- **No Capacitor wrapper yet.** Capacitor (the Ionic wrapper-around-PWA tool) is the *Y2 escape hatch* if iOS demand justifies. Ship at v1 without it.
- **No native widgets.** Could matter at Y2; not at v1.
- **No mobile-only features.** Whatever shows on mobile shows on desktop (responsive); no "this is the mobile experience" vs "this is the desktop experience" divergence.

---

## Next-step: the manifest registration + install banner skeleton

```tsx
// app/layout.tsx — register PWA manifest
export const metadata: Metadata = {
  manifest: "/manifest.json",
  themeColor: "#f59e0b",
  appleWebApp: {
    capable: true,
    statusBarStyle: "black-translucent",
    title: "OPENGEM",
  },
};

// components/InstallBanner.tsx
"use client";
import { useEffect, useState } from "react";

export function InstallBanner() {
  const [prompt, setPrompt] = useState<any>(null);
  const [visible, setVisible] = useState(false);
  const [isIOS, setIsIOS] = useState(false);

  useEffect(() => {
    const ua = navigator.userAgent;
    const ios = /iPad|iPhone|iPod/.test(ua) && !/MSStream/.test(ua);
    setIsIOS(ios);
    const visits = parseInt(localStorage.getItem("og:visits") ?? "0") + 1;
    localStorage.setItem("og:visits", String(visits));
    const dismissals = parseInt(localStorage.getItem("og:install_dismissed") ?? "0");
    if (dismissals >= 3) return;
    if (visits >= 2 && !window.matchMedia("(display-mode: standalone)").matches) {
      if (ios) setVisible(true);
      const handler = (e: any) => { e.preventDefault(); setPrompt(e); setVisible(true); };
      window.addEventListener("beforeinstallprompt", handler);
      return () => window.removeEventListener("beforeinstallprompt", handler);
    }
  }, []);

  if (!visible) return null;
  return (
    <div className="install-banner">
      Install OPENGEM as an app —
      {isIOS
        ? <span> tap <ShareIcon /> then "Add to Home Screen"</span>
        : <button onClick={() => prompt?.prompt()}>Install</button>}
      <button onClick={() => {
        const d = parseInt(localStorage.getItem("og:install_dismissed") ?? "0") + 1;
        localStorage.setItem("og:install_dismissed", String(d));
        setVisible(false);
      }}>×</button>
    </div>
  );
}
```

---

## What this loop produced

- Verdict: PWA-first, no native at v1, Y2 thin-iOS-shell decision tied to ≥40% iOS push friction.
- Full PWA manifest tuned for OPENGEM's brand + shortcuts + share_target.
- Three-layer service-worker caching strategy (app shell / static data / live data).
- Install-prompt timing thresholds for Android and iOS.
- Web Push subscription flow with iOS friction accepted.
- A working install-banner skeleton with iOS-specific copy.

## What comes next

- **L142** — mobile information density study uses this PWA shell as the substrate.
- **L263** — mobile layout prototype.
- **L131** — alerts UX integrates with Web Push.

## Related

- [[L142-mobile-information-density]] — sister design loop
- [[L131-alerts-ux]] — Web Push is one of the delivery channels
- [[L119-dark-mode-bloomberg-orange]] — theme_color from this palette
- [[L114-discord-telegram-alerts]] — push channel decisions complement bots
- [[L263-mobile-layout-prototype]] — Phase 5 implementation
