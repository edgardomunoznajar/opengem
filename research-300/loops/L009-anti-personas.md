# L009 — Anti-Personas and Refusal Scope

**Loop**: 009 / 300
**Phase**: 0 — Strategic framing
**Date**: 2026-06-06

---

## The thesis of this loop

Knowing who OPENGEM is *for* without knowing who OPENGEM is *against* (or, more precisely, *not for*) is half the job. A product that tries to serve everyone becomes thin where it matters and unprincipled where it should be sharp.

The L003 personas tell the team who to build for. This loop tells the team who to *refuse*. Refusal is not rudeness — it's strategic clarity. Every "no" sharpens the product for the right "yes." More importantly: refusal is *values-expressive*. A team that publicly says "we will not serve nation-state intelligence customers" telegraphs to the credibility cohort that the product is built on principles, not on the next available check.

This loop names six anti-personas and writes the corresponding refusal scope. The refusal scope is the published list of *use cases OPENGEM declines to support, no matter the revenue*. Every refusal is grounded in why supporting it would *break* one of the five promises from L008 or one of the three musts/must-nots from L001.

---

## The six anti-personas

### Anti-persona 1 — The intraday trader

**Who they are.** A retail or pro day-trader who wants real-time tick data on equities/FX/crypto, with sub-second latency and execution-rails integration. They are the prototypical TradingView power user, the prop-shop quant, the high-frequency-Twitter degenerate. They want a Bloomberg-Terminal-for-cheap, and they want a ticker that moves every second.

**Why OPENGEM refuses.** OPENGEM is *macro*, not *micro*. The dashboard's cadence is daily / weekly / monthly, with intraday updates only when a macro release hits (CPI, NFP, FOMC). Building a market-data feed would require:
- A market-data licensing budget that would consume the entire revenue model.
- An infrastructure investment (latency, market-data normalization, exchange direct connections) that would compete with Bloomberg's actual moat.
- An audience whose values misalign with OPENGEM's track-record discipline (day traders don't want methodology pop-ups; they want execution speed).

The refusal also protects the brand: a macro-accountability product that gets confused with a trader's terminal would lose credibility in the credibility cohort. Marcus the FT journalist does not cite a "day-trader dashboard"; Lin the NGO researcher does not cite a "tick-data feed." OPENGEM stays *macro* to stay citable.

**What they should use instead.** TradingView (charting), Polygon.io or IEX Cloud (market data), Alpaca / IBKR (execution), Bloomberg / Refinitiv (institutional intraday). OPENGEM's "for whom" page will list these explicitly with no judgment — they are the right tools for that user's job; we are not.

---

### Anti-persona 2 — The securities advisor

**Who they are.** A wealth-management advisor, a financial planner, a robo-advisor, anyone who wants to use OPENGEM as the basis for *recommending specific securities to retail clients*. The temptation: package OPENGEM's recession-probability tile, scenario page, or sovereign-risk page into a client-facing tool that says "based on this, buy X."

**Why OPENGEM refuses.** Two reasons:
1. **Regulatory.** OPENGEM is published macro information, not investment advice. The moment we package it for advisor-to-retail consumption, we trip SEC / FCA / ESMA / CONSOB jurisdiction across every market, requiring registrations and disclosures that destroy the open-data model.
2. **Brand.** A macro forecast saying "Italian sovereign spread is widening" is honest macro information. A wealth-advisor tool saying "your clients should reduce BTP exposure based on OPENGEM" is investment advice, and if OPENGEM is the *named source* of that recommendation, OPENGEM is liable for client outcomes. We will not carry that risk.

**What the refusal looks like operationally.** The Terms of Service explicitly forbid white-label re-use of OPENGEM data as the *primary basis* for retail securities recommendations. The MCP server's output includes a "this is published macro information, not investment advice" header on every relevant tool's response. The Institutional white-label tier requires the buyer to confirm in the contract that they will not present OPENGEM-derived material as investment advice. We don't want this customer.

**What they should use instead.** Morningstar Direct, Aladdin, factor-model providers. Real investment-advice products have full regulatory stacks; OPENGEM is the *upstream macro* they reference, not the recommendation engine.

---

### Anti-persona 3 — The nation-state intelligence customer

