# L278 — Press Kit + Screenshots

**Loop**: 278 / 300
**Phase**: 6 — Synthesis + launch
**Date**: 2026-06-06

---

## The thesis of this loop

A press kit is the *single artifact a journalist asks for* when they cover OPENGEM. If we have one and it's good, the story comes out faster, looks better, and includes our framing rather than their guess. If we don't have one, the journalist either skips us or writes about us with wrong numbers, wrong dates, and a screenshot pulled from a slow page-load. This loop specifies the kit, the screenshots, the GIFs, the demo video file, the headline-copy sketches, and the naming convention.

Press kits are downloaded *once*. They need to work offline, in any country, on any device, in any newsroom CMS. ZIP file, predictable filenames, no DRM, generous licenses.

Press kit lives at `opengem.com/press` (HTML index) with a single `OPENGEM-press-kit.zip` download (~80 MB compressed). Mirror at GitHub releases for archival.

---

## The kit, asset by asset

### Logos (5 files)

| File | Purpose | Dimensions |
|---|---|---|
| `logo/opengem-wordmark.svg` | Primary wordmark, all colors as CSS vars | vector |
| `logo/opengem-wordmark-light.png` | For dark backgrounds | 1200×400, transparent |
| `logo/opengem-wordmark-dark.png` | For light backgrounds | 1200×400, transparent |
| `logo/opengem-mark-only.svg` | The standalone mark (G with amber lozenge) | vector |
| `logo/opengem-favicon.svg` | Favicon source | 32×32 |

License: CC-BY-4.0 with the additional permission to remove attribution when used by journalists in coverage of OPENGEM.

### Screenshots (12 PNG files)

All screenshots taken at 2880×1800 (Retina-ready); auto-downsized to 1440×900 web versions; both included.

| File | Page | Purpose |
|---|---|---|
| `screenshots/home-pulse.png` | `/` | Hero — six situation tiles + scenarios + forecast strip |
| `screenshots/country-USA.png` | `/countries/USA` | Country page with situation tiles + forecast table |
| `screenshots/country-IND.png` | `/countries/IND` | Emerging-market example |
| `screenshots/indicator-CPI-cross-country.png` | `/indicators/cpi_yoy` | Cross-country indicator view |
| `screenshots/scenario-recession.png` | `/scenarios/recession-soft-landing` | Scenario detail |
| `screenshots/forecast-USA-GDP-4Q.png` | `/forecasts/USA/gdp_yoy/4Q` | Forecast with bands + consensus overlay |
| `screenshots/leaderboard.png` | `/leaderboard` | OPENGEM vs WEO vs OECD vs RW/AR(1) |
| `screenshots/accountability-ledger.png` | `/accountability` | THE differentiator screenshot |
| `screenshots/postmortem-example.png` | `/postmortem/usa-gdp-2025q2` | A real post-mortem |
| `screenshots/mcp-install.png` | `/mcp` | MCP install snippets |
| `screenshots/methodology-dfm.png` | `/methodology/dfm-l3-bma` | Model card example |
| `screenshots/pricing.png` | `/pricing` | The "we never charge for X" block |

The most important screenshot is `accountability-ledger.png`. Journalists cropping a single image to illustrate the OPENGEM story will almost always crop this one. We optimize the screenshot specifically for that crop: the four-tile scoreboard + the recent-misses table is the headline image of every press piece.

### GIFs (5 animated files)

Format: APNG (transparent background) for portability; MP4 H.264 backup for legacy CMS.

| File | Purpose | Duration |
|---|---|---|
| `gifs/home-pulse-hover.apng` | Mousing over the home pulse tiles; sparklines animate on hover | 8s |
| `gifs/vintage-rewind.apng` | Using the vintage time-machine to rewind to Sept 2024 | 10s |
| `gifs/forecast-bands-zoom.apng` | Zooming into a forecast bands chart with consensus overlay | 8s |
| `gifs/accountability-scroll.apng` | Scrolling through the accountability ledger | 12s |
| `gifs/mcp-claude-grounding.apng` | A Claude conversation grounding in OPENGEM via MCP | 15s |

GIFs are limited to 12 MB each to ensure they autoplay smoothly on social feeds.

### Demo video (1 MP4, 90 seconds)

The L279 demo video script is shot, edited, and rendered as `video/opengem-demo-90s.mp4` (H.264, 1080p, 8 Mbps, ~80 MB). Plus a 30-second highlight cut as `video/opengem-demo-30s.mp4` for social posts.

Captions are baked-in (not as SRT) because press CMSes often strip caption tracks. EN-only at launch; ES + FR + DE captions added Y1.

### Founder portrait + bio (2 files)

| File | Purpose |
|---|---|
| `team/founder-portrait.jpg` | Professional headshot, 1200×1200, CC-BY-4.0 |
| `team/founder-bio.md` | 50-word, 100-word, 200-word bio versions |

Single founder at launch. If more team members join pre-launch, kit updates. Bio leads with "Edgardo built OPENGEM after watching the cartel hide its track record for the last decade. Background in [credentials]."

### Boilerplate copy (1 Markdown file)

`boilerplate.md` contains pre-approved copy blocks at three lengths (50 / 150 / 300 words) journalists can use directly:

