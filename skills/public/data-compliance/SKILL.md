---
name: data-compliance
description: >-
  数据合规与个人信息保护专项（场景7，合规）。输入企业信息 → 数据跨境传输评估（路径判断、
  适用条件、材料、实施建议）→ 个人信息保护影响评估 PIA → 隐私政策/个人信息保护政策审阅 →
  数据处理协议 DPA 起草。覆盖 PIPL、数据出境、算法合规自评估。
  触发词："数据合规""个人信息保护""数据出境""PIA""隐私政策""DPA""数据跨境""data compliance"。
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
  argument-hint: "[--type 出境评估|PIA|隐私政策|DPA|算法自评估] [--entity <企业>] [--data-type <数据类型>]"
  status: "KS-CP-01~04 数据合规 v0.1 — 出境分析 + PIA + 隐私政策 + DPA"
  pacgate-tier-routing:
    assessment: "main/local"
    pia: "main/local"
    policy: "mid/local"
    dpa: "mid/local"
  pacgate-domain: "compliance-data"
  pacgate-redline: "local-only 不得虚构法规 + 出境路径须以现行规定为准 + PIA须覆盖必要性评估 + 引证须核验"
---

# 数据合规与个人信息保护 Skill（百宸 KS-CP-01~04）

**红线：** 不得虚构法规。出境路径须以检索到的现行规定为准。PIA 须覆盖必要性评估。引证须核验。结论先行。

## 工作流程

### 数据跨境传输评估
- 路径判断（标准合同/安全评估/认证）
- 适用条件分析
- 申报/备案材料
- 实施建议

### 个人信息保护影响评估（PIA）
- 处理活动描述
- 处理目的及必要性
- 对个人权益的影响
- 风险评估
- 保护措施

### 隐私政策/个人信息保护政策
- 信息收集与使用
- 共享、转让、公开披露
- 用户权利（查阅、更正、删除、撤回同意）
- 安全措施
- 未成年人保护
- 跨境传输声明

### 数据处理协议（DPA）
- 角色（控制者/处理者）
- 处理指令
- 分包处理
- 安全措施
- 跨境传输
- 数据泄露通知
- 审计权

## 输出形态

- 数据/个人信息出境法律分析备忘录（docx）
- PIA 报告（docx）
- 隐私政策/个人信息保护政策（docx）
- 数据处理协议 DPA（docx）

## 来源

- 客户Prompt指南：`合规律师实用Prompts指南.md` §1.1-1.6
- 核心种子：KS-CP-01（出境法律分析）、KS-CP-02（PIA报告）、KS-CP-03（隐私政策）、KS-CP-04（DPA）
- 项目档案：PN-CP-01（数据合规及个人信息保护项目）