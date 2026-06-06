---
loop: 139
phase: 3
title: Onboarding Flow — 3 Step
date: 2026-06-06
status: decided
---

# L139 — Onboarding Flow (3 Steps)

**Loop**: 139 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The brief

Design the 3-step onboarding flow. Keep it minimal: pick 3 watchlist items, email, role tag. Nothing more.

## Why 3 steps and not 5

A common onboarding mistake is to ask for too much upfront. Demographic surveys, password setup, profile photo, two-factor enrollment, theme picker, notification preferences — each step adds friction and adds a percent to drop-off.

OPENGEM's onboarding has three constraints:
1. **The free tier is the product.** Onboarding is the path to value, not a marketing funnel.
2. **The watchlist is the personalization surface.** If we get 3 watchlist items, we can render a personalized home, a daily digest, and relevant alerts. That is most of the value.
3. **Email + role tag is enough.** Email enables delivery; role tag enables editorial fit (a journalist sees different empty-state copy than an LP). Beyond that, every other preference is opt-in later.

So we ship three steps. Step 1 picks 3 watchlist items. Step 2 collects email. Step 3 collects role.

## When does onboarding fire

Onboarding fires *after first meaningful engagement*, not at first visit. The flow:

1. **First visit** → land on World page. No interstitial. No "welcome to OPENGEM!" modal. The page is the product.
2. **First interaction** (any click on a country tile, scenario card, indicator, or chart) → no interruption.
3. **At minute 3** (or after 5 page navigations, whichever first) → a subtle bottom-right toast: "Want a personalized daily digest? Set up takes 60 seconds → [Get started]." Dismissable.
4. **Triggered explicitly** by clicking the "Sign in" header button or the [Get started] toast.

The onboarding is opt-in. It is never blocking. The user can use OPENGEM forever without onboarding (anonymous tier).

## Step 1 — Pick 3 watchlist items

```
+--------------------------------------------------------------------------+
| Step 1 of 3 · Watchlist                                                  |
+--------------------------------------------------------------------------+
|                                                                          |
| Pick 3 things to watch                                                  |
| (you can change these any time)                                         |
|                                                                          |
| ┌────────────────────────────────────────────────────────────────────┐  |
| │ search countries, indicators, scenarios...                          │  |
| └────────────────────────────────────────────────────────────────────┘  |
|                                                                          |
| OR PICK FROM A PRESET                                                    |
|                                                                          |
|  🌐 G7 Watch              7 countries           [+ add]                  |
|  🌐 G20 Watch             19 countries          [+ add]                  |
|  🌐 BRICS+ Watch          10 countries          [+ add]                  |
|  🌐 EU-27                 27 countries          [+ add]                  |
|  📊 Recession watch       12 countries + RecProb [+ add]                 |
|  📊 Inflation watch       12 countries + CPI    [+ add]                  |
|  📊 Central bank watch    24 banks + rates      [+ add]                  |
|  ⚠️ Today's scenarios      4 fired              [+ add]                  |
|                                                                          |
| OR PICK INDIVIDUAL ITEMS                                                |
|                                                                          |
| Suggested for first-time visitors:                                       |
|                                                                          |
|  🇺🇸 USA       [+ add]                                                    |
|  🇪🇺 EUR       [+ add]                                                    |
|  🇨🇳 CHN       [+ add]                                                    |
|  🇬🇧 GBR       [+ add]                                                    |
|  🇯🇵 JPN       [+ add]                                                    |
|                                                                          |
|  📊 CPI YoY        [+ add]                                              |
|  📊 GDP YoY         [+ add]                                              |
|  📊 Policy rate     [+ add]                                              |
|  📊 Recession prob  [+ add]                                              |
|                                                                          |
|  ⚠️ Trade-LATAM     [+ add]                                              |
|  ⚠️ Red-Sea-#4      [+ add]                                              |
|  ⚠️ Oil-shock       [+ add]                                              |
|                                                                          |
+--------------------------------------------------------------------------+
| Your selections (1 of 3 minimum)                                         |
|   🇺🇸 USA                                                       [×]      |
+--------------------------------------------------------------------------+
| [Skip onboarding] [Continue →]                                          |
| (continue enabled after 3 items selected)                              |
+--------------------------------------------------------------------------+
```

### Why "3 items minimum, but a preset counts as 1 selection"

If a user picks "G7 Watch" preset, that imports 7 countries — but it counts as "1 of 3" toward the minimum. This is because we want users to express *intentional curation* — three deliberate picks. The preset is fast; one deliberate addition gets them to 1; we still ask for two more.

Or, the user can click "+ add" three times on individual items. Either path satisfies the minimum.

### Why "skip onboarding" is offered

Some users hate flows. Skip lets them continue anonymously. The toast comes back the next session if they engage.

## Step 2 — Email

```
+--------------------------------------------------------------------------+
| Step 2 of 3 · Email                                                      |
+--------------------------------------------------------------------------+
|                                                                          |
| What's your email?                                                       |
|                                                                          |
| ┌────────────────────────────────────────────────────────────────────┐  |
| │ you@example.com                                                     │  |
| └────────────────────────────────────────────────────────────────────┘  |
|                                                                          |
| We'll send you:                                                          |
|   - A magic-link to sign in (no passwords)                              |
|   - A daily digest (toggleable later)                                    |
|   - Important security alerts                                            |
|                                                                          |
| We will NOT send you:                                                    |
|   - Marketing spam                                                       |
|   - Promotional content                                                  |
|   - Third-party offers                                                   |
|                                                                          |
| [+ optional] Daily digest time                                          |
|   ▼ 8:00 user-local (default)                                            |
|                                                                          |
| OR continue with GitHub:                                                 |
|   [Sign in with GitHub]                                                  |
|                                                                          |
| [← Back] [Continue →]                                                    |
+--------------------------------------------------------------------------+
```

