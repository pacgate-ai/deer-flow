---
name: litigation-enforcement
description: >-
  财产保全与强制执行（场景6，执行阶段）。输入判决/裁决/财产线索 → 财产保全（保全标的、
  必要性、财产线索、担保安排）→ 强制执行申请（执行依据、请求、履行情况、财产线索）→
  执行异议与复议 → 执行不能应对（终本恢复）。覆盖诉前保全、诉讼保全、执行保全。
  触发词："财产保全""强制执行""执行申请""执行异议""财产线索""终本恢复""preservation"。
license: Apache-2.0
version: "0.1"
author: PacGate-Law (百宸)
allowed-tools:
  - read_file
  - write_file
  - bash
  - yuandian-case
  - qcc-company
  - qcc-risk
  - openviking
required-secrets:
  - YUANDIAN_API_KEY
  - QCC_API_KEY
  - OPENVIKING_API_KEY
metadata:
  argument-hint: "[--type 保全|执行|异议|终本恢复] [--judgment <判决书编号>] [--assets <财产线索>]"
  status: "KS-LT-11/12 保全执行 v0.1 — 保全申请 + 执行申请 + 异议复议"
  pacgate-tier-routing:
    asset-search: "mid/local"
    application: "mid/local"
    objection: "main/local"
  pacgate-domain: "litigation"
  pacgate-redline: "local-only 不得虚构财产线索 + 保全必要性须有事实依据 + 引证须核验 + 结论先行"
---

# 财产保全与强制执行 Skill（百宸 KS-LT-11/12）

**红线：** 不得虚构财产线索。保全必要性须有事实依据。所有法规引用须标注名称、文号/条文号、效力状态与检索来源。结论先行。

## 工作流程

### 财产保全
- 保全标的（银行存款/房产/股权/车辆/应收账款等）
- 保全必要性论证（判决难以执行的风险）
- 财产线索（来源标注、不得虚构）
- 担保安排（保险保函/现金担保/实物担保）

### 强制执行申请
- 执行依据（判决书/裁决书/调解书/支付令）
- 执行请求（本金/利息/迟延履行金/执行费）
- 履行情况说明
- 财产线索清单

### 执行异议与复议
- 执行行为异议
- 案外人执行异议
- 分配方案异议

### 执行不能应对
- 终本裁定后的恢复执行条件
- 财产线索续查（企查查 + 元典 + 法院网查）

## 输出形态

- 财产保全申请书及担保文件（docx）
- 强制执行申请书（docx）
- 执行异议/复议申请书（docx）
- 财产线索调查报告（docx）

## 来源

- 客户Prompt指南：`诉讼律师实用Prompts指南.md` §7.1-7.4
- 核心种子：KS-LT-11（财产保全申请及担保文件）、KS-LT-12（强制执行申请主文件）
- 项目档案：PN-LT-04（财产保全及执行案件）