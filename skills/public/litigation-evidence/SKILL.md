---
name: litigation-evidence
description: >-
  证据组织与分析（场景6，诉讼证据链）。输入已有证据材料 → 编制证据清单（名称/来源/证明目的/
  页码）→ 举证方案（举证责任、证明标准、缺口分析、补证计划）→ 质证意见（真实性/合法性/
  关联性/证明力）→ 证据时间线（事实节点与证据对应 + 待核实事项）。覆盖电子证据审查和
  司法鉴定申请。
  触发词："证据清单""证据目录""举证方案""质证意见""证据时间线""证据组织""电子证据"。
license: Apache-2.0
version: "0.1"
author: PacGate-Law (百宸)
allowed-tools:
  - read_file
  - write_file
  - bash
  - yuandian-case
  - openviking
required-secrets:
  - YUANDIAN_API_KEY
  - OPENVIKING_API_KEY
metadata:
  argument-hint: "[--matter <matter-id>] [--type 证据清单|举证方案|质证意见|时间线] [--party <我方>]"
  status: "KS-LT-03/06/07/08 证据组织 v0.1 — 证据清单 + 举证方案 + 质证 + 时间线"
  pacgate-tier-routing:
    index: "low/local"
    analysis: "mid/local"
    cross-exam: "main/local"
  pacgate-domain: "litigation"
  pacgate-redline: "local-only 不得虚构证据 + 证明力分析须标注依据 + 缺口须明确标注 + 不得编造证据来源"
---

# 证据组织与分析 Skill（百宸 KS-LT-03/06/07/08）

**红线：** 不得虚构证据。证明力分析须标注依据。证据缺口须明确标注"待补证"。不得编造证据来源。结论先行。

## 工作流程

### 证据清单（KS-LT-06）
| 序号 | 证据名称 | 来源 | 证明目的 | 页码 | 原件/复印件 |

### 举证方案（KS-LT-07）
- 举证责任分配分析
- 证明标准（高度盖然性/排除合理怀疑）
- 证据缺口与补证计划
- 举证顺序策略

### 质证意见（KS-LT-08）
- 真实性（原件核对、形成过程）
- 合法性（取证方式、证据形式）
- 关联性（与争议焦点的联系）
- 证明力（证据间的相互印证/矛盾）

### 证据时间线（KS-LT-03）
- 事实节点 → 对应证据 → 待核实事项
- 标注证据缺口和矛盾点

## 输出形态

- 证据清单/证据目录（docx，含提交说明）
- 举证方案及证据证明力分析表（docx）
- 质证意见（docx）
- 案件事实与证据时间线（docx，含可视化图表）

## 来源

- 客户Prompt指南：`诉讼律师实用Prompts指南.md` §3.1-3.4
- 核心种子：KS-LT-03（证据时间线）、KS-LT-06（证据清单）、KS-LT-07（举证方案）、KS-LT-08（质证意见）
- 项目档案：PN-LT-01~10 证据通用