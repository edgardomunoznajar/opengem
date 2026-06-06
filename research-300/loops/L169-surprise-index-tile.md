# L169 — Surprise Index Tile

**Loop**: 169 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The thesis

Citi's Economic Surprise Index (CESI) is a $20K/year terminal feature. The methodology is published. The math is high-school. We reproduce it openly, expose the methodology, and beat them on transparency and country coverage.

## What it is

An economic surprise index aggregates the standardized differences between actual data releases and pre-release consensus expectations. Positive = data beating expectations. Negative = data missing.

```
   surprise_t = (actual_t - consensus_median_t) / σ_release_history
   index = exponentially-weighted moving average of surprises
```

We rebrand it as the **OPENGEM Surprise Index (OSI)** to avoid trademark friction.

## The tile (atom)

```
   ┌─────────────────────────────────────────────┐
   │ 🇺🇸 USA  Surprise Index — 28-day window      │
   │ ─────────────────────────────────────────── │
   │                                               │
   │          +0.42                                │
   │     "data running hot"                        │
   │                                               │
   │     -3   -2   -1    0   +1   +2   +3          │
   │     ████████████░░░░░░░░░░░                   │
   │                       ●  ← current             │
   │                                               │
   │  ─╱╲╱──╱──╲╱──                                │
   │  12mo history                                 │
   │                                               │
   │  Recent surprises:                            │
   │   +0.7  NFP beat by 50k                       │
   │   +1.2  CPI core upside                       │
   │   -0.3  Retail soft                            │
   │                                               │
   │  Methodology: rolling-std weighted EMA        │
   │  Vintage: 2026-06-04                          │
   │  [ open the surprise page → ]                 │
   └─────────────────────────────────────────────┘
   width: ~360px, height: ~280px
```

## The hero number

A z-score (signed, typically in the -3 to +3 range). Positive = data beating expectations.

Above ±1.5 is "running hot" or "running cold." Beyond ±2 is "extreme."

## The horizontal gauge

```
   -3   -2   -1    0   +1   +2   +3
   ████████████░░░░░░░░░░░
                          ●
```

Diverging color scale (L148). Dot marks current value. Tick marks at -2, -1, 0, +1, +2 for reference.

## The 12-month sparkline

Below the gauge, a sparkline showing the index over the last 12 months. Helps the user see "is it rising or falling."

## Recent surprises (the explanatory layer)

The bottom of the tile lists the 3 most recent contributors:

```
   +0.7  NFP beat by 50k
   +1.2  CPI core upside (above forecast)
   -0.3  Retail soft (below forecast)
```

Each row is hoverable → tooltip with release date, actual, consensus, sigma.

Click any row → routes to that indicator's release page.

## Methodology — published, decisively

```
   OSI methodology (US, daily-updated)
   ────────────────────────────────────

   For each economic release i at date t:
      surprise_i,t = (actual - consensus_median) / σ_i
   
   where σ_i is the rolling 4-year standard deviation
   of (actual - consensus) for that release.

   Then:
      OSI_t = Σ_i [surprise_i × decay_weight(date_i, t)]
   
   where decay_weight uses an EMA half-life of 28 days
   (default; tunable to 7, 14, 28, 84 days).

   The consensus median is taken from Bloomberg's
   pre-release survey (where we have license); otherwise
   from Reuters Poll or OPENGEM-curated median.
```

The methodology page (L172 contract) has this verbatim plus inline code reproducing it.

## Window tabs

```
   Window:  [ 7d ]  [ 28d ]  [ 84d ]  [ 1y ]
```

Different decay half-lives. Default 28d.

## Country coverage

Tier-V (full OSI, daily): USA, EUR-block, GBR, JPN, CAN, AUS, CHN, IND, KOR, BRA, MEX
Tier-IV (weekly OSI): another 20 countries
Below: not available

The grid view shows ranked OSI across all covered countries:

