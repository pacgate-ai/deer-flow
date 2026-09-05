---
name: nda-review
description: >-
  NDA 审查（场景5，单文档主笔制）。按本所 Playbook 红线逐条审查 NDA、出 redline（Word 修订模式）→
  引证核验 → 二次复核（红线遗漏与条款冲突检查）。另设 GREEN/YELLOW/RED 三级分流：GREEN 走快速
  通道，YELLOW/RED 升级人工。触发词："NDA审查""保密协议审查""NDA三级分流""保密协议redline"。
license: Apache-2.0
version: "0.1"
author: PacGate-Law (百宸)
allowed-tools:
  - read_file
  - write_file
  - bash
  - officecli
  - pkulaw
  - yuandian-law
  - openviking
required-secrets:
  - YUANDIAN_API_KEY
  - PKULAW_BEARER_TOKEN
  - OPENVIKING_API_KEY
metadata:
  argument-hint: "[--mode review|redline] [--side discloser|recipient] [--triage green|yellow|red]"
  status: "单文档主笔 v0.1 — 场景5 NDA 审查 + GREEN/YELLOW/RED 三级分流"
  pacgate-tier-routing:
    triage: "low/local"
    review: "mid/local"
    redline: "main/local"
    cite-verify: "low/local"
  pacgate-domain: "transaction-doc"
  pacgate-redline: "单文档主笔制 + Playbook红线逐条 + GREEN/YELLOW/RED分流 + redline交付 + 来源分级 + 律师逐条接受/拒绝"
---

# NDA 审查 Skill（百宸，场景5）

**红线：** 输出为供律师复核的草稿，非最终法律意见。单文档主笔制——一名承办律师主笔，按本所 Playbook 红线逐条审查、出 redline（Word 修订模式）。GREEN 走快速通道，YELLOW/RED 升级人工。主笔律师逐条接受/拒绝修订；高风险强制主办律师加签；合伙人签发。

## 一、单文档主笔制（与尽调线并行不同）

回填件 §2.1 场景5-8 为**单文档主笔制**（写密集、单文档），不用 swarm：
- **主笔**：一名承办律师（associate agent）单线程持笔，按 Playbook 出 redline。
- **复核**：A6 反方复核（红线遗漏与条款冲突检查）+ A5 引文核验，串行把关。
- **定稿**：主笔律师逐条接受/拒绝修订（Word 修订模式交付）。
- **签发**：高风险（含 NDA 中涉及竞业/独家/长保密期等）强制主办律师加签 → 合伙人签发。

## 二、GREEN/YELLOW/RED 三级分流

NDA 另设三级分流（回填件 §2.1 场景5）：

| 级别 | 判定标准 | 处理 |
|---|---|---|
| **GREEN** | 标准模板、无重大偏离、我方立场无明显风险 | 快速通道：批量审查表 + 微调建议，不强制主办律师加签 |
| **YELLOW** | 存在非标准条款、对我方有中等风险、需谈判 | 升级人工：逐条 redline + 风险标注 + 谈判建议，主办律师复核 |
| **RED** | 重大偏离模板、对我方有重大风险、含竞业/独家/长保密期/高额违约金 | 升级人工：逐条 redline + P0/P1 风险标注 + 强制主办律师加签 → 合伙人签发 |

分流判定标准来自本所 Playbook（`.deer-flow/playbooks/nda-playbook.md`，存在则覆盖；否则提示 `cold-start-interview`）。

## 三、硬约束

1. **单文档主笔制**——不用 swarm，单线程持笔，避免写冲突。
2. **Playbook 红线逐条**——按本所 NDA Playbook 红线逐条审查，不漏。
3. **三态标注**——每条审查意见：有问题/无问题/资料不足；"资料不足"不得推断补齐。
4. **来源分级必标**——权威核验/元典辅助/内部模板/模型推断。
5. **检索稀薄即停**。
6. **redline 交付**——Word 修订模式，逐条可接受/拒绝，批注引用 Playbook 红线立场。
7. **GREEN/YELLOW/RED 分流**——按 §二 判定标准分流，YELLOW/RED 升级人工。
8. **主笔律师逐条接受/拒绝**——agent 出 redline，律师定稿。
9. **强制免责声明**+"供律师复核草稿"水印。

## 四、工作流

### Step 0 — 加载 Playbook + 确认立场　`tier: Low/本地 · data: 客户敏感`
加载顺序：`.deer-flow/playbooks/nda-playbook.md`（本所专属，存在则覆盖）→ OpenViking `find "NDA playbook"` → 缺失则提示 `cold-start-interview` 或"临时模式"。
确认立场：披露方（discloser）/ 接收方（recipient）——决定全部条款方向（保密信息范围、保密期限、违约金、竞业/独家等）。

### Step 1 — 三级分流判定　`tier: Low/本地 · data: 客户敏感`
按 §二 判定标准判 GREEN/YELLOW/RED。GREEN 走快速通道（批量审查表 + 微调建议）；YELLOW/RED 进入 Step 2 逐条 redline。

### Step 2 — 逐条审查 + redline　`tier: Main/本地 · data: 客户敏感`
按 Playbook 红线逐条审查 NDA 条款，对每条偏离产出标准块（Playbook 立场/协议原文/差距/法律风险🔴🟠🟡🟢/最小粒度红线/对方不让步 fallback），用 officecli 出 Word redline（修订模式，批注引用 Playbook 立场）。

NDA 核心条款审查清单：
- 保密信息定义与范围
- 保密义务范围（使用限制、复制限制）
- 保密期限（固定期限/无限期/终止后存续）
- 例外情形（已公开、合法获得、独立开发、依法披露）
- 知识产权归属与保留
- 竞业/独家限制（如适用——RED 级触发强制主办律师加签）
- 违约责任与违约金（是否过高/过低）
- 争议解决与管辖
- 返还/销毁义务
- 通知条款
- 适用法律（涉外）
- 签署与生效

### Step 3 — 引证核验（A5）　`tier: Low/本地 · data: 公开法源`
对每条法律依据（如《反不正当竞争法》§9、《民法典》保密条款）调用 pkulaw/yuandian-law 核验现行有效性 + 来源分级。✘/⚠ 项退回 + 台账留痕。

### Step 4 — 二次复核（A6）　`tier: Main/本地 · data: 客户敏感`
红线遗漏检查（Playbook 红线是否漏审）+ 条款冲突检查（如保密期限与返还义务冲突）。A6 只追加质疑，不改写。

### Step 5 — 输出　`tier: Mid/本地 · data: 客户敏感`
- **NDA redline docx**（Word 修订模式，逐条可接受/拒绝，批注引用 Playbook 立场）
- **分流判定报告**：GREEN/YELLOW/RED + 判定理由 + 是否需主办律师加签
- **审查备忘录**：逐条表（条款号/条款标题/风险等级/风险描述/修改建议/修改后文本/Playbook 立场引用）
- **待律师确认事项**（选择题，附默认建议）

## 五、本 skill 不做

- 不替主笔律师定稿——agent 出 redline，律师逐条接受/拒绝。
- 不替合伙人签发——草稿生成，人来办。
- 不替你下最终法律意见。
- 不并行起草（单文档主笔制）——避免写冲突。
- 不跳过 A5/A6。
- 不无声填补——检索稀薄即停。
- 每条都是线索非结论，正式用前须律师核验。