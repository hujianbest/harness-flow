# 产品发现文档模板

若 `AGENTS.md` 为当前项目声明了 discovery 模板、路径或命名要求，优先遵循项目约定。

## 保存路径

默认：`docs/insights/YYYY-MM-DD-<topic>-discovery.md`

若后续需要拆出更细工件，可按需演化为：
- `*-concept-brief.md`
- `*-probe-plan.md`
- `*-insight-pack.md`
- `*-spec-bridge.md`

第一版默认不强制拆分，保持单文档即可。

## 默认结构

```markdown
# <主题> 产品发现草稿

- 状态: 草稿
- 主题: <主题>

## 1. 问题陈述
## 2. 目标用户与使用情境
## 3. Why now / 当前价值判断
## 4. 当前轮 wedge / 最小机会点
## 5. 已确认事实
## 6. 关键假设与风险
## 7. 候选方向与排除项
## 8. 建议 probe / 验证优先级
## 9. Bridge to Spec
## 10. 开放问题（阻塞 / 非阻塞）
```

## 编写要求

- 问题陈述写用户进展被什么阻塞，不写实现方案
- wedge 要明确“当前轮最小推进点”，而不是大而全 roadmap
- 已确认事实与假设必须显式分开
- 候选方向与排除项要帮助收敛，而不是无限发散
- `Bridge to Spec` 必须写清哪些结论已稳定到足以进入 `hf-specify`
- 若存在 later ideas，应明确写为后续候选，而不是埋在 prose 里

## 状态同步

discovery 草稿交评审后，应同步：
- 文档状态（`状态: 草稿`）
- `task-progress.md` 中的 `Current Stage: hf-product-discovery`
- `task-progress.md` 中的 `Next Action Or Recommended Skill: hf-discovery-review`
