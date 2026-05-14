# Wisdom Notebook Update Protocol

> 单 task 完成时 `hf-test-driven-dev` 写 delta 的详细 protocol；fast lane / standard mode 都适用，仅在 audit trail 同步上有差异。

## 触发时机

每个 `hf-test-driven-dev` task 在 REFACTOR-N 步完成且 task 即将进入 `test-review` 之前。

## 步骤

### 1. 计算 entry-id 起点

```bash
# 在 features/<active>/notepads/ 下：
for f in learnings decisions issues verification problems; do
  next_id=$(grep -oE "${f%s}-[0-9]+" "$f.md" 2>/dev/null | sort -t- -k2 -n | tail -1 | awk -F- '{printf "%s-%04d\n", $1, $2+1}')
  next_id=${next_id:-${f%s}-0001}
  echo "$f: next entry-id = $next_id"
done
```

（`scripts/validate-wisdom-notebook.py` 可同时算出每文件 next-id；agent 不必自己跑此 shell，只需参考语义）

### 2. 决定要写的 file（FR-002 强制清单）

| Task 类型 | 必写 | 可选 |
|---|---|---|
| 实现新 feature 行为 | learnings + verification | decisions / issues |
| schema / reference 文档定义 | learnings + verification | decisions |
| SKILL.md 改动 | learnings + verification | decisions |
| 纯 wording 修订（无新 pattern） | （可 wisdom-skip）| issues |
| 遇到阻塞问题 | learnings + verification + **problems**（触发 fast lane escape）| — |

`wisdom-skip` 例外必须在 progress.md 显式声明：

```markdown
- wisdom-skip: TASK-NNN reason: pure wording, no new learnings
```

### 3. 按 schema 追加 entry

每个文件最新 entry 放最上面（按 task 时间倒序），用 `---` 分隔。

样板见 `notebook-schema.md`。

### 4. 即时校验

```bash
python3 skills/hf-wisdom-notebook/scripts/validate-wisdom-notebook.py \
  --feature features/<active>/
```

- exit 0 = PASS → 继续步骤 5
- exit 1 = FAIL → 修正 entry（按错误信息）后重跑

### 5. 同步 progress.md `## Wisdom Delta` 段

往 progress.md 追加一行：

```markdown
| TASK-NNN | learnings/learn-0007 + verification/verify-0012 |
```

router 在选下一 active task 时按"近 N=3 task 的 wisdom 行"读取 + 注入下游 prompt（具体注入协议在 TASK-011 修改 hf-workflow-router 时定义）。

## Fast Lane 下的额外动作

按 ADR-009 D4 fast lane audit trail，**fast lane 中**完成的 task 完成后还需在 progress.md `## Fast Lane Decisions` 段追加一行：

```markdown
| <time> | hf-wisdom-notebook (TASK-NNN) | wisdom-delta-write | TASK-NNN delta written: learn-NNNN + verify-NNNN | architect explicit auto mode | no |
```

这条 audit trail 让架构师事后审计时能看到"哪些 wisdom 是 fast lane 自动写的、哪些是 standard mode 手动写的"。Standard mode 不需要这条。

## 错误处理

| 情况 | 处理 |
|---|---|
| `validate-wisdom-notebook.py` exit 1 | 按错误信息修正 entry；不绕过 |
| 5 文件之一不存在 | 创建空骨架（`# <Title>` + 简短说明 + 空段），entry-id 计数从 0001 开始 |
| problems.md 出现新增 status=open | **立即触发 fast lane escape #4**：让出给架构师；不在 fast lane 内"先记着继续走" |
| Concurrent task（不应发生，HF 禁止并行实现） | 报错并停下；按 D5=A "不并行实现" 硬规 |

## 验证清单（task 完成时自检）

- [ ] 对应 task 至少 1 条 delta（learnings 或 verification）
- [ ] entry-id 严格递增不重用
- [ ] `validate-wisdom-notebook.py` PASS
- [ ] progress.md `## Wisdom Delta` 已追加行
- [ ] fast lane 下额外 progress.md `## Fast Lane Decisions` 已追加行
- [ ] 未在 entry 内写任何 verdict / approval 等价物
