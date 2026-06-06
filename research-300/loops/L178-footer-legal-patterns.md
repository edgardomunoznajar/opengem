# L178 — Footer + Legal Patterns

**Loop**: 178 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The thesis

The footer is the only place in OPENGEM that's the same on every page. It's the place to surface legal, licensing, governance, and "where to go next" links. We design it for trust signals and discoverability.

Not a marketing footer (no "subscribe to our newsletter!" megaboxes). A reference footer.

## The layout

Full-width band at the bottom of every page. Two rows.

### Top row — the columns

```
   ┌────────────────────────────────────────────────────────────────┐
   │                                                                  │
   │  PRODUCT       DATA            DEVELOPERS       ABOUT            │
   │  ─────────    ─────────       ──────────       ──────            │
   │  Home         Countries        API docs         About             │
   │  Watchlist    Indicators       MCP install      Governance        │
   │  Alerts       Scenarios        OpenAPI          Changelog         │
   │  Compare      Forecasts        SDKs             Roadmap           │
   │  Pricing      Leaderboard      Status           Press kit         │
   │               Methodology      GitHub           Contact           │
   │                                                                  │
   │  EDITORIAL     ACCOUNTABILITY  LEGAL                              │
   │  ─────────    ─────────       ──────                              │
   │  Why OPENGEM  Open ledger     Terms                              │
   │  Glossary     Track record    Privacy                            │
   │  RSS feeds    Post-mortems    Cookie notice                      │
   │  Newsletter   Quarterly retro  Acceptable use                    │
   │                                Security                           │
   │                                Citation policy                    │
   │                                                                  │
   └────────────────────────────────────────────────────────────────┘
```

### Bottom row — the brand strip

```
   ┌────────────────────────────────────────────────────────────────┐
   │                                                                  │
   │  OPENGEM · open macro accountability ledger                      │
   │  Code: Apache-2.0  ·  Data: CC-BY-4.0  ·  Built in: California   │
   │                                                                  │
   │  v2.4.1 · last deploy 2026-06-06 14:22 UTC                       │
   │                                                                  │
   │  © 2024–2026 OPENGEM. The forecasts are open.                   │
   │  [GitHub] [RSS] [Discord] [Mastodon] [Substack]                  │
   │                                                                  │
   └────────────────────────────────────────────────────────────────┘
```

## The 7 columns explained

1. **Product** — entry points to the dashboard
2. **Data** — the catalog (countries, indicators, scenarios, forecasts)
3. **Developers** — API, MCP, SDKs, GitHub, status
4. **About** — governance, changelog, roadmap, press
5. **Editorial** — narrative, glossary, feeds, newsletter
6. **Accountability** — ledger, track record, post-mortems
7. **Legal** — terms, privacy, security, citation

Seven columns at desktop. On tablet, 4 columns. On mobile, accordion (collapsed by default with chevrons).

## Required legal links (the mandatory)

These five are surfaced explicitly per regulator expectation:

- **Terms of Service** — `/legal/terms`
- **Privacy Policy** — `/legal/privacy`
- **Cookie Notice** — `/legal/cookies`
- **Acceptable Use Policy** — `/legal/aup`
- **Security & Vulnerability Disclosure** — `/legal/security`

Plus:
- **Citation Policy** — `/legal/citation` (how to cite OPENGEM)
- **Data licenses** — explicit CC-BY-4.0 on data, Apache-2.0 on code

## License badges

The brand strip carries explicit license badges:

```
   Code: Apache-2.0  ·  Data: CC-BY-4.0
```

These link to:
- `/legal/licenses` (full breakdown)
- LICENSE.md in the repo
- The CC-BY-4.0 license at creativecommons.org

## Build / version stamp

```
   v2.4.1 · last deploy 2026-06-06 14:22 UTC
```

The footer shows:
- Current app version (semver)
- Last deploy timestamp
- Click → routes to `/about/changelog`

This is the engineer-quality signal. A user inspecting the footer can see: this is a real system that ships continuously.

## Status link

A subtle indicator in the footer:

```
   [● All systems operational]   ← green if up, red if degraded
```

Routes to `/status` (Statuspage-equivalent).

When degraded: a colored banner appears at the top of the page (not just the footer).

## Trust badges (sparingly)

We resisted "trusted by Forbes / Wall Street Journal." Instead:

