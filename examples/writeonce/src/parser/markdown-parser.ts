import type { Post } from '../platform/platform-adapter.js';

/**
 * Minimal hand-written CommonMark subset parser.
 *
 * Scope (per spec section 6 + section 10):
 *   - first H1 line is the post title (required)
 *   - everything after the title line is the body (raw markdown)
 *   - fenced code blocks (```lang ... ```) are also captured separately
 *   - images (![alt](src)) are also captured separately
 *
 * Out of scope: tables, footnotes, blockquotes, HTML passthrough, link
 * reference definitions, autolinks. These are deliberately omitted to keep
 * the walking skeleton small (spec.md section 10: "no large markdown lib").
 */
export class MarkdownParser {
  parse(source: string): Post {
    const titleMatch = source.match(/^#\s+(.+?)\s*$/m);
    if (!titleMatch || titleMatch.index === undefined) {
      throw new Error('markdown post is missing a top-level "# title" line');
    }
    const title = titleMatch[1]!.trim();
    const body = (source.slice(0, titleMatch.index) +
      source.slice(titleMatch.index + titleMatch[0].length))
      .replace(/^\n+/, '')
      .trimEnd();

    const codeBlocks: Post['codeBlocks'] = [];
    const fenceRe = /```([\w+-]*)\n([\s\S]*?)```/g;
    let m: RegExpExecArray | null;
    while ((m = fenceRe.exec(source)) !== null) {
      const lang = m[1]!.trim();
      const code = m[2]!.replace(/\n$/, '');
      codeBlocks.push(lang ? { lang, code } : { code });
    }

    const images: Post['images'] = [];
    const imgRe = /!\[([^\]]*)\]\(([^)]+)\)/g;
    let im: RegExpExecArray | null;
    while ((im = imgRe.exec(source)) !== null) {
      images.push({ alt: im[1]!, src: im[2]! });
    }

    return { title, body, codeBlocks, images };
  }
}
