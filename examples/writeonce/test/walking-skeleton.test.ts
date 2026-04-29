import { describe, it, expect } from 'vitest';
import { resolve } from 'node:path';
import { PublishService } from '../src/publish/publish-service.js';
import { MarkdownParser } from '../src/parser/markdown-parser.js';
import { MediumAdapter } from '../src/platform/medium-adapter.js';
import { ZhihuAdapter } from '../src/platform/zhihu-adapter.js';
import { WeChatMpAdapter } from '../src/platform/wechat-mp-adapter.js';
import { RecordingHttpClient } from '../src/platform/http-client.js';

const FIXTURE = resolve(__dirname, 'fixtures/post.md');

describe('walking-skeleton e2e', () => {
  it('publishes a Markdown file to Medium via PublishService and records exactly one HTTP request', async () => {
    const http = new RecordingHttpClient();
    const service = new PublishService({
      parser: new MarkdownParser(),
      adapters: [
        new MediumAdapter(http),
        new ZhihuAdapter(),
        new WeChatMpAdapter(),
      ],
    });

    const result = await service.publish(FIXTURE, { to: 'medium' });

    expect(result.ok).toBe(true);
    expect(http.requests).toHaveLength(1);
    const req = http.requests[0]!;
    expect(req.url).toContain('medium.com');
    expect(req.body).toContain('Hello');
    expect(req.body).toContain('export function add');
  });

  it('returns UNKNOWN_PLATFORM when --to references an unregistered name', async () => {
    const http = new RecordingHttpClient();
    const service = new PublishService({
      parser: new MarkdownParser(),
      adapters: [new MediumAdapter(http)],
    });

    const result = await service.publish(FIXTURE, { to: 'mastodon' });

    expect(result.ok).toBe(false);
    if (!result.ok) {
      expect(result.code).toBe('UNKNOWN_PLATFORM');
      expect(result.message).toContain('mastodon');
    }
    expect(http.requests).toHaveLength(0);
  });

  it('returns NOT_IMPLEMENTED when --to references a stubbed platform (zhihu)', async () => {
    const http = new RecordingHttpClient();
    const service = new PublishService({
      parser: new MarkdownParser(),
      adapters: [
        new MediumAdapter(http),
        new ZhihuAdapter(),
        new WeChatMpAdapter(),
      ],
    });

    const result = await service.publish(FIXTURE, { to: 'zhihu' });

    expect(result.ok).toBe(false);
    if (!result.ok) {
      expect(result.code).toBe('NOT_IMPLEMENTED');
      expect(result.message).toContain('zhihu');
      expect(result.message).toContain('not implemented');
    }
    expect(http.requests).toHaveLength(0);
  });

  it('returns FILE_NOT_FOUND when the input markdown file does not exist', async () => {
    const http = new RecordingHttpClient();
    const service = new PublishService({
      parser: new MarkdownParser(),
      adapters: [new MediumAdapter(http)],
    });

    const result = await service.publish('/tmp/definitely-not-here.md', {
      to: 'medium',
    });

    expect(result.ok).toBe(false);
    if (!result.ok) {
      expect(result.code).toBe('FILE_NOT_FOUND');
    }
    expect(http.requests).toHaveLength(0);
  });

  it('does not call HttpClient.request when dryRun is true', async () => {
    const http = new RecordingHttpClient();
    const service = new PublishService({
      parser: new MarkdownParser(),
      adapters: [new MediumAdapter(http)],
    });

    const result = await service.publish(FIXTURE, {
      to: 'medium',
      dryRun: true,
    });

    expect(result.ok).toBe(true);
    expect(http.requests).toHaveLength(0);
  });
});
