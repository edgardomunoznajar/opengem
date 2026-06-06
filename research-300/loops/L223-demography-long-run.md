# L223 — Demography / Long-Run Page

**Loop**: 223 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The thesis of this loop

Demography is the *most predictable* macro variable on the dashboard. The 2050 dependency ratio for Japan is essentially knowable today within a 5% error band. The 2050 working-age population of Africa is knowable within a 10% band. The 2050 urbanization share of India is knowable within a 15% band. **These are the only macro forecasts that fund managers, sovereigns, and policy economists can actually price with confidence** — because the people who will be 30 in 2050 are already born.

And the open data is excellent: UN World Population Prospects 2024 (the canonical source), UN Population Division migrant stock, UN Urbanization Prospects, World Bank Population Estimates, IIASA Wittgenstein Centre (multidimensional projections by education level — the more sophisticated cut). **Yet there is no dashboard that makes these comparable, interactive, and tied to macro implications.** Bloomberg's demographics page is a tab nobody opens. OWID does excellent demographic explainers but not as a *queryable* dashboard. UN's own portal is a bureaucratic catalog.

OPENGEM's demography page does what every long-horizon allocator does internally: surfaces the 2030/2050 demographic trajectory per country, computes the macro implications (labor force growth, dependency burden, savings rate trajectory), and **publishes it as a clickable, vintaged, embeddable dashboard**. It is the page that, for the right audience, becomes the "demographics is destiny" receipt.

This loop **decides** the page structure (population + dependency + urbanization + migration + workforce), the long-horizon visualization style (animation + age-pyramid), and the macro-implication overlay.

## The four panels

1. **Population** — current, trajectory, growth rate, fertility, mortality.
2. **Age structure** — age pyramid, working-age share, dependency ratio (young + old).
3. **Urbanization + migration** — urban share, internal migration, international migrant stocks.
4. **Workforce & macro implications** — labor force trajectory, retirement burden, savings rate proxy.

## Page structure (top to bottom)

