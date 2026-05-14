# HF v0.6 OMO-Inspired — Design

- 状态: 草稿（2026-05-13；spec Round 2 approved 2026-05-13）
- 主题: 把 spec.md Round 2 的 15 FR + 7 NFR 翻译成可拆任务的 design：4 新 skill 的 SKILL.md schema + 7 修改 skill 的具体改法 + 7 OQ 收口 + 工件 schema + fast lane 机制
- 关联：spec.md Round 2 / ADR-008 / ADR-009 / ADR-010

## 1. 设计驱动因素提取

从 spec.md Round 2 提取的设计驱动：

- **D-001（首要）**：HF 自身是 *markdown skill pack*，不是软件系统；本 feature 不需要 DDD Strategic / Tactical Modeling、C4 视图、STRIDE 威胁建模——按 `hf-design/SKILL.md` "架构复杂度匹配团队规模和系统规模"原则与 read-on-presence 语义，跳过这些重型方法。"系统视图" 由 SKILL.md 之间的 handoff / route 关系替代。
- **D-002**：v0.6 范围内的 11 个 SKILL.md 改动必须 100% 通过 `audit-skill-anatomy.py`（NFR-001），意味着每个新 skill 都要符合 anatomy v2：必含 `## Common Rationalizations`、不含独立 `## 和其他 Skill 的区别`、frontmatter 仅 `name` + `description`、正文结构按 skill-anatomy.md `Canonical skeleton`
- **D-003**：fast lane 的 markdown-only 路径 + Fagan + gate 不可绕过的纪律组合（ADR-009 D2 + spec FR-008）决定了 `hf-ultrawork/SKILL.md` 必须把不可压缩 5 类项放在 `Hard Gates` 段直接 enumerate
- **D-004**：跨客户端可移植（ADR-008 D1 + spec NFR-004）决定了 `hf-context-mesh` 不能写死单客户端 AGENTS.md 加载语义；3 套模板优先
- **D-005**：HYP-002（Blocking）"markdown-only fast lane 是否可用"决定了 hf-ultrawork 的实现机制必须依赖 host agent 自觉读取 SKILL.md + 工件，不能假设 host 提供 hook
- **D-006**：spec.md 的 7 OQ 必须在本 design 阶段全部收口给出明确决议，否则 hf-tasks 无法拆任务

## 2. 整体架构（基于 SKILL.md handoff 拓扑）

v0.6 改动后的 HF skill family 拓扑（仅画出本 feature 涉及的 11 个 skill 与其新增 / 变化的边）：

```
                              架构师 explicit opt-in
                                       │
                                       ▼
                       using-hf-workflow (修改: step 5 新增一行)
                                       │
                          ┌────────────┴───────────────┐
                          │                            │
                  standard mode 路径                fast lane 路径 (新)
                          │                            │
                          ▼                            ▼
              hf-workflow-router         ┌─── hf-ultrawork (新)
              (修改: step-level recovery │      │
              + category_hint handoff   │      │ escape (任一命中)
              + wisdom_summary 注入)     │      └─── 回到架构师
                          │              │
                          ▼              │
              ┌──────── 各 hf-* 节点 ────────┴───┐
              │                                   │
       hf-specify (修改: Interview FSM)     hf-tasks-review (修改: momus 4 维 + N=3 loop)
              │                                   │
              ▼                                   ▼
       (前置 self-check) hf-gap-analyzer (新)  ...
              │                                   │
              ▼                                   │
       <artifact>.gap-notes.md ─── 作者吸收 ──→ 标准 review chain
                                                  │
                                                  ▼
                                  hf-test-driven-dev (修改: Output Contract 引 wisdom-notebook)
                                                  │
                                                  ▼
                              hf-wisdom-notebook (新；5 文件 schema + delta protocol)
                                                  │
                                                  ▼
                                  hf-completion-gate (修改: 校验 wisdom-notebook delta)
                                                  │
                                                  ▼
                                   ... hf-finalize（不改）

              (旁路) hf-context-mesh (新)：宿主项目 AGENTS.md 一键生成器
              (旁路) hf-code-review (修改: 新增 ai-slop-rubric.md)
```

## 3. 4 新 skill 的 SKILL.md 详细设计

