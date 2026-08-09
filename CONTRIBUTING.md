# Contributing to HarnessFlow

HarnessFlow is a small, deliberately minimal skill suite: 7 core skills own the main chain (`frame → plan → build → verify → ship`, with `hf-review` at every gate), one stdlib-only gate script (`skills/hf-workflow/scripts/hf_gate.py`) owns mechanical enforcement, and everything domain-specific belongs in `ext-*` extensions.

## What lands easily

- Bug fixes: broken links, typos, factual errors in `SKILL.md` files, gate script bugs (with a failing test first).
- New `ext-*` extensions that follow [the authoring guide](skills/hf-workflow/references/extension-authoring.md): declare binding stages (frame/plan/build/verify/ship) + trigger conditions in the description, only tighten (never relax) main-chain gates, keep the body ≤ 150 lines.
- Sharper checklist items in `skills/hf-review/references/` backed by a real failure they would have caught.
- New optional diagnostics in `hf_gate.py` that help surface missing artifacts — must come with unit tests in `skills/hf-workflow/scripts/test_hf_gate.py`. Do **not** reintroduce mandatory “FAIL blocks stage entry” rules in skills or Cursor rules.

## What needs an issue first

- New core skills or changes to the main chain. The 7-skill shape is intentional — most "missing stage" proposals are better expressed as an extension, a checklist item, or a gate check.
- Anything that adds meta-machinery (routers, profiles, state schemas). HarnessFlow v2 removed these on purpose and v3 kept them out.
- Gate checks that require non-stdlib dependencies. The gate script must stay stdlib-only so it travels with `skills/`.

## Quality bar for edits

- Frontmatter: `name` matches the directory; `description` says what the skill does **and** when to use it.
- Keep `SKILL.md` bodies short (core ≤ 200 lines, extensions ≤ 150); move heavy reference material to `references/`.
- Rules must be decidable ("acceptance criteria in Given/When/Then") rather than aspirational ("write good requirements").
- Run `python3 scripts/validate_skills.py` and `python3 skills/hf-workflow/scripts/test_hf_gate.py` before opening a PR; paste the output in the PR description.
- Test behavior, not prose: give an agent a realistic task with your changed skill and confirm it follows the rule; ideally also confirm it fails without the change.

## Process

1. Branch from `main`, make small logical commits (imperative mood, first line ≤ 72 chars).
2. Open a PR describing what changed, why, and the validation evidence.
3. For security issues see [SECURITY.md](SECURITY.md).
