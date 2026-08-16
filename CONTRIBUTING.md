# Contributing to HarnessFlow

HarnessFlow is a Markdown-based skill suite: Matt-aligned main chain under `hf-*` names (`grill-with-docs` → `to-product-architecture` → `to-spec` → `to-architecture` → `to-tickets` → `implement` → `ship`, with cross-stage `hf-review`), plus progress recovery, auto mode, and demo acceptance.

## What lands easily

- Bug fixes: broken links, typos, factual errors in `SKILL.md` files.
- New domain skills that follow [the authoring guide](skills/hf-workflow/references/extension-authoring.md): declare binding stages + trigger conditions in the description, only tighten (never relax) review/TDD discipline, keep the body ≤ 150 lines if using the `ext-*` convention.
- Sharper checklist items in `skills/hf-review/references/` backed by a real failure they would have caught.

## What needs an issue first

- New core skills or changes to the main chain. Most "missing stage" proposals are better expressed as an extension or a checklist item.
- Anything that adds meta-machinery (routers, profiles, state schemas).

## Quality bar for edits

- Frontmatter: `name` matches the directory; `description` says what the skill does **and** when to use it.
- Keep `SKILL.md` bodies short (core ≤ 200 lines, extensions ≤ 150); move heavy reference material to `references/`.
- Rules must be decidable ("acceptance criteria in Given/When/Then") rather than aspirational ("write good requirements").
- Run `python3 scripts/validate_skills.py` and `python3 -m unittest discover -s tests -v` before opening a PR; paste the output in the PR description.
- Test behavior, not prose: give an agent a realistic task with your changed skill and confirm it follows the rule; ideally also confirm it fails without the change.

## Process

1. Branch from `main`, make small logical commits (imperative mood, first line ≤ 72 chars).
2. Open a PR describing what changed, why, and the validation evidence.
3. For security issues see [SECURITY.md](SECURITY.md).
