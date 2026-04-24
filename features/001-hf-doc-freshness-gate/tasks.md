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
- Verify:
  - `test -f skills/hf-doc-freshness-gate/SKILL.md`
  - 8 标准段 anchor 逐项检查（cold-link `docs/principles/skill-anatomy.md`）：
    ```bash
    for s in "Methodology" "When to Use" "Hard Gates" "Workflow" "Output Contract" "Reference Guide" "Red Flags" "Verification"; do
      grep -F "## $s" skills/hf-doc-freshness-gate/SKILL.md > /dev/null || echo "MISSING SECTION: $s"
    done
    ```
    （全部存在则无输出）
  - frontmatter `description` 字段 ≤ 1024 字符（精确锚定 description 字段，避免 `name` 等其他字段被计入）：
    ```bash
    python3 -c "import sys; t=open('skills/hf-doc-freshness-gate/SKILL.md').read(); blocks=t.split('---'); fm=blocks[1] if len(blocks)>=3 else ''; import re; m=re.search(r'^description:\s*(.+?)(?=^\w|^---)', fm, re.M|re.S); d=m.group(1).strip() if m else ''; assert len(d)<=1024, f'description length {len(d)} > 1024'; print(f'OK: description {len(d)} chars')"
    ```
- 预期证据: `features/001-hf-doc-freshness-gate/evidence/T1-skill-md-created.log`（含 file size + section grep 结果 + description 字符数）
- 完成条件: 文件存在 + 8 段齐全（anchor 逐项检查无 MISSING 输出）+ frontmatter description ≤ 1024 字符 + `hf-test-review` + `hf-code-review` + `hf-traceability-review` 三链通过

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
- Verify:
  - 3 个文件存在：
    ```bash
    for f in skills/hf-doc-freshness-gate/references/{responsibility-matrix,profile-rubric,reviewer-dispatch-handoff}.md; do
      test -f "$f" || echo "MISSING: $f"
    done
    ```
  - SKILL.md Reference Guide 段引用 3 个 references 路径全部存在：
    ```bash
    for f in responsibility-matrix profile-rubric reviewer-dispatch-handoff; do
      grep -F "references/${f}.md" skills/hf-doc-freshness-gate/SKILL.md > /dev/null || echo "MISSING REFERENCE LINK: $f"
    done
    ```
  - 三档强制维度数量验证（`profile-rubric.md` 内含 lightweight/standard/full 三档表）：
    ```bash
    grep -c "^|.*lightweight" skills/hf-doc-freshness-gate/references/profile-rubric.md  # 至少 1
    grep -c "^|.*standard" skills/hf-doc-freshness-gate/references/profile-rubric.md     # 至少 1
    grep -c "^|.*full" skills/hf-doc-freshness-gate/references/profile-rubric.md         # 至少 1
    ```
- 预期证据: `features/001-hf-doc-freshness-gate/evidence/T2-references-created.log`
- 完成条件: 3 文件存在 + SKILL.md 3 处引用全部 cold-link 通过 + profile-rubric 含三档 + 三链通过

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
- Verify:
  - 2 个模板文件存在：
    ```bash
    for f in skills/hf-doc-freshness-gate/templates/{verdict-record-template,lightweight-checklist-template}.md; do
      test -f "$f" || echo "MISSING: $f"
    done
    ```
  - `verdict-record-template.md` 含 verdict 词表 4 值的引用（`pass` / `partial` / `N/A` / `blocked`）：
    ```bash
    for w in pass partial "N/A" blocked; do
      grep -F "$w" skills/hf-doc-freshness-gate/templates/verdict-record-template.md > /dev/null || echo "MISSING VERDICT WORD: $w"
    done
    ```
  - `lightweight-checklist-template.md` 文件总行数 ≤ 50（含 metadata header + 围栏说明 + warning prose）；NFR-002 ≤ 30 行约束的是 *实例化 verdict 文件*（围栏内填空后内容），而非 *模板文件本身*：
    ```bash
    test "$(wc -l < skills/hf-doc-freshness-gate/templates/lightweight-checklist-template.md)" -le 50 || echo "TEMPLATE FILE TOO LONG (containing metadata header + fence + warning prose)"
    ```
  - **注意**：实测 *实例化* lightweight verdict 文件 ≤ 30 行（NFR-002）属 T7 dogfooding 范围，落到 `evidence/dry-run-T-NFR-002-lightweight-time.md`（实测 ~25 行已证），不在本任务 Verify 范围
