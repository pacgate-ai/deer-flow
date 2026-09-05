---
name: arbitration
description: >-
  仲裁案件评估与程序管理（CIETAC/HKIAC/SIAC/ICC 仲裁规则）。输入仲裁条款/合同/证据清单 →
  仲裁条款效力审查 → 管辖权分析 → 仲裁请求构建 → 程序策略（仲裁庭组成、证据开示、
  临时措施）→ 裁决可执行性评估。输出仲裁策略备忘录（docx）。触发词："仲裁""CIETAC""
  HKIAC""SIAC""ICC仲裁""仲裁条款""仲裁程序""临时措施""裁决执行"。
license: Apache-2.0
version: "0.1"
author: PacGate-Law (百宸)
allowed-tools:
  - read_file
  - write_file
  - bash
  - pkulaw
  - yuandian-law
  - yuandian-case
required-secrets:
  - YUANDIAN_API_KEY
  - PKULAW_BEARER_TOKEN
metadata:
  argument-hint: "[--matter <matter-id>] [--institution CIETAC|HKIAC|SIAC|ICC] [--role 申请人|被申请人]"
  status: "仲裁评估策略 v0.1 — 仲裁条款审查 + 管辖 + 程序策略 + 裁决可执行性"
  pacgate-tier-routing:
    clause-review: "mid/local"
    jurisdiction: "main/local"
    procedure: "mid/local"
    enforceability: "main/local"
  pacgate-domain: "arbitration"
  pacgate-redline: "local-only 不得虚构事实 + 仲裁条款效力须逐一审查 + 管辖权异议须评估成功率 + 裁决可执行性须标注执行地法律依据"
---

# 仲裁案件评估与程序管理 Skill（百宸）

**红线：** 不得虚构事实——未提供的材料先输出所需材料清单再继续。所有法规、仲裁规则与案例引用须标注名称、文号/条文号、效力状态与检索来源。仲裁条款效力审查须逐一分析要件。结论先行。

## 工作流程

### 第一步：仲裁条款效力审查
- 逐一审查仲裁条款要件：仲裁机构、仲裁地、仲裁规则、仲裁语言、仲裁员人数
- 识别无效/可撤销风险（《仲裁法》§16/17/18）
- 分析示范条款 vs 非示范条款的差异
- 缺失条款时标注【待确认】

### 第二步：管辖权分析
- 仲裁条款 vs 法院管辖条款的竞合分析
- 仲裁机构管辖权范围审查
- 多方仲裁条款的扩展效力
- 异议期限评估

### 第三步：仲裁请求构建
- 请求权基础与仲裁请求的对应关系
- 仲裁请求的金额计算依据
- 反请求的可能性评估
- 利息/律师费/仲裁费的分担请求

### 第四步：程序策略
- 仲裁庭组成方式（独任 vs 合议）
- 仲裁员人选策略（首席 vs 当事人指定）
- 证据开示范围与策略
- 临时措施申请（财产保全/证据保全）
- 程序时间线规划

### 第五步：裁决可执行性评估
- 裁决撤销风险（《纽约公约》/《仲裁法》§70/71）
- 执行地法律对仲裁裁决的承认与执行程序
- 公共政策例外风险评估
- 裁决执行可行性矩阵

## 输出格式

仲裁策略备忘录（docx），包含：
1. 仲裁条款效力审查清单
2. 管辖权分析报告
3. 仲裁请求构建表
4. 程序策略建议
5. 裁决可执行性评估矩阵
6. 风险评估总结