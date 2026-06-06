# L168 — GDP Nowcast Tile

**Loop**: 168 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The thesis

The Atlanta Fed's GDPNow is the most famous public nowcast in macro. Twitter quotes its number. Goldman benchmarks against it. We mirror it for the US (so we can claim parity), then extend globally (so we beat its scope).

## The tile (atom)

```
   ┌─────────────────────────────────────────────┐
   │ 🇺🇸 USA  GDP nowcast, 2026 Q2 (SAAR)         │
   │ ─────────────────────────────────────────── │
   │                                               │
   │           2.1%                                │
   │       (annualized Q/Q)                        │
   │                                               │
   │   ╱──┬──╲                                     │
   │   │  ●  │   P10  P50  P90                     │
   │   ╲──┴──╱                                     │
   │  1.4   2.1  2.7                               │
   │                                               │
   │  ─╱╲╱─╲╱──                                   │
   │  intra-quarter track                          │
   │                                               │
   │  Next release: BEA · 2026-07-29 08:30 ET     │
   │                                               │
   │  Methodology: GDPNow-class (Atlanta Fed)      │
   │  Vintage: 2026-06-04                          │
   │  [ open the GDP page → ]                      │
   └─────────────────────────────────────────────┘
   width: ~360px, height: ~280px
```

## The hero number

The headline GDP nowcast for the current quarter, expressed in:
- USA / Canada: SAAR (seasonally-adjusted annual rate, Q/Q)
- Most other countries: Q/Q SA (not annualized) by default; toggle to SAAR

We default to the country's *standard* convention, not impose US convention globally.

## The fan strip

Same convention as inflation tile (L167): mini horizontal fan with P10/P50/P90 markers.

## The intra-quarter track

The quarter is 13 weeks. The nowcast updates as data lands. The mini-spark above shows the nowcast's evolution within the quarter:

```
   Week 1: 1.4%  (wide bands)
   Week 2: 1.6%
   Week 3: 1.5%
   ...
   Week 13: 2.1% (narrow bands)
```

The Atlanta Fed's GDPNow chart is iconic for exactly this reason. We reproduce.

## The Atlanta-Fed-style track chart (drilldown)

```
   USA GDP nowcast, 2026 Q2 track
   ─────────────────────────────────────────────
                                                
   3.0% ─                                ┌──── Blue Chip top decile
                                         │
   2.5% ─       ──╱──╲          ╭────┤
                  /    ╲    ─╱╲─╱      OPENGEM nowcast
   2.0% ───╱╲╱╲      ╲──╲╱
                                         │       Blue Chip median
   1.5% ─                          ────┤
                                         │
   1.0% ─                                └──── Blue Chip bottom decile
                                                
       Apr 1   Apr 30   May 31     Jun 30      
       (build-up of nowcast through Q2)         
```

- OPENGEM nowcast as a thick amber line
- Blue Chip consensus range as gray band (private; we license / approximate via published median)
- Important data releases marked (jobs report, retail sales, etc.) as vertical lines

This is *the* nowcast visualization. Copy of GDPNow's archetype.

## Component contributions

A "what's moving the nowcast" stacked bar:

```
   Contribution to 2026 Q2 GDP nowcast (+2.1%)
   ─────────────────────────────────────────
   Consumption (PCE)        +1.5pp  ▇▇▇▇▇▇▇
   Business investment      +0.3pp  ▇▇
   Residential investment   -0.1pp  ▇
   Inventories             +0.2pp  ▇
   Net exports             -0.2pp  ▇
   Government              +0.4pp  ▇▇
   ─────────────────────────────────────────
   Total                   +2.1pp
```

Click each row → indicator page for that GDP component.

## The Atlanta-Fed-class methodology

For US:
- A bridge equation per GDP component
- Components fitted independently to high-frequency indicators
- Aggregated to total GDP

For non-US:
- Mixed-frequency dynamic factor model (DFM)
- Country-specific indicator set
- Bayesian VAR backup when DFM fails to converge

The methodology card (L172) links to per-country specifics.

## Cross-country grid

