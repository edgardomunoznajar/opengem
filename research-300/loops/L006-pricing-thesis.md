# L006 — Pricing Thesis

**Loop**: 006 / 300
**Phase**: 0 — Strategic framing
**Date**: 2026-06-06

---

## The thesis of this loop

OPENGEM's pricing has to encode three commitments simultaneously: (1) the public dashboard stays free and complete — no premium forecasts, no premium country pages, no premium track records; (2) the paid tier exists for *velocity* and *fit*, not for *secrecy*; (3) the revenue model has to survive a world where LLMs increasingly displace human dashboard-visiting as the primary consumption surface.

There are roughly three pricing models that fit this set of commitments. The candidates below are evaluated honestly. One is picked. The unit economics are written out.

---

## Candidate A — Freemium API tier

**Structure.** Public dashboard + RSS feeds + JSON-block-per-chart + low-throughput public API: free forever, no signup required. Higher-throughput API access requires a key. Pricing tiers:

- **Free**: 1,000 API requests / day, 10 RPS, no commercial-use restriction, but `User-Agent` header required.
- **Builder**: $49/mo, 100,000 requests / day, 100 RPS, commercial OK, no SLA.
- **Pro**: $299/mo, 1,000,000 requests / day, 1,000 RPS, 99.5% SLA, priority support.
- **Enterprise**: $2,500/mo + custom, unlimited throughput, 99.9% SLA, dedicated subdomain, custom data slices, NDA support.

**Argument for.** Familiar shape — every dev knows how this works. Easy to instrument (API key per tier). Low friction for the long tail of Damian-class hobbyist devs who want to wire up their YouTube workflow.

**Argument against.** API pricing is *fundamentally a commodity wholesale market*. The buyer can compute their cost per request against the value of the request and arbitrage downward. Margins are thin and shrink over time. Bigger problem: in a 2027-2028 world where LLMs route through MCP, API requests become *invisible* — they happen inside chat sessions, not from developer dashboards — and the pricing model fails to capture the value being delivered. This is a 2010s pricing model in a 2026 market.

**Unit economics (back of envelope).**
- ARPU on Builder tier: $588/year. Variable cost per Builder seat: ~$8/month (egress + compute) → ~75% gross margin.
- ARPU on Pro tier: $3,588/year. Variable cost ~$30/month → ~80% gross margin.
- ARPU on Enterprise: $30k+/year. Variable cost ~$200/month → ~85% gross margin.
- **Realistic 24-month TAM**: ~500 Builder + ~50 Pro + ~10 Enterprise → ~$760k ARR. Decent but not exciting; flat-shape, slow compounding.

---

## Candidate B — Paid white-label / embed

**Structure.** Public dashboard + RSS + JSON: free forever. White-label embeds + branded tearsheets + custom domains require a paid subscription. Pricing tiers:

- **Free**: full public OPENGEM site, with OPENGEM branding, free embed widgets with OPENGEM watermark.
- **Studio**: $99/mo, white-label embeds (own logo, own colors), removal of OPENGEM watermark, custom URL slugs.
- **Newsroom**: $499/mo, multi-author seats, branded daily-digest auto-generation, batch tearsheet export, priority embed CDN.
- **Institutional**: $4,999/mo, fully custom domain (e.g. `macro.cgd.org` powered by OPENGEM), private theme, NDA support, custom data slices for the institution's internal analysts.

**Argument for.** This is the *trust-arbitrage* play: institutions pay OPENGEM to use the open ledger *as if it were their own* because building it themselves is impossible (no track record), and citing the open OPENGEM brand is sometimes too informal. NGOs, mid-tier publishers, think tanks, regional banks — they all want a Bloomberg-grade visual surface they can put under their own brand. The value to the buyer is *credibility-by-borrowing* without disclosing it. This is the most lucrative slice if it works.

**Argument against.** It risks the asymmetry. If institutions white-label OPENGEM, end-users see the institution's brand and *don't know* OPENGEM is the source. That breaks the citation flywheel that L005 anchored on. There's a tension between maximizing white-label revenue and maximizing the visible-attribution model that drives the North-Star metric. We have to be careful that white-label terms always require a footer attribution to OPENGEM with a citation link, even when the rest of the chrome is branded.

