---
name: hf-review
description: HarnessFlow 独立评审协议。规格(spec)、架构(architecture)、实现代码均须经本技能给出落盘结论才能门禁放行。核心纪律:只承认 subagent 或全新会话;主会话冷读为降级且不得自我确认通过。代码门另加载 hf-code-review。不修改被评对象,只产结论与 findings。
---

# Review(独立评审)

评审产出是**落盘结论**,对抗作者自我偏好。独立性是硬约束。

## 独立性

| 方式 | 效力 |
|------|------|
| subagent / 全新会话 | 完整 |
| 主会话冷读 | 降级:结论只能「待独立复核」或「需修改」,不得「通过」 |

`auto` 下降级是硬停点;确认行禁止 `auto-approved`(gate 拦截)。

## 评审对象

| 对象 | Checklist | 记录 |
|------|-----------|------|
| `spec.md` | `references/requirements-checklist.md` | `reviews/spec-review.md` |
| `architecture.md` | `references/design-checklist.md` | `reviews/architecture-review.md` |
| 实现代码 | `references/code-checklist.md` + 加载 `hf-code-review` | `reviews/code-review.md` |

读 `progress.md` 已加载扩展,把扩展声明的检查项并入本轮。

## 流程

1. 冷读被评工件与上游(评架构读 spec;评代码读 spec/architecture/tickets)。
2. **代码门**:必须加载并遵循 `hf-code-review`(Standards + Spec 双轴,宜并行 subagent);评审者自己跑测试、自己读 `git diff`,不采信作者叙述。
3. Findings 格式:`- [严重|一般|建议] <位置>: <问题> → <建议>`。有严重/一般 → `需修改`;仅建议可 `通过`;降级不得 `通过`。
4. 落盘:

```markdown
# <对象> 评审 (第 N 轮)
- 日期: YYYY-MM-DD
- 评审方式: subagent | 独立会话 | 主会话降级
- 结论: 通过 | 需修改 | 待独立复核
## Findings
```

5. `需修改` → 回作者阶段只修 findings 再复审。`通过` → interactive 等用户确认后写 `- 用户确认: <日期>`;auto 非降级写 `auto-approved <日期>`。确认必须在结论行之后。

## 红线

- 评审者顺手改被评对象;用作者记忆开脱;无具体位置的空泛结论;混合「通过但是…」。
