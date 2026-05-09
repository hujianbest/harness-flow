# Runtime Evidence Protocol — `hf-browser-testing`

本文是 `hf-browser-testing` 的深度参考。SKILL.md 已规定三层 evidence（DOM / Console / Network）+ fresh evidence + observation-not-verdict 的硬规则；本文给出工具映射、目录约定与 metadata schema。

## 工具映射

`hf-browser-testing` 不绑定具体工具，只对 evidence 形状有要求。常见工具：

| 工具 | 三层证据如何产出 |
|---|---|
| **Chrome DevTools MCP** | 截图：`page_screenshot`；console：`page_console_log`；network：`page_network_har`。推荐首选，因证据格式与浏览器原生一致。 |
| **Playwright** | 截图：`page.screenshot()`；console：`page.on('console', ...)` 收集器；network：`context.tracing.start({ snapshots: true })` 或 `page.on('response', ...)` 落 HAR。 |
| **Puppeteer** | 截图：`page.screenshot()`；console：`page.on('console', ...)` 收集器；network：`page.on('request' / 'response' ...)` 自行序列化。 |
| **手动浏览器 + DevTools** | 截图：DevTools full-page；console：`Right-click → Save as`；network：DevTools `Save all as HAR with content`。仅在自动化不可用时退而求其次。 |

工具选择优先级：

1. 项目权威约定（`CONTRIBUTING.md` / 项目 sidecar 已声明的工具）。
2. Chrome DevTools MCP（与 AS `browser-testing-with-devtools` 对齐，证据格式标准）。
3. Playwright / Puppeteer（项目已有依赖时优先复用）。
4. 手动浏览器（仅最后手段；observations 必须显式标注 `tool: manual`）。

## 目录约定

```text
features/<active>/verification/browser-evidence/<task-id>/
├── metadata.json
├── observations.md
└── <scenario-name>/
    ├── screenshots/
    │   ├── 01-initial.png
    │   ├── 02-<state>.png
    │   └── ...
    ├── console.log              # 完整时序日志（含 warn / error）
    └── network.har              # HAR 1.2；或 network.json（请求列表 + 异常请求详情）
```

每个 scenario 子目录：

- 名称用 kebab-case（与 spec / ui-design 中的 user flow 名一致）。
- screenshots 目录至少包含一张初始态 + 每个声明的关键 interaction state（hover / focus / disabled / loading / error / empty）至少一张。
- console.log 是完整时序日志；不允许"只保留 error"。
- network 推荐 HAR 1.2；若工具不支持，用 `network.json` 并保留至少 method / url / status / headers / body 摘要。

## `metadata.json` schema

```json
{
  "schema_version": "1.0",
  "task_id": "<task-id>",
  "feature": "<active feature name>",
  "session_started_at": "<ISO 8601>",
  "session_ended_at": "<ISO 8601>",
  "commit_sha": "<full SHA>",
  "worktree_path": "<absolute path>",
  "tool": {
    "name": "chrome-devtools-mcp | playwright | puppeteer | manual",
    "version": "<x.y.z>",
    "browser": "Chromium <ver> | Firefox <ver> | ..."
  },
  "scenarios": [
    {
      "name": "<scenario-name>",
      "user_flow_ref": "<spec / ui-design 中对应的 user flow 标识>",
      "states_covered": ["initial", "hover", "focus", "disabled", "loading", "error", "empty"],
      "screenshots": ["screenshots/01-initial.png", "..."],
      "console": "console.log",
      "network": "network.har"
    }
  ]
}
```

要求：

- `commit_sha` 必填；缺位 → fresh evidence 失败。
- `session_started_at` < `session_ended_at`；同会话内多场景应共享 session 时间窗。
- `tool.name = manual` 时 `observations.md` 中每条 observation 必须显式追加 `manual: true`。

## `observations.md` 格式

```markdown
# Browser Testing Observations — <task-id>

- [observation] <现象简述>
  - scenario: <scenario-name>
  - layer: dom | console | network
  - evidence: <相对路径，例如 scenario-a/screenshots/02-error.png>
  - severity (initial): blocking | major | minor | nit
  - suggested next: hf-test-driven-dev | hf-test-review | hf-ui-review | gate
```

severity 初步判定的指引：

- `blocking`：阻断关键 user flow（页面崩溃、关键请求 5xx 全失败、关键 DOM 完全缺失）。
- `major`：影响功能正确性但有 workaround（部分请求 4xx、关键状态视觉错误、a11y AA 明显违反）。
- `minor`：影响体验但不影响完成（warning 噪音、文案、对齐）。
- `nit`：可忽略（极小视觉抖动、与本 task 不直接相关的历史告警）。

severity 由本 skill 给"初步判定"，**最终 severity 与 verdict 由下游 gate 决定**。

## Severity → canonical next action 映射

```text
0 blocking + 0 major  → hf-regression-gate
≥1 blocking           → hf-test-driven-dev   (回写 finding，要求修复)
0 blocking + ≥1 major → suggested next 中 majority 指向的节点
                        （typically hf-test-review 或 hf-ui-review）
only minor / nit      → hf-regression-gate    (作为 evidence + finding 一并交)
```

混合场景：以最高 severity 决定 next action；observations.md 中保留所有条目，不因 severity 删条目。

## 与下游节点的接力

- `hf-regression-gate`：把 `browser-evidence/<task-id>/` 整个目录纳入 evidence bundle；severity 取本 skill 的初判，再叠加 gate 自己的影响面分析。
- `hf-completion-gate`：仅消费 `observations.md` 中 `severity = blocking` 是否清零，作为 DoD 闭合条件之一。
- `hf-test-review` / `hf-ui-review`：当本 skill 把 observations 指回 review 时，review 节点把 observation 当作 reviewer-input，正常出 finding 与 verdict（不在本 skill 内执行）。

## 不在本 skill 内做的事

- 不执行 e2e 测试框架的「断言」逻辑——本 skill 只观察、记录，断言 / verdict 由下游 gate 完成。
- 不写 / 改 e2e 测试代码——若需要新测试，写 finding 回 `hf-test-driven-dev`。
- 不替代 `hf-ui-review` 的 Nielsen 启发式评估或 WCAG 2.2 AA 全量过 checklist。
- 不替代 `hf-regression-gate` 的影响面分析。
