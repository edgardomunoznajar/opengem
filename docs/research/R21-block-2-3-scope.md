# R21 — Block II and III Scoping (Preview)

| Field | Value |
|---|---|
| Document ID | OG1-RES-021 |
| Revision | A (preview only, 2026-05-24) |
| Date | 2026-05-24 |
| Status | **Preview for what comes after Block I. Not a commitment.** |
| Authority | R100 vision; R99 §3 carries forward "Block II/III deferred" items |

---

## 1. Block II — Width (Year 2 of the arc)

**Pre-condition**: Block I IOC + v0.4 + v1.0 cleared all V&V matrix cells with Tier-V Core; bus factor mitigations in place; program owner sustained ≥6 hr/month over 12 months.

### Scope additions

| Area | Block II addition |
|---|---|
| **Coverage** | Tier-V Extended fully validated and on the leaderboard (~35 countries). Tier-T graduates as self-archive matures (~40 countries by mid-Block-II). |
| **Sectoral** | Industry / services / agriculture splits for GDP where ORDRA + WB + Eurostat carry them. Adds ~5 series per country. |
| **L1 narrative** | Add UK, EA aggregate, and AU semi-structural cores. Now 4 countries with narrative-grade L1. |
| **Variables** | Add: trade balance, current account, fiscal balance, real effective exchange rate (BIS REER dataset). |
| **Wider info surface** | Custom topic model on news (Bybee-Kelly-Manela-Xiu replication) — if skill probe passes in Block I. |
| **Climate-energy** | Initial coupling: ENTSO-E + EIA + AEMO electricity load as L3 covariates; first carbon-intensity series. |
| **Public scoring** | Quarterly published comparison vs. WEO + OECD EO + Consensus (paid; consider access). |

### V&V matrix expansion

- Cells expand to Tier-V Extended (35 countries).
- Add new cells for sectoral GDP, current account, REER (12 new cells).
- Add MCS membership requirement on ≥50% of cells.

### Time budget

Block II is *significantly* more work than Block I. Estimated 12–18 months at 6–12 hr/week. Requires either (a) sustained owner commitment, (b) co-maintainer recruitment, or (c) explicit reduction of Block II scope.

### Failure mode

If Block II accelerates the maintenance burden beyond program-owner capacity, **freeze Block I as the released system and don't pursue Block II**. Better a polished smaller system than a stretched larger one.

## 2. Block III — Depth + Sovereignty (Year 3 of the arc)

**Pre-condition**: Block II completed; OPENGEM has 24+ months of operational history with vintage-correct backtests; demonstrated reuse in oblique suite.

### Scope additions

| Area | Block III addition |
|---|---|
| **Sovereign hosting** | Offer OPENGEM-style infrastructure to small economies that don't have their own model. Free or marginal-cost. Pacific Islands, small Caribbean, small African economies as first candidates. |
| **L1 expansion** | Country cores for the largest 10 economies (G7 + China + India + Brazil). |
| **Daily nowcasting** | Push to true daily granularity for short-horizon variables using high-frequency covariates. |
| **Custom geopolitical event model** | Replace the wrap on Caldara-Iacoviello GPR with an own-built GPR-style index updating daily from GDELT + ACLED. Forecast-of-the-GPR live. |
| **Forecast-of-leaderboard** | Meta-model that predicts when OPENGEM itself is most likely to be wrong, via regime-detection + structural-break indicators. |

### Governance evolution

By Block III, OPENGEM may have outgrown the single-maintainer pattern. R17 escalation triggers fire:

- Foundation incorporation (501(c)(3) or equivalent).
- Co-maintainer formalized.
- Public governance document with clear decision rights.

This is *governance* work, not *engineering* work. It's also where the program owner decides whether to remain the operator or hand off.

## 3. Block IV — Public Goods (Year 4)

**Pre-condition**: 3+ years of public V&V history; OPENGEM is cited by at least one external work.

### Scope additions

| Area | Block IV addition |
|---|---|
| **OPENGEM Dataset Standard** | Publish vintage archive + benchmark forecasts as a service for other open forecasters. Becomes a reference dataset for M-competitions. |
| **Annual "State of the Macro" Report** | Public-facing publication citing OPENGEM's own track record and naming both winners and losers in macro forecasting. |
| **University course materials** | Curriculum-ready modules using OPENGEM as live teaching laboratory. |

### Governance

Foundation-level governance fully active. Block IV is *not* a private-project scope; if reached, OPENGEM has outgrown its origins and is now an institution.

## 4. Block V — Reflection (Year 5)

**Pre-condition**: 5 years of cumulative operation.

### Activities

- Five-year retrospective: did OPENGEM beat consensus on Tier-V? Did it become a citation standard? Did it influence any incumbent's transparency? Honest accounting either way.
- Decision: continue, hand off to foundation, hand off to university, or sunset cleanly.

## 5. What stays out of Block II/III/IV/V scope

These are not pursued at any Block:

| Out of scope | Reason |
|---|---|
| High-frequency financial markets forecasting | Markets price themselves; we're not in that game |
| Sectoral micro-detail (industry codes) | Out of scope per CONOPS rev C |
| Country-specific policy advisory | OPENGEM forecasts; it does not recommend |
| Real-time options-implied densities for financial vols | Different toolchain; not a fit |
| AI/LLM-based "explainer" wrappers around forecasts | Acceptable as add-ons; not Block scope |

## 6. The Block discipline

Each subsequent Block requires its **own pre-PDR research round** before commitment. The R99-style synthesis becomes a recurring artifact:

- Block II R99 = Block II rebaseline.
- Block III R99 = Block III rebaseline.
- ... etc.

This is *not* automatic graduation. Each Block earns the next one.

## 7. Bottom line

Block II/III/IV/V are aspirational. They live in R100 (vision) and are previewed here so that Block I's discipline can be evaluated against whether it makes the later Blocks *possible*, not *required*. Block I is sized for sustainability; everything else is dream-big territory.

---

*End of R21 Rev A.*
