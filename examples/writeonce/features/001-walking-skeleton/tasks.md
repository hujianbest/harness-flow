# WriteOnce Walking Skeleton 任务计划

- 状态: 已批准（tasks-review 2026-04-29 通过）
- 主题: Markdown → Medium walking-skeleton 实现 + PlatformAdapter 抽象
- 上游: `features/001-walking-skeleton/design.md`（已批准）

## 1. 概述

按 Walking Skeleton 纪律，本 feature **只锁 1 个 Current Active Task**：把"读取 Markdown → 通过 PlatformAdapter 调用 Medium → RecordingHttpClient 收到 1 条请求"这条端到端路径打通，并以 RED/GREEN evidence 落地。

其余任务（T2–T4）作为本 feature 的后续候选，但**不**在 v0.1.0 demo 范围内被实现。Demo 的 success metric (Threshold (a)) 只要求 walking-skeleton e2e 路径绿；其它候选任务以"未实现 + traceable" 形式存在。

## 2. 里程碑

| 里程碑 | 含义 | 内容 |
|---|---|---|
| M-task-001 | walking-skeleton e2e 绿 | T1 完成；测试 100% 通过；evidence 齐 |
| M-feature-closeout | 本 feature closeout | regression / doc-freshness / completion 全绿；closeout.md 写完 |

## 3. 文件 / 工件影响图

```
src/
├── cli.ts                              [新增, T4 范围；T1 走 publish-service 直接调用]
├── parser/
│   └── markdown-parser.ts              [新增, T1]
├── platform/
│   ├── platform-adapter.ts             [新增, T1（接口）]
│   ├── http-client.ts                  [新增, T1（接口 + RecordingHttpClient）]
│   ├── medium-adapter.ts               [新增, T1]
│   ├── zhihu-adapter.ts                [新增, T2]
│   └── wechat-mp-adapter.ts            [新增, T2]
└── publish/
    └── publish-service.ts              [新增, T1（含 --to all 串行 dispatcher 雏形）]

test/
├── walking-skeleton.test.ts            [新增, T1]
├── markdown-parser.test.ts             [新增, T1]
├── publish-service.test.ts             [新增, T1]
├── medium-adapter.test.ts              [新增, T1]
├── zhihu-adapter.test.ts               [新增, T2]
└── wechat-mp-adapter.test.ts           [新增, T2]

package.json                            [新增, T1]
tsconfig.json                           [新增, T1]
```

T2 / T3 / T4 不在 v0.1.0 demo 实现范围内，列在影响图中是为了让 traceability-review 能看出"未来落点"。

## 4. 需求与设计追溯

| 任务 | 承接 FR | 承接 NFR | 设计章节 |
|---|---|---|---|
| T1 | FR-1, FR-3, FR-4, FR-5 | NFR-Reliability-1, NFR-Maintainability-1, NFR-Testability-1 | design section 11 / 12 / 14 / 16 |
| T2 | FR-2 (扩展点真实性) | NFR-Maintainability-1 | design section 11 / 14 |
| T3 | FR-6 | NFR-Reliability-1 | design section 12 |
| T4 | FR-1（CLI 入口） | NFR-Reliability-1（CLI 错误码翻译） | design section 11 |

## 5. 任务拆解

### T1. Walking-skeleton end-to-end (MUST, in v0.1.0)

- **目标**：实现从 Markdown 文件到 RecordingHttpClient 收到 1 条请求的最薄端到端路径。
- **Acceptance**：
  - `walking-skeleton.test.ts` 中 1 条 e2e 测试绿：读 fixture `post.md` → `PublishService.publish('post.md', { to: 'medium' })` → `RecordingHttpClient.requests.length === 1` → request payload 含 title 与 fenced code block 内容。
  - 全套单元测试绿：`MarkdownParser`、`PublishService`（含 unknown / not-implemented / file-not-found / 正常）、`MediumAdapter`（含 dryRun）。
  - 所有失败路径返回 `{ ok: false, code, message }`，无未捕获异常（NFR-Reliability-1）。
  - `vitest` 全套运行时间 < 2 s 离线。
- **依赖**：无（首任务）。
- **Ready When**：design + contract 已批准；`package.json` / `tsconfig.json` 准备好。
- **初始队列状态**：`active`
- **Selection Priority**：1（唯一）
- **Files / 触碰工件**：见 section 3 中标 T1 的所有文件 + `package.json` + `tsconfig.json`
- **测试设计种子**：
  - RED 1：`walking-skeleton.test.ts` 在没有任何实现下应失败（缺类）。
  - RED 2：`PublishService.publish` 对 unknown platform 应返回 `{ ok:false, code:'UNKNOWN_PLATFORM' }`。
  - RED 3：`MediumAdapter.publish` 在 dryRun 时不应调用 `HttpClient.request`。
