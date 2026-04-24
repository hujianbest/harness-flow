# `hf-doc-freshness-gate` 任务计划

- 状态: 草稿
- 主题: 把 design.md §11 / §18 中的 7 个候选原子任务 (T1..T7) 转化为可执行 INVEST 任务，含 DAG / Acceptance / Verify / 完成条件
- Workflow Profile: standard
- Execution Mode: auto
- 上游已批准设计: `features/001-hf-doc-freshness-gate/design.md` (design-approval-2026-04-23.md)
- 上游已批准规格: `features/001-hf-doc-freshness-gate/spec.md` (spec-approval-2026-04-23.md)

## 1. 概述

本计划把 design §18 列出的 7 个候选原子任务（T1..T7）正式 INVEST 化，构成可执行队列。所有任务均为**纯 Markdown 文件创建 / 修改 + 一次手动 dogfooding dry run**，与 HF 既有 30+ skill 的实现形态一致；不引入运行时代码、依赖、工具链。

整体队列设计：所有 7 个任务在一次 hf-test-driven-dev session 内完成（属同一 feature 的 dogfooding 闭环），无需多 session；router 只在 T1 → T7 之间逐个推进 `Current Active Task`，每个任务完成后由 `hf-test-review` / `hf-code-review` / `hf-traceability-review` / `hf-regression-gate` / `hf-doc-freshness-gate` (如适用) / `hf-completion-gate` 处理（按 standard profile 完整 Quality 链）。

## 2. 里程碑

| 里程碑 | 包含任务 | 退出标准 | 对应规格 / 设计依据 |
|---|---|---|---|
| **M1: skill 本体落地** | T1, T2, T3 | `skills/hf-doc-freshness-gate/{SKILL.md, references/, templates/}` 全部创建并通过单 task 评审链 | spec FR-001..FR-008, NFR-001..NFR-004, CON-001..CON-007；design §11 模块职责表 |
| **M2: evals + router 集成** | T4, T5 | evals 5 个 scenario 落地；router transition map 含 5 条 logical canonical transition | spec FR-005, FR-007, FR-008；design §13 reviewer-return JSON, ADR-0003 |
| **M3: completion-gate 集成** | T6 | hf-completion-gate SKILL.md evidence bundle 段新增 doc-freshness verdict reference (prose-only) | spec FR-005；design §11 boundary constraints |
| **M4: dogfooding walking skeleton** | T7 | T-NFR-002 + T-NFR-003 + T-NFR-004 三个 manual dry run 在本 feature 自身上跑通；HYP-004 final closure | spec NFR-002, NFR-003, NFR-004；design §16 Walking Skeleton, §10.3 lightweight checklist |

## 3. 文件 / 工件影响图

| 任务 | 创建 | 修改 | 不动 |
|---|---|---|---|
| T1 | `skills/hf-doc-freshness-gate/SKILL.md` | — | 既有 30+ skill |
| T2 | `skills/hf-doc-freshness-gate/references/{responsibility-matrix.md, profile-rubric.md, reviewer-dispatch-handoff.md}` | — | — |
| T3 | `skills/hf-doc-freshness-gate/templates/{verdict-record-template.md, lightweight-checklist-template.md}` | — | — |
| T4 | `skills/hf-doc-freshness-gate/evals/test-prompts.json` | — | — |
| T5 | — | `skills/hf-workflow-router/references/profile-node-and-transition-map.md`（按 ADR-0003 加 5 条 logical canonical transition） | router SKILL.md 主文件、其他 references |
| T6 | — | `skills/hf-completion-gate/SKILL.md`（evidence bundle 段新增 1 段 prose） | hf-completion-gate 既有 verdict 逻辑 |
| T7 | `features/001-hf-doc-freshness-gate/evidence/dry-run-T-NFR-002-lightweight-time.md` + `dry-run-T-NFR-003-no-tools.md` + `dry-run-T-NFR-004-sync-on-presence.md`（dogfooding 实跑记录） | `features/001-hf-doc-freshness-gate/progress.md`（HYP-004 final closure 状态） | 任何其他 skill / 文档 |

## 4. 需求与设计追溯

