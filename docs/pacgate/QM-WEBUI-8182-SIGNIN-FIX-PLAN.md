# QM Web UI (8182) — Sign-In Fix Plan (exact commands)

> Date: 2026-09-03 · Status: **OPTION A APPLIED & VERIFIED** (sign-in works)
> Stack: `ghcr.io/yc-software/qm` (web-ui 8182, core 8180, pg), network `qm-pacgate`

## Confirmed root cause

The qm stack runs in **full production portal mode** with **no portal service**:

| Component | State | Effect |
|---|---|---|
| core | `NODE_ENV=production`, `CORE_SIGNING_SECRET` set, `PORTAL_IDENTITY_SECRET`+`CAPABILITY_SECRET` set | `requirePortalIdentity = Boolean(requireSignedPortalIdentity \|\| production)` = **true** → user-scoped routes need `x-portal-identity` token |
| web-ui | `CORE_SIGNING_SECRET` set → `AUTH_MODE="portal"` | `POST /signin` returns 404; only portal-issued identity works |
| portal | **not running** (no image locally) | nothing mints identity tokens → login/register impossible |

**Key subtlety:** the web-ui uses `CORE_SIGNING_SECRET` to sign its requests to the core
(`signedHeaders`). If you unset it on the web-ui alone, the core rejects with
`401 source-auth`. So the fix must be coordinated across **both** containers.

**Second key subtlety:** because core is `NODE_ENV=production`, `requirePortalIdentity` is
forced true. Dev mode therefore requires changing core's `NODE_ENV` to non-production, not
just unsetting secrets.

---

## Option A — Dev mode (no auth) — fastest, local/personal use

**Security warning:** this removes authentication entirely. Anyone who can reach the ports
is trusted. Do NOT use for a multi-user / production law-firm deployment.

### A1. Recreate core in dev mode
```bash
docker rm -f qm-pacgate-core
docker run -d --name qm-pacgate-core \
  --network qm-pacgate \
  -e NODE_ENV=development \
  -e ALLOW_UNAUTHENTICATED_CORE=1 \
  -e DATABASE_URL='postgres://postgres:88c13a1d33b3a39d1aaa846c89c323a5@pg:5432/qm' \
  -e ORG_ID=pacgate \
  -e HARNESS=pi \
  -e SANDBOX_BACKEND=local \
  -e MODEL_BASE_URL='http://host.docker.internal:11434/v1' \
  -e PUBLIC_WEB_URL='http://localhost:8182' \
  -e WEB_UI_PUBLIC_URL='http://localhost:8182' \
  -e PUBLIC_API_URL='http://localhost:8180' \
  -e CORE_API_URL='http://core:8080' \
  -e PORT=8080 \
  -p 8180:8080 \
  ghcr.io/yc-software/qm/core@sha256:bee03e7f22719dfe76ea2c83bb65db2bdefd55b714eae4014007033800bdb5ab
```
> Note: `NODE_ENV=development` + `ALLOW_UNAUTHENTICATED_CORE=1` + no `CORE_SIGNING_SECRET`
> → `requirePortalIdentity=false` and unsigned source auth allowed. Keep `DATABASE_URL` so
> the existing data (36 tables) is preserved.

### A2. Recreate web-ui in dev/cookie mode
```bash
docker rm -f qm-pacgate-web-ui
docker run -d --name qm-pacgate-web-ui \
  --network qm-pacgate \
  -e NODE_ENV=development \
  -e CORE_API_URL='http://core:8080' \
  -e CORE_ORG_ID=pacgate \
  -e WEB_UI_PUBLIC_URL='http://localhost:8182' \
  -e PORT=8080 \
  -p 8182:8080 \
  ghcr.io/yc-software/qm/web-ui@sha256:f037834fd726bcff220245665ef46accb10b476331006a85c59defbde1635e52
```
> No `CORE_SIGNING_SECRET` → `COOKIE_AUTH=true` → `AUTH_MODE="dev"` → `POST /signin` works.
> Optionally add `-e WEB_UI_PRINCIPALS='alice,bob'` to restrict who may sign in.

