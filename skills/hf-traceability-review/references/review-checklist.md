# Traceability Review Checklist

评审追溯链时，至少对以下 7 个维度逐项审查。每个维度内部评分 `0-10`，评分帮助区分轻微缺口与阻塞问题。

## 评分辅助规则

- 任一关键维度低于 `6/10` → 不得返回 `通过`
- 任一维度低于 `8/10` → 通常至少对应一条具体 finding

## 评审维度

| ID | 维度 | Pass Condition |
|---|---|---|
| `TZ1` | 规格 → 设计追溯 | 关键需求可回指到设计决策或关键接口 |
| `TZ2` | 设计 → 任务追溯 | 关键设计决策已落到任务，不存在设计空洞 |
| `TZ3` | 任务 → 实现追溯 | 实现与任务计划、触碰工件、完成条件一致 |
| `TZ4` | 实现 → 验证追溯 | 测试 / 验证证据支撑当前实现结论 |
| `TZ5` | 漂移与回写义务 | 未记录漂移、未回写工件、undocumented behavior 被显式识别 |
| `TZ6` | 整体链路闭合 | 当前批准工件与代码状态整体一致，可进入 regression gate |
| `TZ7` | UI 设计一致性追溯 | UI surface 的 visual invariants / token / contract 可追到任务、实现和截图/DOM/网络证据；不只证明元素存在 |

### `TZ1` 规格 → 设计追溯

- 关键需求是否被设计承接？
- 是否有规格更新但设计未同步？

### `TZ2` 设计 → 任务追溯

- 关键设计决策是否落到任务？
- 是否有任务计划遗漏关键设计约束？

### `TZ3` 任务 → 实现追溯

- 实现是否完成任务的完成条件？
- 触碰工件是否与任务计划一致？
- 是否存在超出任务范围的额外行为？

### `TZ4` 实现 → 验证追溯

- 测试 / 验证证据是否支撑当前实现？
- RED/GREEN、review、verification 是否可回读到当前实现？

### `TZ5` 漂移与回写义务

- 是否出现 undocumented behavior、orphan code、未回写设计 / 任务 / 状态工件？
- 是否明确列出需要同步的工件？

### `TZ6` 整体链路闭合

- 整条 spec→design→tasks→impl→test/verification→status 链路是否闭合？
- 当前状态是否足以安全进入 regression gate？

### `TZ7` UI 设计一致性追溯

仅在触碰 UI surface、样式系统、App shell/provider、路由、表单、视觉 token 或组件库时适用：

- `ui-design.md` 的 UI Implementation Contract 是否被任务计划引用？
- 任务 Acceptance 是否包含 visual invariants、token mapping、forbidden drift、state matrix 和 evidence targets？
- 实现文件是否可追溯到这些 contract 条目，而不是只追到“有对应组件/文案”？
- 测试/验证证据是否包含 screenshot/DOM/console/network 或明确降级许可？
- 是否存在设计文档写明主色/无渐变/token 化，但实现使用未批准颜色、渐变、硬编码 utility 的 visual drift？
- 是否存在 test evidence 只断言文本存在、组件渲染，而没有覆盖 design conformance？

UI task 中 `TZ7` 低于 6/10 不得通过；若只缺截图/DOM 证据但实现可定向补齐，通常为 `需修改`。

## Anti-Pattern 检测

| ID | Anti-Pattern | 检测信号 | 正确做法 |
|---|---|---|---|
| `ZA1` | spec drift | 规格已变更，设计 / 任务仍基于旧版本 | 回 router 或回写上游工件 |
| `ZA2` | orphan task | 任务无法追溯到规格或设计 | 回补 trace anchor 或删除伪任务 |
| `ZA3` | undocumented behavior | 代码引入未记录的新行为 | 回写工件或走 increment |
| `ZA4` | unsupported completion claim | 验证不足却声称完成 | 回补验证或回实现 |
| `ZA5` | visual drift | 实现使用未批准主色、渐变、字体、阴影、布局范式，与 UI design contract 冲突 | 回实现修正，或先回 `hf-ui-design` 更新设计并重新评审 |
| `ZA6` | low-resolution trace | 追溯只证明“有 Hero / 有按钮 / 有卡片”，没有证明符合 visual invariants / token / state / a11y | 补 UI contract 级追溯矩阵和截图/DOM 证据 |
| `ZA7` | token bypass | 实现直接硬编码 Tailwind 色彩/间距/阴影，未映射到 design token | 补 token mapping 或修正实现 |
| `ZA8` | screenshot evidence missing | UI conformance claim 没有截图/DOM/console/network 证据，也无降级许可 | 回补 browser-runtime visual evidence |
