---
name: hf-ultrawork
description: Use when architect explicitly opts into fast lane via 'auto mode' / 'ultrawork' / 'do not stop' keywords or features/<f>/README.md Metadata `Execution Mode: auto`. Not the default mode; not a review/gate skip mechanism. NEVER skip Fagan review verdicts, gate verdicts, approval-artifact disk writes, closeout pack completeness, or Hard Gates 'stop on unclear standard' clauses (see Hard Gates section for the 5 enumerated non-compressibles per ADR-009 D2).
---

# HF Ultrawork

架构师 explicit opt-in 的 fast lane skill。识别 fast lane 关键词 / Metadata 后接管"节点之间的是否继续"决策权，自动走 router canonical next action，自动写 approval 工件（reviewer verdict 通过时），不打断架构师。

**绝不**绕过 Fagan author/reviewer 分离 + 硬门禁 verdict（见 Hard Gates 5 类不可压缩项）。markdown-only 路径下本 skill 是**宣告式**（declarative），依赖 host agent 自觉读取本 SKILL.md + 工件；v0.7 `harnessflow-runtime` 落地后才有 idle 检测 hook 增强。

## When to Use

适用：
- 架构师在会话中说 fast lane 关键词（`auto mode` / `ultrawork` / `ulw` / `自动执行` / `不要停下来` / `不用确认` / `自动跑完` / `keep going` / `proceed` / `continue`）
- `features/<f>/README.md` Metadata 段写 `Execution Mode: auto`
- 进入新 feature 时 `using-hf-workflow` 步骤 5 entry bias 表 direct invoke 本 skill

不适用：
- 默认（standard mode）行为 → 不调用本 skill；router 直接选下一节点并停下确认
- 已经在某个 review/gate 节点内 → 完成该节点后再回本 skill 决策
- 架构师说显式停下关键词（`停` / `暂停` / `wait` / `hold on` / `等等` / `stop` / `pause`） → 立即让出
- 架构师说 `standard mode` / `恢复 standard` / `回到 standard` / `revert to standard` → 关闭 fast lane
- v0.6 之前的 features（无 ADR-009 治理） → 按 standard mode

## Hard Gates

下列 **5 类不可压缩项** 在 fast lane 中**绝对不能跳过 / 不能简化 / 不能用引用 ADR 替代**（按 ADR-009 D2 enumerate；本 SKILL.md 必须 enumerate 而非仅引 ADR，按 skill-anatomy.md 第 3 条"SKILL.md 是本地 contract"）：

| # | 不可压缩项 | 原因 |
|---|---|---|
| 1 | **8 个 Fagan review 节点的 verdict**：`hf-discovery-review` / `hf-spec-review` / `hf-design-review` / `hf-ui-review` / `hf-tasks-review` / `hf-test-review` / `hf-code-review` / `hf-traceability-review` | author ≠ reviewer 是工程纪律的根；fast lane 不能让作者自审或跳过任一 review verdict |
| 2 | **3 个 gate verdict**：`hf-regression-gate` / `hf-doc-freshness-gate` / `hf-completion-gate` | gate 是"证据是否足以推进"的独立判断；fast lane 不能绕过任一 gate verdict |
| 3 | **`hf-finalize` 的 closeout pack 完整性**（含 closeout HTML companion 由 ADR-005 引入） | PMBOK-style handoff，不减项；fast lane 不能简化 closeout pack |
| 4 | **spec / design / tasks 的 approval 工件落盘**（即便 fast lane auto-APPROVED） | approval 自动化 ≠ approval 工件可省；ADR-009 D2 明文："approval 工件本身**必须**写入磁盘" |
| 5 | **任何 SKILL.md `Hard Gates` 段命中"方向 / 取舍 / 标准不清必须停下抛回用户"** | `docs/principles/soul.md` 第 1 条硬纪律；fast lane 不豁免 standard 不清时的抛回义务 |

