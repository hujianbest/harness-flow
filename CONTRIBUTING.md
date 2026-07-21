# Contributing to HarnessFlow

HarnessFlow is deliberately minimal: one binding constitution (`skills/harness/SKILL.md`, under 120 lines) defines seven invariants and three user checkpoints; one stdlib-only script (`skills/harness/scripts/harness.py`) owns the evidence protocol; four advisory playbooks live in `skills/harness/references/`. Everything else — stages, templates, tier tables, routers — was removed on purpose in v4.

## What lands easily

- Bug fixes: broken links, typos, factual errors in skill files, `harness.py` bugs (with a failing test first in `test_harness.py`).
- Sharper playbook advice in `skills/harness/references/` backed by a real failure it would have prevented. Playbooks are advisory, so they can grow more freely than the constitution.
- Better wording of an existing invariant or checkpoint that keeps its meaning but improves decidability.

## What needs an issue first

- Adding, removing, or materially changing an invariant or checkpoint. The seven-plus-three shape is the product; most proposals are better expressed as playbook advice.
- Anything that reintroduces step control: stage gates, mandatory templates, risk tier tables, per-step approvals. v4's core claim is that these are the wrong constraints.
- New subcommands or checks in `harness.py` that adjudicate process rather than record evidence. The script records; it does not judge.
- Non-stdlib dependencies anywhere. Scripts must travel with `skills/` dependency-free.

## Quality bar for edits

- Frontmatter: `name` matches the directory; `description` says what the skill does **and** when to load it.
- The constitution body stays ≤ 120 lines; heavy material moves to `references/`.
- Constraints must be decidable ("evidence log exists with exit code 0") rather than aspirational ("test thoroughly").
- Run `python3 scripts/validate_skills.py`, `python3 skills/harness/scripts/test_harness.py` and `python3 -m unittest discover tests` before opening a PR; paste the output in the PR description.
- Test behavior, not prose: give an agent a realistic task with your changed skill and confirm the constraint holds; ideally also confirm it fails without the change.

## Process

1. Branch from `main`, make small logical commits (imperative mood, first line ≤ 72 chars).
2. Open a PR describing what changed, why, and the validation evidence.
3. For security issues see [SECURITY.md](SECURITY.md).
