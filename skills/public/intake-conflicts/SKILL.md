---
name: intake-conflicts
description: >-
  利益冲突核查（场景3，立案合规硬关卡）。新事项录入当事人/对手方/关联方 → 对接企查查 +
  所内客户项目档案跑利冲 → 输出命中记录与关联关系图谱（仅事实，不判断）→ 是否可承接由
  合伙人决定。利冲未清，后续一切环节不得启动（五道硬关卡之一）。触发词："立案利冲"
  "利益冲突核查""conflicts check""新事项立项""关联关系图谱"。
license: Apache-2.0
version: "0.1"
author: PacGate-Law (百宸)
allowed-tools:
  - read_file
  - write_file
  - bash
  - qcc-company
  - qcc-risk
  - qcc-legal-case
  - openviking
required-secrets:
  - QCC_API_KEY
  - OPENVIKING_API_KEY
metadata:
  argument-hint: "[--matter <matter-id>] [--parties <当事人>] [--opponents <对手方>] [--affiliates <关联方>]"
  status: "A2 立案利冲 v0.1 — 场景3 立案合规硬关卡"
  pacgate-tier-routing:
    interview: "low/local"
    conflicts-run: "mid/local"
    graph: "mid/local"
    store: "low/local"
  pacgate-domain: "intake-conflicts"
  pacgate-redline: "只产事实不下结论 + 利冲未清不开工 + 隔离墙对 agent 同样生效 + 即时上报命中"
---

# 利益冲突核查 Skill（百宸 A2）

**红线：** 只产出事实性核查结果（关联关系图谱、命中记录）。"是否构成利冲、是否可承接"的判断权在合伙人。未完成利冲核查的事项，A1 不得启动作业（五道硬关卡：利冲未清不开工）。利冲命中即时上报，不等批处理。

## 一、硬约束

1. **只产事实，不下结论**——"是否构成利冲、是否可承接"的判断权在合伙人。本 skill 只提供关联关系图谱 + 命中记录。
2. **利冲未清不开工**——未完成利冲核查的事项，A1 matter-manager 不得启动作业（硬顺序）。
3. **隔离墙对 agent 同样生效**——检索/RAG 范围按事项隔离，agent 不得跨墙调用被隔离事项的任何内容。本 skill 维护隔离墙，但不读隔离墙内的事项内容。
4. **利冲命中即时上报**——不等批处理。
5. **下游不改上游**——关联关系图谱基于企业数据源 + 所内客户档案，如实记录，不修改。
6. **来源标注**——每条命中记录标注来源（企查查/所内客户档案）+ 检索时间。

## 二、工作流

### Step 0 — 结构化访谈　`tier: Low/本地 · data: 客户敏感`
录入：当事人、对手方、关联方、交易类型、法域。识别文件管辖法（交律师确认）。

### Step 1 — 跑利冲　`tier: Mid/本地 · data: 客户敏感`
- 企查查：qcc-company（工商/股东/关联企业）、qcc-risk（经营风险）、qcc-legal-case（司法涉诉）。
- 所内客户项目档案：read_file（历史 matter-workspace 索引，受隔离墙约束）。
- 对当事人/对手方/关联方逐一跑，输出命中记录。

### Step 2 — 关联关系图谱　`tier: Mid/本地 · data: 客户敏感`
构建当事人/对手方/关联方的关联关系图谱（股权/任职/担保/涉诉/同一实际控制人）。仅事实，不判断是否构成利冲。

### Step 3 — 隔离墙设置　`tier: Mid/本地 · data: 客户敏感`
若需隔离（合伙人决定后），在 OpenViking 为本事项设独立 URI 前缀 `viking://resources/matters/<matter-id>/`，确保隔离墙外角色不可见（含向量库层面）。

### Step 4 — 建 matter-workspace + 台账　`tier: Low/本地 · data: 客户敏感`
建 matter-workspace 目录，登记台账（事项 ID/当事人/对手方/关联方/交易类型/法域/利冲结果/是否可承接[待合伙人定]/隔离墙配置）。

### Step 5 — 入库 OpenViking　`tier: Low/本地 · data: 客户敏感`
可选：关联关系图谱 + 命中记录存入 OpenViking `viking://resources/matters/<matter-id>/conflicts/`，受隔离墙约束。

### Step 6 — 输出
- **命中记录表**：事项/当事人/对手方/关联方/命中类型/命中详情/来源/检索时间。
- **关联关系图谱**：节点（当事人/对手方/关联方）+ 边（股权/任职/担保/涉诉/实控人）。
- **待合伙人判断事项**：集中列出（是否构成利冲、是否可承接、是否需隔离墙）。
- **利冲命中即时上报标记**（如适用）。

## 三、本 skill 不做

- 不替合伙人下"是否构成利冲、是否可承接"的判断。
- 不读隔离墙内的事项内容（即使维护隔离墙）。
- 不启动后续作业（利冲未清不开工）。
- 不下法律结论——本岗不产出对外内容。
- 每条都是事实非结论，是否可承接由合伙人定。