# PacGate-Law — MCP Fix & Phase A Verification Report

> **Date**: 2026-09-04
> **Scope**: deer-flow MCP tool loading fix + Phase A (UI smoke) Playwright tests
> **Status**: ✅ MCP fix verified · ✅ Phase A complete (2/3 pass, 1 blocked by separate LLM issue)

---

## 1. MCP Tool Loading Fix — VERIFIED

### Symptom
deer-flow gateway loaded **0 MCP tools** (down from 18 on 2026-09-02). Sylvie reported
`pacgate_pacgate_list_connectors` unavailable.

### Root cause (confirmed)
`MultiServerMCPClient.get_tools()` (langchain_mcp_adapters) loads all MCP servers in
parallel via `asyncio.gather()`. `gather` **propagates the first exception**, so one
failing server aborts the entire tool load.

Failing servers (per-server diagnostic):
- **`qcc-history`** (企查查 变更历史) — `McpError: 当前用户未授权使用历史信息服务`
  (QCC API key lacks permission for the history service) — **consistent failure**
- **`qcc-company`** — intermittent TaskGroup failure (flaky)
- **`ansvar`** — 403 Forbidden (also disabled)

Secondary symptom in logs: `UnboundLocalError: cannot access local variable 'tools'`
(secondary bug in langchain_mcp_adapters/tools.py when `_list_all_tools` raises).

### Fix applied
Disabled all 11 `qcc-*` servers + `ansvar` in the **host-mounted runtime config**:

```
C:\pacgate-ai-pr\deploy\client-bundle\deer-flow-extensions-config.json
```

(⚠️ NOT the repo's `deer-flow/extensions_config.json` — that is a stale template.
The active config is bind-mounted read-only into the container at
`/app/deer-flow-extensions-config.json`.)

Then `docker restart deer-flow`.

### Verification (two independent confirmations)

**1. Direct tool-load check inside the container** (venv python):
```
INITIALIZED: 134 MCP tools
```

**2. Live gateway logs** (2026-09-04 04:36:01):
```
deerflow.mcp.cache - INFO - MCP tools initialized: 134 tool(s) loaded
```

### Core tools confirmed present (user's stated principle)
| Asset | Tools | Status |
|---|---|---|
| **pacgate-mcp** | 3 — `pacgate_kb_search`, `pacgate_connector_search`, `pacgate_list_connectors` | ✅ |
| **openviking** (gateway data / RAG) | 15 — `find`, `search`, `read`, `remember`, `write`, `tree`, … | ✅ |
| firecrawl | 27 | ✅ |
| 元典 yuandian (law/case/company/securities) | 54 | ✅ |
| 北大法宝 pkulaw (9 servers) | 10 | ✅ |
| vaquill | 25 | ✅ |
| qcc-* (企查查) | — | ⏸️ disabled (flaky/unauthorized — re-enable later) |
| ansvar | — | ⏸️ disabled (403) |

**Total: 134 MCP tools loaded** (was 0).

---

## 2. Phase A — UI Smoke Tests (Playwright, live stack)

### Setup
- Config: `deer-flow/frontend/playwright.pacgate-live.config.ts`
  (targets the LIVE running stack; no webServer; uses system **Edge** channel
  `channel: "msedge"` because Playwright chromium is not installed on this box)
- Tests: `deer-flow/frontend/tests/pacgate-live/`
  - `deer-flow-smoke.spec.ts` — login + workspace load + send message
  - `qm-smoke.spec.ts` — QM dev sign-in + chat UI load
- Run: `cd deer-flow/frontend; cmd.exe /c "npx playwright test --config=playwright.pacgate-live.config.ts --reporter=line"`

### Credentials used
- **deer-flow**: `pwtest@pacgate-law.com` / `TestPass123!`
  (registered via `POST /api/v1/auth/register` — registration is open)
- **QM**: dev/cookie mode — principal `admin@pacgate-law.com`, no password

### Results

| Test | Result | Notes |
|---|---|---|
| deer-flow: login and load workspace chat UI | ✅ **PASS** | URL → `/workspace/chats/new`, greeting + input visible |
| QM dev sign-in and load chat UI | ✅ **PASS** | "Dev mode — signed in as admin@pacgate-law.com" + chat input |
| deer-flow: send a message and receive a response | ❌ **FAIL** | Message sends, UI renders — but backend LLM returns 400 (see below) |

**2 of 3 pass.** The failure is NOT a UI/test problem — the message was sent and the
UI correctly rendered the backend's error response.

### The one failure — separate backend issue (NOT hallucination, NOT MCP)
```
LLM request failed: Error code: 400
{"error":{"message":"Failed to initialize samplers: failed to parse grammar",
 "type":"invalid_request_error"}}
```
- The model **never ran** — Ollama rejected the request before generation.
- Cause: deer-flow sends a grammar/structured-output constraint that the local
  Ollama model (`ornith-1.5:9b`) cannot parse.
- **Next step**: separate investigation of deer-flow's model-call config vs Ollama.

---

## 3. How to re-run

```powershell
# MCP tool-load verification (inside deer-flow container)
docker cp <check_mcp_final.py> deer-flow:/tmp/
docker exec deer-flow /app/backend/.venv/bin/python /tmp/check_mcp_final.py

# Phase A UI smoke tests
cd C:\Users\pacga\github-pr\pacgate-law\deer-flow\frontend
cmd.exe /c "npx playwright test --config=playwright.pacgate-live.config.ts --reporter=line"
```

## 4. Follow-ups (tabled, per user decision)

1. **qcc-* re-enable**: obtain a QCC API key with the `history` service permission;
   re-enable one server at a time, verifying each loads before the next.
2. **ansvar re-enable**: fix the 403 (token/permission) then re-enable.
3. **Ollama grammar error**: investigate deer-flow's structured-output/grammar
   parameter vs `ornith-1.5:9b` capabilities — blocks real chat end-to-end.
4. **Phase B (tool-call verification)**: blocked by #3 — needs a working chat run
   to trigger `pacgate_kb_search` from the UI.