### 3.1 `skills/hf-wisdom-notebook/`

**Skill 类型**：Technique + Reference
**Anatomy v2 子目录**：`SKILL.md` + `references/` + `evals/`（高风险）+ `scripts/`（含 `validate-wisdom-notebook.py`，OQ 收口见 §5.7）

**Frontmatter**：
```yaml
---
name: hf-wisdom-notebook
description: Use when a TDD task completes and per-task delta must be appended to feature-level cross-task knowledge; when hf-workflow-router needs to inject wisdom summary into next handoff; when hf-completion-gate needs to verify notebook completeness. Not for review verdicts (use hf-*-review), not for closeout pack assembly (use hf-finalize).
---
```

**Object Contract**：
- Primary Object: `features/<active>/notepads/{learnings,decisions,issues,verification,problems}.md` 5 文件集合
- Frontend Input Object: 单 task 完成时的实现要点（learnings）+ 测试结果（verification）+ 可选的架构选择（decisions）/ 问题（issues / problems）
- Backend Output Object: notebook delta（按 §3.1 schema 追加段）
- Object Boundaries: 不写 verdict、不写 review 结论、不替代 closeout pack

**5 文件 schema（OQ-001 收口）**：

每个文件统一格式：

```markdown
# <File Title> — Feature <feature-id>

> 跨 task 累积，按 task 时间倒序追加

## TASK-<id> — <YYYY-MM-DDTHH:MMZ> — <task title>

- entry-id: <文件名简码>-<NNNN>（如 `learn-0003`）
- author: <agent / session 标识>
- (具体 schema 字段，见下表)

---

(下一条 entry...)
```

| 文件 | 必需字段 | 可选字段 | 触发时机 |
|---|---|---|---|
| `learnings.md` | `pattern` / `applies-to` / `evidence-anchor` | `tags`, `related-decisions` | 每 task 至少 1 条（与 verification.md 二选一） |
| `decisions.md` | `decision` / `alternatives-considered` / `rationale` / `reversibility` | `related-adr`（如指向 docs/decisions/ADR-NNN） | 仅当 task 内做出影响后续 task 的架构性选择时 |
| `issues.md` | `problem` / `status`（`open` / `resolved` / `deferred`） / `discovered-at` | `resolved-by`, `resolved-at`, `workaround` | task 内遇到的非阻塞问题（阻塞问题走 problems.md） |
| `verification.md` | `test-name` / `result`（`pass` / `fail` / `partial`） / `evidence-path` | `coverage-pct`, `runtime-tier` | 每 task 至少 1 条（与 learnings.md 二选一） |
| `problems.md` | `problem` / `status=open` / `severity` / `blocks-task`（task ID list） / `escape-route` | `proposed-fix-by` | 当 task 出现 escape-route 必要的阻塞问题（直接触发 fast lane escape） |

**5 文件容器约束（FR-002）**：首次 task 创建时 5 文件全部以骨架（仅 `# Title` + 空段）形式落盘，后续 task 按需追加。

**Workflow（5 步）**：
1. 读取 feature 当前 notepads（若不存在则创建 5 文件骨架）
2. 根据 task 类型识别要写的 file（learnings / verification 必至少一；其它按需）
3. 按 schema 追加 entry，分配 entry-id
4. 调用 `validate-wisdom-notebook.py`（路径见 §5.7）做即时校验
5. 在 progress.md `## Wisdom Delta` 段追加引用（"TASK-NNN: learnings/learn-0003 + verification/verify-0007"）

**Hard Gates**：
- task 完成必须写 delta（除非 task 是文档级修订 + 无新 learning）
- 不写 verdict 等价物
- 不替代 review record

**Common Rationalizations**：
| 借口 | 反驳 |
|---|---|
| "task 太小不值得写 learnings" | hard rule: 至少要写 verification.md 一条记录测试结果，二选一不是可省略 |
| "decisions 应该走 ADR" | hard rule: notebook decisions 是 task 内决策（影响下 task），ADR 是仓库级决策（影响全 feature / 全 release）；二者不互斥 |
| "fast lane 下没空写 notebook" | ADR-009 D2: notebook 不在 fast lane 可压缩项中；不写 notebook 等价于 escape 触发 |

