# hf-ultrawork — evals

> 高风险 skill 必备 evals（按 design §6 / tasks.md TASK-008）。保护 hf-ultrawork 的 fast-lane 行为契约：5 类不可压缩项 + 6 escape conditions + architect-explicit-opt-in + audit trail completeness。

## 行为 contract（要保护的 invariants）

1. **5 类不可压缩项绝不绕过**（FR-008 + ADR-009 D2）：
   - 8 Fagan review verdicts
   - 3 gate verdicts (regression / doc-freshness / completion)
   - hf-finalize closeout pack 完整性
   - spec / design / tasks approval 工件落盘
   - SKILL.md Hard Gates "方向 / 取舍 / 标准不清抛回"
2. **6 escape 条件每次 verdict 后必检**：Hard Gates 不清 / review verdict=阻塞 / gate verdict=FAIL / problems.md status=open / rewrite loop ≥ 3 / 架构师 explicit pause 关键词
3. **explicit opt-in only**：fast lane 永远不默认启用；必须由架构师关键词或 Metadata 触发
4. **audit trail 即时追加**：每个自动决策 +1 行到 progress.md `## Fast Lane Decisions`，不批量补
5. **不写 review / gate verdict**：hf-ultrawork 只把 reviewer verdict 落到 approval 工件，不替代 reviewer 的判断本身

## eval 文件

| 文件 | 用途 |
|---|---|
| `evals.json` | 4 个 eval case 覆盖 explicit opt-in 识别 / 5 类不可压缩 enumeration / 6 escape conditions / audit trail schema |

## 运行方式

```bash
# 直接复用 TASK-007 的 stdlib python tests
python3 tests/test_ultrawork_skill.py
```

10 stdlib unittest 用例覆盖了 evals.json 中 4 个 eval case 的可执行断言面（特别是最严格的 `test_hard_gates_enumerates_5_noncompressibles` 5 独立 regex 检查）。

## 行为 contract 的 dogfood 验证

本 feature 002-omo-inspired-v0.6/ 自身的 fast lane 全程是 hf-ultrawork 行为的真实 dogfood：

- progress.md `## Fast Lane Decisions` 段累计 19 行（截至 TASK-007 closeout）→ 覆盖 invariant #4 audit trail completeness
- 0 escape 触发 → 覆盖 invariant #2 escape conditions 检查（无误判）
- 全部 spec / design / tasks approval 工件落盘 → 覆盖 invariant #1 第 4 类
- 全部 review verdict 由独立 record 给出（reviewer ≠ author session 角色）→ 覆盖 invariant #1 第 1 / #5