```
   Built openly:
   [GitHub stars] [npm downloads] [PyPI installs]
```

Small, real, verifiable badges. The kind that says "this is a working project." No "as seen in TechCrunch."

## Compliance footer items

For paid customers + regulatory expectations:

- **GDPR**: data processing addendum link
- **SOC 2**: status page (we're not SOC 2 in V1; we'll add as paid tier matures)
- **CCPA**: California privacy rights link

These appear in the legal column.

## Subscribe (subtle)

A small footer-strip option:

```
   Weekly digest:  [your@email]  [Subscribe]
   1 email/week, the best forecasts and the worst misses.
```

Not aggressive. Below-the-fold.

## Internationalization

Footer text is localized when L118 lands. URLs route to localized pages.

## Mobile

At <640px:
- Columns become accordion (collapsed by default)
- Brand strip wraps to multiple lines
- Build stamp remains visible

## Accessibility

- All link groups have `<h3>` headers (visually styled as text-xs uppercase per L147)
- Tab order: left-to-right through columns, then brand strip
- ARIA-labeled nav landmarks

## SEO

The footer carries internal links to every major destination. This is the site's flat-link map, helping search crawlers index everything.

## What the footer is NOT

- A second navigation. The top nav is the primary; the footer is reference.
- A marketing surface. No "join 10,000 users" callouts.
- A "trust signals" parade. Real signals only — license, version, status.
- A cookie banner. Cookie notice link only; banners are top-of-page (when needed).

## The legal pages themselves

Per L283/L284 (Phase 6), but seeding pattern:

### Terms of Service (`/legal/terms`)

Plain-language at the top, lawyer-quality below. CC-BY-SA-4.0 derived from the FAIR Universal Terms template. Includes:
- Service description
- Acceptable use
- API/MCP usage rules
- Forecasting disclaimer ("not financial advice")
- Limitation of liability
- Indemnification
- Termination
- Governing law

### Privacy Policy (`/legal/privacy`)

GDPR + CCPA + standard. Covers:
- What we collect (analytics minimal — Plausible / Umami; no third-party trackers)
- What we don't (no behavioral profiling for ads)
- API key handling (hashed, never logged in cleartext)
- Email handling (transactional + opt-in)
- Data subject rights
- Retention periods

### Cookie Notice (`/legal/cookies`)

Tiny:
- Functional cookies (session, theme preference)
- Analytics cookies (anonymous; opt-out toggle)
- No marketing cookies

No GDPR popover for the analytics tier — they're anonymous and we have a consent-not-needed defense.

### Acceptable Use (`/legal/aup`)

What we don't allow:
- Scraping for resale (but: forking the open data and republishing is fine — CC-BY-4.0)
- Abusive API usage (DDoS, evasion of rate limits)
- Misrepresentation (claiming OPENGEM forecasts are yours)
- Use in regulated trading without your own analyst layer

### Security (`/legal/security`)

- security.txt at `/.well-known/security.txt`
- Disclosure process
- Bug bounty (small — modest cash rewards)
- PGP key for sensitive reports

### Citation Policy (`/legal/citation`)

How to cite OPENGEM:
- The DOI is preferred
- The OPENGEM ID is the fallback
- The URL is sufficient for informal mention
- We ask for attribution; we don't demand exclusivity

## Implementation

- Footer is a server component, rendered on every page
- Status indicator polls `/status.json` on hover; cached client-side for 60s
- Build stamp injected at build time
- License badges static SVGs

## Performance

- Footer adds ~6KB HTML
- Status check is lazy (hover-triggered)
- No layout shift

## The "publish your mistakes" footer line

A subtle but deliberate line at the very bottom:

```
   © 2024–2026 OPENGEM. The forecasts are open.
```

Not a tagline. A reminder. The footer's *job* is to be the place a user looks when they want to verify the legitimacy of the artifact. "The forecasts are open" sits there as the brand truth.

## The asymmetric move

Most fintech footers are marketing soup. Real-product footers (Stripe, Linear, Vercel) are reference: links you actually need, plus a status indicator.

OPENGEM's footer is a *reference desk*. Every legal page is short and plain. Every link works. The version stamp is real. The license is real. The status is real.

A user scrolling to the footer of OPENGEM finds the maintainer's brain: governance, code, status, license. Bloomberg's footer is "Bloomberg.com." Ours is the project.