### 3.2 `skills/hf-gap-analyzer/`

**Skill 类型**：Technique
**Anatomy v2 子目录**：`SKILL.md` + `references/`（中风险，evals 可选）

**Frontmatter**：
```yaml
---
name: hf-gap-analyzer
description: Use when an authoring artifact (spec / design / tasks) draft is complete and the author wants to surface implicit assumptions, AI slop, missing acceptance criteria, or unaddressed edge cases BEFORE submitting to the corresponding Fagan review. Not a review node (does not produce verdict), not a substitute for hf-spec-review / hf-design-review / hf-tasks-review.
---
```

**Object Contract**：
- Primary Object: `<artifact>.gap-notes.md`（与 artifact 平级；如 `features/<f>/spec.md.gap-notes.md`）
- Frontend Input: 作者自己刚写完的草稿
- Backend Output: gap-notes 文件，作者吸收/驳回后清空或归档
- Boundaries: 不写 verdict、不修改 artifact 本身

**gap rubric（references/gap-rubric.md）**：

| 维度 | 检查项 | 典型问题 |
|---|---|---|
| Implicit Intent | 作者脑里有但没写下来的目标 / 假设 | "我想这样但没说为啥不那样" |
| AI Slop | 生成式语言痕迹（冗余形容词 / 解释性自然语言注释 / em-dash / "simply" / "obviously"） | 复用 `hf-code-review/references/ai-slop-rubric.md` 的禁用模式列表 |
| Missing Acceptance | FR / NFR 缺 testable acceptance | "应该正确处理" |
| Unaddressed Edge Cases | 主路径写完但 negative path / boundary / concurrent / failure mode 没写 | 缺 timeout / retry / rollback / 并发 / 权限差异 |
| Scope Creep | 当前轮范围有但 spec 已声明 out-of-scope | 写了 v0.7 runtime 的事 |
| Dangling Reference | 引用了不存在的 ADR / 文件 / 节点 | "见 ADR-099"（不存在） |

**Workflow（4 步）**：
1. Read artifact + 项目 spec 约定 + ADR 列表
2. 按 6 维度 rubric 扫描，输出 finding 列表（每条带 anchor + suggested treat）
3. 写 `<artifact>.gap-notes.md`（作者主导吸收 / 驳回，不强制）
4. 作者吸收后**显式标记**每条 finding 为 `accepted` / `rejected-with-reason`，再提交对应 review

**Output Contract**：gap-notes 文件作为 review 的辅助上下文（review 节点会读但不强制作为 verdict 依据）

### 3.3 `skills/hf-context-mesh/`

**Skill 类型**：Technique + Reference
**Anatomy v2 子目录**：`SKILL.md` + `references/`（含 3 套客户端模板）；evals 可选；scripts 可选

**Frontmatter**：
```yaml
---
name: hf-context-mesh
description: Use when a host project (vendoring HF) wants per-directory hierarchical context (project root / mid-directory / leaf) auto-generated for any AI agent reading the codebase. Not for HF's own docs/principles/ (untouched), not for spec / design artifacts.
---
```

**3 套 AGENTS.md 模板（OQ-002 收口）**：

| 客户端 | 加载机制 | 模板特点 |
|---|---|---|
| **OpenCode** | `directoryAgentsInjector` hook 自动按目录注入 | 模板 frontmatter 用 OpenCode 兼容格式；可含 `# AGENTS.md` 标题 |
| **Cursor** | `.cursor/rules/*.mdc` 全局 alwaysApply rule + agent 主动 Read | 模板用 `.mdc` frontmatter（`alwaysApply: false` + `globs: <dir>/**`），目录级触发 |
| **Claude Code** | `CLAUDE.md` 文件命名约定 | 模板需用 `CLAUDE.md` 文件名；同目录下与 OpenCode AGENTS.md 共存（OpenCode 不读 CLAUDE.md，反之亦然） |

**模板文件**（`references/agents-md-template.md` 内含 3 段）：

```markdown
## OpenCode `AGENTS.md` 模板（项目根 / 中层 / 叶子）

# AGENTS.md — <directory-purpose>

## Conventions
- ...

## Typical Patterns
- ...

## Anti-Patterns
- ...

## Cross-Skill Notes
- ...
```

