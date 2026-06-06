# L167 — Inflation Nowcast Tile

**Loop**: 167 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The thesis

The Cleveland Fed publishes a daily-updated inflation nowcast. It's a Bloomberg fixture. We mirror, extend, and beat it: same model class for US (so we can claim parity), then expand to ~20 countries with adapted models (so we exceed it).

## The tile (atom)

```
   ┌─────────────────────────────────────────────┐
   │ 🇺🇸 USA  CPI nowcast, June 2026             │
   │ ─────────────────────────────────────────── │
   │                                               │
   │           3.32%                               │
   │       (current quarter)                       │
   │                                               │
   │   ╱──┬──╲                                     │
   │   │  ●  │   P10  P50  P90                     │
   │   ╲──┴──╱                                     │
   │  2.9   3.3   3.7                              │
   │                                               │
   │  YoY:   3.32%                                  │
   │  MoM:   +0.27%                                 │
   │                                               │
   │  Next release: BLS · 2026-06-12 08:30 ET      │
   │                                               │
   │  Methodology: DFM (NY Fed style)               │
   │  Vintage: 2026-06-04 14:30 UTC                │
   │  [ open the inflation page → ]                │
   └─────────────────────────────────────────────┘
   width: ~360px, height: ~280px
```

## The hero number

The headline CPI year-over-year nowcast for the current observation period (the month not yet published).

Below: the implied month-over-month rate (more volatile, more relevant for traders).

## The fan strip

Mini P10/P50/P90 fan rendered horizontally:

```
   ╱──┬──╲
   │  ●  │   ← ● is P50
   ╲──┴──╱   ← shaded region between P10 and P90
   2.9  3.3  3.7
```

Fan width encodes uncertainty. Narrows as the data accumulates through the month.

## The release countdown

```
   Next release: BLS · 2026-06-12 08:30 ET
```

A countdown clock until the official BLS release. When release hits, the tile flashes briefly (200ms amber border pulse) and updates to show:

- Actual print
- OPENGEM nowcast at release
- Surprise (actual - nowcast)
- Whether OPENGEM was in the right tail

## The "score on release" arc

For ~24 hours after a release, the tile shows the score:

```
   ┌─────────────────────────────────────────────┐
   │ 🇺🇸 USA  CPI June 2026                       │
   │ ────────────────────────────────             │
   │                                               │
   │  Actual:   3.35%                              │
   │  OPENGEM:  3.32%  (CRPS 0.15)                │
   │  Consensus: 3.30% (Bloomberg)                  │
   │                                               │
   │  We were within band (P10–P90)               │
   │  Better than 78% of forecasters this round    │
   │                                               │
   │  [ See accountability entry ]                 │
   └─────────────────────────────────────────────┘
```

After 24h, reverts to next month's nowcast.

## The methodology

US: a Cleveland-Fed-class Dynamic Factor Model. Inputs: BLS daily indices (gas, food at home), MIT Billion Prices proxies, retail scanner aggregates, energy prices. We replicate the NY Fed Nowcasting code class (per L032).

EU: ECB's high-frequency CPI nowcast methodology (Cascaldi-Garcia et al.) adapted.

UK / JPN / others: model-class adapted per data availability.

The methodology card on each tile links to the country-specific page.

## Cross-country grid

```
   CPI nowcasts (current period)
   ─────────────────────────────────────
   USA   3.32%  ▲ +0.4 vs prev print
   DEU   2.55%  ⌃ flat
   GBR   2.85%  ▼ -0.1
   FRA   2.40%  ⌃ flat
   ITA   1.78%  ▼ -0.2
   JPN   1.20%  ▲ +0.3
   CAN   2.65%  ⌃ flat
   ...
```

Sortable. Each row → tile drawer.

## The forecast track

The tile drilldown (click → page) shows:

```
   USA CPI nowcast track, June 2026
   ────────────────────────────────────────
                              actual ●
            P90 ╲   ╲   ╲
   3.5%       ╲   ╲   ╲   ╲       ●
                                              
   3.3%   ─────────────────●──────●           P50
                                              
   3.1%       ╱   ╱   ╱
                  P10 ╱   ╱
                                              
       May 1   May 8   May 15   May 22   June 1
       (build-up of confidence as data accumulates)
```

The fan narrows as data lands during the month. By release date, the fan is tight; by month-start, it's wide.

This is the "model learning in real time" visualization. Killer.

## "Watch the print" mode

For traders on release day, an opt-in "live print mode":

- Tile expands to full-width banner
- Countdown clock to release
- On release: actual vs nowcast comparison appears within 5 seconds
- Sound alert (opt-in)

## URL contract

```
/inflation?country=usa
/inflation?country=usa&period=2026-06
/inflation?country=usa&vintage=2024-09-15&period=2024-09
/inflation/track?country=usa&period=2026-06   ← the full track view
```

## Real-time updates

The nowcast refreshes:
- Daily for slow inputs (CPI components from BLS API)
- 4× daily for energy prices
- On each Billion Prices update
- On each retail scanner pull

Updates trigger a small "↑ updated 2m ago" badge on the tile.

## Component decomposition

A "what's driving the nowcast" tab in the drilldown:

```
   Components driving the June 2026 nowcast (3.32%)
   ────────────────────────────────────────
                      Weight   YoY   Contribution
   Energy             6.0%    -1.2   -0.07pp
   Food at home       8.3%    +1.8   +0.15pp
   Shelter            32.5%   +4.5   +1.46pp
   Goods (ex-energy)  19.7%   +0.3   +0.06pp
   Services (ex-shelter) 28.5%  +2.8  +0.80pp
   Other              5.0%    +1.5   +0.07pp
   ────────────────────────────────────────
   Sum                       3.32%   (model nowcast)
```

This is the explanatory layer. Click any row → indicator page for that component.

## Comparison: consensus

The drilldown overlays:
- Bloomberg consensus (when available — we cite their median)
- Reuters Poll
- Cleveland Fed (free, public — direct comparator)

OPENGEM-vs-Cleveland is the existential comparison. We must be at least as good. The leaderboard (L133) shows the track.

## Surprise index integration

The tile contributes to the surprise index (L169) for each country.

## Coverage

- Tier-V (full DFM): USA, DEU, FRA, GBR, JPN, ITA, ESP, NLD, CAN, AUS, KOR, MEX, BRA, CHN, IND
- Tier-IV (simpler model): Indonesia, Türkiye, South Africa, Argentina, Russia (data quality permitting), Poland, Sweden, Norway
- Below: not available

## Implementation

- Endpoint: `/api/inflation/nowcast?country=usa&period=2026-06`
- Server uses cached model output, refreshes on input data updates
- Tile: server-rendered, sparkline hydrated client-side
- Fan: D3-generated SVG
- Live print mode: SSE channel for the release window

## Empty states

For countries without nowcast:

```
   ┌─────────────────────────────────────────────┐
   │ 🇲🇲 MMR  Inflation nowcast — unavailable     │
   │                                               │
   │  Insufficient high-frequency data.            │
   │  Showing official monthly print only.         │
   │                                               │
   │  Last official: 5.4% (Apr 2026)               │
   └─────────────────────────────────────────────┘
```

## What we won't ship

- Daily-frequency CPI nowcasts for thinly-covered countries. The Cleveland Fed approach requires daily food and energy data; not everywhere has that.
- "Real-time CPI" that updates each second on retail prices. The signal-to-noise is bad and the model wouldn't trust it.
- A speculative "shadow CPI" stripping rent. Too political; we publish the official methodology with editorial commentary, not alternative CPIs.

## The asymmetric move

We publish the nowcast's full track during the month — every day's update visible. The Cleveland Fed publishes only the daily snapshot; their history of intra-month revisions is in their repo but not on their dashboard. OPENGEM's track view is the differentiator.
