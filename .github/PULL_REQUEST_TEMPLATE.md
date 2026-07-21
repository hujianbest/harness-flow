# Pull Request

## Summary

<!-- What changed and why, in a few sentences. Link the issue if one exists. -->

## Change type

- [ ] Fix (typo, broken link, factual error, `harness.py` bug with failing test first)
- [ ] Playbook improvement (`skills/harness/references/`)
- [ ] Constitution change — invariant / checkpoint / truth layout (needs prior issue discussion)
- [ ] Docs / tooling

## Checklist

- [ ] `python3 scripts/validate_skills.py` passes (paste output below)
- [ ] `python3 skills/harness/scripts/test_harness.py` and `python3 -m unittest discover tests` pass
- [ ] The constitution body stays ≤ 120 lines; heavy material moved to `references/`
- [ ] The change constrains outcomes, not steps — it does not reintroduce stage gates, mandatory templates, or per-step approvals
- [ ] For skill-behavior changes: I tested with a realistic agent task and the constraint holds (describe the scenario below)

## Validation output

```text
$ python3 scripts/validate_skills.py
<paste>
```

## Behavior evidence (for skill changes)

<!-- Scenario given to the agent + how its behavior changed with this edit. -->