**Unit economics.**
- ARPU on Studio: $1,188/year. Variable cost ~$15/month → ~85% gross margin.
- ARPU on Newsroom: $5,988/year. Variable cost ~$50/month → ~90% gross margin.
- ARPU on Institutional: $59,988/year. Variable cost ~$300/month + ~$2k sales overhead → ~80% net.
- **Realistic 24-month TAM**: ~200 Studio + ~50 Newsroom + ~10 Institutional → ~$1.13M ARR. Better than A.

---

## Candidate C — Paid MCP throughput

**Structure.** Public dashboard + RSS + low-throughput MCP server: free forever. Hosted MCP server with high-throughput access and additional tool surface requires a subscription. Pricing tiers:

- **Free**: public MCP server, 100 invocations / day per IP, no auth, ideal for one-person hobby use of Claude/ChatGPT.
- **Researcher**: $19/mo, 10,000 invocations / day, MCP key auth, no commercial restriction.
- **Team**: $199/mo, 100,000 invocations / day, multi-key, team admin, monthly usage report.
- **Vendor**: $1,999/mo, 1M+ invocations / day, dedicated subdomain, priority MCP routing, OEM-tier for LLM platforms that want to embed OPENGEM as a built-in tool.

**Argument for.** This is the *future-shaped* model. By 2027-2028, the dominant macro-information consumption surface is conversational, not visual. The valuable unit is "grounded macro answer in a chat session." MCP is the protocol that delivers it. Pricing on MCP throughput directly captures the value as the surface migrates. The Vendor tier is the *most lucrative single line item we could imagine* — if Anthropic, OpenAI, or Google wants to embed OPENGEM as a first-class tool inside their consumer LLM, they pay a per-million-invocation rate. That's a six-to-seven-figure ARR account potentially.

**Argument against.** MCP is early, the protocol is still settling, and "MCP throughput" is not yet a unit the buyer understands at the line-item level. Pricing for it today is partly bet-on-the-future. Also: LLM vendors might choose to *build* their own macro grounding rather than pay OPENGEM, especially if OPENGEM's data is fully open under CC-BY (which it is). So we may be giving away the cow and trying to charge for the milk.