其它 Hard Gates：
- 不写 verdict / approval / gate verdict（本 skill 只把 reviewer 的 verdict 落到 approval 工件，不替代 reviewer 的判断本身）
- 不修改任何 review record / spec / design / tasks artifact（仅追加 approval + audit trail）
- escape conditions 命中任一项 → **立即让出抛回架构师**（详见 `references/fast-lane-escape-conditions.md` 的 6 条）

## Object Contract

- **Primary Object**: 节点之间的"是否继续"自动决策权 + `progress.md` `## Fast Lane Decisions` audit trail
- **Frontend Input Object**: 架构师 explicit opt-in 信号（关键词 / Metadata） + 当前节点的 verdict / output
- **Backend Output Object**:
  1. 自动 dispatch 下一节点（按 router canonical next action）
  2. 各 approval 工件落盘（spec / design / tasks approval；reviewer verdict 通过时）
  3. `progress.md` `## Fast Lane Decisions` 段每次自动决策 +1 行 audit trail
- **Object Boundaries**:
  - 不写 review record / verdict / gate verdict
  - 不修改 spec / design / tasks artifact
  - 不替代 reviewer / gate 的判断
  - 不在 standard mode 默认启用
- **Object Invariants**:
  - 5 类不可压缩项任一被绕 → 立即停下并标记 violation
  - escape 条件命中 → 让出（不能"先走完再说"）
  - audit trail 每条决策 + 1 行（绝不批量补写）

## Methodology

| 方法 | 落地步骤 |
|---|---|
| **Architect-Explicit Opt-in** | Workflow 步骤 1：识别 explicit 信号；缺则不启用 |
| **Decision-Point Interception** | Workflow 步骤 2：在节点之间的"是否继续"判断点接管，但不替代 router 的节点选择权威 |
| **Verdict-Then-Escape Check** | Workflow 步骤 3：每次 reviewer / gate verdict 后**先**检查 escape 条件再决定是否继续 |
| **Approval Artifact Persistence** | Workflow 步骤 4：reviewer verdict 通过 → 自动写 approval 工件落盘（按 ADR-009 D2 不可省） |
| **Append-Only Audit Trail** | Workflow 步骤 5：每个自动决策 +1 行到 `progress.md` `## Fast Lane Decisions` |

详细 escape 条件：`references/fast-lane-escape-conditions.md`。

## Workflow

1. **检测 explicit opt-in**
   - Object: 架构师信号
   - Method: 关键词 grep（见 fast lane 关键词集合）+ feature README Metadata 字段读取
   - Input: 当前会话 + feature 路径
   - Output: 是否启用 fast lane（boolean）
   - Stop / continue: 启用 → 进步骤 2；未启用 → 退出，让 standard router 接管

2. **在 router canonical next action 后接管"是否继续"决策**
   - Object: 节点之间的过渡确认
   - Method: 监听 router 输出的 next action；若属于 review / gate / approval 类节点 → 直接 dispatch；不停下询问
   - Input: router handoff
   - Output: 自动 dispatch 下一节点
   - Stop / continue: router 选定有效 next action → 进步骤 3；否则退出

3. **verdict 后先检查 escape 条件，再决定是否继续**
   - Object: 上一节点的 verdict / output
   - Method: 按 `references/fast-lane-escape-conditions.md` 6 条逐项检查；命中任一即让出
   - Input: 上一节点 verdict / record
   - Output: 继续 fast lane 或 escape
   - Stop / continue: 0 命中 → 进步骤 4；≥ 1 命中 → escape 抛回架构师

4. **reviewer verdict 通过时，自动写 approval 工件落盘**
   - Object: spec-approval / design-approval / tasks-approval record
   - Method: 写 `features/<f>/approvals/<stage>-approval-YYYY-MM-DD.md`，含 Decision: APPROVED + Approver: cursor cloud agent (auto mode) + Rationale 引用 reviewer record + ADR-009 D4 audit trail 行
   - Input: reviewer verdict 通过的 record
   - Output: approval 工件落盘
   - Stop / continue: 工件落盘成功 → 进步骤 5；失败 → escape

