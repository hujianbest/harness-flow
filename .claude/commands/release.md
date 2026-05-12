---
description: Cut a vX.Y.Z engineer-level release. Aggregates multiple workflow-closeout features into a release scope ADR, runs release-wide regression, syncs CHANGELOG / release notes / ADR statuses, and produces a tag-ready pack. Decoupled from the HF workflow router.
---

Direct invoke `skills/hf-release/SKILL.md`. **Do not** route through `using-hf-workflow` → `hf-workflow-router` first — `hf-release` is a standalone skill (ADR-004 D3) that reads disk artifacts directly to drive release-tier work.

Steps:

1. Load `skills/hf-release/SKILL.md`.
2. Treat the user request following this command as version hint and scope intent (e.g. `/release v1.2.0` → version hint `v1.2.0`; `/release` alone → infer from candidates + SemVer rules in §4).
3. Follow the SKILL.md `Workflow` §1 → §11 in order:
   - §1 Entry vs Recovery (read `features/release-vX.Y.Z/release-pack.md` to decide new vs continue).
   - §2 Candidate feature inventory (only `workflow-closeout` features qualify).
   - §3 Release Scope ADR draft (`docs/decisions/ADR-NNN-release-scope-vX.Y.Z.md`).
   - §4 SemVer + pre-release decision.
   - §5 Worktree / branch state.
   - §6 Release-wide regression (protocol inlined; do **not** call `hf-regression-gate` skill).
   - §7 Cross-feature traceability summary.
   - §8 Pre-Release Engineering Checklist (Code & Evidence / Documentation Sync / Versioning Hygiene / Worktree State; ops items explicitly out of scope).
   - §9 Evidence Matrix.
   - §10 Release pack written to `features/release-vX.Y.Z/release-pack.md`.
   - §11 Final Confirmation (interactive only).

Hard rules (do not bypass):

- **Standalone, no router coupling.** `hf-release` does not enter the `hf-workflow-router` transition map and does not hand work back to the router. Next Action is `null` / specific blocker / `hf-release §<step>` only.
- **Engineer-level release only.** No deployment, no staged rollout, no monitoring, no rollback procedures. Those are out of this skill's scope and must be handled by the project's own ops process.
- **No automatic git tag.** The skill produces a readiness pack; tag operations (`git tag`, `git push --tags`, GitHub Release) are project-maintainer actions.
- **Candidate features must be workflow-closeout.** `task-closeout` / `blocked` features are rejected at §2.
- **Release-wide regression must be fresh.** Stitching historical per-feature regression records does not count.
- **Author / reviewer separation (advisory).** The release scope ADR draft should be reviewed by an independent person / session before commit.

Out of scope (explicitly): feature flag lifecycle, staged rollout (0% → 5% → 100%), monitoring dashboards, error reporting, SLO config, health checks, CDN / DNS / SSL, rate limiting, post-launch observation windows.

The user request following this command is optional version hint + scope intent (e.g. `/release v1.2.0 minor with onboarding + rate-limit, defer billing-export`). The skill uses on-disk closeout records to validate the proposed scope.

See `docs/decisions/ADR-004-hf-release-skill.md` for the full v0.4.0 introduction decision and the rationale for the decoupling stance.
