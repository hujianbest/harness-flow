# Code Review Checklist

评审实现代码时，至少对以下 7 个维度逐项审查。每个维度内部评分 `0-10`，评分帮助区分轻微缺口与阻塞问题。

`CR7` 由 5 个子维度构成；详细规则与 anti-patterns 见 `clean-architecture-guardrails.md`。

## 评分辅助规则

- 任一关键维度低于 `6/10` → 不得返回 `通过`
- 任一维度低于 `8/10` → 通常至少对应一条具体 finding
- `CR7` 的任一子维度 (`CR7.1`-`CR7.5`) 低于 `6/10` → 整个 `CR7` 不得通过

## 评审维度

| ID | 维度 | Pass Condition |
|---|---|---|
| `CR1` | 正确性 | 实现真正完成任务目标，没有明显逻辑缺口 |
| `CR2` | 设计一致性 | 实现遵循已批准设计，偏离可解释且可追溯 |
| `CR3` | 状态 / 错误 / 安全 | 错误处理、状态转换和安全性不过度依赖“测试全绿” |
| `CR4` | 可读性与可维护性 | 命名、结构、抽象层次合理，无明显魔法数字或死代码 |
| `CR5` | 范围守卫 | 不引入未记录的新能力或 undocumented behavior |
| `CR6` | 下游追溯就绪度 | 代码与交接块足以支持 `hf-traceability-review` |
| `CR7` | 架构健康与重构纪律 | 实现节点守住 Two Hats，Refactor Note 完整，Clean Arch conformance 通过，识别并按 escalation 边界处理 architectural smells |

### `CR1` 正确性

- 实现是否真正完成任务目标？
- 是否存在 off-by-one、边界遗漏、遗漏分支？

### `CR2` 设计一致性

- 实现是否遵循已批准设计？
- 若偏离，是否有清晰理由和 trace anchor？
- 是否把本应在 service / domain 层的逻辑塞回了 adapter / handler 层？

### `CR3` 状态 / 错误 / 安全

- 是否有静默失败？
- 状态转换是否安全？
- 是否有明显安全隐患、权限绕过、错误吞掉不报？

### `CR4` 可读性与可维护性

- 命名是否清晰？
- 是否存在魔法数字、死代码、过早优化或过度嵌套？
- 结构是否便于后续维护？

### `CR5` 范围守卫

- 是否顺手加了规格 / 设计中不存在的能力？
- 是否出现 undocumented behavior 或超范围实现？

### `CR6` 下游追溯就绪度

- 当前实现与交接块是否足以支持 traceability review？
- 触碰工件、关键行为和风险是否可回读？

### `CR7` 架构健康与重构纪律

详细判别规则与子维度评分尺度见 `clean-architecture-guardrails.md`。

5 个子维度：

- `CR7.1` Two Hats Hygiene：RGR 步骤是否守住帽子纪律
- `CR7.2` Refactor Note 完整性：字段齐全，使用 Fowler vocabulary
- `CR7.3` Architectural Conformance：实现遵循 `hf-design` 中依赖方向 / 模块边界 / 接口契约
- `CR7.4` Architectural Smells Detection：触碰范围内 smells 被识别并按 escalation 边界处理
- `CR7.5` Boy Scout Compliance：触碰范围 clean code 健康度未退化

## Anti-Pattern 检测

| ID | Anti-Pattern | 检测信号 | 正确做法 |
|---|---|---|---|
| `CA1` | silent failure | 失败后直接 return / swallow error | 记录并按设计传播 / 重试 |
| `CA2` | magic numbers | 状态或阈值直接写裸数字 | 提取常量或枚举 |
| `CA3` | undocumented behavior | 顺手加入未批准的新能力 | 先走 `hf-increment` 或回修 |
| `CA4` | design boundary leak | 业务逻辑塞进错误层次 | 回到已批准边界 |
| `CA5` | dead code / premature optimization | 现在用不到的抽象或路径已提前引入 | 收回到当前范围 |
| `CA6` | hat-mixing | GREEN 步内做 cleanup / 同 commit 内既加行为又改结构 / preparatory refactor 与 RED 步骤纠缠 | 拆 commit；cleanup 归 REFACTOR 步；preparatory refactor 独立成步 |
| `CA7` | undocumented-refactor | 触碰文件出现结构变化但 Refactor Note 未提；In-task Cleanups 缺 vocabulary | 补 Refactor Note 或回滚不必要变更 |
| `CA8` | escalation-bypass | 跨 ≥3 模块 / 改 ADR / 改模块边界 / 改接口契约的变更被在 task 内"顺手"做掉 | `阻塞`，回 `hf-workflow-router`，escalate 到 `hf-increment` |
| `CA9` | over-abstraction | 引入设计未声明的新抽象层 / 新接口 / 新基类，理由是"未来可能用得到" | 回退到 design 声明的边界（YAGNI 与 Clean Arch dependency rule） |
| `CA10` | architectural-smell-ignored | 触碰范围内可见 smell（god-class / cyclic-dep / layering-violation / leaky-abstraction / feature-envy）未被识别或未被 documented | 在 Refactor Note 中识别、分类、按边界处理 |
