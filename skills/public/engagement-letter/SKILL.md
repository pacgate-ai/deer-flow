---
name: engagement-letter
description: >-
  法律服务委托合同起草（场景4，日常通用）。输入服务范围、客户信息 → 非诉专项法律服务委托合同
  （服务范围、交付、依赖、时间、收费、责任边界、终止条款）→ 常年法律顾问合同 → 风险代理协议。
  覆盖律师执业管理的委托关系建立文件。
  触发词："委托合同""法律服务合同""聘书""常年法律顾问""engagement letter""retainer"。
license: Apache-2.0
version: "0.1"
author: PacGate-Law (百宸)
allowed-tools:
  - read_file
  - write_file
  - bash
  - yuandian-law
required-secrets:
  - YUANDIAN_API_KEY
metadata:
  argument-hint: "[--type 专项|常顾|风险代理] [--client <客户>] [--scope <服务范围>] [--fee <收费模式>]"
  status: "KS-DG-08 委托合同 v0.1 — 非诉专项委托合同 + 常顾合同"
  pacgate-tier-routing:
    drafting: "mid/local"
    review: "mid/local"
  pacgate-domain: "daily-general"
  pacgate-redline: "local-only 服务范围须明确 + 责任边界须界定 + 收费条款须清晰 + 引证须核验"
---

# 法律服务委托合同 Skill（百宸 KS-DG-08）

**红线：** 服务范围须明确。责任边界须界定。收费条款须清晰。引证须核验。结论先行。

## 工作流程

### 非诉专项法律服务委托合同
1. 委托事项及服务范围
2. 交付物清单
3. 律师依赖事项（客户提供材料、配合事项）
4. 时间安排
5. 收费条款（固定/计时/上限/垫付）
6. 责任边界（免责条款、赔偿上限）
7. 终止条款
8. 保密条款
9. 利益冲突声明

### 常年法律顾问合同
1. 服务内容（日常咨询、合同审阅、法律风险提示等）
2. 服务期限
3. 常顾费及额外收费
4. 服务响应时效
5. 终止条件

## 输出形态

- 非诉专项法律服务委托合同（docx）
- 常年法律顾问合同（docx）

## 来源

- 核心种子：KS-DG-08（非诉专项法律服务委托合同）
- 项目档案：PN-DG-01（常年法律顾问精选事项集）