---
name: vie-redchip-restructuring
description: >-
  红筹/VIE架构重组方案设计（场景2，非诉跨境重组）。输入项目信息 → 架构设计方案及架构图
  （境外架构、持股路径、返程投资、外汇、税务及上市节点）→ 境内重组及返程投资核心文件
  → VIE核心协议（独家业务合作/独家购买权/股权质押/表决权委托）→ VIE配套文件（配偶同意函/
  关键决议/质押登记）→ 37号文登记材料 → 境外上市备案及数据合规核查清单。
  触发词："VIE""红筹""协议控制""37号文""返程投资""境外上市备案""WFOE""red-chip"。
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
  argument-hint: "[--matter <matter-id>] [--target <目标公司>] [--listing-target <上市地>] [--mode 设计|文件起草]"
  status: "KS-NS-18~23 VIE红筹重组 v0.1 — 架构 + 核心文件 + VIE协议 + 配套 + 37号文 + 上市备案"
  pacgate-tier-routing:
    structure-design: "main/local"
    core-docs: "main/local"
    vie-agreements: "main/local"
    registration: "mid/local"
    listing-filing: "main/local"
  pacgate-domain: "vie-redchip"
  pacgate-redline: "high-risk local-only 不得虚构法规 + 37号文口径须以现行规定为准 + 数据合规须单独评估 + 引证须核验"
---

# 红筹/VIE架构重组 Skill（百宸 KS-NS-18~23）

**红线：** 不得虚构法规。37号文口径须以检索到的现行规定为准。数据合规须单独评估。引证须核验。结论先行。

## 工作流程

### 第一步：架构设计方案
- 境外架构（开曼/BVI + 香港公司 + WFOE + VIE公司）
- 持股路径图
- 返程投资路径
- 外汇路径（37号文/ODI）
- 税务影响
- 上市节点规划

### 第二步：境内重组及返程投资核心文件
- 股权重组文件（增资/股权转让）
- 内部批准文件（股东会/董事会决议）

### 第三步：VIE核心协议（4份）
1. 独家业务合作协议
2. 独家购买权协议
3. 股权质押协议
4. 表决权委托/授权书

### 第四步：VIE配套文件
- 配偶同意函
- 关键股东会/董事会决议
- 质押登记文件

### 第五步：37号文登记
- 登记材料清单
- 办理流程和时间

### 第六步：境外上市备案及数据合规
- 境外上市备案核查清单
- 网络安全审查评估
- 数据出境关键判断

## 输出形态

- 架构设计方案及架构图（docx）
- 境内重组及返程投资核心文件（docx）
- VIE核心协议 ×4（docx）
- VIE配套文件（docx）
- 37号文登记材料及办理清单（docx）
- 境外上市备案及数据合规核查清单（docx）

## 来源

- 核心种子：KS-NS-18（架构设计）、KS-NS-19（境内重组核心文件）、KS-NS-20（VIE核心协议×4）、KS-NS-21（VIE配套文件）、KS-NS-22（37号文登记）、KS-NS-23（境外上市备案及数据合规）
- 项目档案：PN-NS-07（VIE/红筹重组项目）