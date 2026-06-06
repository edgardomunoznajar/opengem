# L106 — RSS + Atom Feed Catalog: One Feed Per Slice That Matters

**Loop**: 106 / 300
**Phase**: 2 — Deep dive on top candidates
**Date**: 2026-06-06

---

## Thesis of this loop

L007 ranked RSS as the #2 ROI channel for the credibility cohort and the channel with the highest *underrated* potential. This loop spec's the catalog: which feeds we publish at v1, the format choice (RSS 2.0 vs Atom 1.0 vs JSON Feed), the item payload shape, the discovery surface, and the integration with Substack-mirror + email-mirror so the Lin-Priya-Marcus cohort can route OPENGEM into their reading flow on whichever surface they prefer.

The mistake most data publishers make with RSS: they ship one global feed ("all updates") that's either too noisy (every tick, every minute) or too sparse (one item per month). The right answer is **fine-grained feeds, one per meaningful slice**, with a discoverability layer that helps users find the *three* feeds they actually want. Per country. Per indicator. Per forecast pack. Per scenario. Per failure log. The combinatorial total is ~3000 feeds. That's not a problem — feeds cost ~nothing to publish; the problem is helping users navigate.

Verdict: **publish ~3000 fine-grained feeds at v1, all three formats (RSS 2.0 + Atom 1.0 + JSON Feed) at one URL each via content negotiation, with a `/feeds` catalog page that's both a humans-friendly browse UI and a machine-readable OPML download for one-click "import all my watched countries into NetNewsWire."** Mirror the daily-digest feed to Substack via Substack's RSS import. Mirror to Buttondown for email. The feed catalog is the single largest top-of-funnel surface for the credibility cohort.

---

## The format decision: ship all three

RSS 2.0, Atom 1.0, and JSON Feed 1.1 all solve the same problem with slightly different shapes. Forcing users to pick costs you adoption. Modern feed readers (NetNewsWire, Feedly, Inoreader, Reeder, FreshRSS) all accept all three.

Strategy:

- Single URL per feed: `/feeds/countries/USA.xml`. Server-side content negotiation: `Accept: application/atom+xml` → Atom; `Accept: application/json` → JSON Feed; default → RSS 2.0.
- Explicit URL variants: `/feeds/countries/USA.rss`, `.atom`, `.json`. Some readers cache the URL, not the content type — so users can paste the format they want.
- A single `<link rel="alternate">` block in the HTML `<head>` of every OPENGEM page exposes all three feed URLs for the country/indicator/scenario in scope. Browser extensions and feed readers auto-detect.

The payload is the same across formats — only the framing differs. A single Pydantic model produces all three.

---

## The catalog (v1 — eight feed families)

### Family 1 — Per country (~200 feeds)

`/feeds/c/{iso3}.rss` — every forecast revision, every indicator update, every scenario trigger touching that country.

