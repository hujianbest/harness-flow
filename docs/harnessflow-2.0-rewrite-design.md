# HarnessFlow 2.0 Rewrite Design

- Status: draft
- Date: 2026-06-03
- Scope: 用 `addyosmani/agent-skills` 的 skill 设计理念反推 HarnessFlow 2.0 的完整重写蓝图
- Primary sources:
  - `https://github.com/addyosmani/agent-skills`
  - `https://raw.githubusercontent.com/addyosmani/agent-skills/main/skills/using-agent-skills/SKILL.md`
  - `https://raw.githubusercontent.com/addyosmani/agent-skills/main/docs/skill-anatomy.md`
  - `https://addyosmani.com/blog/agent-skills/`
  - `docs/principles/soul.md`
  - `docs/principles/skill-anatomy.md`
  - `skills/using-hf-workflow/SKILL.md`
  - `skills/hf-workflow-router/SKILL.md`

## 1. Executive Thesis

HarnessFlow 2.0 应完全重写 skill pack 的表达层，但不能重写掉 HF 的控制面资产。

`agent-skills` 的核心价值不是某个具体流程，而是它把 senior engineer 的隐性纪律变成可逐步执行、可验证、可渐进加载的 Markdown workflow。它的 `using-agent-skills` 是轻量 meta-skill：负责发现、分类、注入共同操作规则，并把任务交给 lifecycle skills。它不是运行时状态机，也不负责恢复进度、签发 verdict 或维护长期 workflow state。

HF 2.0 应吸收这种轻量、清晰、过程优先的 skill anatomy，同时保留并强化 HF 1.x 的差异化能力：

1. 工件驱动的冷启动恢复。
2. `using-hf-workflow` 与 `hf-workflow-router` 的双层控制面。
3. `Workflow Profile`、`Execution Mode`、`Workspace Isolation` 的正交决策。
4. Fagan-style author/reviewer 分离。
5. review、gate、approval、closeout 的结构化证据链。
6. Markdown-only 可移植性，runtime sidecar 只能是可选增强。

一句话：HF 2.0 不是把所有节点合成一个更大的 `using-agent-skills`，而是把每个 HF 节点写得像 `agent-skills` 一样短、硬、可执行，同时让 router/state/gate 继续承担 HF 的 workflow authority。

## 2. What `agent-skills` Gets Right

### 2.1 Skills are workflows, not essays

`agent-skills` 反复强调：skill 不是参考文档，而是 agent 要执行的工作流。一个好 skill 应包含触发条件、步骤、停止条件、反合理化、红旗和验证清单。HF 2.0 的每个 `SKILL.md` 也应从“说明某个理念”改为“让 agent 现在知道怎么做下一步”。

Implication for HF 2.0:

- 删除概念性长段落，把方法论压缩为执行步骤。
- 把长 rubric、schema、template 下沉到 `references/`。
- 主文件只保留会影响 agent 行为的内容。

### 2.2 Anti-rationalization is a control surface

`agent-skills` 的反合理化表不是装饰，而是直接防止 agent 用漂亮话跳过流程。HF 1.x 已经引入 `Common Rationalizations`，但 2.0 应进一步标准化：

- 每个节点至少覆盖 3 类逃逸借口：跳过上游、跳过证据、扩大范围。
- 反驳必须指向本节点 hard gate 或 shared convention。
- 反合理化内容不重复写成哲学，应写成“如果你想这样做，正确动作是 X”。

### 2.3 Verification is the exit criterion

`agent-skills` 的每个 skill 以 evidence 结束：测试输出、build 输出、runtime 数据、review 结论。HF 2.0 应把这一点做得更机器可读：

- authoring 节点输出 artifact path。
- implementation 节点输出 RED/GREEN/REFACTOR fresh evidence。
- review 节点输出 structured verdict record。
- gate 节点输出 evidence-bundle verdict。
- finalize 输出 closeout pack 与 HTML companion。

### 2.4 Progressive disclosure keeps skills usable