| 任务 | spec FR/NFR/CON 锚点 | design 章节锚点 | ADR 锚点 |
|---|---|---|---|
| T1 (SKILL.md) | FR-001..FR-008, NFR-001..NFR-004, CON-001..CON-007 | §11 模块表 + §13 契约表 | ADR-0002 |
| T2 (references) | FR-003, FR-004, FR-008 | §11 references 行 | ADR-0002 |
| T3 (templates) | FR-002, FR-004 | §11 templates 行 + §10.3 lightweight 草样 | ADR-0002 |
| T4 (evals) | FR-001..FR-007 全部 | §16 测试用例 T-FR-001-pass / T-FR-001-blocked / T-FR-003-N/A / T-FR-005-partial / T-FR-007-blocked-increment | ADR-0002 |
| T5 (router transition) | FR-005, FR-007 | §10.2 C4 Container + ADR-0003 | ADR-0003 |
| T6 (completion-gate ref) | FR-005, FR-006 | §11 Boundary Constraints + completion-gate evidence bundle 消费规则 | ADR-0002 |
| T7 (dogfooding dry run) | NFR-002, NFR-003, NFR-004, HYP-004 | §16 Walking Skeleton + §10.3 | ADR-0002 + ADR-0003 |

## 5. 任务拆解

### T1. 创建 `skills/hf-doc-freshness-gate/SKILL.md`

- 目标: 创建本 skill 的权威 prose contract（YAML frontmatter + Methodology + When to Use + Hard Gates + Workflow + Output Contract + Reference Guide + Red Flags + Verification）
- Acceptance:
  - Given `skills/hf-doc-freshness-gate/SKILL.md` 不存在；When 本任务完成；Then 文件已创建，含 frontmatter `name` + `description`（≤ 1024 字符），所有标准 SKILL.md 段落齐全（参照 `docs/principles/skill-anatomy.md`）
  - Given SKILL.md 已创建；When `hf-test-review` reviewer 冷读；Then verdict 列表覆盖 spec §8 全部 8 条 FR
  - Given SKILL.md 已创建；When `hf-code-review` reviewer 冷读；Then 不含运行时代码 / 不引入新依赖（NFR-003 + CON-002）
- 依赖: 无（M1 起点）
- Ready When: design-approval-2026-04-23.md 已落盘 ✅
- 初始队列状态: ready
- Selection Priority: P1（M1 入口）
- Files / 触碰工件: 创建 `skills/hf-doc-freshness-gate/SKILL.md`
- 测试设计种子（test list）:
  - 主行为：reviewer subagent 冷读 SKILL.md，能在不打开其他文件的前提下知道"本 gate 何时激活、产出什么 verdict、写到哪里"
  - 关键边界：YAML frontmatter `description` 不超 1024 字符（HF 既有约束）
  - fail-first：验证不存在 SKILL.md 时，"reviewer 找不到 skill" — 在 RED 阶段刻意以缺文件状态跑一次冷读
- Verify: `grep -c "^## " skills/hf-doc-freshness-gate/SKILL.md` ≥ 8（所有标准段齐全）；`wc -c < <(awk '/^---$/{f=!f;next}f' skills/hf-doc-freshness-gate/SKILL.md | head -10)` ≤ 1024
- 预期证据: `features/001-hf-doc-freshness-gate/evidence/T1-skill-md-created.log`（含 file size + section grep 结果）
- 完成条件: 文件存在 + 8 段齐全 + frontmatter 合规 + `hf-test-review` + `hf-code-review` + `hf-traceability-review` 三链通过

### T2. 创建 `skills/hf-doc-freshness-gate/references/`

