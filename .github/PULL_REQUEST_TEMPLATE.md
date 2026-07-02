# Pull Request

## Summary

<!-- What changed and why, in a few sentences. Link the issue if one exists. -->

## Change type

- [ ] Fix (typo, broken link, factual error)
- [ ] New / updated `ext-*` extension
- [ ] Review checklist improvement
- [ ] Core skill / main chain change (needs prior issue discussion)
- [ ] Docs / tooling

## Checklist

- [ ] `python3 scripts/validate_skills.py` passes (paste output below)
- [ ] Skill bodies stay within limits (core ≤ 200 lines, ext ≤ 150 lines); heavy material moved to `references/`
- [ ] For skill-behavior changes: I tested with a realistic agent task and the agent follows the new rule (describe the scenario below)
- [ ] For new extensions: frontmatter description declares 绑定阶段 and 触发条件; the extension only tightens, never relaxes, main-chain gates

## Validation output

```text
$ python3 scripts/validate_skills.py
<paste>
```

## Behavior evidence (for skill changes)

<!-- Scenario given to the agent + how its behavior changed with this edit. -->
