---
name: Bug report
about: Report a bug in HarnessFlow itself (a skill, the plugin manifest, the demo, or the docs)
title: "BUG: <short description>"
labels: ["bug"]
assignees: []
---

## Before you file

- [ ] I have read the **Scope Note** at the top of `README.md` and `README.zh-CN.md` and confirmed this is **not** a known v0.1.0 scope choice (e.g. "no release/ops skills", "Claude Code + OpenCode only", "main chain ends at `hf-finalize`").
- [ ] I have checked `docs/decisions/ADR-001-release-scope-v0.1.0.md` and confirmed this is not an explicit decision (D1–D11) being filed as a bug.
- [ ] I have searched existing [open and closed issues](https://github.com/hujianbest/harness-flow/issues?q=is%3Aissue) for duplicates.
- [ ] If this is a **security** issue, I am using `SECURITY.md` instead of this template.

## What is broken

A clear, concise description of the actual behavior.

## Where it lives

- [ ] A `skills/<name>/SKILL.md` or its `references/`
- [ ] The Claude Code plugin manifest (`.claude-plugin/`)
- [ ] A slash command file (`.claude/commands/*.md`)
- [ ] A setup doc (`docs/claude-code-setup.md` / `docs/opencode-setup.md`)
- [ ] The WriteOnce demo (`examples/writeonce/`)
- [ ] Repository-root `README.md` / `README.zh-CN.md` / `CHANGELOG.md` / `LICENSE`
- [ ] Other (please specify)

Specific file path(s):

```
path/to/file
```

## Expected behavior

What you expected to happen instead, and why.

## Reproduction steps

1. ...
2. ...
3. ...

If the bug is in the WriteOnce demo, please include the output of:

```bash
cd examples/writeonce && npm test 2>&1 | tail -20
cd examples/writeonce && npx tsc --noEmit 2>&1 | tail -10
```

If the bug is about agent behavior loading a HarnessFlow skill, please include:

- Which agent / client (Claude Code, OpenCode, other)
- Which command or natural-language prompt triggered the issue
- The full agent response that demonstrated the bug (please redact secrets)

## Environment

- HarnessFlow version / commit: <e.g. `v0.1.0` or `main@<sha>`>
- Agent / client: <e.g. Claude Code 1.x, OpenCode 0.y, ...>
- OS: <e.g. macOS 14.5, Ubuntu 22.04, Windows 11>
- (For demo bugs) Node.js version: <output of `node --version`>

## Additional context

Anything else relevant — screenshots, logs, links to related issues / PRs / ADR sections.