- 目标: 创建 3 个 reference 文件：(1) `responsibility-matrix.md`（spec §6.2 责任矩阵的权威 cold-link）；(2) `profile-rubric.md`（lightweight / standard / full 三档强制维度判定细则 + 判定优先级）；(3) `reviewer-dispatch-handoff.md`（复用既有 review-dispatch-protocol 的本 gate 适配点）
- Acceptance:
  - Given 3 个 references 已创建；When SKILL.md `Reference Guide` 段引用它们；Then 引用路径与文件实际位置一致（无 broken link）
  - Given `responsibility-matrix.md`；When reviewer 冷读；Then 能复述 spec §6.2 责任矩阵 14 行 × 5 列（无信息丢失）
  - Given `profile-rubric.md`；When reviewer 按 lightweight 模式判定；Then 仅 row 1 + Conventional Commits 自检为强制（FR-004 + design §10.3）
  - Given `reviewer-dispatch-handoff.md`；When reviewer 派发时；Then 能找到与既有 `hf-workflow-router/references/review-dispatch-protocol.md` 一致的 readonly 约定
- 依赖: T1（SKILL.md 中的 Reference Guide 段需先确定引用结构）
- Ready When: T1 = done
- 初始队列状态: pending
- Selection Priority: P2
- Files / 触碰工件: 创建 `skills/hf-doc-freshness-gate/references/{responsibility-matrix.md, profile-rubric.md, reviewer-dispatch-handoff.md}`
- 测试设计种子:
  - 主行为：reviewer 按 profile-rubric 三档分别判定一次同一输入，verdict 强制维度数随 profile 升高而严格单增
  - 关键边界：profile=lightweight 时，强制维度数 = 2（row 1 + Commits 自检）
  - fail-first：故意把 standard 强制维度漏一项，确认 review 能发现
- Verify: 3 个文件存在；SKILL.md 中 Reference Guide 表的路径列与 ls 输出一致
- 预期证据: `features/001-hf-doc-freshness-gate/evidence/T2-references-created.log`
- 完成条件: 3 文件存在 + 与 SKILL.md 引用一致 + 三链通过

### T3. 创建 `skills/hf-doc-freshness-gate/templates/`

- 目标: 创建 2 个模板：(1) `verdict-record-template.md`（`features/<active>/verification/doc-freshness-YYYY-MM-DD.md` 模板，含 metadata header / 判定明细表 / reviewer-return JSON）；(2) `lightweight-checklist-template.md`（design §10.3 的 5 行 checklist 模板）
- Acceptance:
  - Given verdict-record-template.md；When reviewer 按模板填写；Then 产出文件符合 design §13 输出契约表（verdict 词表 ∈ `{pass, partial, N/A, blocked}`、含 dimension breakdown 表、含 reviewer-return JSON）
  - Given lightweight-checklist-template.md；When reviewer 按模板跑 lightweight；Then verdict 文件 ≤ 30 行（满足 NFR-002）
- 依赖: T2（templates 引用 references 中的 profile-rubric / responsibility-matrix）
- Ready When: T2 = done
- 初始队列状态: pending
- Selection Priority: P3
- Files / 触碰工件: 创建 `skills/hf-doc-freshness-gate/templates/{verdict-record-template.md, lightweight-checklist-template.md}`
- 测试设计种子:
  - 主行为：填一份 verdict-record 模板（手动），verify 5 行 lightweight-checklist 模板填完后整文件 ≤ 30 行
  - 关键边界：verdict 词表如果 reviewer 写了第 5 个值（非 pass/partial/N/A/blocked），模板应能让其立即看出 schema violation
  - fail-first：故意填一个超出词表的 verdict，verify reviewer 能发现
- Verify: 2 个文件存在；按 lightweight checklist 填一次，wc -l 输出 ≤ 30
- 预期证据: `features/001-hf-doc-freshness-gate/evidence/T3-templates-created.log`
- 完成条件: 2 文件存在 + lightweight 实测 ≤ 30 行 + 三链通过

### T4. 创建 `skills/hf-doc-freshness-gate/evals/test-prompts.json`

- 目标: 创建 5 个 pressure scenario JSON（按 design §11 evals 行 + §16 测试策略表）：(a) FR-001-pass / (b) FR-001-blocked-traceability / (c) FR-003-N/A / (d) FR-005-partial / (e) FR-007-blocked-increment
- Acceptance:
  - Given 5 scenario JSON 已创建；When 父会话按 evals dispatch 派发；Then 5 个 verdict 路径全部覆盖（pass / partial / N/A / blocked → tdd / blocked → increment / blocked → traceability）
  - Given test-prompts.json；When `hf-test-review` reviewer 冷读；Then 5 个 scenario 与 spec §8 FR 一一对应（无遗漏，无 overshoot）
