# HarnessFlow on OpenCode

HarnessFlow v0.5.0 supports OpenCode through an **agent-driven, evidence-based routing** integration. There is no plugin manifest and no `AGENTS.md` sidecar — instead, the agent uses natural language plus the on-disk artifacts under `skills/` to route every request through HarnessFlow's main chain.

> **Scope (v0.5.0 pre-release).** v0.5.0 officially supports 3 clients (unchanged from v0.3.0 / v0.4.0): **Claude Code**, **OpenCode**, and **Cursor**. The 4 remaining client expansions (Gemini CLI / Windsurf / GitHub Copilot / Kiro) stay deferred to v0.6+. v0.5.0 adds a **closeout HTML companion report** to `hf-finalize` — every closeout now also produces `features/<active>/closeout.html` rendered by the new stdlib-only `scripts/render-closeout-html.py` (workflow timeline rail + tests + coverage rings + searchable evidence matrix; WCAG 2.2 AA, dark/light, printable). v0.4.0's `hf-release` (release-tier **standalone** skill) is unchanged; on OpenCode it is invoked via natural language ("cut a release / tag a version") through the `using-hf-workflow` entry shell's bias row, which then **direct invokes** `hf-release` without going through `hf-workflow-router` (ADR-004 D3). The HarnessFlow main chain still ends at `hf-finalize` (single-feature engineering-level closeout, now with HTML companion). The remaining 5 ops/release skills (`hf-shipping-and-launch` / etc.) and personas all stay deferred to v0.6+ (ADR-005 D5 / D7). See `docs/decisions/ADR-005-release-scope-v0.5.0.md` for the full v0.5.0 scope decisions.

## How OpenCode discovers HF skills

OpenCode's [`skill` tool](https://opencode.ai/docs/skills/) only loads `SKILL.md` files from these well-known locations:

- `.opencode/skills/<name>/SKILL.md` (project-local)
- `.claude/skills/<name>/SKILL.md` (project-local, Claude-compatible)
- `.agents/skills/<name>/SKILL.md` (project-local, agent-compatible)
- `~/.config/opencode/skills/<name>/SKILL.md` (global)
- `~/.claude/skills/<name>/SKILL.md` (global, Claude-compatible)
- `~/.agents/skills/<name>/SKILL.md` (global, agent-compatible)

OpenCode walks up from the working directory to the git worktree root and loads any matching `*/SKILL.md` it finds along the way. **Putting a `skills/` folder at the repo root is not sufficient.**

HarnessFlow stores its 23 self-contained skills under the top-level `skills/` directory (so vendor-by-copy works for any client). To make those skills discoverable to OpenCode without duplicating files, the repository ships a symlink:

```text
.opencode/skills -> ../skills
```

Cloning the repo and opening it in OpenCode is therefore enough to expose every `hf-*` skill plus `using-hf-workflow` to OpenCode's `skill` tool. No `AGENTS.md` sidecar, no slash commands, no manual install step.

> **Why no `AGENTS.md` sidecar?** PR #21 made every `hf-*` skill self-contained (the `SKILL.md`, `references/`, `evals/` all ship inside the skill folder; no cross-skill `skills/docs/`, `skills/templates/`, or root-level `AGENTS.md.example`). ADR-001 D3 then re-evaluated OpenCode's setup path and confirmed: HarnessFlow on OpenCode does not need an `AGENTS.md` sidecar to function. If your project already uses an `AGENTS.md` for unrelated reasons, HarnessFlow does not require any changes to it.

## 1. Install

You have three install topologies. Pick whichever matches how you already use OpenCode.

### A. Use the HarnessFlow repository directly (recommended for trying it out)

```bash
git clone https://github.com/hujianbest/harness-flow.git
cd harness-flow
opencode .
```

The shipped `.opencode/skills` symlink makes all 23 `hf-*` skills + `using-hf-workflow` immediately discoverable (v0.2.0 added `hf-browser-testing` as the 23rd `hf-*` skill). No further setup.

### B. Vendor HarnessFlow skills into your own project

If you want HarnessFlow to be available inside another repository you are working on, copy (or symlink) the `skills/` directory into that project's `.opencode/skills/`:

```bash
# From inside your project root, with harness-flow cloned alongside:
mkdir -p .opencode
cp -R ../harness-flow/skills .opencode/skills

# Or, if you want updates to track upstream automatically:
ln -s ../../harness-flow/skills .opencode/skills
```

Each `hf-*` skill is self-contained (its `SKILL.md`, `references/`, and `evals/` ship together in the skill folder), so a plain `cp -R` is enough — there is nothing else to vendor.

### C. Install HarnessFlow globally for every OpenCode session

If you want HarnessFlow available across all of your projects:

```bash
# Linux / macOS
mkdir -p ~/.config/opencode/skills
cp -R /path/to/harness-flow/skills/* ~/.config/opencode/skills/
```

