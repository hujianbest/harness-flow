# Wisdom Notebook 5-File Schema

> 5 文件强 schema，承载 feature 内跨 task 知识沉淀。每 task 完成时由 `hf-test-driven-dev` 按此 schema 追加 delta；`hf-workflow-router` / `hf-completion-gate` 消费摘要。

## 文件清单（不可变）

| 文件 | 触发时机 | 必需 |
|---|---|---|
| `learnings.md` | 每 task 至少 1 条（与 `verification.md` 二选一） | yes |
| `decisions.md` | 仅当 task 内做出影响后续 task 的架构性选择 | conditional |
| `issues.md` | task 内遇到非阻塞问题（阻塞问题走 `problems.md`） | conditional |
| `verification.md` | 每 task 至少 1 条（与 `learnings.md` 二选一） | yes |
| `problems.md` | 仅当 task 出现 escape-route 必要的阻塞问题（fast lane escape #4 触发） | conditional |

5 文件作为容器**必须存在**（首次 task 创建空骨架）；**conditional** 文件若 task 内未触发对应条件，保留空骨架不写 entry。

## 通用文件结构

```markdown
# <File Title> — Feature <feature-id>

> 跨 task 累积，按 task 时间倒序追加（最新的 entry 在最上面）。

## TASK-<id> — <YYYY-MM-DDTHH:MMZ> — <task title>

- entry-id: `<file-prefix>-<NNNN>`
- author: <agent / session 标识>
- (具体 schema 字段...)

---

## TASK-<id-next> — ...
```

`<file-prefix>` 约定：`learn` / `dec` / `iss` / `verify` / `prob`。

## 5 文件字段表

### `learnings.md`

| 字段 | 类型 | 必需 | 语义 |
|---|---|---|---|
| `entry-id` | string `learn-NNNN` | yes | 全局递增，不重用 |
| `author` | string | yes | agent / session 标识 |
| `pattern` | string | yes | 可被下 N 个 task 复用的 pattern / convention 摘要 |
| `applies-to` | string | yes | 哪些下游 task / 场景能复用此 pattern |
| `evidence-anchor` | string | yes | 指向具体证据（test 路径 / commit / verification entry-id） |
| `tags` | comma-separated string | no | 便于 router wisdom-summary 筛选 |
| `related-decisions` | comma-separated `dec-NNNN` | no | 关联 decisions.md entry |

### `decisions.md`

| 字段 | 类型 | 必需 | 语义 |
|---|---|---|---|
| `entry-id` | string `dec-NNNN` | yes | 全局递增 |
| `author` | string | yes | — |
| `decision` | string | yes | 一句话决议 |
| `alternatives-considered` | bullet list | yes | 至少 2 个备选 + 拒绝理由 |
| `rationale` | paragraph | yes | 选择理由（与 spec / design / ADR 关联） |
| `reversibility` | enum `low/medium/high` | yes | 改回成本 |
| `related-adr` | string | no | 仓库级 ADR ID（如 `ADR-008`） |

### `issues.md`

| 字段 | 类型 | 必需 | 语义 |
|---|---|---|---|
| `entry-id` | string `iss-NNNN` | yes | — |
| `author` | string | yes | — |
| `problem` | string | yes | 一句话问题描述 |
| `status` | enum `open/resolved/deferred` | yes | 状态 |
| `discovered-at` | ISO 8601 | yes | 发现时间 |
| `resolved-by` | string | conditional（status=resolved） | task ID / commit |
| `resolved-at` | ISO 8601 | conditional | — |
| `workaround` | string | no | 临时绕过方法 |

### `verification.md`

| 字段 | 类型 | 必需 | 语义 |
|---|---|---|---|
| `entry-id` | string `verify-NNNN` | yes | — |
| `author` | string | yes | — |
| `test-name` | string | yes | 测试入口 / 命令 |
| `result` | enum `pass/fail/partial` | yes | — |
| `evidence-path` | string | yes | log / shell 输出位置 |
| `coverage-pct` | string | no | 行 / 行为覆盖估算 |
| `runtime-tier` | enum `unit/integration/e2e` | no | — |

### `problems.md`

| 字段 | 类型 | 必需 | 语义 |
|---|---|---|---|
| `entry-id` | string `prob-NNNN` | yes | — |
| `author` | string | yes | — |
| `problem` | string | yes | 一句话阻塞描述 |
| `status` | string `open` | yes | 写入 problems.md 即 status=open；resolved 后迁移到 issues.md status=resolved 不留 problems.md 行 |
| `severity` | enum `blocker/critical` | yes | problems.md 仅写 blocker / critical；其它 severity 走 issues.md |
| `blocks-task` | comma-separated TASK-NNN | yes | 当前被阻塞的 task ID |
| `escape-route` | string | yes | 触发 fast lane escape #4 后的应对方向 |
| `proposed-fix-by` | string | no | 建议哪个 task / 哪个 increment 修 |

## Entry-id 全局递增协议

- 每文件独立计数（learn-0001 / dec-0001 / iss-0001 不冲突）
- 跨 task 不重置（feature 内全局递增）
- 删除 / 改写不复用 ID
- 计算下一 ID：`max_existing(grep -oE '<prefix>-[0-9]+' notepads/<file>.md) + 1`

## Append-only + Amendment

如发现已有 entry 错误，**不**修改原文，而是在原 entry 下追加 amendment 子段 + 新 entry-id：

```markdown
## TASK-003 — 2026-05-13T14:00Z — original task

- entry-id: `learn-0007`
- author: ...
- pattern: ...

### amendment 2026-05-15T10:00Z

- amend-of: `learn-0007`
- new entry-id: `learn-0012`
- correction: <说明哪一段错了 + 新表述>
- amendment-author: ...
```

## 例子

参见 `features/002-omo-inspired-v0.6/notepads/` 全 5 文件的真实使用（dogfood）。
