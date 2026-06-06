# R06 — Wider Information Surface: Markets, Supply Chain, Geopolitics, Media

| Field | Value |
|---|---|
| Document ID | OG1-RES-006 |
| Revision | B (populated 2026-05-24) |
| Date | 2026-05-24 |
| Status | **Investigated — verdict: H-6 HOLDS with per-domain treatment recommendations.** |
| Tests hypothesis | H-6 |

---

## 1. Hypothesis under test (H-6)

> The OPENGEM information surface should be **wider** than CONOPS §5.1.2: financial markets, supply chain, geopolitical risk, and media awareness should each enter the system — minimally as inputs, ideally as first-class observables with their own forecast and nowcast endpoints.

**Verdict: holds.** Each domain has published evidence of forecasting power above standard macro covariates, and each has a free or low-friction data path. But the right *treatment* differs by domain. See §6.

The three treatment options from R06 rev A:
- **T-A:** inputs only — feed into the L3 DFM/ML residual as covariates. No new endpoints.
- **T-B:** parallel "Situation" subsystem — nowcast each domain's own indices, publish with own model cards.
- **T-C:** structural integration into L1/L2 (Block II/III aspiration; out of scope here).

## 2. D-MKT — Financial markets

### Evidence

- **Yield curve and recessions.** Bauer & Mertens (FRBSF 2018) — using 1972–2018 monthly data, **the 10y–3m term spread is "a strikingly accurate predictor of future economic activity"; every U.S. recession in the past 60 years was preceded by a negative term spread.** The 10y–3m outperforms the 10y–2y by a noticeable margin on AUC. The signal does not vanish in the post-2008 low-rate environment. (Source: [FRBSF Economic Letter 2018-07](https://www.frbsf.org/wp-content/uploads/el2018-07.pdf); [Bauer-Mertens Annual Review of Financial Economics survey](https://www.annualreviews.org/content/journals/10.1146/annurev-financial-100620-065648).)
- **International term-spread evidence** is weaker and country-specific — works in most OECD economies but with lower AUC and more false signals in the early 2000s. (Multiple SF Fed / ECB working papers cited in the surveys.)
- **Credit spreads** (Gilchrist-Zakrajšek-style excess bond premium) are independently informative about future industrial production and employment.
- **Implied-rate paths from policy-rate futures** (SOFR / Eurodollar / OIS) are the *competitor* to OPENGEM at the short end. OPENGEM should not try to beat the market's implied path on policy rate at 1Q–4Q; instead, it should be *consistent* with the implied path and add value via density and through-cycle paths.

### Source path (private project, programmatic)

- **FRED** carries Treasury yields, term spreads, federal funds target, OIS rates, S&P 500, VIX, BAA-10y, AAA spreads. Free API.
- **ECB SDW** carries euro-area swap curves, equity indices, sovereign spreads.
- **BIS Data Portal** carries sovereign yield curves for ~30 economies and policy rate decisions for 38.
- **Equity / FX**: Yahoo / Stooq / EOD-Historical-Data / FRED-mirrored series. Daily granularity is trivial.
- **Commodities**: EIA (oil, gas, electricity), FRED (industrial commodity indices), LME for metals if needed.

### Treatment

**T-A primary, T-B for one specific add-on.**

- **T-A:** include yield curve spreads (10y–3m, 10y–2y), credit spreads (BAA–10y, EM CDS), equity index returns, FX returns, oil and metals price changes as **covariates in L3 DFM/ML**. These are the canonical "financial conditions" features. Effectively free in engineering cost once R05 confirms FRED + BIS access.
- **T-B add-on:** publish a small `/v1/recession-probability?country=&horizon=` endpoint that surfaces a term-spread-based recession probability for each Tier-V country (R02). Single-model, transparent, model-card-clean. This becomes a separate leaderboard category vs. consensus recession-probability estimates and against the OECD's own composite leading indicator.
- **Reject T-C** at Block I: financial markets are *not* first-class state variables in L1/L2 in this round. Defer to Block II/III.

## 3. D-SCN — Supply chain

### Evidence

- **NY Fed GSCPI** integrates **>27 variables** including container shipping costs (HARPEX, Baltic Dry, BDI sub-indices, container freight rates), airfreight cost indices, and PMI delivery-time / inventories / order-backlog sub-components for seven economies (US, EA, UK, JP, CN, KR, TW). Published as a z-score; available monthly since 1997. (Source: [NY Fed GSCPI page](https://www.newyorkfed.org/research/policy/gscpi); [Benigno-Di Giovanni-Groen-Noble methodology paper SR1017](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr1017.pdf).)
- **Forecast power.** GSCPI "demonstrates significant predictive power for inflation outcomes," particularly **producer price inflation in the US and euro area**, assessed via local projections. The index is a clean source of variation that the standard macro model misses.
- **IMF PortWatch** (Carrière-Swallow et al.) provides port-call density and waiting times for thousands of ports, derived from AIS. Public dataset.
- **AIS access** is the practical question: UN Global Platform aggregates (free), Marine Cadastre (US, free), commercial Spire / MarineTraffic (paid). PortWatch already does the synthesis — preferable to consuming raw AIS.

### Source path

- **GSCPI**: monthly CSV from NY Fed, free, no auth, very long history. Trivial ingestion.
- **PortWatch**: IMF-hosted dashboard with downloadable port-level series.
- **Baltic Dry / freight indices**: some free, some paid via Drewry / Freightos. Use what's free at IOC.
- **Inventory-to-sales**: Census M3 (US), Eurostat (EA), monthly cadence.

### Treatment

**T-A only at IOC.**

- Consume GSCPI directly as an L3 covariate. Do not rebuild it.
- Optionally consume PortWatch composite + Baltic Dry as additional features.
- **Do not** at IOC try to publish a competing supply-chain index. The GSCPI is already the canonical benchmark; matching it adds no signal and creates a maintenance burden.
- **T-B revisit at v0.4:** *if* GSCPI proves to be a dominant L3 feature for inflation nowcasting, consider publishing a "GSCPI nowcast" (i.e., predict next-month GSCPI from real-time inputs) — that *would* be a new contribution.

## 4. D-GEO — Geopolitical risk

### Evidence

- **Caldara-Iacoviello GPR Index** ([FRB IFDP 1222](https://www.federalreserve.gov/econres/ifdp/files/ifdp1222.pdf)): tally of newspaper articles covering geopolitical tensions, eight categories (war threats, peace threats, military buildups, nuclear threats, terror threats, beginning of war, escalation of war, terror acts).
  - **Recent index**: 10 newspapers, monthly, since 1985.
  - **Historical index**: 3 newspapers, monthly, since 1900.
  - **Country-specific indexes for 44 countries** (advanced + emerging).
  - **Macro effect documented**: "higher geopolitical risk foreshadows lower investment, stock prices, and employment."
  - Free download at [matteoiacoviello.com/gpr.htm](https://www.matteoiacoviello.com/gpr.htm) and on [policyuncertainty.com](https://www.policyuncertainty.com/gpr.html); replication code on [openICPSR](https://www.openicpsr.org/openicpsr/project/154781/version/V1/view).
- **ACLED / GDELT / ICEWS** give finer-grained event data. ACLED has license restrictions for commercial use but is free for academic/personal/non-commercial. GDELT 2.0 is free, bulk-downloadable, very high volume.
- **Sanctions lists** (OFAC, EU, UN) are free and programmatic; useful for binary indicators.

### Source path

- GPR: monthly CSV, instant ingestion.
- GDELT GKG: free bulk download (gigabytes/month); meaningful preprocessing required.
- ACLED: API + bulk for academic; check ToS for private-research use.
- Sanctions: OFAC SDN list (XML/CSV), EU CFSP list, UN consolidated list.

### Treatment

**T-A core + T-B for one specific contribution.**

- **T-A:** ingest the country-level GPR as an L3 covariate for each of the 44 countries it covers. Use the eight category-decompositions where available. Cheap.
- **T-B candidate:** a **GPR nowcast / short-horizon forecast** endpoint — "given today's news flow, where is country-X's GPR index heading over the next 1–3 months?" This is something the academic index does not provide (Caldara-Iacoviello publishes monthly with a small lag). A nowcast at daily granularity would be a useful add. Defer the build until R03 confirms whether the marginal accuracy of GPR-nowcasting actually exceeds the cost.
- **Reject T-C** at Block I.

## 5. D-MED — Media awareness

### Evidence

- **Bybee, Kelly, Manela, Xiu** ([NBER WP 26648](https://www.nber.org/system/files/working_papers/w26648.pdf) → published as *Business News and Business Cycles*, **Journal of Finance, 2024**, [DOI](https://onlinelibrary.wiley.com/doi/full/10.1111/jofi.13377)). Topic model on 800,000 WSJ articles 1984–2017. Topic-attention shares **track economic activity measures and have *incremental* forecasting power for macroeconomic outcomes above and beyond standard numerical predictors.** Also used to retrieve news-based narratives behind "shocks" in numerical data. (Note: my R06 rev A misnamed the fourth author as "Su"; it is **Xiu**.)
- **Shapiro-Sudhof-Wilson (San Francisco Fed)** sentiment indices show news-sentiment effects on consumer sentiment and inflation.
- **GDELT GKG tone series** can be ingested without a topic model and used as a coarse sentiment / event-attention covariate.

### Source path

- **GDELT GKG**: free bulk, very high volume (multi-GB/day). Tone, themes, NER. Preprocessing-heavy.
- **NewsAPI / Common Crawl News**: NewsAPI is paid past a free dev tier; Common Crawl News is free but large and noisy.
- **Wall Street Journal full-text**: paid licensed corpus; not feasible at private-project budget.
- **Building our own topic model**: requires a stable corpus (so probably Common Crawl News or a curated RSS aggregation), embeddings, BERTopic/LDA pipeline. Multi-week project.

### Treatment

**T-A only at IOC; T-B explicitly deferred.**

- **T-A:** ingest **GDELT GKG tone series**, aggregate to country × monthly granularity, feed L3 as a covariate. Cheap-ish (modulo storage). Aligns with current CONOPS treatment of GDELT.
- **T-B (custom topic model) deferred** beyond Block I. The Bybee et al. result is real and the Block-II case for building this is strong, but the engineering cost is too high to credibly hit IOC. Defer to v0.4 or Block II.
- **Reject T-C** at Block I.

## 6. Summary treatment matrix

| Domain | T-A (input) | T-B (own subsystem) | T-C (structural) | Rationale |
|---|---|---|---|---|
| **D-MKT** Markets | ✅ broad set: term/credit/equity/FX/commodities into L3 | ✅ one specific add: term-spread recession-probability endpoint | ⏸ Block II/III | Term spread is the cleanest, best-evidenced single-feature recession predictor; the rest are L3 covariates. Markets compete with us at short horizons; we don't compete with them. |
| **D-SCN** Supply chain | ✅ GSCPI + PortWatch as L3 covariates | ⏸ defer to v0.4 (GSCPI nowcast) | ⏸ Block II/III | GSCPI is already canonical; reinventing it is waste. A nowcast of GSCPI would be a genuine contribution, but defer until L3 shows it dominates. |
| **D-GEO** Geopolitical | ✅ GPR (44 countries) + sanctions indicators into L3 | ✅ GPR nowcast as separate endpoint (defer build until R03) | ⏸ Block II/III | Academic GPR is monthly with lag; daily nowcast is a real product gap. |
| **D-MED** Media | ✅ GDELT GKG tone series into L3 | ⏸ defer custom topic model to v0.4 / Block II | ⏸ Block II/III | Custom topic model is too engineering-heavy for IOC. The Bybee result is strong but the build is multi-week. |

## 7. Architecture impact

**New subsystem candidate: SSDD-008 "Situation Subsystem."** If T-B is adopted for D-MKT (recession probability) and D-GEO (GPR nowcast), the LOOP_PLAN gains one new SSDD covering both endpoints. The Scenario Subsystem (SSDD-006) and Backtest Subsystem (SSDD-007) need to be extended to handle these new forecast targets (each gets its own benchmark and metric set).

**No change to L1/L2/L3** at the model level — the wider information surface flows in as L3 covariates (T-A) or is published from a sibling subsystem (T-B). The 3-layer hybrid stays intact.

**New ICDs needed:**
- ICD-002 (REST): add `/v1/recession-probability` and `/v1/gpr-nowcast` (if T-B add-ons survive).
- ICD-003 (MCP): add corresponding tools / resources.
- ICD-001 (External data): add rows for GSCPI, PortWatch, GPR, GDELT GKG. R05 will treat these.

**No change to vintage discipline** — these wider surfaces don't pretend to vintage-corrected backtests in the same way as macro variables; their backtests use the index's own real-time publication record (which for GSCPI and GPR is already vintage-correct by construction).

## 8. Verdict on H-6

**H-6 holds.** Each of the four domains has published, citable forecast power for macro outcomes, free programmatic access, and a tractable treatment. The cost of inclusion (under T-A) is small — mostly an L3 feature expansion. The cost of T-B add-ons is bounded — two endpoints, each on top of a publicly available index.

Reject any framing that says "we should be wider still." Two further candidate domains (climate-energy coupling, deep sectoral) are explicitly out of Block I scope per the CONOPS, and nothing in this research changes that.

## 9. Concrete amendments to the CONOPS

| Source | Current text | Proposed change |
|---|---|---|
| **CONOPS §5.1.2 Scope** | "In scope: macro variables (GDP, CPI, policy rate, unemployment, FX), quarterly modeling, monthly nowcasting, scenario impulse responses, public leaderboard." | Add: "**Wider information surface**: ingested as L3 covariates — financial-conditions panel (term/credit/equity/FX/commodities), NY Fed GSCPI, IMF PortWatch, Caldara-Iacoviello GPR (44 countries), GDELT GKG tone. Published as separate endpoints: term-spread recession probability (Tier-V countries), GPR nowcast (44 countries, deferred build pending R03)." |
| **CONOPS §5.3.2 Capabilities** | CAP-01..CAP-11 | Add: CAP-12 Recession probability endpoint (v0.4); CAP-13 GPR nowcast endpoint (Block II candidate). |
| **Master-doc §4.1 Logical View** | Layers L1..L7 | Add a **"Situation"** stripe at L4 (alongside Forecast / Scenario / Backtest services) that hosts the term-spread and GPR-nowcast endpoints. |
| **Master-doc §0 Doc set** | SSDD-001..007 | Add **SSDD-008 — Situation Subsystem** (if T-B add-ons confirmed). |
| **LOOP_PLAN** | 27 iterations | Add Iter 19a — SSDD-008. |
| **R05 source list** | Existing | Append: GSCPI, PortWatch, GPR, GDELT GKG (already there but elevated to L3 covariate, not optional). |

## 10. Open probes deferred

1. **Bybee-style custom topic model**: revisit as a v0.4 / Block II candidate after at least the L3 baseline with GDELT-tone alone is benchmarked.
2. **AIS-direct ingestion** vs. PortWatch synthesis: keep PortWatch as the default; revisit only if PortWatch coverage becomes insufficient.
3. **GPR-nowcast accuracy probe**: small experiment using last 5 years of GPR data + GDELT covariates to see if a 30-day-ahead GPR nowcast has meaningful skill above persistence. Block-I decision gate for the T-B endpoint.
4. **Sanction-onset Granger causality**: small probe — do OFAC/EU sanction listings Granger-cause emerging-market spread widenings at high frequency? If yes, T-A is justified beyond a token feature; if no, sanctions become low-priority.

---

*End of R06 Rev B.*
