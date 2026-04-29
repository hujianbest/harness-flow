import type {
  PlatformAdapter,
  Post,
  PublishOptions,
  PublishResult,
} from './platform-adapter.js';

/**
 * v0 stub. Honest extension point per ADR-0002 + contract Invariant 2:
 * declared but not implemented. Future real integration should:
 *   - drop `notImplemented`
 *   - implement `publish` against whatever Zhihu integration path is chosen
 *   - re-run `hf-design-review` for the new boundary
 *   - update STRIDE per `design.md` section 15
 */
export class ZhihuAdapter implements PlatformAdapter {
  readonly name = 'zhihu';
  readonly notImplemented = true;

  async publish(_post: Post, _options: PublishOptions): Promise<PublishResult> {
    return {
      ok: false,
      code: 'NOT_IMPLEMENTED',
      message: 'platform "zhihu" is declared but not implemented in v0',
    };
  }
}
