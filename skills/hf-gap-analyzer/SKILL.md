---
name: hf-gap-analyzer
description: Use when an authoring artifact (spec / design / tasks) draft is complete and the author wants to surface implicit assumptions, AI slop, missing acceptance criteria, or unaddressed edge cases BEFORE submitting to the corresponding Fagan review. Not a review node (does not produce verdict); not a substitute for `hf-spec-review` / `hf-design-review` / `hf-tasks-review`; not for code review (use `hf-code-review`).
---

# HF Gap Analyzer

作者侧自查工具：在 spec / design / tasks 草稿提交对应 Fagan review 之前，由 *作者本人* 调用本 skill 抓"作者脑里有但纸上没有"的 6 类 gap：Implicit Intent / AI Slop / Missing Acceptance / Unaddressed Edge Cases / Scope Creep / Dangling Reference。

**本 skill 不是 Fagan review 节点**：不写 verdict、不写"通过 / 需修改 / 阻塞"等结论性判断。输出是 `<artifact>.gap-notes.md`，作者**自己**吸收 / 驳回每条 finding，再提交对应 review。

## When to Use

适用：
- 写完 spec / design / tasks 草稿，提交对应 review *之前*，作者主动 self-check
- 作者想在不消耗 reviewer 周期的情况下消灭低级遗漏
- 同一 artifact 多次返工时，自检本轮新增 gap

不适用：
- 给出 review verdict → `hf-spec-review` / `hf-design-review` / `hf-tasks-review`（本 skill 不替代任何 review）
- 评审代码 → `hf-code-review`
- 阶段不清 / 证据冲突 → `hf-workflow-router`
- 已经在 review 节点内 → 继续当前 review skill

## Hard Gates

- **不写 verdict**：本 skill 输出仅是 finding 列表，不写"通过 / 需修改 / 阻塞"或等价结论
- **不修改被分析的 artifact**：finding 提示作者，作者自己改原 artifact
- 不替代独立 Fagan review；gap-notes 通过不等于 review 通过
- 作者吸收 / 驳回必须**显式标记**每条 finding（`accepted` / `rejected-with-reason`），再提交 review；reviewer 会读 gap-notes 作为辅助上下文（不强制作为 verdict 依据）

## Object Contract

- **Primary Object**: `<artifact-path>.gap-notes.md`（与 artifact 平级，如 `features/<f>/spec.md.gap-notes.md`）
- **Frontend Input Object**: 作者刚写完的草稿 + 项目 spec 约定 + ADR 列表 + 邻接 artifact（spec 草稿时读 product-discovery output；design 草稿时读 spec；tasks 草稿时读 design）
- **Backend Output Object**:
  1. gap-notes 文件（含 6 维度 rubric 命中的 finding 列表）
  2. 作者吸收后的 status 标注（accepted / rejected）
- **Object Boundaries**:
  - 不写 review verdict
  - 不修改被分析的 artifact
  - 不替代仓库级 ADR（架构性发现仍需走 ADR）
- **Object Invariants**:
  - 每条 finding 带 anchor（具体行号或段落引用）+ rubric 维度标签 + suggested treat
  - 作者吸收状态全部标完后才能提交对应 review

## Methodology

| 方法 | 落地步骤 |
|---|---|
| **Author-side Self-Check (pre-Fagan)** | 整个 Workflow 在作者侧执行，与 Fagan reviewer 解耦 |
| **6-Dimension Gap Rubric** | Workflow 步骤 2：按 `references/gap-rubric.md` 6 维扫描 |
| **Anchored Findings** | Object Invariants：每条 finding 必带 anchor |
| **Explicit Absorption Markers** | Hard Gates：作者必须标 accepted / rejected-with-reason |

详细 rubric：`references/gap-rubric.md`。

## Workflow

1. **读取 artifact + 邻接上下文**
   - Object: 待分析 artifact + 上游 spec / design / ADR 列表
   - Method: file read + grep 已知 ADR ID
   - Input: artifact 路径
   - Output: 内存中的对照清单
   - Stop / continue: 上游 ADR 引用解析失败 → 直接报"Dangling Reference"finding 到 gap-notes 后继续

