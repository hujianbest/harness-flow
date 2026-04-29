# ADR-0002: Use a `PlatformAdapter` interface as the only extension boundary for new platforms

- 状态: accepted
- 日期: 2026-04-29
- 决策人: cursor agent (per user delegation, demo scope)
- Supersedes: —
- Superseded-by: —

## Context

WriteOnce v0 walking skeleton 必须同时满足两个看起来矛盾的诉求：

1. **窄**——walking-skeleton 只实现一个平台（Medium），且 demo 不真集成 Medium API。
2. **可扩展**——design 必须能让 reviewer 看出"以后接入 Zhihu / WeChat MP 不会推倒重来"。

NFR-Maintainability-1 要求"加一个新平台 = 加一个 adapter 文件 + 一行注册"。FR-3 与 NFR-Maintainability-1 都把 `PlatformAdapter` 抽象作为 walking skeleton 的硬骨头。

候选方案（同 design.md section 8）：

- 方案 X：`PlatformAdapter` 接口 + Map 注册。
- 方案 Y：直接在 `publish-service.ts` 内 `if-else` 分发到具名函数。
- 方案 Z：插件机制（动态加载 npm 模块）。

## Decision

采用**方案 X**：定义 `PlatformAdapter` interface（`publish(post: Post, options): Promise<PublishResult>`），具体平台实现该 interface，注册到 `publish-service.ts` 顶部的 `adapters: Map<string, PlatformAdapter>`。

`publish-service.ts` 自身不感知任何具体平台名称，只通过 `adapters.get(name)` 查找；找不到时返回结构化错误（"unknown platform"），找到但实现声明 `notImplemented = true` 时返回结构化错误（"not implemented in v0"）。

## Consequences

正面：
- 满足 FR-3 与 NFR-Maintainability-1。
- 后续平台对接的 PR 不动 `publish-service.ts`。
- `--to all` 的语义是"遍历 `adapters` 全部值并独立执行"，不需要为新平台改 dispatcher。

负面：
- Map 注册是中央化点，如果 future demo 升级要支持运行时插件，仍要改这一处（可逆，方案 Z 是后续可选升级）。
- adapter 接口的稳定性（Hyrum's Law）会成为 future 风险——v0 仅 1 个真实实现，未来如果接入更多 adapter 需要再开 ADR 复审接口。

中性：
- adapter 之间不直接通信；任何"跨平台"逻辑（例如发布失败回滚）都必须落到 `publish-service.ts`，不允许藏在某个 adapter 里。

## 可逆性评估

中等。改回方案 Y（if-else 分发）需要把 6 行注册代码拆成 dispatch 内部分支，约 30 分钟工作量。
