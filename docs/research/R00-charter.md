# R00 — Research Charter

| Field | Value |
|---|---|
| Document ID | OG1-RES-000 |
| Revision | A (draft) |
| Date | 2026-05-24 |
| Posture | **Treat the existing CONOPS / master-doc commitments as falsifiable hypotheses.** |
| Scope | **Private project. No marketing / venture / monetization questions in scope yet.** |

---

## 1. Purpose

The CONOPS (`OG1-CONOPS-001` rev B) and the master design document (`00-master-design-document-v1.0.md`) already commit to:

- A specific architecture (three-layer hybrid: semi-structural country cores L1 + Bayesian GVAR L2 + DFM/ML residual L3, combined via BMA).
- A specific coverage promise (≥40 economies at IOC, ≥80 at FOC).
- A specific accuracy claim (beat AR(1) RMSE on ≥75% of countries at 4Q-ahead GDP; not statistically worse than consensus on ≥50%).
- A specific cost envelope (≤ USD 200/month sustaining).
- A specific compute envelope (4 vCPU / 16 GB / 1× A10G ephemeral).
- A specific data-vintage promise (vintage-correct backtests).

All six are load-bearing. If any one of them is wrong, the program's shape changes.

This document **opens those commitments for falsification** before any code is written. It is upstream of `LOOP_PLAN.md`, which (until this round closes) is paused.

## 2. Falsifiable hypotheses

Each hypothesis below is stated *strongly enough to break*. The corresponding research memo (R0n) gathers evidence to keep or kill it.

| ID  | Hypothesis (load-bearing claim from CONOPS / master-doc) | Memo |
|-----|------------------------------------------------------------|------|
| H-1 | Best-in-class operational forecasts beat AR(1) on ≥75% of country-horizon cells for 4Q GDP. (i.e. our V&V bar is genuinely ambitious, not a layup AR(1) loses anyway.) | R01 |
| H-2 | Real-time vintage data is available for ≥40 countries with ≥10 years of history for GDP, CPI, policy rate, and unemployment. | R02 |
| H-3 | The 3-layer hybrid (L1 country cores + L2 GVAR + L3 DFM/ML) strictly dominates each layer alone in published out-of-sample evaluations, by a margin that justifies the engineering cost of running all three. | R03 |
| H-4 | A Bayesian GVAR at 40–80 countries is computationally tractable for quarterly re-estimation on commodity hardware (size to be determined; **the 4 vCPU / 16 GB Block-I baseline is no longer a binding constraint** per program-owner direction 2026-05-24). The research question becomes: *what compute does BGVAR actually need, and where does the cost / wall-clock curve flatten?* | R04 |
| H-5 | All planned data sources (IMF IFS, WB WDI, OECD MEI, FRED, ECB SDW, BIS, Comtrade, GDELT, VIIRS, AIS, Google Trends, electricity load) permit automated programmatic access at the rates OPENGEM needs, in their current 2026 ToS. | R05 |
| H-6 | The OPENGEM information surface should be **wider** than CONOPS §5.1.2: financial markets, supply chain, geopolitical risk, and media awareness should each enter the system — minimally as inputs, ideally as first-class observables with their own forecast and nowcast endpoints. Added by program-owner direction 2026-05-24. | R06 |

Each memo's success criterion is **a clear keep/kill verdict with citations**, and an explicit list of what the CONOPS would have to change if the hypothesis breaks.

## 3. Out of scope for this round

Per program owner: this is currently a private project. The following questions are *not* researched here, even where the CONOPS makes claims about them:

- Incumbent (Oxford GEM / NiGEM / Moody's) pricing reality, customer churn, JTBD analysis.
- MCP-monetization comp-set, willingness-to-pay, ICP definition.
- Buyer set / pilot acquisition for OCR gate.
- Trademark / branding concerns ("OPENGEM" name).
- License / redistribution terms of downstream wrappers.

These are deferred to a future "public-launch readiness" research round.

## 4. Method

For each hypothesis:

1. **Specify the claim narrowly.** State it in falsifiable form with the exact threshold, scope, and metric.
2. **Gather evidence.** Web search + paper retrieval + agency documentation. Each non-trivial claim cited with a URL.
3. **Interpret.** Does the evidence support, weaken, or break the hypothesis?
4. **Decision implication.** If broken/weakened, list exactly what changes in CONOPS / master-doc / LOOP_PLAN.
5. **Open questions.** Note what's not answerable from desk research alone (would need a probe / benchmark).

Memos are short (target 2–4 pages) and **fact-dense, not narrative**. Inline citations preferred over a citations section.

## 5. Sequencing

Order chosen by combination of *(a) likely impact on program shape* and *(b) answerability from desk research*:

1. **R02 — Vintage data cliff** — concretely answerable, very high architectural consequence if broken.
2. **R06 — Wider information surface** — scope-defining; should resolve before deep dives into L1/L2/L3 architecture and ICDs, because it may add a whole new subsystem.
3. **R01 — Accuracy ceiling** — answerable from M4/M5/M6 + central-bank backtest literature.
4. **R03 — Hybrid architecture evidence** — answerable from forecasting literature; partially dependent on R06's outcome (does the architecture need to accommodate market/SCN/GEO/MED layers?).
5. **R04 — BGVAR compute** — partially desk-answerable; may need a small benchmark probe (deferred). Reframed as informational, not pass/fail.
6. **R05 — Source access** — clerical but necessary; per-source ToS scan. Now must include the wider information surface from R06.

## 6. Exit criterion

This round closes when:

- All five memos have a stated keep / weaken / kill verdict on their hypothesis.
- The R99 synthesis memo enumerates exactly which CONOPS sections need to change, with proposed amendments.
- Program owner has reviewed R99 and either (a) authorized a CONOPS rev C and a restarted LOOP_PLAN, or (b) sunset the program.

Until then: **no code, no decomposition of design docs below the master doc.**

---

*End of R00 — Research Charter.*