- 依赖: T1, T2, T3（scenario 需要 reference templates / SKILL contract）
- Ready When: T3 = done
- 初始队列状态: pending
- Selection Priority: P4
- Files / 触碰工件: 创建 `skills/hf-doc-freshness-gate/evals/test-prompts.json`
- 测试设计种子:
  - 主行为：5 scenario 各自跑一次（不强求实际派发，但 prompt 须自洽）
  - 关键边界：JSON schema 合法（与既有 30+ skill 的 evals.json / test-prompts.json 形态一致）
  - fail-first：故意让一个 scenario 期望与 spec FR 不对应，verify reviewer 能发现
- Verify: `python3 -c "import json; json.load(open('skills/hf-doc-freshness-gate/evals/test-prompts.json'))"` 退出 0；5 scenario 数 = `jq length`
- 预期证据: `features/001-hf-doc-freshness-gate/evidence/T4-evals-created.log`
- 完成条件: JSON 合法 + 5 scenario + 三链通过

### T5. 修改 `skills/hf-workflow-router/references/profile-node-and-transition-map.md`

- 目标: 按 ADR-0003 加入 logical canonical 5 条 transition（per-profile 行展开 = 5 × 3 = 15 行），把 `hf-doc-freshness-gate` 节点引入三 profile 主链与迁移表
- Acceptance:
  - Given router transition map 修改后；When 父会话按 router 协议解析下一节点（regression-gate=通过）；Then 唯一下一推荐节点 = `hf-doc-freshness-gate`
  - Given doc-freshness-gate verdict = `pass` / `partial` / `N/A`；When router 按表解析；Then next = `hf-completion-gate`
  - Given doc-freshness-gate verdict = `blocked`；When router 按表解析；Then next = `hf-test-driven-dev`
  - Given doc-freshness-gate verdict = `blocked(workflow)` 且 reroute_via_router=true；When router 按表解析；Then next = `hf-workflow-router` 自身
  - Given full / standard / lightweight 三 profile 主链节点列表；When 修改后；Then 三个列表均含 `hf-doc-freshness-gate`
- 依赖: T1, T2, T3, T4（router 引用 skill 本体；本体未到位时 transition 无意义）
- Ready When: T4 = done
- 初始队列状态: pending
- Selection Priority: P5（M2 关键路径）
- Files / 触碰工件: 修改 `skills/hf-workflow-router/references/profile-node-and-transition-map.md`（约 5 处插入）
- 测试设计种子:
  - 主行为：跑 5 个 verdict 路径，verify router 能稳定路由
  - 关键边界：full profile 主链节点列表 + 三迁移表 + canonical route map text 段（"hf-test-review -> hf-code-review -> hf-traceability-review -> hf-regression-gate -> hf-doc-freshness-gate -> hf-completion-gate"）三处都同步修改
  - fail-first：故意只改一张迁移表不改 canonical route map text，verify reviewer 能发现
- Verify:
  - 总出现次数（按 5 logical × 3 profile 迁移表 = 15 + 3 主链节点列表行 + 4 条 canonical route map chain 各 1 行 = 22）：
    ```bash
    test "$(grep -c "hf-doc-freshness-gate" skills/hf-workflow-router/references/profile-node-and-transition-map.md)" -ge 22 || echo "GREP COUNT < 22"
    ```
  - 三 profile 主链节点列表分别含本节点（逐 anchor 检查）：
    ```bash
    for p in "full profile 主链推荐节点" "standard profile 主链推荐节点" "lightweight profile 主链推荐节点"; do
      awk "/$p/,/^### /" skills/hf-workflow-router/references/profile-node-and-transition-map.md | grep -F "hf-doc-freshness-gate" > /dev/null || echo "MISSING IN: $p"
    done
    ```
  - canonical route map 4 条 chain 文本段全部含本节点：
    ```bash
    expected_chains=("hf-regression-gate -> hf-doc-freshness-gate" "hf-doc-freshness-gate -> hf-completion-gate")
    for c in "${expected_chains[@]}"; do
      test "$(grep -c "$c" skills/hf-workflow-router/references/profile-node-and-transition-map.md)" -ge 4 || echo "ROUTE MAP CHAIN COUNT < 4: $c"
    done
    ```
  - **boundary check (R1 缓解 cold-readable)**：本任务对 router 文件的修改仅新增、无删除：
    ```bash
    test "$(git diff skills/hf-workflow-router/references/profile-node-and-transition-map.md | grep -E '^-[^-]' | wc -l)" = "0" || echo "DELETED LINES > 0 — VIOLATES BOUNDARY"
    ```
