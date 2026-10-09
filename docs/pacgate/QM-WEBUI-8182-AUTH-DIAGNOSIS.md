# QM Web UI (8182) — Login/Register/Auth Bottleneck Diagnosis

> Date: 2026-09-03 · Status: **DIAGNOSED, NOT FIXED** (user unavailable; no changes made)
> Stack: `ghcr.io/yc-software/qm` (web-ui + core + pg), network `qm-pacgate`

## Symptom

Opening `http://localhost:8182` shows:
- "Your session ended" → clicking **Sign in** → `http://localhost:8182/auth/login?returnTo=%2F`
- Page: **"Sign in through the portal"** — *"This surface is reached through the portal, and
  signing in there didn't produce a session for it. Open the portal address directly rather than
  this one."*
- Console: `Failed to load resource: 401 (Unauthorized)`
- Core API (`:8180`) returns `401 {"error":"unauthorized","message":"missing, invalid, or stale
  source-auth headers"}`

## Root cause (Phase 1 — evidence)

The Web UI is running in **portal auth mode**, not dev/cookie mode.

From `qm-pacgate-web-ui` `/app/server/index.ts`:
```js
const COOKIE_AUTH = !CORE_SIGNING_SECRET || ALLOW_UNSIGNED_TEST_IDENTITY;
const AUTH_MODE = COOKIE_AUTH ? "dev" : "portal";
```

`docker inspect qm-pacgate-web-ui` shows `CORE_SIGNING_SECRET=4f3ee12a...` **is set** →
`COOKIE_AUTH = false` → `AUTH_MODE = "portal"`.

Consequences in portal mode:
1. `POST /signin` returns **404** (the handler is gated by `if (!COOKIE_AUTH) return 404`).
2. Auth requires a valid `x-portal-identity` token (JWT signed with `PORTAL_IDENTITY_SECRET`),
   verified by `verifyPortalIdentity()` in `src/auth/portal-identity.ts`.
3. The core enforces the same: `src/api/server.ts` returns
   `401 "portal identity required"` for user-scoped / web-turn / admin routes when no valid
   portal identity is present.
4. **No portal service is running** on the `qm-pacgate` network (only `web-ui`, `core`, `pg`).
   So nothing can mint `x-portal-identity` tokens → nobody can authenticate → registration/login
   is impossible.

## Containers (evidence)

| Container | Port | Role |
|---|---|---|
| `qm-pacgate-web-ui` | 8182→8080 | Web UI surface (portal mode) |
| `qm-pacgate-core` | 8180→8080 | Headless core API |
| `qm-pacgate-pg` | 5432 | Postgres (36 tables, no users/accounts table) |

## Two valid fixes (mutually exclusive — pick one)

### Option A — Switch Web UI to dev/cookie auth (fastest, local use)
Unset `CORE_SIGNING_SECRET` on the `qm-pacgate-web-ui` container so `COOKIE_AUTH = true` →
`AUTH_MODE = "dev"`. Then `POST /signin` works and users sign in with a principal id.
Optionally set `WEB_UI_PRINCIPALS` to restrict who may sign in.
- **Tradeoff:** dev-mode auth; not the production-correct path.

### Option B — Stand up a real portal service (production-correct)
Run the portal that issues `x-portal-identity` tokens (signed with `PORTAL_IDENTITY_SECRET`),
and reach the Web UI through the portal address. This is how the stack is designed to work.
- **Tradeoff:** more work; need the portal image/config.

## Recommended next step
User to pick A or B. No container changes were made during this diagnosis.
