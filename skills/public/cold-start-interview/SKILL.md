---
name: cold-start-interview
description: >-
  立项访谈（modular intake interview）。新事项/新项目的结构化访谈——目标公司、交易类型
  （股权/资产/增资）、买卖方、行业、重点关注、报告模板、保留意见口径；访谈结果写入
  practice profile，作为后续 skill 的工作上下文。当 playbook 缺失时，本 skill 是
  nda-review/contract-review/ma-agreement-review/vcpe-financing-suite 的兜底入口。
  触发词："立项访谈""cold-start""新事项访谈""practice profile 初始化""新项目立项"。
license: Apache-2.0
version: "0.1"
author: PacGate-Law (百宸)
allowed-tools:
  - read_file
  - write_file
  - bash
  - openviking
required-secrets:
  - OPENVIKING_API_KEY
metadata:
  argument-hint: "[--matter-type dd|nda|contract|ma|vcpe] [--target <目标公司>] [--side <买方|卖方|投资方|公司|创始人>]"
  status: "立项访谈 v0.1 — practice profile 初始化 + 后续 skill 兜底入口"
  pacgate-tier-routing:
    interview: "low/local"
    write-profile: "low/local"
    store: "low/local"
  pacgate-domain: "intake"
  pacgate-redline: "结构化访谈不推断 + 缺信息问不编 + 结果写入 practice profile 供后续 skill 复用"
---

# 立项访谈 Skill（百宸，cold-start-interview）

**红线：** 输出为供律师确认的访谈记录，非最终法律意见。结构化访谈不推断——缺信息问、不编。访谈结果写入 practice profile（`.deer-flow/playbooks/<matter-type>-profile.md` 或 OpenViking），作为后续 skill 的工作上下文。

## 一、用途

本 skill 是新事项/新项目的**结构化立项访谈**入口。当 playbook 缺失时，`nda-review`/`contract-review`/`ma-agreement-review`/`vcpe-financing-suite` 等 skill 提示 "cold-start-interview 或临时模式"——本 skill 就是那个 cold-start-interview。

访谈目标：收集后续 skill 需要的关键上下文，写入 practice profile，避免每个 skill 重复问同样的问题。

## 二、硬约束

1. **结构化访谈不推断**——缺信息用选择题问（附默认建议），不编。
2. **访谈结果写入 practice profile**——`.deer-flow/playbooks/<matter-type>-profile.md`（本所专属，存在则覆盖）或 OpenViking `viking://resources/playbooks/<matter-type>-profile`。
3. **不替律师做判断**——访谈只收集事实与偏好，不下法律结论。
4. **后续 skill 复用**——practice profile 写入后，后续 skill 按 3-tier 顺序加载（本所专属 → OpenViking → 基线 references/）。
5. **来源标注**——访谈记录标注受访者、访谈时间。

## 三、访谈框架（按事项类型切换）

### 尽调（dd）
- 目标公司：名称、注册地、行业、规模、是否上市
- 交易类型：股权收购 / 资产收购 / 增资 / 合并
- 买卖方：买方/卖方身份、关联关系
- 重点关注：本所或客户特别关注的领域（如税务、劳动、环保、数据）
- 报告模板：本所 11 章标准（默认）/ 客户定制
- 保留意见口径：本所标准措辞 / 客户要求
- 法域：PRC（默认）/ 涉外（开曼/BVI/HK + PRC）
- 交付时限、交付语言

### NDA 审查（nda）
- 立场：披露方（discloser）/ 接收方（recipient）
- NDA 类型：双向 / 单向
- 保密信息范围：是否含技术、商业、财务
- 保密期限：固定 / 无限期 / 终止后存续
- 特殊条款：是否含竞业/独家/长保密期（触发 RED 级）
- 适用法律、管辖

### 商务合同审查（contract）
- 立场：买方/卖方/出租方/承租方/委托方/受托方
- 合同类型：SaaS/租赁/采购/经销/技术许可/其他
- 标的与金额范围
- 重点条款关注（客户指定）
- 适用法律、管辖

### 并购协议审查（ma）
- 立场：买方/卖方/投资方/公司/创始人
- 协议类型：SPA/增资协议/合并协议
- 交易结构：直接收购 / SPV / VIE / 红筹
- 高风险条款关注：对赌/回购/控制权/反稀释/优先清算
- 适用法律、管辖、语言版本

### VC-PE 投融资（vcpe）
- 立场：投资人/公司/创始人
- 轮次：天使/Pre-A/A/B/C
- 架构：境内人民币（默认）/ VIE/红筹/外币基金
- term sheet 是否已定（是→以 term sheet 为真相源；否→先起草 term sheet）

## 四、工作流

### Step 0 — 确认事项类型　`tier: Low/本地`
确认：dd / nda / contract / ma / vcpe。按 §三 切换访谈框架。

### Step 1 — 结构化访谈　`tier: Low/本地 · data: 客户敏感`
按 §三 框架逐项问。缺信息用选择题问（附默认建议），不抛开放式问题。每项记录：受访者回答 / 默认建议 / 是否确认。

### Step 2 — 写入 practice profile　`tier: Low/本地 · data: 客户敏感`
将访谈结果写入 `.deer-flow/playbooks/<matter-type>-profile.md`（本所专属路径）。结构：
- 事项基本信息（目标公司/交易类型/买卖方/行业/法域/时限/语言）
- 立场与重点关注
- 报告模板与保留意见口径
- 受访者、访谈时间、版本

可选同步存入 OpenViking `viking://resources/playbooks/<matter-type>-profile`（受 OpenViking auth 配置约束，如 403 则仅写本地）。

### Step 3 — 输出
- **访谈记录**：逐项问答 + 默认建议 + 确认状态
- **practice profile 文件**：`.deer-flow/playbooks/<matter-type>-profile.md`
- **待律师确认事项**：集中列出未确认项

## 五、本 skill 不做

- 不替律师下法律判断——访谈只收集事实与偏好。
- 不推断缺失信息——缺就问。
- 不替后续 skill 做分析——只提供上下文。
- 不对外发出——访谈记录供内部使用。
- 每条访谈记录须律师确认后写入 practice profile。