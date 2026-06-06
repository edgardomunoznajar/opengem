# L110 — Federated Identity: Auth.js vs Lucia vs Better-Auth vs Clerk-OSS — Pick One

**Loop**: 110 / 300
**Phase**: 2 — Deep dive on top candidates
**Date**: 2026-06-06

---

## Thesis of this loop

L109 picked magic-link as the auth UX and described a hand-rolled ~300-line FastAPI auth router. That's the *backend* answer. This loop tests whether OPENGEM should instead adopt a *library* that ships the auth flows as components and saves the hand-rolling — Auth.js (formerly NextAuth), Lucia, Better-Auth, or Clerk-OSS — *and* sets the foundation for Y2 features (Google OAuth, SAML SSO, team accounts) that we deferred in L109.

The question is non-obvious because the answer turns on whether OPENGEM is fundamentally a **Next.js full-stack app** (in which case Auth.js's tight integration matters a lot) or a **FastAPI backend with a Next.js frontend** (in which case the auth library has to be agnostic). We pick the latter — the FastAPI backend is where Stripe webhooks, Arq jobs, MCP tools, and rate-limited APIs already live; bolting auth onto Next.js would create a second source of truth we'd then have to keep synced with the backend.

Verdict: **Better-Auth, configured in TypeScript-Node sibling-service mode, fronting the same Postgres OPENGEM already uses. The Next.js frontend uses Better-Auth's client. The FastAPI backend verifies the same JWT/session cookie via a tiny middleware that re-reads the same Postgres tables. Auth.js loses because it's Next.js-first. Lucia loses because it's deprecated as of 2024-2025 and the migration path is Lucia → Better-Auth. Clerk-OSS loses because it's a partial OSS-ification of the Clerk SaaS, with the most valuable pieces (UI components, OAuth providers) still gated. Magic-link + Google OAuth + email-password + future SAML all sit on top of Better-Auth without code rewrites.**

---

## Auth.js (NextAuth): the Next.js-first option

**Strengths.**

- The most-installed Next.js auth library; if you Google "Next.js auth," every result points here.
- Battle-tested OAuth provider list (Google, GitHub, Apple, 50+ others).
- Database-adapter pluggable: works with Postgres, Prisma, Drizzle, custom adapters.
- Magic-link, OAuth, credentials, all in one library.

**Weaknesses for OPENGEM.**

- The mental model is "Next.js owns auth." Sessions are stored either as JWT (stateless) or in DB tables addressed via a NextAuth Prisma adapter. Either way, the *primary auth surface* is Next.js API routes. OPENGEM's MCP server, FastAPI backend, and Cloudflare Worker need to verify those sessions independently. Doing that with Auth.js means: either (a) every backend service learns to read Auth.js's session table schema, or (b) we add a `getSession()` endpoint to Next.js that backends call — adding a hop on every API request.
- The recent Auth.js v5 rewrite (still settling in 2026) churned the API surface; sample code from 2024 doesn't always still work.
- The "Edge runtime" support is partial; the database adapter doesn't run on Edge.

If OPENGEM were a pure Next.js app with no separate backend, Auth.js would be the obvious pick. We have a separate backend. **SKIP**.

---

## Lucia: the dead-letter option

**Strengths.**

- Lightweight (~5KB), framework-agnostic, minimal-API. Built around primitives, not auth flows.
- The author's design philosophy ("auth should be unbundled") matches OPENGEM's "own the source" ethos.

**Weaknesses.**

- **Deprecated.** The author (pilcrowOnPaper) announced in late 2024 that Lucia would stop being actively developed and recommended users migrate to Better-Auth (which is by a different author who carried the philosophy forward).
- The migration path Lucia → Better-Auth is documented; the migration Auth.js → Better-Auth is not. So adopting Lucia means adopting a thing destined to be migrated.

**SKIP**. Going to a deprecated library at the start of v1 is malpractice.

---

## Clerk-OSS: the partial open-sourcing

**Strengths.**

- The Clerk SaaS is genuinely excellent at hosted auth UI: drop-in `<SignIn />` and `<SignUp />` components with TOTP, passkeys, SSO. If you don't care about open-source, Clerk is a strong choice.
- They open-sourced a `clerk-elements` library in 2024 that gives the React components without the hosted backend.

**Weaknesses for OPENGEM.**

- The hosted-Clerk pricing starts at $25/mo and ramps quickly. Their "starter" tier caps at 10k MAU and lacks SAML.
- The OSS pieces (`clerk-elements`) are *components only* — they assume you're using the Clerk backend. Self-hosting the Clerk backend isn't supported.
- Adopting Clerk locks you into a vendor relationship — the lock-in is structural, not just contractual.

OPENGEM's "open-source substrate" promise (L008) is hard to reconcile with a closed-backend auth dependency. **SKIP**.

---

## Better-Auth: the recommended pick

**Strengths.**

- Framework-agnostic; designed to work with Next.js, SvelteKit, Astro, plain Express, FastAPI (with a small Python bridge). The TypeScript core runs as a Node service or embeds in any TS server.
- Storage-agnostic: Postgres (recommended), MySQL, MongoDB, SQLite. Schema is explicit and ownable.
- Email + password, magic-link, social OAuth (Google, GitHub, Apple, 30+ providers), passkeys, two-factor — all first-class.
- Plugin model: SSO/SAML is a plugin (`@better-auth/sso`), team accounts is a plugin (`@better-auth/organization`), Stripe subscription syncing is a plugin (`@better-auth/stripe`). We opt-in as we need them.
- Session storage is configurable: cookies + JWT (stateless), DB sessions (stateful), Redis (high-throughput). We pick cookies + JWT to align with the L109 design.
- Active and growing in 2026; the GitHub issue tracker is responsive, the docs are good, there's an MIT license.
- The auth tables are *just Postgres tables you own*. Backend services (FastAPI, MCP, Cloudflare Worker) can read the same `user`, `session`, `account` tables directly with no Better-Auth client dependency.

**The trade-off.**

- Newer than Auth.js — fewer Stack Overflow answers, fewer third-party tutorials. The team has to read Better-Auth's docs as the primary reference rather than copying community recipes.
- The Node sibling-service adds a small operational footprint (~50MB, one process). For OPENGEM at v1, this is acceptable.

**ADOPT-V1.**

---

## The integration shape

```
┌─────────────────┐      ┌──────────────────┐
│  Next.js client │ ────►│  Better-Auth     │
│  (browser cookie│      │  Node service    │
│   + client lib) │      │  (TypeScript)    │
└─────────────────┘      └────────┬─────────┘
                                  │ owns these
                                  ▼ Postgres tables:
                         ┌──────────────────┐
                         │  user            │
                         │  session         │
                         │  account         │
                         │  verification    │
                         │  organization    │
                         └──────────────────┘
                                  ▲ reads (no writes)
                                  │
┌────────────────────────────────┴───┐
│  FastAPI backend                   │
│  (Python — auth_middleware verifies│
│   cookie/JWT, fetches user row)    │
└────────────────────────────────────┘
                                  ▲ reads (no writes)
                                  │
┌────────────────────────────────┴───┐
│  Cloudflare Worker                 │
│  (verifies JWT, applies tier limit)│
└────────────────────────────────────┘
```

Better-Auth's Node service owns *writes* (user creation, session issuance, OAuth callback handling). FastAPI and the Worker are *read-only* against the same Postgres. This gives us a single source of truth for "who is signed in" while letting each backend stay in its own language.

---

## Migration path from L109's hand-rolled auth

L109 described ~300 lines of FastAPI code that does magic-link and JWT issuance. The migration:

1. Stand up Better-Auth as a sibling Node service.
2. Configure it with the email+password and magic-link plugins.
3. Point the Next.js frontend at Better-Auth's `signIn`/`signOut` endpoints.
4. Replace FastAPI's `/auth/*` routes with a thin Better-Auth `/api/auth/*` proxy (or move that path to the Node service directly).
5. FastAPI auth middleware reads the same session cookie, verifies JWT, fetches `user` row from Postgres.
6. Stripe webhook → Arq job (unchanged from L109) updates `user.tier`.

Net code change: ~300 hand-rolled lines deleted, ~80 lines of Better-Auth config added, ~50 lines of FastAPI middleware unchanged but pointing at the same DB. Net loss of code surface to maintain. Net gain: Google OAuth, GitHub OAuth, passkeys, two-factor, all become config changes, not new code.

---

## Plugin roadmap

When OPENGEM needs each Y2 feature, we install the plugin and configure:

- **Google OAuth + GitHub OAuth** — `@better-auth/social-providers`. Probably ship at v1.1 (within 3 months) once we've seen demand.
- **Passkeys** — `@better-auth/passkey`. Y2 nice-to-have.
- **Two-factor (TOTP)** — `@better-auth/two-factor`. Y2 when Institutional buyers ask.
- **Team accounts** — `@better-auth/organization`. Y2 when Newsroom tier needs proper multi-user.
- **SSO/SAML** — `@better-auth/sso`. Y2-Y3 when Institutional buyers' procurement teams ask.
- **Stripe subscription syncing** — `@better-auth/stripe`. Evaluate replacing the hand-rolled Arq webhook handler at Y1.5 once the plugin is stable enough.

Each plugin is opt-in; we pay zero complexity for the ones we don't install.

---

## Why not "just hand-roll forever"

The L109 hand-rolled solution works for v1. The reason we adopt Better-Auth anyway: **Google OAuth at Y1.5 is non-negotiable for the volume cohort**, and hand-rolling OAuth correctly (PKCE, state validation, refresh tokens, account-linking edge cases) is ~1000 lines and a security review. The Better-Auth plugin is one config block.

The choice isn't "magic-link or library"; it's "magic-link forever, or magic-link + OAuth + future SSO at the cost of ~80 lines of config now." The latter is the dominant strategy.

---

## Next-step: the Better-Auth config skeleton

```typescript
// auth-service/src/auth.ts
import { betterAuth } from "better-auth";
import { magicLink } from "better-auth/plugins";
import { pg } from "./db";
import { Resend } from "resend";

const resend = new Resend(process.env.RESEND_API_KEY);

export const auth = betterAuth({
  database: pg,                       // OPENGEM's existing Postgres
  baseURL: "https://opengem.org",
  secret: process.env.OPENGEM_JWT_SECRET!,
  session: {
    expiresIn: 60 * 60 * 24 * 30,     // 30 days
    cookieCache: { enabled: true, maxAge: 60 * 5 },
  },
  emailAndPassword: { enabled: false }, // magic-link only at v1
  plugins: [
    magicLink({
      sendMagicLink: async ({ email, token, url }) => {
        await resend.emails.send({
          from: "auth@opengem.org",
          to: email,
          subject: "Sign in to OPENGEM",
          react: MagicLinkEmail({ url }),
        });
      },
      expiresIn: 60 * 15,
    }),
    // Plugin slots — add as needed:
    // socialProviders({ google: {...}, github: {...} }),
    // organization(),
    // sso(),
    // stripe({ ... }),
  ],
});
```

```python
# api/middleware/auth.py — FastAPI side
from fastapi import Request, HTTPException
from .db import db_pg
from .jwt_utils import verify_better_auth_jwt

async def auth_middleware(request: Request, call_next):
    token = request.cookies.get("better-auth.session_token") \
            or request.headers.get("authorization", "").removeprefix("Bearer ")
    if token:
        try:
            claims = verify_better_auth_jwt(token, secret=settings.JWT_SECRET)
            user = await db_pg.fetch_one(
                "SELECT id, email, tier FROM \"user\" WHERE id = $1", claims["sub"]
            )
            request.state.user = user
        except Exception:
            request.state.user = None
    else:
        request.state.user = None
    return await call_next(request)
```

---

## What this loop produced

- A verdict: Better-Auth in Node sibling-service mode, FastAPI + Worker read against same Postgres.
- A reasoned rejection of Auth.js (Next.js-first), Lucia (deprecated), and Clerk-OSS (partial OSS lock-in).
- An integration diagram showing the read/write split.
- A plugin roadmap mapping Y1.5/Y2/Y3 features to Better-Auth plugins.
- A migration path from L109's hand-rolled auth.
- A Better-Auth config + FastAPI middleware skeleton.

## What comes next

- **L109** (already complete) — wired with this pick.
- **L260** — pricing/checkout prototype uses Better-Auth client.
- **L131** — alerts UX assumes signed-in user via the same session.

## Related

- [[L109-stripe-magic-link]] — the auth UX this loop implements
- [[L102-arq-task-queue]] — Stripe webhooks still land in Arq notifications queue
- [[L131-alerts-ux]] — alerts require account
- [[L130-watchlist-ux]] — watchlist is the anonymous→account conversion driver
- [[L260-pricing-checkout]] — Phase 5 prototype loop