2. **按 6 维度 rubric 扫描**
   - Object: artifact 内容
   - Method: 按 `references/gap-rubric.md` 的 6 维 rubric 逐项扫描（Implicit Intent / AI Slop / Missing Acceptance / Unaddressed Edge Cases / Scope Creep / Dangling Reference）
   - Input: artifact 文本
   - Output: finding 列表（含 anchor + 维度 + suggested treat）
   - Stop / continue: ≥ 1 finding → 进步骤 3；0 finding → 仍写 gap-notes（标"无 finding"）让 reviewer 知道做过自查

3. **写 `<artifact-path>.gap-notes.md`**
   - Object: gap-notes 文件
   - Method: 按模板（在 references/gap-rubric.md 末尾）填写
   - Input: 步骤 2 finding 列表
   - Output: gap-notes.md 落盘
   - Stop / continue: 文件落盘 → 进步骤 4

4. **作者吸收 / 驳回**
   - Object: 每条 finding 的 status 字段
   - Method: 作者读 finding，决定 accepted（修原 artifact）/ rejected-with-reason（不修，写理由）
   - Input: gap-notes 全列表
   - Output: 每条 finding 的 status 标注
   - Stop / continue: 全部 status 标完 → 提交对应 review；否则不提交

## Output Contract

| 工件 | 路径 | 状态 |
|---|---|---|
| gap-notes 文件 | `<artifact-path>.gap-notes.md` | 作者吸收完后保留作为 review 辅助上下文（不删） |

无 verdict 工件、无 approval 工件、不写 progress.md（作者侧 self-check 不算 workflow stage transition）。

## Red Flags

- 把 finding 当 verdict 用（违反 Hard Gates 第 1 条）
- 跳过作者吸收 status 标注就提交 review（违反 Hard Gates 第 4 条）
- 在 gap-notes 里写"我建议改为 X"然后**自己**改了 artifact（违反 Hard Gates 第 2 条；fix 应由作者主导，本 skill 只提示）
- 只跑 1-2 个维度就停（违反 Methodology"6 维 rubric"）

## Common Mistakes

| 错误 | 问题 | 修复 |
|---|---|---|
| gap-notes 用作 review 替代品 | reviewer 不再独立扫，依赖 self-check | 严守 Object Boundaries"不替代 Fagan review"，gap-notes 仅辅助 |
| finding 没有 anchor | reviewer / 作者无法定位 | Object Invariants"每条 finding 必带 anchor" |
| AI Slop 维度只扫词不看 prose 风格 | 漏检中文 prose 中的 AI 痕迹 | rubric 含中英文双语模式（详见 references） |

## Common Rationalizations

| 借口 | 反驳 / Hard rule |
|---|---|
| "我自己写的，应该没什么 gap，跳过 self-check 直接提 review。" | Hard Gates: 不强制使用本 skill，但若使用则 6 维必须全跑；作者跳过 self-check 是合法选择，但 review 阶段会因低级遗漏而打回 |
| "我顺手按 finding 改了原 artifact，没必要标 accepted。" | Hard Gates: 必须显式标 status；review 节点会读 gap-notes 来对比"作者声称 accept 了哪些"，无 status 标注会被 reviewer 视为未吸收 |
| "rejected-with-reason 太麻烦，我就写 'no'。" | Hard Gates: rejected 必须含 reason，否则 reviewer 无法判断驳回理由是否合理 |
| "gap-notes 找出 verdict 等价词，本 skill 已变相在评审。" | Hard Gates 第 1 条 + Object Boundaries: gap-notes 是 finding 列表，措辞不能用"通过 / 不通过 / fail"；用 finding severity（critical / important / minor）标程度而非 verdict 等价词 |

## Reference Guide

| 文件 | 用途 |
|---|---|
| `references/gap-rubric.md` | 6 维度 rubric 详细 + finding 模板 + 中英文双语 AI slop 模式 |

## Verification

- [ ] gap-notes 文件已落盘
- [ ] 6 维度 rubric 全跑过（不论是否命中）
- [ ] 每条 finding 含 anchor + 维度 + suggested treat
- [ ] 作者已为每条 finding 标 accepted / rejected-with-reason
- [ ] 未写任何 verdict 等价物
- [ ] 未自行修改原 artifact