`agent-skills` 不把 20 多个 skill 全塞进上下文，而是用 `using-agent-skills` 决定当下该加载什么。HF 2.0 应保持同一原则，但要区分两类 disclosure：

- Skill discovery disclosure: 入口层识别该进入哪个 family/node。
- Runtime recovery disclosure: router 只读取决定当前节点所需的最少工件。

这要求 HF 2.0 的 `SKILL.md` 更短，router references 更结构化，review/gate record 更稳定。

### 2.5 Commands are entry aids, not the workflow

`agent-skills` 的 slash commands 是 thin wrappers：`/spec` 调 spec skill，`/build` 调 incremental + TDD skill。HF 2.0 应继续使用更严格的原则：command is bias, not authority。命令不能绕过 router、profile、approval、review 或 gate。

## 3. The `using-agent-skills` Relationship Model

`using-agent-skills` 与其他 skills 的关系可以概括为四层：

| Layer | In `agent-skills` | Responsibility | HF 2.0 interpretation |
|---|---|---|---|
| Meta-skill | `using-agent-skills` | 识别任务类型，选择 skill，定义共同操作规则 | `using-hf-workflow` 负责 public entry；不要承担 runtime FSM |
| Lifecycle skill | `spec-driven-development`, `test-driven-development`, etc. | 执行某一类工程工作流 | `hf-specify`, `hf-design`, `hf-tasks`, `hf-test-driven-dev`, review/gate nodes |
| Command | `/spec`, `/build`, etc. | 快速把用户意图映射到 skill | HF commands 只表达 bias；Cursor 走自然语言 |
| Supporting references | `references/*.md`, docs | 按需加载深资料 | HF `references/`, `evals/`, `scripts/` |

关键洞察：

1. `using-agent-skills` 是 meta-skill，不是 mega-skill。
2. 它提供共同纪律，但不复制每个 lifecycle skill 的流程。
3. 它允许多个 skills 顺序或组合应用，但不维护长期状态。
4. 它的判断依据主要是任务语义，不是磁盘上的 workflow evidence。

HF 2.0 因此应避免两个错误：

- 把 `using-hf-workflow` 写成包含所有 transition map 的大路由器。
- 把 `hf-workflow-router` 简化成 `using-agent-skills` 风格的任务分类器。

正确边界：

- `using-hf-workflow`: public entry, command bias, direct invoke vs route-first。
- `hf-workflow-router`: runtime authority, evidence recovery, profile/mode/isolation, canonical next node。

## 4. HF 2.0 Design Principles

### P1. Markdown pack remains the product

HF 2.0 的一等交付物仍是可被 Claude Code、Cursor、OpenCode 和其他 agent 读取的 Markdown skill pack。任何 runtime sidecar、hook、CLI 或 script 都只能增强，不得成为主链必需条件。

### P2. Control plane is explicit

HF 2.0 必须把控制面写成可审计结构，而不是散落在 skill prose 中：

- entry policy
- route policy
- transition map
- shared verdict vocabulary
- progress schema
- approval record contract
- review/gate return contract

### P3. Leaf skills cannot self-route

每个 leaf skill 只能完成自己的 primary object。它可以输出 handoff 建议，但不能自己决定跨节点跳转、profile 降级、review 通过或 gate 通过。

### P4. Evidence beats confidence

HF 2.0 的所有“完成”都必须能从磁盘工件恢复。聊天上下文、口头确认、旧日志、模型自信都不能成为推进依据。

### P5. Small files, strong contracts

每个 `SKILL.md` 目标是 250-450 行；超过预算的内容下沉。短不是为了简陋，而是为了让 agent 在上下文压力下仍能执行正确动作。

### P6. Reviews and gates stay separate

Review 判断 artifact 或实现质量；gate 判断证据是否足以推进。2.0 不允许用一个“quality skill”合并二者。

## 5. Target Architecture

