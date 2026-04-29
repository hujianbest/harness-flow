# Test Review — Task-001 (Walking-skeleton e2e)

- 节点: `hf-test-review`
- Reviewer Role: Independent Reviewer
- Date: 2026-04-29
- Task: T1 — Walking-skeleton end-to-end
- Test Files Reviewed:
  - `test/walking-skeleton.test.ts`
  - `test/markdown-parser.test.ts`
  - `test/medium-adapter.test.ts`
  - `test/zhihu-adapter.test.ts`
  - `test/wechat-mp-adapter.test.ts`
  - `test/publish-service.test.ts`
- Evidence:
  - RED log: `evidence/task-001-red.log`
  - GREEN log: `evidence/task-001-green.log`

## Verdict

`通过`

## Fail-First Validation

| 测试 | 是否在 RED 阶段失败 | 证据 |
|---|---|---|
| `walking-skeleton.test.ts` 全部 5 条 | ✅ | RED log: `Failed Suites 6 ⎯ FAIL test/walking-skeleton.test.ts ... Failed to load url ../src/...` |
| `markdown-parser.test.ts` | ✅ | RED log: `FAIL test/markdown-parser.test.ts` |
| `medium-adapter.test.ts` | ✅ | RED log: `FAIL test/medium-adapter.test.ts` |
| `zhihu-adapter.test.ts` | ✅ | RED log: `FAIL test/zhihu-adapter.test.ts` |
| `wechat-mp-adapter.test.ts` | ✅ | RED log: `FAIL test/wechat-mp-adapter.test.ts` |
| `publish-service.test.ts` | ✅ | RED log: `FAIL test/publish-service.test.ts` |

Fresh evidence anchor：6 个测试文件在 src/ 目录尚未创建时全部加载失败（"Does the file exist?"），证明测试**先于**实现存在。这是 Canon TDD RED 的标准信号。

GREEN 证据：23/23 测试通过；运行时长 364 ms（满足 NFR-Testability-1 的 < 1 s 阈值）。

## Coverage Categories

| 类别 | 是否覆盖 | 证据 |
|---|---|---|
| **Happy path** | ✅ | walking-skeleton 第 1 个测试：post.md → MediumAdapter → 1 条 RecordedRequest |
| **Failure paths (per spec NFR-Reliability-1)** | ✅ | UNKNOWN_PLATFORM / NOT_IMPLEMENTED / FILE_NOT_FOUND / PARSE_FAILED / HTTP_FAILED / INTERNAL 全部有测试 |
| **Boundary conditions** | ✅ | dryRun=true（不调 HTTP）；缺 H1 标题（PARSE_FAILED）；adapter 抛错（INTERNAL）|
| **Contract invariants** (per `platform-adapter.contract.md`) | ✅ | Invariant 1：`publish-service.test.ts` "never throws — internal exceptions are wrapped to INTERNAL"；Invariant 2：Zhihu/WeChatMp 测试覆盖 `notImplemented = true` + 任意 options 都返回 NOT_IMPLEMENTED；Invariant 3：每个 adapter 单元测试断言 `.name` 是 stable 字符串 |
| **NFR Acceptance** | ✅ | NFR-Maintainability-1：`publish-service.test.ts` 第 4 条用 `fakeAdapter` 注入证明加 adapter 不动 publish-service.ts；NFR-Testability-1：23 测试全部用 RecordingHttpClient（0 socket）+ 364 ms < 1 s |
| **Bug-pattern coverage** | ⚠️ 适度 | demo 不要求历史 bug pattern 回归（`docs/bug-patterns/` 未启用）|

## Anti-Pattern Sweep

| 反模式 | 是否触发 | 备注 |
|---|---|---|
| 测试与实现同时写（"先实现再补测试"） | 否 | RED log 在源码不存在时已存在测试 |
| 用 `expect(true).toBe(true)` 等空壳测试凑数 | 否 | 23 测试每条都有非平凡断言 |
| 用真实网络 / 真实文件系统污染测试 | ⚠️ 部分使用 `tmpdir + writeFileSync` | publish-service.test.ts 使用 `mkdtempSync`+ `tmpdir` 写临时文件——属合理 sandbox 用法，不污染 repo |
| Mock 内部模块导致测试脱离实际行为 | 否 | 仅 mock HttpClient（外部边界），其它链路均使用真实 PublishService / MarkdownParser / Adapter |
| 一次断言只断言 `result.ok === true` 不查 payload | 否 | walking-skeleton.test.ts 第 1 条断言 payload 含 title + 代码块原文 |

## Findings

无重大问题。观察：

1. RED log 显示的是"模块不存在"型失败（vitest 在 import 阶段就 abort），这是 walking skeleton 第一刀的典型形态。如果未来 task 已经有部分实现，RED 会变成"断言失败"型——形式不同但语义一致。
2. `publish-service.test.ts` 中的 `fakeAdapter` 显式以**普通对象**（非 class）注入，证明 `PlatformAdapter` interface 是结构化类型（duck typing），不强迫调用方继承基类——和 contract.md 一致。
3. GREEN log 显示 medium-adapter "payload 含代码块原文" 这条测试在第一次 GREEN 时失败，被 fix 后通过。这种"先发现真实 bug 再修"是 TDD 应有的产物，不是缺陷——但 evidence 文件因覆盖只保留最新一次 GREEN。建议未来在 `evidence/` 内保留中间版本时使用 `task-001-green-N.log` 序号后缀。
4. 测试中没有显式断言"e2e 总时长 < 1 s"——靠 vitest 整体时长达成。如果未来 demo 真要把这条作为 hard NFR，应加 `Date.now()` 包测试体。

## Conclusion

- Conclusion: `通过`
- Next Action Or Recommended Skill: `hf-code-review`
