---
name: litigation-case-evaluation
description: >-
  诉讼案件初步评估与策略制定（场景6，诉讼全流程入口）。输入起诉状/合同/往来函件/证据清单 →
  按时间线梳理事实 → 识别核心争议焦点（事实争议 vs 法律争议）→ 请求权基础分析（违约/侵权/
  不当得利/缔约过失竞合选择）→ 管辖分析 → 当事人分析 → 风险评估矩阵（胜诉概率/判决金额/
  执行可行性/时间成本）→ 策略建议。输出案件评估报告（docx），含风险评估矩阵表和时间线图。
  触发词："案件评估""诉讼策略""初步评估""案件分析""诉讼风险评估""请求权基础"。
license: Apache-2.0
version: "0.1"
author: PacGate-Law (百宸)
allowed-tools:
  - read_file
  - write_file
  - bash
  - yuandian-law
  - yuandian-case
  - yuandian-company
  - openviking
required-secrets:
  - YUANDIAN_API_KEY
  - OPENVIKING_API_KEY
metadata:
  argument-hint: "[--matter <matter-id>] [--role 原告|被告|第三人] [--claims <核心诉求>]"
  status: "KS-LT-01/02 诉讼评估策略 v0.1 — 案件评估报告 + 策略备忘录"
  pacgate-tier-routing:
    fact-analysis: "mid/local"
    legal-research: "mid/local"
    strategy-memo: "main/local"
    report: "mid/local"
  pacgate-domain: "litigation"
  pacgate-redline: "local-only 不得虚构事实 + 请求权基础须逐一分析 + 风险评估须标注概率依据 + 结论先行 + 引证须核验"
---

# 诉讼案件评估与策略制定 Skill（百宸 KS-LT-01/02）

**红线：** 不得虚构事实——未提供的材料先输出所需材料清单再继续。所有法规与案例引用须标注名称、文号/条文号、效力状态与检索来源。风险评估须标注概率依据。结论先行。

## 工作流程

### 第一步：事实梳理
- 按时间线整理关键事实
- 识别核心争议焦点（不超过3-5个）
- 标注事实争议 vs. 法律争议
- 缺失材料时先输出所需材料清单

### 第二步：请求权基础分析
- 列出所有可能的请求权基础（违约/侵权/不当得利/缔约过失/无因管理等）
- 各请求权的构成要件逐一分析
- 请求权竞合时的选择策略
- 诉讼时效审查

### 第三步：管辖与程序分析
- 级别管辖 + 地域管辖
- 协议管辖条款有效性审查
- 仲裁 vs. 诉讼主管问题
- 是否需要追加当事人

### 第四步：风险评估矩阵
| 争议焦点 | 胜诉概率 | 判决金额预估 | 执行可行性 | 时间成本 |
|----------|---------|-------------|-----------|---------|

### 第五步：策略建议
- 起诉/应诉总体方向
- 调解/谈判可行性
- 财产保全/证据保全必要性
- 需补充收集的证据清单

## 输出形态

1. **案件评估报告**（docx）——含风险评估矩阵表、时间线图、请求权基础分析表
2. **诉讼策略备忘录**（docx）——含目标、路径、攻防重点、和解区间、阶段计划

## 来源

- 客户Prompt指南：`诉讼律师实用Prompts指南.md` §1.1-1.2
- 核心种子：KS-LT-01（民商事案件初步评估报告）、KS-LT-02（诉讼策略备忘录）
- 项目档案：PN-LT-01~10 通用评估入口