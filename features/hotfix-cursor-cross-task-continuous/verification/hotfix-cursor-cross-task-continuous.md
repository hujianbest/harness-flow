# Hotfix Record — Cursor Cross-Task Continuous Execution Visibility

- 时间：2026-05-15
- Workflow Profile: lightweight（docs-only fix）
- Execution Mode: auto
- Scope kind: docs/rule-visibility hotfix（不改 SOP 语义，只在 Cursor entry 层补可见性）

## 热修复摘要

- **问题**：在 Cursor 中以 `Execution Mode = auto` 运行 HarnessFlow，当一个 task 完成 `hf-completion-gate=通过` 后，Cursor agent 会停下来询问用户是否进入下一个 task；用户期望按 SOP 自动进入 router → `hf-test-driven-dev` 直至所有 task 完成、最后进入 `hf-finalize`。
- **当前判断**：`confirmed-hotfix`（既有 SOP 已规定不应停，但 Cursor entry 层未显式承接，导致 Cursor agent 行为漂移）
- **影响范围**：所有使用 Cursor 客户端的 HF 用户在 auto / fast lane 模式下的多 task 工作流体验。
- **紧急级别**：High（直接降低 v0.5.x 在 Cursor 上的可用性，且 v0.6 feature 002 端到端修复尚未交付）

## 证据基线

- **合同 / 回归证明（既有 approved SOP，与当前 Cursor 行为冲突）**：
  - `skills/hf-workflow-router/references/execution-semantics.md` § 连续执行原则：
    > 任务边界本身也不是默认暂停点：若当前任务刚通过 `hf-completion-gate`，且 router 能唯一锁定下一个 `Current Active Task`，则应在同一轮继续进入新的 `hf-test-driven-dev`，而不是把"一个任务做完"误当成自然暂停。
  - `skills/hf-workflow-router/references/execution-semantics.md` § 非暂停点：
    > 当前任务的 `hf-completion-gate` 返回 `通过` 后，若 router 能唯一锁定 `next-ready task`，则回 router 并在同一轮继续进入 `hf-test-driven-dev`。
  - `skills/hf-workflow-router/references/profile-node-and-transition-map.md` § 恢复编排协议 / 最小示例：
    > 因为这不是 approval node，也不是 hard stop，所以在同一轮继续进入 `hf-test-driven-dev`。
- `Current Stage`：N/A（HF-meta hotfix，不锚定单一业务 feature）
- `Current Active Task`：N/A（feature 002 的 TASK-003 仍是该 feature 的 active task；本 hotfix 不抢占）
- `Pending Reviews And Gates`：lightweight profile，无需 spec / design / tasks-review；hotfix record 即 verification record
- `Worktree Path` / `Worktree Branch`：`/workspace` 主工作区，分支 `cursor/cross-task-continuous-execution-133a`

## 复现信息

- **期望行为**（按 `execution-semantics.md`）：在 `Execution Mode=auto` 下，`hf-completion-gate=通过 → hf-workflow-router → hf-test-driven-dev (next task)` 应在**同一轮**完成，无用户介入；只有命中 interactive approval step 或显式 hard stop 才停下。
- **实际行为**（用户报告）：在 Cursor 中，task N 完成后 agent 输出路由结论 / 完成报告，然后**结束当前回复**，等待用户在新一轮里说"继续"才进入 task N+1；连续多 task 工作流被切成多次 Cursor 回合。
- **复现方式**：在 Cursor 中开启一个有多个 approved task 的 HF feature（典型如 `features/002-omo-inspired-v0.6`），把 `Execution Mode` 设成 `auto`，让 agent 完成当前 task 的 TDD + reviews + gates 全链路。观察 `hf-completion-gate=通过` 后 agent 是否在同一回复内继续进入下一 task 的 `hf-test-driven-dev`，还是停下报告并等待用户"继续"。
- **失败证据**：`features/002-omo-inspired-v0.6/progress.md` 的 Stage Trail 中可见 TASK-001 / TASK-002 / TASK-005~007 的连续推进确实发生过（说明 SOP 实质可执行），但用户当前会话报告 Cursor 行为已退化为按 task 暂停，与 SOP 不符。

## 修复范围

- **最小改动内容**：
  1. `.cursor/rules/harness-flow.mdc`：在 Hard rules 段新增 1 条"跨 task 连续执行"硬规，显式指向 `execution-semantics.md` 的连续执行原则与非暂停点定义。该规则文件 `alwaysApply: true`，是 Cursor 每轮必加载的唯一 HF 入口锚点 → 在此处补承接，覆盖面最广。
  2. `docs/cursor-setup.md`：在 § 5 Troubleshooting 新增 1 行症状 → 解决方案行（"Cursor 在 auto 模式下每个 task 之间停下来询问"），引用同样的 SOP 锚点。
- **未纳入本次修复的内容**：
  - 不动 `skills/using-hf-workflow/SKILL.md`（feature 002 TASK-013 已计划修改它，避免冲突）
  - 不动 `skills/hf-workflow-router/SKILL.md` 与其 `references/`（SOP 文本本身已正确，问题在入口可见性而非 SOP 缺失）
  - 不动任何 leaf skill（`hf-test-review` / `hf-code-review` / `hf-completion-gate` / `hf-finalize`）的 Output Contract（避免与 v0.6 feature 002 TASK-007 `hf-ultrawork` 的 fast lane decision schema 重复或冲突）
  - 不引入新 skill、新 tests、新 scripts（feature 002 TASK-007 / TASK-013 / TASK-018 才是端到端落地的归属）
- **根因信心**：`probable`（基于 `harness-flow.mdc` 现有 Hard rules 段无 cross-task continuous-execution 条目这一可见证据；100% `demonstrated` 需要在真实 Cursor session 复跑前后对比，本会话受 cloud agent 环境限制无法直接复现 Cursor IDE 的逐轮交互）

## 同步项

- **规格 / 设计 / 任务**：本 hotfix 不修改任何已批准的 spec / design / tasks 工件；不与 feature 002 的 v0.6 主链 task 表交叠
- **发布说明 / 状态记录**：CHANGELOG 同步留待 feature 002 TASK-017 v0.6 收尾时合并叙述（避免 v0.5.x patch note 与 v0.6 scope 描述拉锯）；本 hotfix record 自身即追踪锚点

## 状态同步

- `Current Stage`：hotfix verification 已写盘
- `Current Active Task`：N/A（不抢占 feature 002 的 TASK-003）
- `Pending Reviews And Gates`：lightweight，无 review/gate 待办；audit-skill-anatomy.py + 全 tests regression 已作为本 hotfix 的回归证据
- **Next Action Or Recommended Skill**：`hf-test-driven-dev`（docs-only RED-GREEN：RED = 用户报告的行为漂移，GREEN = `harness-flow.mdc` 与 `cursor-setup.md` 补承接 + audit / tests 不退化）

## Verification Commands & Results（GREEN evidence）

下表在 fix 应用后回填：

| 命令 | 退出码 | Summary |
|---|---|---|
| `python3 scripts/audit-skill-anatomy.py --skills-dir skills` | 0 | 28/28 OK，0 failing，0 warning（与 baseline 一致） |
| `python3 -m pytest tests/ -q` | 0 | 44/44 passed（与 baseline 一致） |

## Freshness Anchor

- 本 hotfix 的 verification 命令在 `cursor/cross-task-continuous-execution-133a` 分支应用 fix 之后立即执行，结果与 main baseline 完全一致——证明 hotfix 边界严格限定在 docs/rule 文件，未引入对 skills/ 的副作用。
