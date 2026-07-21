---
name: fund-establishment
description: >-
  基金设立及募集法律文件起草（场景5，基金全生命周期入口）。输入基金类型/目标规模/投资方向/
  GP团队/LP构成 → 架构设计对比（境内人民币 LP vs 境外开曼 ELP）→ LPA 核心条款 → 认购协议 →
  适当性及风险揭示文件 → 基金备案核心文件 → 募集合规。覆盖私募股权/创投/S基金/对冲基金。
  触发词："基金设立""LPA""认购协议""基金架构""基金募集""AMAC备案""基金备案""fund formation"。
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
  argument-hint: "[--type PE|VC|S基金|对冲|基础设施] [--size <规模>] [--currency RMB|USD] [--gp <GP团队>]"
  status: "KS-FD-01~05 基金设立 v0.1 — 架构 + LPA + 认购 + 适当性 + 备案"
  pacgate-tier-routing:
    structure-design: "main/local"
    lpa-draft: "main/local"
    subscription: "mid/local"
    filing: "mid/local"
  pacgate-domain: "fund-establishment"
  pacgate-redline: "local-only 不得虚构法规 + 备案要求须以检索到的现行规定为准 + 税务分析须标注口径 + 引证须核验"
---

# 基金设立及募集 Skill（百宸 KS-FD-01~05）

**红线：** 不得虚构法规。备案要求须以检索到的现行规定为准。税务分析须标注口径。引证须核验。结论先行。

## 适用范围

覆盖基金全生命周期的设立阶段：
- 架构设计（境内人民币 LP vs 境外开曼 ELP/SPC）
- LPA 核心条款（GP/LP 权利义务、分配瀑布、关键人条款、LPAC）
- 认购协议/认购申请书
- 投资者适当性及风险揭示文件
- 新基金备案核心文件（AMAC）

## 工作流程

### 第一步：架构设计对比
| 维度 | 境内人民币基金 | 境外美元基金 |
|------|--------------|-------------|
| 法律形式 | 有限合伙（合伙企业法） | 开曼 ELP / SPC |
| GP/管理人 | 分离/合一利弊 | 开曼 GP + 管理公司 |
| 税务 | LP 所得税、创投优惠 | 开曼零税 + 预提税路径 |
| 监管 | AMAC 备案 | CIMA 登记 / SFC 牌照 |
| 外汇 | 人民币便利 | QDII/QDLP/QFLP/ODI |

### 第二步：LPA 核心条款起草
- 期限与延展
- 认缴与实缴
- 分配瀑布（Waterfall）
- Clawback
- 关键人条款
- LPAC 权限
- 利益冲突
- 转让与退伙

### 第三步：认购与适当性
- 认购协议
- 合格投资者核查
- 风险揭示书
- KYC/AML

### 第四步：备案
- AMAC 备案主文件
- 托管/监督协议

## 输出形态

- 基金架构设计备忘录（docx）
- LPA 草案（docx）
- 认购协议草案（docx）
- 风险揭示书（docx）
- 备案文件清单及主文件（docx）

## 来源

- 客户Prompt指南：`基金律师实用Prompts指南.md` §1.1-1.x
- 核心种子：KS-FD-01（基金架构设计备忘录）、KS-FD-02（LPA）、KS-FD-03（认购协议）、KS-FD-04（适当性及风险揭示）、KS-FD-05（备案核心文件）
- 项目档案：PN-FD-01（基金设立及募集项目）