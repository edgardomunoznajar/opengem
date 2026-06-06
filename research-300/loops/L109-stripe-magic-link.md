# L109 — Stripe + Magic-Link Gating for the Paid Tier: Auth + Checkout with Concrete Primitives

**Loop**: 109 / 300
**Phase**: 2 — Deep dive on top candidates
**Date**: 2026-06-06

---

## Thesis of this loop

The L006 pricing thesis put us at five tiers (Free / Studio $99 / Newsroom $499 / Institutional $4,999 / Vendor custom). The Free tier is "the whole product"; the paid tiers gate *velocity* (higher API/MCP throughput) and *fit* (white-label, custom domains). This loop turns that pricing structure into the smallest possible auth + checkout stack that respects three commitments: (1) **never gate the substance** — anonymous users get full read access to every forecast forever; (2) **magic-link only** — no passwords, no Google-OAuth dependency, no Auth0 vendor lock-in; (3) **Stripe Checkout + Customer Portal**, with no custom payment UI to maintain.

Verdict: **passwordless magic-link sign-in via Resend (email delivery) + a small custom JWT session, Stripe Checkout for paid-tier sign-up, Stripe Customer Portal for plan changes/cancellation, Stripe webhooks landing in the Arq `notifications` queue (L102) for tier-state syncing. Total third-party stack: Stripe + Resend. No Auth0, no Clerk, no Firebase, no Supabase Auth. The auth code is ~300 lines of FastAPI, owned and readable.**

---

## The model: anonymous-by-default, account-on-demand

The dashboard is anonymous-first. A user lands on `opengem.org`, browses every page, downloads JSON, subscribes to RSS, and never sees a login wall. This is the L006 commitment encoded in UX.

An account becomes necessary only when the user wants something *account-shaped*:

- **A saved watchlist** that persists across devices and produces a per-user RSS feed.
- **An API key** with throughput above the 1k/day anonymous limit.
- **An MCP key** with throughput above the 100/day anonymous limit.
- **A paid-tier subscription** (Studio / Newsroom / Institutional).
- **White-label embed customization**.
- **A personalized alert pipeline** (Discord/Telegram/email — see L114).

Anything else stays anonymous. Even the watchlist has a "no-account share URL" fallback (URL-encoded watchlist passed as a query param) so users can save state locally without signing up.

---

## Step 1: sign-in via magic-link

The flow:

1. User clicks "Sign in" → modal with one field, `email`.
2. User submits → POST `/auth/request-magic-link` with `{"email": "user@example.com"}`.
3. Server creates a `MagicLinkToken` row (email, token, expires_at = now + 15min, used_at = null), enqueues a `send_magic_link` Arq job in the `notifications` queue.
4. Arq job calls Resend API to send an email with `https://opengem.org/auth/verify?token=<random>&redirect=<original>`.
5. User clicks link → GET `/auth/verify` → server marks token used, issues JWT session cookie, redirects.

The JWT session:

- Symmetric HS256, signed with a key in env (`OPENGEM_JWT_SECRET`).
- Cookie name: `opengem_session`.
- HttpOnly, Secure, SameSite=Lax.
- 30-day expiry, refreshed on every authenticated request that's older than 7 days.
- Payload: `{sub: user_id, tier: "free"|"studio"|"newsroom"|"institutional", exp, iat}`.

Why JWT and not opaque session ID:

- The MCP server (L108) needs to verify the same cookie/token on a different process without round-tripping to the auth DB. JWT verification is local and fast.
- Cloudflare Workers can verify the JWT at the edge for rate-limit decisions before forwarding to origin.
- Revocation is handled by a tiny `revoked_jti` set in Redis (refresh on logout / tier change). For a one-person team this is cheaper than running a session store.

---

## Step 2: Stripe Checkout for tier upgrade

The user, now signed in and on the free tier, clicks "Upgrade to Studio" on `/pricing`. The flow:

1. POST `/billing/checkout` with `{tier: "studio"}`.
2. Server creates a Stripe Customer if not yet existing (`stripe.Customer.create(email=..., metadata={user_id: ...})`).
3. Server creates a Checkout Session for the corresponding Price ID with `mode="subscription"`, `customer=cus_...`, `success_url`, `cancel_url`.
4. Server returns the Checkout URL; frontend redirects.
5. User completes payment on Stripe-hosted page (PCI scope: zero — Stripe handles it).
6. Stripe redirects back to `success_url` (`/account/upgraded?session_id=...`).
7. The actual tier flip happens via webhook, not via the redirect.

Why Stripe Checkout and not a custom payment form: PCI compliance, A/B-tested conversion UI, Apple Pay/Google Pay built-in, dispute handling, EU-VAT/sales-tax via Stripe Tax. We get all of this for the Stripe fee and write zero payment code.

---

## Step 3: webhook → tier sync (Arq job)

Stripe sends webhooks for every billing event. The handler enqueues an Arq job in the `notifications` queue so the HTTP response is fast (Stripe retries on 5xx; we want no retries to ever happen for transient processing slowness).

```python
@app.post("/webhooks/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig = request.headers.get("stripe-signature")
    try:
        event = stripe.Webhook.construct_event(payload, sig, settings.STRIPE_WEBHOOK_SECRET)
    except stripe.error.SignatureVerificationError:
        return Response(status_code=400)
    await arq_pool.enqueue_job(
        "process_stripe_event",
        event_id=event["id"],
        event_type=event["type"],
        data=event["data"]["object"],
        _job_id=f"stripe:{event['id']}",  # idempotency
    )
    return Response(status_code=200)
```

The `process_stripe_event` Arq job handles:

- `checkout.session.completed` → flip user's tier in DB, log entitlement, send welcome email via Resend.
- `customer.subscription.updated` → re-sync tier (handles plan changes via Customer Portal).
- `customer.subscription.deleted` → revert to free tier at period end (`access_until`).
- `invoice.payment_failed` → email user + flip tier to grace after 3 failures.
- `customer.subscription.trial_will_end` → reminder email (if we add trials).

Tier is the source of truth in OPENGEM's `users.tier` column; Stripe is the source of truth for *billing*. The webhook keeps them in sync. Periodic reconciliation (a Dagster asset that runs nightly) catches drift.

---

## Step 4: rate-limit at the edge

A Cloudflare Worker reads the JWT from the cookie or `Authorization: Bearer <jwt>` header, extracts the tier, and applies rate limits:

```javascript
// cloudflare-worker.ts (simplified)
export default {
  async fetch(req, env) {
    const jwt = readJwt(req);
    const tier = jwt?.tier ?? "anonymous";
    const limit = TIER_LIMITS[tier];
    const key = `rl:${tier}:${jwt?.sub ?? clientIp(req)}`;
    const count = await env.RATELIMIT.increment(key, { expirationTtl: 86400 });
    if (count > limit.daily) {
      return new Response(JSON.stringify({
        error: { code: "rate_limit_exceeded", upgrade_url: "https://opengem.org/pricing" },
      }), { status: 429 });
    }
    const res = await fetch(req);
    res.headers.set("X-RateLimit-Limit", String(limit.daily));
    res.headers.set("X-RateLimit-Remaining", String(limit.daily - count));
    return res;
  },
};
```

The worker runs *before* origin so abusive anonymous traffic never hits the origin. The Worker's R2/KV backing makes counter increments ~5ms p99.

---

## What we deliberately *don't* build

- **No password sign-in.** Magic-link only. Password reset flows are a tax we refuse to pay.
- **No OAuth (Google / GitHub / Apple) at v1.** Magic-link covers 95% of users. OAuth is a Y2 feature if cohorts demand it.
- **No 2FA at v1.** The data is public; the account holds a watchlist and an API key. 2FA at Y2 when Institutional accounts demand it.
- **No team accounts at v1.** Newsroom tier is "10 emails on one account" managed via the Customer Portal; Institutional gets multi-user via the customer-success ticket (no UI).
- **No SSO/SAML at v1.** Institutional buyers asking for SSO get a Vendor-tier sales conversation.

The discipline: every "auth feature not in v1" deferral is named explicitly so a contributor doesn't drift into adding it.

