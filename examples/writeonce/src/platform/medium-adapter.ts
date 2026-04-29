import type {
  PlatformAdapter,
  Post,
  PublishOptions,
  PublishResult,
} from './platform-adapter.js';
import type { HttpClient } from './http-client.js';

const MEDIUM_CREATE_POST_URL = 'https://api.medium.com/v1/users/me/posts';

export class MediumAdapter implements PlatformAdapter {
  readonly name = 'medium';

  constructor(private readonly http: HttpClient) {}

  async publish(post: Post, options: PublishOptions): Promise<PublishResult> {
    const payload = {
      title: post.title,
      contentFormat: 'markdown',
      content: this.composeMarkdown(post),
      tags: [],
    };

    if (options.dryRun) {
      return { ok: true, payload };
    }

    try {
      const response = await this.http.request(MEDIUM_CREATE_POST_URL, {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (response.status >= 200 && response.status < 300) {
        return { ok: true, payload: { request: payload, response } };
      }
      return {
        ok: false,
        code: 'HTTP_FAILED',
        message: `medium responded with status ${response.status}`,
      };
    } catch (err) {
      return {
        ok: false,
        code: 'HTTP_FAILED',
        message: err instanceof Error ? err.message : String(err),
      };
    }
  }

  private composeMarkdown(post: Post): string {
    const fences = post.codeBlocks
      .filter((b) => !post.body.includes(b.code))
      .map((b) => '```' + (b.lang ?? '') + '\n' + b.code + '\n```')
      .join('\n\n');
    const tail = fences ? `\n\n${fences}\n` : '\n';
    return `# ${post.title}\n\n${post.body}${tail}`;
  }
}