### A3. Verify
- Open `http://localhost:8182` → should show a sign-in form (not "through the portal").
- Sign in with a principal id (e.g. `admin`).
- Confirm `/me` returns 200 and the chat surface loads.

---

## Option B — Real portal (keep production auth) — production-correct

Requires the portal service that mints `x-portal-identity` tokens. **No portal image exists
locally** (`docker images` shows only `core` + `web-ui`). Steps:
1. Obtain the portal image/config from `ghcr.io/yc-software/qm` (or the qm repo).
2. Run the portal on the `qm-pacgate` network, sharing `PORTAL_IDENTITY_SECRET`.
3. Reach the web-ui **through the portal address** (the web-ui cannot authenticate on its own).
4. Register/login users via the portal.

---

## Recommended next step
User to pick **A** (fast, local) or **B** (production). No container changes were made during
this diagnosis. When you choose, I'll execute the exact commands above and verify sign-in.

---

## ✅ APPLIED — Option A (dev mode) — 2026-09-03

Both containers were recreated in dev mode. Sign-in now works.

### What was done
1. **core** recreated with `NODE_ENV=development`, `ALLOW_UNAUTHENTICATED_CORE=1`, and **no**
   `CORE_SIGNING_SECRET`. Data volume `qm-pacgate-coredata` and the skills/tools bind mounts
   were preserved. `DATABASE_URL` unchanged → existing data intact.
2. **web-ui** recreated with `NODE_ENV=development` and **no** `CORE_SIGNING_SECRET` →
   `AUTH_MODE="dev"` → `POST /signin` works.
3. **Network alias fix:** the recreated core lost its `core` DNS alias, so the web-ui couldn't
   resolve `http://core:8080` (502 `getaddrinfo ENOTFOUND core`). Fixed with:
   ```bash
   docker network disconnect qm-pacgate qm-pacgate-core
   docker network connect --alias core qm-pacgate qm-pacgate-core
   ```

### Verification (passed)
- `POST /signin` → **200** `{"ok":true,"user":"admin@pacgate-law.com"}` + `set-cookie: webuiuser=...`
- `GET /me` → **200** `{"user":"admin@pacgate-law.com","org":"pacgate","mode":"dev",...}`
- Browser `http://localhost:8182` → **"Dev mode — no identity provider, signed in as
  admin@pacgate-law.com"** + chat UI loads.
- Core `:8180` `/healthz` and `/v1/surface-config` → **200**.

### Known follow-up (NOT auth)
`POST /api/turn` returns **403** when actually sending a chat message. This is a **separate
concern** from sign-in — it's about running an agent turn (model provider reachability /
capability minting), not authentication. Sign-in itself is fully working.

---

## 🔍 `/api/turn` 403 — root cause (traced 2026-09-03)

**Symptom:** sending a chat message → `403 {"status":"refused","reason":"that model isn't
available on this deployment (its provider isn't configured)"}`.

**Root cause (pre-existing, NOT caused by the dev-mode change):**
- The core's model resolution (`src/model/pi-models.ts`) only supports **3 providers**:
  `anthropic`, `openai`, `openrouter` — each requires its API key env var
  (`ANTHROPIC_API_KEY` / `OPENAI_API_KEY` / `OPENROUTER_API_KEY`).
- The core has **none of these keys set** → `modelProviderConfigured:false` (confirmed via
  `GET /v1/surface-config`).
- The `MODEL_NAME=ornith-1.5:9b` and `MODEL_BASE_URL=http://host.docker.internal:11434/v1`
  env vars point at local Ollama, but **the core's provider selection never reads
  `MODEL_BASE_URL`** — the openai provider hardcodes `https://api.openai.com/v1` and requires
  `OPENAI_API_KEY`. So the Ollama config is effectively dead for the core's turn path.
- `app-turn.ts:166` refuses the turn because `modelServiceable(runtime.modelId, providers)`
  is false (no provider key present).

