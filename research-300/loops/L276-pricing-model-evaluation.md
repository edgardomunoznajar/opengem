# L276 — Pricing Model: 4 Candidates Evaluated Against L006 Thesis

**Loop**: 276 / 300
**Phase**: 6 — Synthesis + launch
**Date**: 2026-06-06

---

## The thesis of this loop

[[L006-pricing-thesis]] picked a hybrid model anchored on white-label / embed (B), with MCP throughput (C) as the future-facing tier and API throughput rebuilt as an underlying capacity (A). [[L260-pricing-checkout]] shipped the prototype: four tiers (Public free, Pro $29, Pro Team $149, Sovereign $2k+). [[L271]] section 10 then names five tiers: Free, Studio $99, Newsroom $499, Institutional $4,999, Vendor custom.

There's a tension. The L260 prototype priced Pro at $29 — a self-serve developer SKU; [[L271]] / L006 priced Studio at $99 — a creator / publisher SKU. They aren't the same product. This loop reconciles, picks the canonical pricing for v1 launch, and projects cohort math against the [[L274]] KPI-7 trajectory.

Four candidates re-evaluated, sharper than [[L006]] because we now have the cost model from [[L275]] grounding the unit-economics math.

---

## Candidate 1 — The L260 prototype (Pro $29 / Team $149 / Sovereign $2k+)

**Structure.** Self-serve developer-API pricing.

| Tier | Price | Headline |
|---|---|---|
| Public | Free | API 60 req/min, MCP 1k/day |
| Pro | $29/mo | API 1k req/min, MCP 100k/day, white-label embed |
| Pro Team | $149/mo | 10 seats, SSO, priority support |
| Sovereign | $2k+/mo | On-prem option, custom adapters, audit trail |

**Argument for.** Friction-low entry. $29 is impulse-purchase territory; Damian could buy it on a tip from a single video. Faster top-of-funnel conversion. Developer-friendly framing matches HN launch audience.

**Argument against.** Pricing Pro at $29 commodifies the surface. The buyer's mental model becomes "API throughput at $29/month" rather than "credibility-by-borrowing under your brand." It anchors low. The Studio cohort (Substack writers, mid-tier publishers, freelance analysts) actually has higher willingness-to-pay than $29/month because their alternative is *the time cost* of making their own charts. Pricing low is leaving money on the table for an audience that would happily pay $99.

**Unit economics against [[L275]] cost model.**

- Variable cost per Pro user at Y1 scale: ~$2/month (Workers + Cloud Run share). Gross margin ~93%.
- Y1 target: 30 Pro users + 5 Team + 1 Sovereign → ~$8.7k + $7.5k + $24k = ~$40k ARR.
- Y3 target: 500 Pro + 30 Team + 5 Sovereign → ~$145k + $45k + $120k = ~$310k ARR.

**Verdict.** Y3 ARR is *one-tenth* the L006 / L271 trajectory. This is the price of pricing low.

---

## Candidate 2 — The L006/L271 publisher tier (Studio $99 / Newsroom $499 / Institutional $4,999 / Vendor custom)

**Structure.** Publisher/institutional ladder.

| Tier | Price | Headline |
|---|---|---|
| Free | $0 | Full public dashboard, embed with attribution, 1k API/day, 100 MCP/day |
| Studio | $99/mo | White-label embed, 100k API/day, 10k MCP/day |
| Newsroom | $499/mo | 10 seats, branded digest, 1M API/day, 100k MCP/day |
| Institutional | $4,999/mo | Custom subdomain, NDA, SOC2, unlimited |
| Vendor | Custom | LLM platform OEM, per-million MCP pricing |

**Argument for.** Anchors the buyer in the publisher/institutional mindset where willingness-to-pay is structurally higher. Studio at $99 is still impulse for a Substack writer making $3-5k/mo from their own paid newsletter. Institutional at $4,999 is *low* for an NGO communications budget that routinely spends $50k+/yr on visualization contractors.

**Argument against.** $99 is a real friction step for an individual Damian-class user. We risk losing the indie-developer cohort entirely.

**Unit economics.**

- Variable cost per Studio user: ~$2/month. Gross margin ~98%.
- Variable cost per Newsroom: ~$15/month (multi-seat + branded digest generation). Gross margin ~97%.
- Variable cost per Institutional: ~$60/month + $2k setup. Gross margin ~98%.
- Y1: 25 Studio + 10 Newsroom + 1 Institutional → ~$30k + $60k + $60k = ~$150k ARR.
- Y3: 500 Studio + 150 Newsroom + 30 Institutional + 1 Vendor → ~$600k + $900k + $1.8M + $1.5M = ~$4.8M ARR.

**Verdict.** Matches L010 Y3 target. Buyer mental model aligns with what we're actually selling. Misses the indie-dev cohort.

---

## Candidate 3 — Hybrid: Pro $29 + Studio $99 + Newsroom $499 + Institutional $4,999 + Vendor

**Structure.** Two entry tiers — $29 self-serve developer, $99 white-label publisher.

