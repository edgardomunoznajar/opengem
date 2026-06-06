# L229 — Sentiment / News Tone Page

**Loop**: 229 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The thesis of this loop

Tone matters more than ever, and **tone is now free data**. GDELT 2.0's Global Knowledge Graph (GKG) records every monitored news event, scored on the Goldstein scale (cooperation -10 ↔ conflict +10), tone (positive/negative), themes (50+ categories from POLITICS to ECONOMY to PROTEST), and locations — refreshed every 15 minutes. The Caldara-Iacoviello **GPR** (Geopolitical Risk Index) builds on a similar substrate. EPU (Economic Policy Uncertainty) does the same for policy-specific terms. And — distinctively for OPENGEM — the **Trump-vintage / political-rhetoric layer** is a unique opportunity: the 2024-2028 era is producing measurable shifts in *who-says-what* that drive currency vol, equity drawdowns, and sovereign-spread moves. No public dashboard tracks "executive-rhetoric-vintage" against macro markets.

OPENGEM's sentiment page does what Stratfor's narrative team does, but with *numbers*: maps the news pulse, tracks rhetoric shifts, and joins to macro market response. It is the page that, when the US president posts something that moves Mexico's peso 2%, becomes the *receipt* — here is the tone vector, here is the historical pattern of similar posts, here is the implied market response. It is the page that, when GDELT spikes for "PROTEST" + "ENERGY" in three EU countries, surfaces the macro tail risk before it shows up in spreads.

This loop **decides** the page structure (tone time series + GPR / EPU overlays + rhetoric tracker + macro response), the GDELT integration depth, and the Trump-vintage / political-rhetoric methodology.

## The four panels

1. **Global tone heatmap** — GDELT GKG-derived tone score by country, daily.
2. **GPR / EPU country indices** — Caldara-Iacoviello GPR + Baker-Bloom-Davis EPU per country.
3. **Rhetoric tracker** — named-leader rhetoric vintage (with the Trump-vintage layer as flagship), tone over time, market response.
4. **Macro response panel** — for each tone shock, the joint move in FX / equity / spread.

## Page structure (top to bottom)