**This was already broken before Option A** — the original core env had the same
`MODEL_NAME`/`MODEL_BASE_URL` and no provider keys.

### Options to make chat work
1. **Set a real provider key** on core (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, or
   `OPENROUTER_API_KEY`) → `modelProviderConfigured:true` and turns run against that cloud
   provider. Requires a paid key.
2. **Wire Ollama as an OpenAI-compatible provider** — the core's openai provider hardcodes
   the base URL, so this needs either a code change or a proxy that maps
   `https://api.openai.com/v1` → local Ollama. More involved.
3. **Leave chat disabled** — sign-in works; only agent turns are refused until a provider is
   configured.

> This is a config/architecture decision (which model provider to use), so it was left for the
> user to choose rather than guessed.

### ⚠️ Important correction (2026-09-03)
The user believed the **Ollama API was already configured** and that assigning the Ollama cloud
model would enable chat. **This is NOT the case.** Verified evidence:
- `MODEL_BASE_URL=http://host.docker.internal:11434/v1` and `MODEL_NAME=ornith-1.5:9b` are set
  on the core container, **but nothing in the core source or the pi-ai library reads
  `MODEL_BASE_URL`** (searched `/app/src` and `/app/node_modules/@earendil-works/pi-ai/dist`).
- The core's model resolution (`src/model/pi-models.ts`) only supports `anthropic`/`openai`/
  `openrouter`, each requiring its API key env var. None is set → `modelProviderConfigured:false`.
- The openai provider (`pi-ai/dist/providers/openai.js`) **hardcodes**
  `https://api.openai.com/v1` and only reads `OPENAI_API_KEY` — no base-URL env override exists.
- Ollama IS reachable at `:11434` (returns 200, `ornith-1.5:9b` available), but the core has
  **no mechanism to route to it** without a code change or a proxy.

**Conclusion:** enabling chat requires either a real cloud provider API key, or a code change /
proxy to point the openai provider at Ollama. This is an architectural decision that was left
for the user (unavailable at the time) rather than guessed.

---

## ✅ DONE — Chat enabled via local Ollama (2026-09-03)

The user authorized wiring local Ollama. Implemented a **surgical code change** to the core's
`src/model/pi-models.ts`:

### What was changed
1. **Added a custom model entry** to `MODEL_REGISTRY`:
   ```ts
   {
     id: "glm-5.3-flash:cloud",
     name: "GLM 5.3 Flash (Ollama)",
     fastMode: false, webui: true, base: true,
     custom: { template: "gpt-4.1-mini", baseUrl: "http://host.docker.internal:11434/v1" },
   }
   ```
2. **Extended `ModelEntry`** with an optional `custom: { template, baseUrl }` field.
3. **Updated `resolveModel()`** to handle `custom` — it clones the `gpt-4.1-mini` openai model
   (provider `openai`, api `openai-responses`) and overrides `baseUrl` to point at Ollama.
4. **Set a dummy `OPENAI_API_KEY=ollama-local`** on the core container so the openai provider is
   "configured" (Ollama ignores the key value). This makes `modelServiceable()` return true.

### Why this works
- Ollama at `:11434` supports the **OpenAI Responses API** (`/v1/responses`) — verified with
  `glm-5.3-flash:cloud` returning a valid response.
- The pi-ai openai provider uses `model.baseUrl` directly (verified in
  `pi-ai/dist/api/openai-responses.js:183`), so overriding `baseUrl` to Ollama routes correctly.
- The model's `provider` is `openai`, so it's serviceable once `OPENAI_API_KEY` is set.

### Verification (passed)
- `GET /v1/surface-config` → `modelProviderConfigured:true`, `glm-5.3-flash:cloud` in webuiModels.
- `POST /api/turn` with `model:"glm-5.3-flash:cloud"` → **202 Accepted** (was 403 before).
- Run completed: `status:"done"`, `result.status:"ok"`, real reply from the model.
- Browser UI: chat input active, model selector shows the model, no 403.