**Unit economics.**
- ARPU on Researcher: $228/year. Variable cost ~$3/month → ~85% gross margin.
- ARPU on Team: $2,388/year. Variable cost ~$20/month → ~90% gross margin.
- ARPU on Vendor: $23,988+/year (base) plus per-million overages. With one or two real vendor accounts, this can be ~$200k+/year per account.
- **Realistic 24-month TAM**: ~1,000 Researcher + ~100 Team + ~3 Vendor → ~$1.13M ARR (if vendor accounts close); ~$470k ARR (if vendor accounts don't). High variance.

---

## The recommendation

**Pick the *hybrid* model anchored on Candidate B (white-label / embed), with Candidate C (MCP throughput) as the future-facing tier and Candidate A's API throughput rebuilt as a *technical* feature of B and C, not its own line item.**

The reasoning:

1. **B is the lucrative middle.** White-label / embed is where institutional money actually lives. Newsrooms, NGOs, think tanks, regional banks: these are all real buyers with a recurring need for "credible-looking macro visuals under our brand." The CGDs and Atlantic Councils and Bertelsmann Stiftungs of the world will pay $5-50k/year happily.

2. **C is the option on the future.** Even if MCP turns out to be a smaller market than hoped, having the MCP pricing line item built from day one means that *if* an LLM vendor wants to license OPENGEM as a built-in tool, we have a price to quote. We're not building the entire business on it, but we're not foreclosing the option either.

3. **A is a feature, not a product.** API throughput is the underlying *capacity* that the white-label and MCP tiers consume. If we sold A as a separate product, we'd commodify it. If we bundle it as a capacity-allocation inside B and C, we capture the value at the surface where the buyer has willingness to pay.

4. **Free tier is generous and stays generous.** Public dashboard fully functional, RSS / JSON-block-per-chart / embeddable widgets with attribution, MCP server with 100 calls/day, public API with 1k calls/day. The free tier is *the marketing*; it's the credibility flywheel; it's the citation engine that moves VC/w (L005). We do not gate forecasts behind paywalls — ever. The paid tier is for buyers who want OPENGEM under their own brand or at vendor-scale throughput.

---

## The hybrid pricing page

```
FREE
$0 forever
  ✓ Full public dashboard, every country, every indicator, every forecast, every vintage
  ✓ RSS / Atom feeds, JSON-block-per-chart
  ✓ Embeddable widgets with OPENGEM attribution
  ✓ Public API: 1,000 requests / day
  ✓ Public MCP: 100 tool invocations / day
  ✓ Cite-this-view permanent identifiers
  Forever. No "freemium throttling."

STUDIO
$99 / month
  ✓ Everything free, plus
  ✓ White-label embeds (your logo, your colors)
  ✓ Removal of OPENGEM watermark (attribution link in footer remains)
  ✓ Custom URL slugs (yourname.opengem.com/...)
  ✓ API: 100,000 requests / day
  ✓ MCP: 10,000 invocations / day
  Built for: Substack writers, mid-tier publishers, freelance analysts.

NEWSROOM
$499 / month
  ✓ Everything Studio, plus
  ✓ Multi-author seats (up to 10)
  ✓ Branded daily-digest auto-generation
  ✓ Batch tearsheet PDF export
  ✓ Priority embed CDN
  ✓ API: 1M requests / day, MCP: 100k invocations / day
  ✓ Office hours support
  Built for: small newsrooms, magazines, think-tank communications teams.

INSTITUTIONAL
$4,999 / month + setup
  ✓ Everything Newsroom, plus
  ✓ Fully custom subdomain (macro.yourorg.org)
  ✓ Private theme + branding system
  ✓ Custom data slices (your countries / indicators of interest)
  ✓ NDA support, SOC2 documentation
  ✓ API: unlimited, MCP: unlimited
  ✓ Quarterly calibration report comparing your usage to peers
  Built for: NGOs, sovereign funds, regional central banks, university research centers.

VENDOR
Custom
  ✓ Everything Institutional, plus
  ✓ LLM-platform OEM tier — embed OPENGEM as a built-in tool in your chat product
  ✓ Per-million MCP invocation pricing with volume discounts
  ✓ Dedicated MCP routing infrastructure
  ✓ Co-marketing
  Built for: LLM vendors who want grounded macro built in.
```

The free tier is *the whole product*. The paid tiers are *modifications of how it appears* (white-label, custom domain) or *guarantees about throughput* (API/MCP scale).

---

## The 24-month revenue model

Assuming reasonable conversion:

| Tier | 24mo customers | ARPU | ARR |
|---|---|---|---|
| Studio | 200 | $1,188 | $237,600 |
| Newsroom | 50 | $5,988 | $299,400 |
| Institutional | 10 | $59,988 | $599,880 |
| Vendor | 2 | $250,000 | $500,000 |
| **Total ARR @ 24mo** | | | **~$1.6M** |

Add ~30% gross margin overhead for hosting, CDN, MCP infrastructure, and Stripe fees → ~$1.1M net gross profit at 24 months. Single founder + occasional contract help can run this. CAC is roughly zero because the free tier *is* the customer acquisition engine — paid tiers are upsells from satisfied free users.

By 36 months, if the Vendor tier lands one major LLM partner ($1M+ ARR), the entire model unbalances upward — that's the asymmetric upside we're keeping the door open for.

---

## What the price tiers explicitly do not gate

- Forecasts (all forecasts are free and public, always, every vintage).
- Track records (all open, always).
- Methodology pop-ups (always free).
- Backtest results (always free).
- Vintage history (always free).
- The MCP server's *core* tools (always free at 100/day).

The paid tier *never* gates the OPENGEM substance. It gates *velocity* (throughput) and *fit* (white-label, custom domain). This commitment is published on the pricing page itself, as a public promise.

---

## What this loop produced

- Three pricing candidates evaluated honestly.
- A hybrid recommendation: white-label / embed as the core, MCP throughput as the future option, API throughput as an underlying capacity (not a line item).
- A five-tier pricing page with the free tier holding the whole product.
- A 24-month revenue model arriving at ~$1.6M ARR with single-founder operability.
- A "never gates the substance" commitment published on the pricing page.

## What comes next

- **L007** translates the pricing structure into distribution channel ROI (the white-label tier needs different channels than the API tier).
- **L138** (Phase 3) designs the actual pricing page UI.
- **L260** (Phase 5) ships the Stripe + magic-link checkout prototype.

## Related

- [[L001-vision-statement]] — the never-gate-the-substance commitment originates here
- [[L002-competitive-landscape]] — the Stratfor / Bloomberg / Macrobond comparison that the white-label tier exploits
- [[L005-north-star-metric]] — VC/w is the leading indicator for white-label conversion
- [[L007-distribution]] — channels keyed to each pricing tier