```
   GDP nowcasts (current quarter, country convention)
   ────────────────────────────────────────
   USA   +2.1% SAAR  ⌃ flat
   EUR   +0.4% Q/Q   ▲ +0.1
   CHN   +5.2% YoY   ⌃ flat
   JPN   +0.1% Q/Q   ▼ -0.2
   GBR   +0.3% Q/Q   ⌃ flat
   IND   +6.8% YoY   ▲ +0.3
   ...
```

Note the convention column — USA shows SAAR, Europe shows Q/Q, China and India show YoY (their published convention). We respect the country's customary unit.

## Comparison: consensus

The drilldown overlays:
- Atlanta Fed GDPNow (US only) — the parity comparator
- ECB nowcast (euro area)
- Bundesbank nowcast (Germany)
- IMF WEO last vintage
- Bloomberg consensus median
- OECD short-term indicator

OPENGEM-vs-Atlanta-Fed on US is the headline; the others are the moat.

## The release-day flash

Same as L167: on official BEA release, tile flashes, shows actual vs nowcast, computes score, persists for 24h.

## Coverage

- Tier-V (full nowcast): USA, DEU, FRA, ITA, GBR, JPN, CAN, AUS, KOR, MEX, BRA, IND, CHN, EUR (aggregate)
- Tier-IV (DFM only): ESP, NLD, BEL, SWE, NOR, CHE, IDN, THA, MYS, ZAF, RUS (if data quality permits)
- Below: official quarterly print only

## URL contract

```
/gdp?country=usa
/gdp?country=usa&period=2026-Q2
/gdp/track?country=usa&period=2026-Q2   ← Atlanta-Fed-style track view
/gdp?country=usa&vintage=2024-09-15
```

## "Pulse vs print" mode

A toggle that shows the diff between OPENGEM's nowcast and the consensus median:

```
   OPENGEM:       2.1%
   Consensus:     1.8%
   Diff:          +0.3pp  (more bullish than consensus)
```

The diff bias becomes a useful editorial summary: "OPENGEM is consistently +0.3pp more bullish than Bloomberg consensus on US GDP." That's signal.

## The "what data is missing" tab

A view showing which indicators have landed for this quarter and which haven't:

```
   Quarter Q2 2026 — data status
   ──────────────────────────────
   ✓ April jobs report (released May 3)
   ✓ April CPI (May 13)
   ✓ April retail sales (May 16)
   ✓ April industrial production (May 16)
   ✗ May jobs report (due June 6)
   ✗ May CPI (due June 12)
   ...
```

Helps the user see "we're only 40% into the quarter's data; bands are wide because of it."

## Editorial tag

Each tile carries an editorial tag where relevant:
- "Within range of consensus"
- "Above consensus" / "Below consensus"
- "Significantly above" (>1σ above consensus dispersion)
- "Risk-on environment" (broader macro classifier)

Editorial-curated.

## Implementation

- Endpoint: `/api/gdp/nowcast?country=usa&period=current`
- Component contributions: cached server-side
- Track chart: D3 with delayed-load consensus overlays (consensus data has its own license/refresh)
- Animation: track chart can be replayed (similar to L167 inflation)

## Mobile

At <640px:
- Tile compresses; component breakdown collapses to a "Show drivers" expand
- Track chart shown without consensus overlays (saves bandwidth)
- Release-day flash banner pinned to top

## Performance

- Tile initial render: <100ms (server component)
- Track chart: lazy-loaded ~80KB JS
- Component breakdown: <50KB additional

## The accountability arc

When the official BEA release lands:
- Score computed: CRPS, MAE, in-band flag
- Logged to the accountability ledger
- "OPENGEM forecast 2.1%, actual 2.3%, error +0.2pp, ranked 4th of 12" entry created
- 30-day exponential decay weighting for the leaderboard

## What we won't ship

- "GDP at high frequency" (truepulse-style daily GDP). The signal isn't there.
- Quarter-of-quarter (Q/Q non-annualized) vs annualized toggle as the headline. Country convention wins; toggle is in the menu.
- Pre-revisions backcast. We publish first-vintage nowcast and stick with it. Revisions get their own diff page.

## The asymmetric move

Atlanta Fed publishes the nowcast but its "raw signals" are visible only in their model documentation. OPENGEM publishes:
- The nowcast.
- The component contributions.
- The intra-quarter track.
- The list of data releases pending.
- The diff vs every public comparator.

All in one tile drilldown. Atlanta Fed gives you the number; we give you the workshop.