### ⚠️ Persistence note
The `pi-models.ts` edit lives in the container's writable layer. **If the core container is
recreated, the edit is lost** and must be re-applied (re-copy the file + restart). The
`OPENAI_API_KEY` env var is in the `docker run` command, so it persists across recreation.
For a durable fix, the change should be committed to the qm source repo and rebuilt into the
image.

---

## ↩️ Rollback to production portal mode (Option B later)

To restore the original production config (and later stand up the portal), recreate both
containers with the original env vars captured during diagnosis:

### Core (production)
```bash
docker rm -f qm-pacgate-core
docker run -d --name qm-pacgate-core --network qm-pacgate --restart unless-stopped \
  -v qm-pacgate-coredata:/data \
  -v /run/desktop/mnt/host/c/pacgate-ai-pr/deploy/qm-pacgate/sandbox/skills:/layer/skills:ro \
  -v /run/desktop/mnt/host/c/pacgate-ai-pr/deploy/qm-pacgate/sandbox/tools:/layer/tools:ro \
  -e NODE_ENV=production \
  -e CORE_SIGNING_SECRET='4f3ee12a2701392aebeb23327294484a8d2aedbbce7004f70d55d5f7c0e38e1e' \
  -e DATABASE_URL='postgres://postgres:88c13a1d33b3a39d1aaa846c89c323a5@pg:5432/qm' \
  -e CAPABILITY_SECRET='a441ecd2f7074187685f5f1b4e62cb87b32fef016a778bd1900b9b089a50546f' \
  -e CONNECTOR_SECRET_KEY='47da66bc5e08e966613a0949e065c33bd163a4b29754a9178b151762dd695547' \
  -e PORTAL_IDENTITY_SECRET='ee1e014403f4dea96834170939fca48e218d689b5192c28a46fed759c07b5074' \
  -e PUBLIC_API_URL='http://localhost:8180' \
  -e SKILL_SIGNING_SECRET='1d679466b3ca7b6244de0222d79e6a8aab9929b937ce79d3b4dc6a8dc5666685' \
  -e MODEL_BASE_URL='http://host.docker.internal:11434/v1' \
  -e ORG_ID=pacgate -e WEB_UI_PUBLIC_URL='http://localhost:8182' \
  -e SANDBOX_BACKEND=local -e SESSION_STORE=postgres -e RUN_STORE=postgres \
  -e DEPLOYMENT_LAYER=/layer -e PORT=8080 -e HARNESS=pi -e MODEL_NAME='ornith-1.5:9b' \
  -e PUBLIC_WEB_URL='http://localhost:8182' -e DATA_DIR=/data \
  -p 8180:8080 \
  ghcr.io/yc-software/qm/core@sha256:bee03e7f22719dfe76ea2c83bb65db2bdefd55b714eae4014007033800bdb5ab
docker network disconnect qm-pacgate qm-pacgate-core
docker network connect --alias core qm-pacgate qm-pacgate-core
```

### Web-ui (production)
```bash
docker rm -f qm-pacgate-web-ui
docker run -d --name qm-pacgate-web-ui --network qm-pacgate --restart unless-stopped \
  -e NODE_ENV=production \
  -e CORE_SIGNING_SECRET='4f3ee12a2701392aebeb23327294484a8d2aedbbce7004f70d55d5f7c0e38e1e' \
  -e PORTAL_IDENTITY_SECRET='ee1e014403f4dea96834170939fca48e218d689b5192c28a46fed759c07b5074' \
  -e PORT=8080 -e CORE_API_URL='http://core:8080' -e CORE_ORG_ID=pacgate \
  -e WEB_UI_PUBLIC_URL='http://localhost:8182' \
  -p 8182:8080 \
  ghcr.io/yc-software/qm/web-ui@sha256:f037834fd726bcff220245665ef46accb10b476331006a85c59defbde1635e52
```

> After rollback, sign-in will again require the portal (Option B). The data volume is
> preserved throughout — no data loss either way.
