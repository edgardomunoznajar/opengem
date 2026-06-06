# L295 — YouTube content engine plan

**Loop**: 295 / 300
**Phase**: 6 — Synthesis + launch
**Date**: 2026-06-06

---

## The thesis

YouTube is OPENGEM's **most underrated distribution channel** because the founding use case (per OPENGEM README) is supporting a YouTuber friend's macro+geopolitics content workflow. The dashboard already produces JSON the friend pastes into ChatGPT for narrative — wrapping that workflow as a *generalized* YouTube content engine multiplies it from 1 user to 1000.

But the YouTube engine is **not OPENGEM's own channel**. It's a *tool* + *partnership pattern* that lets multiple creators produce OPENGEM-grounded content. This avoids two traps: (1) us becoming a content company, (2) us depending on a single creator for distribution.

## The four content engine surfaces

### 1. JSON-paste workflow (already exists, refine for v1)

The friend's existing flow:
- Open daily digest URL
- Skim situation indicators
- Pick a scenario / forecast
- Copy JSON block
- Paste into ChatGPT with OPENGEM system prompt (per L198)
- Get 3-paragraph video segment grounded in real numbers

Refinements at v1:
- "Copy as ChatGPT prompt" button on every scenario page (not just JSON; includes the system prompt automatically)
- "Copy as Claude prompt" alternative with MCP-tool-call syntax
- Saved-prompt history (server-side for paid users)

### 2. B-roll generator (per L113)

Static images or short MP4 animations of charts that creators can drop into video timelines:
- `https://opengem.org/b-roll/forecasts/USA/gdp_yoy/4q.png` — chart at the current vintage as PNG
- `https://opengem.org/b-roll/forecasts/USA/gdp_yoy/4q.webm` — 5-second zoom-pan animation
- `https://opengem.org/b-roll/scenarios/<slug>/probability.gif` — animated probability fan

Generated server-side via Playwright `screenshot()` + `recordVideo()` (per L116 tearsheet pattern). Cached at the CDN.

Spec-style URL grammar:
```
/b-roll/<entity>/<id>/<view>[.png|.webm|.gif]?[theme=editorial-pink]&[dim=1920x1080]
```

### 3. "Topic of the week" scripted segments

Every week we publish:
- A 90-second teleprompter script tied to one OPENGEM scenario or forecast that's news-relevant
- Companion slides (Markdown + reveal.js style)
- 3-5 b-roll links

The teleprompter is CC-BY-4.0 licensed. Any creator can use it verbatim with attribution. The competitive moat is that OPENGEM has the freshest, most-defensible numeric anchors.

### 4. Creator-tier API

A paid tier specifically for video creators (Pro $29/mo or higher) with:
- Higher-resolution b-roll exports
- Custom-themed b-roll (channel branding)
- Watermark removal on b-roll
- Bulk API access for batch script generation
- Discord channel with other OPENGEM-grounded creators

## Distribution economics

| Resource | Cost to OPENGEM | Value to creator | Creator's audience |
|---|---|---|---|
| JSON paste workflow | $0 (already exists) | Replaces "I had to make this up" | Per video |
| B-roll PNG/MP4 | Cached at CDN; ~$0.001/render | Replaces stock-photo subscription + own chart-making | Per video |
| Weekly teleprompter | 1 hour writing/wk | Replaces 1-2 hours of research per video | Recurring |
| Creator-tier API | Pro tier upgrade ($29/mo) | Reaches 100+ creators by Y2 | 100x amplification |

The leverage: a single creator with 50k subscribers using OPENGEM b-roll once per week ≈ 200k impressions/month of OPENGEM attribution. Twenty such creators ≈ 4M impressions/month.

## What we explicitly will NOT do

- **OPENGEM doesn't run its own YouTube channel.** That competes with our creator partners.
- **No paid sponsorship deals with creators.** That distorts the editorial neutrality.
- **No "OPENGEM exclusive" content arrangements.** Anyone can use the b-roll under CC-BY-4.0.

## The cooperative-content discipline

We publish:
- The teleprompter script (CC-BY-4.0)
- The b-roll (CC-BY-4.0 via the dashboard CDN)
- A "Featured creators using OPENGEM" page (per the L291 partnership model — non-monetary mutual attribution)

We do **not** publish:
- Our own videos competing with creators
- Edit suggestions that constrain creator voice
- Embargo windows or "first publication rights"

## What this loop produced

- The 4-surface YouTube engine (JSON workflow + b-roll + weekly script + creator tier)
- The "OPENGEM doesn't run its own channel" guardrail
- The distribution economics: 20 creators ≈ 4M impressions/month
- The CC-BY-4.0 cooperative-content discipline

## Related

- [[L113-youtube-broll-generator]] — implementation spec for b-roll
- [[L007-distribution-thesis]] — YouTube is channel 3 of 6
- [[L116-print-grade-svg-tearsheets]] — adjacent rendering tech
- [[L297-substack-newsletter-engine]] — sibling channel logic