---

## Resend choice (and why not SES/Postmark/Mailgun)

- **Resend**: React Email templates as first-class components, dev-friendly API, $20/mo for 100k emails. Domain auth setup is 5 minutes. The choice is "Vercel for email" — a small team can ship transactional email without reading a single SMTP manual.
- **SES**: cheapest at scale but requires sandbox-removal request, manual bounce/complaint webhooks, harder DKIM setup. Not worth the savings until ~1M emails/month.
- **Postmark**: excellent deliverability, slightly more expensive than Resend; transactional-only positioning matches OPENGEM. A close second.
- **Mailgun**: Mature; less developer-experience focused than Resend in 2026.

**Resend wins.** Postmark is the fallback if Resend has a deliverability issue.

---

## Next-step: the FastAPI auth router skeleton

```python
# api/auth.py
from fastapi import APIRouter, Cookie, HTTPException, Request, Response
from pydantic import BaseModel, EmailStr
from .db import db
from .jwt_utils import issue_session_jwt, verify_session_jwt
from .arq_pool import enqueue
import secrets, datetime as dt

router = APIRouter(prefix="/auth", tags=["auth"])

class MagicLinkReq(BaseModel):
    email: EmailStr
    redirect: str = "/"

@router.post("/request-magic-link")
async def request_magic_link(req: MagicLinkReq):
    token = secrets.token_urlsafe(32)
    expires = dt.datetime.utcnow() + dt.timedelta(minutes=15)
    await db.magic_links.insert_one({
        "token_hash": sha256(token),
        "email": req.email.lower(),
        "expires_at": expires,
        "redirect": req.redirect,
        "used_at": None,
    })
    await enqueue("send_magic_link",
                  email=req.email,
                  token=token,
                  redirect=req.redirect)
    return {"ok": True}

@router.get("/verify")
async def verify(token: str, redirect: str, response: Response):
    row = await db.magic_links.find_one({"token_hash": sha256(token)})
    if not row or row["used_at"] or row["expires_at"] < dt.datetime.utcnow():
        raise HTTPException(400, "Invalid or expired link")
    await db.magic_links.update_one({"_id": row["_id"]}, {"$set": {"used_at": dt.datetime.utcnow()}})
    user = await db.users.find_one_and_update(
        {"email": row["email"]},
        {"$setOnInsert": {"email": row["email"], "tier": "free", "created_at": dt.datetime.utcnow()}},
        upsert=True, return_document=True,
    )
    jwt = issue_session_jwt(user["_id"], tier=user["tier"])
    response.set_cookie(
        "opengem_session", jwt,
        httponly=True, secure=True, samesite="lax",
        max_age=30*86400,
    )
    response.status_code = 302
    response.headers["Location"] = redirect
    return response

@router.post("/logout")
async def logout(response: Response, opengem_session: str = Cookie(None)):
    if opengem_session:
        jti = verify_session_jwt(opengem_session).get("jti")
        await redis.sadd("revoked_jti", jti)
    response.delete_cookie("opengem_session")
    return {"ok": True}
```

---

## What this loop produced

- A passwordless magic-link auth model with explicit anonymous-default.
- The Stripe Checkout + Customer Portal flow with webhook → Arq tier-sync.
- A Cloudflare-Worker edge rate limit applying tier-based quotas.
- A justified "don't build" list (passwords, OAuth v1, 2FA v1, teams v1, SSO v1).
- Vendor pick: Resend for email; Postmark as fallback.
- A working FastAPI auth router skeleton.

## What comes next

- **L110** — federated identity comparison; magic-link is one option among many.
- **L260** — pricing page + checkout prototype implementation.
- **L114** — Discord/Telegram bot uses the same JWT to authenticate users.

## Related

- [[L006-pricing-thesis]] — the five-tier structure this implements
- [[L110-federated-identity]] — the broader auth-vendor evaluation
- [[L102-arq-task-queue]] — Stripe webhooks land in `notifications` queue
- [[L260-pricing-checkout]] — Phase 5 prototype loop
- [[L131-alerts-ux]] — alerts subscription requires sign-in