类似 Cursor `.mdc` 段 + Claude Code `CLAUDE.md` 段（结构一致，仅 frontmatter 差异）

**Workflow（4 步）**：
1. 扫描宿主项目目录树，识别 3 类目录（root / mid / leaf）：root = 项目根；mid = 含 ≥ 2 子目录或 README.md 的目录；leaf = 仅含源文件的目录
2. 询问架构师"目标客户端"（OpenCode / Cursor / Claude Code / all 3）
3. 按选定客户端 + 目录层级生成对应模板
4. 让架构师填充 Conventions / Patterns / Anti-Patterns（HF 不替架构师写约定）

**Hard Gates**：
- 不替架构师写约定（按 soul.md 第 5 条）
- 不修改 HF 自身 `docs/principles/`

### 3.4 `skills/hf-ultrawork/`

**Skill 类型**：Technique + Pattern
**Anatomy v2 子目录**：`SKILL.md` + `references/`（含 fast-lane-escape-conditions.md）+ `evals/`（高风险，必含）

**Frontmatter**：
```yaml
---
name: hf-ultrawork
description: Use when architect explicitly opts into fast lane via 'auto mode' / 'ultrawork' / 'do not stop' keywords or features/<f>/README.md Metadata Execution Mode = auto. Not the default mode; not a review/gate skip mechanism. NEVER skip Fagan review verdicts, gate verdicts, approval-artifact disk writes, or Hard Gates 'stop on unclear standard' clauses.
---
```

**Object Contract**：
- Primary Object: 节点之间的"是否继续"自动决策权 + `progress.md` Fast Lane Decisions audit trail
- Frontend Input: 架构师 explicit opt-in 信号 + 当前节点的 verdict / output
- Backend Output: 自动 dispatch 下一节点 + audit trail 行
- Boundaries: 不写任何 verdict、不修改任何 review record、不替代 approval（只把 reviewer verdict 落到 approval 工件）

**Hard Gates（FR-008 强制 enumerate 5 类不可压缩项）**：

| 不可压缩项 | 原因 | 命中后行为 |
|---|---|---|
| 8 个 Fagan review 节点（hf-{discovery,spec,design,ui,tasks,test,code,traceability}-review） | author ≠ reviewer 是工程纪律的根 | 永远走完整 review 节点 |
| 3 个 gate verdict（hf-regression-gate / hf-doc-freshness-gate / hf-completion-gate） | gate 是独立质量判断 | 永远走完整 gate 节点 |
| `hf-finalize` 的 closeout pack 完整性（含 closeout HTML companion） | PMBOK-style handoff，不减项 | 永远走完整 finalize |
| spec / design / tasks approval 工件 | 即便 fast lane auto-APPROVED，工件**必须**落盘 | 自动写 approval record（含 fast lane decision 行） |
| 任何 SKILL.md `Hard Gates` 段命中"方向 / 取舍 / 标准不清" | soul.md 第 1 条硬纪律 | 强制 escape 抛回架构师 |

**fast lane 关键词集合（OQ-003 收口）**：

| 类别 | 关键词 |
|---|---|
| 显式启用 | `auto mode` / `ultrawork` / `ulw` / `自动执行` / `不要停下来` / `不用确认` / `自动跑完` / `auto run` / `keep going` / `proceed` / `continue` |
| 显式停下 | `停` / `暂停` / `wait` / `hold on` / `等等` / `stop` / `pause` / `先停` |
| 显式恢复 standard | `standard mode` / `恢复 standard` / `回到 standard` / `revert to standard` |

**escape conditions（references/fast-lane-escape-conditions.md，按 ADR-009 D3 第 4 项的 6 个信号）**：

1. 任一节点的 `Hard Gates` 命中"方向 / 取舍 / 标准不清"
2. 任一 review verdict = `阻塞`
3. 任一 gate verdict = FAIL
4. `hf-wisdom-notebook` 的 `problems.md` 出现新增 status=open 项
5. 连续 3 次同一节点 rewrite loop 仍未通过（与 hf-tasks-review N=3 上限对齐）
6. 架构师在会话中说显式停下关键词（见 §3.4 关键词集合）

