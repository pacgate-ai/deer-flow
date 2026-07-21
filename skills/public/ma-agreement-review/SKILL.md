---
name: ma-agreement-review
description: >-
  并购协议审查（场景7，单文档主笔制，高风险）。按本所 Playbook 红线逐条审查 SPA/Share Purchase
  Agreement/增资协议、出 redline → 引证核验 → 二次复核。**高风险：强制主办律师加签 → 合伙人签发。**
  涉对赌/回购/控制权/反稀释/优先清算等高风险条款，复杂推理强制走 Main（本地或境内云）。
  触发词："并购协议审查""SPA审查""增资协议审查""对赌条款""回购权""反稀释""优先清算"。
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
  argument-hint: "[--mode review|redline] [--side buyer|seller|investor|company|founder] [--agreement-type spa|capital-increase|merger]"
  status: "单文档主笔 v0.1 — 场景7 并购协议审查（高风险，强制主办律师加签）"
  pacgate-tier-routing:
    review: "main/local-or-inland-cloud"
    high-risk-clauses: "main/local"
    redline: "main/local"
    cite-verify: "low/local"
    cross-check: "main/local"
  pacgate-domain: "transaction-doc"
  pacgate-redline: "高风险强制主办律师加签 + 单文档主笔制 + Playbook红线逐条 + 高风险条款专项决策程序 + redline交付 + 来源分级 + P0即时上报"
---

# 并购协议审查 Skill（百宸，场景7）

**红线：** 输出为供律师复核的草稿，非最终法律意见。**高风险：强制主办律师加签 → 合伙人签发。** 涉对赌/回购/控制权/反稀释/优先清算等高风险条款，复杂推理强制走 Main（本地或境内云），低置信强制升级，高风险无论置信都强制律师复核。

## 一、单文档主笔制（高风险变体）

同 `nda-review`/`contract-review` 单文档主笔制，差异：
- **高风险强制主办律师加签**（回填件 §2.1 场景7）——并购协议除主笔承办律师外，强制主办律师复核加签后方可交合伙人签发。
- **复杂推理强制 Main tier**——对赌/回购/控制权/反稀释/优先清算等条款，模型走 Main（本地或境内云）。
- **P0 即时上报**——前置审批未过、控制权瑕疵、重大权属问题、大额隐性负债即时报合伙人。

## 二、硬约束

1. **单文档主笔制**——不用 swarm。
2. **高风险强制主办律师加签**——非签发前不可对外。
3. **复杂推理强制 Main tier**——高风险条款不走 Mid/Low。
4. **Playbook 红线逐条**——按本所并购协议 Playbook 红线逐条审查。
5. **高风险条款专项决策程序**——见 §四，不得一行带过。
6. **三态标注**。
7. **来源分级必标**。
8. **检索稀薄即停**。
9. **redline 交付**——Word 修订模式，逐条可接受/拒绝。
10. **中国法强制点 delta**——对赌可履行性、回购资本维持、领售对小股东效力等，标注 playbook 偏好 vs 中国法限制。
11. **强制免责声明**+"供律师复核草稿"水印。

## 三、工作流

### Step 0 — 加载 Playbook + 确认立场 + 协议类型　`tier: Low/本地 · data: 客户敏感`
加载顺序：`.deer-flow/playbooks/ma-playbook.md`（本所专属，存在则覆盖）→ OpenViking `find "并购协议 playbook"` → 缺失则提示 `cold-start-interview`。
确认：立场（买方/卖方/投资方/公司/创始人）+ 协议类型（SPA/增资协议/合并协议）。

### Step 1 — 形式审查 + 齐套性　`tier: Low/本地 · data: 客户敏感`
形式审查（同 `contract-review` Step 1）+ 齐套性检查（SPA/SHA/章程修正案/补充协议是否齐备，参见 `vcpe-financing-suite`）。

### Step 2 — 实质性条款逐条审查 + redline　`tier: Main/本地 · data: 客户敏感`
按 Playbook 红线逐条审查，对每条偏离产出标准块 + officecli 出 Word redline。并购协议核心条款审查清单：
- 估值与对价
- 交割条件（CP）
- 陈述与保证（R&W）+ 赔偿上限/存续期
- 对赌/业绩承诺（VAM）
- 优先清算权
- 反稀释（full ratchet / weighted average）
- 优先购买权/共售权（tag-along）
- 领售权（drag-along）
- 回购权
- 董事会席位与保护性条款（一票否决权）
- 信息权与检查权
- 知识产权归属
- 竞业/服务期
- 交割后事项
- 争议解决

### Step 3 — 高风险条款专项决策程序　`tier: Main/本地 · data: 客户敏感`
高风险条款不得一行带过，按专项决策程序展开：

- **对赌**：标的公司 vs 股东；现金补偿 vs 股权补偿；触发条件与上限；可履行性（《九民纪要》与公司对赌 vs 与股东对赌的效力差异）。
- **回购权**：触发条件、回购方、利率/溢价、可执行性（资本维持约束）。
- **优先清算权**：参与 vs 不参与 vs 附上限参与；倍数；叠加顺序（seniority）。
- **反稀释**：完全棘轮 vs 加权平均（广义/狭义）；pay-to-play 例外；逐字引用公式。
- **领售权**：触发门槛（持股%/轮次同意）、对创始人/小股东强制范围、保护性下限。
- **董事会与保护性条款**：席位分配、否决事项清单范围（过宽=拖累运营）。

### Step 4 — 中国法强制点 delta　`tier: Main/本地 · data: 去标识化+公开法源`
逐项核查 Playbook 偏好是否撞中国法（结合 A4 检索）：对赌可履行性、回购利润分配限制、领售对小股东效力、防稀释工商登记可行性、外资准入、ODI/37号文、经营者集中。冲突标记：`"playbook 偏好[X]，中国法下[X]受[限制/override]。[法源核验]"`。

### Step 5 — 引证核验（A5）　`tier: Low/本地 · data: 公开法源`
对每条法律依据核验现行有效性 + 来源分级。

### Step 6 — 二次复核（A6）　`tier: Main/本地 · data: 客户敏感`
红线遗漏检查 + 条款冲突检查 + **套内一致性检查**（与 SHA/章程/补充协议的数字/定义/权利一致性，参见 `vcpe-financing-suite` Step 2）。

### Step 7 — 输出　`tier: Mid/本地 · data: 客户敏感`
- **并购协议 redline docx**（Word 修订模式）
- **审查备忘录**：逐条表 + 高风险条款专项决策展开 + 中国法强制点 delta
- **强制主办律师加签标记** + P0 即时上报清单
- **待律师确认事项**（选择题，附默认建议）

## 四、本 skill 不做

- 不替主笔律师定稿——redline 出，律师逐条接受/拒绝。
- 不替主办律师加签——强制人工关卡。
- 不替合伙人签发。
- 不并行起草（单文档主笔制）。
- 不跳过 A5/A6。
- 不自行降级 P0——前置审批/控制权瑕疵/大额隐性负债统一 P0 即时上报。
- 不无声填补。
- 每条都是线索非结论，正式用前须律师核验 + 主办律师加签 + 合伙人签发。