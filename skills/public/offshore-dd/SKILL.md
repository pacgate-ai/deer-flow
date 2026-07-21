---
name: offshore-dd
description: >-
  离岸尽调报告（场景4，尽调线变体）。流程同场景1 中国法律尽调报告，另加：离岸法域（开曼/
  BVI/香港）审查要点按法域切换；登记信息经注册代理/当地律所调档归集后录入（非系统抓取）；
  离岸法源结论降一档标注、强制当地律师复核。触发词："离岸尽调""开曼尽调""BVI尽调"
  "香港尽调""offshore due diligence"。
license: Apache-2.0
version: "0.1"
author: PacGate-Law (百宸)
allowed-tools:
  - read_file
  - write_file
  - bash
  - officecli
  - pkulaw
  - yuandian-law
  - yuandian-case
  - qcc-company
  - openviking
required-secrets:
  - YUANDIAN_API_KEY
  - PKULAW_BEARER_TOKEN
  - QCC_API_KEY
  - OPENVIKING_API_KEY
metadata:
  argument-hint: "[--matter <matter-id>] [--jurisdiction Cayman|BVI|HK|multi] [--mode extract|grade|assemble]"
  status: "A3+A8 离岸尽调 v0.1 — 场景4 尽调线变体，离岸法源降一档+强制当地律师复核"
  pacgate-tier-routing:
    extract: "mid/local"
    grade: "main/local"
    offshore-source: "mid/local-gate"
    assemble: "mid/local"
  pacgate-domain: "offshore-dd"
  pacgate-redline: "离岸法源降一档标注 + 强制当地律师复核 + 登记信息经注册代理调档非系统抓取 + 来源分级 + P0即时上报"
---

# 离岸尽调报告 Skill（百宸，场景4）

**红线：** 输出为供律师复核的草稿，非最终法律意见。离岸法源结论降一档标注（权威核验→辅助库比对→内部模板→模型推断 各降一档）、强制当地律师复核。登记信息经注册代理/当地律所调档归集后录入，非系统抓取。

## 一、与场景1 中国法律尽调的关系

本 skill 是场景1 `dd-report-assembly` 的**离岸变体**，流程相同，差异如下：

| 维度 | 场景1（境内） | 场景4（离岸） |
|---|---|---|
| 法域 | PRC | Cayman / BVI / HK（按法域切换） |
| 登记信息 | 企查查等系统抓取 | **经注册代理/当地律所调档归集后录入**（非系统抓取） |
| 法源标注 | 正常来源分级 | **降一档标注**（权威核验→辅助库比对等） |
| 复核 | 承办律师 + 合伙人 | **强制当地律师复核**（额外关卡） |
| 审查要点 | 11章 PRC 体系 | 按法域切换（见 §二） |

其余硬约束（单域负责制、三态标注、来源分级、检索稀薄即停、P0即时上报、五道硬关卡、只装配不创作、强制免责声明）同 `dd-report-assembly` skill，不在此重复。

## 二、按法域切换的审查要点

### 开曼（Cayman）
- 公司设立与良好存续（Good Standing Certificate）
- 董事登记（Register of Directors，需注册代理调档）
- 股东登记（Register of Members，非公开，需注册代理调档）
- 章程（Memorandum & Articles of Association）
- 年度报告与年费
- 经济实质（Economic Substance）合规
- 反洗钱（AML/KYC）合规

### BVI
- 公司设立与良好存续（Certificate of Good Standing）
- 董事登记（Register of Directors，需注册代理调档）
- 股东登记（Register of Members，非公开，需注册代理调档）
- 章程（Memorandum & Articles of Association）
- 年度申报与年费
- 经济实质（Economic Substance）合规
- 反洗钱（AML/KYC）合规

### 香港（HK）
- 公司注册处查册（Companies Registry，可系统抓取）
- 董事/股东登记（可系统抓取）
- 章程（Articles of Association）
- 年度申报（Annual Return）
- 商业登记证（Business Registration Certificate）
- 税务合规（IRD）
- 重要控制人登记（SCR - Significant Controllers Register）

## 三、工作流（差异点）

### Step 0 — 法域前置　`tier: Low/本地 · data: 客户敏感`
确认法域（Cayman / BVI / HK / 多法域）。涉外前置：标注适用法、管辖、语言版本，提示外资准入/国安审查/ODI/37号文/经营者集中等强制点。

### Step 1 — 登记信息归集　`tier: Mid/本地 · data: 客户敏感`
**经注册代理/当地律所调档归集后录入**（Cayman/BVI 非公开登记信息），非系统抓取。HK 可系统抓取（Companies Registry）。

### Step 2 — 实体分析　`tier: Main/本地 · data: 客户敏感`
按 §二 审查要点逐项分析，三态标注 + 定级建议（P0–P3）。**离岸法源结论降一档标注**（如本应"权威核验"的，降为"辅助库比对"）。

### Step 3 — 法源核验　`tier: Mid/本地 · data: 公开法源·查询须脱敏`
离岸法源（开曼公司法、BVI BCA、香港公司条例等）调用 pkulaw/yuandian-law（如有离岸库）+ 当地律所出具的法律意见作为权威来源。**强制当地律师复核**作为额外关卡。

### Step 4 — 装配　`tier: Mid/本地 · data: 客户敏感`
同 `dd-report-assembly`，按本所报告模板装配，额外在每条离岸 finding 标注：
- 法域
- 法源降一档标注
- "强制当地律师复核"标记
- 登记信息来源（注册代理调档/当地律所/系统抓取）

### Step 5 — 输出
- 离岸尽调报告 docx 草稿（11章或按法域调整 + 离岸标注 + 强制当地律师复核标记）
- 装配说明 + 审计痕迹

## 四、本 skill 不做

- 同 `dd-report-assembly`：不创作、不替律师下定级、不跳过 A5/A6、不分发、不签署。
- 不替当地律师出具离岸法域结论——强制当地律师复核。
- 不系统抓取 Cayman/BVI 非公开登记信息——经注册代理调档。
- 每条都是线索非结论，正式用前须律师核验 + 当地律师复核。