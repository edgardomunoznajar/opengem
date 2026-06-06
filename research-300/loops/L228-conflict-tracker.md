# L228 — Conflict Tracker Page

**Loop**: 228 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The thesis of this loop

Armed conflict is no longer rare. The post-2022 era has seen a 30-year high in active state-based conflicts: Ukraine, Gaza, Sudan, Myanmar, Tigray, the Sahel insurgencies, Yemen, Syria, Mexican cartel violence above many "conflict" thresholds, Haiti. **The data is exceptional**: UCDP (Uppsala Conflict Data Program) is the canonical academic source, ACLED (Armed Conflict Location & Event Data) publishes near-real-time event-level data with location + actor + casualties, GDELT 2.0 publishes news-derived event records hourly. **The integration is awful**: UCDP has a portal nobody uses; ACLED has a portal with charts but no API for the casual consumer; GDELT requires technical chops.

OPENGEM's conflict tracker is the page that *finally* makes near-real-time conflict data legible for non-specialists. It is the page that, when a Sahel coup happens, becomes the *receipt* — current conflict intensity map, event feed, comparison to historical analogs, sovereign-spread response. It is the page that, when Haiti collapses into open gang warfare, surfaces what the *market hasn't yet priced*.

This loop **decides** the page structure (live heatmap + event feed + per-conflict detail), the conflict-intensity scoring, and the integration with sovereign-risk for the "conflict-priced-in?" question.

## The four panels

1. **Live heatmap** — geographic map of active conflict, weighted by fatalities × events × media intensity.
2. **Event feed** — chronological feed of newly-recorded events (ACLED + GDELT).
3. **Per-conflict detail** — for named conflicts, the full state-of-play: actors, fatalities trend, territory map, peace-talks status.
4. **Macro overlay** — for each affected country, current sovereign spread / CDS / FX vs pre-conflict baseline.

## Page structure (top to bottom)

