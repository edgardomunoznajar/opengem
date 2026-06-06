# R99 — Synthesis & CONOPS Rebaseline Recommendation

| Field | Value |
|---|---|
| Document ID | OG1-RES-099 |
| Revision | A (initial synthesis 2026-05-24) |
| Date | 2026-05-24 |
| Status | **Decision-ready: read this before approving any further work.** |
| Audience | Program Owner |

---

## 0. Executive Summary

After five investigations (R01–R05) and one scope expansion (R06), the original CONOPS (`OG1-CONOPS-001` rev B) and master design document (`00-master-design-document-v1.0.md`) are **partially load-bearing and partially aspirational.** The system is buildable. The system as currently described is *not* — at least three of its five load-bearing claims are broken or weakened in ways the design has to absorb before any code is written.

**The big four findings:**

1. **R02 — Vintage data does not exist for "≥40 countries."** It exists for ~25 (OECD-26 minus a few). The "global" in OPENGEM is, today, OECD-26. (See R02 §6.)
2. **R03 — The 3-layer hybrid is the wrong architecture for forecast accuracy.** L3 is the workhorse. L1 and L2 should be *narrative* and *scenario* satellites, not co-equal forecast producers. (See R03 §5.)
3. **R05 — FRED 2024 ToS prohibits archiving and ML training.** Hard. The data layer needs to source from upstream agencies directly, not from FRED. (See R05 §3.)
4. **R06 — A "Situation" subsystem should be added** for two new endpoints (term-spread recession probability, GPR nowcast). The architecture grows wider but stays disciplined. (See R06 §7.)

**The two smaller findings:**

5. **R01 — The V&V bar "beat AR(1) on 75%" is the wrong bar.** Easy for GDP, surprisingly hard for inflation. Variable×horizon matrix proposed. (See R01 §4.)
6. **R04 — BGVAR compute is fine.** Mature CRAN package; VB fallback; with R03's rescope, only annual re-estimation needed. Not a problem. (See R04 §5.)

**Recommendation: do the rebaseline. Issue CONOPS rev C and master-doc rev 2.0. Restart LOOP_PLAN.**