```
┌──────────────────────────────────────────────────────────────────────┐
│ SENTIMENT / NEWS TONE                                                │
│ GDELT GKG + GPR + EPU + rhetoric vintage.                            │
└──────────────────────────────────────────────────────────────────────┘

[Tabs]
 [Global heatmap]  [GPR / EPU]  [Rhetoric tracker]  [Macro response]

╔══════════════════════════════════════════════════════════════════════╗
║ GLOBAL TONE HEATMAP                                                   ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ World map: tone by country ───────────────────────────────────────┐
│  Choropleth: 30-day average tone (GDELT GKG Avg Tone)               │
│  Color: red (negative tone) → white (neutral) → green (positive)    │
│  Hover: tooltip with current tone + 30d Δ + top themes              │
│                                                                      │
│  Toggle theme: ECONOMY / SECURITY / POLITICS / PROTEST / DEFAULT     │
│   Filter restricts heatmap to articles tagged with that theme.      │
│                                                                      │
│  Time slider: 2015 → 2026, hourly granularity                       │
└─────────────────────────────────────────────────────────────────────┘

┌─ Tone time series per country ─────────────────────────────────────┐
│  Y: tone score (-10 ↔ +10)                                          │
│  X: 2018 → 2026 daily                                                │
│  Line: 30-day rolling avg tone                                      │
│  Band: ±1σ                                                          │
│  Annotations: elections, conflicts, central-bank events             │
│  Multi-country overlay: select 4 countries to compare                │
└─────────────────────────────────────────────────────────────────────┘

┌─ Top themes by country (per 30d) ──────────────────────────────────┐
│  Stacked bar showing theme share of mentions per country             │
│  Reveals: what is the world *talking about* in this country         │
│  Example: BRA — currently 35% POLITICS, 25% ECONOMY, 15% CRIME,     │
│   10% ENERGY, 15% other                                              │
└─────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════╗
║ GPR / EPU PANEL                                                       ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Cross-country GPR + EPU grid ─────────────────────────────────────┐
│ Country │ GPR z │ EPU z │ Δ 30d │ Δ 90d │ Drivers              │
│ USA     │ +1.4  │ +1.8  │ +0.3  │ +0.6  │ trade-policy uncertainty │
│ CHN     │ +0.8  │ +1.2  │ +0.2  │ +0.4  │ US-China relations      │
│ DEU     │ +1.1  │ +1.5  │ +0.4  │ +0.7  │ Ukraine, energy         │
│ UKR     │ +4.5  │ +3.8  │ -0.1  │ -0.3  │ ongoing war             │
│ TUR     │ +1.8  │ +2.1  │ +0.3  │ +0.5  │ Med tension              │
│ KOR     │ +1.4  │ +1.6  │ +0.2  │ +0.4  │ PRK, US trade            │
│ TWN     │ +2.6  │ +2.4  │ +0.3  │ +0.5  │ PRC posture              │
│ ISR     │ +3.5  │ +2.8  │ -0.1  │ -0.3  │ Gaza                    │
│ ...                                                                  │
└─────────────────────────────────────────────────────────────────────┘

┌─ GPR time series + spike detector ─────────────────────────────────┐
│  Country: USA selected                                              │
│  GPR plotted 2000-2026                                              │
│  Spike thresholds: +2σ marked with red triangles                    │
│  Notable spikes: 9/11, 2003 Iraq, 2008 GFC, 2020 COVID, 2022 UKR,  │
│   2023 GAZ, 2024 election, ...                                       │
└─────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════╗
║ RHETORIC TRACKER                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Named-leader rhetoric layer ──────────────────────────────────────┐
│  Selectable leaders:                                                │
│   - Trump (US, 2025-2029) — Trump-vintage flagship                  │
│   - Xi Jinping (CHN)                                                │
│   - Putin (RUS)                                                     │
│   - Modi (IND)                                                      │
│   - Lula (BRA)                                                      │
│   - Erdoğan (TUR)                                                   │
│   - AMLO successor (MEX)                                            │
│   - Plus ECB / Fed / BoE / BoJ chairs (monetary policy tone)         │
│                                                                      │
│  Per leader: speech / X-post / interview corpus, scored on:         │
│   - Tone (sentiment)                                                │
│   - Hawkishness (for monetary leaders)                              │
│   - Trade-rhetoric escalation (for executive leaders)               │
│   - Country-target frequency (who is mentioned how often)            │
└─────────────────────────────────────────────────────────────────────┘

┌─ Trump-vintage rhetoric tracker (flagship) ────────────────────────┐
│ ─────────────────────────────────────────────────────────────────── │
│  Date       │ Post / Speech excerpt           │ Tone │ Target │ ΔFX │
│  2026-06-05 │ "Mexico isn't doing enough..."  │ -7.2 │ MEX    │-1.8%│
│  2026-06-04 │ "Tariffs on China increased..." │ -8.4 │ CHN    │-0.5%│
│  2026-06-02 │ "EU is treating us unfairly..." │ -6.8 │ EU     │-0.7%│
│  2026-05-30 │ "Powell should cut now..."      │ -5.1 │ Fed    │+0.3%│
│  ...                                                                 │
│                                                                      │
│  Aggregate metrics:                                                 │
│   30-day avg tone:         -6.5 (vs 2017-2021 avg -4.9)              │
│   Per-target frequency: MEX 18, CHN 24, EU 15, Fed 12, ...           │
│   Escalation index: 0.78 (high)                                      │
│                                                                      │
│  Trend line: 1y rolling avg of tone, by target                       │
└─────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════╗
║ MACRO RESPONSE PANEL                                                  ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Tone shock × market response scatter ─────────────────────────────┐
│  For each tagged tone event in last 12m, plot:                      │
│   X = tone shock magnitude (z-score of single-day tone deviation)   │
│   Y = same-day market response (FX / equity / spread)               │
│                                                                      │
│  Reveals: which tone shocks moved markets, which didn't.            │
│  Used for calibration: how big a tone move needs to be to be tradeble│
│                                                                      │
│  Per country: separate scatter for MXN, CNY, EUR, etc.              │
└─────────────────────────────────────────────────────────────────────┘

┌─ Implied vol around tone events ───────────────────────────────────┐
│  For "rhetoric shock" events (tone < -8 in single day), the page    │
│   computes mean implied-vol jump in FX / equity for 1d, 5d, 30d    │
│   post.                                                              │
│                                                                      │
│  Example finding (Trump-vintage):                                   │
│   - MXN 1d vol after a tone <-7 Trump post: +180bp avg              │
│   - MXN 5d vol: +120bp avg                                           │
│   - MXN 30d vol: +40bp avg                                           │
│                                                                      │
│  This is the *tradeable* signal: rhetoric → vol is measurable.       │
└─────────────────────────────────────────────────────────────────────┘
```

## The Trump-vintage / rhetoric methodology

The "rhetoric vintage" layer is the page's *distinctive* contribution. It works as follows:

1. **Corpus**: continuously scrape declared leaders' public speech (Truth Social, X, official statements, press conferences, prepared speeches).
2. **Scoring**:
   - **Tone**: BERT-derived sentiment + custom-fine-tuned model for political speech.
   - **Target detection**: NER + entity-resolution to identify which countries / institutions are mentioned.
   - **Escalation index**: rolling measure of how *new* the rhetoric is vs the leader's prior baseline.
   - **Action-words detector**: detect threats of specific policy actions (tariff, sanction, withdrawal).
3. **Aggregation**: per-day rolling tone + per-target frequency.
4. **Macro join**: align each post / speech timestamp with intra-day FX / equity / spread response, compute event-study betas.

The Trump-vintage layer is the *first* implementation — but the framework generalizes: any leader's public speech feeds the same pipeline. By 2027 OPENGEM tracks 12-15 named leaders + the major central bank chairs.

The methodology is fully **open** — the prompts, the models, the alignment code are all in `opengem-rhetoric` (new package). The accusations of bias are *mitigated* by transparency, not by hiding.

## Data sources / adapter dependencies

| Input | Source | Adapter | Status |
|---|---|---|---|
| GDELT GKG (tone, themes, events) | GDELT 2.0 | `opengem-data-gdelt` ⚠️ NOT YET BUILT (in roster) | gap |
| Caldara-Iacoviello GPR | replication website | `opengem-data-gpr` ✅ (in roster) | partial |
| EPU (Baker-Bloom-Davis) | policyuncertainty.com | `opengem-data-epu` ⚠️ NOT YET BUILT | gap |
| Truth Social / X scraping | direct (subject to ToS) | `opengem-data-ts-x` ⚠️ NOT YET BUILT | gap |
| Leader corpus archives | official .gov + miller-center.org | `opengem-data-leader-corpus` ⚠️ NOT YET BUILT | gap |
| Sentiment models | open-source BERT + custom fine-tune | `opengem-sentiment-models` ⚠️ NOT YET BUILT | gap |
| FX intra-day | as L217 | partial | partial |

**Identified gaps**: GDELT (the largest), EPU, social-media-scraping pipeline (legally sensitive), sentiment fine-tunes. Truth Social and X have evolving ToS / API access policies; OPENGEM must operate within fair-use / publicly-posted-only constraints and *not* scrape private accounts.

## JSON contract — rhetoric event

```json
{
  "event_id": "trump-x-2026-06-05-1234",
  "leader": "Trump (US)",
  "vintage": "2026-06-06",
  "datetime": "2026-06-05T14:23:00-04:00",
  "platform": "Truth Social",
  "text_excerpt": "Mexico isn't doing enough at the border...",
  "tone_score": -7.2,
  "tone_baseline": -4.9,
  "tone_shock_z": -1.6,
  "targets": ["MEX"],
  "themes": ["IMMIGRATION", "TRADE"],
  "action_words_detected": ["increased tariffs", "withdraw"],
  "escalation_index": 0.78,
  "market_response": {
    "mxn_intra_day_pct": -1.8,
    "mxn_5d_pct": -0.9,
    "mxn_vol_30d_change_bp": +180,
    "ipc_1d_pct": -1.2
  },
  "historical_analogs": [
    {"event_id": "trump-x-2025-01-15-456", "similarity": 0.82, "mxn_response_pct": -2.1}
  ],
  "cite_this": "https://opengem.org/sentiment/event/trump-x-2026-06-05-1234?v=2026-06-06"
}
```

## What this loop produced

- The four-panel layout: global heatmap + GPR/EPU + rhetoric tracker + macro response.
- A Trump-vintage rhetoric tracker as the flagship implementation of a generalizable pipeline.
- An "open methodology, open prompts, open models" stance for the rhetoric pipeline.
- A macro-response panel that quantifies tone-shock → market response with event-study betas.
- Seven adapter gaps named (GDELT, EPU, social-media, leader corpora, sentiment models).
- Explicit legal-sensitivity flag for social-media scraping.

## What comes next

- **L228** conflict tracker — GDELT pulse overlap.
- **L227** elections — pre-election rhetoric tracking.
- **L225** alliances + sanctions — rhetoric → sanctions causal chain.

## Related

- [[L001-vision-statement]]
- [[L228-conflict-tracker]]
- [[L227-elections-political-risk]]
- [[L225-alliances-sanctions]]
- [[L221-energy-commodity]] — sentiment around energy embargoes
- [[L146-iconography-system]] — `radio-tower`, `newspaper`, `siren`
