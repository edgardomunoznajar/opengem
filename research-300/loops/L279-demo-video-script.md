# L279 — Demo Video Script (90-second narrated walkthrough)

**Loop**: 279 / 300
**Phase**: 6 — Synthesis + launch
**Date**: 2026-06-06

---

## The thesis of this loop

A demo video does one job: it makes a journalist or institutional buyer who skims the homepage in 8 seconds spend 90 seconds with us instead. Within those 90 seconds, the video must (a) establish the thesis ("the cartel won't publish their track record; we will"), (b) show the product working, (c) land on the accountability ledger as the closing image, (d) leave the viewer with a verb ("go to /accountability and audit us").

90 seconds is the length the video must be. Not 60 (too short to land the thesis), not 120 (too long for cold-share retention). At 30 frames per second that's 2,700 frames; at 200 wpm narration that's ~300 words; at 6-7 scenes that's ~12-15 seconds per scene.

The video shoots in one studio session. Edit pass is one week. Captions are baked-in (not SRT). Music is one royalty-free track (Chosic / FreePD) low-mixed under the narration. Voice: founder if confident on-camera; otherwise hired voice talent.

Output files: `opengem-demo-90s.mp4` (1080p), `opengem-demo-90s.webm` (open codec), `opengem-demo-30s.mp4` (highlight cut for social), `opengem-demo-script.md` (this file, archived to the press kit).

---

## The script

### Scene 1 — Cold open (0:00 — 0:08)

**Visual.** Black screen with the Bloomberg-orange amber tile color. Three words appear in JetBrains Mono, one per second:

```
"Forecast."
"Published."
"Accountable."
```

Then fades to the OPENGEM wordmark for one second.

**Narration.** *(beat)* *(beat)* *(beat)*

**Audio.** Music starts under the third word; volume low.

---

### Scene 2 — The problem (0:08 — 0:22)

**Visual.** Quick montage of Bloomberg Terminal, IMF WEO PDF, OECD EO PDF, Stratfor logo, each with a "subscription required" or "behind paywall" lozenge overlay. Quick-cut, 1.5 seconds each. Final frame: a TradingEconomics page with a paywall.

**Narration.** *"The world economy has a forecasting cartel. IMF, OECD, Bloomberg Economics, Stratfor. Their forecasts are priced. Their track records are private. Their margins depend on opacity."*

**Audio.** Music continues; mid-volume; minor-key, restrained.

---

### Scene 3 — The pivot (0:22 — 0:32)

**Visual.** Cut to the OPENGEM home page, full-screen. Camera zooms slowly across the World Pulse hero strip. Six tiles animate their sparklines in sequence.

**Narration.** *"OPENGEM has no margins to protect. So we publish what they cannot — every forecast, every vintage, every miss."*

**Audio.** Music shifts to major key.

---

### Scene 4 — Show the product, fast (0:32 — 1:00)

**Visual.** Four quick page-tour cuts, ~7 seconds each:

1. **0:32 — Country page.** Pan across USA country page. Hover one situation tile; the sparkline expands. Cursor moves to the forecast table; one row highlights showing OPENGEM + WEO + OECD numbers side-by-side. *Narration: "Every country. Every indicator. Every forecast with bands and consensus overlays."*

2. **0:39 — Forecast detail.** Quick zoom into the forecast detail page bands chart. The chart shows P10/P50/P90 bands, with the WEO and OECD overlay lines. Cursor clicks the "methodology" pop-up; it opens showing the model card. *Narration: "Click any forecast. Click any chart. The methodology is one click away. No black box."*

3. **0:46 — Vintage time machine.** A page with a vintage scrubber. The cursor drags it back to September 2024. The chart updates showing what OPENGEM was predicting at that date. *Narration: "Rewind to any date. See exactly what we were predicting. Nothing is retroactively rewritten."*

4. **0:53 — MCP grounding.** A Claude Desktop conversation window. User types: "What's the consensus for German GDP growth in 2027?" Claude responds with a grounded answer that includes "[According to OPENGEM]" with a clickable cite-this-view URL. *Narration: "Use it from any LLM. Open MCP server. Free."*

**Audio.** Music builds gently through this section.

---

### Scene 5 — The accountability ledger (1:00 — 1:18)

**Visual.** This is the most important shot. Cut to `/accountability`, full-screen. Camera pans down slowly:

- Four-tile scoreboard: 14,283 forecasts published; 11,902 scored; 2,117 outside band; 264 pending.
- The recent-misses table appears row by row. Each row shows country, indicator, forecast vs actual, miss size, and a "post-mortem" link.
- The cursor clicks one post-mortem link; the post-mortem page opens; visible at the top is the country + indicator + forecast vintage + the words "What we got wrong" as a heading.

**Narration.** *"Every miss we have ever made is named, in the same place as the original forecast, with a post-mortem. This is the page that does not exist anywhere else."*

**Audio.** Music plateaus; the narration carries.

---

### Scene 6 — The promise (1:18 — 1:26)

**Visual.** The five promises page (`/why-different`). Five lines appear one at a time in JetBrains Mono:

```
We publish every forecast we ever make.
We name every miss.
We open every methodology.
We cite every number.
We embed, export, and expose everything.
```

**Narration.** *"Five promises no closed competitor can match. Apache-2.0 code. CC-BY-4.0 data. Free tier holds the whole product. Paid tier is for velocity, never substance."*

