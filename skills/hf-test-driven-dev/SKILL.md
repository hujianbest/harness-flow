---
name: hf-test-driven-dev
description: 适用于任务计划获批后的单任务实现、受控 hotfix 修复实现、review/gate 回流修订。不适用于任务计划未批准（→ 上游）、hotfix 无复现路径（→ hf-hotfix）、需并行多任务（→ hf-workflow-router）。
---

# HF 测试驱动开发与实现入口

HF workflow family 唯一实现入口。把单个活跃任务从"准备实现"推进到"已写回新鲜证据与 canonical 下一步"。不是任务循环控制器——跨 task 切换由 `hf-workflow-router` 决定。

三层职责：1) 唯一实现入口 2) TDD 执行入口 3) 向 review/gate 输出证据与 handoff 的交接入口。

## Methodology

本 skill 融合以下已验证方法。每个方法在 Workflow 中有对应的落地步骤。

| 方法 | 核心原则 | 来源 | 落地步骤 |
|------|----------|------|----------|
| **TDD (Test-Driven Development)** | 严格遵循 Red → Green → Refactor 循环 | Kent Beck, 2002 "Test-Driven Development: By Example" | 步骤 4 — 执行有效 TDD |
| **Walking Skeleton** | 优先建立最薄端到端可运行路径 | Alistair Cockburn, "Software Development as a Cooperative Game" | 步骤 4 — TDD 中优先走通关键路径 |
| **Test Design Before Implementation** | 在 Red-Green-Refactor 前完成测试设计 approval step | 项目化实践（HF 质量链约定） | 步骤 2 — 产出测试设计；步骤 3 — approval step |
| **Fresh Evidence Principle** | 所有验证证据必须在当前会话内产生 | 项目化实践（HF 证据链约定） | 步骤 4 — 有效 RED/GREEN；步骤 5 — 交接块 |

## When to Use

适用：
- 任务计划获批后的实现（full/standard/lightweight）
- 受控 hotfix 的修复实现
- 来自 bug-patterns/test-review/code-review/traceability-review/regression-gate/completion-gate 的回流修订
- 用户要求"开始实现这个 active task"

不适用：任务计划未批准 → 回上游；hotfix 无复现路径 → `hf-hotfix`；需并行多任务 → `hf-workflow-router`。

前提：存在唯一活跃任务、有已批准计划或 hotfix handoff、能读取 feature `progress.md`（默认 `features/<active>/progress.md`）和规格/设计锚点（默认 `features/<active>/spec.md` / `features/<active>/design.md`）。证据冲突 → 回 router。

## Hard Gates

- 主链实现时，任务计划未获批准前不得开始
- hotfix 实现时，必须有 `hf-hotfix` 的复现路径和最小修复边界
- 当前任务完成质量链前不得切换到下一任务
- 若 worktree-required，动手前必须先准备 worktree
- Red-Green-Refactor 前必须完成测试设计 approval step
- 写回 fresh evidence 和 canonical handoff 前不得声称完成

## Workflow

### 1. 对齐上下文并锁定唯一活跃任务

读 feature `progress.md`（默认 `features/<active>/progress.md`）的 Current Active Task → 校验任务计划（默认 `features/<active>/tasks.md`）/hotfix handoff → 补读回流 findings → 证据冲突则暂停。

### 1A. 按需准备 worktree

- `worktree-active`：复用 Worktree Path
- `worktree-required`：按当前 skill pack 共享的 worktree isolation guide 准备（默认 `skills/docs/hf-worktree-isolation.md`；若 `AGENTS.md` 声明项目等价路径，优先遵循）
- `in-place`：仅干净工作区时继续
- 准备失败 → fresh blocking evidence，不先改代码再补 worktree

### 2. 产出测试设计并自检

TDD 前先输出测试设计：验证哪些行为、正反向场景、边界条件、预期 I/O、哪些应先失败、测试分层、与测试设计种子的差异。

自检：覆盖关键成功行为？覆盖反向/边界？能抓住"错误但看起来完成了"的实现？mock 限定在真正边界？

### 3. 完成测试设计确认

