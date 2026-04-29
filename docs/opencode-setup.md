# HarnessFlow on OpenCode

HarnessFlow v0.1.0 supports OpenCode through an **agent-driven, evidence-based routing** integration. There is no plugin manifest and no `AGENTS.md` sidecar — instead, the agent uses natural language and the on-disk artifacts under `skills/` to route every request through HarnessFlow's main chain.

> **Scope (v0.1.0 pre-release).** v0.1.0 only officially supports **Claude Code** and **OpenCode**. Other clients (Cursor / Gemini CLI / Windsurf / GitHub Copilot / Kiro) are deferred to v0.2+. The HarnessFlow main chain ends at `hf-finalize` (engineering-level closeout); release / ops / monitoring / metrics-feedback are intentionally out of scope for this version. See ADR-001 D1 / D3.

## Why no AGENTS.md sidecar?

PR #21 made every `hf-*` skill **self-contained** (the SKILL.md, `references/`, `evals/` all ship inside the skill folder; no cross-skill `skills/docs/`, `skills/templates/`, or root-level `AGENTS.md.example`). ADR-001 D3 then re-evaluated OpenCode's setup path and confirmed: HarnessFlow on OpenCode does not need an `AGENTS.md` sidecar to function. The agent only needs:

1. The `skills/` directory in the workspace.
2. A short instruction to enter via `using-hf-workflow` and let `hf-workflow-router` decide the next node.

If your project already uses an `AGENTS.md` for unrelated reasons, HarnessFlow does not require any changes to it.

## 1. Install

```bash
git clone https://github.com/hujianbest/harness-flow.git
cd harness-flow
```

Open the repository in OpenCode. The only files OpenCode needs to see are:

- `skills/using-hf-workflow/SKILL.md` — entry shell (Front Controller).
- `skills/hf-workflow-router/SKILL.md` — runtime router (FSM).
- `skills/hf-*/SKILL.md` — 23 leaf skills.

That is it. No additional config, no installation step, no command registration.

## 2. How agent-driven routing works

OpenCode supports custom slash commands, but HarnessFlow on OpenCode intentionally does **not** ship them — that matches HarnessFlow's own design rule that "commands are bias, on-disk artifacts decide the next node" (ADR-001 D4 rationale). Instead, agents read intent from natural language and let the router pick the leaf skill.

Mapping from natural-language intent to HarnessFlow nodes (the same set that Claude Code's 6 slash commands bias toward):

| Natural-language intent | Router selects |
|---|---|
| "I'm not sure where we are, route me." | `using-hf-workflow` -> `hf-workflow-router` (default entry) |
| "Write / revise the spec for X." | `hf-specify` (after upstream discovery preconditions) |
| "Plan this — design and tasks." | `hf-design` (and `hf-ui-design` when the spec declares a UI surface) -> `hf-tasks` |
| "Implement the current active task with TDD." | `hf-test-driven-dev` (only when one `Current Active Task` is locked) |
| "Review the [spec / design / UI / tasks / tests / code / traceability]." | router dispatches to the matching `hf-*-review` per `skills/hf-workflow-router/references/review-dispatch-protocol.md` |
| "Close out this task / workflow." | `hf-completion-gate` -> `hf-finalize` (gate decides if finalize can run) |

Hard rule: every intent above is a **bias**, not a bypass. The router still inspects on-disk artifacts under the active feature directory and routes to the correct upstream node if preconditions are not met.

## 3. Recommended first prompt

Paste this into OpenCode after opening the repository:

```text
Use HarnessFlow from this repo. Start with `using-hf-workflow` and route me
through the correct HF workflow. I want to add rate limiting to our
notifications API. Do not jump straight to code.
```

Expected behavior:

1. The agent loads `skills/using-hf-workflow/SKILL.md` as the entry shell.
2. It hands off to `skills/hf-workflow-router/SKILL.md`.
3. For a brand-new feature with no prior artifacts, the router routes into `hf-product-discovery` or `hf-specify` (depending on what evidence already exists).

If the agent skips straight into implementation (`hf-test-driven-dev`) without an approved spec / design / tasks chain, that is a **bug** — please open an issue.

## 4. Side branches and gates

Natural-language intents also cover side branches and gates:

| Intent | Router behavior |
|---|---|
| "Production defect, hotfix needed." | branches into `hf-hotfix` (RCA / minimal safe fix boundary) |
| "Scope change, re-enter the workflow." | branches into `hf-increment` (impact analysis + re-entry) |
| "Capture the bug pattern we just hit." | activates `hf-bug-patterns` (optional learning loop) |
| "Run the regression evidence check before completion." | router pulls `hf-regression-gate` from the canonical next action — do not push it manually |

The `hf-regression-gate`, `hf-doc-freshness-gate`, and `hf-completion-gate` skills are intentionally **pulled** by upstream nodes, not pushed by the user. Asking for "/gate" directly would encourage skipping implementation or review — that is why HarnessFlow ships no `/gate` command, on Claude Code or on OpenCode (ADR-001 D4).

## 5. What is NOT included in v0.1.0

Per ADR-001 D1 (P-Honest, "narrow but hard") and D11 (R1 concluded):

- No release / deployment / ops skills (no `hf-shipping-and-launch`, `hf-ci-cd-and-automation`, `hf-security-hardening`, `hf-performance-gate`, `hf-deprecation-and-migration`, `hf-debugging-and-error-recovery`, `hf-browser-runtime-evidence` in v0.1.0).
- No automated SKILL.md anatomy audit script.
- No batched `Common Rationalizations` / `Object Contract` rewrites across the 24 skills (D8 superseded, D10 voided).

These constraints are intentional. They keep the surface area small enough for the v0.1.0 pre-release to be honest about what it does and does not cover.

## 6. Where to look when something is wrong

| Symptom | Look at |
|---|---|
| Agent ignores HarnessFlow and writes code directly | Re-prompt explicitly: "Use HarnessFlow. Enter via `using-hf-workflow`." |
| Router routes to the wrong node | `skills/hf-workflow-router/SKILL.md` + `skills/hf-workflow-router/references/profile-node-and-transition-map.md` |
| Reviewer wants to edit the artifact under review | That violates author/reviewer separation — file an issue |
| `hf-test-driven-dev` keeps refusing to start | No `Current Active Task` is locked; ask the router to plan first |
| `hf-finalize` keeps bouncing back | A gate (regression / doc-freshness / completion) failed; follow the canonical next action it returned |

## 7. Cross-references

- ADR-001 (release scope decisions): `docs/decisions/ADR-001-release-scope-v0.1.0.md`
- Repository overview: `README.md` (English) / `README.zh-CN.md` (Chinese)
- Claude Code setup: `docs/claude-code-setup.md`
