# PlatformAdapter Contract (Draft)

- 状态: 草稿（design 内部契约）
- 主题: WriteOnce v0 walking skeleton 的 `PlatformAdapter` 接口契约
- 生效: 本 feature 实现 + 后续平台 adapter 实现
- Canonical 实现位置: `examples/writeonce/src/platform/platform-adapter.ts`

## TypeScript 接口（规范）

```typescript
export interface Post {
  title: string;
  body: string;            // raw markdown body without title line
  codeBlocks: Array<{ lang?: string; code: string }>;
  images: Array<{ alt: string; src: string }>;
}

export interface PublishOptions {
  dryRun?: boolean;
}

export type PublishResult =
  | { ok: true; payload: unknown }
  | { ok: false; code: string; message: string };

export interface PlatformAdapter {
  /** Stable platform identifier used in CLI `--to <name>`. */
  readonly name: string;

  /**
   * Walking-skeleton signal:
   * `true` = adapter is declared as an extension point but not implemented.
   * Such adapters MUST return `{ ok:false, code:'NOT_IMPLEMENTED', message:... }` from `publish`.
   */
  readonly notImplemented?: boolean;

  publish(post: Post, options: PublishOptions): Promise<PublishResult>;
}
```

## Invariants

1. `publish` MUST resolve; it MUST NOT throw or reject the promise.
   - Any internal throw must be wrapped into `{ ok:false, code:'INTERNAL', message }`.
2. When `notImplemented === true`, `publish` MUST resolve to `{ ok:false, code:'NOT_IMPLEMENTED', message }` regardless of `options`.
3. The `name` field MUST be a stable, lowercase, kebab-case identifier (e.g. `medium`, `zhihu`, `wechat-mp`).
4. Adapters MUST NOT perform any I/O outside the injected `HttpClient` (filesystem reads belong to `MarkdownParser`, not to adapters).

## Error code vocabulary (controlled)

| code | 何时 | 谁返回 |
|---|---|---|
| `FILE_NOT_FOUND` | 输入 markdown 文件不存在 / 不可读 | PublishService |
| `PARSE_FAILED` | MarkdownParser 抛错 | PublishService (wrap) |
| `UNKNOWN_PLATFORM` | `adapters.get(name)` 返回 undefined | PublishService |
| `NOT_IMPLEMENTED` | 平台 adapter 声明 `notImplemented = true` | Adapter |
| `HTTP_FAILED` | HttpClient.request 失败（未来真集成场景） | Adapter (wrap) |
| `INTERNAL` | 任何意外异常 | PublishService 或 Adapter (wrap) |

新增 code 必须**先**更新本契约，再加代码——traceability-review 节点会校验。

## Hyrum-safety notes

- `Post` 的字段集**只**保证以上 4 项；任何依赖未声明字段的 adapter 实现违反契约。
- `PublishResult` 是 discriminated union，禁止靠 `ok === undefined` 判断。
- adapter 不应在 `publish` 之外暴露任何额外公开方法（注册时只通过 `name + publish` 被使用）。