Why this matters: a Brazil-focused journalist follows `/feeds/c/BRA.rss` and gets every OPENGEM update about Brazil in their reader. This is the single most-used feed shape in practice (modeled on FT's per-country feeds).

Item cadence: ~5-15 items/week for Tier-V countries, ~1-3/week for Tier-T countries.

### Family 2 — Per indicator (~50 feeds)

`/feeds/i/{indicator}.rss` — every country's update of a given indicator (CPI, GDP, unemployment, policy rate, etc.) on its release calendar.

Why this matters: the CPI specialist at a sovereign fund subscribes to `/feeds/i/cpi_yoy.rss` and gets every CPI release across every country with OPENGEM's nowcast overlay.

Item cadence: ~30-50 items/week (high-volume).

### Family 3 — Per scenario (~10-20 feeds, dynamic)

`/feeds/s/{scenario_slug}.rss` — every probability update, every trigger event, every methodology change for that scenario pack.

Why this matters: the geopolitical analyst tracking the `oil_shock_2026` pack subscribes to its feed and gets a notification when its probability moves materially or when new triggering data arrives.

Item cadence: 2-10 items/week per scenario. Variable.

### Family 4 — Per forecast pack (~5-10 feeds)

`/feeds/f/{pack_slug}.rss` — a curated weekly "best forecast revisions" feed per major pack (recession-probability, inflation-regime, sovereign-risk, exchange-rate, supply-chain).

Item cadence: ~1-3 items/week per pack — editorial curation, not firehose.

### Family 5 — Global firehoses (~6 feeds)

- `/feeds/all-revisions.rss` — every forecast revision, full firehose.
- `/feeds/all-triggers.rss` — every scenario probability change above 5%.
- `/feeds/all-misses.rss` — every forecast miss surfaced from the accountability ledger.
- `/feeds/all-methodology.rss` — every methodology change with diff link.
- `/feeds/all-events.rss` — every GDELT/ACLED event burst flagged by the pulse globe.
- `/feeds/daily-digest.rss` — the curated daily digest (the Substack mirror feeds off this).

Item cadence: firehoses are 50-500 items/week. Daily digest is 7 items/week.

### Family 6 — Country×indicator (~10,000 feeds, lazy-generated)

`/feeds/c/{iso3}/{indicator}.rss` — the cartesian product. Only generated on demand (not pre-baked), cached for 1 hour.

Why this matters: the very narrow user — "I track only Argentina inflation" — gets exactly the feed shape they want. We don't bake all 10k feeds at build time; the URL pattern is registered and the response is generated when first requested.

Item cadence: ~1-4 items/month per pair.

### Family 7 — Watchlist (per-user)

`/feeds/u/{token}.rss` — a personalized feed derived from a user's saved watchlist. Token is opaque, revocable, no auth required at request time.

Why this matters: power users who configure a watchlist of 20 countries + 10 indicators want one feed, not 30 feeds. This is the discovery flywheel — the user signs up for free, configures a watchlist, gets a personalized URL, pastes it into Feedly, and is now a recurring subscriber forever.

Item cadence: whatever their watchlist sums to. Typically 10-100 items/week.

### Family 8 — Editorial / failure log (1-2 feeds)

- `/feeds/failure-log.rss` — every post-mortem.
- `/feeds/editorial.rss` — manually-curated explainer posts.

Why this matters: the *brand* of "we publish our mistakes" lives in the failure-log feed. It's the one feed every macro journalist should subscribe to.

---

## The item payload shape

Every feed item, regardless of family, has the same shape:

```xml
<item>
  <title>USA CPI YoY nowcast revised 3.1% → 3.2% (vintage 2026-06-06)</title>
  <link>https://opengem.org/c/USA/cpi_yoy?v=2026-06-06</link>
  <guid isPermaLink="true">https://opengem.org/c/USA/cpi_yoy?v=2026-06-06#fc-a3f2</guid>
  <pubDate>Fri, 06 Jun 2026 13:42:00 GMT</pubDate>
  <description><![CDATA[
    <p>OPENGEM's nowcast for USA CPI YoY moved from 3.1% (vintage 2026-06-05)
    to 3.2% (vintage 2026-06-06), driven by the latest BLS release.</p>
    <p><img src="https://opengem.org/static/c/USA/cpi_yoy/2026-06-06.png"
            alt="USA CPI YoY chart, vintage 2026-06-06" /></p>
    <p><strong>Methodology:</strong>
       <a href="https://opengem.org/methodology/cf-nowcast-v3">CF Nowcast v3.1</a></p>
    <p><strong>JSON:</strong>
       <a href="https://opengem.org/v1/forecasts?country=USA&indicator=cpi_yoy&vintage=2026-06-06">.json</a></p>
    <p><strong>Cite this view:</strong>
       <a href="https://opengem.org/cite/USA-cpi_yoy-2026-06-06">opengem:USA/cpi_yoy/2026-06-06</a></p>
  ]]></description>
  <category>USA</category>
  <category>cpi_yoy</category>
  <enclosure url="https://opengem.org/static/c/USA/cpi_yoy/2026-06-06.png"
             type="image/png" length="48230" />
</item>
```

Non-obvious choices:

- **The description embeds a hosted PNG of the chart.** A reader can paste the item into a memo and the chart goes with it. L007 tactic: feeds carry the full payload.
- **The JSON link is in every item.** A reader who wants the raw data clicks once.
- **The cite-this-view link is in every item.** Reinforces the brand promise that every view is permanent.
- **The category fields populate Feedly's "tag" filter** — power users can filter by country or indicator across multiple feeds.
- **The PNG is enclosed** so podcast-style feed readers display it inline.

---

## The discovery surface: `/feeds`

The catalog page is both a humans-friendly browse UI and a machine-readable OPML download.

UI structure:

- Top: search bar ("Find feed: country, indicator, scenario").
- Section "By country" — alphabetical list with click-to-copy URL.
- Section "By indicator" — same.
- Section "By scenario" — current + historical.
- Section "Firehoses" — the six global firehoses.
- Section "Editorial" — failure log + curated.
- Bottom: "Download my watchlist as OPML" (auto-generated from user's saved watchlist).

The OPML download is the killer feature. A user with a 30-country watchlist gets a single OPML file they import into NetNewsWire and now have 30 organized feeds in their reader. This converts "casual visitor" → "permanent subscriber" in two clicks.

---

## Substack and email mirrors

Substack accepts external RSS feeds as the import source for a Substack newsletter. We configure `opengem.substack.com` to import from `/feeds/daily-digest.rss`. Every digest item becomes a Substack post automatically. Substack's discovery cross-recommends us to readers of adjacent stacks (Joey Politano, Skanda Amarnath, etc.).

Buttondown (or Beehiiv) handles the email mirror: subscribers enter email → Buttondown polls the daily-digest RSS → sends as email at 7am ET.

Both mirrors are zero-marginal-cost — they're consuming the feed we publish anyway.

---

## Next-step: the feed generator skeleton

```python
# api/feeds/router.py
from fastapi import APIRouter, Response, Request
from feedgen.feed import FeedGenerator
from .models import FeedItem

router = APIRouter()

def render(items: list[FeedItem], meta: FeedMeta, request: Request) -> Response:
    fg = FeedGenerator()
    fg.id(meta.canonical_url)
    fg.title(meta.title)
    fg.link(href=meta.canonical_url, rel="alternate")
    fg.link(href=meta.canonical_url + ".rss", rel="self")
    fg.description(meta.description)
    fg.language("en")
    fg.author({"name": "OPENGEM", "email": "editor@opengem.org"})
    fg.image(url="https://opengem.org/static/feed-icon.png")

    for it in items:
        e = fg.add_entry()
        e.id(it.guid)
        e.title(it.title)
        e.link(href=it.url)
        e.pubDate(it.published)
        e.description(it.html_description)
        for cat in it.categories:
            e.category({"term": cat})
        if it.image_url:
            e.enclosure(it.image_url, str(it.image_bytes), "image/png")

    accept = request.headers.get("accept", "")
    if "atom" in accept:
        return Response(fg.atom_str(), media_type="application/atom+xml")
    if "json" in accept:
        return Response(fg.json_str(), media_type="application/json")
    return Response(fg.rss_str(), media_type="application/rss+xml")

@router.get("/feeds/c/{iso3}.{ext}")
async def country_feed(iso3: str, ext: str, request: Request):
    items = await fetch_country_feed_items(iso3, limit=50)
    meta = FeedMeta(
        title=f"OPENGEM — {iso3} updates",
        canonical_url=f"https://opengem.org/c/{iso3}",
        description=f"Forecast revisions, indicator updates, and scenario triggers for {iso3}.",
    )
    return render(items, meta, request)
```

---

## What this loop produced

- An eight-family feed catalog totaling ~3000 published feeds + ~10,000 lazy-generated feeds.
- A content-negotiation strategy supporting RSS 2.0 + Atom 1.0 + JSON Feed at one URL.
- A full-payload item shape with embedded chart PNG + JSON link + cite-this-view link.
- The `/feeds` catalog page design with OPML export.
- Substack + email mirror integration via Buttondown.
- A feed generator skeleton ready for `api/feeds/router.py`.

## What comes next

- **L112** — the Substack integration deep-dive uses this digest feed as the upstream source.
- **L179** — RSS / Atom feed catalog (Phase 3 design surface).
- **L247** — RSS / Atom feed generator implementation.

## Related

- [[L007-distribution-thesis]] — RSS is channel #2 for credibility cohort
- [[L112-substack-integration]] — uses `/feeds/daily-digest.rss` as upstream
- [[L130-watchlist-ux]] — watchlist feed is per-user
- [[L179-rss-atom-feed-catalog]] — UI design loop pairs with this
- [[L200-failure-log]] — failure log feed is the editorial brand anchor
