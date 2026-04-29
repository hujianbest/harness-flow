/**
 * PlatformAdapter contract — see
 * `examples/writeonce/features/001-walking-skeleton/contracts/platform-adapter.contract.md`.
 *
 * Invariants:
 *   1. `publish` MUST resolve, never reject. Internal throws are wrapped.
 *   2. When `notImplemented === true`, `publish` MUST return
 *      { ok: false, code: 'NOT_IMPLEMENTED' } regardless of options.
 *   3. `name` is a stable, lowercase, kebab-case identifier.
 */

export interface Post {
  title: string;
  body: string;
  codeBlocks: Array<{ lang?: string; code: string }>;
  images: Array<{ alt: string; src: string }>;
}

export interface PublishOptions {
  dryRun?: boolean;
}

export type PublishOk = { ok: true; payload: unknown };
export type PublishErr = {
  ok: false;
  code: PublishErrorCode;
  message: string;
};
export type PublishResult = PublishOk | PublishErr;

export type PublishErrorCode =
  | 'FILE_NOT_FOUND'
  | 'PARSE_FAILED'
  | 'UNKNOWN_PLATFORM'
  | 'NOT_IMPLEMENTED'
  | 'HTTP_FAILED'
  | 'INTERNAL';

export interface PlatformAdapter {
  readonly name: string;
  readonly notImplemented?: boolean;
  publish(post: Post, options: PublishOptions): Promise<PublishResult>;
}
