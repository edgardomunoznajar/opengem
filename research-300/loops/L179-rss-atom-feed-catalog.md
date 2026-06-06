# L179 — RSS / Atom Feed Catalog

**Loop**: 179 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The thesis

RSS is the open distribution channel that the cartel has abandoned and the LLM ecosystem has rediscovered. We publish Atom feeds everywhere it makes sense. LLM agents subscribe. Substack writers paste. Power users use Inoreader / Reeder / Miniflux. We win the "where does new OPENGEM stuff appear" question.

## The feeds (18 total)

### Catalog feeds (5)

| Feed | URL | Update |
|---|---|---|
| All forecasts | `/feed/forecasts.atom` | On new forecast vintage |
| All accountability entries | `/feed/accountability.atom` | On new score |
| All methodology changes | `/feed/methodology.atom` | On new methodology version |
| All scenario packs | `/feed/scenarios.atom` | On new scenario release |
| All glossary additions | `/feed/glossary.atom` | On new term added |

### Editorial feeds (5)

| Feed | URL | Update |
|---|---|---|
| Daily digest | `/feed/daily.atom` | Daily 06:00 UTC |
| Weekly retrospective | `/feed/weekly.atom` | Friday 17:00 UTC |
| Quarterly | `/feed/quarterly.atom` | First trading day of new quarter |
| Post-mortems | `/feed/postmortems.atom` | On new post-mortem |
| Editorial picks | `/feed/picks.atom` | On editorial annotation publish |

### Per-entity feeds (4)

| Feed | URL | Example |
|---|---|---|
| Per country | `/country/<iso3>/feed.atom` | `/country/usa/feed.atom` |
| Per indicator | `/indicator/<id>/feed.atom` | `/indicator/cpi-yoy/feed.atom` |
| Per scenario pack | `/scenario/<id>/feed.atom` | `/scenario/2026q3-globe/feed.atom` |
| Per methodology | `/methodology/<id>/feed.atom` | `/methodology/combiner-v4/feed.atom` |

### Top-of-mind feeds (2)

| Feed | URL | Update |
|---|---|---|
| Top of mind (global) | `/feed/top.atom` | Hourly, ranked |
| Top of mind (cohort) | `/feed/top.atom?cohort=g7` | Per cohort |

### Operational feeds (2)

| Feed | URL | Update |
|---|---|---|
| Status / incidents | `/feed/status.atom` | On status change |
| Changelog / releases | `/feed/changelog.atom` | On deploy |

## What an Atom entry looks like

Take the daily digest feed:

```xml
<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>OPENGEM Daily Digest</title>
  <subtitle>Top forecasts and misses, daily.</subtitle>
  <link href="https://opengem.app/" rel="alternate"/>
  <link href="https://opengem.app/feed/daily.atom" rel="self"/>
  <id>tag:opengem.app,2026:feed/daily</id>
  <updated>2026-06-06T06:00:00Z</updated>
  <icon>https://opengem.app/favicon.ico</icon>
  <logo>https://opengem.app/logo.png</logo>
  <generator uri="https://opengem.app">OPENGEM v2.4.1</generator>
  <rights>CC-BY-4.0</rights>

  <entry>
    <title>2026-06-06 daily digest</title>
    <id>tag:opengem.app,2026:digest/2026-06-06</id>
    <link href="https://opengem.app/digest/2026-06-06"/>
    <published>2026-06-06T06:00:00Z</published>
    <updated>2026-06-06T06:00:00Z</updated>
    <summary type="text">Top US CPI release came in hot; OPENGEM nowcast within band; recession-prob unchanged.</summary>
    <content type="html">
      <![CDATA[
        <h2>USA CPI release</h2>
        <p>Actual 3.5% YoY. OPENGEM nowcast 3.32% (within P10-P90 band). Surprise +0.7σ.</p>
        <p><a href="https://opengem.app/indicator/cpi-yoy?countries=usa">View chart</a></p>
        ...
      ]]>
    </content>
    <category term="data-release"/>
    <category term="country:usa"/>
    <category term="indicator:cpi-yoy"/>
  </entry>

  ...more entries...
</feed>
```

Categories are machine-parseable: `country:usa`, `indicator:cpi-yoy`, `type:data-release`, etc. Feed readers can filter.

## Discovery

Every page that has a feed declares it in `<head>`:

```html
<link rel="alternate" type="application/atom+xml"
      title="OPENGEM USA feed"
      href="/country/usa/feed.atom">
```

Inoreader, Feedly, etc. auto-detect.

## RSS 2.0 mirrors

For older readers, every Atom feed has an RSS 2.0 mirror at the same path with `.rss` extension:
- `/feed/daily.atom` (Atom)
- `/feed/daily.rss` (RSS 2.0)

Atom is preferred (better metadata, better dates), but RSS coverage is universal.

## JSON Feed mirrors

For modern readers and LLM consumption:
- `/feed/daily.json` (JSON Feed v1.1)

JSON Feed is much easier for LLM agents to parse than XML.

## Per-cohort feeds

Top-of-mind feed per cohort (G7, G20, EU, etc.):