整理成可回读确认输入。interactive → 展示给真人等待确认；auto → 写 approval record。完成后才能进入 TDD。

### 4. 执行有效 TDD

1. 先写失败测试 → 运行确认失败原因符合预期
2. 写最小实现让测试通过 → 运行确认新通过来自本次会话
3. 全绿后做最小重构

**有效 RED**：会话里真的执行了、失败对应行为缺口、能说清为什么预期失败。

不算有效 RED：只写没跑、一跑就绿、无关旧失败、看不出在证明什么。

**有效 GREEN**：任务测试转绿、证明命令本次会话成功、保留 fresh evidence。

### 5. 生成实现交接块并同步状态

写回稳定交接块：

```md
## 实现交接块
- Task ID:
- 回流来源: 主链实现 | hf-hotfix | hf-bug-patterns | ...
- 触碰工件:
- Workspace Isolation / Worktree Path / Worktree Branch:
- 测试设计确认证据:
- RED 证据: <命令 + 失败摘要 + 为什么预期失败>
- GREEN 证据: <命令 + 通过摘要 + 关键结果>
- 与任务计划测试种子的差异:
- 剩余风险 / 未覆盖项:
- Pending Reviews And Gates:
- Next Action Or Recommended Skill:
```

Next Action 用 canonical skill ID：full/standard 通常 → `hf-test-review`；lightweight 通常 → `hf-regression-gate`；回流修订完成 → 写回触发回流的那个 node。不把下一任务的实现写成输出。若 AI 发现当前问题命中了值得长期沉淀的重复错误，可**额外建议**独立触发 `hf-bug-patterns`，但不要把它写成 HF 主链的 canonical next action。

### 6. 回流修订协议

明确回流来源 → 只修当前活跃任务的相关 findings → 若改行为预期需重做测试设计确认 → 修订后写新 fresh evidence → 不从头重走质量链。

## 和其他 Skill 的区别

| 场景 | 用 hf-test-driven-dev | 不用 |
|------|----------------------|------|
| 任务计划获批后的单任务 TDD 实现 | ✅ | |
| review/gate 回流修订 | ✅ | |
| 任务计划未批准 | | → 上游（`hf-tasks` / `hf-workflow-router`） |
| 热修复但无复现路径 | | → `hf-hotfix` |
| 需并行多任务 | | → `hf-workflow-router` |
| 评审测试质量 | | → `hf-test-review` |
| 评审代码质量 | | → `hf-code-review` |
| 评审追溯完整性 | | → `hf-traceability-review` |

## Red Flags

- 并行处理多个任务
- 未完成测试设计 approval step 就开始写测试
- 先写实现再补失败测试
- 旧绿测结果当当前证据
- completion gate 前就说"做完了"
- 不读 feature `progress.md` 靠印象决定活跃任务
- 把命令日志、性能基线等大体量证据塞进 progress.md / 实现交接块，而不是落到 `features/<active>/evidence/`
- 测试直接通过却没重新定义要抓的行为

## Supporting References

| 文件 | 用途 |
|------|------|
| `references/cpp-gtest-deep-guide.md` | C++/GoogleTest/CMake 栈深度参考 |
| `references/testing-anti-patterns.md` | C++ 测试反模式（mock 误用、测试专用方法等） |
| `skills/docs/hf-worktree-isolation.md` | 当前 skill pack 共享的 Worktree 隔离操作指南；若 `AGENTS.md` 声明项目等价路径，优先遵循 |

C++/GoogleTest 项目且需要语言级细节时才加载深度参考。非 C++ 也必须遵守同一实现契约。

## Verification

- [ ] 围绕唯一活跃任务推进
- [ ] worktree 已准备（若需要）
- [ ] 测试设计已完成 approval step（approval record 落在 `features/<active>/approvals/`）
- [ ] 留下有效 RED 与 GREEN 证据；体量大的原始日志/基线落在 `features/<active>/evidence/`
- [ ] 实现交接块已写回，含 canonical Next Action
- [ ] feature `progress.md` 已同步
- [ ] 未私自重排后续质量链
