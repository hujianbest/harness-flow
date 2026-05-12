# Tasks Review Checklist

评审任务计划时，至少对以下 6 个维度逐项审查。每个维度内部评分 `0-10`，评分帮助区分轻微缺口与阻塞问题。

## 评分辅助规则

- 任一关键维度低于 `6/10` → 不得返回 `通过`
- 任一维度低于 `8/10` → 通常至少对应一条具体 finding

## 评审维度

| ID | 维度 | Pass Condition |
|---|---|---|
| `TR1` | 可执行性 | 关键任务可冷启动推进，不存在“实现某模块”式大任务 |
| `TR2` | 任务合同完整性 | 关键任务具备 `Acceptance`、`Files`、`Verify`、完成条件 |
| `TR3` | 验证与测试设计种子 | 测试设计种子足够支持后续 fail-first 实现；UI / API / full-stack 任务声明 runtime evidence tier |
| `TR4` | 依赖与顺序正确性 | 依赖链、关键路径和执行顺序合理，无循环依赖 |
| `TR5` | 追溯覆盖 | 关键任务可回指到已批准规格与设计，不存在 orphan task |
| `TR6` | Router 重选就绪度 | `Current Active Task` 选择规则唯一，queue projection 稳定可回读 |

### `TR1` 可执行性

- 每个关键任务是否小到能在单任务闭环里推进？
- 是否存在“实现某模块”“完成整条流程”这类脱离工件现实的任务？
- 是否有任务一开始就依赖多个未稳定前提？

### `TR2` 任务合同完整性

- 关键任务是否显式写出 `Acceptance`？
- 是否写出 `Files / 触碰工件`？
- 是否写出 `Verify` 与完成条件？
- reviewer 能否冷读出“完成时什么必须为真”？

### `TR3` 验证与测试设计种子

- 测试设计种子是否能帮助 `hf-test-driven-dev` 进入测试设计？
- 是否至少指出主要行为、关键边界和适合 fail-first 的点？
- 是否只写了“补测试”“自行验证”这类空泛表述？
- UI / API / full-stack 任务是否写清 required evidence tier：component-integration、api-contract、browser-runtime、full-stack-smoke？
- 是否写清服务启动、health check、API base URL、smoke routes 或引用项目 runtime-smoke profile？

### `TR4` 依赖与顺序正确性

- 依赖关系是否正确？
- 关键路径是否合理？
- 是否有循环依赖或顺序反转？
- 风险区域是否通过顺序或验证被前置处理？

### `TR5` 追溯覆盖

- 任务是否忠实覆盖已批准规格 / 设计？
- 是否有任务无法追溯到上游依据？
- 是否有关键需求 / 关键设计决策完全没有落到任务中？

### `TR6` Router 重选就绪度

- `Current Active Task` 选择规则是否唯一？
- 当前任务完成后，router 是否能稳定重选下一任务？
- queue projection 是否可回读，而不是靠聊天记忆理解？

## Anti-Pattern 检测

| ID | Anti-Pattern | 检测信号 | 正确做法 |
|---|---|---|---|
| `TA1` | 大任务 | 一个任务打包多条行为、多个文件簇或多个发布轮次 | 拆成单任务可验证闭环 |
| `TA2` | 缺 Acceptance | 任务只有“目标”，没有明确完成判定 | 写出完成时必须为真的条件 |
| `TA3` | 缺 Files / Verify | 任务不说明触碰工件，也不说明如何验证 | 补齐 `Files` 与 `Verify` |
| `TA4` | 无 test seed | 任务进入实现前没有测试设计种子 | 写出主要行为、边界与 fail-first 点 |
| `TA5` | 里程碑冒充任务 | 里程碑标题直接当成真实任务执行 | 里程碑与任务分层表达 |
| `TA6` | orphan task | 任务无法追溯到规格或设计 | 回补 trace anchor 或删除伪任务 |
| `TA7` | unstable active task | 多个候选任务都像“当前活跃任务” | 显式写唯一选择规则 |
| `TA8` | missing runtime tier | UI/API/full-stack 任务只写单测或 build，不写 browser/API/contract/smoke 证据 | 在 Verify/DoD 中补 required tier 和允许降级条件 |
| `TA9` | runtime entry unspecified | 任务要求运行时验证，但未写服务启动、健康检查、API base URL 或 smoke route | 引用 runtime-smoke profile 或在任务中写明入口 |