**Workflow（5 步）**：
1. Detect architect explicit opt-in（关键词识别 + Metadata 字段）
2. Route to canonical next action without confirmation prompt（ router 仍是节点选择权威）
3. After each node verdict: check escape conditions → 命中即让出
4. After review verdict = 通过 + approval pending: auto-write approval record（含 fast lane decision 行）
5. Append to progress.md `## Fast Lane Decisions` audit trail

**HYP-002 实现机制**：markdown-only 路径下，hf-ultrawork 是**宣告式**（declarative）skill，依赖 host agent 自觉读取 SKILL.md + Hard Gates + escape conditions + 工件。不依赖 host hook。OpenCode 用户后续可挂 v0.7 runtime 的 todo-continuation-enforcer / ralph-loop hook 提升 idle 检测精度，但不是必需。

## 4. 7 修改 skill 的具体改法

### 4.1 `skills/hf-tasks-review/`（FR-005）

**新增** `references/momus-rubric.md`：

| 维度 | 阈值 | 评分定义 |
|---|---|---|
| **Clarity** | 100% | 100% 任务 ID / 描述 / Acceptance / Files / Verify 字段齐全；缺一字段即 0% |
| **Verification** | 90% | ≥ 90% 任务 Acceptance 是 PASS/FAIL 可机械判断（不允许 "应该" / "尽可能" 表述） |
| **Context** | 80% | ≥ 80% 任务有"参考实现锚点"（指向已有代码 / spec / design / 别的 task），剩余 ≤ 20% 可基于 design 直推 |
| **Big Picture** | 100% | 100% 任务能映射回 spec FR / NFR（traceability matrix），无悬空任务 |
| **Zero-tolerance** | 0% | 0 任务依赖未确认业务事实；0 critical red flag |

**SKILL.md 修改**：
- `Workflow` 步骤 4 (verdict) 表格新增一行：

| 条件 | verdict | 下一步 |
|---|---|---|
| 4 维全过 + 0% 零容忍 | `通过` | `任务真人确认` |
| 4 维差任一阈值，但属于 LLM-FIXABLE wording 类 | `rejected-rewrite` | `hf-tasks` Round N+1（N < 3）|
| 第 4 次 rejected-rewrite 仍未通过 | `阻塞` | 升级架构师（fast lane escape #5）|
| 任务结构有根本问题 | `阻塞` | `hf-tasks` |

- `Common Rationalizations` 新增一条："'momus 阈值太严，第 3 轮还差 1% 就通过吧' → hard rule: 阈值是 0/1 判断，差 1% 也是不达标；自动转 阻塞 升级架构师"

### 4.2 `skills/hf-specify/`（FR-006）

**新增** `references/interview-fsm.md` + `references/spec-intake-template.md`

**FSM 5 状态（OQ-005 收口：允许 ClearanceCheck → Research 回退）**：

```
Interview ──question──→ Research ──finding──→ ClearanceCheck
   ▲                                              │
   │                                              ├──(unclear)──→ Interview (next question)
   │                                              ├──(needs more research)──→ Research (loop)
   │                                              └──(all-clear)──→ PlanGeneration
   │                                                                       │
   └────────────────────(needs more clarification)─────────────────────────┘

PlanGeneration ──finalize──→ Output (spec.md draft)
```

**`spec.intake.md` schema**：

```markdown
# Spec Intake — <feature-id>

- Status: <Interview | Research | ClearanceCheck | PlanGeneration | Done>
- Last Question Asked: <question text or "n/a">
- Last Question Answered At: <timestamp or "pending">

## Question Trail

| # | Time | State Before | Question | Answer | State After |
|---|---|---|---|---|---|
| 1 | ... | Interview | "..." | "..." | Research |

## Research Trail

| # | Time | Topic | Source / File | Finding |

## Clearance Checks

| # | Time | Check | Result | Action |
```

**SKILL.md 修改**：Workflow 步骤新增"FSM 状态读取 / 写入"约束；不破坏现有 Socratic 步骤，只是把它们形式化。

### 4.3 `skills/hf-workflow-router/`（FR-003 + FR-015）

