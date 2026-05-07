# HarnessFlow Agent Personas (v0.2.0)

3 user-facing **agent personas** introduced in v0.2.0 (ADR-002 D4 / D8). Each persona is an **orchestration shortcut** over one or more `hf-*-review` skills — never a replacement.

## What personas are NOT

Per ADR-002 D4 / D8 + soul.md hard rule:

- **Personas do not produce verdicts.** All "pass / fail" judgements come from the underlying `hf-*-review` skills.
- **Personas do not call implementation / authoring skills** (`hf-test-driven-dev` / `hf-specify` / `hf-design` / `hf-tasks` / `hf-ui-design`). They write findings; authors fix.
- **Personas do not edit the artifact under review.** Fagan author/reviewer separation is preserved.
- **Personas do not pull gates.** Gates are pulled by the canonical next action of upstream nodes, not by personas or the user.
- **Personas are NOT covered by `scripts/audit-skill-anatomy.py`.** They use the persona-anatomy template (`docs/principles/persona-anatomy.md`), not the SKILL.md anatomy.

## The 3 personas

| Persona | 角色定位 | 委派的 review skill |
|---|---|---|
| [`hf-staff-reviewer`](hf-staff-reviewer.md) | Senior Staff Engineer，整体代码 + 架构 review | `hf-design-review` + `hf-code-review` + `hf-traceability-review` |
| [`hf-qa-engineer`](hf-qa-engineer.md) | QA Specialist，关注测试设计与覆盖 | `hf-test-review`（read-only consume `hf-regression-gate` evidence + `hf-browser-testing` observations） |
| [`hf-security-auditor`](hf-security-auditor.md) | Security Engineer，STRIDE 风险 surface | `hf-design-review`（追加 risk finding；v0.2.0 缺 `hf-security-hardening`，不签独立安全 verdict） |

## How to invoke

Personas are markdown files. On Claude Code, invoke as a subagent (`Task` tool with the persona name). On other clients, point the agent at the persona file:

```text
请用 hf-staff-reviewer 看下 features/001-walking-skeleton 整个 feature 是否可以合并。
```

```text
Use the hf-qa-engineer persona at agents/hf-qa-engineer.md to review TASK-003's
test quality and regression evidence.
```

The persona file's frontmatter `description` is the trigger classifier; the body defines the orchestration recipe and the hard "do not" rules.

## When NOT to use a persona

- Single-artifact review (e.g. "review just this spec") → call the `hf-*-review` skill directly. Going through a persona is more overhead.
- Need an actual verdict on security / performance / shipping in v0.2.0 — those skills don't exist yet (deferred to v0.3+, ADR-002 D1). The persona will surface this gap rather than fabricate a verdict.
- Need someone to write code → personas do not write code; ask `hf-test-driven-dev` (with one Current Active Task locked) or use the regular `/build` slash command.

## Cross-references

- Persona anatomy: [`docs/principles/persona-anatomy.md`](../docs/principles/persona-anatomy.md)
- Personas release decision: [`docs/decisions/ADR-002-release-scope-v0.2.0.md`](../docs/decisions/ADR-002-release-scope-v0.2.0.md) D4 / D8
- Underlying review skills: [`skills/hf-design-review/`](../skills/hf-design-review/), [`skills/hf-code-review/`](../skills/hf-code-review/), [`skills/hf-traceability-review/`](../skills/hf-traceability-review/), [`skills/hf-test-review/`](../skills/hf-test-review/)
- Soul / hard rules: [`docs/principles/soul.md`](../docs/principles/soul.md)
