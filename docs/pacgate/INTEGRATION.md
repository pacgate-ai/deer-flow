# PacGate-Law (百宸法律 AI) — DeerFlow Integration

> **Status**: 2026-07-18 — Phase 0 + Phase 1 implementation complete; sync state documented.
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

## What's been implemented (Phase 0 + Phase 1)

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
- ✅ `config.yaml` — 3-tier models (main/mid/low), hermes ACP agent, scheduler
  enabled, `agents_api.enabled: true`, memory with CJK-aware char token counting
- ✅ `extensions_config.json` — 12 MCP servers: 3× 元典 (HTTP), 1× 北大法宝 (HTTP),
  4× 企查查 (HTTP), CourtListener (stdio, disabled), Vaquill (stdio, disabled),
  SEC EDGAR (stdio), OfficeCLI (stdio)
- ✅ `.env` template — all PacGate secret env vars (model tier keys + legal MCP keys)
- ✅ Sylvie custom agent — `.deer-flow/users/default/agents/sylvie/` with `SOUL.md`
  (ported persona) + `config.yaml` (model: main, skills: null)
- ✅ `skills/public/vcpe-financing-suite/SKILL.md` — ported VCPE skill skeleton with
  YAML frontmatter (allowed-tools, required-secrets, 3-axis routing metadata)

## What's next (Phase 2+)

### Phase 2 — P0/P1 skills porting (BLOCKED — skeletons missing)
**⚠ Blocker**: 6 of 7 skill skeletons are missing from pacgate-law. Before B1 DD
report MVP can proceed, the following must be drafted or obtained:
- `cold-start-interview` (P0 — light rewrite)
- `matter-workspace` (P0 — direct-use)
- `tabular-review` (P0 — direct-use, signature anti-fabrication)
- `diligence-issue-extraction` (P1 — rewrite to China 11-chapter framework)
- `deal-team-summary` (P1 — direct-use)
- `closing-checklist` (P1 — China transaction conditions)
- `report-assembly` (B1 deliverable — new, uses OfficeCLI for docx)

### Phase 3 — Scheduled tasks & cron
- Enable `scheduler.enabled: true` (done in config.yaml)
- Create tasks via HTTP API after `make dev`:
  - `openwiki-regen`: cron `0 3 * * *` Asia/Shanghai
  - `regulation-sync`: cron `0 6 * * *` Asia/Shanghai

### Phase 4 — 3-axis routing & compliance middleware (B1.5, critical path)
- Custom middleware at slot 18 in `build_middlewares()` (before ClarificationMiddleware)
- Axis A (complexity/risk) → model tier routing
- Axis B (compliance) → client-sensitive data local-only, de-id before cloud
- Axis C (resilience) → high-risk forced upgrade, no silent degradation
- Audit logging for every routing decision + de-id gate event

### Phase 5 — ironclaw integration (deferred to B2+)
- Write `ironclaw-acp` adapter (~1 day, mirrors `@zed-industries/codex-acp`)
- OR run ironclaw standalone as MCP client

## Config files (all gitignored)

| File | Purpose |
|---|---|
| `config.yaml` | Models (3-tier), ACP agents (hermes), scheduler, agents_api, memory |
| `extensions_config.json` | Legal MCP servers (12), OfficeCLI, skills enable state |
| `.env` | PacGate secrets (model API keys, legal MCP credentials) |
| `.deer-flow/users/default/agents/sylvie/SOUL.md` | Sylvie persona (ported from pacgate-law) |
| `.deer-flow/users/default/agents/sylvie/config.yaml` | Sylvie agent config (model: main) |
| `skills/public/vcpe-financing-suite/SKILL.md` | VC/PE financing suite skill (ported skeleton) |

## Key corrections from the original integration doc

1. **Legal MCP servers are HTTP, not stdio npm** — 元典/北大法宝/企查查 are HTTP
   streamable MCP servers. The draft `extensions_config.json` in
   `DEER-FLOW-INTEGRATION.md` §5.1 used placeholder `npx` commands — replaced with
   real HTTP URLs.
2. **Scheduled tasks are API-created, not in config.yaml** — `config.yaml` only has
   `scheduler.enabled: true`. Tasks are created via `POST /api/scheduled-tasks` with
   field `prompt` (not `message`), `schedule_type`, `schedule_spec`, `timezone`.
3. **6 of 7 skill skeletons are missing** — the pacgate-law index lists 7 skeletons
   but only 1 (VCPE) was committed. B1 is blocked until skeletons are drafted.

## Verification checklist

- [ ] `uv run python ../scripts/doctor.py` passes (config validation)
- [ ] `make dev` starts all services (Gateway + Frontend + Nginx)
- [ ] MCP tools (yuandian, pkulaw, qcc, officecli) appear in tool list
- [ ] `invoke_acp_agent` with `hermes` works
- [ ] Sylvie persona renders in `<soul>` block of system prompt
- [ ] `/vcpe-financing-suite` slash-activation loads SKILL.md
- [ ] `cd backend && make lint && make test` pass