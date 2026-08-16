---
name: hf-review
description: HarnessFlow 独立评审协议。规格、架构、实现代码宜经本技能给出落盘结论再推进。核心纪律：只承认 subagent 或全新会话；主会话冷读属于降级评审，且不得自我确认通过。代码门在本技能内按 Standards + Spec 双轴评审。不修改被评对象，只产出结论与发现项。
---

# hf-review（独立评审）

评审产出是**落盘结论**,对抗作者自我偏好。独立性是硬约束。

## 独立性

| 方式 | 效力 |
|------|------|
| subagent / 全新会话 | 完整 |
| 主会话冷读 | 降级:结论只能「待独立复核」或「需修改」,不得「通过」 |

`auto` 模式下降级评审是硬停点；确认行禁止写入 `auto-approved`。

## 评审对象

| 对象 | 检查清单 | 记录 |
|------|-----------|------|
| `product/architecture.md` | `references/product-architecture-checklist.md` | `product/reviews/product-architecture-review.md` |
| `spec.md` | `references/requirements-checklist.md` | `reviews/spec-review.md` |
| 特性 `architecture.md` | `references/design-checklist.md` | `reviews/architecture-review.md` |
| 实现代码 | `references/code-checklist.md`（Standards + Spec 双轴） | `reviews/code-review.md` |

有 UI 时加载 `hf-ui-design`，把其检查项并入本轮。

## 流程

1. 冷读被评工件与上游（评产品架构时读 CONTEXT/ADR；评特性架构时读规格与 `product/architecture.md`；评代码时读取规格/架构/任务票）。
2. **代码门**见下节。评审者自己运行测试、自己读取 `git diff`，不采信作者叙述。
3. 发现项格式：`- [严重|一般|建议] <位置>: <问题> → <建议>`。存在严重/一般问题 → `需修改`；仅有建议时可判定为 `通过`；降级评审不得判定为 `通过`。
4. 落盘:

```markdown
# <对象> 评审 (第 N 轮)
- 日期: YYYY-MM-DD
- 评审方式: subagent | 独立会话 | 主会话降级
- 结论: 通过 | 需修改 | 待独立复核
## 发现项
```

代码评审额外保留 `## Standards` 与 `## Spec` 两节，发现项分轴列出，不要合并重排。

5. `需修改` → 返回作者阶段，只修复发现项后再复审。`通过` → `interactive` 等待用户确认后写 `- 用户确认: <日期>`；`auto` 下非降级评审写 `auto-approved <日期>`。确认必须位于结论行之后。

## 代码门（Standards + Spec）

对固定点与 `HEAD` 的差异做双轴评审（宜并行 subagent，避免互相污染）：

- **Standards**——是否符合本仓库已记录的编码标准，外加 `references/code-smells.md` 异味基线（仓库规则优先；异味均为判断项）。
- **Spec**——是否忠实实现 `features/<id>/spec.md` / 架构 / 任务票；缺失规格则跳过 Spec 轴并注明 `no spec available`。

固定点由用户指定（提交、分支、标签、`main` 等）；未指定则询问。先确认 `git rev-parse` 有效且 `git diff <fixed-point>...HEAD` 非空。

一项变更可通过一轴而未通过另一轴（代码规范但做错需求，或需求对但违反约定）。分别报告，防止一轴掩盖另一轴。

## 红线

- 评审者顺手改被评对象;用作者记忆开脱;无具体位置的空泛结论;混合「通过但是…」。
