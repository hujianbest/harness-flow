# HF 热修复复现与同步记录模板

这个模板用于记录一次 `hf-hotfix` 的关键闭环：

- 当前问题是否真的是 hotfix，而不是 increment / blocked
- 问题是如何被定义和复现的
- 修复做了什么最小改动
- 如何验证修复已经生效
- 哪些工件需要同步刷新
- 下一步应该进入哪个质量动作或实现阶段

## 使用原则

- 热修复记录要偏操作闭环，不要写成长篇事故报告。
- 先固定“这是 hotfix 而不是 increment”的判断，再继续复现和边界收敛。
- 重点是“先复现、再修复、再验证、再同步”，每一步都留下最小但足够的证据。
- 只要热修复改变了用户可见行为、设计假设、任务状态或验证依据，就应记录同步项。
- 若 task-progress / worktree / 既有契约证据冲突，先阻塞并回 `hf-workflow-router`，不要伪造 hotfix handoff。
- 对紧急问题可以先写简版，但不能省略复现方式、修复边界和唯一下一步。

## 建议使用时机

- 用户明确要求紧急修复问题
- 修复已经开始进入验证链条
- 热修复后需要回写规格、设计、任务、状态或发布说明

## 标准记录模板

```markdown
## 热修复摘要

- 问题：
- 当前判断：`confirmed-hotfix` | `more-like-increment` | `blocked`
- 影响范围：
- 紧急级别：critical | high | medium

## 证据基线

- 合同 / 回归证明：
- `Current Stage`：
- `Current Active Task`：
- `Pending Reviews And Gates`：
- `Worktree Path`：
- `Worktree Branch`：

## 复现信息

- 期望行为：
- 实际行为：
- 复现方式：
- 失败证据：

## 修复范围

- 最小改动内容：
- 未纳入本次修复的内容：
- 根因信心：`demonstrated` | `probable`

## 验证结果

- 复现路径是否已通过：
- 补充测试：
- 额外验证：

## 同步项

### 规格 / 设计 / 任务

- 是否需要同步：
- 同步内容：

### 发布说明 / 状态记录

- 是否需要同步：
- 同步内容：

## 风险与状态同步

- 剩余风险：
- 是否需要后续补强：
- `Current Stage`：
- `Current Active Task`：
- `Pending Reviews And Gates`：

## 下一步

写出唯一 canonical 下一步动作或 skill，例如：`hf-test-driven-dev` | `hf-increment` | `hf-workflow-router` | `hf-regression-gate` | `hf-completion-gate`
```

## 简化版模板

对于时间非常紧的场景，可以先使用这个版本：

```markdown
## 热修复摘要

- 问题：
- 影响：
- 当前判断：

## 证据基线

- 条目

## 复现方式

- 条目

## 修复范围

- 条目

## 验证 / 状态同步

- 条目

## 下一步

写出唯一 canonical 下一步动作或 skill，例如：`hf-test-driven-dev` | `hf-increment` | `hf-workflow-router` | `hf-regression-gate` | `hf-completion-gate`
```

## 评审提示

记录时优先回答这些问题：

- 这个问题是否真的被稳定复现过？
- 当前问题是否真能证明“原本应成立的行为被破坏了”？
- 修复是否足够小，避免顺手引入无关改动？
- 修复后的验证是否真的覆盖了原故障路径？
- 本次修复是否暴露出规格、设计、任务或发布说明已经失真？
- 修复后是否还需要补经验固化、追溯性评审或进一步回归？

## 常见遗漏

- 问题没有被真正复现，只是“猜测修好了”
- 其实更像需求变化，却被误写成 hotfix
- 修复范围混入了无关清理或重构
- 只验证主路径，没有确认原故障路径
- 行为已经改变，但规格、设计或发布说明没同步
- 热修复做完就直接宣称完成，跳过质量链条

## 示例骨架

```markdown
## 热修复摘要

- 问题：登录接口在空 token 场景下触发 500
- 当前判断：`confirmed-hotfix`
- 影响范围：匿名请求、网关重试流量
- 紧急级别：high

## 证据基线

- 合同 / 回归证明：既有鉴权契约要求无 token 请求返回 401，而不是 500
- `Current Stage`：`hf-hotfix`
- `Current Active Task`：T18
- `Pending Reviews And Gates`：`hf-regression-gate`, `hf-completion-gate`
- `Worktree Path`：`<path-if-any>`
- `Worktree Branch`：`hotfix/T18-auth-null-token`

## 复现信息

- 期望行为：返回 401 或明确错误提示
- 实际行为：抛出未处理异常，返回 500
- 复现方式：构造空 token 请求调用登录校验接口
- 失败证据：接口日志、失败测试、错误栈

## 修复范围

- 最小改动内容：补充空 token 判断并统一错误返回
- 未纳入本次修复的内容：认证模块整体错误码整理
- 根因信心：`demonstrated`

## 验证结果

- 复现路径是否已通过：是
- 补充测试：空 token、缺失 token、非法 token
- 额外验证：相关匿名请求链路回归

## 同步项

### 规格 / 设计 / 任务

- 是否需要同步：是
- 同步内容：设计中补充匿名请求错误处理说明；任务记录补充异常路径覆盖

### 发布说明 / 状态记录

- 是否需要同步：是
- 同步内容：记录接口异常修复与当前热修复状态

## 风险与状态同步

- 剩余风险：其他认证入口可能存在相同空值问题
- 是否需要后续补强：需在其他认证入口排查是否存在相同的空值分支遗漏
- `Current Stage`：`hf-regression-gate`
- `Current Active Task`：T18
- `Pending Reviews And Gates`：`hf-regression-gate`, `hf-completion-gate`

## 下一步

`hf-regression-gate`
```