**Who they are.** A government foreign-intelligence agency that wants OPENGEM's geopolitical risk indices, conflict data, supply-chain pulse, sanctions tracking, etc., as one feed into a national-security analytical workflow. This includes the equivalents inside US, UK, French, German, Israeli, Chinese, Russian, Indian, Brazilian, and any other state intelligence apparatus.

**Why OPENGEM refuses.** This is the most important refusal in the entire scope. Reasoning:
- OPENGEM's published data is, by license (CC-BY-4.0), legally *available* to anyone, including intelligence agencies. We cannot prevent them from scraping the public site. That's the point of CC-BY.
- But OPENGEM will not *sell* a contract, will not *brand-partner*, will not *MCP-vendor-tier*, and will not *co-market* with any state intelligence agency. The white-label tier is closed to them at any price.
- Why: the brand becomes corrosive the moment it's perceived as a national-security-adjacent tool. The credibility cohort would lose trust. The international users would lose trust. Open-source contributors would lose trust. Academic citers would lose trust.
- Secondary why: state intelligence agencies have their own internal data resources at scales OPENGEM cannot match anyway. We are not the right tool for that job.

**The published statement.** OPENGEM's About page includes a values statement: "We will not sell, partner with, or co-market with any state intelligence agency. Our data is openly licensed and they may use it under the CC-BY-4.0 terms like anyone else, but they will not appear in our customer list, our case studies, or our co-marketing."

---

### Anti-persona 4 — The military command-and-control system

**Who they are.** A defense contractor or military procurement office that wants OPENGEM data integrated into a C2 system, weapons-targeting decision-support, or operational planning for armed forces. This includes "dual-use" framings where the same data feed is sold to humanitarian *and* military customers.

**Why OPENGEM refuses.** Direct alignment with the L001 must-nots and the broader values framework:
- Macro economic and geopolitical risk data has a clear-eyed dual-use risk: the same indicator that helps a NGO predict famine can help a military plan a blockade. We are not equipped to adjudicate end-use case by case.
- The simpler, defensible commitment is *categorical refusal*: no MoD contracts, no defense-prime co-marketing, no NATO procurement, no equivalents in any country. The CC-BY license still applies to public data; the *commercial relationship* is what we refuse.
- The values cost of this refusal is zero relative to the brand cost of accepting. The financial cost is real (defense contracts pay well) but worth the principle.

**The published statement.** "OPENGEM will not enter commercial relationships with defense ministries, military procurement offices, defense primes, or military command-and-control systems. Our public data is free for anyone to use under CC-BY-4.0; we cannot prevent military use of public data, but we will not facilitate it commercially or by partnership."

---

### Anti-persona 5 — The "AI alpha" hedge fund signal-buyer

**Who they are.** A quant hedge fund that wants OPENGEM's forecast surface as a *trading signal feed* — i.e., they want sub-publish-cadence access (pre-publication forecasts) or co-located low-latency API access so they can trade ahead of public OPENGEM-driven price moves. The pitch: "you publish your nowcasts at 9 a.m.; let us see them at 8:55 a.m. for a fee."

**Why OPENGEM refuses.** This breaks Promise 1 (every forecast is published with its vintage timestamp) and Promise 4 (every number resolves to a public source). A pre-publication tier would create *two* OPENGEM products: the public one with the public vintage, and the private one with the actual operative numbers. The public one would become a delayed-decoy of the private one. The North-Star metric (VC/w) would collapse because the *real* OPENGEM would be the private feed, not the citable public ledger.

This refusal protects the brand from the most lucrative-looking trap. A pre-publication forecast feed could plausibly close $1M-$10M ARR with one or two hedge fund accounts. We refuse anyway.

**The published statement.** "OPENGEM publishes every forecast simultaneously to the public, the API, the MCP server, the RSS feeds, and the paid tiers. There is no pre-publication tier at any price. Every forecast vintage is timestamped to the second of publication."

---

### Anti-persona 6 — The disinformation packager

**Who they are.** A media organization, political-operative shop, troll-farm operator, or marketing agency that wants to selectively pull OPENGEM data, strip the context and methodology pop-ups, and republish under a misleading framing. The classic move: "OPENGEM says Italy is heading for sovereign default" when OPENGEM's actual published forecast was "probability of sovereign default 12-month horizon: 8%, up from 5%."

