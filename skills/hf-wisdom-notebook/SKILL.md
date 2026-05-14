---
name: hf-wisdom-notebook
description: Use when an `hf-test-driven-dev` task completes and per-task delta must be appended to the feature-level cross-task knowledge notebook; when `hf-workflow-router` needs to inject wisdom summary into the next handoff; when `hf-completion-gate` needs to verify notebook completeness before closeout. Not for review verdicts (use `hf-*-review`); not for closeout pack assembly (use `hf-finalize`); not a substitute for repo-level ADR (use `docs/decisions/`).
---

# HF Wisdom Notebook

跨 task 累积 feature 内的 learnings / decisions / issues / verification / problems 5 类知识。每 task 完成时由 `hf-test-driven-dev` 写 delta；`hf-workflow-router` 在选下一个 active task 时把摘要注入下游 handoff；`hf-completion-gate` 在 closeout 前校验 notebook 完整性。

不替代仓库级 ADR；不替代 review record；不替代 closeout pack。

## When to Use

适用：

- `hf-test-driven-dev` 完成一个 task，需要追加 delta（FR-002 强制）
- `hf-workflow-router` 选下一 active task 前，需要把近 N task 的 wisdom 摘要注入 handoff
- `hf-completion-gate` 在 closeout 前调用 `validate-wisdom-notebook.py` 校验

不适用：

- task 内 review verdict / 决议 → 对应 `hf-*-review` skill 写 review record
- 仓库级架构决策 → `docs/decisions/ADR-NNN-*.md`（轻量 task 级决议在 notebook decisions.md，仓库级跨 feature 决议在 ADR pool）
- closeout 包装 → `hf-finalize`
- 上游路由不清 → `hf-workflow-router`

## Hard Gates

- task 完成必须写 delta（除非该 task 是纯 wording 修订且无新 learning，需在 progress.md 显式声明 `wisdom-skip: <task-id> reason: ...`）
- 不写任何 verdict 等价物（不写"task 通过 / review 通过 / gate 通过"等结论性判断）
- 不替代 review record 给出独立 review verdict
- 5 文件容器一旦初始化即不可删除（仅追加；`problems.md` 可保持空骨架）
- 跨 feature 知识沉淀不在本 skill 范围（用 `docs/principles/` 或 `docs/decisions/`）

## Object Contract

- **Primary Object**: `features/<active>/notepads/{learnings,decisions,issues,verification,problems}.md` 5 文件集合 + 各 entry 的 schema-合规 delta
- **Frontend Input Object**: 单 task 完成时的实现要点 + 测试结果 + 可选的架构选择 / 问题 / 阻塞项
- **Backend Output Object**:
  1. notebook delta（按 schema 追加段）
  2. `progress.md` `## Wisdom Delta` 段的引用行（"TASK-NNN: learnings/learn-NNNN + ..."）
- **Object Boundaries**:
  - 不写 review verdict / approval / gate verdict
  - 不修改其它 feature 的 notepads
  - 不替代 closeout pack 的 evidence 索引（finalize 仍负责 closeout 自己的 pack）
- **Object Invariants**:
  - 5 文件名不可变
  - entry-id 全局递增不重用（如 `learn-0001` / `learn-0002`...）
  - delta 仅追加不删改（除非 review 阶段发现错误且记录 amendment 段）

## Methodology

| 方法 | 落地步骤 |
|---|---|
| **Cross-task Knowledge Accumulation** | Workflow 步骤 1-3：识别要写的 file → 按 schema 追加 entry |
| **Append-only Audit Trail** | Hard Gates "5 文件容器不可删除" + Object Invariants "delta 仅追加" |
| **Schema-Validated Persistence** | Workflow 步骤 4：调用 `scripts/validate-wisdom-notebook.py` 即时校验 |
| **Handoff Summary Injection** | Workflow 步骤 5：往 `progress.md` 写引用行供 router 消费 |

详细 schema：`references/notebook-schema.md`；每 task 写入 protocol：`references/notebook-update-protocol.md`。

## Workflow

1. **读取当前 feature notepads 状态**
   - Object: 5 文件存在性
   - Method: file existence check
   - Input: feature 路径（默认 `features/<active>/notepads/`）
   - Output: 文件清单 + 各文件最大 entry-id
   - Stop / continue: 5 文件全在 → 继续步骤 2；否则进步骤 1A 创建空骨架

1A. **首次 task 创建空骨架**（仅当 step 1 发现 notepads/ 缺失或不全）
   - 创建 5 个 markdown 文件，每个含 `# <Title>` + 简短说明 + 空段
   - 不写任何 entry；entry-id 计数从 0001 开始