```text
commands/ or natural-language intent
        |
        v
skills/using-hf-workflow
        |
        | direct invoke when node is clear and legal
        | route-first when evidence/recovery/profile is involved
        v
skills/hf-workflow-router
        |
        | reads progress + reviews + verification + task board
        v
canonical node
        |
        +-- authoring nodes: discovery/spec/design/ui/tasks
        +-- implementation nodes: test-driven-dev/subagent-driven-dev
        +-- review nodes: hf-reviewer + review skill
        +-- gate nodes: regression/doc-freshness/completion
        +-- branch nodes: hotfix/increment
        +-- finalize/release nodes
```

### 5.1 Layers

| Layer | Owns | Does not own |
|---|---|---|
| Public entry | user intent classification, command bias, minimal direct invoke | runtime recovery, profile transition map |
| Runtime router | profile/mode/isolation, canonical next node, recovery | authoring content, review findings |
| Leaf workflow | one primary object and one output object | global state authority |
| Reviewer agent | independent findings and verdict records | implementation fixes |
| Gate | evidence sufficiency verdict | missing evidence fabrication |
| Runtime sidecar | optional atomic tools, schema validation, context hooks | verdicts, approvals, architectural decisions |

## 6. HF 2.0 Skill Taxonomy

HF 2.0 should keep the family shape but rename and document roles consistently.

| Role | Keep / rewrite | 2.0 purpose |
|---|---|---|
| Public Entry | Rewrite | Minimal meta-skill inspired by `using-agent-skills`; only entry classification and kickoff |
| Router | Rewrite | Deterministic evidence router; references hold machine-ish tables |
| Discovery | Rewrite | Product thesis, wedge, probe; stops before formal spec |
| Authoring | Rewrite | `spec`, `design`, `ui-design`, `tasks` as artifact transformers |
| Implementation | Rewrite | TDD per active task; subagent optional; fresh evidence mandatory |
| Review | Rewrite | Thin, rubric-driven review nodes dispatched through `hf-reviewer` |
| Gate | Rewrite | Evidence sufficiency nodes with structured verdicts |
| Branch | Rewrite | Hotfix/increment re-entry without corrupting main state |
| Context/Wisdom | Consolidate | Support router and implementation, not standalone ceremony |
| Release | Keep standalone | Tag-readiness pack only; no deployment claims |

2.0 should reduce surface area where roles overlap. If two skills share the same primary object and output object, merge or demote one into a reference.

## 7. Skill Anatomy 2.0

Every `skills/<name>/SKILL.md` should use this structure:

```text
---
name: <directory-name>
description: <classifier: use when / not for>
---

# <Skill Title>

1-2 sentence responsibility statement.

## When to Use
Positive triggers, negative triggers, adjacent-skill boundary.

## Hard Gates
Non-negotiable stop conditions.

## Object Contract
Primary object, input object, output object, ownership boundary.

## Workflow
Numbered steps. Each step states input, action, output, stop rule.

## Output Contract
Exact artifact/record/handoff shape.

## Red Flags
Observable signs of misuse.

## Common Rationalizations
Excuse -> correction.

## Verification
Evidence checklist.

## Reference Guide
Only links to optional deeper material.
```

Differences from `agent-skills`:

- HF keeps `Object Contract` because workflow recovery depends on knowing what each node transforms.
- HF keeps `Hard Gates` because review/gate/approval cannot be reduced to generic verification.
- HF keeps `Output Contract` because downstream router consumes records.

Differences from HF 1.x:

- `Methodology` becomes optional unless it changes execution.
- Long historical context moves to docs/ADR, not skill body.
- Transition rules move out of leaf skills and into router references.
- Repeated cross-cutting principles move into shared conventions.

## 8. State and Artifact Model

HF 2.0 should move from prose-first Markdown state toward dual-readable artifacts:

| Artifact | Human-readable | Machine-readable recommendation |
|---|---|---|
| `progress.md` | Status snapshot and links | `progress.json` sidecar or fenced canonical block |
| `tasks.md` | Approved task plan | `tasks.progress.json` for active/ready/done |
| review records | Findings and rationale | frontmatter or JSON block with verdict fields |
| gate records | Evidence bundle and conclusion | canonical verdict block |
| approvals | Human or auto approval rationale | canonical approval fields |
| evidence | Logs, screenshots, commands | metadata: command/action, timestamp, git ref |