- 预期证据: `features/001-hf-doc-freshness-gate/evidence/T3-templates-created.log`
- 完成条件: 2 文件存在 + verdict-record 含 4 词表值 + lightweight-checklist 模板文件 ≤ 50 行 + 三链通过（实例化 verdict 文件 ≤ 30 行的 dogfooding 实测延后到 T7）

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
- Verify:
  - JSON 合法：
    ```bash
    python3 -c "import json; json.load(open('skills/hf-doc-freshness-gate/evals/test-prompts.json'))"
    ```
  - scenario 数 = 5：
    ```bash
    test "$(jq 'length' skills/hf-doc-freshness-gate/evals/test-prompts.json)" = "5"
    ```
  - 5 scenario id 与 design §16 测试策略表 5 行一一对应：
    ```bash
    expected=("T-FR-001-pass" "T-FR-001-blocked-traceability" "T-FR-003-N-A" "T-FR-005-partial" "T-FR-007-blocked-increment")
    for id in "${expected[@]}"; do
      jq -e ".[] | select(.id == \"$id\")" skills/hf-doc-freshness-gate/evals/test-prompts.json > /dev/null || echo "MISSING SCENARIO: $id"
    done
    ```
- 预期证据: `features/001-hf-doc-freshness-gate/evidence/T4-evals-created.log`
- 完成条件: JSON 合法 + 5 scenario + 5 scenario id 全部命中 + 三链通过

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
  - **boundary check (R1 缓解 cold-readable, semantic-aware)**：本任务对 router 文件的修改是"新增节点 + in-place 修改既有 chain 与 transition rule（把 `→ hf-completion-gate` 改为 `→ hf-doc-freshness-gate → hf-completion-gate`）"。git diff 文本上会显示 textual delete（属 in-place 行替换的副作用），不能用 `grep -E '^-[^-]' | wc -l = 0` 严格判定。改用 **semantic-aware check**：用 6 条 anchored grep 反向验证既有 transition rules 全部保持：
    ```bash
    for r in "hf-tasks-review.*通过.*任务真人确认" "hf-test-driven-dev.*实现完成.*hf-test-review" "hf-test-review.*通过.*hf-code-review" "hf-code-review.*通过.*hf-traceability-review" "hf-traceability-review.*通过.*hf-regression-gate" "hf-completion-gate.*主链任务全部完成.*hf-finalize"; do
      cnt=$(grep -cE "$r" skills/hf-workflow-router/references/profile-node-and-transition-map.md)
      test "$cnt" -ge 1 || echo "VIOLATION: previous rule [$r] removed!"
    done
    ```
    （所有 6 条既有 rule 仍可被 anchored grep 命中即视为 semantic delete = 0；textual delete 行数仅作信息记录）
- 预期证据: `features/001-hf-doc-freshness-gate/evidence/T5-router-transition-modified.log`（含修改前后 grep 计数 diff + 6 条 anchored grep 反向验证）
- 完成条件: 总出现 ≥ 22 + 三 profile 主链 + 4 条 canonical route map chain + 三迁移表（隐含在 grep 总数中）+ semantic delete = 0（6 条 anchored grep 全部保持）+ 三链通过

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
- Verify:
  - prose 段引用本 gate verdict 至少 2 次（evidence bundle 段 + Reference Guide 或类似段）：
    ```bash
    test "$(grep -c "doc-freshness" skills/hf-completion-gate/SKILL.md)" -ge 2 || echo "doc-freshness REFERENCE COUNT < 2"
    ```
  - **boundary check (R1 缓解 cold-readable)**：git diff 删除行 = 0（不改既有 verdict 逻辑）：
    ```bash
    test "$(git diff skills/hf-completion-gate/SKILL.md | grep -E '^-[^-]' | wc -l)" = "0" || echo "DELETED LINES > 0 — VIOLATES CON-001 (不破坏既有合同)"
    ```
  - git diff 净增行数 ≤ 30（修改范围最小化原则；确保仅 prose-only 1–2 段插入）：
    ```bash
    test "$(git diff --numstat skills/hf-completion-gate/SKILL.md | awk '{print $1}')" -le 30 || echo "ADDED LINES > 30 — modification too large"
    ```
  - completion-gate 既有 verdict 词表段未被改动（grep 既有词表关键词数量稳定）：
    ```bash
    git diff skills/hf-completion-gate/SKILL.md | grep -E "verdict|完成|approve" > /tmp/t6-verdict-vocab-diff.log
    test ! -s /tmp/t6-verdict-vocab-diff.log || echo "WARN: verdict vocabulary lines may have been touched — manual review required"
    ```
- 预期证据: `features/001-hf-doc-freshness-gate/evidence/T6-completion-gate-modified.log`（含 git diff 摘要 + 删除行计数 + 净增行数）
- 完成条件: prose 段新增 ≥ 2 处引用 + git diff 删除行 = 0（不改 verdict 逻辑）+ 净增 ≤ 30 行 + 三链通过

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

关键路径：T1 → T2 → T3 → T4 → T5 → T6 → T7（共 7 步，全部 sequential）。

### 6.1 Sequential vs parallel trade-off（显式称重）

T2 / T3 / T4 在**文件层面**确实可并行（都是新建文件、互不引用），T1 的 Reference Guide 段只需占位路径即可解锁三者并行起步。当前选择 **全 sequential** 是 conservative 决策，trade-off 如下：

