import { describe, it, expect } from 'vitest';
import { WeChatMpAdapter } from '../src/platform/wechat-mp-adapter.js';
import type { Post } from '../src/platform/platform-adapter.js';

const POST: Post = {
  title: 'T',
  body: 'b',
  codeBlocks: [],
  images: [],
};

describe('WeChatMpAdapter', () => {
  it('has stable name "wechat-mp" and notImplemented = true', () => {
    const a = new WeChatMpAdapter();
    expect(a.name).toBe('wechat-mp');
    expect(a.notImplemented).toBe(true);
  });

  it('returns NOT_IMPLEMENTED on publish', async () => {
    const a = new WeChatMpAdapter();
    const r = await a.publish(POST, {});
    expect(r.ok).toBe(false);
    if (!r.ok) {
      expect(r.code).toBe('NOT_IMPLEMENTED');
      expect(r.message).toContain('wechat-mp');
    }
  });
});