### Why magic link, not password

Magic-link login (per L110) is friction-light, secure, and aligns with the brand. No password recovery flow, no breach risk for OPENGEM's auth surface. The trade-off is dependency on email delivery; we accept this.

### Why GitHub OAuth as an alternative

Many of OPENGEM's prosumer audience (developers, data scientists) have GitHub. One-click OAuth is faster than magic link for them.

### Why timing the digest is optional

Power users want to control delivery. Most don't care. Default to 8am user-local based on IP geolocation.

## Step 3 — Role tag

```
+--------------------------------------------------------------------------+
| Step 3 of 3 · What brings you to OPENGEM?                                |
+--------------------------------------------------------------------------+
|                                                                          |
| (one tag, optional, helps us tailor what you see)                       |
|                                                                          |
|  ⦿ I'm a journalist or media person                                     |
|  ○ I'm an analyst (sell-side, NGO, gov, consultancy)                    |
|  ○ I work at an investment firm (hedge fund, family office, fund)       |
|  ○ I'm an academic researcher                                            |
|  ○ I run a YouTube / Substack / newsletter                              |
|  ○ I'm just curious about the world economy                             |
|  ○ I'm a developer building on the API / MCP                            |
|  ○ Other / prefer not to say                                            |
|                                                                          |
| What we use this for:                                                    |
|   - Tailoring empty-state copy and feature hints                         |
|   - Aggregate (de-identified) analytics on user mix                     |
|   - Nothing else                                                         |
|                                                                          |
| We do NOT share this with anyone, ever. It is stored on your profile.  |
|                                                                          |
| [← Back] [Skip] [Finish setup →]                                         |
+--------------------------------------------------------------------------+
```

### Why role tag

Role tag drives editorial fit. A journalist sees prompts for citation and forecast quotes. An analyst sees prompts for sensitivity analysis. An LP sees pricing-relevant content highlighted. A YouTuber sees the JSON-paste-to-ChatGPT recipe surfaced.

The tag is *optional* — the user can skip without choosing one. We default to "Just curious" if skipped.

The tag is stored on the user profile. It is *never* sold, shared, or aggregated to identifying-level granularity. It is used to render UI variants.

### Why these 8 roles

The roles match the L003 persona work (journalist, analyst, LP, prosumer, academic, developer, plus "other"). Eight is the maximum that fits without scrolling on portrait mobile.

## Confirmation screen

```
+--------------------------------------------------------------------------+
| You're in.                                                               |
+--------------------------------------------------------------------------+
|                                                                          |
| ✓ Watchlist: USA, EUR, CPI YoY                                          |
| ✓ Email: you@example.com (check your inbox to verify)                  |
| ✓ Role: journalist                                                       |
|                                                                          |
| WHAT NEXT                                                                |
|                                                                          |
|   - Your World page is now personalized.                                |
|   - The daily digest will arrive tomorrow at 8am user-local.            |
|   - You can change everything at /settings.                              |
|                                                                          |
| THREE COMMANDS TO TRY                                                    |
|                                                                          |
|   ⌘K then type:                                                          |
|                                                                          |
|     > compare USA EZ                                                     |
|     > rewind 2024-09                                                     |
|     > packs:fired-today                                                  |
|                                                                          |
| [Take me to the dashboard →]                                            |
+--------------------------------------------------------------------------+
```

The confirmation screen is the on-ramp to power-user features (the command bar). It shows three commands they can try immediately. This converts onboarding into engagement.

## Edge cases

- **Existing user signs in**: skip steps 1-3 entirely; go straight to dashboard.
- **Email already exists**: send magic link to existing account; show "we sent you a sign-in link" message; do not reveal whether email is registered (privacy).
- **GitHub OAuth path**: skip step 2 (email derived from GitHub), proceed to step 3.
- **Mobile**: steps stack vertically, no side rails, larger tap targets.
- **Returning unverified email**: send a new magic link from the start of the next session.

## Verification

The magic-link in the email is the verification. Until clicked:
- Watchlist is created.
- User can use the dashboard (Free tier).
- Daily digest is NOT sent (we don't email unverified addresses).
- Alerts can be configured but NOT delivered.

Once clicked: full Free tier access.

## What this loop produced

- Three steps: watchlist (3 items), email, role.
- Triggered after first engagement (not at first visit). Toast at minute 3 / page 5.
- Step 1 lets user pick preset OR individual items. Preset import counts as 1 selection.
- Step 2 supports magic-link or GitHub OAuth. Optional digest time selection.
- Step 3 is one role tag (8 options), optional, drives editorial fit.
- Confirmation screen shows three try-now commands to convert onboarding into engagement.
- Magic-link verification gates email delivery (alerts, digest) but not dashboard use.
- All steps are skippable.
- Onboarding never blocks access to the free tier.

## What comes next

- **L130** integrates: watchlist items selected here flow to /settings/watchlist.
- **L131** integrates: alerts cannot fire until email verified.
- **L140** designs the empty-states the role tag controls.
- **L261** prototypes the onboarding flow in code.
- **L289** designs the email drip post-onboarding.

## Related

- [[L121-information-architecture]] — header sign-in button triggers this flow
- [[L130-watchlist-ux]] — step 1 creates the initial watchlist
- [[L131-alerts-ux]] — alerts gated by email verification
- [[L138-pricing-page]] — free tier is the destination of this flow
- [[L140-empty-states]] — role tag controls empty-state copy
- [[L289-onboarding-email-drip]] — follow-up emails