```
┌──────────────────────────────────────────────────────────────────────┐
│ CONFLICT TRACKER                                                     │
│ UCDP + ACLED + GDELT. Live heatmap. Event feed.                      │
└──────────────────────────────────────────────────────────────────────┘

[Tabs]
 [Live heatmap]  [Event feed]  [Per-conflict]  [Macro overlay]

╔══════════════════════════════════════════════════════════════════════╗
║ LIVE HEATMAP                                                          ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ World map (geographic, zoomable) ─────────────────────────────────┐
│  Layers (toggleable):                                                │
│   - ACLED events (last 30 days): dots colored by event type          │
│     (battle, violence-against-civilians, riot, protest, explosion)   │
│   - Fatalities heat: hex-binned, color intensity = fatality count    │
│   - UCDP-classified conflicts (state-based, non-state, one-sided)    │
│   - Borders: highlight contested territory                           │
│   - Refugee flow arcs (UNHCR data)                                   │
│                                                                      │
│  Time slider: scrub 2010-2026 to see conflict landscape over time    │
│                                                                      │
│  Top-of-page lozenges:                                               │
│   - Currently active state-based conflicts: 47 (vs 32 in 2018)       │
│   - 30-day fatalities (ACLED): ~14,500                               │
│   - Newly-erupted conflicts in last 12m: 4                           │
└─────────────────────────────────────────────────────────────────────┘

┌─ Country-level conflict intensity grid ────────────────────────────┐
│ Country │Status        │Intensity│30d fatalities│Trend │Actors    │
│ UKR     │Active (state)│ Extreme │ 2,100        │ ─    │RUS, ZUKR │
│ SDN     │Active (NS)   │ Extreme │ 1,800        │ ▲▲▲ │SAF, RSF  │
│ MMR     │Active (NS)   │ High    │   650        │ ▲    │SAC, PDF, EAOs│
│ MEX     │Active (CL)   │ High    │ 2,400        │ ▲    │Cartels   │
│ PSE     │Active (state)│ High    │   400        │ ▼    │ISR, HAMAS│
│ YEM     │Active (state)│ Mod     │   320        │ ─    │SAU, Houthi│
│ HTI     │Active (NS)   │ Extreme │   900        │ ▲▲▲ │Gangs     │
│ ETH     │Active (state)│ Mod     │   250        │ ▼    │FDRE, OLA │
│ NER     │Active (NS)   │ Mod     │   180        │ ▲    │JNIM, ISGS│
│ MLI     │Active (NS)   │ Mod     │   150        │ ─    │JNIM, ISGS, Wagner│
│ ...                                                                  │
└─────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════╗
║ EVENT FEED                                                            ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Chronological event stream ───────────────────────────────────────┐
│  2026-06-06 08:14 UTC ┊ SDN ┊ Battle  ┊ Khartoum  ┊ ~40 fatal  ┊ ACLED│
│  2026-06-06 07:50 UTC ┊ UKR ┊ Strike  ┊ Kharkiv   ┊ ~12 fatal  ┊ ACLED│
│  2026-06-06 07:42 UTC ┊ MEX ┊ Cartel  ┊ Culiacán  ┊ ~6 fatal   ┊ GDELT│
│  2026-06-06 07:15 UTC ┊ HTI ┊ Gang    ┊ Port-au-P.┊ ~25 fatal  ┊ ACLED│
│  2026-06-06 06:58 UTC ┊ MMR ┊ Strike  ┊ Sagaing   ┊ ~14 fatal  ┊ ACLED│
│  ...                                                                 │
│                                                                       │
│  Filter by: country / actor / event type / fatality threshold        │
│  Sort: chronological / fatality count / location proximity           │
│  Each row → click for full event detail + source links               │
└─────────────────────────────────────────────────────────────────────┘

┌─ Daily fatality time series ───────────────────────────────────────┐
│  Y: fatalities / day                                                 │
│  X: 2018 → 2026                                                      │
│  Stacked area: conflict (UKR, GAZ, SDN, MMR, MEX, YEM, etc.) by name │
│  Annotations: 2022-02-24 Ukraine invasion, 2023-10-07 Gaza, etc.     │
└─────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════╗
║ PER-CONFLICT DETAIL                                                   ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Selected: Sudan civil war (SAF vs RSF) ───────────────────────────┐
│ Onset: 2023-04-15                                                    │
│ Days active: 1,148                                                   │
│ Total estimated fatalities: ~36,000                                  │
│ Estimated displaced: 11.4M (one of the largest displacement crises   │
│   in the world)                                                      │
│                                                                      │
│ Active actors:                                                       │
│   - SAF (Sudanese Armed Forces) — al-Burhan                          │
│   - RSF (Rapid Support Forces) — Hemedti                             │
│   - JEM, SLM-MM (Darfur factions, intermittent)                      │
│                                                                      │
│ Territory map: which faction controls which province                 │
│   - Khartoum: contested, mostly RSF                                  │
│   - Darfur: RSF                                                      │
│   - East: SAF                                                        │
│                                                                      │
│ Peace-talk status: Jeddah talks suspended, AU framework stalled      │
│                                                                      │
│ Comparable historical analogs:                                       │
│   - South Sudan 2013-2018 (similar intensity, similar duration)      │
│   - Libya 2011-2020 (faction-based, foreign intervention)            │
│                                                                      │
│ ┌─ Fatality time series ─────────────────────────────────────────┐  │
│ │  Daily fatalities chart (since 2023-04)                         │  │
│ │  Annotations: Khartoum offensive, Darfur escalation, talks       │  │
│ └─────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════╗
║ MACRO OVERLAY                                                         ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Pre-conflict baseline vs current macro ───────────────────────────┐
│ Country │ Conflict│ Sovrn   │ FX     │ Inflation│ Comment              │
│         │ since   │ spread  │ vs pre │ vs pre   │                     │
│ UKR     │2022-02  │ +12pp   │ -32%   │ +28pp    │ Largely priced in    │
│ SDN     │2023-04  │ n/a (no │ -340%  │ +180pp   │ Currency collapse    │
│         │         │ market) │        │          │                     │
│ MMR     │2021-02  │ n/a     │ -65%   │ +35pp    │ Sustained pressure   │
│ PSE/ISR │2023-10  │ ISR +60 │ ISR -8%│ ISR +1pp │ ISR resilient        │
│         │         │ bp      │        │          │                     │
│ HTI     │2024-03  │ n/a     │ -45%   │ +28pp    │ Acute collapse       │
│ ETH     │2020-11  │ +200bp  │ -42%   │ +18pp    │ Partly priced        │
│ YEM     │2014-09  │ n/a     │ -85%   │ +110pp   │ Long-running         │
│ ...                                                                  │
└─────────────────────────────────────────────────────────────────────┘

┌─ Conflict-pricing widget ──────────────────────────────────────────┐
│  Per country with active conflict, the page computes:               │
│   "Has the market priced this in?" by comparing current sovereign   │
│   spread / CDS / FX vol to similar historical conflict episodes.    │
│                                                                      │
│   Output: a single bar from 0 ("not yet priced") to 100% ("priced"). │
│   For UKR: 85% priced (deep pricing post-2022).                      │
│   For SDN: 50% priced (limited market access, hard to gauge).        │
│   For HTI: 30% priced (gangs unrecognized as systemic risk).         │
│   For MEX: 15% priced (cartel violence not in sovereign pricing).    │
│                                                                      │
│  This is the *trader's* version of the page — where IS opportunity? │
└─────────────────────────────────────────────────────────────────────┘
```

