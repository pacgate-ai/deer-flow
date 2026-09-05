---
name: internal-investigation
description: >-
  内部调查及合规整改（场景7，合规）。输入调查授权信息 → 调查授权文件 → 证据保全方案 →
  访谈提纲 → 证据索引 → 调查报告（调查范围、证据、事实认定、责任、整改建议）→ 整改法律意见 →
  关闭验证。覆盖反商业贿赂调查、内部舞弊调查、监管调查应对。
  触发词："内部调查""反舞弊""反贿赂""监管调查""调查报告""合规整改""internal investigation"。
license: Apache-2.0
version: "0.1"
author: PacGate-Law (百宸)
allowed-tools:
  - read_file
  - write_file
  - bash
  - yuandian-law
  - yuandian-case
  - openviking
required-secrets:
  - YUANDIAN_API_KEY
  - OPENVIKING_API_KEY
metadata:
  argument-hint: "[--type 内部调查|监管应对|反贿赂] [--entity <企业>] [--scope <调查范围>]"
  status: "KS-CP-05/06/09/10 调查合规 v0.1 — 合规体系 + 反贿赂 + 调查报告 + 监管回复"
  pacgate-tier-routing:
    investigation: "main/local"
    report: "main/local"
    remediation: "main/local"
    regulatory-response: "main/local"
  pacgate-domain: "compliance-investigation"
  pacgate-redline: "high-risk local-only 不得虚构事实 + 调查范围须有授权依据 + 证据须保全 + 引证须核验"
---

# 内部调查及合规整改 Skill（百宸 KS-CP-05/06/09/10）

**红线：** 不得虚构事实。调查范围须有授权依据。证据须保全。引证须核验。结论先行。

## 工作流程

### 第一步：调查准备
- 调查授权文件（董事会/管理层授权）
- 调查范围界定
- 证据保全方案（电子证据固定、文件封存）
- 访谈提纲

### 第二步：调查执行
- 证据收集与索引
- 访谈记录
- 事实认定

### 第三步：调查报告
- 调查范围及方法
- 证据清单及索引
- 事实认定
- 责任分析
- 整改建议

### 第四步：整改法律意见
- 合规体系评估
- 制度缺陷分析
- 整改方案
- 责任处理建议

### 第五步：监管应对（如适用）
- 应对方案
- 监管回复/申辩
- 证据提交
- 自查整改报告
- 结案文件

## 输出形态

- 调查报告及整改法律意见（docx）
- 合规体系建设方案及风险评估报告（docx）
- 反商业贿赂管理制度（docx）
- 监管问询/调查回复及证据提交文件（docx）

## 来源

- 客户Prompt指南：`合规律师实用Prompts指南.md` §9 合规体系搭建、§10 刑事合规、§11 政府监管与行政程序应对
- 核心种子：KS-CP-05（企业合规体系建设方案）、KS-CP-06（反商业贿赂管理制度）、KS-CP-09（内部调查报告及整改法律意见）、KS-CP-10（监管问询/调查回复）
- 项目档案：PN-CP-03（反商业贿赂）、PN-CP-04（内部调查）、PN-CP-05（行政检查或监管调查应对）