The alternative — proceeding under the rev B documents — produces a system that either falsely claims global coverage (because the data isn't there), spends engineering effort on L1/L2 layers that don't materially improve forecasts, or violates FRED's ToS the day it caches its first vintage.

---

## 1. The five hypotheses, status, and decisive evidence

| ID  | Hypothesis | Verdict | Decisive evidence |
|-----|-----------|---------|---------------------|
| H-1 | Beat AR(1) on 75% is ambitious for 4Q GDP density | **Partially holds; wrong bar.** It's a layup for GDP; surprisingly hard for inflation post-1985. | Faust-Wright (2013) handbook; D'Agostino-Gambetti-Giannone (2013) JoAE; Rossi-Sekhposyan (IJF 2014). |
| H-2 | Vintage data covers ≥40 countries × 4 vars × ≥10y | **Broken as stated.** Real-world ceiling is OECD-26 (~25 countries with full quartet incl. policy rate from BIS). | Philly RTDSM is US-only; OECD ORDRA = 26 OECD countries since 1999; Dallas Fed extends to 1962 for same set; no EM equivalent exists. |
| H-3 | 3-layer hybrid strictly dominates each layer alone, by margin worth the cost | **Weak.** Combination > single, but 3 > 2-or-1 not supported. L3 carries forecasts; L1/L2 carry narrative+scenarios. | Coulombe (2022/2024) ML-for-macro; Christoffel-Coenen-Warne ECB WP 1185 (DSGE vs BVAR); Chudik-Pesaran on GVAR forecast limits. |
| H-4 | BGVAR fits 4 vCPU / 16 GB at 40–80 countries with full MCMC | **Reframed (constraint removed by owner); holds anyway.** Mature CRAN package; VB fallback; R03 rescope drops cadence to annual. | Boeck-Feldkircher-Huber (JSS 2022); Crespo Cuaresma-Feldkircher-Huber (JoAE 2016); Koop-Korobilis VB validation. |
| H-5 | Sources permit automated programmatic access at our rates | **Holds for 10/12; FRED is the exception.** 2024 ToS prohibits caching and ML training. Substitute to upstream agencies. | FRED ToS June 2024 update. |
| H-6 | Wider information surface (markets/SCN/GEO/MED) should be in scope | **Holds.** Per-domain treatment recommended (T-A for D-MKT/SCN/MED; T-A+T-B for D-GEO and recession-prob endpoint). | Bauer-Mertens (2018); NY Fed SR1017 (GSCPI); Caldara-Iacoviello (2022); Bybee-Kelly-Manela-Xiu (JoF 2024). |

---

## 2. What changes — the rebaseline at a glance

### 2.1 What stays

- Open license posture (Apache-2.0 code, CC-BY-4.0 docs).
- Vintage-correct backtest discipline **for the tier where vintage exists**.
- BMA combiner — but now over L3 variants, not 3 layers.
- Public leaderboard concept.
- MCP-compatible interface (deferred monetization, kept for personal/agentic use).
- Three-layer code structure as a *staged ambition*; not as the Block-I architecture.

### 2.2 What changes

| What | From | To |
|---|---|---|
| **Coverage promise** | ≥40 economies at IOC, ≥80 at FOC, all density | **Tier-V** ≈ 25 economies vintage-correct at IOC; **Tier-T** for the rest as tracked-only (no leaderboard inclusion); Tier-V grows slowly as self-archive matures. |
| **Architecture critical path** | L1+L2+L3 with BMA over all three | L3 baseline; BMA over L3 variants. L2 invoked annually for scenario IRFs only. L1 reduced to US-only narrative layer. |
| **Cadence** | Quarterly full system run ≤4h | Quarterly L3 run ≤2h; annual L2 re-est. ≤12h; L1 (US) quarterly with L3. |
| **V&V framework** | Single "beat AR(1) on 75%" gate | Matrix per variable×horizon with WEO/OECD EO + forward-curve benchmarks. |
| **Data sources** | FRED + ALFRED authoritative | Upstream US agencies (BEA / BLS / FRB / Treasury / Census) authoritative; FRED for discovery only. ALFRED replaced by Philly RTDSM for US vintages. |
| **New subsystem** | None | SSDD-008 "Situation" — term-spread recession-probability + GPR nowcast endpoints. |
| **Wider information surface** | GDELT/AIS as alt-data L3 inputs only | Formal D-MKT/SCN/GEO/MED ingestion; specific endpoints from Situation subsystem. |
| **Cost envelope** | ≤USD 200/mo binding | ≤USD 200/mo informational; if L2 needs upsizing post-rescope, still likely inside. |

---

## 3. Concrete amendment list (collated from R01–R06)

The list of textual changes the CONOPS and master-doc need. Each row is small; together they constitute a clean rev C.

### 3.1 CONOPS amendments

| Section | Change |
|---|---|
| §1.2 System Overview | Replace "three estimation layers ... combined via BMA" with "L3 baseline forecast (BMA over DFM + ML variants). L2 invoked for spillover scenarios on demand. L1 (US-only at IOC) for structural narrative." |
| §4.1 Strategic Fit | Unchanged. |
| §4.2 Commercial Rationale | Mark "deferred — not in Block-I private-project scope per program-owner direction 2026-05-24." |
| §5.1.1 Objectives | Reorder: (1) Verifiability for Tier-V; (2) Coverage tiered Tier-V/Tier-T; (3) Interpretability + Accuracy; (4) Cost; (5) Integration. |
| §5.1.2 Scope | Explicit Tier-V / Tier-T split. Add wider info surface (markets/SCN/GEO/MED). |
| §5.2 POL-01 | Add FRED-substitution disclaimer per R05. |
| §5.2 POL-03 | "Vintage data only on leaderboard" applies to Tier-V; Tier-T countries get a separate tracked panel with no leaderboard inclusion. |
| §5.3.1 Block diagram | Redraw: L3 in critical path; L2/L1 as scenario/narrative satellites; new "Situation" stripe. |
| §5.3.2 Capabilities | Add CAP-12 recession-probability endpoint; CAP-13 GPR-nowcast endpoint (deferred build). Attribute CAP-01..05 to L3. |
| §5.4 Modes of Operation | M-03 monthly recalibration: L3 weights only. M-04 quarterly full run: L3 + L1 (US); L2 only if "annual" triggered separately. |
| §5.5 User Classes | Personal use (Edgardo as both U-02 and U-04). Drop unrealistic external personas. |
| §7.3 Financial | Restate at the new cadence; expected ~USD 50–100/mo more realistic than 200. |
| §8.3 V&V | Replace single bar with the matrix from R01 §4. |
| §8.4 CSF | CSF-04 hardware ceiling now informational. Add CSF-05: "Upstream-substitution adapters complete for US series by IOC." |
| §8.5 CFC | Update CFC-01 trigger (re-baseline at Tier-V failure); update CFC-02 (no auto-rebase; cost is informational). |
| Appendix B TBD/TBR | Resolve TBR-001 (country list = Tier-V roster). Resolve TBR-002 (Australia in Tier-V via ABS + OECD ORDRA). Resolve TBD-004 (L1 reduced; defer language choice). Add TBR-006: ACLED ToS for private-non-commercial. |

### 3.2 Master design doc amendments

| Section | Change |
|---|---|
| §0 Doc Set Index | Add OG1-SSDD-008 Situation Subsystem. |
| §3.1 FR-DAT-001 | New source list per R05 §6 (BEA/BLS/FRB/Treasury/Census + ORDRA + ECB SDW + BIS + Comtrade + GSCPI + GPR + GDELT). |
| §3.1 FR-MOD-001 | "Three estimation layers" → "L3 baseline; L2 scenario; L1 narrative (US-only at IOC)." |
| §3.2 NFR-PRF-003 | Restate per subsystem. |
| §3.2 NFR-COS-001 | Mark informational. |
| §4.1 Logical View | New diagram (see R03 §5.5 and CONOPS §5.3.1 redraw). |
| §4.4 ADR | ADR-005 rewrite (three layers, three jobs, not three forecasters). ADR-007 rewrite (BMA over L3 variants). Add ADR-009 (R for L2 via BGVAR package). Add ADR-010 (FRED-substitution). Add ADR-011 (Tier-V/Tier-T data split). |
| §5 SSDDs | SSDD-003 reduced to US-only. SSDD-004 cadence annual. Add SSDD-008. |
| §6 ICDs | ICD-001 rewrite per source list. ICD-002 add new endpoints. ICD-003 add new MCP tools. |
| §8 V&V | Replace §8.3 with R01 §4 matrix. |
| §9 Risk Register | Update RSK-001 to L=5 I=4 (confirmed reality). Update RSK-002 to L=1 I=2 (effectively resolved). Add RSK-011 (FRED ToS). |
| §10 WBS / Schedule | Per-subsystem cadence; IOC scope is Tier-V only. |
| §11 AGP | Gate criteria reference Tier-V. |
| Appendix B TBD/TBR | Resolutions per CONOPS list above. |

### 3.3 LOOP_PLAN amendments

| Section | Change |
|---|---|
| Iter 02 OG1-STRS-001 | Tier-V/Tier-T explicit. |
| Iter 03 OG1-SRS-001 | Replace single AR(1) gate with R01 §4 matrix. |
| Iter 04 OG1-SAD-001 | New ADR set; new logical view. |
| Iter 12 SSDD-001 | Upstream-agency adapter set, not FRED. |
| Iter 14 SSDD-003 | US-only at IOC. |
| Iter 15 SSDD-004 | Annual cadence; uses `BGVAR` R package. |
| Iter 19 SSDD-007 | Tier-V-only leaderboard; separate tracked panel. |
| **NEW Iter 19a** | **SSDD-008 Situation Subsystem.** |
| Iter 20 VVP | Matrix-based gates. |
| Iter 21 Risk | Per §3.2 above. |

---

## 4. The new program shape (one-paragraph version)

OPENGEM-1 Block I is a personal-use, open-source, **OECD-26-vintage-correct** macroeconomic forecasting and situation-awareness system. **L3 (DFM + ML residual + large BVAR variants combined by BMA)** is the baseline forecast producer for ~25 Tier-V countries, scored on a public leaderboard against AR(1), random walk, IMF WEO, OECD EO, and forward-curve benchmarks per a horizon×variable matrix. **L2 (Bayesian GVAR via the R `BGVAR` package)** is invoked on-demand for spillover scenarios and re-estimated annually. **L1 (single US semi-structural core)** provides shock identification and narrative for the Scenario Subsystem. A **Situation Subsystem** publishes a term-spread recession-probability endpoint (Tier-V countries) and, when the build proves valuable, a daily GPR nowcast (44 countries). The wider information surface (markets, supply chain, geopolitics, media) is ingested as L3 covariates from free public sources (GSCPI, PortWatch, GPR, GDELT GKG). The US data layer sources from upstream agencies (BEA, BLS, FRB, Treasury, Census) rather than FRED to comply with FRED's 2024 ToS. Tier-T countries are tracked from 2026 onward via self-archive; they appear in dashboards but not on the leaderboard.

---

## 5. Risks and unresolved questions after rebaseline

After the proposed rebaseline, the residual risks are:

| Risk | Severity after rebaseline | Comment |
|---|---|---|
| Tier-V backtests still don't beat the cell-specific V&V bars | High — the empirical risk doesn't go away by re-stating the bar | The matrix at least makes failure interpretable rather than catastrophic. |
| Upstream-agency adapter complexity (BEA, BLS, FRB, Treasury, Census) higher than FRED single-API | Medium | One-time engineering; well-documented APIs. |
| OECD ORDRA / Philly RTDSM ToS specifics not yet verified | Low | Both are research datasets by design; expected permissive. |
| L1 US-only core still a substantial build | Medium | Reduced from 25–80 per-country cores to 1; still nontrivial; defer to post-IOC if needed. |
| New Situation Subsystem adds scope | Low–Medium | Two endpoints, each on top of an existing public index. Smallest new SSDD. |
| Personal-use scope means single maintainer remains a risk | Medium | Mitigated by doc-as-code (existing). |

Open probes deferred (re-listed for tracking):

- [R02] BIS Policy Rates programmatic access details.
- [R02] Wayback-Machine synthetic vintage feasibility for EM.
- [R03] Whether scenarios actually want L1+L2 joint propagation.
- [R04] Concrete BGVAR memory benchmark on a small VM.
- [R05] Explicit ToS confirmation for RTDSM, ORDRA, ACLED, ECB SDW caching.
- [R06] GPR-nowcast skill probe (does it actually beat persistence?).
- [R06] Bybee-style custom topic model (deferred to v0.4+).

---

## 6. Decision the program owner needs to make

**One decision, three options.**

**Option A — Accept rebaseline.** Approve CONOPS rev C and master-doc rev 2.0 (drafts in this directory). Restart LOOP_PLAN with the new sequence. Begin upstream-agency adapter work in parallel with SAD/SSDD decomposition.

**Option B — Renarrow scope further.** Drop FOC ambition entirely. Block I final = "Tier-V OECD-26 with L3 baseline, no L1/L2, no Situation subsystem." Minimal product. Re-evaluate if it lands.

**Option C — Sunset the program.** The gap to FOC is too far; the FRED issue is too unrewarding to work around; the L1/L2 narrative value is not worth its build cost in private-project scope. Mothball cleanly, move attention elsewhere.

Recommendation: **A.** Option B is too austere — the wider information surface (R06) is a genuine differentiator and cheap to add. Option C dismisses a real opportunity: a personal-use OECD-26 vintage-correct forecasting system is *unique*; the existing free open systems (FRB/US, EAGLE, GVAR Toolbox) all fail one or more of {non-US, density, vintage, operational}. OPENGEM rev C meets all four. That's the actual market gap, and a personal project doesn't need a market.

---

## 7. What's in this directory now

- `R00-charter.md` — falsifiable-hypotheses framework
- `R01-accuracy-ceiling.md` — V&V matrix
- `R02-vintage-coverage.md` — Tier-V/Tier-T split
- `R03-hybrid-evidence.md` — L3-as-workhorse rescope
- `R04-bgvar-compute.md` — green-light with VB fallback
- `R05-source-access.md` — FRED-substitution plan
- `R06-wider-information-surface.md` — Situation subsystem
- `R99-synthesis.md` — this document

Concrete draft documents (next phase of this round; produced in parallel):
- `OG1-CONOPS-001-revC-draft.md` — see `../design/00-program/`
- `00-master-design-document-v2.0-draft.md` — see `../design/`
- `LOOP_PLAN-v2.md` — see `../design/`

---

*End of R99 Rev A.*
