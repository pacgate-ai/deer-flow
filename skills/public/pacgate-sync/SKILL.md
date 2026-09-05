---
name: pacgate-sync
description: >-
  PacGate-Law 三仓库同步：推送 inner pacgate-ai、outer pacgate-law、deer-flow 集成内容
  到各自的 GitHub origin，以便开发者从 JZKK720/* 拉取。包含凭证保护检查（OPERATOR.md、
  法律数据库MCP.md、.env、config.yaml、.deer-flow/ 必须 gitignored）和 VPN 提示。
  触发词："pacgate 同步"、"推送三仓库"、"sync pacgate"、"push to origin"。
license: Apache-2.0
version: "0.1"
author: PacGate-Law (百宸)
allowed-tools:
  - read_file
  - write_file
  - bash
required-secrets: []
metadata:
  argument-hint: "[--repo inner|outer|deer-flow|all] [--dry-run]"
  status: "运维 skill v0.1 — 同步三仓库到 GitHub origin"
  vpn-required: true
  repos:
    inner: "c:\\Users\\pacga\\github-pr\\pacgate-law\\pacgate-ai → origin=JZKK720/pacgate-ai"
    outer: "c:\\Users\\pacga\\github-pr\\pacgate-law → origin=JZKK720/pacgate-law (需创建)"
    deer-flow: "c:\\Users\\pacga\\github-pr\\deer-flow → origin=pacgate-ai/deer-flow"
---

# PacGate-Law 三仓库同步 Skill

## 用途

此 skill 在 VPN-required 客户机上运行，把三仓库的本地状态推送到 GitHub origin，
以便开发者从自己的机器（无需 VPN）拉取 `JZKK720/*` 和 `pacgate-ai/*`。

## 前置检查（每次运行必做）

在推送任何内容之前，验证凭证文件被 gitignored：

```bash
# Inner repo (pacgate-ai)
git -C c:/Users/pacga/github-pr/pacgate-law/pacgate-ai check-ignore \
  assets/pacgate-ai-remote-handbook/OPERATOR.md \
  "assets/智库资料收集/智库资料收集/MCP授权/法律数据库MCP.md"
# 两条都必须返回路径（exit 0）。任一为空 → STOP，gitignore 损坏。

# Outer repo (pacgate-law)
git -C c:/Users/pacga/github-pr/pacgate-law check-ignore \
  pacgate-ai/assets/pacgate-ai-remote-handbook/OPERATOR.md \
  "pacgate-ai/assets/智库资料收集/智库资料收集/MCP授权/法律数据库MCP.md"

# deer-flow repo
git -C c:/Users/pacga/github-pr/deer-flow check-ignore \
  config.yaml extensions_config.json .env .deer-flow/
# 四条都必须返回路径（exit 0）。
```

**任一检查失败 → STOP，不得推送。** 先修复 .gitignore。

## 1. Inner repo: pacgate-ai → JZKK720/pacgate-ai

```bash
git -C c:/Users/pacga/github-pr/pacgate-law/pacgate-ai status
git -C c:/Users/pacga/github-pr/pacgate-law/pacgate-ai log --oneline origin/main..main
# 如果有未推送 commit：
git -C c:/Users/pacga/github-pr/pacgate-law/pacgate-ai push origin main
# 验证：
git -C c:/Users/pacga/github-pr/pacgate-law/pacgate-ai log --oneline origin/main..main
# 应为空
```

凭证：`assets/pacgate-ai-remote-handbook/OPERATOR.md`（gitignored）有 GitHub token。
**绝不打印 token。**

## 2. Outer repo: pacgate-law → JZKK720/pacgate-law（首次推送）

outer repo 无 commit、无 remote。先解决 broken submodule gitlink（mode 160000，
无 .gitmodules）。

### Option A（推荐）：proper submodule

```bash
cd c:/Users/pacga/github-pr/pacgate-law
git rm --cached pacgate-ai
git submodule add https://github.com/JZKK720/pacgate-ai.git pacgate-ai
git commit -m "chore: initial commit with pacgate-ai submodule"
# 在 GitHub 创建空仓库 JZKK720/pacgate-law，然后：
git remote add origin https://github.com/JZKK720/pacgate-law.git
git push -u origin main
```

### Option B：nested folder（非 submodule）

```bash
cd c:/Users/pacga/github-pr/pacgate-law
git rm --cached pacgate-ai
echo "pacgate-ai/" >> .gitignore
git add .gitignore AGENTS.md DEER-FLOW-INTEGRATION.md
git commit -m "chore: initial commit (docs only, pacgate-ai nested)"
git remote add origin https://github.com/JZKK720/pacgate-law.git
git push -u origin main
```

## 3. deer-flow: pacgate 集成内容 → pacgate-ai/deer-flow

```bash
git -C c:/Users/pacga/github-pr/deer-flow status --short
# 应显示 untracked: docs/pacgate/, skills/public/vcpe-financing-suite/
git -C c:/Users/pacga/github-pr/deer-flow add docs/pacgate/ skills/public/vcpe-financing-suite/
git -C c:/Users/pacga/github-pr/deer-flow commit -m "feat(pacgate): add integration doc + VCPE skill skeleton"
git -C c:/Users/pacga/github-pr/deer-flow push origin main
```

**绝不 commit** gitignored 配置：`config.yaml`、`extensions_config.json`、`.env`、
`.deer-flow/`（含 Sylvie SOUL.md + agent config + secrets）。

## VPN 提示

- 此客户机需要 VPN 才能访问 `github.com` 和 `docker.io`。
- 开发者自己的机器无需 VPN，从 `JZKK720/*` 和 `pacgate-ai/*` 拉取。
- 同步状态必须从此机器推送，以便开发者拉取。

## 验证清单

- [ ] inner: `git log --oneline origin/main..main` 为空
- [ ] outer: `git remote -v` 显示 origin = JZKK720/pacgate-law
- [ ] deer-flow: `git status --short` 无 untracked pacgate 内容
- [ ] 三个仓库的凭证文件均 gitignored（前置检查通过）