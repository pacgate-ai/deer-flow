---
name: litigation-pleading
description: >-
  起诉状/答辩状/反诉状/仲裁申请书起草（场景6，诉讼文书）。输入案件材料、我方当事人身份、
  核心诉求 → 逐条组织请求权基础 → 起草诉讼请求/仲裁请求 → 事实与理由部分（按时间线 +
  法律依据组织）→ 证据清单附件。覆盖民商事诉讼起诉状、仲裁申请书、答辩状、反诉状。
  触发词："起诉状""答辩状""反诉状""仲裁申请""仲裁答辩""诉讼文书""pleading"。
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
  argument-hint: "[--type 起诉状|答辩状|反诉状|仲裁申请书|仲裁答辩状] [--court <法院>] [--claims <诉求>]"
  status: "KS-LT-04/05 诉讼文书起草 v0.1 — 起诉状/答辩状/仲裁申请书"
  pacgate-tier-routing:
    research: "mid/local"
    draft: "main/local"
    review: "main/local"
  pacgate-domain: "litigation"
  pacgate-redline: "local-only 不得虚构事实 + 请求须有法律依据 + 事实须有证据支撑 + 引证须核验 + 结论先行"
---

# 诉讼文书起草 Skill（百宸 KS-LT-04/05）

**红线：** 不得虚构事实。诉讼请求须有请求权基础，事实须有证据支撑。所有法规引用须标注名称、文号/条文号、效力状态与检索来源。结论先行。

## 适用文书类型

1. **民事起诉状** —— 诉讼请求、事实与理由、证据清单
2. **仲裁申请书** —— 仲裁请求、事实与理由、证据目录
3. **答辩状** —— 答辩请求、事实与理由、抗辩结构
4. **仲裁答辩状** —— 仲裁答辩请求、事实与理由
5. **反诉状** —— 反诉请求、事实与理由

## 工作流程

### 第一步：请求/抗辩基础确认
- 确认请求权基础或抗辩权基础
- 列出构成要件 → 逐一匹配事实
- 确认诉讼/仲裁请求金额计算依据

### 第二步：文书结构起草
- 当事人信息
- 诉讼/仲裁请求（明确、具体、可执行）
- 事实与理由（按时间线 + 法律依据组织）
- 证据清单（证据名称、来源、证明目的、页码）

### 第三步：审查与优化
- 请求与事实的对应关系
- 理由部分的法律论证完整性
- 证据清单的证明力覆盖

## 输出形态

- 起诉状/答辩状/反诉状/仲裁申请书（docx）
- 证据清单附件（docx）

## 来源

- 客户Prompt指南：`诉讼律师实用Prompts指南.md` §2.1-2.4
- 核心种子：KS-LT-04（起诉状/仲裁申请书）、KS-LT-05（答辩状/仲裁答辩状）
- 项目档案：PN-LT-01~10 通用文书