**Audio.** Music swells slightly.

---

### Scene 7 — The call to action (1:26 — 1:30)

**Visual.** Cut to a clean wordmark + URL + tagline. White on near-black.

```
OPENGEM
opengem.com / accountability

The macro accountability ledger.
Audit us.
```

**Narration.** *"Go to opengem.com slash accountability. Audit us. The data is open."*

**Audio.** Music fades on the word "open."

---

### End card (1:30 — fade)

Static wordmark + URL + tiny line of attribution copy:

```
Apache-2.0 + CC-BY-4.0  ·  opengem.com  ·  Made by a single founder + an open community.
```

Two seconds of static; fade to black.

---

## Production notes

### Voice

- **First choice**: founder voice if confident on-camera, even with mild accent. Authenticity carries.
- **Second choice**: a calm, mid-register voice (think NPR style, not advertising style). No upspeak. No vocal fry. Female or male, doesn't matter; deeper register reads as more authoritative for financial audiences, but the founder's actual voice always beats a hired voice for trust.

### Pacing

- Narration is *under* the visual, never over. The visuals do the heavy lifting; narration provides anchor sentences.
- ~300 words across 90 seconds = 200 WPM. That's noticeably slower than conversational; it gives time for the visual to land. We deliberately under-pace.
- Three explicit beats: one at end of Scene 2 ("opacity"), one at end of Scene 5 ("anywhere else"), one at end of Scene 6 ("substance"). Each ~0.5s pause. These are the emotional landings.

### Visual rhythm

- Scenes 1, 2, 6, 7 are full-screen text or static frames (low cognitive load).
- Scenes 3, 4, 5 are product UI footage (high information density).
- Alternation: text → UI → text → UI → text. Lets the viewer rest between dense product shots.

### Color

- The OPENGEM amber (Bloomberg-orange) is the only saturated color in the video. Everything else is grayscale or near-grayscale. This means our brand color reads as the *signal* throughout — it's the answer to where to look.

### Music

- Royalty-free, ambient, minor → major shift between Scene 2 and Scene 3.
- Chosic.com or FreePD are the source. Anything by Chris Zabriskie tends to work.
- Volume: -15dB under narration; ducked further during the explicit beats.
- No copyrighted music. No "free" music with restrictive license. The video has to be redistributable as part of the press kit.

### Captions

- Baked-in to the video file as a separate track is *not* sufficient because press CMSes strip tracks. Captions are rendered into the visual layer.
- Caption styling: white text, semi-transparent black box, JetBrains Mono Bold at ~28px equivalent for 1080p.
- Position: bottom third, never overlapping with the most-important visual element on screen.

### Accessibility

- The 90-second cut and the 30-second cut both ship with audio descriptions for visually-impaired viewers (separate audio track, not baked-in). Audio description is 60 seconds; describes the visual flow for someone who can't see the product UI footage.
- Transcripts ship as `opengem-demo-transcript.md` in the press kit, full sentence-level with timestamps.

---

## The 30-second highlight cut

A separate edit, ~30 seconds, for Twitter / LinkedIn / TikTok-style social posts. Includes only:

1. Scene 1 cold open, abbreviated (3 seconds).
2. Scene 3 pivot, the OPENGEM home page reveal (5 seconds).
3. Scene 5 accountability ledger, the close-up of the misses table (12 seconds).
4. Scene 7 call to action (10 seconds).

Narration is a single sentence: *"OPENGEM. The macro forecast dashboard that publishes its own mistakes. Open data. Apache-2.0 code. Free. Audit us at opengem dot com."*

This cut is shareable independently; the 90-second cut is the full press-kit asset.

---

## Distribution plan for the demo video

- **OPENGEM home page**: 30s autoplay (muted) hero loop; click-to-watch full 90s.
- **ProductHunt launch**: 90s video as the primary asset.
- **Show HN**: linked in the first comment as "demo video, 90s."
- **Substack mirror**: embedded in the launch post.
- **YouTube**: uploaded as a public video, link in the home page footer. Comments enabled.
- **Twitter / X**: 30s cut as a native video upload (not a link, because Twitter penalizes external links).
- **LinkedIn**: 30s cut + a thread description.
- **Reddit**: 30s cut on r/macroeconomics, r/datasets, r/Economics. Linked from a community member, not founder.

---

## What this loop produced

- A 90-second video script with seven named scenes, narration text per scene, visual choreography per scene, audio cues, total word count ~300.
- Production notes covering voice choice, pacing, visual rhythm, color, music, captions, accessibility.
- A separate 30-second highlight cut script.
- A distribution plan across home page, ProductHunt, HN, Substack, YouTube, Twitter, LinkedIn, Reddit.
- Output files specified: `opengem-demo-90s.mp4`, `opengem-demo-90s.webm`, `opengem-demo-30s.mp4`, transcript Markdown, audio description audio file.

## What comes next

- Founder + an editor produce the actual video in one studio session + one edit pass.
- **L278** — press kit includes the rendered video.
- **L277** — launch plan W 0 + W+1 deploy the video across channels.

## Related

- [[L008-differentiation]] — the five promises drive the script
- [[L277-launch-plan]] — distribution channels using this video
- [[L278-press-kit-screenshots]] — kit containing the rendered file
- [[L285-accountability-ledger]] — the page Scene 5 features
