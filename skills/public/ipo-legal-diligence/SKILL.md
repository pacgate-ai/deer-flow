---
name: ipo-legal-diligence
description: >-
  IPO申报及法律尽调（场景2，非诉IPO）。输入项目信息 → IPO法律尽调报告（发行条件、规范整改、
  披露口径）→ 核查计划/清单 → 律师工作报告 → 法律意见书 → 审核问询回复（事实核查、法律分析、
  披露衔接）。覆盖境内A股、境外上市法律尽调。
  触发词："IPO""法律尽调""法律意见书""律师工作报告""问询回复""发行条件""上市尽调"。
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
  argument-hint: "[--target <发行人>] [--board 主板|创业板|科创板|北交所|境外] [--stage 尽调|意见书|问询回复]"
  status: "KS-NS-24~26 IPO法律尽调 v0.1 — 法律意见书 + 工作报告 + 问询回复"
  pacgate-tier-routing:
    diligence: "main/local"
    opinion: "main/local"
    inquiry-reply: "main/local"
  pacgate-domain: "ipo-legal"
  pacgate-redline: "high-risk local-only 不得虚构事实 + 发行条件须逐一核查 + 问询回复须与核查底稿对应 + 引证须核验"
---

# IPO申报及法律尽调 Skill（百宸 KS-NS-24~26）

**红线：** 不得虚构事实。发行条件须逐一核查。问询回复须与核查底稿对应。引证须核验。结论先行。

## 工作流程

### 第一步：法律尽调报告
- 发行人基本情况核查
- 股本及演变核查
- 业务及资质核查
- 主要财产核查
- 关联交易及同业竞争核查
- 诉讼仲裁及行政处罚核查
- 规范运行及整改情况

### 第二步：核查计划/清单
- 核查事项清单
- 核查方法（文件审阅/访谈/检索/函证）
- 核查底稿索引

### 第三步：律师工作报告
- 事实认定
- 法律分析
- 结论意见
- 与法律意见书的对应关系

### 第四步：法律意见书
- 发行条件逐条核查
- 结论意见
- 限制和假设声明

### 第五步：审核问询回复
- 事实核查（与核查底稿对应）
- 法律分析
- 披露衔接

## 输出形态

- IPO法律尽调报告（docx）
- 核查计划/清单（xlsx/docx）
- 律师工作报告（docx）
- 法律意见书（docx）
- 审核问询回复（docx）

## 来源

- 核心种子：KS-NS-24（IPO法律意见书）、KS-NS-25（IPO律师工作报告）、KS-NS-26（IPO审核问询回复）
- 项目档案：PN-NS-08（IPO申报及法律尽调项目）