- 预期证据: `features/001-hf-doc-freshness-gate/evidence/T5-router-transition-modified.log`（含修改前后 grep 计数 diff + git diff 删除行计数）
- 完成条件: 总出现 ≥ 22 + 三 profile 主链 + 4 条 canonical route map chain + 三迁移表（隐含在 grep 总数中）+ git diff 删除行 = 0 + 三链通过

### T6. 修改 `skills/hf-completion-gate/SKILL.md`

- 目标: 在 `hf-completion-gate` SKILL.md 的 evidence bundle 段新增 1 段 prose，说明 doc-freshness verdict 的 evidence reference 规则（pass / partial / N/A 进入 bundle；blocked 由 doc-freshness-gate 自行路由回 tdd，不进入 bundle）
- Acceptance:
  - Given hf-completion-gate SKILL.md 已修改；When `hf-completion-gate` reviewer 冷读 evidence bundle 段；Then 能找到 doc-freshness verdict reference 的明确说明
  - Given doc-freshness verdict 文件路径作为 evidence；When `hf-completion-gate` reviewer 按 evidence bundle 校验；Then 能找到引用规则
  - Given hf-completion-gate verdict 逻辑；When 修改后；Then **未** 引入 doc-freshness blocked 的额外判定分支（CON-001：不破坏既有合同）
- 依赖: T5（router transition 必须先到位，evidence bundle 才有意义）
- Ready When: T5 = done
- 初始队列状态: pending
- Selection Priority: P6
- Files / 触碰工件: 修改 `skills/hf-completion-gate/SKILL.md`（1 段 prose-only 插入）
- 测试设计种子:
  - 主行为：`hf-completion-gate` 在评估完成时能正确 reference doc-freshness verdict
  - 关键边界：blocked 不进入 bundle 的规则必须显式写出
  - fail-first：故意写"所有 doc-freshness verdict 都进入 bundle"，verify reviewer 能发现违反 spec FR-005 第三条 acceptance
- Verify: `grep -c "doc-freshness" skills/hf-completion-gate/SKILL.md` ≥ 2（evidence bundle 段 + Reference Guide 段）；既有 verdict 词表段未被改动（diff -u 输出仅含新增段）
- 预期证据: `features/001-hf-doc-freshness-gate/evidence/T6-completion-gate-modified.log`（含 git diff 摘要）
- 完成条件: prose 段新增 + 不改 verdict 逻辑 + 三链通过

### T7. Walking Skeleton dogfooding dry run（HYP-004 final closure）

- 目标: 把本 feature 自身（`features/001-hf-doc-freshness-gate/`）作为被测对象，跑 3 个 manual dry run：T-NFR-002（lightweight ≤ 5 分钟 + ≤ 30 行）+ T-NFR-003（无外部 lint 工具）+ T-NFR-004（sync-on-presence N/A 维度），最终关闭 HYP-004 from "preliminarily closed by estimation" → "fully closed by dogfooding dry run"
- Acceptance:
  - Given 本 feature 自身的 spec / tasks / commits 作为输入；When 按 lightweight checklist template 跑 dry run；Then 总耗时 ≤ 5 分钟 + verdict 文件 ≤ 30 行（满足 NFR-002）
  - Given 项目无任何 docs lint 工具链；When 跑 dry run；Then verdict 仍能输出（满足 NFR-003）
  - Given 本仓库无 `packages/` 子目录；When dry run 判定 "模块层 README" 维度；Then verdict 该维度 = `N/A`，evidence 标 "未启用此资产"（满足 NFR-004）
  - Given 3 个 dry run 完成；When 父会话更新 progress.md；Then HYP-004 状态由 "preliminarily closed by estimation" 改为 "fully closed by dogfooding dry run on 2026-04-23"
