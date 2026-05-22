# 任务计划模板

## 保存路径

默认：`features/<active>/tasks.md`

若 项目声明了任务计划路径映射，优先使用映射路径。

## 默认结构

```markdown
# <主题> 任务计划

- 状态: 草稿
- 主题: <主题>

## 1. 概述
## 2. 里程碑
## 3. 文件 / 工件影响图
## 4. 需求与设计追溯
## 5. 任务拆解

### T1. <任务名>
- 目标:
- Acceptance:
- 依赖:
- Ready When:
- 初始队列状态:
- Selection Priority:
- Files / 触碰工件:
- 测试设计种子:
- Verify:
- 预期证据:
- 完成条件:

## 6. 依赖与关键路径
## 7. 完成定义与验证策略
## 8. 当前活跃任务选择规则
## 9. 任务队列投影视图 / Task Board Path
## 10. 风险与顺序说明
```

## 编写要求

- 不把任务计划写成设计文档副本
- 不把里程碑标题当成真实任务
- 关键任务具备冷启动可执行性
- 关键任务能追溯回规格与设计
- 每个关键任务都要能回答“完成时什么必须为真”
- 每个关键任务都要能回答“如何验证”与“会触碰哪些文件/工件”
- 每个任务都能回答"做完的证据是什么"
- 每个关键任务都要显式标注 `Risk Tag` 与 `Risk Tag Rationale`（v0.7 新增；详见下节）

## Risk Tag 判定（v0.7 新增）

每个 task 必须固化一个 `Risk Tag`，由作者写入、`hf-tasks-review` 批准时固化。runtime 不允许 reviewer / implementer 自降自升；如需变更回 `hf-tasks` 或 `hf-increment`。

| Risk Tag | 触发信号（满足任一即建议升档） |
|---|---|
| `trivial` | 单文件改动 ≤ ~50 行；不触碰已批准接口契约；不触碰跨模块公共边界；不引入新依赖；不触碰 ADR / 设计已声明的不变量；不触碰 UI surface；测试设计种子能用 ≤ 2 个测试覆盖 |
| `high-risk` | 触碰已批准接口契约 / ADR / 公共模块边界；跨 ≥ 2 模块；触碰认证 / 数据迁移 / 状态机切换 / 安全敏感面；spec 标 high-risk 区；触碰 UI surface 中 forbidden drift 监控段 |
| `standard` | 其余情形（默认） |

不同 Risk Tag 对应的 per-task 评审链路由 router 在 `hf-test-driven-dev` 之后选定（详见 `hf-workflow-router/references/profile-node-and-transition-map.md` 的 `Risk Tag 链路` 章节）：

| Risk Tag | per-task 链路 |
|---|---|
| `trivial` | TDD → `hf-regression-gate` → `hf-completion-gate (per-task)` |
| `standard` | TDD → `hf-task-review` → `hf-regression-gate` → `hf-completion-gate (per-task)` |
| `high-risk` | TDD → `hf-task-review` → `hf-code-review`（深审） → `hf-regression-gate` → `hf-completion-gate (per-task)` |

`lightweight` profile 不接受 `high-risk`；遇到必须先升级到 `standard` profile。

`Risk Tag Rationale` 写不出充分理由时，作者应给更保守的档（向上靠）；reviewer 在 `hf-tasks-review` 检查"给低档的理由是否站得住"。

## 状态同步

- 任务计划状态字段（如 `状态: 草稿`）
- 主题或范围标识
- 当前活跃任务选择规则
- 可供评审定位的章节结构
- feature `progress.md`（默认 `features/<active>/progress.md`）中的 `Current Stage: hf-tasks`
- feature `progress.md` 中的 `Next Action Or Recommended Skill: hf-tasks-review`
