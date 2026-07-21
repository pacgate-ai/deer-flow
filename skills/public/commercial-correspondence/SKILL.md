---
name: commercial-correspondence
description: >-
  商业函件及争议预防文书起草（场景4，日常通用）。输入事实材料、授权信息 → 催告履约函
  （事实、依据、要求、期限、后果、权利保留、送达）→ 合同解除通知函 → 索赔函 → 澄清函 →
  和解/处置文件。覆盖争议预防全流程函件。
  触发词："催告函""解除通知""索赔函""澄清函""律师函""commercial correspondence""争议预防"。
license: Apache-2.0
version: "0.1"
author: PacGate-Law (百宸)
allowed-tools:
  - read_file
  - write_file
  - bash
  - yuandian-law
  - openviking
required-secrets:
  - YUANDIAN_API_KEY
  - OPENVIKING_API_KEY
metadata:
  argument-hint: "[--type 催告|解除|索赔|澄清] [--recipient <收件方>] [--contract <合同编号>]"
  status: "KS-DG-09 商业函件 v0.1 — 催告/解除/索赔/澄清函"
  pacgate-tier-routing:
    drafting: "mid/local"
    review: "main/local"
  pacgate-domain: "daily-general"
  pacgate-redline: "local-only 不得虚构事实 + 函件须有法律依据 + 期限和后果须明确 + 送达须可证明"
---

# 商业函件及争议预防 Skill（百宸 KS-DG-09）

**红线：** 不得虚构事实。函件须有法律依据。期限和后果须明确。送达须可证明。结论先行。

## 工作流程

### 催告履约函
- 事实概述（合同约定 + 对方违约行为）
- 法律依据（合同条款 + 法规引用）
- 履约要求（具体行为 + 期限）
- 逾期后果（解除合同/索赔/诉讼）
- 权利保留声明
- 送达方式说明

### 合同解除通知函
- 解除权依据（约定解除/法定解除）
- 解除生效时间
- 解除后果（返还/赔偿/清算）
- 送达

### 索赔函
- 损失计算（直接损失/间接损失）
- 索赔金额及依据
- 支付期限和方式
- 不支付后果

### 澄清函
- 争议事项说明
- 我方立场和依据
- 要求对方澄清/确认的事项

## 输出形态

- 催告履约函（docx）
- 合同解除通知函（docx）
- 索赔函（docx）
- 澄清函（docx）
- 送达回证模板（docx）

## 来源

- 客户Prompt指南：`律师日常通用Prompts指南.md` §4 争议预防与商业谈判支持
- 核心种子：KS-DG-09（催告履约函及合同解除通知函）
- 项目档案：PN-DG-05（商业函件及争议预防事项）