```
   Surprise Index ranking (28d)
   ───────────────────────────────
   AUS    +1.4   ▣▣▣▣▣▣▣▣▣
   USA    +0.42  ▣▣▣▣▣
   GBR    +0.15  ▣▣
   DEU    -0.18  ▣▣
   FRA    -0.31  ▣▣▣
   JPN    -0.85  ▣▣▣▣▣▣▣▣
   CHN    -1.22  ▣▣▣▣▣▣▣▣▣▣▣▣
   ...
```

Click any row → tile drilldown.

## Cross-asset variants

A research-grade view exposes the OSI broken down by category:

```
   USA OSI 28d breakdown
   ──────────────────────────
   Growth (PMI, NFP, IP)    +0.6
   Inflation (CPI, PPI)     +1.1
   Housing                  -0.2
   Trade                    -0.1
   Sentiment                +0.3
   ──────────────────────────
   Composite                +0.42
```

Each sub-index click → indicator group page.

## The surprise heatmap

For traders: a calendar-style heatmap of the past 28 days, with each day colored by that day's surprise contribution:

```
   May 2026
   M  T  W  T  F
   ▣  ▣  ▣  ▣  ▣
   ▣  ▣  ░  ▣  ▣
   ▣  ▣  ▣  ▣  ░
   ▣  ░  ▣  ▣  ▣
```

Hover → which release happened that day. Click → release page.

## URL contract

```
/surprise?country=usa
/surprise?country=usa&window=84d
/surprise?country=usa&breakdown=category
/surprise?countries=usa,deu,jpn,chn   ← multi-country chart
```

## The asymmetric move

CESI is private. The composition is opaque (which releases, which weights, which decay). OPENGEM:

- Lists every release in the index
- Shows the weight on each
- Lets the user toggle releases on/off
- Lets the user change the decay
- Exposes the full math

A user can build their own variant. Power users adore this.

## "Build your own OSI"

A drawer:

```
   ┌────────────────────────────────────┐
   │  ✕  Custom surprise index           │
   │  ──────────────────────────────    │
   │  Window: [28d ▼]                    │
   │  Decay: half-life [28d ▼]            │
   │                                      │
   │  Releases included:                  │
   │  ☑ NFP (weight 1.0)                  │
   │  ☑ CPI (weight 1.0)                  │
   │  ☑ Retail (weight 1.0)               │
   │  ☐ Industrial production              │
   │  ...                                 │
   │                                      │
   │  [Preview] [Save to my profile]      │
   └────────────────────────────────────┘
```

Saved custom indices get URLs. Paying users can share with colleagues.

## Implementation

- Endpoint: `/api/surprise?country=usa&window=28d`
- Server keeps a rolling buffer of (release, actual, consensus, surprise_z) tuples
- Daily recompute of EMA
- Caching: 1h TTL (refreshed on new release landing)

## Mobile

At <640px:
- Tile retains hero, gauge, and recent surprises
- Sparkline simplified
- "Build your own" available but with reduced fidelity

## What we won't ship

- Real-time surprise during a release. The CESI methodology already standardizes; the high-frequency-during-release pulse is too noisy.
- A "implied trade signal" from surprises. We're not selling alpha; we're publishing data.
- Closed-form license to Bloomberg consensus. Where we don't have legal access, we use Reuters Poll or OPENGEM-curated consensus (transparent methodology).

## The accountability layer

Each surprise event contributes to OPENGEM's own forecast scoring (since OPENGEM publishes forecasts for the same release dates). The leaderboard (L133) tracks whether OPENGEM beats consensus on these release-by-release.

## Editorial

A "weekly surprise summary" generated automatically each Friday:

```
   This week's surprise digest (May 30 – Jun 6)
   ───────────────────────────────────────────
   USA: +0.6 (NFP and CPI both beat)
   DEU: -0.3 (PMI and industrial production miss)
   ...
   Largest surprise: AUS retail +2.1σ
```

Goes into the daily-digest RSS feed (L179).

## The "surprise index of surprise indices"

A meta-index across countries (population-weighted): the world's current data-beat-or-miss tone. Shown on the home page:

```
   World OSI: +0.18   (slightly hot)
```

A useful one-glance "where's the world data running."
