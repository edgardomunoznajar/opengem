# R27 — Open Issues Catalog (Consolidated)

| Field | Value |
|---|---|
| Document ID | OG1-RES-027 |
| Revision | A (2026-05-24) |
| Date | 2026-05-24 |
| Status | **Consolidated TBR/TBD list across the research round. Ground-truth for the rev C SRR-2 walkthrough.** |

---

## 1. Why this exists

Open issues are scattered across R01–R26 + rev C CONOPS Appendix B + master-doc v2.0 Appendix B. R27 collects them in one place, severity-ranked.

## 2. Catalog

### 2.1 P0 — Resolve before SRR-2 sign-off

| ID | Issue | Source | Path to resolution |
|---|---|---|---|
| OI-001 | Final Tier-V country roster (Core + Extended) confirmed | R07 §3, CONOPS rev C §5.1.3 | Pull current ORDRA coverage matrix from OECD; finalize at SRR-2 |
| OI-002 | ORDRA full variable matrix per country (especially BRICS+) | R07 §5 | Same as OI-001 |
| OI-003 | Philly RTDSM and OECD ORDRA explicit ToS for caching | R02 §5, R05 §3 | Read agency T&Cs; document |
| OI-004 | ECB SDW redistribution clause for derived series | R05 §7 | Read ECB SDW terms |
| OI-005 | Confirm L3 MVP can clear C-01, C-02, C-03 V&V cells on US | R18 §6.4 | Phase 3 of first 90 days; concrete probe |

### 2.2 P1 — Resolve before CDR

| ID | Issue | Source | Path |
|---|---|---|---|
| OI-006 | NumPyro vs. statsmodels for V1 DFM | R14 §9 | SAD-time decision based on tooling fit |
| OI-007 | LightGBM vs XGBoost vs CatBoost for V2 ML residual | R14 §9 (carry from rev B TBD-002) | Pilot all three at IOC |
| OI-008 | L1 / L2 mapping for Path B (US-origin structural shocks) | R11 §3.2 | Detailed SSDD-006 work |
| OI-009 | Per-country recession dating proxy for non-US | R10 §8 | Use OECD CLI peak-to-trough as default |
| OI-010 | Country-specific term-spread confidence thresholds | R10 §8 | Per-country AUC; document at IOC |
| OI-011 | R adapter for L2 BGVAR: `rpy2` vs subprocess vs dagster-r | R04 §7 | Pilot at IOC; test in Docker |
| OI-012 | VB fallback validation for L2 | R04 §7 | Replicate one BGVAR example with VB; compare CRPS |
| OI-013 | ACLED ToS for private-non-commercial use | R05 §7 | Read ACLED license |
| OI-014 | WEO + OECD EO historical-vintage download paths | R08 §9 | Verify both archives are downloadable in bulk |
| OI-015 | Forward-curve historical archive per Tier-V country | R08 §9 | Per-country: FRB H.15 (US); BIS for non-US |

### 2.3 P2 — Resolve before v0.4

| ID | Issue | Source | Path |
|---|---|---|---|
| OI-016 | GPR-nowcast skill probe (build or defer SSDD-008 endpoint #2) | R10 §3.2, R06 §10 | 4-week probe at v0.4 planning time |
| OI-017 | Crisis-mode L2 on-demand re-estimation workflow pre-built | R13 §5 | v0.4 scope item |
| OI-018 | Bus-factor escalation plan formalized | R17 §3.7 | At v0.4 year-2 reckoning |
| OI-019 | Block II R99-style research round | R21, R23 | At Block I completion |
| OI-020 | Wayback-Machine synthetic vintages for select EM | R02 §8 | Block II R&D probe |

### 2.4 P3 — Defer to public-launch round (no current commitment)

| ID | Issue | Source | Note |
|---|---|---|---|
| OI-021 | Consensus Economics access | R01 §6, R05 §7 | Subject to budget decision |
| OI-022 | Commercial AIS feed | R05 §2.3 | Use PortWatch instead at IOC; revisit only if needed |
| OI-023 | "OPENGEM" name vs. realistic OECD-26 scope | R99 §0 | Defer the rename question |
| OI-024 | Public-launch security review | R26 §9 | When external users actually appear |
| OI-025 | Foundation incorporation governance | R21 §2 | Block III if reached |

## 3. Resolution mechanism

- P0: blocks SRR-2 sign-off.
- P1: must close before CDR (Critical Design Review).
- P2: tracked in `docs/issues/` as it materializes; not blocking earlier gates.
- P3: noted but explicitly out-of-scope; revisit at future research round.

## 4. Per-issue document template

Each issue eventually gets:

```yaml
# docs/issues/OI-NNN.md
id: OI-NNN
title: ...
status: open | in-progress | resolved | deferred
opened: YYYY-MM-DD
priority: P0..P3
owner: program-owner
source: R0x §y
description: ...
investigation: ...
resolution: ...
resolved_at: YYYY-MM-DD
```

## 5. Bottom line

25 open issues identified. **5 are P0 and must be addressed at SRR-2.** The rest are budgeted across CDR, v0.4, and explicit-defer buckets. This is normal for a pre-PDR design; the count is healthy, not excessive.

---

*End of R27 Rev A.*
