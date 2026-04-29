import type {
  PlatformAdapter,
  Post,
  PublishOptions,
  PublishResult,
} from './platform-adapter.js';

/**
 * v0 stub. Honest extension point per ADR-0002 + contract Invariant 2:
 * declared but not implemented. See `zhihu-adapter.ts` for the same pattern.
 */
export class WeChatMpAdapter implements PlatformAdapter {
  readonly name = 'wechat-mp';
  readonly notImplemented = true;

  async publish(_post: Post, _options: PublishOptions): Promise<PublishResult> {
    return {
      ok: false,
      code: 'NOT_IMPLEMENTED',
      message: 'platform "wechat-mp" is declared but not implemented in v0',
    };
  }
}
