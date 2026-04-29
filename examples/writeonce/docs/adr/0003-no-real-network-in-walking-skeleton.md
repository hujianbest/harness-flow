# ADR-0003: No real network calls in the walking skeleton; HTTP is injected via `HttpClient` interface

- 状态: accepted
- 日期: 2026-04-29
- 决策人: cursor agent (per user delegation, demo scope)
- Supersedes: —
- Superseded-by: —

## Context

NFR-Testability-1 要求 walking-skeleton end-to-end 测试在离线机器上 < 1 s 通过；spec.md section 11 显式禁止 walking-skeleton 中发起真实网络请求。HYP-V-1 也明确 demo 不追求真实 Medium 集成。

候选方案：

- 方案 P：定义 `HttpClient` interface，`MediumAdapter` 通过构造注入；测试中用一个内存实现替换。
- 方案 Q：使用 `nock` 等 HTTP mock 库拦截真实 fetch。
- 方案 R：完全不写网络层，把 `MediumAdapter.publish` 在 walking skeleton 中直接返回 stub。

## Decision

采用**方案 P**：`MediumAdapter` 依赖 `HttpClient` interface（`request(url, init): Promise<HttpResponse>`），构造时注入。

- 默认运行时实现 `Node20FetchHttpClient`：内部调用 `globalThis.fetch`（Node 20 内置），但 walking skeleton 的真实 publish 路径**不**会被 demo 执行（CLI 默认走测试路径，因为 demo 不真集成）。
- 测试时实现 `RecordingHttpClient`：拦截 `request` 调用并记录 payload，不走任何 socket。

理由：
- 方案 P 同时满足 NFR-Testability-1（测试 < 1 s 离线）和"adapter 形态真实可读"。
- 方案 Q 引入 `nock` 等大依赖，且 walking skeleton 不需要这种复杂度。
- 方案 R 让 `MediumAdapter` 形同虚设，design 失去说服力，违反 HYP-F-2。

## Consequences

正面：
- 测试 100% 离线 + 快速。
- `MediumAdapter` 在 v0 walking skeleton 中"几乎"和真实集成时长得一样（只少了真实 HTTP），减少未来真集成时的改动面。
- `HttpClient` 是 Hyrum-safe 的窄接口，只暴露 `request(url, init): Promise<HttpResponse>`。

负面：
- 没有真实网络验证 → demo **不能**作为 Medium 集成的可工作样本（demo README "Limits" 已说明）。
- `Node20FetchHttpClient` 在 demo 中不会被走到，但仍要保留，否则 future 真集成需要重写。

中性：
- `HttpClient` 也可以用于未来 Zhihu / WeChat MP adapter；但本 ADR 不预设那种用法。

## 可逆性评估

高。任意时点可以删除 `HttpClient` 接口、把 fetch 直接调用回 adapter 内；唯一影响是离线测试要重写。
