# R26 — Security and Privacy Boundary

| Field | Value |
|---|---|
| Document ID | OG1-RES-026 |
| Revision | A (2026-05-24) |
| Date | 2026-05-24 |
| Status | **Cross-cutting design memo: data classification, secrets, threat model.** |
| Authority | NFR-SEC-001, POL-07 |

---

## 1. Why this exists

OPENGEM handles macro time series and publishes forecasts. Nothing in scope is sensitive in the PII sense (POL-07). But the system does have **secrets** (API keys, deploy credentials) and **trust assets** (reproducibility hashes, V&V results) that must be protected.

This memo specifies the security boundary at the level appropriate for a single-maintainer, public-code, public-data system.

## 2. Data classification

| Class | Examples | Storage |
|---|---|---|
| **Public-by-design** | All forecasts, leaderboard, V&V results, model cards, code | Postgres + Git public |
| **Public-by-source** | All raw observations (US government data, ORDRA, etc.) | Postgres |
| **Operational secrets** | API keys (BEA, BLS, Census), DB password, deploy SSH key, GHCR push token | SOPS + age encrypted in repo |
| **Personal use logs** | API access logs (if owner uses own server) | Local; not committed |

**No PII anywhere.** OPENGEM has no user accounts in the meaningful sense at Block I — public dashboard is anonymous; MCP / API key access is owner + agents only.

## 3. Threat model

| Threat | Severity | Mitigation |
|---|---|---|
| API key leakage from GitHub | High | SOPS encryption; pre-commit hook scans for unencrypted secrets |
| Compromised VM | Medium-High | VM hardening (UFW, fail2ban, no password SSH); admin via SSH key + 2FA |
| Public dashboard defaced | Medium | Vercel platform-level protection; build from Git on tag only |
| Database breach (data exfil) | Low | All data is public-by-design or public-by-source; only secret is owner-level access; PG protected with strong password |
| Supply-chain attack via Python deps | Medium | `uv.lock` pinned; CI fails on deps with known CVEs (osv-scanner); manual review on dep upgrades |
| Supply-chain attack via R deps (BGVAR) | Low-Medium | `BGVAR` is CRAN-hosted with reproducible builds; pin specific version |
| DoS on public API | Low | Single-maintainer; low-traffic; Cloudflare-style proxy if needed |
| Vintage archive corruption | Medium | Per-vintage SHA hashes; replay-and-diff CI; daily integrity check job |
| ToS violation (FRED archiving) | High | ADR-010 mandates upstream substitution; FRED only for queries |
| Adversarial inputs to MCP server | Low-Medium | Validate all MCP tool inputs; rate-limit per-key |

## 4. Secret management

### 4.1 Storage

- `.sops.yaml` config in repo root.
- Encrypted secrets in `deploy/secrets/*.enc.yaml`.
- `age` key file: owner laptop + locked-down recovery copy.
- Unencrypted secrets never committed.

### 4.2 Rotation

| Secret | Rotation cadence | How |
|---|---|---|
| BEA / BLS / Census API keys | Annual | Re-register; update SOPS |
| DB password | Annual | Postgres role rotation |
| GHCR push token | Annual | GitHub PAT rotation |
| Deploy SSH key | Annual | Generate new keypair; revoke old |
| MCP / API keys for personal agents | Per-month | Self-issue, log |

### 4.3 Compromise response

If a secret is suspected compromised:

1. Revoke immediately (per-source revocation flow).
2. Rotate to a new value via SOPS workflow.
3. Audit log for any usage during the compromise window.
4. Document incident in `docs/security/incidents/YYYY-MM-DD.md`.

## 5. Public dashboard / API security

### 5.1 Public read

- Public dashboard is statically generated; rebuild from Git tag.
- Public REST API is read-only; serves forecasts, leaderboard, V&V results, run metadata.
- No write endpoints exposed to anonymous traffic.

### 5.2 MCP / Authenticated tools

- MCP server exposes write tools (e.g., `scenario(...)`).
- Authentication: API key (32+ char random), Bearer header.
- Per-key rate limit: 60 req/min default; configurable.
- Per-key audit log of every request.
- Keys are scoped (e.g., `scenario:write`, `forecast:read`).

### 5.3 Admin operations

- All admin via SSH + 2FA.
- No web admin interface at Block I.
- Deploys are CI-driven only; no SSH-then-edit-in-place.

## 6. Reproducibility integrity

The hash quintuple (R16) is the core trust artifact. Defenses:

- All hashes stored in Postgres with FK constraints; no overwrites.
- Posterior parquet files stored in MinIO with versioning and immutability.
- Replay-and-diff CI catches any unauthorized modification of a published forecast.
- All hash-bearing tables have `INSERT-only` permission grants; updates are forbidden at the DB role level.

## 7. Audit and logging

- Application logs: structured JSON, Loki-collected.
- Audit-grade logs (provenance, hash changes, secret rotations): separate append-only table.
- Retention: 90 days for app logs; forever for audit-grade.

## 8. Public security disclosure

- `SECURITY.md` in repo root with vulnerability disclosure email.
- 30-day responsible-disclosure window for non-critical issues.
- Critical issues acknowledged within 48h.

## 9. What's NOT in scope at Block I

- SOC 2 / ISO compliance (deferred to Block IV+ if non-profit / external users).
- Pen-test by professional firm (deferred to v0.4+ if public dashboard sees meaningful traffic).
- Multi-tenant security (deferred to Block III sovereign-hosting if pursued).
- Privacy regulations (no PII, no users → GDPR/etc. effectively N/A at Block I).

## 10. Bottom line

OPENGEM is a low-risk public-data project. Security boundary is **secret management + vintage archive integrity + reproducibility hash chain**. No PII concerns. Public dashboard is statically generated. MCP server is API-key authenticated and rate-limited. The threat model is dominated by routine credential hygiene, not by sophisticated adversaries.

---

*End of R26 Rev A.*