**Why OPENGEM refuses (and what we do about it).** This refusal is harder operationally because we can't fully prevent it — CC-BY-4.0 gives anyone the right to redistribute with attribution. But we can:
- Engineer the dashboard so that decontextualized re-use is *uglier* than contextualized re-use. The embed iframe always includes the methodology link, the vintage timestamp, the credibility band. The PNG export always includes the chart title with confidence interval, the source citation, and the OPENGEM watermark.
- Write Terms of Service that forbid *commercial* republication of OPENGEM data in ways that materially misrepresent the methodology, the vintage, or the confidence interval. Non-commercial bad-faith re-use is impossible to enforce; commercial bad-faith re-use we can pursue legally.
- Maintain a *public correction log* — when major media organizations misrepresent OPENGEM, we publish a "what we actually said" post on the OPENGEM blog with the corrected context. Marcus the FT journalist will use OPENGEM properly; the bad actors get publicly corrected by name.

**The published statement.** "OPENGEM data is open under CC-BY-4.0. We require attribution and reasonable context. We will publicly correct material misrepresentations of our forecasts, and we will pursue legal remedies against commercial republishers who materially misrepresent our methodology or confidence intervals."

---

## The refusal-scope page

This is a *public* page on OPENGEM, linked from the footer alongside the "Five Promises" page. Format: one paragraph per refusal, written in the second person, signed by the OPENGEM team.

```
WHAT OPENGEM IS NOT FOR

If you are an intraday trader looking for tick data and execution rails:
  OPENGEM is not for you. Use TradingView + Polygon + IBKR.

If you are a securities advisor looking for a recommendation engine:
  OPENGEM is not for you. We publish macro information, not advice.
  Use Morningstar, Aladdin, or your factor-model provider.

If you are a state intelligence agency:
  Our public data is yours under CC-BY-4.0 like anyone else's.
  We will not enter commercial, branding, or partnership relationships with you.

If you are a military command-and-control system or defense contractor:
  Same. Public data is yours under the license. Commercial relationships are closed.

If you are a quant hedge fund looking for a pre-publication signal feed:
  We do not have one and never will. Every forecast publishes simultaneously
  to the public dashboard, the API, the MCP server, the RSS feed, and every
  paid tier. There is no pre-publication tier at any price.

If you are a disinformation packager:
  Our license allows re-use with attribution. We will correct material
  misrepresentations of our methodology in public, and we will pursue
  commercial bad-faith re-use legally.
```

The page is signed:
> "OPENGEM is a public macro-accountability ledger. These are the limits we set on what that means. Edgardo, founder."

---

## The values statement (the why)

A product without an enemies-list is a product without a brand. The credibility cohort (Marcus, Lin, Priya) chose to trust OPENGEM partly because OPENGEM has visibly refused customers other products would accept. The refusal scope is *brand-positive* with the right audience and *brand-irrelevant* with the wrong audience.

The harder ones — defense, intelligence, quant hedge funds — are where the test of values happens. Each of these refusals has a price tag in dollars. The board, the early team, and any future investor should know that the refusals are *first principles*, not "we'll see when the offer comes." When the offer comes, the answer is no, regardless of the number. We publish the refusal scope before the offer arrives precisely to make this a non-discussion.

The five promises (L008) say what OPENGEM *is*. The refusal scope says what OPENGEM is *not*. Together, they define the brand. Everything else is implementation.

---

## What this loop produced

- Six anti-personas named, with the business model + brand reasons for each refusal.
- A published Refusal-Scope page with second-person framing.
- A values statement: refusals are first principles, not negotiations.
- A direct link back to L008: the five promises explain the "yes"; the refusal scope explains the "no."

## What comes next

- **L010** assembles the strategic-framing arc into a 5-year milestone sequence.
- **L283-L284** (Phase 6) operationalize the refusals into Terms of Service and Privacy Policy.
- **L294** (Phase 6) builds the government/NGO outreach plan that explicitly excludes the anti-personas.

## Related

- [[L001-vision-statement]] — the three musts/must-nots that the refusal scope amplifies
- [[L003-personas]] — the personas OPENGEM is for; the anti-personas are the complement
- [[L008-differentiation]] — the five promises whose preservation requires these refusals
- [[L010-five-year-arc]] — the trajectory these refusals constrain (no defense pivot, no quant signal pivot)