2. **识别要写的 file**
   - Object: 当前 task 类型 → 要 touch 的文件集合
   - Method: 按 task 类型映射（FR-002 强制：每 task 至少 learnings 或 verification 任一）
   - Input: task ID + task outcome
   - Output: 要写的 file 列表
   - Stop / continue: 至少 1 个文件 → 继续；0 个 → 必须在 progress.md 写 `wisdom-skip` 声明

3. **按 schema 追加 entry**
   - Object: 各文件的新 entry
   - Method: 按 `references/notebook-schema.md` 字段表填写
   - Input: task 实现细节 / 测试结果 / 决策点 / 问题
   - Output: 追加段 + 分配 entry-id
   - Stop / continue: schema 字段齐全 → 继续；否则补全

4. **即时校验**
   - Object: 5 文件 schema 合规性
   - Method: `python3 skills/hf-wisdom-notebook/scripts/validate-wisdom-notebook.py --feature <feature-dir>`
   - Input: feature 路径
   - Output: PASS / FAIL + 具体问题
   - Stop / continue: PASS → 继续；FAIL → 修正 entry

5. **写 progress.md `## Wisdom Delta` 段**
   - Object: feature 级 progress 的 wisdom 引用
   - Method: 追加一行 `| TASK-NNN | <file>/<entry-id> + <file>/<entry-id> ... |`
   - Input: 步骤 3 分配的 entry-id
   - Output: progress.md 更新
   - Stop / continue: router 在选下一 task 时按 wisdom-summary 注入协议消费此段

## Output Contract

每 task 完成时本 skill 必产出：

| 工件 | 路径 | schema |
|---|---|---|
| 5 文件容器（首次 task）| `features/<active>/notepads/{5 files}.md` | `references/notebook-schema.md` |
| Per-task delta | 同上文件追加段 | 同上 |
| progress.md Wisdom Delta 行 | `features/<active>/progress.md` `## Wisdom Delta` | progress.md schema（v0.6 新增） |

## Red Flags

- 试图把 review verdict 写进 notepads（违反 Hard Gates）
- 跨 feature 复制 entry（违反 Object Boundaries）
- 修改已有 entry 而不写 amendment 段（违反 append-only）
- 在 fast lane 下跳过写 delta（fast lane escape #4：problems.md status=open 时必须 escape，但跳过写 delta 本身是 escape #1 "方向 / 取舍 / 标准不清"的同款违规）

## Common Mistakes

| 错误 | 问题 | 修复 |
|---|---|---|
| `learnings.md` 写成"task 实现日志" | 失去跨 task 复用价值 | 只写"可被下 N 个 task 复用的 pattern / convention" |
| `decisions.md` 与 ADR 重复 | 浪费 token | task 级决策走 notebook，跨 feature 走 ADR；二者通过 `related-adr` 字段联系 |
| `problems.md` 用作 issues backlog | 触发不必要的 fast lane escape | open problem 必须真正阻塞 task；其它待办去 `issues.md` deferred |
| 跳过 entry-id 编号 | 破坏 append-only audit trail | 严格递增；从最大已存在 ID +1 |

## Common Rationalizations

| 借口 | 反驳 / Hard rule |
|---|---|
| "task 太小不值得写 learnings。" | Hard Gates: 至少要写 verification.md 一条记录测试结果，二选一不是可省略；纯 wording 修订例外需在 progress.md 写 `wisdom-skip` 显式声明，不能默默跳过。 |
| "decisions 应该走 ADR，不写 notebook decisions.md。" | Object Boundaries: notebook decisions 是 task 级（影响下 N 个 task 实现选择），ADR 是仓库级（影响整 feature / 整 release）；二者不互斥，通过 `related-adr` 字段联系。 |
| "fast lane 下没空写 notebook，等 closeout 时一起补。" | ADR-009 D2: notebook 不在 fast lane 可压缩项中；不写 notebook = task 未完成 = router 无法选下一 task。 |
| "我顺手把上个 task 的 entry 改一下措辞。" | Object Invariants: append-only；改措辞要走 amendment 段（在原 entry 下追加 `## amendment` 子段 + 新 entry-id），不修改已有 entry 文本。 |

## Reference Guide

| 文件 | 用途 |
|---|---|
| `references/notebook-schema.md` | 5 文件 schema 字段表 + 字段语义 + 例子 |
| `references/notebook-update-protocol.md` | 单 task 完成时的写 delta 详细 protocol（含 fast lane 下的 audit trail 同步） |
| `scripts/validate-wisdom-notebook.py` | stdlib python 校验器；hf-completion-gate 调用；详见自身 `--help` |

## Verification

- [ ] 5 文件容器存在
- [ ] 当前 task 已写入至少 1 条 delta（learnings 或 verification）
- [ ] 所有 entry 有唯一 entry-id
- [ ] `validate-wisdom-notebook.py` 跑过 PASS
- [ ] `progress.md` `## Wisdom Delta` 段已加入对应行
- [ ] 未写任何 verdict / approval 等价物