## The conflict-pricing widget — the alpha generator

The "Has the market priced this in?" widget is the page's most distinctive output. The methodology:

1. For each country with active conflict, retrieve current sovereign spread / CDS / FX-vol.
2. Identify historical conflict analogs (matched by intensity, duration, actor type via UCDP-style classification).
3. Compute the historical median market response 6m-after-onset for analogs.
4. Compare current pricing to the historical median: a 0-100 "priced-in" percentage.

This is **the** feature that turns a humanitarian dashboard into a macro-trading tool. For a hedge-fund analyst, low-priced-in conflicts are signal: Mexico is the canonical example — cartel violence above traditional civil-war thresholds but barely reflected in MXN pricing.

## Data sources / adapter dependencies

| Input | Source | Adapter | Status |
|---|---|---|---|
| UCDP conflict classification | UCDP (Uppsala) | `opengem-data-ucdp` ⚠️ NOT YET BUILT | gap |
| ACLED event data | ACLED API (free tier limited) | `opengem-data-acled` ⚠️ NOT YET BUILT | gap |
| GDELT 2.0 events | GDELT API | `opengem-data-gdelt` ⚠️ NOT YET BUILT (in roster, not built) | gap |
| UNHCR displacement data | UNHCR | `opengem-data-unhcr` ⚠️ NOT YET BUILT | gap |
| EM-DAT (for natural-disaster overlay) | CRED | `opengem-data-emdat` ⚠️ NOT YET BUILT | gap |
| Sovereign spreads / CDS | as L216 | partial | partial |
| FX vs pre-conflict baseline | per-country FX series | as L217 | partial |

**Identified gaps**: UCDP, ACLED, GDELT, UNHCR. ACLED has a paid API for high-frequency / commercial use and a free tier with rate limits; OPENGEM's adapter must respect ACLED's licensing carefully (the page must give explicit attribution and link, per ACLED's CC-BY).

## JSON contract — per-conflict

```json
{
  "conflict_id": "sdn-civil-war-2023",
  "country": "SDN",
  "vintage": "2026-06-06",
  "ucdp_classification": "state-based: SAF vs RSF",
  "onset_date": "2023-04-15",
  "days_active": 1148,
  "total_fatalities_est": 36000,
  "displaced_est": 11400000,
  "active_actors": [
    {"name": "SAF", "leader": "al-Burhan", "type": "government"},
    {"name": "RSF", "leader": "Hemedti", "type": "paramilitary"},
    {"name": "JEM", "type": "rebel-darfur"}
  ],
  "territory_control_pct": {
    "saf_controlled": 38,
    "rsf_controlled": 35,
    "contested": 22,
    "no_clear_control": 5
  },
  "fatalities_30d": 1800,
  "fatalities_trend_30d": "rising-fast",
  "peace_status": "talks_suspended",
  "macro_pricing": {
    "sovereign_spread_bp_pre_conflict": 850,
    "sovereign_spread_bp_current": "n/a (no functional market)",
    "fx_vs_pre_conflict_pct": -340,
    "implied_priced_in_pct": 50
  },
  "analog_conflicts": ["ssd-2013-2018", "lby-2011-2020"],
  "cite_this": "https://opengem.org/conflict/sdn-2023?v=2026-06-06"
}
```

## What this loop produced

- The four-panel layout: live heatmap + event feed + per-conflict detail + macro overlay.
- A conflict-pricing widget computing "% priced-in" via historical analog comparison.
- The country-level intensity grid with actor lists.
- Per-conflict detail with territory control + analog identification.
- Four major adapter gaps named (UCDP, ACLED, GDELT, UNHCR).

## What comes next

- **L229** sentiment / news tone (GDELT pulse — adjacent dataset).
- **L225** alliances + sanctions — conflict actors and sanctions sometimes overlap.
- **L227** elections — post-electoral violence integration.

## Related

- [[L001-vision-statement]]
- [[L229-sentiment-news-tone]]
- [[L225-alliances-sanctions]]
- [[L227-elections-political-risk]]
- [[L216-sovereign-risk]] — conflict-affected sovereigns
- [[L146-iconography-system]] — `swords`, `siren`, `map-pin`, `flag`
