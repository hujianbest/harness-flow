---
name: using-mwf-workflow
description: Use when a new session needs to enter the mwf workflow for an AR / DTS / change request, when the user expresses a generic intent like "继续这个 AR" / "开始处理这个缺陷" / "做规格澄清" / "做 AR 设计" / "做 TDD" / "做 review" without confirming the canonical mwf node, or when deciding direct invoke vs route-first for a single mwf-* skill. Not for runtime recovery or profile decisions (→ mwf-workflow-router), not when already inside a leaf skill (→ continue current skill), not for product discovery (mwf does not own product discovery — escalate to product owner).
---

# Using mwf Workflow

`mdc-workflow` (mwf) skill family 的 **public entry**。本 skill 在新会话或意图模糊时帮助决定：

- `direct invoke`：当前节点已经明确，且工件证据稳定 → 直接进入对应 `mwf-*` leaf skill
- `route-first`：阶段 / profile / 证据不稳定 → 交给 `mwf-workflow-router` 做权威路由

本 skill 不做 authoritative routing，不替 `mwf-workflow-router` 决定 profile / execution mode；不做团队角色拍板（模块架构师 / 开发负责人 / 开发人员的判断不能被入口接管）。

## When to Use

适用：

- 新会话不确定从哪进入 mwf
- 用户说"继续"/"推进"/"开始做"但当前节点未确认
- 用户提出 `/mwf-*` 命令意图但是否能直接落到 leaf skill 仍不清
- 需判断 direct invoke 还是 route-first
- 用户表达 `auto mode` 偏好但还没确定交给哪个节点

不适用 → 直接走对应入口：

- 已在某个 leaf skill 内部 → 继续当前 skill
- 需要 authoritative routing / profile 判断 / review 派发 → `mwf-workflow-router`
- 仍在做产品发现 / 决定要不要做这个 AR → 回需求负责人，mwf 不承担产品发现

## Hard Gates

- 不替 `mwf-workflow-router` 做 profile / execution mode / canonical 节点的最终决定
- 不替模块架构师、开发负责人、开发人员拍板任何专业判断
- 不把本 skill 写进 `Next Action Or Recommended Skill`
- direct invoke 仅在节点明确 + 工件证据稳定时才允许；任一不满足 → route-first

## Object Contract

- Primary Object: 用户意图分类结果（`direct invoke` / `route-first`）
- Frontend Input Object: 用户原始请求 + `/mwf-*` 命令偏好 + 当前 work item 锚点（如有）
- Backend Output Object: 进入合法 leaf skill 的 minimal kickoff 或交给 `mwf-workflow-router`
- Transformation: 把模糊意图分类为两条路径之一
- Boundaries: 不读取大量代码 / 不做 routing 决定 / 不修改任何工件
- Invariants: 输出永远是两类之一，且不会自我递归地把 `using-mwf-workflow` 写进 handoff

## Methodology

- **Front Controller Pattern**：作为统一入口，识别意图后分发，不内嵌 router 状态机
- **Evidence-Based Dispatch**：仅做最小必要工件检查（progress.md 是否存在、work item 类型是否清晰），不展开全量探查
- **Separation Of Concerns**：入口层只负责分流，不做 authoritative routing 或工件修改
- **Team Role Discipline（mwf-soul）**：本 skill 不替团队角色拍板；遇到需要专业判断的请求，告诉用户 mwf 的协作边界并把工程化执行交给对应 leaf skill 或 router

## Workflow

### 1. 判断 entry vs runtime recovery

入口（继续本 skill）适用：新会话、高层意图、命令偏好、direct vs route 决策。
runtime recovery（交给 router）适用：review / gate 刚完成、evidence 冲突、需要切支线、需要消费 gate 结论 → 直接 `mwf-workflow-router`。本 skill 不做 runtime 编排。

### 2. 识别主意图

把请求归到下表之一；归不出来或同时落在 ≥2 个候选 → route-first。

| 用户意图 | 默认偏向 leaf |
|---|---|
| 澄清需求 / 整理 AR 规格 | `mwf-specify` |
| 评审需求规格 | `mwf-spec-review` |
| 写 / 修组件实现设计 | `mwf-component-design` |
| 评审组件实现设计 | `mwf-component-design-review` |
| 写 / 修 AR 实现设计（含测试设计章节） | `mwf-ar-design` |
| 评审 AR 实现设计 | `mwf-ar-design-review` |
| TDD 实现 / 改代码 | `mwf-tdd-implementation` |
| TDD 后审查测试用例有效性 | `mwf-test-checker` |
| C / C++ 代码检视 | `mwf-code-review` |
| 判断能否完成 / completion gate | `mwf-completion-gate` |
| 收口 / closeout / handoff | `mwf-finalize` |
| 紧急缺陷 / hotfix 复现与根因 | `mwf-problem-fix` |

不明确时统一回退 `mwf-workflow-router`。

