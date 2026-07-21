---
name: fund-exit-liquidation
description: >-
  基金退出与清算法律文件（场景5，基金退出阶段）。输入基金信息、退出方式 → 退出路径分析
  （股权转让/回购/IPO退出/份额转让）→ 审批文件 → 交易文件 → 分配方案 → 税务影响。
  覆盖基金延期、重组、接续基金（GP-led Secondary/Continuation Fund）、清算及注销。
  触发词："基金退出""基金清算""基金注销""接续基金""GP-led""Continuation Fund""份额转让"。
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
  argument-hint: "[--fund <基金名称>] [--type 退出|延期|重组|清算|注销] [--exit-method 转让|回购|IPO] "
  status: "KS-FD-11~15 基金退出 v0.1 — 退出路径 + 延期重组 + 清算注销 + 瀑布 + 跨境"
  pacgate-tier-routing:
    exit-analysis: "main/local"
    restructure: "main/local"
    liquidation: "mid/local"
    cross-border: "main/local"
  pacgate-domain: "fund-exit"
  pacgate-redline: "local-only 不得虚构法规 + 分配方案须以LPA为依据 + 税务分析须标注口径 + 引证须核验"
---

# 基金退出与清算 Skill（百宸 KS-FD-11~15）

**红线：** 不得虚构法规。分配方案须以 LPA 分配瀑布条款为依据。税务分析须标注口径。引证须核验。结论先行。

## 适用场景

1. **基金退出** — 股权转让、回购、IPO 退出
2. **基金延期/重组** — 延期、关键人触发、GP-led Secondary/Continuation Fund
3. **基金清算/注销** — 清算决议、LP 通知、资产处置、分配、协会注销、工商注销
4. **跨境基金** — ODI、外汇、跨境资金路径

## 工作流程

### 退出路径分析
| 退出方式 | 审批要求 | 交易文件 | 分配方案 | 税务影响 |

### 延期及重组
- 延期条件（LPA 延期条款）
- 关键人条款触发
- GP-led Secondary / Continuation Fund 结构
- LP 同意及利益冲突处理

### 清算及注销
- 清算决议
- LP 通知
- 资产处置及分配
- 清算报告
- 协会注销 + 工商注销

### 收益分配瀑布及 Clawback
- 模型逻辑、假设、条款来源
- Clawback 计算

### 跨境投资与外汇合规
- ODI、外汇、跨境资金路径

## 输出形态

- 基金退出路径分析及清算分配方案（docx）
- 基金延期及重组法律备忘录（docx）
- 基金清算及注销核心文件（docx）
- 收益分配瀑布及 Clawback 模型（xlsx/docx）
- 跨境投资与外汇合规路径决策文件（docx）

## 来源

- 客户Prompt指南：`基金律师实用Prompts指南.md` §5.1-5.x, §6.1-6.x
- 核心种子：KS-FD-11（清算注销）、KS-FD-12（分配瀑布及Clawback）、KS-FD-13（延期重组备忘录）、KS-FD-14（退出路径分析）、KS-FD-15（跨境投资合规）
- 项目档案：PN-FD-05（基金退出）、PN-FD-06（延期重组）、PN-FD-07（清算注销）