```
   /feed/top.atom?cohort=g7
   /feed/top.atom?cohort=g20
   /feed/top.atom?cohort=eu
   /feed/top.atom?cohort=watchlist  ← requires auth
```

For authenticated cohorts (watchlist), the URL includes a private token:

```
   /feed/top.atom?token=<feed-token>
```

Feed-tokens are personal and revocable from the user settings.

## Feed limits

| Feed | Items / fetch | Window |
|---|---|---|
| Daily digest | 30 | 30 days |
| Per indicator | 50 | unlimited |
| Per country | 50 | unlimited |
| Top of mind | 50 | rolling |
| Catalog feeds | 100 | unlimited (paginated) |

Pagination via Atom `<link rel="next">` headers.

## Polling cadence

We advertise in feed:

```xml
<sy:updatePeriod>hourly</sy:updatePeriod>
<sy:updateFrequency>1</sy:updateFrequency>
```

Most feeds are hourly. Daily digest is daily.

WebSub / PubSubHubbub for instant push:

```xml
<link rel="hub" href="https://pubsubhubbub.appspot.com/"/>
<link rel="self" href="https://opengem.app/feed/daily.atom"/>
```

Subscribers via WebSub get instant notifications. Most feed readers fall back to polling, which is fine at our scale.

## Feed pages (UI)

Each page that has a feed shows a small RSS button:

```
   [RSS] [Atom] [JSON]   ← in the page toolbar
```

Click → reveals the URL with copy-to-clipboard.

For the catalog of all feeds, a directory page at `/feeds`:

```
   ┌──────────────────────────────────────────────────┐
   │  OPENGEM Feeds                                    │
   │  ────────────────────────────────────────────    │
   │                                                    │
   │  Editorial                                         │
   │   • Daily digest      [RSS] [Atom] [JSON]         │
   │   • Weekly retro      [RSS] [Atom] [JSON]         │
   │   • Quarterly         [RSS] [Atom] [JSON]         │
   │   • Post-mortems      [RSS] [Atom] [JSON]         │
   │   • Editorial picks   [RSS] [Atom] [JSON]         │
   │                                                    │
   │  Catalog                                           │
   │   • All forecasts                                  │
   │   • Accountability                                 │
   │   • Methodology                                    │
   │   • Scenarios                                      │
   │   • Glossary                                       │
   │                                                    │
   │  Top of mind                                       │
   │   • Global, hourly                                 │
   │   • G7                                             │
   │   • G20                                            │
   │   • Per cohort (custom)                            │
   │                                                    │
   │  Per-entity (search to find)                       │
   │   [Search: countries, indicators, ...]             │
   │                                                    │
   │  Operational                                        │
   │   • Status                                         │
   │   • Changelog                                      │
   │                                                    │
   └──────────────────────────────────────────────────┘
```

## OPML export

A user can download an OPML file with all their subscribed feeds:

```
   GET /feeds.opml?token=<feed-token>
```

Paste into Inoreader / Feedly → all OPENGEM feeds added in bulk.

## Substack integration

A Substack writer can paste a feed URL into their newsletter's "RSS" integration. The newsletter automatically includes new OPENGEM entries.

For high-volume writers (paid OPENGEM tier): we offer a customizable digest feed with per-newsletter branding (V2).

## LLM consumption

The MCP server (L177) exposes a tool `feed.subscribe(url)` and `feed.fetch(url)`. Agents can pull the latest entries on demand.

JSON Feed is the preferred format for agents (XML parsing is fragile).

## Feed for podcasts (V2)

V2: a "daily briefing podcast" feed where each entry is a 5-minute AI-generated audio briefing.

```
   /feed/podcast.xml
```

Apple Podcasts / Spotify Podcasts compatible.

V1 — we don't ship this. Audio gen is a serious infra commitment.

## Implementation

- Feed generation: server-side rendered, cached at CDN
- Cache TTL: 5min for hourly feeds, 24h for daily
- Compression: gzip + Brotli
- Size: feeds typically <50KB
- Format: Atom 1.0 (primary), RSS 2.0 + JSON Feed (mirrors)

## Validation

Every feed validated by:
- W3C Feed Validator
- Atom test suite
- Feedly's compatibility check

CI runs validation on every deploy.

## Anti-patterns avoided

- Feed-only premium content. Free tier sees full content in feeds.
- Truncated feeds with "click to read more." Full content in feeds.
- Trackers / ads in feed entries. None.
- Feeds with stale timestamps. We use real `<updated>` dates.

## The asymmetric move

Bloomberg's RSS is unavailable. Stratfor publishes some news as RSS (limited). OPENGEM publishes EVERYTHING:
- Every forecast vintage → feed entry
- Every score → feed entry
- Every methodology change → feed entry
- Every glossary addition → feed entry

A power user with a Reeder subscription becomes a real-time OPENGEM observer without ever opening the dashboard.

Feeds are also how an LLM agent maintains state. An MCP-connected Claude can subscribe to a country's feed, and on each conversation pull the new entries to ground itself in the latest.

## Feed → newsletter pipeline (internal)

The OPENGEM newsletter is generated from the daily-digest Atom feed via a Substack publication. Eats our own dog food.
