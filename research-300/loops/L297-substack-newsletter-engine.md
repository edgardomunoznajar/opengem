# L297 — Substack / newsletter engine plan

**Loop**: 297 / 300
**Phase**: 6 — Synthesis + launch
**Date**: 2026-06-06

---

## The thesis

OPENGEM runs a **single weekly newsletter** as both a content channel and a "soft conversion to paid" funnel. The newsletter is free; it links to the dashboard for the canonical version of every chart; the only Pro-tier upsell is "want the daily digest? upgrade to Pro $29/mo."

The newsletter platform is **Substack at launch** for distribution reach + builds-in cross-cite from other macro Substacks (per L291 partnerships). It migrates to self-hosted (Buttondown or a small custom mailer) once the list hits 2k subscribers and we want the email-list ownership.

## Weekly newsletter format

**Title**: *Vintage* — published Sunday evenings UTC.

**Length**: ~1,200–1,800 words. Five fixed sections:

### 1. The number of the week (200 words)

One concrete numeric anchor — a forecast revision, a scenario that triggered, a nowcast that moved. Cited with vintage_id and link to the canonical page.

### 2. What we got wrong (300 words)

If any forecasts scored in the past week landed outside their 80% band, we name the miss, link to the post-mortem (per L286/L298), and give a 2-paragraph "what we learned." If no misses scored that week, we instead link to the open ledger and remind readers we'll cover them when they do.

This section is the editorial signature. It anchors the newsletter to the "publishes its mistakes" promise.

### 3. The chart that explains it (300 words)

One chart — picked from the week's scenarios or forecast revisions — annotated with context. Vega-Lite spec link so other macro Substack-ers can fork.

### 4. What we're watching (300 words)

Three scenarios with rising probability over the past week. Brief reasoning. Pointers to the trigger conditions for each.

### 5. From the inbox (100 words)

One reader question or external citation — short, conversational. Builds community.

### Footer — always the same

- "All forecasts in this email are vintage-stamped. Replay them at opengem.org/vintage/[date]."
- "Want the daily digest? Upgrade to Pro: opengem.org/pricing."
- "Apache-2.0 + CC-BY-4.0. Cite freely."

## Editorial cadence

- **Drafted Friday**, sent Sunday 8pm UTC.
- **One editor (Edgardo at v1)** — single-voice newsletter, no ghostwriters.
- **No skipped weeks.** If absent, the newsletter ships an "auto-digest" generated from the dashboard's weekly summary. The reader still gets something.
- **Quarterly retrospective newsletter** (per L299) — replaces a normal newsletter once per quarter.

## Substack-specific tactics

- **Cross-posts** via Substack's note system to macro Substack adjacent communities (Joey Politano's, Conor Sen's, Tracy Alloway's, Adam Tooze's, Cardiff Garcia's audiences).
- **Comment ecosystem**: every newsletter has comments open; replies count for both engagement and editorial-feedback intake.
- **Substack Mailbag**: enable replying-to-email-creates-comment for paid subscribers.
- **No Substack-paid subscription**. Keep Substack as a free distribution channel only. Paid tier lives on opengem.org.

## Email list ownership migration

At 2k subscribers we migrate from Substack-hosted to self-hosted (Buttondown $9/mo + Substack cross-post for new-subscriber acquisition). This is a cost / ownership / SEO move:

| Factor | Substack | Self-hosted |
|---|---|---|
| Email list ownership | Limited (Substack owns subscriber relationship via their app) | Full |
| SEO | Decent | Excellent (drive traffic to opengem.org directly) |
| Cost | Free | $9/mo |
| Cross-cite by other Substack-ers | Easy | Slightly harder |
| Migration cost | One-time export + reimport | — |

The migration is at 2k subscribers because that's roughly when the list becomes a strategic asset worth controlling.

## What this loop produced

- Weekly newsletter format (5 fixed sections + always-the-same footer)
- "What we got wrong" as the editorial signature
- Substack-at-launch + migration-to-self-hosted at 2k
- The "no skipped weeks" discipline + auto-digest fallback

## Related

- [[L007-distribution-thesis]] — newsletter is channel 4 of 6
- [[L008-differentiation]] — "publishes its mistakes" mirrored in the newsletter
- [[L286-failure-log-page]] — post-mortem pages the newsletter links to
- [[L298-postmortem-template]] — the format
- [[L299-quarterly-retrospective-template]] — the quarterly companion
