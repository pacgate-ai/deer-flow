---
name: contract-review
description: >-
  商务合同审查（场景6，单文档主笔制）。按本所 Playbook 红线逐条审查商务合同、出 redline
  （Word 修订模式）→ 引证核验 → 二次复核。立场自适应（买方/卖方/出租方/承租方/委托方/受托方）。
  触发词："商务合同审查""合同审查""合同redline""SaaS合同""租赁合同""采购合同""经销合同"。
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
  - yuandian-case
  - openviking
required-secrets:
  - YUANDIAN_API_KEY
  - PKULAW_BEARER_TOKEN
  - OPENVIKING_API_KEY
metadata:
  argument-hint: "[--mode review|redline] [--side buyer|seller|lessor|lessee|principal|agent] [--contract-type saas|lease|purchase|distribution]"
  status: "单文档主笔 v0.1 — 场景6 商务合同审查"
  pacgate-tier-routing:
    review: "mid/local"
    redline: "main/local"
    cite-verify: "low/local"
  pacgate-domain: "transaction-doc"
  pacgate-redline: "单文档主笔制 + Playbook红线逐条 + 立场自适应 + redline交付 + 来源分级 + 律师逐条接受/拒绝"
---

# 商务合同审查 Skill（百宸，场景6）

**红线：** 输出为供律师复核的草稿，非最终法律意见。单文档主笔制——一名承办律师主笔，按本所 Playbook 红线逐条审查、出 redline（Word 修订模式）。立场自适应（买方/卖方/出租方/承租方/委托方/受托方）。

## 一、单文档主笔制

同 `nda-review`：主笔-复核双人组，单线程持笔，避免写冲突。主笔律师逐条接受/拒绝修订；合伙人签发。

## 二、硬约束

1. **单文档主笔制**——不用 swarm。
2. **Playbook 红线逐条**——按本所商务合同 Playbook 红线逐条审查。
3. **立场自适应**——买方/卖方/出租方/承租方/委托方/受托方，决定条款方向。
4. **三态标注**——每条审查意见：有问题/无问题/资料不足。
5. **来源分级必标**。
6. **检索稀薄即停**。
7. **redline 交付**——Word 修订模式，逐条可接受/拒绝。
8. **主笔律师逐条接受/拒绝**。
9. **强制免责声明**+"供律师复核草稿"水印。

## 三、工作流

### Step 0 — 加载 Playbook + 确认立场 + 合同类型　`tier: Low/本地 · data: 客户敏感`
加载顺序：`.deer-flow/playbooks/contract-playbook-<type>.md`（本所专属，存在则覆盖）→ OpenViking `find "<合同类型> playbook"` → 缺失则提示 `cold-start-interview`。
确认：立场（买方/卖方/...）+ 合同类型（SaaS/租赁/采购/经销/技术许可等）。

### Step 1 — 形式审查　`tier: Low/本地 · data: 客户敏感`
合同名称与内容匹配性、当事人信息完整性、签署与生效条件、附件清单完整性、页码与条款编号连续性。

### Step 2 — 实质性条款逐条审查 + redline　`tier: Main/本地 · data: 客户敏感`
按 Playbook 红线逐条审查，对每条偏离产出标准块 + officecli 出 Word redline。商务合同核心条款审查清单（参照 律师日常通用Prompts指南 §1.1）：
- 定义条款
- 标的条款
- 数量与质量
- 价格与支付
- 交付与验收
- 权利义务对等性
- 违约责任（违约情形穷尽、违约金合理性、违约与解除关系）
- 合同解除（解除条件、清算安排、单方解除权）
- 不可抗力
- 保密条款
- 知识产权（归属、许可、侵权责任）
- 竞业/排他（如适用）
- 保证与陈述
- 争议解决（管辖/仲裁对我方是否有利）
- 适用法律（涉外）
- 通知条款
- 合同修改与转让
- 可分割性/完整协议

每条标注风险等级（🔴必须修改/🟡建议修改/🟢可接受）+ 立场视角评析（我方/对方/市场惯例）。

### Step 3 — 引证核验（A5）　`tier: Low/本地 · data: 公开法源`
对每条法律依据（如《民法典》合同编相关条款）核验现行有效性 + 来源分级。

### Step 4 — 二次复核（A6）　`tier: Main/本地 · data: 客户敏感`
红线遗漏检查 + 条款冲突检查（如违约金条款与解除条款冲突、验收标准与付款节点不匹配）。

### Step 5 — 输出　`tier: Mid/本地 · data: 客户敏感`
- **合同 redline docx**（Word 修订模式）
- **审查备忘录**：逐条表（条款号/条款标题/风险等级/风险描述/修改建议/修改后文本/立场视角）
- **整体风险评估**：🔴高风险条款/🟡中风险/🟢低风险
- **待律师确认事项**（选择题，附默认建议）

## 四、本 skill 不做

- 不替主笔律师定稿——redline 出，律师逐条接受/拒绝。
- 不替合伙人签发。
- 不并行起草（单文档主笔制）。
- 不跳过 A5/A6。
- 不无声填补。
- 每条都是线索非结论，正式用前须律师核验。