### 3. 提取 Execution Mode 偏好

用户说 `auto mode` / `自动执行` / `不用等我确认` → 视为 Execution Mode 偏好，原样向下游传递；本 skill 不归一化为 canonical 字段。`auto` 不是跳过 review / gate / approval 的理由，也不是 direct invoke 的充分条件。

### 4. 判断是否允许 direct invoke

同时满足才可：

- 候选节点唯一
- 请求明确属于该节点职责
- 必要工件可读（如：进入 `mwf-ar-design` 至少需要 `requirement.md` 已存在）
- 没有 profile / route / 证据冲突
- Execution Mode 偏好已记录可传递

任一不满足 → route-first 交给 `mwf-workflow-router`。

### 4A. 单事实分流检查点

如果只差 **1 个关键事实**就能稳定判断 direct invoke vs route-first，先问 1 个最小判别问题，再继续。典型适用：只差「这是 AR 还是 DTS」、只差「组件实现设计是否需要修订」、只差「AR 实现设计是否已通过 review」。

不适用：需要 ≥2 个事实、工件互相冲突、涉及 profile 升级（component-impact / hotfix / lightweight）、涉及跨组件协调。任一命中 → 直接 route-first。

### 5. 命令当作 bias，不当作 authority

| 命令 | 默认偏向 |
|---|---|
| `/mwf-spec` | `mwf-specify` |
| `/mwf-design` | `mwf-ar-design` |
| `/mwf-component-design` | `mwf-component-design` |
| `/mwf-build` / `/mwf-tdd` | `mwf-tdd-implementation` |
| `/mwf-test-check` | `mwf-test-checker` |
| `/mwf-code-review` | `mwf-code-review` |
| `/mwf-completion` | `mwf-completion-gate` |
| `/mwf-finalize` / `/mwf-closeout` | `mwf-finalize` |
| `/mwf-hotfix` / `/mwf-problem-fix` | `mwf-problem-fix` |
| `/mwf-route` | `mwf-workflow-router` |

命令不替代工件检查；命令偏好与工件证据冲突时一律 route-first。

### 6. 正确结束

输出只有两类：

1. 进入合法 mwf-* leaf skill 的最小 kickoff
2. 立即转交 `mwf-workflow-router`

唯一确定下一步时用 3 行编号快路径：

```text
1. Entry Classification: direct invoke | route-first
2. Target Skill: <canonical mwf-* 节点名>
3. Why: <1-2 条决定性证据>
```

`direct invoke` 时，3 行之后**同一回复**继续追加目标 leaf skill 的最小 kickoff（第 1 步动作 / 最小 intake），不再等一轮「要不要继续」。`route-first` 时，只说明「为什么不能 direct invoke」，立即转交 `mwf-workflow-router`，不展开 transition map、不做 review recovery、不把 `using-mwf-workflow` 写进 handoff。

## Output Contract

- 输出永远是两类之一：
  1. 进入合法 `mwf-*` leaf skill 并执行其第 1 步
  2. 把控制权交给 `mwf-workflow-router`
- 不修改任何工件
- 不把 `using-mwf-workflow` 写进 handoff

## Red Flags

- 把 `using-mwf-workflow` 写成完整 routing 状态机
- 路由不清却硬做 direct invoke
- 因为用户报命令名就跳过工件检查
- review / gate 完成后仍在做恢复编排（应交 router）
- 把本 skill 写进 `Next Action Or Recommended Skill`
- 替模块架构师、开发负责人、开发人员拍板

## Common Mistakes

| 错误 | 修复 |
|---|---|
| 用户说「我要做这个 AR」就直接进入 `mwf-tdd-implementation` | 先确认是否有 AR 实现设计；缺则进入 `mwf-ar-design` |
| 把产品发现请求强行分类成 mwf 节点 | 告知 mwf 不承担产品发现，回需求负责人 |
| 命令是 `/mwf-build` 但工件还停留在规格阶段 | route-first，让 router 决定 |

## Verification

- [ ] 已识别 entry vs runtime recovery
- [ ] 已分类 direct invoke vs route-first
- [ ] 单事实分流检查点（如适用）已使用
- [ ] clear case 使用 3 行编号快路径
- [ ] direct invoke 时已在同一回复进入 target leaf skill 的最小 kickoff
- [ ] route-first 时已立即转交 `mwf-workflow-router`
- [ ] Execution Mode 偏好已记录可传递
- [ ] 未把本 skill 写入 handoff

## Supporting References

| 文件 | 用途 |
|---|---|
| `skills/docs/mwf-workflow-shared-conventions.md` | mwf 工件路径、canonical 字段、handoff 字段、profile 与节点对应表 |
| `mwf-workflow-router/SKILL.md` | authoritative runtime routing |
| `docs/mwf-principles/00 soul.md` | mwf soul / 角色边界 |
| `docs/mwf-principles/04 workflow-architecture.md` | profile 与主链路 |
