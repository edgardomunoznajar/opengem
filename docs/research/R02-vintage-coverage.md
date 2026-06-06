# R02 — Vintage Data Coverage Cliff

| Field | Value |
|---|---|
| Document ID | OG1-RES-002 |
| Revision | B (populated 2026-05-24) |
| Date | 2026-05-24 |
| Status | **Investigated — verdict: H-2 BROKEN as stated; HOLDS for a restricted country tier.** |
| Tests hypothesis | H-2 |

---

## 1. Hypothesis under test (H-2)

> Real-time *vintage* data is available for **≥40 countries** with ≥10 years of history for the OPENGEM Block I core variables: GDP (real and nominal), CPI (headline and core), policy rate, unemployment rate.

## 2. Tier map of vintage archives

Findings are organized by what's actually centrally available, not by what individual agencies sit on internally.

### Tier 1 — Rich, deep, single-country (US)

| Archive | Coverage | Earliest vintage | Variables (relevant to OPENGEM) |
|---|---|---|---|
| **Philadelphia Fed RTDSM** | US only | 1965Q4 (NIPA), various | Real/nominal GDP, GDP deflator, IP (total + manuf), CPI (headline), unemployment, M1/M2, reserves, GDI (added recently) |
| **ALFRED (Archival FRED)** | "Collection of vintage versions of U.S. economic data" — US-focused; international series carried in FRED are *not* archived with full vintage history | 2006 onward for FRED-API access | Same US variables, plus broader; **non-US series are not preserved as vintages** in ALFRED's archive |