Minimum canonical fields:

- `current_stage`
- `workflow_profile`
- `execution_mode`
- `workspace_isolation`
- `current_active_task`
- `pending_reviews_and_gates`
- `next_action_or_recommended_skill`
- `last_verdict`
- `record_paths`
- `git_ref`

Markdown remains the source humans review. Structured blocks exist so routers, scripts and runtime sidecars can validate without rereading prose.

## 9. Routing Model 2.0

### 9.1 Public entry decision

`using-hf-workflow` returns only:

1. `direct invoke <leaf>` when the user asks for a clear standalone node and all prerequisites are visible.
2. `route-first hf-workflow-router` when state, evidence, profile, recovery, branch, review, gate or task continuation is involved.

It must not:

- read broad code context;
- mutate progress;
- consume review verdicts;
- choose profile;
- appear in runtime handoff.

### 9.2 Runtime router decision

`hf-workflow-router` owns:

- active feature detection;
- evidence freshness check;
- profile selection;
- execution mode;
- workspace isolation;
- branch signal detection;
- transition map lookup;
- review/gate recovery;
- task reselection after completion gate.

Router output should be a compact block:

```text
Current Stage:
Workflow Profile:
Execution Mode:
Workspace Isolation:
Target Skill:
Why:
Required Input Artifacts:
Expected Output Record:
```

### 9.3 Determinism target

Given the same artifact bundle and user intent, router must choose the same canonical next node. If it cannot, the correct output is `blocked` or upstream clarification, not best-effort execution.

## 10. Review and Gate Model

HF 2.0 should keep Fagan separation, but make review records thinner by default.

### Review node contract

- Runs in fresh context or `hf-reviewer`.
- Reads the target artifact plus declared context only.
- Produces findings with severity.
- Produces exactly one verdict: `通过`, `需修改`, `阻塞`.
- Writes `record_path`.
- Sets `reroute_via_router` when the next step is not local.

### Gate node contract

- Consumes evidence bundle.
- Refuses stale or missing evidence.
- Does not create missing evidence.
- Produces verdict and next action.
- Can pass with thin record only when evidence is complete and no finding matters.

### Thin records

2.0 should default to thin records for pass cases:

- verdict;
- evidence anchors;
- checked scope;
- next action.

Expanded diagnosis is required only for `需修改`, `阻塞`, stale evidence, route conflict, profile mismatch or critical findings.

## 11. Commands and Client Integration

HF 2.0 should keep seven stable command intents but document them as client-neutral:

| Intent | Command | Meaning |
|---|---|---|
| enter/resume | `/hf` | start with entry shell and route from artifacts |
| specify | `/spec` | bias toward spec authoring |
| plan | `/plan` | bias toward design/tasks |
| build | `/build` | bias toward current active task implementation |
| review | `/review` | bias toward review/gate recovery |
| closeout | `/ship` | bias toward completion/finalize |
| release | `/release` | direct standalone release readiness pack |

Rules:

- Commands never bypass evidence.
- Cursor and clients without slash commands use natural language with identical semantics.
- Command definitions live in top-level `commands/`.
- Client adapters only install or expose commands; they do not redefine workflow policy.

## 12. Runtime Sidecar Boundary

HF 2.0 may introduce or consume optional runtime support, but the boundary is strict:

Allowed:

- schema validation;
- atomic progress writes;
- evidence recording;
- hash-checked file edits;
- context-window recovery;
- skill anatomy audits;
- router fixture tests.

Forbidden:

- writing approval verdicts;
- writing review/gate verdicts;
- silently changing profile;
- auto-skipping hard stops;
- making OpenCode-only behavior required for Cursor or Claude Code.

This keeps HF portable while allowing stronger execution in hosts that support runtime hooks.

## 13. Migration Plan

### Phase 0: Freeze contracts before rewriting prose

Deliverables:

- `workflow-shared-conventions.md` 2.0 schema.
- transition map 2.0.
- skill anatomy 2.0 reference.
- review/gate return contract 2.0.
- audit script expectations.

