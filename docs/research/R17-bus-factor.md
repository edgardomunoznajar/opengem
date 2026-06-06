# R17 — Bus-Factor and Sustainability Plan

| Field | Value |
|---|---|
| Document ID | OG1-RES-017 |
| Revision | A (2026-05-24) |
| Date | 2026-05-24 |
| Status | **Operational sustainability plan — addresses R13 Attack #7 and #9.** |
| Authority | RSK-007 in master-doc v2.0 §9 |

---

## 1. The problem

OPENGEM is a single-maintainer project for the foreseeable future. Bus factor = 1. The 5-year vision (R100) requires this to evolve. The 90-day plan (R18) requires it to *survive* even if attention is intermittent. R17 spells out the mitigations.

## 2. Failure modes for a single-maintainer project

| Failure mode | Cause | Consequence |
|---|---|---|
| Maintainer hit by bus | Catastrophic external | System dies; data preserved if open |
| Maintainer loses interest | Attention drift | System decays; gradual quality loss |
| Maintainer drowns in other projects | Six-project context-switch tax | System updates fall behind; vintage discipline degrades |
| Adapter cohort breaks invisibly | Schema drift + lack of oversight | Bad data flows into forecasts; trust collapses if discovered |
| Public dashboard goes stale | Operational drift | Reputation cost |

## 3. Mitigations

### 3.1 Doc-as-code from day 1

Every architectural decision, ADR, design memo, V&V cell definition is in `docs/`. The current research round produced ~16 memos. Future decisions follow the same pattern. **Anyone (including the future maintainer's future self) can pick up the project state by reading docs.**

### 3.2 Mechanized correctness

Tests, CI, replay-and-diff (R16), and the V&V matrix (R08) all *mechanize* the things the maintainer would otherwise need to remember. The system is more like a watered plant than a juggled-balls act:

- Daily CI run = "is everything still working?"
- Weekly V&V matrix run = "are the forecasts still meaningful?"
- Monthly model card refresh = "did anything drift?"
- Annual L2 re-estimation = scheduled, not on-demand.

Maintainer can be absent for 30+ days and the system tells them what's broken when they return.

### 3.3 Alerting

GitHub Actions workflow + a simple email/webhook on:
- CI failure
- Adapter outage > 24h
- Replay-and-diff failure
- V&V cell that previously passed now fails by > threshold
- Disk usage > 80% on data volume

The maintainer is paged only when something concrete is wrong, not on a schedule.

### 3.4 Public mirror

GitHub repository public from day 1. Anyone interested can fork. **Eventually** a second contributor may appear; the doc-as-code legacy makes onboarding tractable.

### 3.5 Bus-factor-aware design choices

- **R adapter for L2 via subprocess** (ADR-009) means L2 is one thin Python wrapper around a mature, externally-maintained R package. If maintainer attention is intermittent, L2 still works.
- **Upstream-agency adapters** are isolated; one breaking doesn't break others.
- **Reproducibility architecture** (R16) means a future maintainer can verify what the current pipeline is doing without trust in the original maintainer.

### 3.6 Escalation triggers

If certain conditions arise, the project enters a different mode:

| Trigger | Action |
|---|---|
| 90+ days without any commit | Public README banner: "project in low-maintenance mode" |
| Maintainer pre-announced absence | Pause public dashboard; archive vintages continue; commits paused |
| Co-maintainer recruited | Update README; share ops responsibility |
| Foundation/non-profit fork | Hand-off documented in `docs/governance/handoff.md` |

### 3.7 Year-2 explicit reckoning

At v0.4 milestone (estimated ~12 months post-IOC), the program owner explicitly answers:

1. Has OPENGEM been used in any of the personal use cases (R15) in the past 90 days?
2. Has any time been spent on it in the past 30 days?
3. Are there V&V cell failures or adapter outages older than 14 days?
4. Is there at least one external person who would care if it went away?

**Score interpretation**:
- 4 yes: project is healthy; proceed to Block II/III.
- 3 yes: project is fine; address the failing dimension.
- 2 yes: project is at risk; reduce scope or recruit help.
- 0–1 yes: project is unsustainable; honest sunset.

## 4. Operational rituals

These small habits keep the system alive:

| Ritual | Frequency | Time cost |
|---|---|---|
| Glance at CI status | Daily | 30 sec |
| Read incoming-alert summary | Weekly | 2 min |
| Review V&V matrix dashboard | Weekly | 5 min |
| Update model cards if anything material changed | Monthly | 15 min |
| Re-tag latest stable release | Quarterly | 10 min |
| Annual L2 re-estimation kick-off | Once a year | 1 h |
| Annual retrospective + decision review | Once a year | 4 h |

Total non-development overhead: **≤ 2 hours/month** if nothing's broken. **≤ 4 hours/month** with normal-grade issues.

## 5. The unsentimental sunset clause

If the year-2 reckoning fails decisively:

1. Public README updated: "OPENGEM is archived. Forecasts continue to be served from frozen pipeline through {date}, after which the system goes read-only."
2. Final V&V report published. Honest accounting of what worked and what didn't.
3. Code remains public under Apache-2.0.
4. Domain (if registered) redirects to the GitHub repo.
5. Owner-time freed; no shame in the failure.

The discipline of a clean sunset clause is itself a sustainability mechanism — it reduces the sunk-cost burden of keeping a dead system alive out of guilt.

## 6. What this memo is *not*

Not a productivity plan; not an attempt to make a single maintainer do the work of three. It's an acknowledgment that the project's odds of long-term survival depend more on **the architecture's tolerance for inattention** than on the maintainer's heroism.

## 7. Bottom line

OPENGEM is designed to tolerate intermittent maintenance, document its own state, mechanize correctness, alert only when concrete things are wrong, and sunset cleanly if year-2 reality demands it. **The single-maintainer risk is real but bounded.**

---

*End of R17 Rev A.*
