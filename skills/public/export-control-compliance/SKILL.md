---
name: export-control-compliance
description: >-
  出口管制与制裁合规专项（场景7，合规-贸易）。输入企业/交易信息 → 主体和交易筛查（SDN/实体清单/
  军事最终用户）→ 物项/最终用途分析（EAR/两用物项）→ 合同制裁条款起草 → 许可/报告路径 →
  风险处置方案。覆盖美国EAR/BIS、中国出口管制法、欧盟双用途、制裁筛查。
  触发词："出口管制""制裁合规""EAR""BIS""实体清单""SDN""两用物项""export control"。
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
  argument-hint: "[--type 筛查|物项分析|合同条款|许可|风险处置] [--entity <企业>] [--items <物项>]"
  status: "KS-CP-08 出口管制合规 v0.1 — 主体/物项分析 + 合同条款 + 许可路径"
  pacgate-tier-routing:
    screening: "mid/local"
    classification: "main/local"
    contract: "mid/local"
    licensing: "main/local"
  pacgate-domain: "compliance-trade"
  pacgate-redline: "high-risk local-only 不得虚构法规 + 筛查结果须标注来源 + 物项分类须以ECCN/CCL为依据 + 引证须核验"
---

# 出口管制与制裁合规 Skill（百宸 KS-CP-08）

**红线：** 不得虚构法规。筛查结果须标注来源。物项分类须以 ECCN/CCL 为依据。引证须核验。结论先行。

## 工作流程

### 第一步：主体和交易筛查
- SDN 名单筛查（OFAC）
- 实体清单筛查（BIS）
- 军事最终用户/最终用途筛查
- 中国出口管制管控清单
- 筛查结果记录

### 第二步：物项/最终用途分析
- ECCN 分类（EAR）
- CCL 分类（欧盟两用物项）
- 中国两用物项目录
- 最终用户/最终用途证明

### 第三步：合同制裁条款起草
- 制裁合规陈述与保证
- 制裁违规的终止权
- 审计权与合规配合
- 制裁条款与不可抗力的关系

### 第四步：许可/报告路径
- 美国出口许可申请（BIS/OFAC）
- 中国出口许可申请
- 欧盟出口许可申请
- 报告义务

### 第五步：风险处置方案
- 风险分级（高/中/低）
- 缓释措施
- 退出策略（如适用）

## 输出形态

- 出口管制专项法律意见/交易审查报告（docx）
- 主体筛查报告（docx）
- 合同制裁条款草案（docx）
- 许可申请文件清单（docx）

## 来源

- 客户Prompt指南：`合规律师实用Prompts指南.md` §3.1-3.6
- 核心种子：KS-CP-08（出口管制专项法律意见/交易审查报告）
- 项目档案：PN-CP-07（制裁、出口管制或跨境贸易合规项目）