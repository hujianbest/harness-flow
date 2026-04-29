import { describe, it, expect } from 'vitest';
import { ZhihuAdapter } from '../src/platform/zhihu-adapter.js';
import type { Post } from '../src/platform/platform-adapter.js';

const POST: Post = {
  title: 'T',
  body: 'b',
  codeBlocks: [],
  images: [],
};

describe('ZhihuAdapter', () => {
  it('has stable name "zhihu" and notImplemented = true', () => {
    const a = new ZhihuAdapter();
    expect(a.name).toBe('zhihu');
    expect(a.notImplemented).toBe(true);
  });

  it('returns NOT_IMPLEMENTED on publish, regardless of options', async () => {
    const a = new ZhihuAdapter();
    const r1 = await a.publish(POST, {});
    const r2 = await a.publish(POST, { dryRun: true });
    expect(r1.ok).toBe(false);
    expect(r2.ok).toBe(false);
    if (!r1.ok && !r2.ok) {
      expect(r1.code).toBe('NOT_IMPLEMENTED');
      expect(r2.code).toBe('NOT_IMPLEMENTED');
      expect(r1.message).toContain('zhihu');
      expect(r1.message).toContain('not implemented');
    }
  });
});
