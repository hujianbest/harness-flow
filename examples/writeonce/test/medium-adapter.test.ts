import { describe, it, expect } from 'vitest';
import { MediumAdapter } from '../src/platform/medium-adapter.js';
import { RecordingHttpClient } from '../src/platform/http-client.js';
import type { Post } from '../src/platform/platform-adapter.js';

const POST: Post = {
  title: 'Hello',
  body: 'body content here',
  codeBlocks: [{ lang: 'ts', code: 'const a = 1;' }],
  images: [],
};

describe('MediumAdapter', () => {
  it('has stable name "medium"', () => {
    expect(new MediumAdapter(new RecordingHttpClient()).name).toBe('medium');
  });

  it('makes one HTTP POST request when not dryRun', async () => {
    const http = new RecordingHttpClient();
    const adapter = new MediumAdapter(http);
    const result = await adapter.publish(POST, {});
    expect(result.ok).toBe(true);
    expect(http.requests).toHaveLength(1);
    expect(http.requests[0]!.method).toBe('POST');
    expect(http.requests[0]!.url).toContain('medium.com');
  });

  it('payload contains markdown contentFormat and the post body', async () => {
    const http = new RecordingHttpClient();
    const adapter = new MediumAdapter(http);
    await adapter.publish(POST, {});
    const body = http.requests[0]!.body;
    expect(body).toContain('"contentFormat":"markdown"');
    expect(body).toContain('Hello');
    expect(body).toContain('const a = 1;');
  });

  it('does not call HttpClient.request when dryRun is true', async () => {
    const http = new RecordingHttpClient();
    const adapter = new MediumAdapter(http);
    const result = await adapter.publish(POST, { dryRun: true });
    expect(result.ok).toBe(true);
    expect(http.requests).toHaveLength(0);
  });

  it('wraps unexpected throws into INTERNAL error code', async () => {
    const throwing = {
      async request(): Promise<never> {
        throw new Error('boom');
      },
    };
    const adapter = new MediumAdapter(throwing);
    const result = await adapter.publish(POST, {});
    expect(result.ok).toBe(false);
    if (!result.ok) {
      expect(result.code).toBe('HTTP_FAILED');
      expect(result.message).toContain('boom');
    }
  });
});
