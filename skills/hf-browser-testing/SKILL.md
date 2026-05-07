---
name: hf-browser-testing
description: Use when hf-test-driven-dev finishes GREEN on a frontend-touching active task whose spec declares a UI surface, and fresh browser runtime evidence (screenshot / console log / network trace) is required for downstream gates. Not for issuing verdicts (gates do that), not for replacing hf-test-review's test-quality review, not for backend-only tasks.
---

# HF 浏览器端运行时证据节点

HF workflow family 中 verify 阶段的 runtime evidence side node。对触碰前端表面的 active task，在 hf-test-driven-dev 的 GREEN 之后产生一份新鲜的浏览器运行时证据 bundle，供 hf-regression-gate / hf-completion-gate 消费。**不是 review，不是 gate，不签发 verdict**。

## When to Use

适用：

- 当前 active task 是前端 / UI 表面，且 spec 显式声明 UI surface（`hf-specify` 输出的 spec 中含 UI surface 声明，或 `hf-ui-design` 的设计已批准）。
- `hf-test-driven-dev` 已完成当前 task 的 GREEN，单元测试新鲜证据已在交接块中写回。
- 下游 gate（`hf-regression-gate` / `hf-completion-gate`）需要 runtime DOM / 控制台 / 网络层证据。

不适用：

- 后端 / CLI / 库类 task（无浏览器表面） → 跳过本 skill，直接由 hf-test-driven-dev 交接到下游。
- spec 未声明 UI surface 且 hf-ui-design 也未启动 → 越权，回 `hf-workflow-router`。
- 已经在审 verdict / 评测测试质量 → `hf-test-review`。
- 回归证据汇集 / DoD 判定 → `hf-regression-gate` / `hf-completion-gate`。
- 阶段不清 / 证据冲突 → `hf-workflow-router`。

前提：存在唯一 active task；feature 目录可写（默认 `features/<active>/`）；浏览器自动化工具链可用（Chrome DevTools MCP、Playwright、或项目已声明的等价工具）。工具链不可用 → fresh blocking evidence，不替换为"主观描述"。

## Hard Gates

- 主链触发时，`hf-test-driven-dev` 当前 task 的 GREEN 与新鲜单元证据必须先存在；缺位则不应启动本 skill。
- 浏览器证据**必须**在当前会话内产生（fresh evidence）；从历史目录复制 / 截图复用 → 视为未完成。
- 证据 bundle 至少包含三类：(a) DOM / 视觉证据（截图或 DOM 快照），(b) 控制台日志（含 error / warning），(c) 网络层证据（关键请求的 method / status / 关键响应字段或失败原因）。任一缺失 → fresh blocking evidence。
- 不签发 pass / fail verdict；只产出 evidence + 「问题清单」。verdict 由下游 gate 决定。
- 不修改实现代码；如发现实现缺陷 → 写 finding 并 reroute 回 `hf-test-driven-dev`，不在本 skill 内"顺手修一下"。
- 不修改测试代码；如测试覆盖不足 → 写 finding 并 reroute 回 `hf-test-review` / `hf-test-driven-dev`。

## Object Contract

- Primary Object：当前 active task 的浏览器运行时 evidence bundle。
- Frontend Input Object：hf-test-driven-dev 的 GREEN 交接块（含 SUT Form / Refactor Note / 单元测试 fresh evidence）+ 已批准 spec / ui-design / tasks 工件。
- Backend Output Object：落盘的 evidence bundle（截图 / DOM / console / network trace）+ 「问题清单」（observations，不是 verdict）+ canonical next action handoff。
- Object Transformation：从「单元层 GREEN」过渡到「runtime 层证据齐备」，把 task 的可验证面从「单测通过」扩展到「浏览器中观察到的真实行为」。
- Object Boundaries：不修改 spec / design / tasks / 实现代码 / 测试代码；不签发 verdict；不替代下游 gate 的 evidence bundle 汇集逻辑（`hf-regression-gate` 仍会重新读 evidence 做影响面判断）。
- Object Invariants：evidence 必须是当前会话产物；timestamps + commit SHA / worktree state 在 bundle metadata 中可回读。

## Methodology

