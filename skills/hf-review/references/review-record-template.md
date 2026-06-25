# 评审记录模板

> 每轮评审在 `features/<id>-<slug>/reviews/` 落盘一份记录；同一目标的复审追加轮次后缀（`-r2`、`-r3`）。findings 修复过程必须**逐条回写**本记录的 Resolution 列——没有 Resolution 闭环的 critical/important，门禁不算通过。

```markdown
# <R1/R2/R3> <对象> 评审< -r轮次>

## 评审对象
- 工件: <path>（spec.md / design.md / 测试代码 + plan.md / 实现 diff）
- 版本: <commit / 范围>
- 评审者: <hf-reviewer subagent / 人>（独立上下文，非产物作者）
- 上游输入: <spec.md / design.md / 适用 rubric / hf-clean-code / 适用 coding-standards / 领域技能>
- 抽查: <如做了 mutation 自检：改了哪行、哪个测试红了；如读了错误路径：列出>

## Findings

| # | 位置 | 问题 | 为什么是问题 | 严重级 | 分类 | 建议返工阶段 | Resolution / 复审 |
|---|---|---|---|---|---|---|---|
| 1 | `spec.md` §FR-003 Acceptance | 验收用「足够快」，无法落成失败测试 | 不可测试，两人会做出不同东西 | critical | LLM-FIXABLE | hf-specify | <修复摘要 + commit + 验证命令；复审记录路径> |
| 2 | `src/mode.c:42` mode_set | 非法输入返回 OK | 留 bug | critical | LLM-FIXABLE | hf-tdd | … |

## Verdict

**通过 / 需修改 / 重新设计**

理由: <一句话，点明是否还有 critical/important；若为「重新设计」说明指向上游哪个阶段>

## 人工确认（attended）/ N/A(unattended)

- attended: <yes / no + 意见摘要 + 谁>
- unattended: N/A(unattended) —— 评审/记录/critical 阻塞照做，留待人事后审计

## 下一步

- 通过（attended 已确认）→ 进入下一阶段
- 需修改 → 回建议返工阶段定向修复，回填每条 Resolution 后发起复审（新轮次记录）
- 重新设计 → 回上游阶段（hf-specify / hf-design），重新经过受影响的 R 门禁
- R3 需修改 → 下一步是 hf-tdd（不是直接复审，不是 ship）

## 评审者备注

<额外上下文或建议；不确定的判断标注「待人裁决」>
```

## 写法约束

- **每条 finding 必须具体到位置**（文件 + 行号/章节/Case ID）和**可执行的修复方向**；不写「质量有待提高」。
- 严重级用 critical / important / minor；分类用 LLM-FIXABLE / USER-INPUT / TEAM-EXPERT；返工阶段用 hf-specify / hf-design / hf-tdd。
- R3 评审按测试 rubric 和代码 rubric 分别过；可合并到本表（在「位置」列标明是测试 finding 还是代码 finding），也可拆成两份记录，但都挂同一 R3 门禁。
- 复审记录追加 `-r2`/`-r3` 后缀，并在 Findings 表里**核对上一轮 Resolution 与实际 diff 一致**；问题不能在新记录里「凭空消失」。
