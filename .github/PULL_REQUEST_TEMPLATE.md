<!--
Thanks for opening a PR against HarnessFlow.

Please fill in the sections below. Sections marked OPTIONAL can be removed if not applicable.

If you are running this repository's own cloud-agent flow, the agent system will automatically wrap and append metadata to this body — leave that to the system, do not add cloud-agent comments here yourself.
-->

## Summary

A one-paragraph description of what this PR changes and why.

## Linked issue / ADR

- Closes #
- Related to #
- ADR section (`docs/decisions/ADR-001-release-scope-v0.1.0.md` D…) impact: <none / quoted decision IDs>

## Type of change

- [ ] Bug fix (non-breaking)
- [ ] Documentation update
- [ ] WriteOnce demo improvement (`examples/writeonce/`)
- [ ] Setup / plugin manifest fix
- [ ] New feature (non-breaking) — please confirm scope below
- [ ] Breaking change — please confirm ADR amendment below

## Scope check

- [ ] I have read the **Scope Note** at the top of `README.md` and confirmed this PR does not introduce out-of-scope changes for v0.1.x (no release / ops / monitoring skill, no client other than Claude Code + OpenCode unless explicitly marked as additive for v0.2+, no `docs/principles/` edit unless re-opening D11).
- [ ] I have read `docs/decisions/ADR-001-release-scope-v0.1.0.md` and confirmed this PR does not silently contradict an accepted decision. If it does, the change is captured in an ADR amendment commit in this PR.

## Files changed

Brief enumeration. For larger PRs, group by area:

- `skills/<name>/`: <what changed>
- `examples/writeonce/`: <what changed>
- `docs/`: <what changed>
- `.claude-plugin/` / `.claude/commands/`: <what changed>
- `README.md` / `README.zh-CN.md` / `CHANGELOG.md`: <what changed>

## Testing / verification

Paste evidence that your change works. v0.1.0 has no CI; PR authors are expected to run local checks.

For demo (`examples/writeonce/`) changes:

```text
$ cd examples/writeonce && npm test
<paste tail>

$ cd examples/writeonce && npx tsc --noEmit
<paste output>
```

For documentation / SKILL.md changes:

- [ ] Internal links (`[…](…)`) point to existing files
- [ ] Affected feature `README.md` Status Snapshot updated (if any)
- [ ] `CHANGELOG.md`'s `[Unreleased]` section updated

For plugin manifest / setup doc changes:

- [ ] JSON validates with `python3 -m json.tool`
- [ ] (If you have access to a real Claude Code or OpenCode environment) installed locally and confirmed the change works

## Out of scope

What you deliberately **did not** change in this PR (to keep the diff small / reviewable). Helps reviewers know what to expect in a follow-up.

## Walkthrough artifacts (OPTIONAL)

If your change is GUI-visible (e.g. an updated marketplace install flow demo, a screenshot of a slash command in action), attach them here. Plain-text changes do not need walkthroughs.

## Final checks

- [ ] One commit per logical change (no batched commits unless clearly justified).
- [ ] Branch is up to date with `main`.
- [ ] No force-push, no amended commits on shared branches.
- [ ] No secrets / tokens / private URLs included.
