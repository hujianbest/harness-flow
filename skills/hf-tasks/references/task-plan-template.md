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

## 状态同步

- 任务计划状态字段（如 `状态: 草稿`）
- 主题或范围标识
- 当前活跃任务选择规则
- 可供评审定位的章节结构
- feature `progress.md`（默认 `features/<active>/progress.md`）中的 `Current Stage: hf-tasks`
- feature `progress.md` 中的 `Next Action Or Recommended Skill: hf-tasks-review`