| Tier | Price | Audience |
|---|---|---|
| Free | $0 | Everyone |
| Pro | $29/mo | Indie devs, hobbyists, small project use. API 100k/day + MCP 10k/day. No white-label. |
| Studio | $99/mo | Substack writers, freelance analysts. White-label embed, MCP 50k/day. |
| Newsroom | $499/mo | Small newsrooms, think-tank comms. Multi-seat. |
| Institutional | $4,999/mo | NGOs, regional CBs, university research centers. Custom subdomain. |
| Vendor | Custom | LLM platform OEM. |

**Argument for.** Captures both cohorts. Pro at $29 is the indie / Damian path; Studio at $99 is the Substacker / Marcus path. Different feature mix at each (Pro is API-throughput-focused; Studio is white-label-focused) so they don't cannibalize.

**Argument against.** Five paid tiers is too many. Decision paralysis at the pricing page. Sales support cost compounds. The L260 wisdom was that the pricing page should be readable in 20 seconds; five tiers + a Free tier is borderline.

**Unit economics.**

- Y1: 30 Pro + 15 Studio + 5 Newsroom + 1 Institutional → ~$10k + $18k + $30k + $60k = ~$118k ARR.
- Y3: 800 Pro + 300 Studio + 100 Newsroom + 25 Institutional + 1 Vendor → ~$280k + $360k + $600k + $1.5M + $1.5M = ~$4.2M ARR.

**Verdict.** Roughly matches Candidate 2 at Y3 but at a complexity cost. The added Pro tier captures ~$280k incremental ARR (worth it) at the cost of pricing page complexity (manageable).

---

## Candidate 4 — Usage-based with a small base fee (Free + $0.01/MCP-call + $0.001/API-call beyond free quotas)

**Structure.** No tiers. Free tier with generous quotas; everything beyond is metered.

| Layer | Price |
|---|---|
| Free | Full dashboard, embed with attribution, 1k API + 100 MCP / day |
| Beyond free | $0.001 / API call, $0.01 / MCP call, no minimum |
| White-label add-on | $99/mo on top |
| Custom domain | $499/mo on top |
| SLA + NDA | $2k/mo on top |

**Argument for.** Transparent. Matches how AWS / GCP / OpenAI charge. Scales with usage automatically. No tier-decision friction.

**Argument against.** Macro researchers and journalists don't want to think about per-call cost when they're researching. Bill shock is real ("I exported one country's full vintage history and got a $40 invoice"). The L008 promise "we never charge for the substance" is harder to communicate under usage-based pricing. Also: the AWS/GCP pricing pattern works for enterprises with procurement teams; our buyer is a Substack writer with a Visa card.

**Unit economics.**

- Highly variable. A power user could cost $200/mo; a casual user $0. Median Pro-equivalent user: $40/mo.
- Y1 projection: ~25 paying users at ~$40 average + 1 Institutional add-on bundle = $12k + $24k = ~$36k ARR.
- Y3 projection: ~500 paying users + 20 Institutional bundles = $240k + $480k + Vendor = ~$1.5M ARR.

**Verdict.** Underperforms Candidates 2 and 3. Usage-based is a poor fit for our buyer.

---

## The recommendation

**Pick Candidate 3 — hybrid Pro $29 + Studio $99 + Newsroom $499 + Institutional $4,999 + Vendor.**

The L271 PRD names five tiers but conflates Pro and Studio. This loop separates them. The reasoning, in priority order:

1. **The indie cohort is real.** L003's Damian persona is a $29 buyer, not a $99 buyer. Pricing him out of the paid tier means he never converts. Pricing him at $29 captures incremental ARR (~$280k at Y3) and turns him into an advocate who pulls in the Substack / Newsroom cohort.

2. **The publisher cohort doesn't downgrade.** Substack writers and freelance analysts who *would have* paid $99 don't downgrade to $29 because Pro doesn't include white-label embed. The feature wall is clean: Pro buys throughput, Studio buys brand-borrowing. Different buyers, different value props.

3. **Five tiers is acceptable if the pricing page communicates well.** [[L138-pricing-page]] design supports a five-tier ladder if the visual hierarchy is right. The [[L260]] prototype currently shows four; we add the Studio tier between Pro and Newsroom.

4. **The "we never charge for substance" block is unchanged.** It works at any tier complexity because it's about what we *don't* gate, not what we *do*.

---

## The final pricing page

