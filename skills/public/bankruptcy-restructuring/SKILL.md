---
name: bankruptcy-restructuring
description: >-
  破产重整与清算案件评估（企业破产法/公司法清算程序/跨境破产认可）。输入财务报表/债权清单/
  资产清单/诉讼清单 → 债权债务梳理 → 资产估值 → 重整可行性评估 → 债权人优先级排序 →
  重整方案设计/清算分配方案 → 跨境破产认可与协助评估。输出破产评估报告（docx），
  含债权优先级矩阵和重整可行性分析。触发词："破产""重整""清算""破产管理人""债权申报""
  跨境破产""破产和解""资产变现"。
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
  - qcc-company
  - qcc-risk
required-secrets:
  - YUANDIAN_API_KEY
  - PKULAW_BEARER_TOKEN
  - QCC_API_KEY
metadata:
  argument-hint: "[--matter <matter-id>] [--mode reorganization|liquidation|cross-border] [--role 管理人|债权人|债务人]"
  status: "破产重整评估 v0.1 — 债权优先级 + 重整可行性 + 跨境破产认可"
  pacgate-tier-routing:
    debt-analysis: "mid/local"
    asset-valuation: "mid/local"
    reorganization: "main/local"
    cross-border: "main/local"
  pacgate-domain: "bankruptcy-restructuring"
  pacgate-redline: "local-only 不得虚构事实 + 债权优先级须逐一排序 + 重整可行性须标注概率依据 + 跨境破产须分析认可程序"
---

# 破产重整与清算案件评估 Skill（百宸）

**红线：** 不得虚构事实——未提供的材料先输出所需材料清单再继续。所有法规与案例引用须标注名称、文号/条文号、效力状态与检索来源。债权优先级须逐一排序并标注法律依据。结论先行。

## 工作流程

### 第一步：债权债务梳理
- 债权分类：优先债权（税收/工资/社保）vs 普通债权 vs 有担保债权
- 债权金额核实（本金/利息/违约金分别列明）
- 债权申报期限与审查
- 未到期债权的加速到期评估

### 第二步：资产估值
- 资产清单核查（固定资产/无形资产/应收账款/投资性资产）
- 估值方法选择（市场法/收益法/成本法）
- 资产变现能力评估（流动性/变现周期/变现折扣）
- 关联交易资产的特殊审查

### 第三步：重整可行性评估
- 重整原因审查（《企业破产法》§2）
- 重整价值评估（经营价值 vs 清算价值）
- 重整投资人招募可行性
- 重整计划草案的核心条款设计（债务豁免/股权调整/经营方案）
- 重整成功率概率评估（标注依据）

### 第四步：债权人优先级排序
- 担保债权优先受偿范围
- 职工债权优先受偿范围
- 税款债权优先受偿范围
- 普通债权受偿比例预估
- 后顺位债权（罚款/惩罚性赔偿）的排除

### 第五步：跨境破产认可评估
- 主程序与从程序的识别
- 跨境破产认可的法律依据（《企业破产法》§5/跨境破产协助司法解释）
- 境外破产程序在中国的认可程序
- 中国破产程序在境外的认可障碍
- 资产所在地法律冲突分析

## 输出格式

破产评估报告（docx），包含：
1. 债权债务梳理表
2. 资产估值报告
3. 重整可行性分析报告
4. 债权人优先级矩阵
5. 跨境破产认可评估
6. 风险评估总结与建议