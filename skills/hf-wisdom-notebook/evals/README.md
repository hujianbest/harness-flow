# hf-wisdom-notebook — evals

> 高风险 skill 必备 evals（按 design §6 / tasks.md TASK-004）。保护 hf-wisdom-notebook 的核心行为契约：5 文件 schema 严格 + 跨 task delta 累积 + entry-id append-only + 不写 verdict。

## 行为 contract（要保护的 invariants）

1. **5 文件容器约束**：每个 feature 的 `notepads/` 必须含 5 文件齐全（learnings / decisions / issues / verification / problems）；首次 task 创建空骨架
2. **每 task delta**：每个 task 完成时至少在 `learnings.md` 或 `verification.md` 任一中追加 entry；`wisdom-skip` 是显式例外
3. **Append-only + entry-id 全局递增**：不修改已有 entry，只追加；entry-id 不重用，应严格递增（gap 允许但 strict 模式 FAIL）
4. **不写 verdict / approval 等价物**：notepads 内容不能含"通过 / 阻塞 / APPROVED / FAILED" 类结论性判断
5. **跨 feature 隔离**：本 skill 只读写 active feature 的 notepads；不跨 feature 复制 entry

## eval 文件

| 文件 | 用途 |
|---|---|
| `evals.json` | 4 个 eval case 覆盖正常路径 / 5 文件缺失 / delta 缺失 / verdict 误写 |
| `fixtures/` | 复用 `../scripts/test-fixtures/` 的 4 个 fixture（`negative-missing-file` / `negative-no-delta` / `negative-duplicate-entry-id` / `negative-non-monotonic`）+ 真实 dogfood `features/002-omo-inspired-v0.6/notepads/` 作为 positive |

## 运行方式

```bash
# 直接复用 TASK-003 的 stdlib python tests
python3 skills/hf-wisdom-notebook/scripts/test_validate_wisdom_notebook.py
```

10 stdlib unittest 用例覆盖了 evals.json 中描述的 4 个 eval case 的可执行断言面。

## 触发评测

evals 在以下时机由 hf-completion-gate 自动调用：
- v0.6 feature closeout 前（gate 调 validate-wisdom-notebook.py）
- CI 跑 tests/test_*.py + skills/hf-*/scripts/test_*.py 的整批 stdlib 测试
