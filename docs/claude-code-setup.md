# HarnessFlow on Claude Code

HarnessFlow v0.2.0 ships a Claude Code plugin so you can install the skill pack from the marketplace and use 6 short slash commands.

> **Scope (v0.2.0 pre-release).** v0.2.0 still officially supports only **Claude Code** and **OpenCode** (ADR-002 D11 revoked the in-flight 7-client expansion). Other clients (Cursor / Gemini CLI / Windsurf / GitHub Copilot / Kiro) are deferred to v0.3+. The HarnessFlow main chain still ends at `hf-finalize` (engineering-level closeout); v0.2.0 added `hf-browser-testing` as a verify-stage runtime evidence side node, but release pipelines / deployment / monitoring / security hardening / performance gating remain out of scope. See ADR-002 D1 / D11.

## 1. Marketplace install (recommended)

Use the **full HTTPS URL** form, not the `owner/repo` shortcut. Claude Code's marketplace defaults to SSH (`git@github.com:...`) when given a shortcut, which fails for users without GitHub SSH keys configured. Passing the explicit HTTPS URL forces HTTPS cloning:

```text
/plugin marketplace add https://github.com/hujianbest/harness-flow.git
/plugin install harness-flow@hujianbest-harness-flow
```

The install command is `harness-flow@hujianbest-harness-flow`, not `harness-flow@harness-flow`. The format is `<plugin-name>@<marketplace-name>`; HarnessFlow's marketplace is named `hujianbest-harness-flow` (mirroring `addyosmani/agent-skills`'s `addy-agent-skills` pattern) to keep it distinct from the plugin name `harness-flow`. Earlier v0.2.x docs incorrectly used `harness-flow@harness-flow`, which made Claude Code's resolver hit a name-collision bug; v0.2.1 renamed the marketplace to fix this.

After install, the following 6 slash commands become available in Claude Code:

| Command | Bias toward | Notes |
|---|---|---|
| `/hf` | `using-hf-workflow` -> `hf-workflow-router` | Default. Use this when you are not sure which node should run next. |
| `/spec` | `hf-specify` | Spec authoring / revision. Router still validates upstream preconditions. |
| `/plan` | `hf-design` (and `hf-ui-design` when the spec declares a UI surface) or `hf-tasks` | Combined planning command (design + task breakdown). |
| `/build` | `hf-test-driven-dev` | Only valid when exactly one `Current Active Task` is locked. |
| `/review` | router dispatches to the correct `hf-*-review` skill | Reviews are independent nodes (Fagan-style separation). |
| `/ship` | `hf-completion-gate` -> `hf-finalize` | Gate decides whether finalize can actually run. |

Hard rule: every command above is a **bias**, not a bypass. The router decides the actual next node from on-disk artifact evidence under your active feature directory.

> **Already hit the SSH error?** If you previously ran `/plugin marketplace add hujianbest/harness-flow` (the shortcut form) and saw `git@github.com: Permission denied (publickey)`, the marketplace entry registered partially but the install clone failed. Recover with:
>
> ```text
> /plugin marketplace remove hujianbest-harness-flow
> /plugin marketplace add https://github.com/hujianbest/harness-flow.git
> /plugin install harness-flow@hujianbest-harness-flow
> ```
>
> If you installed v0.2.0 with the older marketplace name `harness-flow`, run `/plugin marketplace remove harness-flow` (the old name) before re-adding — otherwise the old marketplace entry stays cached.
>
> **Alternative (global git config workaround)**: rewrite all SSH GitHub URLs to HTTPS once and for all:
>
> ```bash
> git config --global url."https://github.com/".insteadOf "git@github.com:"
> ```
>
> After that, even the shortcut form `/plugin marketplace add hujianbest/harness-flow` works. This affects **all** of your future GitHub clones, not just HarnessFlow — only do it if you want that side effect.
>
> **Long-term fix**: [add an SSH key to your GitHub account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account); then the original shortcut form (`hujianbest/harness-flow`) works without rewrites.

## 2. Local / development install

If you are iterating on HarnessFlow itself, install from a local clone:

```bash
git clone https://github.com/hujianbest/harness-flow.git
cd harness-flow
claude --plugin-dir "$PWD"
```

Claude Code will read:

- `.claude-plugin/plugin.json` — plugin manifest (name, version, license, commands path).
- `.claude-plugin/marketplace.json` — marketplace entry used when published.
- `.claude/commands/*.md` — the 6 slash command definitions.
- `skills/` — the 23 self-contained `hf-*` skills + `using-hf-workflow` (v0.2.0 added `hf-browser-testing` as the 23rd `hf-*`).

## 3. Verify the install

Run the smallest end-to-end check:

```text
/hf
I want to add rate limiting to our notifications API. Do not jump straight to code.
```

Expected behavior:

1. `using-hf-workflow` engages as the entry shell.
2. `hf-workflow-router` inspects on-disk state and selects the next node.
3. For a new feature with no prior artifacts, the router should route into `hf-product-discovery` or `hf-specify` (depending on what evidence already exists).

If the router skips straight into implementation (`hf-test-driven-dev`) without an approved spec / design / tasks chain, that is a **bug** — please open an issue.

## 4. What is NOT included in v0.2.0

Per ADR-001 D1 + ADR-002 D1 / D11 (P-Honest, "narrow but hard"):

- 6 of 7 deferred ops/release skills remain out of scope (`hf-shipping-and-launch`, `hf-ci-cd-and-automation`, `hf-security-hardening`, `hf-performance-gate`, `hf-deprecation-and-migration`, `hf-debugging-and-error-recovery`). Only `hf-browser-testing` was added in v0.2.0 (verify-stage runtime evidence side node, ADR-002 D1 / D7).
- No `/hotfix` or `/gate` slash command (use natural language + `/hf` to let the router branch into `hf-hotfix` / `hf-increment`; gates are pulled by the canonical next action, not pushed by the user).
- No 5-client expansion (Cursor / Gemini CLI / Windsurf / GitHub Copilot / Kiro) — ADR-002 D11 revoked the in-flight v0.2.0 expansion; deferred to v0.3+.
- No 3 user-facing personas (`hf-staff-reviewer` / `hf-qa-engineer` / `hf-security-auditor`) — ADR-002 D11 revoked; deferred to v0.3+.
- The SKILL.md anatomy audit script `scripts/audit-skill-anatomy.py` is **advisory** (does not block PR merge in maintainer workflows).

These constraints are intentional. They keep the surface area small enough for the v0.2.0 pre-release to be honest about what it does and does not cover.

## 5. Where to look when something is wrong

| Symptom | Look at |
|---|---|
| Slash command not visible after install | `.claude-plugin/plugin.json` `commands` path; reinstall plugin |
| Router routes to the wrong node | `skills/hf-workflow-router/SKILL.md` + `skills/hf-workflow-router/references/profile-node-and-transition-map.md` |
| `/build` refuses to start TDD | No `Current Active Task` is locked; run `/plan` first |
| `/ship` keeps bouncing back | A gate (regression / doc-freshness / completion) failed; follow the canonical next action it returned |
| Reviewer wants to edit the artifact under review | That violates author/reviewer separation — file an issue |

## 6. Cross-references

- ADR-002 (v0.2.0 release scope, with D11 narrowing): `docs/decisions/ADR-002-release-scope-v0.2.0.md`
- ADR-001 (v0.1.0 release scope): `docs/decisions/ADR-001-release-scope-v0.1.0.md`
- Repository overview: `README.md` (English) / `README.zh-CN.md` (Chinese)
- OpenCode setup: `docs/opencode-setup.md`