```
┌──────────────────────────────────────────────────────────────────────┐
│ DEMOGRAPHY / LONG-RUN                                                │
│ UN WPP 2024 + Wittgenstein. 2025-2100 trajectories per country.      │
└──────────────────────────────────────────────────────────────────────┘

[Tabs]
 [Population]   [Age structure]   [Urbanization & migration]   [Workforce & macro]

[Selectors]
 [Country: ALL ▼]   [Variant: median / 80% PI / Wittgenstein-SSP ▼]   [Year: 2025 ▼ ↔ 2100]

╔══════════════════════════════════════════════════════════════════════╗
║ POPULATION PANEL                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Headline grid (cross-country, 2025/2050/2100) ────────────────────┐
│ Country │Pop 2025│Pop 2050│Pop 2100│Δ 2025-2050│Δ 2025-2100        │
│ IND     │1450M   │1670M   │1530M   │+15%       │+5%                │
│ CHN     │1410M   │1300M   │770M    │-8%        │-45%               │
│ USA     │340M    │375M    │395M    │+10%       │+16%               │
│ NGA     │225M    │375M    │545M    │+67%       │+142%              │
│ IDN     │280M    │320M    │335M    │+14%       │+20%               │
│ BRA     │215M    │220M    │190M    │+2%        │-12%               │
│ PAK     │240M    │335M    │425M    │+40%       │+77%               │
│ EGY     │115M    │160M    │190M    │+39%       │+65%               │
│ JPN     │125M    │105M    │74M     │-16%       │-41%               │
│ RUS     │145M    │130M    │112M    │-10%       │-23%               │
│ ETH     │125M    │210M    │310M    │+68%       │+148%              │
│ DEU     │84M     │81M     │70M     │-4%        │-17%               │
│ ...                                                                  │
│ Sort by: 2050 size / 2050 change / 2100 change / fertility           │
└─────────────────────────────────────────────────────────────────────┘

┌─ Population trajectory chart (per country, 1950-2100) ─────────────┐
│  Y: millions                                                         │
│  X: 1950 → 2100                                                      │
│  Solid line: median UN WPP 2024                                      │
│  Band: 80% probabilistic interval (UN PI)                            │
│  Annotations: 1-child policy (CHN), demographic transition starts    │
│  Toggle: stacked area showing births + deaths + net migration        │
└─────────────────────────────────────────────────────────────────────┘

┌─ World map (animated) ─────────────────────────────────────────────┐
│  Choropleth: population growth rate                                 │
│  Time slider: 1950 → 2100, animated playback                        │
│  Reveals the "demographic transition" sweep across continents        │
└─────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════╗
║ AGE STRUCTURE PANEL                                                   ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Animated age pyramid (per country) ───────────────────────────────┐
│                                                                     │
│  Year selector: 2000 ←┄┄┄●┄┄┄┄┄┄→ 2100  (drag to scrub)             │
│                                                                     │
│       MALES        Age      FEMALES                                 │
│  ░░░░░░░░░  100+   ░░░░░░░░                                         │
│  ████░░░░  90-94   ░░░░░████                                        │
│  ████████  85-89   █████████                                        │
│  ████████  80-84   █████████                                        │
│  ████████  75-79   █████████                                        │
│  ████████  70-74   █████████                                        │
│  █████████ 65-69   ██████████                                       │
│  ██████████ 60-64  ███████████                                      │
│  ██████████ 55-59  ███████████                                      │
│  ██████████ 50-54  ███████████                                      │
│  ██████████ 45-49  ███████████                                      │
│  ████████   40-44  █████████                                        │
│  ███████    35-39  ████████                                         │
│  ██████     30-34  ███████                                          │
│  █████      25-29  ██████                                           │
│  ████       20-24  █████                                            │
│  ████       15-19  █████                                            │
│  ████       10-14  ████                                             │
│  ████       5-9    ████                                             │
│  ████       0-4    ████                                             │
└─────────────────────────────────────────────────────────────────────┘

┌─ Cross-country dependency ratio grid ──────────────────────────────┐
│ Country │Total dep│ Old dep│Young dep│Δ Total 2050│Note            │
│ JPN     │ 78%     │ 52%    │ 26%     │ +18pp      │ already extreme│
│ DEU     │ 65%     │ 38%    │ 27%     │ +12pp      │ aging fast     │
│ CHN     │ 52%     │ 31%    │ 21%     │ +35pp      │ aging fastest  │
│ ITA     │ 67%     │ 42%    │ 25%     │ +18pp      │ already aged   │
│ KOR     │ 48%     │ 30%    │ 18%     │ +35pp      │ collapsing     │
│ USA     │ 56%     │ 30%    │ 26%     │ +8pp       │ moderate       │
│ IND     │ 53%     │ 12%    │ 41%     │ +12pp      │ youthful       │
│ NGA     │ 88%     │ 6%     │ 82%     │ -8pp       │ youthful       │
│ ETH     │ 81%     │ 6%     │ 75%     │ -3pp       │ youthful       │
│ ...                                                                  │
└─────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════╗
║ URBANIZATION & MIGRATION PANEL                                        ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Urbanization trajectory ──────────────────────────────────────────┐
│  Urban share % by country, 1950-2100                                │
│  Highlights: India crossing 50% urban ~2040, China at 80% by 2050    │
│  Per-country line + cross-country grid                              │
└─────────────────────────────────────────────────────────────────────┘

┌─ Migrant stocks ───────────────────────────────────────────────────┐
│  Inbound: top destination countries (USA 50M, DEU 17M, SAU 13M, ...) │
│  Outbound: top source countries (IND 18M, MEX 11M, ROM 4M, ...)      │
│  Bilateral matrix: flows source × destination                        │
│  Per-country net migration as % of population                        │
└─────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════╗
║ WORKFORCE & MACRO IMPLICATIONS PANEL                                  ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Working-age population trajectory ────────────────────────────────┐
│  Per country: working-age (15-64) population 2025-2100               │
│  Reveals "peak workforce" timing per country                         │
│   - CHN: peaked ~2017                                                │
│   - IND: peaks ~2050                                                 │
│   - NGA: still rising 2100                                           │
│   - USA: peaks ~2055, then plateaus                                  │
└─────────────────────────────────────────────────────────────────────┘

┌─ Macro implications widget (per country) ──────────────────────────┐
│  Country: Germany                                                    │
│                                                                      │
│  Working-age growth 2025-2050:    -8%                                │
│  Implied trend GDP growth drag:    -0.4pp/yr                         │
│  Old-age dependency 2025:          38% → 2050: 60%                   │
│  Implied savings rate:             -2pp by 2050 (life-cycle model)   │
│  Implied real rate:                +30bp by 2050 (savings ↓)         │
│  Implied long-horizon CPI bias:    +0.2pp by 2050 (labor scarcity)   │
│                                                                      │
│  [Methodology: ageing-CPI model from Goodhart-Pradhan (2020)         │
│   + Mauro-Zhou (2020) implications-of-aging panel]                   │
└─────────────────────────────────────────────────────────────────────┘
```

## The animated age pyramid as the headline

The animated age pyramid is the **single most viral** visualization in long-horizon macro. Watching Japan's pyramid invert from 1950 to 2100 is more persuasive than any number. OPENGEM's pyramid:

- Scrubbable year by year, 1950-2100.
- Click "play" → animates the transition with cohort labels (e.g., "1980s baby boom passes age 65 in 2050").
- Toggle: side-by-side comparison of two countries (Japan vs Nigeria, China vs India).
- Export as MP4 / GIF for embeds — a "shareable demographic destiny" object.

