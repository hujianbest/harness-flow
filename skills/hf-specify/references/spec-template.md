# 规格文档模板

若 `AGENTS.md` 为当前项目声明了规格模板、章节骨架或命名要求，优先遵循项目约定。

## 保存路径

默认：`features/<active>/spec.md`

Deferred backlog（若存在）：`features/<active>/spec-deferred.md`

若 `AGENTS.md` 声明了规格路径映射，优先使用映射路径。

## Product Discovery 上游输入

若当前主题来自 product discovery，优先补充读取：
- `docs/insights/*-spec-bridge.md`（高价值上游输入）
- 按需展开：`*-insight-pack.md`、`*-concept-brief.md`、`*-probe-plan.md`

`spec-bridge` 只负责提供更稳定的上游 thesis、范围边界与 unknowns，不替代正式需求规格正文。

## 默认结构

```markdown
# <主题> 需求规格说明

- 状态: 草稿
- 主题: <主题>

## 1. 背景与问题陈述
## 2. 目标与成功标准
## 3. 用户角色与关键场景
## 4. 当前轮范围与关键边界
## 5. 范围外内容
## 6. 功能需求
## 7. 非功能需求
## 8. 外部接口与依赖（按需）
## 9. 约束与兼容性要求
## 10. 假设与失效影响（按需）
## 11. 开放问题（区分阻塞 / 非阻塞）
## 12. 术语与定义（按需）
```

## 编写要求

- 背景描述为什么要做，不写成方案介绍
- 目标与成功标准要具体、可判断，避免只写抽象愿景
- 范围章节应显式区分当前轮边界与后续增量边界
- 功能需求描述可观察行为，而不是实现手段
- 非功能需求描述可判断条件，而不是空泛形容词
- 约束描述硬性限制
- 假设要写明失效风险或影响
- 开放问题要标出阻塞 / 非阻塞；阻塞项在送评审前应关闭
- 若存在 deferred backlog，应在范围外内容中明确指向
- 不要为追求形式统一而破坏项目已声明的模板结构

## 状态同步

规格草稿交评审后，应同步：
- 规格文档状态（`状态: 草稿`）
- feature `progress.md`（默认 `features/<active>/progress.md`）中的 `Current Stage: hf-specify`
- feature `progress.md` 中的 `Next Action Or Recommended Skill: hf-spec-review`
