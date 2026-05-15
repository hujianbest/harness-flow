# HF v0.6 — Author-side Discipline 升级 + Execution Mode Fast Lane 需求规格说明

- 状态: 草稿 Round 2（2026-05-13；架构师本会话拍板 D1~D7 + 删除 v0.8 + auto mode 推进；Round 1 spec-review 8 条 finding 已全部回修）
- 主题: 为 HarnessFlow 引入 7 项 author-side / wisdom-accumulation 改造（纯 markdown，三客户端通吃）+ 1 项 explicit opt-in 的 fast lane 节点（`hf-ultrawork`），把 OMO 在 *方法论层* 已验证的机制吃进 HF
- 范围锚点: ADR-008 D2

## 1. 背景与问题陈述

HarnessFlow（HF）当前在 v0.5.1 已经是一个跨 Claude Code / OpenCode / Cursor 三客户端的纯 Markdown skill pack（24 个 `hf-*` + `using-hf-workflow`）。架构师在 2026-05-13 提出参照 [Oh My OpenAgent (OMO) `code-yeongyu/oh-my-openagent`](https://github.com/code-yeongyu/oh-my-openagent) 的实现（不仅 README + manifesto，还包括其 `src/agents/` 11 agent + `src/hooks/` 52~59 hook + `src/tools/hashline-edit/` 24 文件 + `src/features/team-mode/` 13k LOC 等代码）进一步开发 HF。

读完 OMO 代码后，对照 HF 现状识别出 **HF 在 author-side 与 wisdom-accumulation 层面有 7 个具体空白**：

1. **作者侧无 gap analysis**：作者在写完 spec / design / tasks 之后直接提 review；OMO 用 Metis 在 plan 写出之前抓"作者忘了写下来的隐含意图、AI slop、漏写的验收标准"。HF 当前 review 节点要承担"既审专业性又审作者疏忽"的双重负担，信噪比下降。
2. **tasks-review 一锤子定生死**：HF `hf-tasks-review` verdict 只有 `通过` / `需修改` / `阻塞` 三档，没有"差一点就过的有限重写循环"机制；OMO Momus 用 4 维 rubric（Clarity / Verification / Context / Big Picture）+ 阈值（100% / 80% / 90% / 0% / 0%）+ 无限循环（直到达标），实践中给出"还差什么、改完再来"的明确反馈。
3. **`hf-specify` 缺 Interview State Machine**：HF `hf-specify` 现有 Socratic 步骤是线性的，长会话被打断后无法从工件恢复"问到第几个澄清问题了"；OMO Prometheus 的 Interview FSM 显式状态化（Interview ↔ Research ↔ ClearanceCheck → PlanGeneration），可恢复。
4. **跨 task 无知识沉淀通道**：HF 的 `hf-test-driven-dev` 完成一个 task 后，learnings / decisions / issues / verification / problems 都散落在各 task 的 review record 里，下一个 task 启动时不会显式继承；OMO Atlas 用 `notepads/{learnings,decisions,issues,verification,problems}.md` 5 文件强 schema 跨 task 累积，下游 prompt 显式注入摘要。**这是 HF 当前最大的方法论短板**。
5. **宿主项目无层次化上下文**：HF skill pack 自身有 `docs/principles/`（单层），但宿主项目（vendor 进 HF 的项目）没有按目录层级生成 `AGENTS.md` 的能力；OMO `/init-deep` 命令一键生成项目根 + `src/` + `src/components/` 各一层 `AGENTS.md`，agent 自动读取就近上下文。
6. **router 不消费 step-level 进度**：HF `hf-workflow-router` 只到 *节点级* 恢复（"现在该跑 hf-test-driven-dev"），不到 *task 内步级* 恢复（"task TASK-003 走到 RED 第几次"）。会话被打断后 task 内进度在工件中没有稳定存储。
7. **AI slop 检查只是 review checklist 文字**：HF `hf-code-review` 的"comment 质量"是 reviewer 的人工判断，没有可执行 rubric；OMO `comment-checker` 二进制 + 禁用模式列表（`simply` / `obviously` / `clearly` / em-dash 等）已经验证，可降级为 host 可 grep 的 markdown rubric。

外加架构师在本会话拍板 D3 + D4 = A：引入 OMO ultrawork 风格的 fast lane（"不做完不停"）。这与 HF `docs/principles/soul.md` 第 1 条硬纪律的张力**已由 ADR-009 治理**，本 spec 直接落 `hf-ultrawork` skill 作为 fast lane 承载节点。

ADR-008 D2 把这 7 个空白 + `hf-ultrawork` 锁成 v0.6 的范围。本 spec 把范围翻译成可执行的需求 + 验收标准。

## 2. 目标与成功标准

**高层目标**：让 HF v0.6 在不破坏三客户端可移植性、不引入 runtime 依赖的前提下，把 OMO 在 *方法论层* 已验证的 author-side / wisdom-accumulation 机制全部吃下；并为架构师提供 explicit opt-in 的 fast lane 体验。

**总体成功标准口径**：

- HF skill 数从 24 → **28**（新增 `hf-wisdom-notebook` / `hf-gap-analyzer` / `hf-context-mesh` / `hf-ultrawork`），`using-hf-workflow` skill 数不变（但 SKILL.md 内部修改一行，见下）
- 现有 25 个 SKILL.md（24 hf-* + `using-hf-workflow`）中允许修改 **7 个**：4 个主升级（`hf-tasks-review` / `hf-specify` / `hf-workflow-router` / `hf-code-review`）+ 3 个集成点修改（`using-hf-workflow` 步骤 5 entry bias 加一行 / `hf-test-driven-dev` Output Contract 引用 wisdom-notebook / `hf-completion-gate` 校验 wisdom-notebook delta）；其它 18 个 skill 在本 feature 不动
- 全部新增 / 修改的 skill 通过 `scripts/audit-skill-anatomy.py` 检查（v0.2.0 起的 anatomy 合规基线：必含 `## Common Rationalizations`、不含独立 `## 和其他 Skill 的区别`）
- `hf-ultrawork` 的 fast lane 行为在以下场景被 dogfood 验证：本 feature 自己作为第一个 dogfood 案例，从 `hf-spec-review` 一路推到 `hf-finalize`，全程 `Execution Mode: auto`，`progress.md` 必须含完整 Fast Lane Decisions audit trail
- 三客户端集成路径（Cursor / OpenCode / Claude Code）在 v0.6 install 后均能识别 4 个新 skill 与 4 个修改后的 skill；`install.sh` / `uninstall.sh` 不需修改（v0.6 是 skill 内增量，install topology 不变）
- soul.md / methodology-coherence.md / skill-anatomy.md 三份宪法文档**不变**；HF 灵魂保持

## 3. Success Metrics

| 指标 | 阈值 | 测量方法 |
|---|---|---|
| Outcome Metric: v0.6 范围 11 个 skill 改动 100% 落地 | 4 新 + 7 改 = 11 个 SKILL.md 文件全部存在并通过 `audit-skill-anatomy.py` | `find skills/{hf-wisdom-notebook,hf-gap-analyzer,hf-context-mesh,hf-ultrawork} -name SKILL.md` 必须 4 条；`git diff --name-only main..HEAD skills/{hf-tasks-review,hf-specify,hf-workflow-router,hf-code-review,using-hf-workflow,hf-test-driven-dev,hf-completion-gate}/SKILL.md` 必须 7 条；`python3 scripts/audit-skill-anatomy.py --skills-dir skills` 必须 PASS |
| Leading Indicator 1: wisdom-notebook 5 文件强 schema 校验通过 | 新增 `scripts/validate-wisdom-notebook.py` 在本 feature 的 `notepads/` 上跑过 PASS（包括 `learnings.md` / `decisions.md` / `issues.md` / `verification.md` / `problems.md` 5 文件齐全且 schema 合规） | TDD 阶段写 fixture + script，CI / hf-completion-gate 调用 |
| Leading Indicator 2: tasks-review momus rubric 在本 feature 自己的 `tasks-review` 跑过 | 本 feature 自己的 `reviews/tasks-review-*.md` 必须含 4 维评分（Clarity / Verification / Context / Big Picture）+ 阈值判断 | reviewer 在 review record 中按 `references/momus-rubric.md` 给分 |
| Leading Indicator 3: fast lane audit trail 完整 | `progress.md` 的 Fast Lane Decisions 段在本 feature 全流程结束时，必须包含**所有**自动决策行（spec/design/tasks 的 auto-approve 各 1 行 + router 的 canonical next action 自动推进若干行 + 任意 boulder loop 触发记录） | `grep -c '^|' features/002-omo-inspired-v0.6/progress.md` 在 Fast Lane Decisions 段中行数 ≥ 5 |
| Leading Indicator 4: 三客户端 install 后能看到 4 个新 skill | 在干净宿主仓库跑 `install.sh --target both` 后，`.opencode/skills/` 与 `.cursor/harness-flow-skills/` 下都能看到 4 个新 skill 目录 | 端到端测试脚本 |
| Lagging Indicator: 文档刷新覆盖度 | `README.md` / `README.zh-CN.md` / `docs/principles/soul.md` 中"v0.6+ 计划 `hf-shipping-and-launch` / `hf-ci-cd-and-automation` / etc."的"未来计划"措辞**全部**改为"显式 out-of-scope（参 ADR-008 D1）" | doc-freshness gate 时 grep `hf-shipping-and-launch` 必须仅出现在"已删除"语境 |
| Measurement Method | TDD 阶段的端到端 dogfood + audit-skill-anatomy.py + validate-wisdom-notebook.py + grep |
| Non-goal Metrics | **不**度量：runtime 性能（runtime 在 v0.7 feature）；新 skill 的"用户首次理解时间"（不是性能 feature）；多人协作下的 fast lane 行为（架构师单人模型） |
| Instrumentation Debt | `progress.md` 的 Fast Lane Decisions 段是唯一观测点；不接入任何外部 telemetry |

## 4. Key Hypotheses

| ID | Statement | Type | Impact If False | Confidence | Validation Plan | Blocking? |
|---|---|---|---|---|---|---|
| HYP-001 | wisdom-notebook 的 5 文件强 schema（D7 = A）足以承载跨 task 知识沉淀，不需要数据库 / SQLite | Design | 必须重做 schema（按 OMO Atlas 是单 markdown 文件，但实际上 OMO 也是 5 文件——所以 confidence 高） | High | TDD 阶段在本 feature 自己的 notepads/ 上跑通跨 task 知识传递，至少包含 3 个 task 的累积 | 否 |
| HYP-002 | 在不引入 v0.7 runtime 的前提下，markdown 包内已有的 Execution Mode preference 机制 + 可被 host agent 读取的 progress 工件，足以承载 fast lane 的全部行为（具体机制由 hf-design 阶段决定） | Design | fast lane 在 markdown-only 路径下精度严重下降（idle 检测不可靠 / boulder loop 无法触发），需要把 fast lane 推到 v0.7 | Medium-High（OMO 的 fast lane 严重依赖 runtime hook；HF 在 markdown-only 路径下能做到的是"宣告式"fast lane——告诉 host agent "这个 mode 下要这样做"，由 host 自觉遵守） | TDD 阶段在 Cursor / OpenCode / Claude Code（三客户端无 runtime）上**横向**跑本 feature 自己的 fast lane（hf-design 拆出独立跨客户端 verification task），验证全程不需要架构师手动确认即可推到 hf-finalize | **是**（如果 markdown-only fast lane 不可用，必须把 `hf-ultrawork` 改为"runtime 不可用时降级为提示用户开 standard mode"） |
| HYP-003 | `hf-gap-analyzer` 作为 author-side self-check（D6 = A），不破坏 8 个 Fagan review 节点拓扑 | Design | 必须升格为第 9 个 review 节点，工作流复杂度上升 | High（gap analysis 的输出 `<artifact>.gap-notes.md` 是辅助上下文，作者吸收后仍走标准 review；这与 OMO Metis 的角色一致——Metis 不是 reviewer） | TDD 阶段在本 feature 自己的 spec.md 上跑一次 gap-analyzer，验证 gap-notes 被 spec 作者吸收后仍由 hf-spec-review 给出 verdict | 否 |
| HYP-004 | v0.6 范围 8 个 skill 改动可在不修改 `install.sh` / `uninstall.sh` / `.cursor/rules/harness-flow.mdc` 的情况下被三客户端正确加载 | Feasibility | 必须修改 install topology，feature 范围扩大 | High（install.sh 是按 `skills/<name>/SKILL.md` 通配符复制的，新增 skill 自动覆盖；mdc rule 不依赖具体 skill 列表） | TDD 阶段在干净宿主仓库 install 后 ls 验证 | 否 |
| HYP-005 | `hf-context-mesh` 生成的层次化 `AGENTS.md` 在 Cursor / OpenCode / Claude Code 三客户端下都能被正确读取（host 各自的 AGENTS.md 加载语义） | Compatibility | hf-context-mesh 在某些客户端上无效 | Medium（OpenCode 通过 `directoryAgentsInjector` hook 加载；Cursor 通过 `.cursor/rules/` 加载；Claude Code 通过 `CLAUDE.md` 加载——三者语义不完全相同） | TDD 阶段在三客户端各自跑一次 hf-context-mesh，验证生成的 AGENTS.md 被加载 | 否（即便部分客户端不完美支持，hf-context-mesh 仍是 markdown 文件，agent 显式 Read 也能读取） |

无 Blocking 假设处于"未验证"状态：HYP-002 是 Blocking，但 confidence Medium-High、有明确 Validation Plan，会在 TDD 阶段第一个验证通过后才允许 hf-completion-gate 通过。

## 5. 用户角色与关键场景

**主要用户**：

- **HF 架构师**（你）：在三客户端任一中跑 HF workflow 的工程师；可能 explicit opt-in fast lane 也可能走 standard mode
- **HF 自身的 cloud agent**：在 dogfood 流程中扮演 reviewer / implementer 角色
- **下游 vendor HF 的项目工程师**：把 HF skill pack 装进自己仓库，按 v0.6 新能力执行 SDD / TDD / fast lane

**关键场景**：

- **场景 A — author-side gap self-check**：作者写完 `spec.md` 后，主动 invoke `hf-gap-analyzer` 检查"作者脑里有但纸上没有"的隐含意图、AI slop、漏写验收标准。期望：得到 `spec.md.gap-notes.md`，作者读完吸收 / 驳回某些条目，再提交 `hf-spec-review`。
- **场景 B — tasks-review momus 4 维循环**：reviewer 在 `hf-tasks-review` 中按 4 维 rubric 给分；总分不达 4 个阈值（100% / 80% / 90% / 0% / 0%）时给 `verdict: rejected-rewrite`，author 改完再来；3 次后仍不达标升级到架构师决策。期望：plan quality 显著提升，进入实现阶段时不再有"任务粒度 / 依赖 / acceptance"模糊。
- **场景 C — 长会话被打断后 hf-specify 恢复**：作者在 `hf-specify` 的 Interview FSM 中正在回答第 5 个澄清问题时，会话崩溃。新会话起 `hf-specify` 时，从 `spec.intake.md` 读出"已经问过 4 个问题，第 5 个问题已发出但未收到答复"，从断点继续。期望：不丢澄清进度。
- **场景 D — 跨 task 知识沉淀**：feature 002 的 TASK-003 完成时，作者在 notepads/ 写入 `learnings.md`（如"v0.6 SKILL.md 必须含 Common Rationalizations 段"）；router 在选 TASK-004 时把 learnings 摘要注入下游 prompt。期望：TASK-004 的实现节点不重复 TASK-003 已踩过的坑。
- **场景 E — 宿主项目层次化上下文**：vendor 用户在自己仓库跑 `hf-context-mesh`，自动生成根目录 `AGENTS.md` + `src/AGENTS.md` + `src/components/AGENTS.md`。期望：每层 AGENTS.md 包含该目录的关键约定与典型 pattern，agent 自动读取就近上下文。
- **场景 F — fast lane 全流程不停**：架构师在会话开头说"auto mode 完成，中间不要停下来"，feature 002 自己作为 dogfood：spec → spec-review → spec-approval → design → design-review → design-approval → tasks → tasks-review → tasks-approval → TDD × N tasks → 各 review → gates → finalize 全程 ultrawork 推进，每个 auto 决策点写入 progress.md Fast Lane Decisions。期望：架构师只在以下时刻被打断：(a) 任一 Hard Gate 命中"方向 / 取舍 / 标准不清"；(b) review verdict = `阻塞`；(c) gate FAIL；(d) wisdom notebook problems.md 出现 status=open 项；(e) rewrite loop 连续 3 次未通过；(f) 架构师主动说"停"。
- **场景 G — fast lane 的 escape**：fast lane 推进中 reviewer 给 `tasks-review` verdict = `阻塞`，escape 触发，回到架构师；架构师指示后再决定是否切回 fast lane 继续。期望：escape 干净，不会被 boulder loop 强制覆盖架构师指示。

## 6. 当前轮范围与关键边界

**当前轮范围**：

新增 4 个 skill：
- `skills/hf-wisdom-notebook/SKILL.md` + `references/notebook-schema.md` + `references/notebook-update-protocol.md`
- `skills/hf-gap-analyzer/SKILL.md` + `references/gap-rubric.md`
- `skills/hf-context-mesh/SKILL.md` + `references/agents-md-template.md`
- `skills/hf-ultrawork/SKILL.md` + `references/fast-lane-escape-conditions.md`

修改 7 个 skill —— 4 个主升级 + 3 个集成点修改：

**主升级 4 个**：
- `skills/hf-tasks-review/SKILL.md` + 新增 `references/momus-rubric.md`：引入 4 维 rubric + N=3 rewrite loop + `verdict: rejected-rewrite`
- `skills/hf-specify/SKILL.md` + 新增 `references/interview-fsm.md` + `references/spec-intake-template.md`：引入 5 状态 Interview FSM + `spec.intake.md` schema
- `skills/hf-workflow-router/SKILL.md` + 修改 `references/profile-node-and-transition-map.md` + 修改 `references/workflow-shared-conventions.md`：引入 step-level recovery + `category_hint` handoff 字段 + progress.md schema 新增 Fast Lane Decisions 段
- `skills/hf-code-review/SKILL.md` + 新增 `references/ai-slop-rubric.md`：把 AI slop 检查升级为可执行 rubric（基于 OMO comment-checker 已验证模式）

**集成点修改 3 个**：
- `skills/using-hf-workflow/SKILL.md`：步骤 5 entry bias 表新增一行 `Execution Mode = auto 且当前不在 review/gate 节点 → direct invoke hf-ultrawork`；**步骤 3 现有 Execution Mode preference 解析逻辑保持不变**；步骤 6 命令 bias 表保持不变（不引入 `/ultrawork` 命令）
- `skills/hf-test-driven-dev/SKILL.md`：Output Contract 段引用 `hf-wisdom-notebook`，要求 task 完成时按 FR-002 schema 写 notebook delta
- `skills/hf-completion-gate/SKILL.md`：closeout 前调用 `scripts/validate-wisdom-notebook.py` 校验 wisdom-notebook delta 完整性

**4 个新 skill 全部按 ADR-006 D1 anatomy v2 创建**（`SKILL.md` + `references/` + `evals/` + `scripts/` 四子目录约定）：
- `hf-wisdom-notebook` 与 `hf-ultrawork` 必须含 `evals/` 目录（高风险 skill：分别承载工件 schema 强约束 / fast lane 决策权）
- `hf-gap-analyzer` 与 `hf-context-mesh` `evals/` 可选（中风险 skill；hf-design 阶段决定是否落 evals）
- `hf-wisdom-notebook` 是否需要 `scripts/`（schema validator 可能放该 skill 内而非 repo-root `scripts/`）由 hf-design 阶段决定

新增 1 个 stdlib python 工具：
- `scripts/validate-wisdom-notebook.py`（与 `scripts/audit-skill-anatomy.py` 同等地位，stdlib-only，CI / hf-completion-gate 可调用）；**或**经 hf-design 决定后落到 `skills/hf-wisdom-notebook/scripts/validate-wisdom-notebook.py`（per ADR-006 D1 / D2 skill-owned tooling 优先于 repo-root tooling）

文档刷新：
- `README.md` / `README.zh-CN.md` / `docs/principles/soul.md` 中"v0.6+ 计划 `hf-shipping-and-launch` / `hf-ci-cd-and-automation` / etc."的"未来计划"措辞改为"显式 out-of-scope（参 ADR-008 D1）"
- `README.md` / `README.zh-CN.md` 的 skill 总数从 24 → 28；`hf-finalize` 的 closeout HTML 渲染脚本不变
- `CHANGELOG.md` Unreleased 段新增"v0.6 author-side + fast lane scope"条目

文档刷新：
- `README.md` / `README.zh-CN.md` / `docs/principles/soul.md` 中"v0.6+ 计划 `hf-shipping-and-launch` / `hf-ci-cd-and-automation` / etc."的"未来计划"措辞改为"显式 out-of-scope（参 ADR-008 D1）"
- `README.md` / `README.zh-CN.md` 的 skill 总数从 24 → 28；`hf-finalize` 的 closeout HTML 渲染脚本不变
- `CHANGELOG.md` Unreleased 段新增"v0.6 author-side + fast lane scope"条目

**关键边界**：

- **不**修改 25 个现有 SKILL.md 中除 4 主升级 + 3 集成点修改外的 18 个 skill
- **不**新增 / 修改任何 slash 命令（v0.6 仍是 7 个 slash 命令）
- **不**修改 `install.sh` / `uninstall.sh` / `.cursor/rules/harness-flow.mdc` / `.claude-plugin/marketplace.json`（HYP-004）
- **不**引入任何 runtime 依赖；本 feature 全程纯 markdown + stdlib python 工具
- **不**修改 `docs/principles/soul.md` / `docs/principles/methodology-coherence.md` / `docs/principles/skill-anatomy.md`（宪法层不变）
- **不**做 v0.7 runtime 范围内的事（hashline / record-evidence / progress-store 等等）
- **不**做 v0.8 删除范围内的事（任何部署 / 可观测 / 度量 / 性能 / 安全 / 调试相关 skill）
- **不**做 OMO Team Mode 等价物（多 worktree / 并行实现）
- **不**做 OMO Hephaestus 等价物（autonomous deep worker 跳过 review/gate）
- `hf-ultrawork` 的 fast lane 在三客户端下行为可能存在差异（HYP-002）；本 feature 验证 markdown-only 路径足够，深度增强留给 v0.7 runtime

## 7. 功能需求（FR）

| FR ID | 描述 | 优先级 | Acceptance |
|---|---|---|---|
| **FR-001** | 新增 `hf-wisdom-notebook` skill 承载跨 task 知识沉淀 | MUST | (1) `skills/hf-wisdom-notebook/SKILL.md` 存在并通过 audit-skill-anatomy.py；(2) 文件含 5 文件 schema 引用（learnings/decisions/issues/verification/problems.md）；(3) 含 `When to Use` / `Object Contract` / `Workflow` / `Common Rationalizations` 各段 |
| **FR-002** | `hf-test-driven-dev` 完成一个 task 后 **必须** 写 wisdom notebook delta | MUST | (1) `hf-test-driven-dev/SKILL.md` 的 Output Contract 段要求 task 完成时：(a) 5 个 notebook 文件作为容器**必须存在**（`learnings.md` / `decisions.md` / `issues.md` / `verification.md` / `problems.md`；首次 task 创建空骨架，validate 时只检查文件存在性）；(b) 每个 task **至少**在 `learnings.md` / `verification.md` 任一中追加 delta 段（其它 3 个文件按需）；(2) `hf-completion-gate` 在 closeout 前调用 `validate-wisdom-notebook.py` 校验 5 文件容器齐全 + 每 task 至少有 learnings/verification delta |
| **FR-003** | `hf-workflow-router` 选下一个 Current Active Task 时 **必须** 把 notebook 摘要注入 handoff | MUST | router transition map 含 "wisdom notebook 摘要注入" 步骤；handoff schema 含 `wisdom_summary` 字段 |
| **FR-004** | 新增 `hf-gap-analyzer` skill 作为 author-side self-check | MUST | (1) `skills/hf-gap-analyzer/SKILL.md` 存在并通过 audit；(2) 输出 `<artifact>.gap-notes.md`；(3) 不是 Fagan review 节点 |
| **FR-005** | `hf-tasks-review` 引入 Momus 4 维 rubric + N=3 rewrite loop | MUST | (1) `skills/hf-tasks-review/references/momus-rubric.md` 存在；(2) SKILL.md 含 `verdict: rejected-rewrite` + 3 次循环上限；(3) 第 4 次仍未通过 → `verdict: 阻塞` 升级到架构师 |
| **FR-006** | `hf-specify` 引入 5 状态 Interview FSM 与 `spec.intake.md` schema | MUST | (1) `skills/hf-specify/references/interview-fsm.md` 存在；(2) `references/spec-intake-template.md` 存在；(3) SKILL.md Workflow 段引用 FSM |
| **FR-007** | 新增 `hf-context-mesh` skill 一键生成宿主项目层次化 AGENTS.md | MUST | (1) `skills/hf-context-mesh/SKILL.md` 存在并通过 audit；(2) `references/agents-md-template.md` 含项目根 / 中层目录 / 叶子目录三种模板 |
| **FR-008** | 新增 `hf-ultrawork` skill 承载 explicit opt-in fast lane | MUST | (1) `skills/hf-ultrawork/SKILL.md` 存在并通过 audit；(2) SKILL.md `Hard Gates` 段直接 enumerate 不可压缩的 5 类项（8 个 Fagan review / 3 个 gate / closeout pack 完整性 / spec-design-tasks approval 工件落盘 / 任何 Hard Gates 命中"方向 / 取舍 / 标准不清"必须停下抛回——具体见 ADR-009 D2 表格），**不允许**只写"按 ADR-009 D2 执行"；(3) 含 escape conditions 引用 `references/fast-lane-escape-conditions.md`（按 ADR-009 D3 第 4 项的 6 个 escape 信号 enumerate） |
| **FR-009** | `using-hf-workflow` step 5 entry bias 新增 fast lane 一行 | MUST | (1) SKILL.md 步骤 5 表格新增 `Execution Mode = auto 且当前不在 review/gate → direct invoke hf-ultrawork` 行；(2) **步骤 3 现有 Execution Mode preference 解析逻辑保持不变**；(3) 步骤 6 命令 bias 表保持不变（不引入 `/ultrawork` 命令）；(4) FR-009 仅在步骤 5 entry bias 表新增一行，不动其它步骤 |
| **FR-010** | `progress.md` schema 新增 Fast Lane Decisions 段 | MUST | (1) `hf-workflow-router/references/workflow-shared-conventions.md` 中新增 progress.md schema 段；(2) 本 feature 自己 `progress.md` 含此段且有完整 audit trail |
| **FR-011** | `hf-code-review` AI slop 检查升级为可执行 rubric | MUST | `skills/hf-code-review/references/ai-slop-rubric.md` 存在，含禁用模式列表（`simply` / `obviously` / `clearly` / em-dash 等），可被 host grep 调用 |
| **FR-012** | 新增 `scripts/validate-wisdom-notebook.py`（stdlib-only） | MUST | (1) 文件存在；(2) 跑本 feature `notepads/` 通过 PASS；(3) `--help` 自描述清晰 |
| **FR-013** | `README.md` / `README.zh-CN.md` / `docs/principles/soul.md` 中 v0.6+ 计划末段措辞统一改为"显式 out-of-scope（参 ADR-008 D1）" | MUST | doc-freshness gate 时 grep `hf-shipping-and-launch` 仅出现在"已删除"语境 |
| **FR-014** | `CHANGELOG.md` Unreleased 段新增 v0.6 scope 条目 | MUST | grep `v0.6` 找到对应条目 |
| **FR-015** | `hf-workflow-router` handoff schema 新增 `category_hint` 字段（不强制下游消费） | SHOULD | (1) transition map 中 handoff 示例含 `category_hint`；(2) 下游 skill 不消费时直接忽略不报错；(3) **SHOULD 失败处理**：FR-015 不达标时 `hf-completion-gate` **不阻塞** closeout，但需在 closeout pack 的 deferred backlog 段记录"FR-015 deferred to v0.6.x"以便后续 increment |

## 8. 非功能需求（NFR）

| NFR ID | 描述 | 验证 |
|---|---|---|
| **NFR-001** | 全部新增 / 修改 SKILL.md 通过 `scripts/audit-skill-anatomy.py`（v0.2.0 anatomy 合规基线：必含 `Common Rationalizations`、不含独立 `和其他 Skill 的区别`） | CI / regression-gate 调用 audit |
| **NFR-002** | 新增 4 个 SKILL.md 主文件正文 < 500 行 / < 5000 tokens（skill-anatomy.md 第 9 条预算） | wc -l + token 估算 |
| **NFR-003** | 不修改 `install.sh` / `uninstall.sh` / `.cursor/rules/harness-flow.mdc` / `.claude-plugin/marketplace.json` | git diff 校验 |
| **NFR-004** | **三**客户端 install 后 4 个新 skill 与 7 个修改后 skill 全部可识别 | 端到端测试在 Cursor / OpenCode / **Claude Code** 三客户端各装一次后验证：Cursor 检查 `.cursor/harness-flow-skills/` 内 4 个新 skill 目录存在 + 7 个改 SKILL.md 含本 feature 修改痕迹；OpenCode 检查 `.opencode/skills/` 同上；Claude Code 通过 `/plugin install` 后检查 `~/.claude/plugins/<plugin>/skills/`（依赖 install topology 拷贝 `skills/` 全树的语义，本 feature 不动 `.claude-plugin/marketplace.json`，HYP-004） |
| **NFR-005** | `validate-wisdom-notebook.py` 仅依赖 python3 stdlib（与 `audit-skill-anatomy.py` 同等约束） | grep `^import` 仅出现 stdlib 模块 |
| **NFR-006** | fast lane 在 markdown-only 路径下（无 v0.7 runtime）的精度足以让 dogfood 全程不需要架构师手动确认即可推到 hf-finalize | HYP-002 验证 |
| **NFR-007** | 本 feature 自身的 SDD 主链 dogfood：spec → spec-review × N → design → design-review × N → tasks → tasks-review × N → TDD × M tasks → 各 review × N → gates → finalize 全部走完，且 `progress.md` 含完整 Fast Lane Decisions audit trail | hf-finalize closeout pack 检查 |

## 9. Scope Out（明确不做）

- v0.7 runtime 范围（hashline-edit / record-evidence / progress-store / hooks 等）→ ADR-010 + 后续 v0.7 feature
- v0.8 删除范围（任何部署 / 可观测 / 度量 / 事故 / 性能 / 安全 / 调试 / 弃用迁移相关 skill）→ ADR-008 D1 永久封禁
- OMO Team Mode 等价物（多 worktree + 并行实现）→ D5 = A 拒绝
- OMO Hephaestus 等价物（autonomous deep worker 跳过 review/gate）→ ADR-009 D2 拒绝
- 任何修改 `docs/principles/soul.md` / `docs/principles/methodology-coherence.md` / `docs/principles/skill-anatomy.md` 的改动（宪法层不变）
- 任何新增 slash 命令的改动（v0.6 仍是 7 个 slash 命令）
- 任何 `hf-product-discovery` / `hf-experiment` / `hf-discovery-review` / `hf-design` / `hf-ui-design` / `hf-ui-review` / `hf-spec-review` / `hf-design-review` / `hf-tasks` / `hf-test-review` / `hf-traceability-review` / `hf-regression-gate` / `hf-doc-freshness-gate` / `hf-finalize` / `hf-hotfix` / `hf-increment` / `hf-release` / `hf-browser-testing` 的改动（18 个未升级 skill 在本 feature 不动；`hf-test-driven-dev` 与 `hf-completion-gate` 不在此列——它们属于 §6 列出的 3 个集成点修改 skill，由 FR-002 触发）

## 10. Open Questions（spec-review 时需澄清）

| ID | 问题 | 建议处理时机 |
|---|---|---|
| OQ-001 | wisdom-notebook 5 文件 schema 的字段细节（每个文件应含哪些固定字段 / Front-matter / 是否要加 status / severity / classification）？ | hf-design 阶段决定 |
| OQ-002 | `hf-context-mesh` 生成的 AGENTS.md 在三客户端的语义差异如何调和（OpenCode `directoryAgentsInjector` / Cursor `.cursor/rules/` / Claude Code `CLAUDE.md`）？ | hf-design 阶段决定，必要时拆出多套模板 |
| OQ-003 | `hf-ultrawork` 的 fast lane 关键词集合（中英文同义词覆盖度）边界在哪？ | hf-design 阶段决定 |
| OQ-004 | `hf-tasks-review` 的 N=3 rewrite loop 上限是否应该按 task 复杂度浮动（小 task N=2，大 task N=4）？还是统一 N=3？ | hf-design 阶段决定，建议统一 N=3 简化 |
| OQ-005 | `hf-specify` 的 5 状态 FSM 是否应允许 ClearanceCheck → Research 回退？还是只允许向前推进？ | hf-design 阶段决定 |
| OQ-006 | `progress.md` 的 Fast Lane Decisions 段是否应在长 feature 中拆出 `progress.fast-lane.md`（按 ADR-009 D4 的"中性"风险条目）？ | hf-design 阶段决定，建议本 feature 不拆，记入 instrumentation debt 待 v0.6.x 评估 |
| OQ-007 | `hf-ultrawork` 在 dogfood 本 feature 时，是否需要先单独写一个 minimal SKILL.md 跑通然后再完善？还是一次性写完？ | hf-tasks 阶段决定，建议一次性写完（fast lane 自身的 chicken-and-egg 不严重，因为本 feature 大部分工作不依赖 fast lane） |

无 Blocking Open Question 进入 spec-review 后未决：所有 OQ 都标了"hf-design 阶段决定"或"hf-tasks 阶段决定"，spec-review 通过的前提是 OQ-001 ~ OQ-007 在 review 时各自有"建议解 / 待 design 阶段确认"的明确归档。

## 11. 风险与缓解

| 风险 | 概率 | 影响 | 缓解 |
|---|---|---|---|
| HYP-002 falsified（markdown-only fast lane 不可用） | Medium | High（必须把 hf-ultrawork 改为"runtime 不可用时降级提示"） | hf-design 阶段先做 markdown-only fast lane prototype；TDD 阶段第一个验证 |
| 4 新 skill + 4 改 skill 总 token 占用超过 anatomy v2 共享预算（25000 tokens） | Low-Medium | Medium（需要 skill split / merge） | NFR-002 限制每个新 SKILL.md < 5000 tokens；超出时优先下沉 references/ |
| 三客户端 hf-context-mesh 行为不一致（HYP-005） | Medium | Low-Medium（不影响核心 workflow，只是上下文注入精度差异） | OQ-002 在 hf-design 决定；可拆 3 套模板 |
| dogfood 流程过长导致本 feature 自身 progress.md 巨大 | Medium | Low | 必要时按 OQ-006 在 v0.6.x 拆 progress.fast-lane.md |
| reviewer 在 momus rubric 下给分主观 | Low-Medium | Medium（rubric 写得不够明确会导致 reviewer 判断飘） | references/momus-rubric.md 必须含具体的 0-10 分定义 + 例子 |
| `hf-ultrawork` 与现有 `using-hf-workflow` Execution Mode preference 解析逻辑冲突 | Low | Medium | ADR-009 D5 已锁逻辑：using-hf-workflow 不变 + step 5 加一行 |
| OMO upstream 持续演进导致 HF 复制的 Momus / Atlas / Metis 逻辑过时 | Low | Low（HF 是 *方法论* 复制，不是代码 fork；OMO 升级不影响 HF markdown） | 无需特殊处理 |

## 12. Spec-Review Checklist（reviewer 用）

reviewer 必须验证：

- [ ] 7 个 v0.6 改动项（FR-001 ~ FR-013）与 ADR-008 D2 一一对应，无遗漏 / 无越界
- [ ] `hf-ultrawork`（FR-008）与 ADR-009 D2 / D3 一一对应
- [ ] HYP-002（Blocking）的 Validation Plan 在 TDD 阶段可执行
- [ ] OQ-001 ~ OQ-007 各自有"建议解 / 待决时机"，无悬空 OQ
- [ ] Scope Out 段（§9）显式列出 20 个未升级 skill + v0.7/v0.8/Team Mode/Hephaestus 等所有不做项
- [ ] 三客户端兼容（NFR-004）的端到端验证路径明确
- [ ] 与 `docs/principles/soul.md` 第 1 ~ 5 条硬纪律的对照：fast lane 引入是否破坏 soul（按 ADR-009 D2 验证）
- [ ] 是否漏掉对 `hf-finalize` 的影响（应该没有：v0.6 不修改 hf-finalize）
- [ ] doc-freshness 范围（FR-013 / FR-014）的 grep 验证可执行

## 13. 修订历史

| Round | 日期 | 变更摘要 |
|---|---|---|
| Round 1 | 2026-05-13 | 初稿；15 FR + 7 NFR + 5 HYP + 7 OQ + 12 review checklist 项 |
| Round 2 | 2026-05-13 | 按 `reviews/spec-review-2026-05-13.md` Round 1 verdict（需修改）回修 8 条 finding（important × 2 + minor × 6）：<br>- §2 / §3 / §6 / §9 统一口径"修改 7 个 skill"（4 主升级 + 3 集成点）<br>- NFR-004 验证补 Claude Code 三客户端横向口径<br>- FR-002 Acceptance 明确 5 文件容器齐全 + delta 至少落 learnings/verification 任一<br>- FR-008 Acceptance 要求 SKILL.md `Hard Gates` 段直接 enumerate 5 类不可压缩项<br>- §6 显式声明 4 新 skill 走 anatomy v2 四子目录；hf-wisdom-notebook / hf-ultrawork 必含 evals/<br>- FR-009 补 4 子项明确步骤 3 / 步骤 6 不变<br>- FR-015 SHOULD 补失败处理（不阻塞 + 记入 deferred backlog）<br>- HYP-002 去设计泄漏 wording；Validation Plan 加三客户端横向 verification |