| 方法 | 核心原则 | 来源 | 落地步骤 |
|------|----------|------|----------|
| **Runtime evidence over self-report** | 取浏览器真实行为而非"应该是这样"的口头判断 | 项目化实践（HF 证据链约定） | 步骤 2 — 启动浏览器；步骤 3 — 抓 evidence |
| **Three-layer evidence (DOM / Console / Network)** | 截图、控制台、网络三层证据并存以避免单层假阴 / 假阳 | Chrome DevTools 实践 + AS browser-testing-with-devtools | 步骤 3 — 三类必抓 |
| **Fresh evidence principle** | 所有证据必须当前会话内产生；带 timestamp + commit SHA | 项目化实践 | 步骤 1、5 — bundle metadata |
| **Observation, not verdict** | 本 skill 仅观察并写 finding；通过 / 不通过由下游 gate 决定 | Fagan / soul.md（不验收自己） | 步骤 4 — 问题清单写法；Hard Gates |
| **Walking-skeleton scenario** | 从 spec 声明的关键 UI surface 中挑选最小可观察 e2e 路径 | Cockburn — Walking Skeleton | 步骤 2 — 场景选取 |

## Workflow

### 1. 对齐上下文与触发条件

读 `features/<active>/progress.md` 的 Current Active Task → 校验 `hf-test-driven-dev` 是否完成 GREEN（交接块存在 + 单元 fresh evidence）→ 校验 spec / ui-design 是否声明 UI surface → 否则 reroute 回 `hf-workflow-router`。

- Object：active task + 交接块。
- Method：evidence-based precondition check。
- Input：`features/<active>/progress.md`、最新 hf-test-driven-dev 交接块。
- Output：触发判断（继续 / 跳过 / reroute）。
- Stop / continue：UI surface 缺位或 GREEN 未完成 → 停。

### 2. 选取浏览器场景与启动

依据 spec / ui-design 选取覆盖当前 task 的最小 walking-skeleton 场景（≤ 3 个关键 user flow）。启动浏览器自动化工具（推荐 Chrome DevTools MCP；Playwright / Puppeteer 等等价方案见 `references/runtime-evidence-protocol.md`）。

- Object：要观察的 user flow 列表。
- Method：Walking Skeleton + 关键路径优先。
- Input：spec UI surface 段、ui-design IA + interaction state inventory、当前 task 影响面。
- Output：场景脚本或交互步骤清单 + 浏览器 session。
- Stop / continue：工具不可用 → 写 fresh blocking evidence，停。

### 3. 抓取三层 evidence

按选定场景跑通后，对每个场景抓取：

- **DOM / 视觉**：full-page 截图（建议 + element 截图）；关键状态（hover / focus / disabled / loading / error / empty）至少各一张。
- **Console**：完整 console 日志（含 warn / error），按时序保留。
- **Network**：关键请求的 method / URL / status / 响应概要（敏感字段脱敏）+ 异常请求（4xx / 5xx）的全量记录。

落盘到 `features/<active>/verification/browser-evidence/<task-id>/<scenario>/`，每个场景一子目录；bundle metadata（`metadata.json`）必须包含：timestamps、commit SHA、worktree path、浏览器 / 工具版本、所用场景脚本路径。

- Object：runtime evidence 三层产物。
- Method：Three-layer evidence + fresh evidence principle。
- Input：浏览器 session、场景脚本。
- Output：evidence bundle 文件树。
- Stop / continue：任一层缺失 → fresh blocking evidence。

### 4. 写「问题清单」（observations，不是 verdict）

对每个 evidence 异常（console error、4xx / 5xx、未预期 DOM 状态、a11y 明显违反等）写一条 observation：

```markdown
- [observation] <现象简述>
  - scenario: <对应 user flow 名>
  - layer: dom | console | network
  - evidence: <相对路径>
  - severity (initial): blocking | major | minor | nit
  - suggested next: hf-test-driven-dev | hf-test-review | hf-ui-review | gate
```

**禁止**写"已通过"/"无问题"作为终态结论；终态由下游 gate 判定。

- Object：observation 清单。
- Method：Observation-not-verdict + Fagan 角色分离。
- Input：evidence bundle。
- Output：`features/<active>/verification/browser-evidence/<task-id>/observations.md`。
- Stop / continue：observation 缺 evidence 引用 → 不允许提交。

