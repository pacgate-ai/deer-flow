# PacGate-Law (百宸法律 AI) — DeerFlow Integration

> **Status**: 2026-07-21 — Phase 0–4 implementation complete; 5 hard gates + 3-axis routing middleware shipped; 42 tests passing.
> **Source repo**: `C:\Users\pacga\github-pr\pacgate-law` (read-only assets)
> **Bridge doc**: `pacgate-law/DEER-FLOW-INTEGRATION.md`

## Git sync state (2026-07-18)

- **Branch**: `main` (up to date with `origin/main` = `9a4c72db`)
- **Remotes**: `origin` = `github.com/pacgate-ai/deer-flow.git` (your fork),
  `upstream` = `github.com/bytedance/deer-flow.git`
- **Untracked PacGate content** (NOT yet committed/pushed):
  - `docs/pacgate/INTEGRATION.md` — this file
  - `skills/public/vcpe-financing-suite/SKILL.md` — ported VCPE skill skeleton
- **Gitignored (do NOT commit)**: `config.yaml`, `extensions_config.json`, `.env`,
  `.deer-flow/` (contains Sylvie SOUL.md + agent config with secrets). Verified by
  deer-flow's `.gitignore`.

### To push (run from deer-flow repo root)

```
git add docs/pacgate/ skills/public/vcpe-financing-suite/
git commit -m "feat(pacgate): add integration doc + VCPE skill skeleton"
git push origin main
```
Before adding, verify gitignored configs are excluded:
```
git check-ignore config.yaml extensions_config.json .env .deer-flow/
```
All four must return their paths (exit 0). If any is empty, **STOP** — the gitignore
is broken and secrets would be committed.

### VPN note

This client machine requires VPN to reach `github.com`. The developer's own machine
pulls from `pacgate-ai/deer-flow` without VPN. Push from this machine so the developer
can pull.

## What this is

The PacGate-Law legal-AI system (百宸律师事务所) integrated into deer-flow as the
agent workspace harness. DeerFlow provides ACP agent integration (hermes
config-only), MCP consumption (`extensions_config.json`), `SKILL.md` skills,
`scheduled_tasks` cron, custom-agent `SOUL.md` persona, and a multi-tier model
factory — covering ~80% of PacGate's needs out of the box.

## What's been implemented (Phase 0–4)

### Phase 0 — Security & verification
- ✅ Credentials: `pacgate-law/.../法律数据库MCP.md` is gitignored (confirmed)
- ✅ Missing skill skeletons verified: **6 of 7 skeletons are MISSING** from
  pacgate-law (only `skill骨架_VCPE投融资协议套.md` exists). The B1 DD skeletons
  (diligence-issue-extraction, tabular-review, practice_profile) are referenced
  in the index as "已起草骨架" but were never committed. **Action required**: draft
  these skeletons before B1 can proceed, or obtain them from the author.
- ✅ Legal MCP install commands verified: Chinese DBs (元典/北大法宝/企查查) are
  **HTTP streamable MCP servers** (not stdio npm packages — the integration doc's
  draft was wrong). CourtListener/Vaquill/SEC EDGAR are stdio. See
  `extensions_config.json` for real URLs/commands.

### Phase 1 — DeerFlow bootstrap (B0 foundation)
- ✅ `config.yaml` — 3-tier models (main/mid/low → Ollama gemma4:e2b-it-q8_0), 7 A-series
  subagents in `custom_agents`, scheduler enabled, `agents_api.enabled: true`, memory
  (deermem with local gemma4), `pacgate:` section (routing + hard gates)
- ✅ `extensions_config.json` — 12 MCP servers: 3× 元典 (HTTP), 1× 北大法宝 (HTTP),
  4× 企查查 (HTTP), CourtListener (stdio, disabled), Vaquill (stdio, disabled),
  SEC EDGAR (stdio), OfficeCLI (stdio), OpenViking (HTTP, port 1933)
- ✅ `.env` template — all PacGate secret env vars (model tier keys + legal MCP keys)
- ✅ 5 role-tier custom agents — `.deer-flow/users/default/agents/{sylvie,supervising-associate,
  associate,paralegal,conflicts-officer}/` each with `SOUL.md` + `config.yaml` (refined
  skills whitelists: sylvie=16, supervising-associate=5, associate=10, paralegal=3,
  conflicts-officer=1)
