---
name: litigation-trial
description: >-
  庭审准备与代理词（场景6，庭审阶段）。输入案件材料、争点、证据 → 庭审方案（庭审目标、
  争议焦点归纳、举证质证顺序、辩论提纲）→ 发问提纲（对己方证人/对方证人/鉴定人）→
  庭审笔录要点预判 → 庭后代理词（事实论证 + 法律分析 + 请求支持）。覆盖一审/二审/再审。
  触发词："庭审方案""庭审准备""代理词""发问提纲""庭审提纲""庭后代理词""cross-examination"。
license: Apache-2.0
version: "0.1"
author: PacGate-Law (百宸)
allowed-tools:
  - read_file
  - write_file
  - bash
  - yuandian-case
  - yuandian-law
  - openviking
required-secrets:
  - YUANDIAN_API_KEY
  - OPENVIKING_API_KEY
metadata:
  argument-hint: "[--matter <matter-id>] [--stage 一审|二审|再审] [--role 原告|被告]"
  status: "KS-LT-09/10 庭审准备 v0.1 — 庭审方案 + 发问提纲 + 代理词"
  pacgate-tier-routing:
    preparation: "mid/local"
    strategy: "main/local"
    brief: "main/local"
  pacgate-domain: "litigation"
  pacgate-redline: "local-only 不得虚构事实 + 代理词论证须与证据对应 + 引证须核验 + 结论先行"
---

# 庭审准备与代理词 Skill（百宸 KS-LT-09/10）

**红线：** 不得虚构事实。代理词论证须与证据清单对应。所有法规引用须标注名称、文号/条文号、效力状态与检索来源。结论先行。

## 工作流程

### 庭审方案
- 庭审目标（确认诉求/抗辩目标）
- 争议焦点归纳（不超过3-5个）
- 举证质证顺序
- 法庭辩论提纲（第一轮/第二轮）
- 可能的对方抗辩预判及应对

### 发问提纲
- 对己方证人：补充关键事实
- 对对方证人：质疑可信度/暴露矛盾
- 对鉴定人：质疑鉴定方法和结论

### 庭后代理词
- 事实论证（与证据清单对应）
- 法律分析（请求权基础/抗辩权基础）
- 请求支持（明确诉讼/仲裁请求）

## 输出形态

- 庭审方案及发问提纲（docx）
- 庭后代理词（docx）

## 来源

- 客户Prompt指南：`诉讼律师实用Prompts指南.md` §5.1-5.4
- 核心种子：KS-LT-09（庭审方案及发问提纲）、KS-LT-10（民商事代理词）
- 项目档案：PN-LT-01~10 庭审通用