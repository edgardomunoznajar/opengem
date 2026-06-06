# L225 — Geopolitical Alliances + Sanctions Page

**Loop**: 225 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The thesis of this loop

The world has, in the post-2018 era, *re-bifurcated* along geopolitical lines that did not exist twenty years ago. NATO+, the Quad, AUKUS, IPEF, the Belt and Road, BRICS+, the SCO, the EAEU — these alliance structures *and the sanctions regimes that overlay them* are now first-order macro variables. **Who sanctions whom is now a tradable.** And the data is shockingly open: Open Sanctions (consolidated, free), OFAC SDN list (US), EU consolidated sanctions list, OFSI (UK), DFAT (Australia), MEXT (Japan), CFIUS investment-restriction lists, CHIPS Act tech-export-control lists.

**No public dashboard puts the sanctions matrix and the alliance overlap side-by-side.** Stratfor *talks* about alliances; OPENGEM *plots* them. Bloomberg has a "Country Risk" tab; it has no alliance graph. CSIS has alliance maps but no sanctions overlay. OurWorldInData has trade blocs but not regime overlap.

OPENGEM's alliances + sanctions page is the page that turns *narratives* about geopolitical fragmentation into *visualizations* anyone can drill into. It is the page that, when the US announces new tech sanctions against China, becomes the *receipt* for "here is the existing CHIPS Act surface, here is what's new, here is what trade flows are most exposed." It is the page that, when BRICS+ admits a new member, automatically updates the alliance map and re-computes overlap metrics.

This loop **decides** the page structure (who-sanctions-who matrix + alliance overlap + trade bloc map), the sanctions classifier, and the alliance-graph data model.

## The three pivots

The page is organized around three pivots:

1. **Sanctions matrix** — who-sanctions-who, broken out by sanctions type (financial, trade, individual, sectoral).
2. **Alliance overlap** — which countries co-participate in which alliances; overlap metrics (Jaccard index across membership lists).
3. **Trade-bloc map** — visual map of WTO, USMCA, EU, ASEAN, RCEP, AfCFTA, MERCOSUR, EAEU, CPTPP and overlaps.

## Page structure (top to bottom)