### 5. 写交接块并 handoff

向 active task 的 progress.md 追加 verify-stage handoff 块：

```markdown
## Browser Testing Handoff (<task-id>, <timestamp>)

- evidence bundle: features/<active>/verification/browser-evidence/<task-id>/
- scenarios covered: ...
- observations: <count> total (<blocking>/<major>/<minor>/<nit>)
- canonical next action:
  - 0 blocking + 0 major → hf-regression-gate
  - any blocking → hf-test-driven-dev (with finding)
  - major-only → hf-test-review or hf-ui-review (per suggested next)
```

canonical next action 唯一；不允许同时给出多个。

- Object：browser-testing 交接块。
- Method：Evidence-based handoff（与 family 其它节点一致）。
- Input：evidence bundle、observations。
- Output：progress.md 追加块；canonical next action。
- Stop / continue：next action 非唯一 → 视为未完成。

## Output Contract

- evidence 路径：`features/<active>/verification/browser-evidence/<task-id>/`
  - `metadata.json`：timestamps、commit SHA、worktree、工具版本、场景索引。
  - `<scenario>/screenshots/`、`<scenario>/console.log`、`<scenario>/network.har` 或 `<scenario>/network.json`。
  - `observations.md`：observation 清单。
- progress.md 追加 `## Browser Testing Handoff` 块。
- canonical next action：唯一一个 leaf skill / gate 名。

## Red Flags

- Console 有 error 但 observations 里没记录 → 三层证据未真正读完。
- 截图全是"happy path"无任何 hover / disabled / loading / error / empty 状态 → walking-skeleton 没真正覆盖关键状态。
- `metadata.json` 缺 commit SHA → 不构成 fresh evidence。
- handoff 给出多个 next action → 路由会被破坏，回写 finding。
- observation 中出现"verdict: pass/fail" → 越权，必须改写为 observation + suggested next。

## Common Mistakes

| 错误 | 问题 | 修复 |
|------|------|------|
| 直接复用 CI 上的截图 | 不是 fresh evidence | 当前会话内重跑 |
| 网络层只抓 200 OK | 漏 4xx/5xx 才是排错关键 | 至少把每个 4xx/5xx 落盘 |
| observation 不引用具体 evidence 文件路径 | 下游 gate 无法回读 | 每条 observation 必须有 `evidence:` 行 |
| 把 "通过" 写进 handoff | 越权签 verdict | 改成 observation + canonical next action |

## Common Rationalizations

| 借口 | 反驳 / Hard rule |
|------|-------------------|
| "单元测试都 GREEN 了，浏览器跑一下没必要。" | Hard Gates: spec 声明 UI surface 时本 skill 是 hf-test-driven-dev 后的 evidence 必经路径；省略导致下游 gate 缺 evidence。 |
| "用 dev 上的 staging 截图凑数。" | Hard Gates: fresh evidence 必须当前会话产生，metadata.json 必含 commit SHA + timestamp。 |
| "console 偶尔有 warning，不重要不记。" | Workflow stop rule (步骤 3): console 必须按时序保留 warn / error；筛选由下游 gate 决定，不在本 skill 裁。 |
| "我看着没问题，verdict pass。" | Hard Gates (soul.md / Fagan): 本 skill 只产 observation，不签 verdict；verdict 由 hf-regression-gate / hf-completion-gate 决定。 |
| "我顺手把 console error 对应的 bug 修了。" | Hard Gates: 不修改实现 / 测试代码；发现缺陷写 finding 并 reroute 回 hf-test-driven-dev。 |

## Reference Guide

- `references/runtime-evidence-protocol.md`：三层证据格式、metadata.json schema、Chrome DevTools MCP / Playwright 等工具的等价命令。

## Verification

- `features/<active>/verification/browser-evidence/<task-id>/metadata.json` 存在且含 commit SHA + timestamp。
- 每个声明的 scenario 子目录下三层 evidence 都存在。
- `observations.md` 落盘且每条 observation 引用具体 evidence 路径。
- progress.md 中 `## Browser Testing Handoff` 块存在且 canonical next action 唯一。
- 未签发任何 verdict 字样（pass / fail / approved / rejected）。
