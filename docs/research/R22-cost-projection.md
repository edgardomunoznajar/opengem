# R22 — 5-Year Cost Projection

| Field | Value |
|---|---|
| Document ID | OG1-RES-022 |
| Revision | A (2026-05-24) |
| Date | 2026-05-24 |
| Status | **Operational cost projection aligned with R100 vision arc.** |

---

## 1. Why this exists

The CONOPS rev C makes USD 200/mo informational rather than binding. Knowing the realistic 5-year trajectory is still useful — both for the owner's budgeting and as a transparency artifact (people will ask).

## 2. Block I (Year 0–1)

Per master-doc v2.0 §7.3:

| Line | Estimate (USD/mo) |
|---|---|
| Primary VM (Hetzner CCX23) | 30–50 |
| Annual L2 re-est. burst (amortized) | 5–10 |
| GPU bursts (Modal/RunPod) | 10–30 |
| Storage | 5–10 |
| Egress + dashboard | 5–10 |
| Contingency | 10 |
| **Total** | **65–120** |

**Annual Block I total**: ~USD 800–1500.

## 3. Block II (Year 1–2)

Adds:

| Line | Δ from Block I | Notes |
|---|---|---|
| Secondary VM (for L2 routinely) | +50/mo | L2 re-est. moves from annual burst to quarterly burst |
| Custom topic model training (Bybee-style) | +25/mo amortized | One-time training cost amortized |
| Wider sectoral data adapters | +10/mo | More API requests |
| Optional: Consensus Economics archive | +X/mo | Variable; only if owner decides to pay |

**Block II total (excl. Consensus)**: ~USD 150–250/mo.

## 4. Block III (Year 2–3)

Adds (if hosted-sovereignty pursued):

| Line | Δ from Block II | Notes |
|---|---|---|
| Multi-tenant infrastructure | +100/mo | Per-country isolation; load balancer; auth |
| Backup VM (HA) | +50/mo | Up-time becomes meaningful for hosted users |
| Daily-frequency adapters | +20/mo | High-freq data ingestion |
| Custom GPR-equivalent index pipeline | +15/mo amortized | News-corpus storage + ML training |

**Block III total**: ~USD 350–500/mo. Begins to require either sustained owner commitment or external funding.

## 5. Block IV (Year 3–4)

Adds:

| Line | Δ from Block III | Notes |
|---|---|---|
| Annual report production | One-time/yr | Negligible monthly cost |
| Standard-dataset hosting (publishing) | +30/mo | More egress; possibly CDN tier |
| Foundation incorporation costs | One-time | $500–$5k legal/registration |
| Co-maintainer compensation | +X/mo | Depends on hours; could be volunteer |

**Block IV monthly run-rate**: ~USD 400–600/mo. Now reasonably-sized for foundation funding or grants.

## 6. Block V (Year 4–5)

Steady-state per Block IV.

## 7. Cumulative 5-year operational cost (excl. one-time)

| Block | Monthly | Annual | 5y running |
|---|---|---|---|
| I | $90 | $1080 | ... |
| II | $200 | $2400 | $3480 |
| III | $425 | $5100 | $8580 |
| IV | $500 | $6000 | $14580 |
| V | $500 | $6000 | **$20580** |

**Total 5-year cost ceiling**: ~USD 20–25k cumulative cloud/infra spend.

For comparison: a single year's NiGEM subscription is USD 80–150k. Oxford GEM is USD 50–250k. OPENGEM's 5-year cumulative cost is **less than 1 month** of a NiGEM subscription.

## 8. Hidden costs not in this projection

Acknowledged but not quantified:

- **Developer time** at opportunity cost — significant but not cash-flow.
- **One-time legal review** at any point: ~$2–5k.
- **Security audit** at any public-launch point: ~$5–15k.
- **Potential paid-data dependencies** (Consensus Economics, AIS, etc.) — variable, $0–$10k/yr per dependency.

These would only become commitments at Block III+ governance transitions. Block I is unambiguously sub-$1500/yr.

## 9. Cost discipline mechanisms

Per master-doc v2.0 ADR-014 and R99 §5:

- Any new paid-data dependency requires an explicit ECP per CMP.
- Monthly cloud bill alarm at USD 300; auto-alert.
- Quarterly cost report.
- Annual budget review at the year-2 reckoning (R17 §3.7).

## 10. Funding scenarios (if Block III+ pursued)

Per R20 Tree 8:

- **<$5k/yr**: paid data add-ons, occasional contractor sprints.
- **$5k–$50k/yr**: ~3-month contractor stretches or single foundation grant.
- **$50k+/yr**: 1 FTE co-maintainer; non-profit incorporation.

No commitment is made to pursue funding. The cost projection is *what it would cost if it happens*, not *what it will cost*.

## 11. Bottom line

OPENGEM is **structurally cheap**. Block I sits at ~$1000/yr. Even the 5-year vision arc tops out at ~$5000–6000/yr operational. The cost is small enough that the maintenance bottleneck is **owner attention, not money**.

---

*End of R22 Rev A.*
