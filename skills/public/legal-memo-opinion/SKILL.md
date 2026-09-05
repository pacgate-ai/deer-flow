---
name: legal-memo-opinion
description: >-
  法律备忘录与专项法律意见起草（场景4，日常通用非交易咨询）。输入事实材料、研究过程 →
  法律备忘录（结论先行、事实假设、法律依据、分析、风险、建议）→ 日常咨询书面答复 →
  专项法律意见书（委托、资料依据、分析、结论、限制、签章）。覆盖非交易咨询完整交付。
  触发词："法律备忘录""legal memo""法律意见""专项意见""咨询答复""legal opinion"。
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
  argument-hint: "[--type 备忘录|咨询答复|法律意见书] [--matter <事项>] [--client <客户>]"
  status: "KS-DG-02/03/04 法律备忘录与意见 v0.1 — memo + 咨询答复 + 专项法律意见书"
  pacgate-tier-routing:
    research: "mid/local"
    analysis: "main/local"
    opinion: "main/local"
  pacgate-domain: "daily-general"
  pacgate-redline: "local-only 不得虚构事实 + 结论先行 + 法规引用须标注名称文号效力来源 + 限制和假设须明确声明"
---

# 法律备忘录与专项法律意见 Skill（百宸 KS-DG-02/03/04）

**红线：** 不得虚构事实。结论先行。法规引用须标注名称、文号/条文号、效力状态与检索来源。限制和假设须明确声明。

## 工作流程

### 法律备忘录（Legal Memo）
结构：
1. **结论摘要**（先给一段结论，再展开分析）
2. **事实与假设**
3. **法律依据**（法规 + 案例，逐一标注来源）
4. **分析**（构成要件 → 事实匹配 → 风险评估）
5. **建议**
6. **限制声明**

### 日常咨询书面答复
- 结论先行
- 简洁可操作的行动建议
- 必要的法律依据

### 专项法律意见书（通用盖章版）
结构：
1. 委托事项
2. 资料依据
3. 法律分析
4. 结论意见
5. 限制和假设
6. 签章

## 输出形态

- 法律备忘录（docx）
- 日常咨询书面答复（docx）
- 专项法律意见书（docx，含签章页）

## 来源

- 客户Prompt指南：`律师日常通用Prompts指南.md` §1 合同起草与日常审阅、§5 知识产权、§6 税务
- 核心种子：KS-DG-02（法律备忘录）、KS-DG-03（日常咨询书面答复）、KS-DG-04（专项法律意见书）
- 项目档案：PN-DG-04（法律备忘录或专项法律意见事项）