```
50 words:
OPENGEM is the public macro-accountability ledger for the world economy — a
Bloomberg-grade dashboard for everyone, where every forecast is open, every
number is dated, and every miss is named. Apache-2.0 code; CC-BY-4.0 data;
free tier holds the whole product.

150 words:
[The 50-word version, plus]
The forecasting cartel — IMF, OECD, Bloomberg Economics — produces priced
forecasts whose track records are private. OPENGEM operates the opposite
model: every vintage of every forecast we have ever made is published with
the date we made it, the methodology that made it, and the score it earned
against reality. When we miss, the post-mortem appears on the same URL as
the original forecast. The accountability ledger at /accountability is the
page that does not exist anywhere else in the industry.

300 words:
[The 150-word version, plus the five promises from L008 in compressed
form, the three-cohort thesis, and the founder's one-line motivation.]
```

### Headline sketches (1 Markdown file)

`press-headlines.md` lists 12 candidate headlines we'd like to see, organized by outlet style:

```
Bloomberg / FT macro column style:
- "The open-source dashboard that wants to grade the IMF"
- "OPENGEM publishes its forecasting misses. The cartel won't."
- "A guerrilla-developer is building the macro Bloomberg for everyone"

Reuters / WSJ news style:
- "Macroeconomic forecasting moves toward radical transparency"
- "Open dashboard challenges incumbents on track-record disclosure"

Tech press (Wired / Verge / TechCrunch) style:
- "OPENGEM is the open Bloomberg-killer that publishes its own mistakes"
- "Why this developer wants every macroeconomic forecast to come with a
  receipt"
- "LLMs already cite OPENGEM. Now Bloomberg has to compete."

Academic / Substack style:
- "What happens when forecast accountability becomes a public good?"
- "OPENGEM and the end of opacity-arbitrage in macroeconomics"

Aspirational long-shot:
- "The Wikipedia of macroeconomic forecasting just shipped"
- "OPENGEM joins the IMF and OECD as a forecast benchmark — and beats them
  on transparency"
```

These are not for OPENGEM to write or pitch. They are for journalists to riff on. The exercise of writing them sharpens our internal sense of the brand.

### Press contact (1 vCard)

`press-contact.vcf` — vCard with founder's press email + Signal handle for journalists who want to chat off-record. The press email is dedicated (`press@opengem.com`) and routes to founder with a 24h SLA for press inquiries (24h Mon-Fri; 72h weekends and holidays).

---

## Naming convention

All files follow `[category]/[asset-id].[ext]`:

- `logo/opengem-wordmark.svg`
- `screenshots/home-pulse.png`
- `gifs/vintage-rewind.apng`
- `video/opengem-demo-90s.mp4`

No version numbers in filenames (versions are tracked via the press-kit git tag). No "FINAL", no "v2", no spaces, no uppercase. Press kit version in the README: `OPENGEM-PRESS-KIT-2026-Q3-v1.0`.

Inside the ZIP:

```
OPENGEM-press-kit/
├── README.md                  ← what's in here + license
├── boilerplate.md             ← 50/150/300-word descriptions
├── press-headlines.md         ← 12 candidate headlines
├── press-contact.vcf          ← vCard
├── logo/                      ← 5 files
├── screenshots/               ← 12 PNG files (2880×1800 + 1440×900)
├── gifs/                      ← 5 APNG + 5 MP4 backups
├── video/                     ← 90s + 30s MP4
└── team/                      ← founder portrait + bio
```

---

## License language

All assets are CC-BY-4.0 unless noted. The `README.md` inside the ZIP says:

```
These assets are released under CC-BY-4.0 (Creative Commons Attribution 4.0
International). You may use them in coverage, derivative works, and
educational materials with attribution to OPENGEM and a link back to
opengem.com.

Specifically permitted without further request:
- Use in news articles, books, blog posts, podcasts, videos
- Cropping, resizing, recoloring
- Translating bio + boilerplate text

Specifically requested (not required):
- Tell us when you publish so we can add the citation to our press page.
- press@opengem.com

The OPENGEM wordmark and mark may be used to identify our project in
coverage. They may not be used as your product's identifier.

Apache-2.0 license applies to the underlying OPENGEM code (separately).
```

---

## What this loop produced

- A press kit asset list (logos × 5, screenshots × 12, GIFs × 5, demo video, founder bio, boilerplate, headlines, vCard).
- Dimensions, naming convention, license language.
- The "most important screenshot" identified: `accountability-ledger.png`, optimized for journalist crop.
- 12 candidate press headlines for internal calibration.
- A single ZIP at `opengem.com/press` + GitHub release mirror.

## What comes next

- **L279** — demo video script that produces `video/opengem-demo-90s.mp4`.
- **L277** — launch plan uses press kit assets at W 0 and W+1.
- **L283** — ToS draft confirms the CC-BY-4.0 commitment on assets.

## Related

- [[L008-differentiation]] — the five promises drive the screenshot and boilerplate selection
- [[L277-launch-plan]] — channels using these assets
- [[L279-demo-video-script]] — the video script behind `opengem-demo-90s.mp4`
- [[L285-accountability-ledger]] — the page producing the most important screenshot
