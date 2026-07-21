---
name: asset-purchase-agreement
description: >-
  资产/业务收购协议起草（APA）（场景2，非诉资产并购）。输入项目信息 → APA核心条款起草
  （资产范围、负债承接、合同和许可转移、人员承接、税费、业务连续安排）→ 交割条件 →
  过渡期安排 → 交割文件。覆盖境内资产收购和业务转让。
  触发词："APA""资产收购""业务转让""资产购买协议""asset purchase""业务收购"。
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
  argument-hint: "[--target <目标资产/业务>] [--buyer <买方>] [--seller <卖方>] [--mode 起草|审阅]"
  status: "KS-NS-17 APA v0.1 — 资产购买/业务转让协议"
  pacgate-tier-routing:
    drafting: "main/local"
    review: "main/local"
    closing: "mid/local"
  pacgate-domain: "transaction-doc"
  pacgate-redline: "local-only 不得虚构事实 + 资产范围须逐一列举 + 人员承接须符合劳动法 + 引证须核验"
---

# 资产/业务收购协议起草 Skill（百宸 KS-NS-17）

**红线：** 不得虚构事实。资产范围须逐一列举。人员承接须符合劳动法。引证须核验。结论先行。

## 工作流程

### 第一步：APA核心条款
- 资产范围界定（逐一列举，含知识产权、合同、存货、设备等）
- 排除资产
- 承接负债
- 交易对价及调整机制

### 第二步：合同和许可转移
- 合同转移清单（需对方同意的合同）
- 知识产权许可转移
- 资质/许可变更

### 第三步：人员承接
- 劳动合同承接（劳动合同法规定）
- 经济补偿责任分配
- 工龄连续计算

### 第四步：税费分配
- 增值税、所得税、印花税
- 转让方/受让方各自承担的税费

### 第五步：交割条件及过渡期
- 交割条件清单
- 过渡期安排（经营维持、重大事项限制）
- 交割文件

## 输出形态

- 资产购买/业务转让协议（docx）
- 资产清单（xlsx/docx）
- 合同转移清单（xlsx/docx）
- 交割文件清单（docx）

## 来源

- 核心种子：KS-NS-17（资产购买/业务转让协议 APA）
- 项目档案：PN-NS-04（境内资产/业务收购项目）