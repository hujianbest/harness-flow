# WriteOnce Demo Changelog

This is the **demo-internal** changelog. It is independent of HarnessFlow's repository-root `CHANGELOG.md` (which tracks the HarnessFlow skill pack itself).

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
