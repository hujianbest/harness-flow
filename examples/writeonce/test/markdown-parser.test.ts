import { describe, it, expect } from 'vitest';
import { MarkdownParser } from '../src/parser/markdown-parser.js';

describe('MarkdownParser', () => {
  it('extracts the first H1 as the post title', () => {
    const parser = new MarkdownParser();
    const post = parser.parse('# Hello\n\nbody text');
    expect(post.title).toBe('Hello');
  });

  it('strips the title line out of the body', () => {
    const parser = new MarkdownParser();
    const post = parser.parse('# Hello\n\nbody text');
    expect(post.body.startsWith('# Hello')).toBe(false);
    expect(post.body).toContain('body text');
  });

  it('captures fenced code blocks with language identifier', () => {
    const md = '# T\n\n```ts\nconst a = 1;\n```\n';
    const post = new MarkdownParser().parse(md);
    expect(post.codeBlocks).toHaveLength(1);
    expect(post.codeBlocks[0]).toEqual({ lang: 'ts', code: 'const a = 1;' });
  });

  it('captures images with alt text and src', () => {
    const md = '# T\n\n![alt](https://e.com/x.png)\n';
    const post = new MarkdownParser().parse(md);
    expect(post.images).toEqual([
      { alt: 'alt', src: 'https://e.com/x.png' },
    ]);
  });

  it('throws a recognizable error when no H1 title is present', () => {
    const parser = new MarkdownParser();
    expect(() => parser.parse('no title here')).toThrowError(/title/);
  });
});
