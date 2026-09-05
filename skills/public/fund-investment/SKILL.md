---
name: fund-investment
description: >-
  基金项目投资交易法律支持（场景5，基金投资阶段）。输入投资项目信息 → 投资决策法律支持备忘录
  （投资限制、法律风险、交易条件、投委会建议）→ 立项及投委会核心文件 → 投资限制及利益冲突
  核查表 → 资本缴款通知（Capital Call）→ 分配通知（Distribution Notice）。覆盖基金立场 DD
  和投后管理文件。
  触发词："投资决策""投委会""Capital Call""分配通知""投资限制核查""利益冲突""fund investment"。
license: Apache-2.0
version: "0.1"
author: PacGate-Law (百宸)
allowed-tools:
  - read_file
  - write_file
  - bash
  - yuandian-company
  - qcc-company
  - openviking
required-secrets:
  - YUANDIAN_API_KEY
  - QCC_API_KEY
  - OPENVIKING_API_KEY
metadata:
  argument-hint: "[--fund <基金名称>] [--target <目标公司>] [--round <轮次>] [--amount <金额>]"
  status: "KS-FD-06~10 基金投资 v0.1 — 投资决策 + 投委会 + 限制核查 + 缴款 + 分配"
  pacgate-tier-routing:
    legal-memo: "main/local"
    ic-paper: "mid/local"
    compliance: "mid/local"
    notices: "low/local"
  pacgate-domain: "fund-investment"
  pacgate-redline: "local-only 不得虚构项目信息 + 投资限制须以LPA条款为依据 + 利益冲突须逐一核查 + 引证须核验"
---

# 基金项目投资交易 Skill（百宸 KS-FD-06~10）

**红线：** 不得虚构项目信息。投资限制须以 LPA 条款为依据。利益冲突须逐一核查。引证须核验。结论先行。

## 工作流程

### 投资决策法律支持备忘录
- 投资限制核查（LPA 投资范围、集中度限制）
- 法律风险评估（合规、诉讼、监管）
- 交易条件分析（估值、对赌、保护性条款）
- 投委会建议（同意/附条件/不同意）

### 立项及投委会核心文件
- 投资立项报告
- 投委会决议模板
- 投资条件清单

### 投资限制及利益冲突核查表
| 核查项 | LPA 条款依据 | 当前状态 | 是否合规 |

### 资本缴款通知
- 缴款金额、账户、期限
- 违约条款引用
- 送达确认

### 分配通知
- 分配依据（LPA 分配瀑布）
- 金额、税务、账户
- Clawback 调整

## 输出形态

- 投资决策法律支持备忘录（docx）
- 投委会决议（docx）
- 投资限制及利益冲突核查表（xlsx/docx）
- 资本缴款通知（docx）
- 分配通知（docx）

## 来源

- 客户Prompt指南：`基金律师实用Prompts指南.md` §3.1-3.x
- 核心种子：KS-FD-06（投资决策备忘录）、KS-FD-07（立项及投委会）、KS-FD-08（投资限制核查表）、KS-FD-09（Capital Call）、KS-FD-10（Distribution Notice）
- 项目档案：PN-FD-03（基金项目投资交易）、PN-FD-04（投后管理及基金治理）