Global skills live alongside any project-local skills you may have; project-local copies win on name collision.

## 2. Verify the install

After opening OpenCode in any of the three topologies above, run:

```text
/skills
```

You should see at least the following skills listed (23 `hf-*` skills + `using-hf-workflow`; v0.2.0 added `hf-browser-testing` as the 23rd):

- `using-hf-workflow`
- `hf-workflow-router`
- `hf-product-discovery`, `hf-discovery-review`
- `hf-specify`, `hf-spec-review`
- `hf-design`, `hf-ui-design`, `hf-design-review`, `hf-ui-review`
- `hf-tasks`, `hf-tasks-review`
- `hf-test-driven-dev`, `hf-test-review`
- `hf-code-review`, `hf-traceability-review`
- `hf-regression-gate`, `hf-doc-freshness-gate`, `hf-completion-gate`
- `hf-finalize`
- `hf-hotfix`, `hf-increment`, `hf-experiment`
- `hf-browser-testing` (new in v0.2.0)
- `hf-release` (new in v0.4.0; release-tier standalone skill, not in router transition map)

If the list is empty, see [§5 Troubleshooting](#5-troubleshooting).

## 3. How agent-driven routing works

OpenCode supports custom slash commands, but HarnessFlow on OpenCode intentionally does **not** ship them — that matches HarnessFlow's own design rule that "commands are bias, on-disk artifacts decide the next node" (ADR-001 D4 rationale). Instead, the agent reads intent from natural language and lets the router pick the leaf skill.

Mapping from natural-language intent to HarnessFlow nodes (the same set that Claude Code's 7 slash commands bias toward):

| Natural-language intent | Selected node |
|---|---|
| "I'm not sure where we are, route me." | `using-hf-workflow` -> `hf-workflow-router` (default entry) |
| "Write / revise the spec for X." | `hf-specify` (after upstream discovery preconditions) |
| "Plan this — design and tasks." | `hf-design` (and `hf-ui-design` when the spec declares a UI surface) -> `hf-tasks` |
| "Implement the current active task with TDD." | `hf-test-driven-dev` (only when one `Current Active Task` is locked) |
| "Review the [spec / design / UI / tasks / tests / code / traceability]." | router dispatches to the matching `hf-*-review` per `skills/hf-workflow-router/references/review-dispatch-protocol.md` |
| "Close out this task / workflow." | `hf-completion-gate` -> `hf-finalize` (gate decides if finalize can run) |
| "Cut a release / tag vX.Y.Z / write release notes." | **direct invoke** `hf-release` (does **not** go through `hf-workflow-router`; ADR-004 D3). Engineer-level release only — does **not** deploy or staged-rollout. |

Hard rule: the first 6 intents are **bias**, not bypass — the router still inspects on-disk artifacts under the active feature directory and routes to the correct upstream node if preconditions are not met. The "cut a release" intent is the exception: the entry shell direct-invokes `hf-release`, which has its own internal Hard Gates (candidate features must be `workflow-closeout`, release-wide regression must be fresh, no auto `git tag`).

## 4. Recommended first prompt

Paste this into OpenCode after opening the repository (or any project that has HF skills installed):

```text
Use HarnessFlow from this repo. Load `using-hf-workflow` via the skill tool and
route me through the correct HF workflow. I want to add rate limiting to our
notifications API. Do not jump straight to code.
```

Expected behavior:

1. The agent calls `skill({ name: "using-hf-workflow" })` to load the entry shell.
2. It hands off to `hf-workflow-router` (also via the `skill` tool).
3. For a brand-new feature with no prior artifacts, the router routes into `hf-product-discovery` or `hf-specify` (depending on what evidence already exists).

If the agent skips straight into implementation (`hf-test-driven-dev`) without an approved spec / design / tasks chain, that is a **bug** — please open an issue.

## 5. Troubleshooting

| Symptom | Look at |
|---|---|
| `/skills` shows no `hf-*` entries | The current project has no `.opencode/skills/`, `.claude/skills/`, or `.agents/skills/`, **and** there are no skills under `~/.config/opencode/skills/`. Re-do step 1 (one of A / B / C). |
| Some skills missing, others present | Skill name collision across discovery locations — OpenCode requires unique names. Remove duplicates from one of the locations. |
| Symlink `.opencode/skills -> ../skills` broken | Restore with `ln -snf ../skills .opencode/skills` from the harness-flow repo root. |
| Agent ignores HarnessFlow and writes code directly | Re-prompt explicitly: "Use HarnessFlow. Load `using-hf-workflow` via the skill tool first." |
| Router routes to the wrong node | `skills/hf-workflow-router/SKILL.md` + `skills/hf-workflow-router/references/profile-node-and-transition-map.md` |
| Reviewer wants to edit the artifact under review | That violates author/reviewer separation — file an issue |
| `hf-test-driven-dev` keeps refusing to start | No `Current Active Task` is locked; ask the router to plan first |
| `hf-finalize` keeps bouncing back | A gate (regression / doc-freshness / completion) failed; follow the canonical next action it returned |

### Permissions (optional)

If your team wants to gate which skills OpenCode can auto-load, configure pattern-based permissions in `opencode.json`:

```json
{
  "permission": {
    "skill": {
      "*": "allow",
      "hf-*": "allow"
    }
  }
}
```

## 6. Side branches and gates

Natural-language intents also cover side branches and gates:

| Intent | Router behavior |
|---|---|
| "Production defect, hotfix needed." | branches into `hf-hotfix` (RCA / minimal safe fix boundary) |
| "Scope change, re-enter the workflow." | branches into `hf-increment` (impact analysis + re-entry) |
| "Run the regression evidence check before completion." | router pulls `hf-regression-gate` from the canonical next action — do not push it manually |

The `hf-regression-gate`, `hf-doc-freshness-gate`, and `hf-completion-gate` skills are intentionally **pulled** by upstream nodes, not pushed by the user. Asking for "/gate" directly would encourage skipping implementation or review — that is why HarnessFlow ships no `/gate` command, on Claude Code or on OpenCode (ADR-001 D4).

## 7. What is NOT included in v0.5.0

Per ADR-001 D1 + ADR-002 D1 / D11 + ADR-003 D2 / D3 / D6 + ADR-004 D2 / D3 (P-Honest, "narrow but hard"):

- All 6 originally-deferred ops/release skills (`hf-shipping-and-launch`, `hf-ci-cd-and-automation`, `hf-security-hardening`, `hf-performance-gate`, `hf-deprecation-and-migration`, `hf-debugging-and-error-recovery`) remain out of scope. v0.4.0 added a **new** skill `hf-release` (release-tier engineer-level version cut), and v0.5.0 added a **closeout HTML companion report** to `hf-finalize` — neither is one of the 6 original deferred ops/release skills, and neither replaces `hf-shipping-and-launch`; all three slices are orthogonal (closeout reviewer experience vs. version cut vs. ship to production).
- `hf-release` does **not** enter the router transition map — it is a release-tier standalone skill, decoupled from the main chain (ADR-004 D3). Asking "where in the workflow is `hf-release`?" — it isn't; it sits beside the workflow.
- `hf-release` does **not** auto-execute `git tag` or `git push --tags`. The skill produces a readiness pack only; tag operations are project-maintainer actions.
- The SKILL.md anatomy audit script `scripts/audit-skill-anatomy.py` is **advisory** and does not block PR merge in maintainer workflows (ADR-002 D5 sub-decision; ADR-003 D8 / ADR-004 keep this stance).
- No 4-client expansion (Gemini CLI / Windsurf / GitHub Copilot / Kiro) — Cursor was added in v0.3.0; the other 4 stay deferred to v0.6+.
- No 3 user-facing personas (`hf-staff-reviewer` / `hf-qa-engineer` / `hf-security-auditor`) — ADR-002 D11 revoked; ADR-003 D3 / ADR-004 / ADR-005 D5 keep deferred to v0.6+.
- ADR-001 D11's stance on `Object Contract` (neither mandatory nor recommended in v0.1.0) is preserved — only `Common Rationalizations` (required) and `和其他 Skill 的区别` (forbidden) are hard rules in `skill-anatomy.md` (ADR-002 D9 / D10; ADR-003 D9 / ADR-004 keep the rest as design reference).

These constraints are intentional. They keep the surface area small enough for the v0.5.0 pre-release to be honest about what it does and does not cover.

## 8. Cross-references

- ADR-004 (v0.4.0 release scope: hf-release standalone skill + /release command): `docs/decisions/ADR-004-hf-release-skill.md`
- ADR-005 (v0.5.0 release scope: hf-finalize closeout HTML companion + scripts/render-closeout-html.py): `docs/decisions/ADR-005-release-scope-v0.5.0.md`
- ADR-003 (v0.3.0 release scope: Cursor-only client expansion): `docs/decisions/ADR-003-release-scope-v0.3.0.md`
- ADR-002 (v0.2.0 release scope, with D11 narrowing): `docs/decisions/ADR-002-release-scope-v0.2.0.md`
- ADR-001 (v0.1.0 release scope): `docs/decisions/ADR-001-release-scope-v0.1.0.md`
- `hf-release` skill: `skills/hf-release/SKILL.md`
- Repository overview: `README.md` (English) / `README.zh-CN.md` (Chinese)
- Other supported client setups: `docs/claude-code-setup.md` / `docs/cursor-setup.md`
- OpenCode official skills docs: <https://opencode.ai/docs/skills/>