Exit criteria:

- Existing workflows can still be routed from old artifacts.
- New fields have read-time normalization rules.

### Phase 1: Rewrite control plane

Rewrite:

- `using-hf-workflow`
- `hf-workflow-router`
- router references
- command docs

Exit criteria:

- cold session entry fixtures pass;
- direct invoke vs route-first fixtures pass;
- review/gate recovery fixtures pass.

### Phase 2: Rewrite authoring chain

Rewrite:

- product discovery
- specify
- spec review
- design
- UI design/review
- tasks/tasks review

Exit criteria:

- one feature can progress from idea to approved tasks using only artifacts.
- every approval writes a record.

### Phase 3: Rewrite implementation chain

Rewrite:

- test-driven-dev
- subagent-driven-dev
- test/code/traceability reviews
- browser testing activation
- wisdom/context support

Exit criteria:

- one active task completes RED/GREEN/REFACTOR with fresh evidence.
- review chain can reject stale or incomplete evidence.

### Phase 4: Rewrite gates and closeout

Rewrite:

- regression gate
- doc freshness gate
- completion gate
- finalize
- release standalone pack

Exit criteria:

- completion gate can either select a unique next task or enter finalize.
- finalize produces `closeout.md` and `closeout.html`.
- release remains tag-readiness only.

### Phase 5: Conformance fixtures

Create fixtures for:

- no feature yet;
- approved spec but missing design approval;
- implementation done but stale evidence;
- review pass with next gate;
- completion pass with another ready task;
- completion pass with no remaining task;
- hotfix and increment re-entry;
- release candidate with incomplete closeout.

Exit criteria:

- fixture runner reports deterministic target skill for each case.
- anatomy audit passes for every rewritten skill.

## 14. Non-Goals

HF 2.0 must not:

- become a deployment, monitoring, rollback or incident-response framework;
- require a runtime sidecar to run the main workflow;
- merge all lifecycle behavior into one mega-skill;
- let implementation nodes self-approve;
- make `auto` mean skipping approvals, reviews or gates;
- replace artifacts with chat memory;
- add personas that bypass `hf-reviewer` contracts.

## 15. Acceptance Criteria for the Rewrite

The 2.0 rewrite is successful when:

1. A cold agent can enter from `using-hf-workflow`, read artifacts, and reach one canonical next node.
2. Every state-changing node writes a durable artifact or record.
3. Every review/gate has a structured verdict and record path.
4. `SKILL.md` files are shorter, more action-oriented, and pass anatomy audit.
5. Long references are loaded only when needed.
6. The same command intent behaves consistently across Claude Code, Cursor and OpenCode.
7. A full fixture workflow proves: idea -> spec -> design -> tasks -> TDD task -> reviews -> gates -> closeout.
8. Release remains a readiness pack, not deployment.

## 16. Open Design Decisions

These should be decided before implementation:

1. Should 2.0 introduce `progress.json` as authoritative, or keep `progress.md` authoritative with canonical fenced blocks?
2. Should old 1.x artifacts be migrated in place, or normalized read-only by router until touched?
3. Should `hf-context-mesh`, `hf-gap-analyzer`, and `hf-wisdom-notebook` remain standalone skills or become router/implementation references?
4. Should pass-case thin records be mandatory, or only recommended?
5. Should the audit script become blocking for 2.0 PRs?
6. Should `hf-release` stay outside the router forever, or enter a separate release-tier router with no dependency on main-chain FSM?

## 17. Recommended First Rewrite Slice

Start with the smallest slice that proves the design:

```text
using-hf-workflow
  -> hf-workflow-router
  -> hf-specify
  -> hf-spec-review
  -> approval record
  -> hf-design
```

Why this slice:

- exercises public entry vs runtime routing;
- proves artifact-driven recovery before implementation complexity;
- validates review separation;
- keeps runtime sidecar unnecessary;
- creates the pattern all later nodes can copy.

Do not start with implementation or ultrawork. If the control plane is unclear, faster implementation will only create faster drift.
