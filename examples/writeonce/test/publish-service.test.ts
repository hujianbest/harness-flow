import { describe, it, expect } from 'vitest';
import { PublishService } from '../src/publish/publish-service.js';
import { MarkdownParser } from '../src/parser/markdown-parser.js';
import { MediumAdapter } from '../src/platform/medium-adapter.js';
import { RecordingHttpClient } from '../src/platform/http-client.js';
import { writeFileSync, mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

function makeTempPostFile(contents: string): string {
  const dir = mkdtempSync(join(tmpdir(), 'writeonce-test-'));
  const file = join(dir, 'post.md');
  writeFileSync(file, contents, 'utf8');
  return file;
}

describe('PublishService', () => {
  it('returns FILE_NOT_FOUND structurally for missing files', async () => {
    const service = new PublishService({
      parser: new MarkdownParser(),
      adapters: [new MediumAdapter(new RecordingHttpClient())],
    });
    const result = await service.publish('/tmp/does-not-exist.md', { to: 'medium' });
    expect(result.ok).toBe(false);
    if (!result.ok) expect(result.code).toBe('FILE_NOT_FOUND');
  });

  it('returns PARSE_FAILED structurally when the file is not a valid Markdown post', async () => {
    const file = makeTempPostFile('no title here at all');
    const service = new PublishService({
      parser: new MarkdownParser(),
      adapters: [new MediumAdapter(new RecordingHttpClient())],
    });
    const result = await service.publish(file, { to: 'medium' });
    expect(result.ok).toBe(false);
    if (!result.ok) expect(result.code).toBe('PARSE_FAILED');
  });

  it('never throws — internal exceptions are wrapped to INTERNAL', async () => {
    const file = makeTempPostFile('# T\n\nbody\n');
    const throwingAdapter = {
      name: 'medium',
      async publish(): Promise<never> {
        throw new Error('boom');
      },
    };
    const service = new PublishService({
      parser: new MarkdownParser(),
      adapters: [throwingAdapter],
    });
    const result = await service.publish(file, { to: 'medium' });
    expect(result.ok).toBe(false);
    if (!result.ok) {
      expect(result.code).toBe('INTERNAL');
      expect(result.message).toContain('boom');
    }
  });

  it('NFR-Maintainability-1: adding a new adapter requires no edit to publish-service.ts', async () => {
    const file = makeTempPostFile('# T\n\nbody\n');
    const fakeAdapter = {
      name: 'fake',
      async publish() {
        return { ok: true, payload: { fake: true } } as const;
      },
    };
    const service = new PublishService({
      parser: new MarkdownParser(),
      adapters: [fakeAdapter],
    });
    const result = await service.publish(file, { to: 'fake' });
    expect(result.ok).toBe(true);
    if (result.ok) expect(result.payload).toEqual({ fake: true });
  });
});