- ✅ 16 PacGate skills — `skills/public/{dd-report-assembly,regulation-research,
  intake-conflicts,offshore-dd,nda-review,contract-review,ma-agreement-review,
  vcpe-financing-suite,corporate-equity,finance-tax,labor-hr,regulatory-compliance,
  cold-start-interview,tabular-review,diligence-issue-extraction,pacgate-sync}/SKILL.md`
  all with YAML frontmatter (pacgate-tier-routing + pacgate-redline metadata)
- ✅ 7 A-series subagents — matter-manager, intake-conflicts, research-agent,
  cite-checker, devils-advocate, doc-pipeline, report-assembly (in config.yaml
  `subagents.custom_agents`)
- ✅ OpenViking context DB — Docker container (port 1933), local file-based vectordb,
  Ollama bge-m3 embeddings, MCP endpoint at `/mcp`, matter-isolation via URI scoping
  verified
- ✅ deermem + OpenViking layered memory — deermem for conversation, OpenViking for
  matter knowledge
- ✅ DD report skill + regulation-sync cron job — scheduler enabled, task created via
  HTTP API

## What's next (Phase 5+)

### Phase 5 — ironclaw integration (deferred to B2+)
- Write `ironclaw-acp` adapter (~1 day, mirrors `@zed-industries/codex-acp`)
- OR run ironclaw standalone as MCP client

### E2E smoke test (pending)
- `make dev` starts all services (Gateway + Frontend + Nginx)
- MCP tools (yuandian, pkulaw, qcc, officecli, openviking) appear in tool list
- Sylvie persona renders in `<soul>` block of system prompt
- Skill slash-activation loads SKILL.md
- Gate 1 blocks matter-work skills until `/intake-conflicts` is activated
- Gate 3 blocks `write_file` to report paths without cite-verified marker
- `cd backend && make lint && make test` pass

### Phase 4 — 3-axis routing & 5 hard gates middleware (B1.5) — ✅ COMPLETE
- ✅ `backend/packages/harness/deerflow/config/pacgate_config.py` — Pydantic config models for `pacgate.routing` (axis_a/axis_b/axis_c) + `pacgate.hard_gates` (gate1–gate5)
- ✅ `backend/packages/harness/deerflow/agents/middlewares/pacgate_routing_middleware.py` — `PacGateRoutingMiddleware` hooks `wrap_model_call`, injects advisory system-reminders from skill frontmatter `metadata.pacgate-tier-routing` + `metadata.pacgate-redline`
  - Axis A (complexity → tier): reads `pacgate-tier-routing` dict, injects tier-routing hint
  - Axis B (compliance → local-only / de-id): reads `pacgate-redline` for `local-only` / `deid-required` tags
  - Axis C (resilience → forced upgrade): reads `pacgate-redline` for `high-risk` tag, recommends escalation
- ✅ `backend/packages/harness/deerflow/agents/middlewares/pacgate_hard_gates_middleware.py` — `PacGateHardGatesMiddleware` hooks `wrap_tool_call`, system-enforced:
  - Gate 1 (利冲未清不开工): blocks 11 matter-work skills until `intake-conflicts` loaded in `skill_context`
  - Gate 3 (引证未核验不上行): blocks `write_file` to report paths (`**/dd-report*`, `**/尽职调查*`) without `<!-- pacgate:cite-verified:` marker
  - Gates 2, 4, 5: disabled in config (advisory / SOUL.md only)
- ✅ Wired into `build_middlewares()` in `agent.py` (before `TerminalResponseMiddleware` + `ClarificationMiddleware`)
- ✅ `config.yaml` — `pacgate:` section with all 3 axes + 5 gates configured
- ✅ `backend/tests/test_pacgate_routing_middleware.py` — 17 tests (axis A/B/C hints, metadata extraction, injection)
- ✅ `backend/tests/test_pacgate_hard_gates.py` — 25 tests (gate 1 block/allow, gate 3 block/allow, async, fail-open)
- ✅ All 42 PacGate tests pass; full backend suite: 7734 passed, 84 pre-existing failures (none PacGate-related)

## Config files (all gitignored)