This is the page's *acquisition vector*. A 30-second age-pyramid GIF posted on a YouTube short or a Substack draws traffic.

## The macro-implications widget

The widget on the workforce panel is where demography earns its keep as *macro*. Per country, it shows:

- Working-age population growth → trend GDP drag (via labor-input contribution).
- Old-age dependency → savings rate via the life-cycle model.
- Savings rate → real interest rate via the saving-investment balance.
- Old-age dependency → long-horizon CPI bias via labor scarcity / wage demands (Goodhart-Pradhan thesis).

The methodology is *linked, not hidden*. Each implication carries a `info` icon → pop-up explaining the model + the literature. This is *the* page where demographic determinism gets quantified with intellectual honesty.

## Data sources / adapter dependencies

| Input | Source | Adapter | Status |
|---|---|---|---|
| UN WPP 2024 (medium variant + probabilistic intervals) | UN Population Division | `opengem-data-unpop` ⚠️ NOT YET BUILT | gap |
| Wittgenstein Centre multidimensional projections | Wittgenstein Centre | `opengem-data-witt` ⚠️ NOT YET BUILT | gap |
| UN Urbanization Prospects | UN Population Division | `opengem-data-unpop` extension | gap |
| Migrant stock | UN Pop Div | `opengem-data-unpop` extension | gap |
| Migrant flows | OECD IMD | `opengem-data-oecd-imd` ⚠️ NOT YET BUILT | gap |
| Population by age & sex (current) | World Bank + national stats | `opengem-data-wb` | partial |
| Macro implications model | Goodhart-Pradhan replication, Mauro-Zhou replication | `opengem-demo-macro` ⚠️ NOT YET BUILT | gap |

**Identified gaps**: UN Population Division adapter (foundational), Wittgenstein, OECD migration. The page is *moderately gap-blocked* but the highest-priority gap (UN WPP) is straightforward — the data is open CSV/XLSX with well-documented schema.

## JSON contract — per-country headline

```json
{
  "country": "JPN",
  "vintage": "2026-06-06",
  "source": "UN WPP 2024 median variant",
  "population_M": {"2025": 124.5, "2030": 121.8, "2050": 104.6, "2100": 73.6},
  "population_M_p20_p80": {
    "2050": {"p20": 100.2, "p80": 109.1},
    "2100": {"p20": 64.8, "p80": 82.3}
  },
  "fertility_tfr": {"2025": 1.30, "2050": 1.46, "2100": 1.65},
  "life_expectancy_y": {"2025": 84.3, "2050": 88.1, "2100": 91.5},
  "age_structure_2025": {
    "share_0_14_pct": 12.0,
    "share_15_64_pct": 58.9,
    "share_65_plus_pct": 29.1
  },
  "age_structure_2050": {
    "share_0_14_pct": 9.5,
    "share_15_64_pct": 52.0,
    "share_65_plus_pct": 38.5
  },
  "dependency": {
    "total_dependency_ratio_2025": 0.78,
    "old_dep_ratio_2025": 0.52,
    "young_dep_ratio_2025": 0.26,
    "total_dependency_ratio_2050": 0.96,
    "old_dep_ratio_2050": 0.74,
    "young_dep_ratio_2050": 0.22
  },
  "urbanization_pct": {"2025": 91.9, "2050": 95.4, "2100": 97.5},
  "macro_implications": {
    "working_age_change_2025_2050_pct": -19,
    "implied_trend_gdp_drag_pp_per_year": -0.6,
    "implied_savings_rate_change_pp": -4,
    "implied_long_real_rate_change_bp": +40,
    "implied_long_cpi_bias_pp": +0.25,
    "methodology": ["goodhart-pradhan-2020", "mauro-zhou-2020"]
  },
  "cite_this": "https://opengem.org/demography/jpn?v=2026-06-06"
}
```

## What this loop produced

- The four-panel layout: population + age structure + urbanization & migration + workforce.
- An animated age pyramid as the visual headline + acquisition vector.
- A macro-implications widget translating demographic facts into GDP / savings / rates / CPI implications.
- The UN WPP 2024 + Wittgenstein integration plan.
- Six adapter gaps named.

## What comes next

- **L230** long-horizon scenarios (consumes demography + climate jointly).
- **L222** climate-macro (SSPs share population assumptions).
- **L213** recession prob — demographic trend GDP is a baseline input.

## Related

- [[L001-vision-statement]]
- [[L222-climate-macro-link]] — SSP population assumptions
- [[L230-long-horizon-scenarios]]
- [[L219-labor-market]] — workforce shorter-horizon
- [[L146-iconography-system]] — `globe`, `briefcase`, `clock`