- **Verify**：`npx vitest run`；evidence 落 `evidence/task-001-red.log` 与 `evidence/task-001-green.log`。
- **预期证据**：RED log 至少 3 条 failing；GREEN log 全绿；测试运行时间记录。
- **完成条件**：Acceptance 全部满足；`hf-test-review` + `hf-code-review` + `hf-traceability-review` 全部 `通过`；`hf-regression-gate` + `hf-completion-gate` `通过`。

### T2. NotImplemented adapters (Should, deferred to v0.x)

- **目标**：实现 `ZhihuAdapter` 与 `WeChatMpAdapter`，`notImplemented = true`，`publish` 直接返回 `{ ok:false, code:'NOT_IMPLEMENTED', ... }`。
- **Acceptance**：spec FR-2 acceptance；contract.md Invariant 2。
- **依赖**：T1 完成。
- **初始队列状态**：`pending`
- **Selection Priority**：2
- **v0.1.0 demo 范围**：**否**——T2 留作 traceable backlog；本 feature 在 closeout 时声明该任务作为"已规划未实现"，不阻塞 closeout。

### T3. `--to all` dispatcher (Should, deferred)

- **目标**：在 `PublishService` 中实现 `--to all` 遍历 `adapters` Map 的串行 dispatcher。
- **Acceptance**：FR-6 acceptance（结果数组 3 entries）。
- **依赖**：T1 + T2 完成。
- **初始队列状态**：`pending`
- **Selection Priority**：3
- **v0.1.0 demo 范围**：**否**。

### T4. CLI flag parsing & exit code translation (Must for ergonomic, deferred)

- **目标**：用 `commander` 实现 `cli.ts`，把 `PublishService` 的 PublishResult 翻译成 stdout / stderr / exit code。
- **Acceptance**：单元测试覆盖 `cli.ts` 的退出码翻译表。
- **依赖**：T1 完成。
- **初始队列状态**：`pending`
- **Selection Priority**：4
- **v0.1.0 demo 范围**：**否**——demo 直接通过 `PublishService` 跑 e2e 测试就足以证明 walking skeleton 端到端打通；CLI 的 ergonomic 留到 v0.x。

## 6. 依赖与关键路径

```
T1 (walking-skeleton e2e) ─┬─▶ T2 (notImpl adapters)
                           ├─▶ T3 (--to all)
                           └─▶ T4 (CLI ergonomic)
```

关键路径：T1 是阻塞所有其它任务的前置；T2/T3/T4 在 T1 完成后可并行。本 feature 在 v0.1.0 只关心 T1；其它任务作为 "已规划但 v0.1.0 不实现" backlog 进入 closeout 注记。

## 7. 完成定义与验证策略

T1 的 Definition of Done（DoD）：

- [ ] `npx vitest run` 全绿，e2e 测试包含 walking-skeleton.test.ts
- [ ] RED/GREEN evidence log 落 `evidence/`
- [ ] `hf-test-review`、`hf-code-review`、`hf-traceability-review` 各产出 `通过` review 文档
- [ ] `hf-regression-gate` 产出 `通过`
- [ ] `hf-completion-gate` 产出 `通过`
- [ ] feature `progress.md` 同步：Current Active Task 翻为 `task-001-completed`；Next Action Or Recommended Skill 翻为 `hf-finalize`

Feature workflow-closeout DoD：

- [ ] T1 DoD 全部满足
- [ ] T2/T3/T4 在 closeout 中作为 "regular backlog（v0.x）" 显式声明，**不**作为 blocker
- [ ] `closeout.md` 写完，`Release / Docs Sync` 段列出 ADR-0001/0002/0003 状态、demo `CHANGELOG.md` 更新、`examples/writeonce/README.md` 更新

## 8. 当前活跃任务选择规则

- v0.1.0 demo 内：始终为 T1。
- 当 T1 完成且 closeout 触发时：进入 workflow-closeout 路径，不再选下一任务。

## 9. 任务队列投影视图 / Task Board Path

不启用独立 task-board.md（仅 4 个候选任务，且只 1 个在 v0.1.0 实现，无需 task-to-task 自动推进）。本节即作队列视图。

## 10. 风险与顺序说明

- T1 即整个 demo 的"hard 骨头"。任何"先实现 T2/T3/T4 增加 demo 表面"的诱惑都属反模式（违反 Walking Skeleton + ADR-001 D9 "demo 是 HF 主链留下可读痕迹，不是产品成熟度比拼"）。
- T2 作为 "声明扩展点 + 不实现" 是 design 中 `notImplemented = true` 约定的活样本——v0.x 真要实现时直接把 `notImplemented` 删掉 + 实现 `publish` 即可。