```
FREE
$0 forever
  Full public dashboard, every country, every indicator, every forecast, every vintage
  Cite-this-view permanent identifiers
  RSS / Atom feeds, JSON-block per chart
  Embeddable widgets with OPENGEM attribution
  Public API: 1,000 requests / day
  Public MCP: 100 invocations / day
  Forever. No "freemium throttling."

PRO
$29 / month
  Everything Free, plus
  API: 100,000 requests / day
  MCP: 10,000 invocations / day
  Single seat
  Email support
  Built for: indie devs, hobbyists, individual project use.

STUDIO
$99 / month
  Everything Pro, plus
  White-label embeds (your logo, your colors)
  Removal of OPENGEM watermark (attribution link in footer remains)
  Custom URL slugs (yourname.opengem.com/...)
  API: 100,000 requests / day, MCP: 50,000 invocations / day
  Single seat
  Built for: Substack writers, freelance analysts, mid-tier publishers.

NEWSROOM
$499 / month
  Everything Studio, plus
  Multi-author seats (up to 10)
  Branded daily-digest auto-generation
  Batch tearsheet PDF export
  Priority embed CDN
  API: 1M requests / day, MCP: 100k invocations / day
  Office hours support
  Built for: small newsrooms, magazines, think-tank communications teams.

INSTITUTIONAL
$4,999 / month + setup
  Everything Newsroom, plus
  Fully custom subdomain (macro.yourorg.org)
  Private theme + branding system
  Custom data slices (your countries / indicators of interest)
  NDA support, SOC2 documentation
  API: unlimited, MCP: unlimited
  Quarterly calibration report comparing your usage to peers
  Built for: NGOs, sovereign funds, regional central banks, university research centers.

VENDOR
Custom
  Everything Institutional, plus
  LLM-platform OEM tier — embed OPENGEM as a built-in tool in your chat product
  Per-million MCP invocation pricing with volume discounts
  Dedicated MCP routing infrastructure
  Co-marketing
  Built for: LLM vendors who want grounded macro built in.

─────────────────────────────────────────────────────────
WHAT WE WILL NEVER CHARGE FOR

   The full forecast track record. Free.
   Reading any historical vintage. Free.
   Reading the miss log. Free.
   Reading the methodology. Free.
   Forking the codebase. Apache-2.0.
   Republishing derived metrics. CC-BY-4.0.

   We charge for velocity and fit, never substance.
─────────────────────────────────────────────────────────
```

---

## Cohort math against KPI-7

The recommended pricing produces the following ARR trajectory:

| Horizon | Pro | Studio | Newsroom | Institutional | Vendor | Total ARR |
|---|---|---|---|---|---|---|
| Y1 (Q3 2027) | 30×$29 = $10k | 15×$99 = $18k | 5×$499 = $30k | 1×$4,999 = $60k | 0 | ~$118k |
| Y2 (Q3 2028) | 200×$29 = $70k | 100×$99 = $120k | 30×$499 = $180k | 8×$4,999 = $480k | 1×$200k | ~$1.05M |
| Y3 (Q3 2029) | 800×$29 = $280k | 300×$99 = $360k | 100×$499 = $600k | 25×$4,999 = $1.5M | 1×$1.5M | ~$4.2M |
| Y5 (Q3 2031) | 4k×$29 = $1.4M | 1k×$99 = $1.2M | 300×$499 = $1.8M | 100×$4,999 = $6M | 4×$2M = $8M | ~$18.4M |

Y1 hits the [[L010]] Y1 target ($100-150k). Y2 hits the Y2 target ($1M). Y3 hits the Y3 target ($4-5M). Y5 hits the Y5 midpoint ($15-25M).

Conversion rates baked into these numbers:

- **Free → Pro**: ~0.5% of WAU per quarter. Realistic for an unmarketed self-serve tier.
- **Pro → Studio**: ~5%/quarter of Pro users discover they want white-label and upgrade.
- **Studio → Newsroom**: ~3%/quarter of Studio users grow into multi-author teams.
- **Newsroom → Institutional**: ~2%/quarter via founder-sales conversation.
- **Direct sales of Institutional**: ~1 every 6 months via warm-intro / inbound.

These are conservative. The asymmetric upside is the Vendor tier — if a major LLM vendor signs, ARR shifts up an order of magnitude on a single contract.

---

## Sensitivity to two scenarios

**Scenario A — Pro tier underperforms (impulse-buy hypothesis is wrong).** If Pro converts at 0.1% instead of 0.5%, Pro ARR at Y3 is $56k instead of $280k. Total Y3 ARR drops ~5%. Not catastrophic; the Institutional/Vendor tiers carry the load.

**Scenario B — Vendor tier lands early.** If a Vendor account signs at Y1 ($500k) instead of Y2, Y1 ARR jumps to $618k. The infra/revenue ratio from [[L275]] becomes 1.5% — extremely healthy. We can hire a second engineer six months ahead of the L010 plan.

The pricing structure absorbs both surprises gracefully.

---

## What this loop produced

- Four pricing candidates re-evaluated against the [[L275]] cost model.
- A reconciled five-tier pricing recommendation (Pro + Studio + Newsroom + Institutional + Vendor).
- The final pricing page copy with the "what we never charge for" block.
- Cohort math hitting [[L010]] ARR trajectory across Y1-Y5.
- Sensitivity analysis for Pro underperformance and early Vendor signing.

## What comes next

- **L260 (Phase 5)** to update the pricing-page prototype with the five-tier structure.
- **L283** — ToS draft mirrors the "never charge for substance" block.
- **L290** — churn flow handles cancellations across all five tiers.

## Related

- [[L006-pricing-thesis]] — the original five-tier framing this loop sharpens
- [[L260-pricing-checkout]] — Phase 5 prototype to update
- [[L274-kpi-dashboard-meta]] — KPI-7 trajectory this pricing produces
- [[L275-cost-projection]] — cost model grounding the unit economics
- [[L300-final-synthesis]] — re-audits this pricing at Y5
