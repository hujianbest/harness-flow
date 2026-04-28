# Task Board 与队列投影

## 最小任务计划到 Task Board 示例

### 任务计划片段

```markdown
## 5. 任务拆解

### T1. 建立解析器骨架
- 目标: 补齐最小 parser 主路径
- 依赖: -
- Ready When: spec / design / tasks approval 已完成
- 初始队列状态: ready
- Selection Priority: P1
- 触碰工件: src/parser.ts, tests/parser.test.ts
- 测试设计种子: 主路径解析 + 非法输入失败
- 验证方式: npm test -- parser
- 预期证据: fail-first 失败记录 + parser tests 转绿
- 完成条件: parser 主路径通过，且实现交接块已写回

### T2. 接入 CLI 命令
- 目标: 让 CLI 调用 parser
- 依赖: T1
- Ready When: T1=done
- 初始队列状态: pending
- Selection Priority: P2
- 触碰工件: src/cli.ts, tests/cli.test.ts
- 测试设计种子: CLI 成功调用 + 参数缺失失败
- 验证方式: npm test -- cli
- 预期证据: CLI tests 转绿
- 完成条件: CLI 命令接入完成，且实现交接块已写回
```

### 对应 Task Board

```markdown
# Task Board

- Source Task Plan: features/003-parser/tasks.md
- Current Active Task: T1

## Task Queue

| Task ID | Status | Depends On | Ready When | Selection Priority |
|---------|--------|------------|------------|-------------------|
| T1 | in_progress | - | approval 已完成 | P1 |
| T2 | pending | T1 | T1=done | P2 |
```

## 当前活跃任务选择规则

```markdown
## 8. 当前活跃任务选择规则
- 若存在且仅存在一个 ready 任务，则将其锁定为 Current Active Task
- 若存在多个同优先级 ready 任务，则停止自动推进并回到 hf-workflow-router
```

## Task Board 操作

- 建议的首个活跃任务先写在任务计划正文中
- 只有 review 通过且 approval step 完成后，才把权威版 Current Active Task 写入 feature `progress.md`（默认 `features/<active>/progress.md`）
- 后续任务切换由 hf-workflow-router 在每次 completion gate 通过后根据 queue projection 重选
- 若需要新建 board，优先使用本 skill 内 `references/task-board-template.md`

## queue projection 最小要求

router 能唯一判断下一个 task 即可。至少做到：
- 每个任务有初始队列状态（ready / pending）
- 每个任务有 Ready When 条件
- 当上游任务 =done 时，下游任务状态变更为 ready
