# HarnessFlow on GitHub Copilot

HarnessFlow v0.2.0 supports GitHub Copilot through Copilot's **custom instructions** mechanism. Copilot doesn't have native slash-command extension or skill-pack discovery, so HF integrates by referencing the `skills/` tree from `.github/copilot-instructions.md` (auto-loaded by Copilot Chat / Copilot for VS Code / Copilot Workspace).

> **Scope (v0.2.0 pre-release).** v0.2.0 officially supports 7 clients: Claude Code, OpenCode, Cursor, Gemini CLI, Windsurf, GitHub Copilot, Kiro. Main chain ends at `hf-finalize` (engineering-level closeout); only `hf-browser-testing` was added in v0.2.0. See ADR-002 D1 / D2.

## How GitHub Copilot sees HF skills

Copilot loads the following on every chat session:

- `.github/copilot-instructions.md` — repo-level custom instructions (auto-loaded by Copilot Chat / Copilot Workspace).
- VS Code workspace instructions (settings.json `github.copilot.chat.codeGeneration.instructions`).

HarnessFlow keeps every `hf-*` skill self-contained under the top-level `skills/` directory. The shipped `.github/copilot-instructions.md` block (created in v0.2.0) tells Copilot to read the entry skill + router on every prompt.

## 1. Install

You have two install topologies.

### A. Use the HarnessFlow repository directly

```bash
git clone https://github.com/hujianbest/harness-flow.git
code harness-flow   # or: gh repo clone hujianbest/harness-flow && cd harness-flow
```

The repository ships `.github/copilot-instructions.md` (created in v0.2.0). Opening the repo in any Copilot-enabled IDE picks it up automatically.

### B. Vendor HarnessFlow into your own project

```bash
# From inside your project root, with harness-flow cloned alongside:
mkdir -p .github

# Append (or create) the HF instructions block:
cat ../harness-flow/.github/copilot-instructions.md >> .github/copilot-instructions.md

# And expose the skills tree itself:
ln -s ../harness-flow/skills .github/harness-flow-skills
```

If your repo already has a `.github/copilot-instructions.md`, append the HF block at the end and adjust the wording so the two don't conflict.

## 2. The shipped instructions block

`.github/copilot-instructions.md` tells Copilot:

1. Load `skills/using-hf-workflow/SKILL.md` as the entry shell.
2. Hand off to `skills/hf-workflow-router/SKILL.md` whenever intent is ambiguous, a review/gate just finished, or artifacts conflict.
3. Honor HarnessFlow's hard rules: one `Current Active Task` at a time, approvals and gates are first-class nodes, evidence-based routing.

Do not summarize the SKILL.md content into the instructions block — Copilot will treat the summary as the source of truth and lose the actual node contracts.

## 3. Verify the install

Open Copilot Chat (or Copilot Workspace) in this repo and ask:

> Use HarnessFlow from this repo. Load `using-hf-workflow` and route me through the correct HF workflow. I want to add rate limiting to our notifications API. Do not jump straight to code.

Expected:

1. Copilot reads `skills/using-hf-workflow/SKILL.md`.
2. Hands off to `skills/hf-workflow-router/SKILL.md`.
3. For a feature with no prior artifacts, the router routes into `hf-product-discovery` or `hf-specify`.

If Copilot jumps straight into `hf-test-driven-dev` without an approved spec/design/tasks chain, that is a **bug** — please open an issue.

## 4. Mapping from natural-language intent to HF nodes

GitHub Copilot doesn't ship slash commands for HF in v0.2.0 (Copilot's slash command extension surface is limited; ADR-002 D2 keeps the user surface narrow). Use natural language; the router selects:

| Intent | Router selects |
|---|---|
| "I'm not sure where we are, route me." | `using-hf-workflow` → `hf-workflow-router` |
| "Write / revise the spec for X." | `hf-specify` (after upstream discovery) |
| "Plan this — design and tasks." | `hf-design` (and `hf-ui-design` when UI surface declared) → `hf-tasks` |
| "Implement the current active task with TDD." | `hf-test-driven-dev` |
| "Verify the UI in a browser." | `hf-browser-testing` (post-GREEN, UI surface only) |
| "Review the [spec / design / UI / tasks / tests / code / traceability]." | corresponding `hf-*-review` |
| "Close out this task / workflow." | `hf-completion-gate` → `hf-finalize` |
| "Production defect, hotfix needed." | `hf-hotfix` |
| "Scope change, re-enter the workflow." | `hf-increment` |

Hard rule: every intent above is a **bias**. The router still inspects on-disk artifacts and routes upstream if preconditions are missing.

## 5. Troubleshooting

| Symptom | Look at |
|---|---|
| Copilot ignores HF and writes code directly | Re-prompt: "Use HarnessFlow. Load `using-hf-workflow` first." Verify `.github/copilot-instructions.md` is committed to the repo and contains the HF block. |
| Copilot doesn't see the instructions | Check whether your IDE has Copilot custom instructions enabled (`github.copilot.chat.codeGeneration.useInstructionFiles` in VS Code). |
| Skills reference broken paths | Ensure `skills/` is reachable from the project root (or symlinked under `.github/`). |
| Router routes to the wrong node | `skills/hf-workflow-router/SKILL.md` + `skills/hf-workflow-router/references/profile-node-and-transition-map.md`. |

## 6. What is NOT included in v0.2.0

Per ADR-002 D1 / D2:

- Only `hf-browser-testing` was added in v0.2.0; 6 other ops/release skills stay deferred to v0.3+.
- No HF-specific slash commands on Copilot.
- No `agents/` Copilot persona binding (HF personas live in `agents/hf-*.md` and are invoked via natural language; ADR-002 D8 keeps personas decoupled from Copilot's persona system).

## 7. Cross-references

- ADR-002 (v0.2.0 release scope decisions): `docs/decisions/ADR-002-release-scope-v0.2.0.md`
- Other client setups: `docs/claude-code-setup.md` / `docs/opencode-setup.md` / `docs/cursor-setup.md` / `docs/gemini-cli-setup.md` / `docs/windsurf-setup.md` / `docs/kiro-setup.md`
- GitHub Copilot custom instructions: <https://docs.github.com/en/copilot/customizing-copilot/about-customizing-github-copilot-chat-responses>