**修改** `references/profile-node-and-transition-map.md`：
- 新增"step-level recovery"段：从 `tasks.progress.json`（v0.6 新增的可选工件，由 hf-test-driven-dev 写入）恢复 task 内 RED/GREEN 步级
- 新增"category_hint"段：handoff JSON 增加可选字段 `category_hint`（取值如 `visual-engineering` / `deep` / `quick` / `ultrabrain`，对齐 OMO 类目体系），下游 host 不消费时直接忽略
- 新增"wisdom_summary 注入"段：在选 next active task 前从 `notepads/` 读取近 N=3 task 的 learnings + verification + open problems 摘要，注入下游 handoff

**修改** `references/workflow-shared-conventions.md`（FR-010）：
- 新增"progress.md schema"段，定义 `## Fast Lane Decisions` 段（OQ-006 收口：v0.6 不拆 progress.fast-lane.md，记入 instrumentation debt）
- schema 字段：`time` / `node` / `decision_type` / `decision_content` / `trigger_condition` / `escape_enabled`

### 4.4 `skills/hf-code-review/`（FR-011）

**新增** `references/ai-slop-rubric.md`（基于 OMO `comment-checker` 已验证模式）：

```markdown
# AI Slop Rubric（hf-code-review 子规则）

## 禁用模式（host 可 grep）

### 注释类
- `\b(simply|obviously|clearly|just|merely|moreover|furthermore|in fact|notably)\b`
- `// (Import the | Define the | Initialize the | Increment the | Return the)\s+\w+`
- em-dash `—` / en-dash `–`

### 代码类
- 解释性自然语言注释（描述代码做了什么，而不是为什么）
- 过度抽象（< 3 处使用的 abstract base class / interface）
- 命名漂移（同一概念在 2+ 处使用不同变量名）

## 检测命令（示例）

\`\`\`bash
git diff main..HEAD -- '*.ts' '*.py' '*.md' | rg -i '\b(simply|obviously|clearly)\b'
\`\`\`

## 例外

- 用户文档（README / docs/）允许 plain English
- 测试断言消息可含说明
```

**SKILL.md 修改**：在已有 "Comment 质量" 子节中加一句"按 `references/ai-slop-rubric.md` 跑 grep；命中即 finding"。

### 4.5 `skills/using-hf-workflow/`（FR-009）

**修改**：步骤 5 entry bias 表新增一行：

```
| 用户意图 | 可优先尝试 | 不明确时回退 |
|---|---|---|
| ...（既有行不变）... |
| Execution Mode = auto 且当前不在 review/gate 节点 + 满足 fast lane direct invoke 条件 | `hf-ultrawork`（direct invoke，**不**绕过 review/gate） | `hf-workflow-router` |
```

**步骤 3** 既有 Execution Mode preference 解析逻辑保持不变；**步骤 6** 命令 bias 表保持不变（不引入 `/ultrawork` 命令）。

### 4.6 `skills/hf-test-driven-dev/`（FR-002 集成点）

**修改**：`Output Contract` 段加一段：

