---
name: ai-product-compliance
description: >-
  AI产品合规专项法律意见（场景7，合规-AI）。输入AI产品信息 → 中国AI产品合规——备案与许可
  路径分析（产品定性、训练数据、输入输出、备案、安全评估、用户规则）→ 欧盟AI Act合规评估 →
  算法合规自评估。覆盖生成式AI、深度合成、大模型服务备案。
  触发词："AI合规""算法备案""生成式AI""深度合成""AI Act""大模型合规""算法自评估"。
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
  argument-hint: "[--product <AI产品>] [--target-market 中国|欧盟|美国|东南亚] [--stage 备案|评估|意见书]"
  status: "KS-CP-07 AI产品合规 v0.1 — 中国备案/许可 + 算法自评估"
  pacgate-tier-routing:
    classification: "main/local"
    filing: "main/local"
    assessment: "main/local"
    opinion: "main/local"
  pacgate-domain: "compliance-ai"
  pacgate-redline: "local-only 不得虚构法规 + 备案要求须以现行规定为准 + 训练数据合规须单独审查 + 引证须核验"
---

# AI产品合规专项法律意见 Skill（百宸 KS-CP-07）

**红线：** 不得虚构法规。备案要求须以检索到的现行规定为准。训练数据合规须单独审查。引证须核验。结论先行。

## 工作流程

### 第一步：产品定性
- AI功能定性（生成式AI/深度合成/推荐算法/其他）
- 服务类型定性（面向公众/面向企业/内嵌产品）
- 适用法规识别

### 第二步：备案与许可路径分析
- 算法备案（互联网信息服务算法推荐管理规定）
- 深度合成备案
- 生成式AI备案/安全评估
- 大模型服务备案
- 训练数据来源合规

### 第三步：安全评估
- 内容安全评估
- 模型安全评估
- 数据安全评估
- 评估报告

### 第四步：用户规则
- 用户协议
- 隐私政策
- 内容审核规则
- 未成年人保护

### 第五步：跨境合规（如适用）
- 欧盟 AI Act 合规评估
- 美国 AI 合规与风险管理

## 输出形态

- 中国AI产品专项法律意见/合规备忘录（docx）
- 算法合规自评估报告（docx）
- 备案文件清单及主文件（docx）

## 来源

- 客户Prompt指南：`合规律师实用Prompts指南.md` §2 AI与大模型合规
- 核心种子：KS-CP-07（中国AI产品专项法律意见/合规备忘录）
- 项目档案：PN-CP-08（行业、Web3/RWA或ESG专项项目 — AI专项）