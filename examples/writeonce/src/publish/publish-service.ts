import { readFile } from 'node:fs/promises';
import type { MarkdownParser } from '../parser/markdown-parser.js';
import type {
  PlatformAdapter,
  PublishOptions,
  PublishResult,
} from '../platform/platform-adapter.js';

export interface PublishServiceDeps {
  parser: MarkdownParser;
  adapters: readonly PlatformAdapter[];
}

export interface PublishCallOptions extends PublishOptions {
  to: string;
}

export class PublishService {
  private readonly adapters: Map<string, PlatformAdapter>;
  private readonly parser: MarkdownParser;

  constructor(deps: PublishServiceDeps) {
    this.parser = deps.parser;
    this.adapters = new Map(deps.adapters.map((a) => [a.name, a]));
  }

  async publish(
    file: string,
    options: PublishCallOptions,
  ): Promise<PublishResult> {
    const adapter = this.adapters.get(options.to);
    if (!adapter) {
      return {
        ok: false,
        code: 'UNKNOWN_PLATFORM',
        message: `unknown platform "${options.to}"; registered adapters: ${[...this.adapters.keys()].join(', ') || '(none)'}`,
      };
    }

    let raw: string;
    try {
      raw = await readFile(file, 'utf8');
    } catch (err) {
      return {
        ok: false,
        code: 'FILE_NOT_FOUND',
        message: err instanceof Error ? err.message : String(err),
      };
    }

    let post;
    try {
      post = this.parser.parse(raw);
    } catch (err) {
      return {
        ok: false,
        code: 'PARSE_FAILED',
        message: err instanceof Error ? err.message : String(err),
      };
    }

    try {
      return await adapter.publish(post, { dryRun: options.dryRun });
    } catch (err) {
      return {
        ok: false,
        code: 'INTERNAL',
        message: err instanceof Error ? err.message : String(err),
      };
    }
  }
}