```markdown
## Output Contract（v0.6 新增 wisdom-notebook 集成点）

每个 task 完成时（无论 fast lane 还是 standard mode）必须：

1. 5 个 notebook 文件作为容器存在（`features/<f>/notepads/{learnings,decisions,issues,verification,problems}.md`）；首次 task 创建空骨架
2. 至少在 `learnings.md` / `verification.md` 任一中追加 delta 段（按 `hf-wisdom-notebook` schema）
3. 在 `progress.md` `## Wisdom Delta` 段记录本 task 写入的 entry-id 列表
```

**Hard Gates** 段新增："不写 wisdom notebook delta = task 未完成"。

### 4.7 `skills/hf-completion-gate/`（FR-002 集成点）

**修改**：`Workflow` 段 closeout 前置检查新增一项：

```
- [ ] `validate-wisdom-notebook.py` 校验通过（5 文件容器齐全 + 每 task 至少有 learnings/verification delta）
```

校验失败 → gate verdict = FAIL，回到 hf-test-driven-dev 补 delta。

## 5. OQ 收口（spec §10）

| OQ | 决议 |
|---|---|
| OQ-001 wisdom-notebook 5 文件 schema 字段 | 见 §3.1 schema 表 |
| OQ-002 hf-context-mesh 三客户端模板 | 见 §3.3 三套模板 |
| OQ-003 hf-ultrawork 关键词集合 | 见 §3.4 关键词表 |
| OQ-004 N=3 是否浮动 | **统一 N=3 不浮动**（与 fast lane escape #5 对齐；rewrite loop 第 4 次自动升级架构师） |
| OQ-005 hf-specify FSM 是否允许回退 | **允许 ClearanceCheck → Research 回退 + ClearanceCheck → Interview 回退**；只禁止 PlanGeneration 之后回退（PlanGeneration 完成即冻结） |
| OQ-006 progress.md Fast Lane Decisions 是否拆出 | **本 feature 不拆**；记入 instrumentation debt，待 v0.6.x 评估若长 feature 该段 > 100 行再拆 progress.fast-lane.md |
| OQ-007 hf-ultrawork 是否一次性写完 | **一次性写完**；fast lane chicken-and-egg 不严重（本 feature 大部分节点不依赖 fast lane runtime 行为，hf-ultrawork SKILL.md 是宣告式文档） |

## 5.7 `validate-wisdom-notebook.py` 落点（FR-012）

按 ADR-006 D1 / D2 "skill-owned 优先于 repo-root" 原则：

**决定**：落到 `skills/hf-wisdom-notebook/scripts/validate-wisdom-notebook.py`，**不**落 repo-root `scripts/`。

理由：
- 它是 hf-wisdom-notebook 节点的 hard gate 工具（hf-completion-gate 调用），属于 skill-owned
- 与 `skills/hf-finalize/scripts/render-closeout-html.py` 同形态（v0.5.1 ADR-006 D2 已确立的 pattern）
- vendoring 时随 skill 一并搬运，不会丢

**接口**：

```
python3 skills/hf-wisdom-notebook/scripts/validate-wisdom-notebook.py [--feature <feature-dir>] [--strict]

stdout:
  PASS / FAIL
  [feature-dir] notepads/ has all 5 files: yes/no
  [feature-dir] task TASK-NNN has learnings/verification delta: yes/no
  ...

exit code:
  0 = PASS
  1 = FAIL (validation issue)
  2 = invalid args / IO error
```

**stdlib only**（NFR-005）；与 `audit-skill-anatomy.py` 同等约束。

## 6. 关键技术决策（ADR-on-presence）

本 feature 的关键决策已经在 ADR-008 / ADR-009 / ADR-010 锁定，不需要新 ADR。设计阶段决议（OQ 收口、schema 细节、文件落点）由本 design.md 直承，不开新 ADR。

例外：若 hf-design-review 提出"5 文件 schema 应该 SQLite 化"等结构性挑战，那才开新 ADR-011。

## 7. 风险与缓解（承接 spec §11）

| 风险 | 设计层缓解 |
|---|---|
| HYP-002 falsified | hf-ultrawork SKILL.md 包含 "若 host agent 在 markdown-only 路径下无法可靠遵守 escape conditions，应主动建议架构师切回 standard mode" 的 fallback 段；实际 hf-design-review 时关注此段是否可冷读 |
| 11 个 SKILL.md 总 token 超 25000 预算 | 本 design 设定每个新 SKILL.md 主体 < 3000 tokens（NFR-002 限制 5000 留余地）；超出时优先下沉到 references/ |
| 三客户端 hf-context-mesh 行为不一致 | §3.3 三套独立模板，互不依赖 |
| dogfood progress.md 巨大 | OQ-006 决议 v0.6 不拆，但 instrumentation debt 显式入档，post-feature 评估 |
| reviewer 在 momus rubric 下给分主观 | momus-rubric.md 含具体 0-100% 阈值定义，不留主观空间；OQ-004 决议 N=3 不浮动也降低主观调整空间 |

## 8. 不在本 design 解决的事

- v0.7 runtime 的具体 hashline / record-evidence / progress-store 实现细节（ADR-010 + 后续 v0.7 feature）
- v0.8 删除范围内的任何东西（ADR-008 D1 永久封禁）
- 既有 18 个未升级 skill 的任何变化
- v0.6 release 的 release-pack（待全部 task 完成 + closeout 后由 hf-release 处理）

## 9. 下一步

`hf-design-review` 通过 + design-approval 后进入 `hf-tasks` 拆任务。