- 依赖: T1, T2, T3, T4, T5, T6（全部 skill 本体 + router + completion-gate 集成必须就绪）
- Ready When: T6 = done
- 初始队列状态: pending
- Selection Priority: P7（M4 最后一步，walking skeleton）
- Files / 触碰工件: 创建 `features/001-hf-doc-freshness-gate/evidence/{dry-run-T-NFR-002-lightweight-time.md, dry-run-T-NFR-003-no-tools.md, dry-run-T-NFR-004-sync-on-presence.md}`；修改 `features/001-hf-doc-freshness-gate/progress.md` (HYP-004 final closure)
- 测试设计种子:
  - 主行为：本 feature 自身的 README / spec / tasks 作为 reviewer subagent 的输入，按 lightweight checklist 模板跑出 verdict
  - 关键边界：跑完后实测耗时 + 行数；判定 N/A 维度时 evidence 内容
  - fail-first：跑前先估算"本仓库会有哪些维度判定"，跑后比对，确认估算与实测一致
  - **NFR-001 一致性测试（追加 T-NFR-001-consistency）**：对 lightweight checklist 同输入派发**两次**独立 reviewer subagent，diff 两份 verdict 文件，确认 verdict + dimension breakdown 完全一致（允许 evidence 文件名 timestamp 不同；与 design §14 NFR-001 QAS 一致）。落到 evidence 文件 `dry-run-T-NFR-001-consistency.md`
- Verify:
  - 4 个 dry run evidence 文件存在（追加 T-NFR-001）：
    ```bash
    for f in dry-run-T-NFR-001-consistency dry-run-T-NFR-002-lightweight-time dry-run-T-NFR-003-no-tools dry-run-T-NFR-004-sync-on-presence; do
      test -f "features/001-hf-doc-freshness-gate/evidence/${f}.md" || echo "MISSING: ${f}.md"
    done
    ```
  - T-NFR-001 evidence 文件含 "verdict 一致" 关键句：
    ```bash
    grep -E "verdict.*一致|consistency.*pass|两次.*verdict.*相同" features/001-hf-doc-freshness-gate/evidence/dry-run-T-NFR-001-consistency.md > /dev/null || echo "MISSING NFR-001 CONSISTENCY EVIDENCE"
    ```
  - T-NFR-002 evidence 含实测耗时记录与行数：
    ```bash
    grep -E "耗时|时间|minute|行数|line" features/001-hf-doc-freshness-gate/evidence/dry-run-T-NFR-002-lightweight-time.md > /dev/null || echo "MISSING NFR-002 TIMING EVIDENCE"
    ```
  - progress.md HYP-004 行已更新为 "fully closed by dogfooding dry run on 2026-04-23"：
    ```bash
    grep -F "fully closed by dogfooding" features/001-hf-doc-freshness-gate/progress.md > /dev/null || echo "HYP-004 STATUS NOT UPDATED"
    ```
- 预期证据: 4 个 dry run evidence 文件本身就是预期证据（追加 T-NFR-001-consistency 后总数 = 4）
- 完成条件: HYP-004 final closure + NFR-001 一致性 evidence 落盘 + 三链通过 + 本任务作为 walking skeleton 同时验证 NFR-001 / NFR-002 / NFR-003 / NFR-004

## 6. 依赖与关键路径

```text
T1 (SKILL.md)
  ↓
T2 (references) ── T3 (templates) ── T4 (evals)
                                       ↓
                                  T5 (router transition)
                                       ↓
                                  T6 (completion-gate)
                                       ↓
                                  T7 (Walking Skeleton dogfooding)
```

关键路径：T1 → T2 → T3 → T4 → T5 → T6 → T7（共 7 步，全部 sequential，无并行机会，因每步都依赖前一步的合同稳定）。

T1, T2, T3 可在概念上并行（都是新建文件无相互引用），但 SKILL.md (T1) 的 Reference Guide 段会引用 references (T2) 与 templates (T3) 的具体路径——按 sequential 拆解可让每步评审更聚焦。