5. **追加 audit trail 行到 progress.md**
   - Object: `progress.md` `## Fast Lane Decisions` 段
   - Method: 按 ADR-009 D4 schema 追加一行（time / node / decision_type / decision_content / trigger_condition / escape_enabled）
   - Input: 步骤 2-4 的决策记录
   - Output: progress.md 更新
   - Stop / continue: 一条决策一条 audit row；进入下一循环（回步骤 2）

## Output Contract

| 工件 | 路径 | 触发时机 |
|---|---|---|
| approval 工件 | `features/<f>/approvals/<stage>-approval-<date>.md` | 每次 reviewer verdict 通过时 |
| audit trail 行 | `features/<f>/progress.md` `## Fast Lane Decisions` 段 | 每次自动决策 |

不写：review record / verdict / gate verdict / spec / design / tasks artifact 的内容。

## fast lane 关键词集合（OQ-003 收口）

| 类别 | 关键词 |
|---|---|
| 显式启用 | `auto mode` / `ultrawork` / `ulw` / `自动执行` / `不要停下来` / `不用确认` / `自动跑完` / `auto run` / `keep going` / `proceed` / `continue` |
| 显式停下 | `停` / `暂停` / `wait` / `hold on` / `等等` / `stop` / `pause` / `先停` |
| 显式恢复 standard | `standard mode` / `恢复 standard` / `回到 standard` / `revert to standard` |

## Red Flags

- 自动写 review verdict（违反 Object Boundaries + Hard Gates 第 1 类）
- 跳过 approval 工件落盘（违反 Hard Gates 第 4 类）
- 检测到 escape 条件却"先走完再让出"（违反 Object Invariants）
- 把 v0.6 之前的 features 也按 fast lane 处理（违反 When to Use 边界）
- 默认启用 fast lane（违反 Methodology "Architect-Explicit Opt-in"）

## Common Mistakes

| 错误 | 问题 | 修复 |
|---|---|---|
| approval 工件压缩到一句"已 auto-approve" | 违反 ADR-009 D2 工件落盘要求 | 按 features/001 / features/002 既有 approval 模板写完整 |
| audit trail 批量补写 | 失去逐次可冷读性 | 每个决策即时追加 1 行 |
| escape 条件检查只查 verdict 字段 | 漏 problems.md / Hard Gates 类条件 | 按 6 条全跑（见 references） |

## Common Rationalizations

| 借口 | 反驳 / Hard rule |
|---|---|
| "review verdict 通过了，approval 工件不写也行，反正 review record 已经有了。" | Hard Gates 第 4 类（不可压缩 #4）+ ADR-009 D2: approval 工件**必须**落盘；review record + approval 工件是 2 类不同 audit 链 |
| "escape 条件 5（rewrite loop 第 4 次）跟我现在没关系，跳过。" | Hard Gates: 6 条 escape 必须每个 verdict 后全检；漏检 = 违反 fast lane 边界 |
| "架构师明确说了 ultrawork，意思就是连 review 也不用做了吧。" | Hard Gates 第 1 / 第 2 类（不可压缩 #1 #2）+ ADR-009 D2: ultrawork 仅压缩"中间确认"，**不**替代 Fagan review 与 gate verdict |
| "audit trail 太啰嗦，会话末尾一并补就行。" | Object Invariants: append-only + 即时追加；批量补 = 失去 fresh evidence 性质 |

## Reference Guide

| 文件 | 用途 |
|---|---|
| `references/fast-lane-escape-conditions.md` | 6 条 escape 条件详细 + 检查 protocol + 命中后行为 |

## Verification

- [ ] explicit opt-in 信号已识别（关键词或 Metadata）
- [ ] 5 类不可压缩项无被绕的痕迹（review verdict / gate verdict / closeout pack / approval 工件落盘 / 方向标准不清抛回）
- [ ] 每个 verdict 后 6 条 escape 都已检查
- [ ] reviewer verdict 通过时，approval 工件已落盘
- [ ] 每个自动决策已追加 1 行 audit trail 到 progress.md
- [ ] 未写任何 review verdict / gate verdict
