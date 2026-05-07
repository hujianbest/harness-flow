# WriteOnce Demo Changelog

This is the **demo-internal** changelog. It is independent of HarnessFlow's repository-root `CHANGELOG.md` (which tracks the HarnessFlow skill pack itself).

## [Unreleased] — HF v0.2.0 refresh

> 触发：HarnessFlow 升级到 v0.2.0 pre-release（参见 HF 仓库根 `CHANGELOG.md` `[Unreleased] / Planned (v0.2.0)` 段 + `docs/decisions/ADR-002-release-scope-v0.2.0.md`）。**demo 工件、实现、测试均不变**；只补一份 v0.2.0 新节点的 evidence-based 激活核对痕迹。

### Added

- `features/001-walking-skeleton/verification/browser-testing-skip-2026-05-07.md` — HF v0.2.0 新增节点 `hf-browser-testing`（verify-stage runtime evidence side node，ADR-002 D1 / D7）的激活规则核对记录。结论 **SKIP**：spec 未声明 UI surface 且 task-001 模块边界未触碰前端，激活规则 2/3 均不命中（条件 1 GREEN 已满足）。4 条独立旁证（spec-review verdict / closeout matrix / feature README artifacts / spec.md grep）同向支持 SKIP。

### Notes

- 新增的 `hf-browser-testing` 是 v0.2.0 首个对外承诺面新增工程节点（其余 R3/R4/R5 由 ADR-002 D11 撤回到 v0.3+，不影响本 demo）。
- demo 受 HF 升级影响的范围**仅限 evidence 痕迹补全**：`closeout.md` Evidence Matrix、`features/001-walking-skeleton/README.md` Artifacts + Reviews & Approvals 表、`progress.md` Progress Notes / Evidence Paths 各加一条对应 SKIP 记录的索引行。
- demo 不改代码 / 测试 / spec / design / tasks / 任何 review verdict / 任何 gate verdict（与 ADR-001 D9 "demo 的 deliverable 是 HF 主链工件痕迹，不是产品本身" 一致）。
- 当 writeonce 后续真的引入 UI surface 时（例如 web 化的发布预览），spec 会显式声明 UI surface，`hf-ui-design` + `hf-ui-review` 与 `hf-browser-testing` 都会被 router 自动激活，届时本 SKIP 记录自然失效。

## [0.1.0] - 2026-04-29

First and only WriteOnce release for the HarnessFlow v0.1.0 quickstart demo.

### Added

- `examples/writeonce/README.md` — demo overview, scope, layout, limits.
- `docs/insights/2026-04-29-writeonce-discovery.md` — `hf-product-discovery` output.
- `docs/insights/2026-04-29-writeonce-spec-bridge.md` — bridge for `hf-specify`.
- `docs/adr/0001-record-architecture-decisions.md` — ADR pool boot.
- `docs/adr/0002-platform-adapter-as-extension-boundary.md` — selected adapter Map approach.
- `docs/adr/0003-no-real-network-in-walking-skeleton.md` — selected `HttpClient` injection approach.
- `features/001-walking-skeleton/` — full HarnessFlow main-chain artifact set:
  - `spec.md`, `design.md`, `tasks.md`, `progress.md`, `closeout.md`
  - `contracts/platform-adapter.contract.md`
  - `reviews/` — discovery / spec / design / tasks reviews + per-task test / code / traceability reviews
  - `approvals/` — discovery / spec / design / tasks approvals
  - `verification/` — regression record + completion record
  - `evidence/` — RED / GREEN / regression test logs
- `src/` — walking-skeleton implementation (TypeScript, Node 20+):
  - `parser/markdown-parser.ts` — minimal CommonMark subset.
  - `platform/platform-adapter.ts` — `PlatformAdapter` interface + `PublishResult` union.
  - `platform/http-client.ts` — `HttpClient` interface + `RecordingHttpClient` test double + `Node20FetchHttpClient`.
  - `platform/medium-adapter.ts` — Medium adapter (walking-skeleton implementation).
  - `platform/zhihu-adapter.ts` — extension point only (`notImplemented = true`).
  - `platform/wechat-mp-adapter.ts` — extension point only.
  - `publish/publish-service.ts` — Markdown → adapter dispatch with structured failure handling.
- `test/` — 23 unit + e2e tests (vitest), all passing in 367 ms; offline; no real network.
- `package.json`, `tsconfig.json`, `vitest.config.ts` — TypeScript strict + Node 20+ engine.

### Decided (locked by cursor agent per user delegation, see discovery section 0)

- Target users = technical content creators.
- Initial platforms = Medium (implemented), Zhihu + WeChat MP (extension points only).
- MVP boundary = single Markdown source → publish; no comment sync / analytics back-flow / scheduling.
- Tech stack = Node.js 20 + TypeScript + minimal CLI.
- Walking-skeleton scope = Medium end-to-end via TDD; other adapters declared but not implemented.

### Deferred (to v0.x of the demo)

- Real Medium API integration (OAuth / token / rate limits).
- Real Zhihu / WeChat MP integration.
- T3: `--to all` dispatcher.
- T4: `cli.ts` CLI ergonomic layer (commander wiring + exit code translation).
- Notion / Obsidian / multi-file source.
- GUI / Electron.
- CI/CD pipeline (consistent with HarnessFlow ADR-001 D1 P-Honest — release/ops out of v0.1.0).

### Notes

- This demo does **not** publish to a real Medium account.
- All HTTP calls are intercepted by `RecordingHttpClient`; tests are 100% offline.
- The demo's `docs/adr/` is independent of the HarnessFlow repository-root `docs/decisions/`.

[0.1.0]: https://github.com/hujianbest/harness-flow/tree/main/examples/writeonce