## 7. 完成定义与验证策略

每个任务的完成定义：

- 文件创建 / 修改完成
- `Verify` 段所有命令退出码 = 0
- `hf-test-review` 通过
- `hf-code-review` 通过（含 Clean Architecture / SOLID / Two Hats 检查；本 feature 无运行时代码，主要检查 prose 一致性 / 引用合法 / 不破坏既有 skill 合同）
- `hf-traceability-review` 通过（追溯到 spec FR/NFR/CON + design 章节 + ADR）
- `hf-regression-gate` 通过（**预期 N/A**：本 feature 是 prose skill，无运行时代码，无 regression 测试可跑；reviewer 应判定 verdict = `N/A` 而非强行跑 nonexistent 测试）
- `hf-doc-freshness-gate` 通过（**dogfooding 路径**：本 gate 评估自己——本 feature 的 README / 模块 README 是否需要刷新）
- `hf-completion-gate` 通过（evidence bundle 包含上述全部 verdict）

整 feature 完成定义：所有 7 任务通过完成定义 + `hf-finalize` workflow closeout 同步：CHANGELOG.md（vX.Y.Z 入口）、ADR 状态翻 accepted、仓库根 README.md 更新 active feature 行。

## 8. 当前活跃任务选择规则

- T1 是 ready 起点
- 任一 task 完成（含全部 reviews + gates 通过）后，按依赖图选下一 ready task
- 在本 feature 内，因 T1..T7 全部 sequential，next-ready 选择规则简化为：当前 task done → 下一 task = 当前 task `Depends On` 的子节点中第一个 status=pending 的（即按 T1→T2→T3→T4→T5→T6→T7 顺序）
- 任一 task 评审失败 → next = `hf-test-driven-dev` 或 `hf-test-review` 或对应 review skill（按反馈结论）
- 任一 task 触发 reroute_via_router=true → next = `hf-workflow-router`

## 9. 任务队列投影视图

| Task ID | Status | Depends On | Ready When | Selection Priority |
|---|---|---|---|---|
| T1 | ready | - | spec/design/tasks approval 已完成 | P1 |
| T2 | pending | T1 | T1=`done` | P2 |
| T3 | pending | T2 | T2=`done` | P3 |
| T4 | pending | T3 | T3=`done` | P4 |
| T5 | pending | T4 | T4=`done` | P5 |
| T6 | pending | T5 | T5=`done` | P6 |
| T7 | pending | T6 | T6=`done` | P7 |

`Task Board Path`: 不需要单独 `task-board.md` 文件——本 queue 投影视图已足够 cold-readable，且 7 任务全 sequential 不需 board 协调。

## 10. 风险与顺序说明

- **R1 (中)**：T5 修改 router 与 T6 修改 hf-completion-gate 都是"改既有 skill"，必须严守 design §11 Boundary Constraints（不破坏既有合同；只新增 prose 段，不改既有 verdict 逻辑）。缓解：T5 / T6 的 `hf-code-review` reviewer 重点检查 git diff 的"删除行"（应为 0）+ "新增行"（应仅在新段内）。
- **R2 (低)**：T7 dogfooding 在本 feature 自身上跑 dry run 存在 chicken-and-egg 启动语义——本 gate 评估自己。缓解：design Q2 已识别此特殊性；dry run 时应明确声明"本次被测对象是 features/001-hf-doc-freshness-gate/ 自身"，不与"评估其他真实 feature"混淆。
- **R3 (低)**：reviewer subagent 在 T1 / T2 / T3 / T4 阶段读取 spec §6.2 责任矩阵时，可能因长度（14 行 × 5 列）误解某行；缓解：T2 的 `responsibility-matrix.md` 必须 cold-link spec §6.2，不复述（避免双 source-of-truth 漂移）。
- **R4 (低)**：HYP-004 final closure 在 T7 中通过实测，如 dogfooding 实测耗时 > 5 分钟，应回到 hf-design 修订 §10.3 lightweight checklist 模板（按 hf-test-review verdict=blocked → hf-test-driven-dev 路径处理，并按 router 升级到回 design）。
