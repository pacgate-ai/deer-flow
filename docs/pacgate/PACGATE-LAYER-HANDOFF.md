---
artifact_contract: "ce-handoff/v1"
created_at: "2026-09-05T00:00:00Z"
title: "PacGate-Layer reconciliation handoff — apply clean layer to upstream deer-flow"
summary: "Clean pacgate-layer branch (on latest upstream) ready for an upstream agent to merge/build the GHCR pacgate image from."
keywords: ["pacgate", "deer-flow", "layer", "reconciliation", "ghcr", "middleware", "config-hook"]
cwd: "C:/Users/pacga/github-pr/pacgate-law/deer-flow"
resume_focus: "Merge pacgate-layer into JZKK720/deer-flow main (or a PR) and rebuild ghcr.io/jzkk720/deer-flow-pacgate"
repository: "pacgate-ai/deer-flow"
branch: "pacgate-layer"
head: "cdf7a584"
---

# PacGate-Layer Handoff

## Objective

An upstream agent should pick up the **clean PacGate layer** and rebuild the
`ghcr.io/jzkk720/deer-flow-pacgate` image **directly from the upstream repo** so
the fork stays unified and current.

## Where the layer lives

- **Branch:** `pacgate-layer` — pushed to `pacgate-ai/deer-flow` at `cdf7a584`.
- **Base:** current `bytedance/deer-flow` main (`27b2b676`).
- **Local clone:** `C:/Users/pacga/github-pr/pacgate-law/deer-flow`.

The `pacgate-layer` branch is a **complete, verified reconstruction** of the
PacGate work layered onto the latest upstream. It is 3 commits ahead of
`upstream/main`:

1. `0816716c` — re-apply additive assets (58 files, all pure additions, zero
   core-file edits)
2. `ca71db5a` — re-implement config + middleware hooks on upstream/main
3. `cdf7a584` — carry forward matters + skills WIP onto clean layer

## What it contains

### 1. Additive assets (no upstream conflict)
- 34 legal skills in `skills/public/` (NDA, VC/PE, DD, litigation, compliance, etc.)
- `backend/packages/harness/deerflow/config/pacgate_config.py` — typed 3-axis
  routing + 5-hard-gates config models
- `backend/packages/harness/deerflow/agents/middlewares/pacgate_routing_middleware.py`
- `backend/packages/harness/deerflow/agents/middlewares/pacgate_hard_gates_middleware.py`
- `docker/Dockerfile.pacgate`, `docker/docker-compose.prod.yaml`,
  `docker/docker-compose.override.yaml`, `docker/pacgate-entrypoint.sh`
- `.github/workflows/build-pacgate-image.yml` — GHCR build for
  `ghcr.io/jzkk720/deer-flow-pacgate`
- `config.example.pacgate.yaml`, `.env.example.pacgate`,
  `extensions_config.example.pacgate.json`
- `docs/pacgate/*` integration reports

### 2. Core-file hooks (re-implemented on new architecture)
- **`config/app_config.py`**:
  - import `PacGateConfig, load_pacgate_config_from_dict`
  - `pacgate: PacGateConfig = Field(default_factory=PacGateConfig, ...)` on `AppConfig`
  - `load_pacgate_config_from_dict(config.pacgate.model_dump())` in the
    `model_validator` load chain
- **`agents/lead_agent/agent.py`** (`build_middlewares()`):
  - appends `PacGateRoutingMiddleware` + `PacGateHardGatesMiddleware` before
    custom/extension middlewares, gated on `getattr(resolved_app_config, "pacgate", None)`
- **`app/gateway/app.py`**:
  - `matters` router import + `app.include_router(matters.router)` registration

### 3. Carried-forward PacGate WIP
- `backend/app/gateway/routers/matters.py` + frontend `matters` module
  (`page.tsx`, `api.ts`, `hooks.ts`, `index.ts`, `types.ts`)
- 3 extra skills: `antitrust-compliance`, `arbitration`, `bankruptcy-restructuring`
- Diagnostic docs (`MCP-FIX-PHASEA-VERIFICATION.md`, `QM-WEBUI-8182-*`,
  `pi-models.*`, `webui-index.js`)
- `playwright.pacgate-live.config.ts` + pacgate-live tests

## Verification (done)

- ✅ 42 pacgate tests pass: `backend/tests/test_pacgate_hard_gates.py` +
  `test_pacgate_routing_middleware.py`
- ✅ `AppConfig.pacgate` field resolves at runtime
- ✅ Both pacgate middlewares instantiate
- ✅ `matters` router imports and constructs
- ✅ Credentials (`config.yaml`, `extensions_config.json`, `.env`, `.deer-flow/`)
  are gitignored (confirmed `git check-ignore` exit 0)

## Environment notes (Windows box)

- `python` not in PATH — use `C:\Program Files\Python313\python.exe` or the
  venv `backend\.venv\Scripts\python.exe`.
- PowerShell blocks `npx.ps1` — wrap in `cmd.exe /c "npx ..."`.
- Encoding: never `Get-Content`/`Set-Content` on UTF-8 Chinese files (GBK
  mojibake). Use `[System.IO.File]::ReadAllBytes` / `WriteAllBytes`.
- Headless Chrome: use legacy `--headless` (not `--headless=new`).

## Push/remote situation

- **This machine's credentials push to `pacgate-ai/*`** (403 on `JZKK720/*`).
- The developer pulls from `JZKK720/*` (no VPN needed on their machine).
- `pacgate-layer` is pushed to `pacgate-ai/deer-flow` (verified `cdf7a584`).
- `JZKK720/deer-flow` `main` is at `c5685723` (old pacgate commits + stale
  upstream). It needs to be updated to the clean layer.

## Next steps for the upstream agent

1. **Review/merge** `pacgate-layer` into `main` (either on `JZKK720/deer-flow`
   directly if you have those creds, or via a PR).
2. **Rebuild GHCR:** tag/push `main` — the `build-pacgate-image.yml` workflow
   triggers on `push: branches: [main]` (builds `:latest`) and `push: tags: ['v*']`
   (builds `:vX.Y.Z`). Or run `workflow_dispatch`.
3. **Update runtime:** `docker compose -f docker/docker-compose.prod.yaml pull && up -d`.
4. If a versioned release is needed, tag `v0.1.1` → update
   `docker-compose.prod.yaml` image reference to `:v0.1.1`.

## Credentials warning

Do **NOT** commit `OPERATOR.md`, `法律数据库MCP.md`, `config.yaml`,
`extensions_config.json`, `.env`, or `.deer-flow/`. All are gitignored.
