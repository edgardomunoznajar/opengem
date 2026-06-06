# L061 — Streamlit: Maturity, Perf Ceiling, License, Hosting, Theming, Embedding

**Loop**: 061 / 300
**Phase**: 1 — Open-source landscape survey
**Date**: 2026-06-06

---

## Thesis of this loop

Streamlit is the *fastest* path from a Python script to a shareable browser-rendered "thing that looks like a dashboard." That is also exactly why it is the wrong choice for OPENGEM's public-facing surface. The two product modes are not commensurable: Streamlit excels at internal data-science apps where the audience is bounded, the latency budget is generous, and the developer is also the user; OPENGEM's public dashboard is the opposite of every one of those conditions.

This loop says: Streamlit lives in OPENGEM's stack — but as an **internal modeling sandbox**, not as the public dashboard. SKIP for public dashboard, ADOPT-V1 for internal ops/scenario authoring.

## What Streamlit is, plainly

Streamlit is a Python library that turns a top-to-bottom Python script into a web app. Every user interaction re-runs the script from the top, with caching primitives (`@st.cache_data`, `@st.cache_resource`) papered over the re-run model. It is Apache 2.0 licensed, owned by Snowflake (acquired March 2022 for ~$800M), and the canonical hosted tier is Streamlit Community Cloud — free, capped, and clearly a top-of-funnel for Snowflake's paid runtime.

The license is fine. The ownership matters: Snowflake's strategic interest is Streamlit-as-Snowflake-frontend, which is *exactly* why the public OSS frontier of features (auth, multi-page state, true multi-user concurrency, custom rendering pipelines) has stagnated since the acquisition.

## The performance ceiling — where it breaks

The script-re-run model is the single load-bearing architectural decision that bounds everything. Concretely:

1. **Single-process, single-threaded by default.** Tornado server. One user blocks another on long-running operations unless every callsite is awaitable and caching is meticulous. The naive Streamlit app caps out around 10-50 concurrent users on a 2-vCPU box. Industry chatter pins the "real" ceiling at ~100-300 concurrent users with aggressive caching, multi-process workers behind a load balancer, and ruthless discipline about what runs on every rerun.

2. **Full-page re-render on every interaction.** This is the killer. A user toggles a checkbox; the entire script reruns; every cached function is checked, every chart is re-emitted, every dataframe is re-serialized to the browser. For a dashboard with 20 charts and a 5MB JSON payload, this is 200-500ms of overhead *per click*. That is fine for an analyst exploring; it is fatal for a public surface where the user is going to bounce after the first laggy interaction.

3. **No real component model.** Custom components are possible but expensive — a custom React bundle, an iframe handshake, a duplicated state model. OPENGEM needs a sparkline grid, a country picker with fuzzy search, a forecast band chart, a vintage drawer — each one of these is a 2-week project in custom-component land vs a 2-day component in React.

4. **Theming is shallow.** Streamlit ships with light/dark and a config file with 6 colors. Bloomberg-orange, terminal density, custom fonts, custom grid behaviors — all require fighting the framework. The new `st.theme` config (2024) helps; the underlying CSS surface is still a hostile environment.

5. **Embedding is iframe-only.** No widget SDK. To put a Streamlit chart in someone's Substack, the only path is an iframe pointed at a Community Cloud URL. No SSR, no static fallback, no graceful degradation. SEO is effectively zero — the page renders in the browser after a Python boot.

## Hosting cost reality

- **Community Cloud**: Free, public-only, 1GB RAM, sleeps after 7 days idle. Not a serious production option — limit-bound for any real usage and the "sleep" is unacceptable for an alerting/public dashboard.
- **Streamlit-in-Snowflake**: Bundled with Snowflake compute. Not cheap; expect $200-2000/mo even for low-traffic if Snowflake is your DB anyway.
- **Self-hosted on Cloud Run / Fly.io**: A 1-vCPU 2GB instance is ~$15-30/mo idle, $50-150/mo with traffic. For ~100 concurrent users you need 2-4 such instances behind a sticky-session load balancer (Streamlit doesn't tolerate non-sticky LBs). Practical floor: ~$80-200/mo for a real public deployment.
- **Snowflake's reserved capacity** is not even worth modeling — OPENGEM doesn't pay Snowflake rates for compute it can run on Cloud Run for a tenth of the price.

Ramp-up time: a competent Python dev ships a Streamlit MVP in 2-3 days. A polished Streamlit app is 3-4 weeks. A Streamlit app that competes on UX with a Next.js dashboard is roughly *infinite* — it's not the same product.

## Where Streamlit *does* belong in OPENGEM

The scenario engine (L080) needs an authoring UI: pick a copula, sweep a parameter, eyeball the distribution, hit "save vintage." That is a single-author, single-session, latency-tolerant workflow with rich Python integration. Streamlit is perfect for it.

Similarly, the V&V matrix audit page (an internal tool that scores forecasts vs realizations) is a Streamlit-shaped problem — one analyst, dense Python compute, rare interaction.

## Verdict

- **Public OPENGEM dashboard**: **SKIP**. Wrong architecture for SEO-driven, embeddable, multi-tenant terminal-grade UX.
- **Internal scenario authoring + V&V audit tools**: **ADOPT-V1**. Two Streamlit apps, behind auth, on a single small VM. Cost: ~$15/mo. Ramp: 1 week each.
- **Long-term**: Watch for Streamlit's `st.fragment` model (selective rerun, shipped 2024) to mature. If by Y2 it offers true partial reactivity, revisit for internal admin surfaces — but not the public dashboard.

The public surface goes to Next.js + Tailwind + Tremor or shadcn (see L073).

## Cost summary

| Use | Cost | Ramp |
|---|---|---|
| Internal scenario authoring | $15/mo | 1 week |
| Internal V&V audit | $15/mo | 1 week |
| Public dashboard | (skipped) | (skipped) |

## What comes next

- **L062** evaluates Dash (Plotly), the other Python-script-to-web tool, with a different (callback-based) reactivity model.
- **L073** picks the Next.js dashboard starter for the public surface.

## Related

- [[L073-next-tailwind-dashboard-starters]] — where the public dashboard actually lives
- [[L080-scenario-engine-libs]] — what the Streamlit-on-the-inside tool actually authors