| 维度 | sequential（当前选择） | parallel (T2/T3/T4) | 选择理由 |
|---|---|---|---|
| 评审聚焦 | ✅ 每个 task 单独走完 6-gate quality 链 | ⚠ 三任务并行时 reviewer 上下文需同时持有 3 份 draft | sequential 让每步 reviewer 只看一个 artifact，cold-read 成本最低 |
| 时间总开销 | ⚠ 三任务串行，理论开销 = 3 × N | ✅ 三任务并行，理论开销 ≈ N | parallel 节省约 2/3 编排时间 |
| 错误隔离 | ✅ 任一 task 评审失败不阻塞其他（已 done 的不退） | ⚠ 任一并行任务失败时，其他可能已经 review 过但需重审 | sequential 更容易回滚单 task |
| router FSM 复杂度 | ✅ 单线性队列，next-ready 选择规则极简 | ⚠ 需要 fork/join 编排，router 当前不支持任务并行 | router 既有协议是单 active task，并行需要扩展 |
| 与 HF 既有节奏一致性 | ✅ 与 HF "单 Current Active Task" 强约束完全一致 | ❌ 违反 router 既有"同时只锁定 1 个 active task"承诺 | sequential 是 HF 既有合同硬约束 |

**结论**：选择 sequential 不是没有评估并行收益，而是 router 既有"单 active task"硬约束（参见 `hf-workflow-router/SKILL.md`）+ 评审聚焦 + 错误隔离三项收益**优于** 2/3 时间节省。如未来 HF 引入 parallel-task 支持（属 `hf-increment` 或更大 evolution），可重新评估。

## 7. 完成定义与验证策略

每个任务的完成定义：

- 文件创建 / 修改完成
- `Verify` 段所有命令退出码 = 0（无错误输出）
- `hf-test-review` 通过
- `hf-code-review` 通过（含 Clean Architecture / SOLID / Two Hats 检查；本 feature 无运行时代码，主要检查 prose 一致性 / 引用合法 / 不破坏既有 skill 合同）
- `hf-traceability-review` 通过（追溯到 spec FR/NFR/CON + design 章节 + ADR）
- `hf-regression-gate`：见 §7.1 例外条款
- `hf-doc-freshness-gate`：见 §7.2 dogfooding 例外条款
- `hf-completion-gate` 通过（evidence bundle 包含上述全部 verdict）

整 feature 完成定义：所有 7 任务通过完成定义 + `hf-finalize` workflow closeout 同步：CHANGELOG.md（vX.Y.Z 入口）、ADR 状态翻 accepted、仓库根 README.md 更新 active feature 行。

### 7.1 `hf-regression-gate` 在 prose-only feature 上的处理（与 reviewer-return verdict 词表对齐）

reviewer-return-contract verdict 词表 = `{通过, 需修改, 阻塞}`，**没有** `N/A`。本 feature 是 prose skill，无运行时代码，无可跑的 regression 测试，但 verdict 仍必须落到合法词表内。**采用合规处理路径 (a)**：

- reviewer 返回 `通过` + record 显式标注 `"无 regression 测试范围（prose-only feature）"`
- evidence 文件路径仍按 `features/<active>/verification/regression-YYYY-MM-DD.md` 落盘，内容写明 "本 feature 无运行时代码，无 regression 测试可执行；reviewer 已确认无既有功能受影响（git diff 未触碰任何运行时代码路径）"
- 不允许 reviewer 返回非词表值（如 `N/A`），避免 router 无法解析

### 7.2 `hf-doc-freshness-gate` dogfooding chicken-and-egg 例外条款

`hf-doc-freshness-gate` 在本 feature 完成后才存在；T1..T6 完成时本 gate skill 尚未落地（T5 引入 router transition 后 router 才会指向本 gate）。处理规则：

- **T1..T4 完成时**：router 尚未含本 gate transition（T5 才修改 router）→ router 路径自然不经过本 gate，按 `hf-regression-gate → hf-completion-gate` 的旧路径处理；不强制 doc-freshness-gate verdict
- **T5 完成后**：router 含本 gate transition，但 skill 主体（SKILL.md / references / templates / evals）已在 T1-T4 完成 → router 派发 reviewer subagent 评估"本 task 是否 user-visible behavior change"。本 feature 内**唯一对外可见行为变化**是"引入了新 skill `hf-doc-freshness-gate`"；该变化的文档承接路径 = T7 dogfooding dry run + hf-finalize closeout 同步 README 与 CHANGELOG。因此 T5 / T6 完成时 verdict = `N/A`（本 gate 词表内合法值；本 task 未独立触发对外可见行为变化，外可见承载点 = T7）
- **T7 完成时**：T7 自身的 dogfooding dry run = 本 gate 评估自己 + walking skeleton 同时验证 NFR-001..NFR-004。verdict = `pass`（dogfooding 实测通过）
- **重要**：上述例外不破坏 design §11 boundary（本 gate verdict ∈ `{pass, partial, N/A, blocked}`），只是说明在 chicken-and-egg 场景下哪些 task 的 dogfooding evidence 是"独立产出" vs "由 T7 统一覆盖"

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
