# Contributing to HarnessFlow

HarnessFlow is a small, deliberately minimal skill suite: 6 core skills own the main chain (`specify → review → design → review → tdd → review → ship`), and everything domain-specific belongs in `ext-*` extensions.

## What lands easily

- Bug fixes: broken links, typos, factual errors in `SKILL.md` files.
- New `ext-*` extensions that follow [the authoring guide](skills/hf-workflow/references/extension-authoring.md): declare binding stages + trigger conditions in the description, only tighten (never relax) main-chain gates, keep the body ≤ 150 lines.
- Sharper checklist items in `skills/hf-review/references/` backed by a real failure they would have caught.

## What needs an issue first

- New core skills or changes to the main chain. The 6-skill shape is intentional — most "missing stage" proposals are better expressed as an extension or a checklist item.
- Anything that adds meta-machinery (routers, profiles, state schemas). HarnessFlow v2 removed these on purpose.

## Quality bar for skill edits

- Frontmatter: `name` matches the directory; `description` says what the skill does **and** when to use it.
- Keep `SKILL.md` bodies short (core ≤ 200 lines, extensions ≤ 150); move heavy reference material to `references/`.
- Rules must be decidable ("acceptance criteria in Given/When/Then") rather than aspirational ("write good requirements").
- Run `python3 scripts/validate_skills.py` before opening a PR; paste the output in the PR description.
- Test behavior, not prose: give an agent a realistic task with your changed skill and confirm it follows the rule; ideally also confirm it fails without the change.

## Process

1. Branch from `main`, make small logical commits (imperative mood, first line ≤ 72 chars).
2. Open a PR describing what changed, why, and the validation evidence.
3. For security issues see [SECURITY.md](SECURITY.md).