| File | Purpose |
|---|---|
| `config.yaml` | Models (3-tier Ollama), 7 A-series subagents, scheduler, agents_api, memory, `pacgate:` section (routing + hard gates) |
| `extensions_config.json` | 12 MCP servers (元典/北大法宝/企查查/SEC EDGAR/OfficeCLI/OpenViking) |
| `.env` | PacGate secrets (model API keys, legal MCP credentials, OpenViking key) |
| `.deer-flow/users/default/agents/{sylvie,supervising-associate,associate,paralegal,conflicts-officer}/` | 5 role-tier custom agents (SOUL.md + config.yaml each) |
| `skills/public/{16 PacGate skills}/SKILL.md` | 16 legal task skills with pacgate-tier-routing + pacgate-redline metadata |
| `backend/packages/harness/deerflow/config/pacgate_config.py` | Pydantic config models for pacgate.routing + pacgate.hard_gates |
| `backend/packages/harness/deerflow/agents/middlewares/pacgate_routing_middleware.py` | 3-axis advisory routing middleware (wrap_model_call) |
| `backend/packages/harness/deerflow/agents/middlewares/pacgate_hard_gates_middleware.py` | Gate 1 + Gate 3 enforcement middleware (wrap_tool_call) |
| `backend/tests/test_pacgate_routing_middleware.py` | 17 tests for routing middleware |
| `backend/tests/test_pacgate_hard_gates.py` | 25 tests for hard gates middleware |

## Key corrections from the original integration doc

1. **Legal MCP servers are HTTP, not stdio npm** — 元典/北大法宝/企查查 are HTTP
   streamable MCP servers. The draft `extensions_config.json` in
   `DEER-FLOW-INTEGRATION.md` §5.1 used placeholder `npx` commands — replaced with
   real HTTP URLs.
2. **Scheduled tasks are API-created, not in config.yaml** — `config.yaml` only has
   `scheduler.enabled: true`. Tasks are created via `POST /api/scheduled-tasks` with
   field `prompt` (not `message`), `schedule_type`, `schedule_spec`, `timezone`.
3. **~~6 of 7 skill skeletons are missing~~** — resolved: all 16 PacGate skills
   have been authored directly in `skills/public/` with YAML frontmatter including
   `pacgate-tier-routing` and `pacgate-redline` metadata. The original pacgate-law
   skeletons were used as reference but all skills are now self-contained.

## Verification checklist

- [x] `config.yaml` loads with `pacgate:` section (AppConfig.pacgate populated)
- [x] `build_middlewares()` includes `PacGateRoutingMiddleware` + `PacGateHardGatesMiddleware`
- [x] 42 PacGate tests pass (`test_pacgate_routing_middleware.py` + `test_pacgate_hard_gates.py`)
- [x] Full backend suite: 7734 passed, 84 pre-existing failures (none PacGate-related)
- [x] 16 PacGate skills on disk with frontmatter metadata
- [x] 5 role-tier custom agents (sylvie=16 skills, supervising-associate=5, associate=10, paralegal=3, conflicts-officer=1)
- [x] 7 A-series subagents in config.yaml (matter-manager, intake-conflicts, research, cite-checker, devils-advocate, doc-pipeline, report-assembly)
- [x] 12 MCP servers in extensions_config.json (including OpenViking)
- [x] OpenViking Docker deployment + matter-isolation verified
- [x] Gateway API starts on port 8001 — health endpoint returns `healthy`
- [x] 65 MCP tools loaded from 12 servers (gateway startup log confirmed)
- [x] 1 ACP agent (hermes) loaded
- [x] PacGate config verified live: routing.axis_a/b/c enabled, hard_gates.gate1/gate3 enabled
- [x] Middleware chain verified: [21] PacGateRoutingMiddleware → [22] PacGateHardGatesMiddleware → [23] TerminalResponseMiddleware → [25] ClarificationMiddleware
- [x] Sylvie agent loads: model=main, 16 skills whitelisted
- [ ] nginx not installed on this Windows machine (use Docker mode or WSL for full `make dev`)
- [ ] Frontend not started (requires nginx for unified endpoint; Gateway API verified directly)
- [ ] Gate 1 live enforcement (requires authenticated API call with skill activation)
- [ ] Gate 3 live enforcement (requires authenticated API call with write_file to report path)