Source: [Philadelphia Fed RTDSM](https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/real-time-data-set-for-macroeconomists); [ALFRED](https://alfred.stlouisfed.org/); [ALFRED at 15 — FRED blog](https://fredblog.stlouisfed.org/2021/04/alfred-at-15-archiving-fred-data-since-2006/).

**Implication for OPENGEM.** US is in the easiest tier — every Block I core variable, deep history, well-documented API. Policy rate is best taken from FRED (FEDFUNDS, DFEDTARU/L) where vintage isn't really a concept (rate decisions are dated and not revised).

### Tier 2 — Multi-country OECD vintage (the workhorse)

| Archive | Coverage | Earliest vintage | Variables |
|---|---|---|---|
| **OECD MEI Original Release Data and Revisions Database** (ORDRA) | 26 OECD countries: US, AU, AT, BE, CA, DK, FI, FR, DE, GR, IS, IE, IT, JP, KR, LU, MX, NL, NZ, NO, PT, ES, SE, CH, TR, UK | **January 1999** (continuous monthly vintages) | "Continuously updated monthly vintages" of MEI series — incl. real/nominal GDP, IP, CPI, unemployment, leading indicators, trade. |
| **Dallas Fed Real-Time Historical Database for the OECD** (Fernandez, Koenig, Nikolsko-Rzhevskyy 2011) | Same 26 OECD countries; 19 "core" since 1961 | **1962** (digitized from hard-copy MEI releases) | 13 quarterly variables per country: real/nominal GNP/GDP, GDP deflator, IP (total + manuf), capacity utilization, **unemployment rate**, **CPI**, money supply, capital, imports, exports, net capital movements |

Notable: the Dallas Fed dataset is intended to be **merged with current OECD ORDRA** to give a 1962→present vintage history for the OECD 26.

**Critical gap in Tier 2: policy rate.** OECD MEI carries interest rate series, but the ORDRA / Dallas Fed papers explicitly enumerate 13 variables that do *not* include a central-bank policy rate per country. Policy rates have to be sourced separately from BIS / central bank archives. See §4.

Sources: [Dallas Fed dataset description](https://www.dallasfed.org/research/international/oecd); [Fernandez-Koenig-Nikolsko-Rzhevskyy 2011 WP no. 96](https://www.dallasfed.org/~/media/documents/research/international/wpapers/2011/0096.pdf); [OECD on the ORDRA database](https://www.oecd.org/en/publications/undertaking-revisions-and-real-time-data-analysis-using-the-oecd-main-economic-indicators-original-release-data-and-revisions-database_146528313656.html).

### Tier 3 — Euro-area members deep dive

| Archive | Coverage | Earliest vintage | Variables |
|---|---|---|---|
| **EABCN Real-Time Database** (now hosted by **ECB SDW**) | AT, BE, DE, IE, IT, LU, NL, ES, UK (9 countries) | January 2001 monthly vintages; smaller subset since late 1999 | **>200 macroeconomic variables**, taken from ECB Monthly Bulletin tables |

Source: [EABCN RTD page](https://eabcn.org/data/eabcn-real-time-database); [ECB SDW RTD dataset](https://data.ecb.europa.eu/data/datasets/RTD/data-information); [Giannone et al. ECB WP 1145](https://www.econstor.eu/bitstream/10419/153579/1/ecbwp1145.pdf).

**Implication.** EABCN is a superset of OECD ORDRA for those 9 countries — richer variable set, including financial and credit aggregates. Useful for L3 nowcast features.

### Tier 4 — Country-specific real-time archives

| Country | Archive | Coverage | Note |
|---|---|---|---|
| Canada | **RT-CANSIM** (Statistics Canada) | 20 CANSIM tables since **January 2015** | National accounts, BoP, trade, employment. Compiled by Simon van Norden. |
| Canada | **Bank of Canada Staff Economic Projection Database** | ~20 policy-relevant variables; mostly NA + unemployment, prices, output gaps, interest rates; quarterly vintages **mostly from the 1980s/90s** | Long history; gaps in some series. |
| Australia | **ABS revision triangles** | "Made available on request" | Not a programmatic API. Practical only for batch loads. |
| US | (covered in Tier 1) | — | — |

Source: [Simon van Norden — Original Vintage Data Sources](https://svannorden.org/original-vintage-data-sources/); [ABS GDP Revisions Analysis](https://www.abs.gov.au/statistics/research/analysis-revisions-gross-domestic-product).

### Tier 5 — Emerging markets (the cliff)

**No centralized public vintage archive exists** for the major non-OECD emerging markets — Brazil, Russia, India, China, Indonesia, South Africa, Turkey (the OECD-subset members AU/KR/MX/CL are in ORDRA; the rest are not).

- **Banco de México** (Banxico SIE) and **Banco Central do Brasil** publish current revised series via API, but the searches surfaced **no documented public vintage tables** comparable to RTDSM/ALFRED/ORDRA.
- **IMF SDDS+** sets a *revision policy and transparency* standard for adherents, but **does not itself preserve vintages** — vintage preservation is left to source agencies.
- Croushore-Stark's foundational vintage work (1999, 2001, 2003) and subsequent surveys explicitly cite the US as the well-served case and do not enumerate EM-vintage archives.

The structural problem: vintage preservation is a *day-by-day* discipline. If an agency hasn't been preserving vintages from day 1, they can't be reconstructed — except by laborious hard-copy digitization (the Dallas Fed precedent for 1962–1998 OECD).

Sources: [IMF SDDS+ overview](https://dsbb.imf.org/sdds-plus/overview); [Croushore-Stark RTDSM paper, JE 2001](https://www.sciencedirect.com/science/article/abs/pii/S0304407601000720).

## 3. The OPENGEM coverage matrix (best-case, ignoring source-access issues)

Restricted to the four Block-I core variables. ✓ = full vintage history available without self-archiving; ◐ = partial (e.g., one variable missing, or covered by Tier 4 with gaps); ✗ = not available, must self-archive from 2026 forward.

| Country tier | n | GDP-real | CPI | Unemp. | Pol. rate | Source |
|---|---:|---|---|---|---|---|
| **US** | 1 | ✓ | ✓ | ✓ | ✓ (no-vintage rates) | RTDSM / ALFRED / FRED |
| **OECD core 19** (founders, deep MEI back to 1962) | 19 | ✓ | ✓ | ✓ | ◐ — must source from BIS / central banks separately | Dallas Fed + ORDRA |
| **OECD post-1999** (AU, KR, MX, CL, TR, IL, EE, LV, LT, SI, SK, HU, PL, CZ, CR — ORDRA only) | ~15 (depending on exact ORDRA roster) | ◐ (since 1999) | ◐ (since 1999) | ◐ | ◐ — BIS Policy Rates dataset is the cleanest mirror; vintages effectively-not-revised | ORDRA + BIS |
| **Euro-area extras via EABCN** (subset already in Tier 2; PT/FI gap) | — | ✓ | ✓ | ✓ | ✓ | EABCN/SDW |
| **BRICS + middle-tier EMs not in OECD** (BR, RU, IN, CN, ID, ZA, SA, AE, EG, NG, VN, TH, PH, MY, AR, CO, PE, …) | ~20+ | ✗ | ✗ | ✗ | ◐ — BIS Policy Rates covers ~38 economies | Self-archive from 2026 |

**Approximate totals at IOC (today, without self-archive backfill):**
- **Full Block-I vintage (all 4 vars, ≥10 years): ~25–28 countries** — US + OECD-26 with policy-rate added from BIS.
- **Partial (3/4 vars, ≥10 years): ~25–28 countries** (same set; missing one or two depending on definition rigor).
- **No vintage at all (rely on self-archive from 2026): ~50+ countries** if FOC target is "≥80 economies."

## 4. The policy-rate footnote

Policy rate is conceptually different from GDP / CPI / unemployment for vintage purposes: **central-bank decisions are dated events, not later-revised series.** A policy-rate "vintage" effectively equals the *recorded decision history*, which is almost universally available from:

- **BIS Policy Rates dataset** — covers 38 central banks, daily history, programmatic access via BIS Data Portal.
- Each central bank's own decision archive (FRED for the Fed; ECB SDW for the ECB; etc.).

So **policy rate is a near-non-issue** for OPENGEM's vintage discipline. The "vintage" record is just the dated decision; revisions essentially never happen except for inflation-index linkage adjustments that are explicit.

That means the binding gap is in **GDP, CPI, unemployment** — these *are* revised and *do* require true vintage preservation.

## 5. Self-archive cost rough estimate

If OPENGEM mirrors every weekly release of every series of interest from 2026 onward:

- ~50 series × ~80 countries × monthly cadence ≈ 4k observations / month at archival snapshot grain.
- Storage: trivial. Even at 1KB per observation per snapshot with weekly cadence over 10 years: ~5 × 50 × 80 × 52 × 10 × 1KB ≈ 10 GB raw. Negligible vs. baseline node's 500 GB.
- API hit rate: also trivial under any reasonable rate-limit policy (R05 will confirm per-source).
- **The expensive thing is calendar time:** the first useful self-archived vintage for a Tier-5 country in 2026 produces its first vintage-correct backtest pair in ~2027 (one year of release history). The first useful 4Q-ahead backtest at the 2014–2025 horizon **cannot be reconstructed** for Tier-5 countries — that window is permanently lost.

## 6. Verdict on H-2

**H-2 as stated is broken.** OPENGEM **cannot** field a vintage-correct backtest leaderboard for "≥40 countries × 4 variables × ≥10 years of history" today. The honest ceiling is:

- **~26 countries** at Tier 2 quality (OECD ORDRA + BIS policy rates) for 1999-onwards vintages on GDP/CPI/UR.
- **~19 countries** with 1962-onwards depth via Dallas Fed extension.
- **1 country** (US) with the gold-standard archive.
- **0 EM countries** outside the OECD-26 subset can have a vintage-correct backtest before ~2028 (start self-archive 2026; need 2y of release history for one 4Q comparison).

H-2 **holds** if we restrict the CONOPS coverage promise to the OECD-26 subset for vintage-correct backtests, and accept that "≥40 / ≥80" is either (a) a *tracking* (not backtesting) promise for non-OECD countries until self-archive matures, or (b) abandoned at IOC and re-targeted for Block II / FOC.

## 7. Decision implications for the CONOPS

Concrete amendments required if program owner accepts this finding:

| Source | Current text | Proposed change |
|---|---|---|
| `StRS-001` | "≥40 economies at IOC and ≥80 at FOC" | Split: **vintage-eligible economies** ≥25 at IOC, ≥30 at FOC (limited by ORDRA roster + Euro 9 + Canada + Australia-on-request); **tracked economies** ≥40 at IOC, ≥80 at FOC (where "tracked" = latest revised values, no vintage backtest) |
| `POL-03` | "Backtests using revised data are categorically prohibited from the leaderboard" | Keep as-is **for vintage-eligible tier**; introduce a separate "latest-revised" leaderboard category for tracked-only countries, clearly labelled and statistically discounted |
| `FR-DAT-002` | "Every ingestion shall write a new vintage row; revisions shall not overwrite prior values" | Keep as-is for the OPENGEM ingestion layer (self-archive from 2026 is still strict). Add `FR-DAT-002b`: for tracked-only countries, vintage history before 2026 is acknowledged as unavailable and is not synthesized. |
| `CONOPS §5.1.1 / §1.2` | "Multi-country" framing | Add a tier explanation in §5.1.2 Scope: **Tier-V (vintage-eligible)** vs **Tier-T (tracked-only)** with the rosters spelled out. |
| `CONOPS §8.3 V&V primary metric` | "Beat AR(1) on ≥75% of covered countries at 4Q GDP" | Replace "covered" with "**Tier-V vintage-eligible**" for the binding gate. Add a softer Tier-T metric for additional countries. |
| `RSK-001` (L=4 I=4 currently) | "Vintage data unavailable for many emerging markets" | Re-score to L=5 I=4 = 20 (now a confirmed reality, no longer probabilistic). Mitigation already implicit in the Tier-V/Tier-T split. |

## 8. Open probes (deferred)

1. **Confirm BIS Policy Rates programmatic access** (will be in R05; expected easy).
2. **Negotiate / request ABS Australia revision triangles** as a small one-off batch load to upgrade Australia from "on request" to "loaded once." Trivial if owner emails ABS Stats.
3. **Wayback-Machine synthetic vintages** for a few high-priority EM agencies (BR, MX, IN) to see if release-archive scraping can backfill *some* vintage history. Likely partial and noisy; flag as Block-II if anyone is interested.
4. **OECD ORDRA exact roster check** — the literature varies between "26 countries" and slightly different lists; pull the current ORDRA roster from OECD directly to nail down which of MX/TR/CL/IL are fully in scope.

## 9. Bottom line for the CONOPS rebaseline

Set realistic expectations: **OPENGEM is, in 2026, an OECD-26-plus-self-archive system at best.** Calling it "Open Global" is aspirational past the OECD perimeter. Either (a) accept the tier split openly and re-target the global ambition for Block II/III (when self-archive matures), or (b) re-name and re-scope as an "OECD-vintage-correct economic monitor" with FOC defined more honestly.

The 3-layer hybrid architecture is *not* what's broken here. The data foundation is. Architecture choices in R03/R04 should assume the Tier-V ≈ 25-country reality.

---

*End of R02 Rev B.*