```
┌──────────────────────────────────────────────────────────────────────┐
│ GEOPOLITICAL ALLIANCES + SANCTIONS                                   │
│ Who sanctions whom. Who allies with whom. Open Sanctions + alliances.│
└──────────────────────────────────────────────────────────────────────┘

[Tabs]
 [Sanctions matrix]  [Alliance graph]  [Trade-bloc map]  [Per-country]

╔══════════════════════════════════════════════════════════════════════╗
║ SANCTIONS MATRIX VIEW                                                 ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Matrix: imposer × target ─────────────────────────────────────────┐
│                                                                     │
│                          TARGET →                                   │
│              RUS   IRN   PRK   CUB   VEN   SYR   MMR   BLR   CHN    │
│ IMPOSER ↓  ╔═════╤═════╤═════╤═════╤═════╤═════╤═════╤═════╤═════╗  │
│   USA      ║ ■■■ │ ■■■ │ ■■■ │ ■■■ │ ■■■ │ ■■■ │ ■■  │ ■■  │ ■◐  ║  │
│   EU       ║ ■■■ │ ■■  │ ■■■ │  ◐  │ ■■  │ ■■  │ ■■  │ ■■■ │ ◐   ║  │
│   GBR      ║ ■■■ │ ■■  │ ■■■ │     │ ■■  │ ■■  │ ■   │ ■■■ │     ║  │
│   JPN      ║ ■■  │ ■   │ ■■■ │     │     │     │     │ ■   │     ║  │
│   CAN      ║ ■■■ │ ■■  │ ■■  │ ■   │ ■   │ ■■  │ ■   │ ■■  │     ║  │
│   AUS      ║ ■■■ │ ■   │ ■■■ │     │ ■   │ ■■  │ ■   │ ■■  │     ║  │
│   KOR      ║ ■■  │     │ ■■■ │     │     │     │     │     │     ║  │
│   CHN      ║ ─   │ ─   │ ─   │ ─   │ ─   │ ─   │ ─   │ ─   │ ─   ║  │
│   RUS      ║ ─   │ ─   │ ─   │ ─   │ ─   │ ─   │ ─   │ ─   │ ─   ║  │
│            ╚═════╧═════╧═════╧═════╧═════╧═════╧═════╧═════╧═════╝  │
│                                                                     │
│  Cell encoding:                                                     │
│   ■■■ comprehensive (financial + trade + individual + sectoral)     │
│   ■■  partial (2-3 types)                                           │
│   ■   targeted (1 type, often individuals only)                     │
│   ◐   pending / under-discussion                                    │
│                                                                     │
│  Cell hover: tooltip listing specific programs + count of designees │
│  Cell click: opens detail panel with full sanctions inventory        │
└─────────────────────────────────────────────────────────────────────┘

┌─ Sanctions type filter ────────────────────────────────────────────┐
│  [Financial] [Trade] [Individuals] [Sectoral] [Tech-export] [All]  │
│  Selecting one type re-renders the matrix to that type only         │
└─────────────────────────────────────────────────────────────────────┘

┌─ Time slider ──────────────────────────────────────────────────────┐
│  2000 ←──────●──→ 2026   (scrub to see matrix evolution)            │
│  Reveals e.g., the post-2014 RUS sanctions stack vs the post-2022   │
│   sanctions wave                                                    │
└─────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════╗
║ ALLIANCE GRAPH VIEW                                                   ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Network graph: countries as nodes, alliances as edges ────────────┐
│                                                                     │
│  Node = country (size = GDP; color = bloc affiliation)               │
│  Edge = co-membership (thickness = number of shared alliances)       │
│                                                                     │
│  Default layout: force-directed (D3 / observable-plot-graph)        │
│  Cluster reveal: NATO+ cluster (top-left), BRICS+ cluster (right),  │
│   ASEAN cluster (bottom), Non-aligned cluster (center)              │
│                                                                     │
│  Highlight: hover a country → all its alliances pulsate              │
│  Filter: select alliances to show — uncheck NATO to hide that edge   │
└─────────────────────────────────────────────────────────────────────┘

┌─ Overlap metric panel ─────────────────────────────────────────────┐
│  Jaccard index between major bloc pairs:                            │
│   NATO ∩ EU:        24 / 32 = 0.75   (highly overlapping)            │
│   NATO ∩ Quad:      2 / 4   = 0.50                                   │
│   BRICS+ ∩ SCO:     5 / 12  = 0.42                                   │
│   Quad ∩ AUKUS:     3 / 4   = 0.75                                   │
│   IPEF ∩ CPTPP:     8 / 14  = 0.57                                   │
│                                                                     │
│  Reveals which alliance pairings are functionally co-extensive vs   │
│   independent levers of influence.                                  │
└─────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════╗
║ TRADE-BLOC MAP                                                        ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Geographic map ───────────────────────────────────────────────────┐
│  World map, each country colored by primary trade-bloc affiliation │
│  Overlays toggleable: USMCA, EU/EEA, ASEAN, RCEP, AfCFTA, MERCOSUR, │
│   EAEU, CPTPP, IPEF                                                 │
│                                                                     │
│  Multi-bloc countries: pie-chart symbol on country                  │
│  Free-trade-agreement (FTA) network overlay: line between countries │
│   that have bilateral FTAs                                          │
│                                                                     │
│  Click country: opens detail panel listing every FTA + every bloc   │
│   + every sanctions imposed by/on this country                      │
└─────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════╗
║ PER-COUNTRY DETAIL                                                    ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Selected: Turkey ─────────────────────────────────────────────────┐
│ ALLIANCES                                                            │
│  NATO (1952), CoE, OECD, G20, Customs Union with EU (1995)          │
│  Pending: BRICS+ membership conversation (informal)                  │
│  Sanctions co-imposer with: USA, EU (selectively)                    │
│                                                                      │
│ SANCTIONS RECEIVED                                                   │
│  US CAATSA (2020 — S-400 acquisition)                                │
│   - Defense industry suppliers list                                  │
│   - Limited financial impact                                         │
│                                                                      │
│ SANCTIONS OUTBOUND                                                   │
│  Targeted (individuals + entities): Cyprus, Syria                    │
│                                                                      │
│ TRADE-BLOC OVERLAP                                                   │
│  - EU Customs Union: high tariff alignment                           │
│  - No bilateral FTAs outside CU partners + OIC partners              │
│  - D-8 (Developing-8) member                                         │
│                                                                      │
│ GEOPOLITICAL TENSION INDEX (GPR-style) — 30d: rising                 │
│  Drivers: Mediterranean energy claims, Cyprus, Greece                │
└─────────────────────────────────────────────────────────────────────┘
```

## The sanctions classifier — what counts as a sanction?

OPENGEM uses a deliberately *expansive* taxonomy. Five types:

1. **Financial sanctions**: asset freezes, banking restrictions, SWIFT exclusion, secondary-sanctions threats.
2. **Trade sanctions**: import/export bans, tariffs above WTO MFN as punitive measure.
3. **Individual sanctions**: SDN list designations, visa bans, travel bans.
4. **Sectoral sanctions**: oil price caps, tech-export controls, dual-use restrictions.
5. **Tech-export sanctions**: CHIPS Act, EAR + ITAR, EU dual-use, foreign-direct-product rule applications.

Each sanctions program is classified by type and severity (Comprehensive / Targeted / Symbolic). The classifier is rule-based + LLM-assisted from program description; classifications are vintaged and challengeable.

## The alliance graph data model

Each alliance entry has:

- **Name** + abbreviation.
- **Type** (military, economic, diplomatic, tech).
- **Founding date** + accession history.
- **Member list** (per year, vintaged).
- **Charter / treaty link**.

Stored as a property graph (Neo4j-compatible JSON-LD) and queryable via the page's API + MCP.

## The Trump-vintage / regime-shift overlay

The page carries a **regime-shift overlay** that marks major sanctions waves with vintaged events:

- 2014: Russia / Crimea
- 2018: US-China tariff war
- 2019: CHIPS-precursor entity-list adds (Huawei)
- 2022: Russia full-spectrum sanctions
- 2023: tech-export expansion (chip rules)
- 2024-2026: trajectory under new US administration

The overlay reveals *who pivoted with whom*: which countries joined which sanctions waves, which countries abstained, which countries took counter-positions.

## Data sources / adapter dependencies

| Input | Source | Adapter | Status |
|---|---|---|---|
| Consolidated sanctions data | Open Sanctions | `opengem-data-opensanctions` ⚠️ NOT YET BUILT | gap |
| OFAC SDN list | US Treasury OFAC | `opengem-data-ofac` ⚠️ NOT YET BUILT | gap |
| EU consolidated list | EU External Action Service | `opengem-data-eu-csl` ⚠️ NOT YET BUILT | gap |
| UK OFSI | UK HMT | `opengem-data-ofsi` ⚠️ NOT YET BUILT | gap |
| UN Security Council sanctions | UN SC | `opengem-data-un-sc` ⚠️ NOT YET BUILT | gap |
| Alliance membership | manual curation + DCAF + CSIS | `opengem-data-alliances` (manual JSON) | manual |
| Trade-bloc membership | WTO RTA database | `opengem-data-wto-rta` ⚠️ NOT YET BUILT | gap |
| Tech-export control lists | BIS Entity List, EU dual-use list | `opengem-data-bis-entity-list` ⚠️ NOT YET BUILT | gap |
| GDELT events for geopolitical pulse | GDELT 2.0 | `opengem-data-gdelt` ⚠️ NOT YET BUILT | gap |

**Identified gaps**: Open Sanctions is the *single most important* adapter — it consolidates ~30 source lists into a clean schema. Building this one adapter unlocks 80% of the sanctions page. The alliance membership data is manageable as a curated JSON file maintained by OPENGEM.

## JSON contract — sanctions cell

```json
{
  "imposer": "USA",
  "target": "CHN",
  "vintage": "2026-06-06",
  "severity_code": "■◐",
  "severity_label": "partial",
  "by_type": {
    "financial": {"present": true, "programs": ["EO 13959 (military-industrial)"]},
    "trade": {"present": true, "programs": ["Section 301 (selective)"]},
    "individuals": {"present": true, "designees_count": 145},
    "sectoral": {"present": true, "programs": ["chip export controls"]},
    "tech_export": {"present": true, "programs": ["BIS Entity List subsidiaries", "FDPR application"]}
  },
  "first_imposed": "2018-07-06",
  "last_modified": "2026-05-14",
  "trade_value_affected_usdbn": 425,
  "narrative_link": "https://opengem.org/sanctions/usa-chn?v=2026-06-06"
}
```

## What this loop produced

- The three-pivot layout: sanctions matrix + alliance graph + trade-bloc map.
- A five-type sanctions classifier (financial, trade, individual, sectoral, tech-export).
- A property-graph alliance model.
- Time-slider on the matrix to scrub history.
- Nine adapter gaps named — Open Sanctions is the highest-leverage single addition.

## What comes next

- **L228** conflict tracker (overlays conflict events on the alliance graph).
- **L218** trade balance (sanctions affect bilateral flows).
- **L229** sentiment / news tone (GDELT pulse joins the alliance overlay).

## Related

- [[L001-vision-statement]]
- [[L218-trade-balance-capital-flows]]
- [[L228-conflict-tracker]]
- [[L229-sentiment-news-tone]]
- [[L216-sovereign-risk]] — sanctions are sovereign-risk events
- [[L146-iconography-system]] — `gavel`, `swords`, `handshake`, `flag`
