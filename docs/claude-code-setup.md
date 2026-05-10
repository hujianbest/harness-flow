# HarnessFlow on Claude Code

HarnessFlow v0.6.0 ships a Claude Code plugin so you can install the skill pack from the marketplace and use 7 short slash commands. The orchestrator agent persona (`agents/hf-orchestrator.md`) is auto-activated on HF-intent queries via Claude Code's skill-discovery mechanism — no manual operation required.

> **Scope (v0.6.0 pre-release).** v0.6.0 officially supports 3 clients (unchanged from v0.3.0 / v0.4.0 / v0.5.x): **Claude Code**, **OpenCode**, and **Cursor**. The 4 remaining client expansions (Gemini CLI / Windsurf / GitHub Copilot / Kiro) stay deferred to v0.7+. **v0.6.0 introduces `agents/hf-orchestrator.md` as the canonical always-on agent persona** replacing `using-hf-workflow` + `hf-workflow-router` (now plugin-loading-channel + redirect aliases respectively through v0.6.x). On Claude Code, the orchestrator is loaded through Claude Code's skill-discovery mechanism — when you express HF intent (start a new session / `/hf-*` command / continue / review-gate completion / route unclear), the plugin's `skills/using-hf-workflow/SKILL.md` activates and reads `agents/hf-orchestrator.md` to adopt the orchestrator persona for the rest of the session (the `.claude-plugin/plugin.json` originally tried to register the agent persona via an `agents` array, but Claude Code's plugin schema does not accept that field; spec C-005 fallback engaged in pre-tag fix — see ADR-007 D1 Amendment for the loading-channel reconciliation). `agents/hf-orchestrator.md` remains the canonical single source of truth; on direct-clone hosts (Cursor) it is loaded directly via `.cursor/rules/harness-flow.mdc`. v0.5.x's closeout HTML companion in `hf-finalize` is unchanged. v0.4.0's `hf-release` (release-tier **standalone** skill + `/release` slash command) is unchanged. v0.6.0 does **not** grow the leaf skill set (still 24 `hf-*`), does **not** add slash commands (still 7), and does **not** touch the main-chain FSM (which now lives in the orchestrator's `agents/references/profile-node-and-transition-map.md`). The HarnessFlow main chain still ends at `hf-finalize`. The remaining 5 ops/release skills and 3 specialist personas all stay deferred to v0.7+ (ADR-005 D5 / D7 + ADR-007 D6 / D7). See `docs/decisions/ADR-007-orchestrator-extraction-and-skill-decoupling.md` for the full v0.6.0 scope decisions including the D1 Amendment.

## 1. Marketplace install (recommended)

Use the **full HTTPS URL** form, not the `owner/repo` shortcut. Claude Code's marketplace defaults to SSH (`git@github.com:...`) when given a shortcut, which fails for users without GitHub SSH keys configured. Passing the explicit HTTPS URL forces HTTPS cloning:

```text
/plugin marketplace add https://github.com/hujianbest/harness-flow.git
/plugin install harness-flow@hujianbest-harness-flow
```

The install command is `harness-flow@hujianbest-harness-flow`, not `harness-flow@harness-flow`. The format is `<plugin-name>@<marketplace-name>`; HarnessFlow's marketplace is named `hujianbest-harness-flow` (mirroring `addyosmani/agent-skills`'s `addy-agent-skills` pattern) to keep it distinct from the plugin name `harness-flow`. Earlier v0.2.x docs incorrectly used `harness-flow@harness-flow`, which made Claude Code's resolver hit a name-collision bug; v0.2.1 renamed the marketplace to fix this.

After install, the following 7 slash commands become available in Claude Code:

| Command | Bias toward | Notes |
|---|---|---|
| `/hf` | `using-hf-workflow` -> `hf-workflow-router` | Default. Use this when you are not sure which node should run next. |
| `/spec` | `hf-specify` | Spec authoring / revision. Router still validates upstream preconditions. |
| `/plan` | `hf-design` (and `hf-ui-design` when the spec declares a UI surface) or `hf-tasks` | Combined planning command (design + task breakdown). |
| `/build` | `hf-test-driven-dev` | Only valid when exactly one `Current Active Task` is locked. |
| `/review` | router dispatches to the correct `hf-*-review` skill | Reviews are independent nodes (Fagan-style separation). |
| `/ship` | `hf-completion-gate` -> `hf-finalize` | Gate decides whether finalize can actually run. Single-feature engineering-level closeout — **not** production deployment. |
| `/release [version]` | **direct invoke** `hf-release` (does **not** route through `hf-workflow-router`) | Cut a vX.Y.Z engineer-level release: aggregate `workflow-closeout` features, draft scope ADR, run release-wide regression, sync CHANGELOG / release notes / ADR statuses, produce tag-ready pack. Does **not** deploy / staged-rollout / monitor / rollback (those remain v0.6+ planned `hf-shipping-and-launch`, **not yet implemented**). ADR-004 D3 / D4. |

Hard rule: the first 6 commands are **bias**, not bypass — the router validates upstream preconditions from on-disk artifact evidence under your active feature directory. `/release` is the exception: it bypasses the router because `hf-release` is a standalone release-tier skill that reads disk artifacts directly (ADR-004 D3); it has its own internal Hard Gates (candidate features must be `workflow-closeout`, release-wide regression must be fresh, no auto `git tag`).

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
- `.claude/commands/*.md` — the 7 slash command definitions (v0.4.0 added `release.md`).
- `skills/` — the 24 self-contained `hf-*` skills + `using-hf-workflow` (v0.2.0 added `hf-browser-testing` as the 23rd `hf-*`; v0.4.0 added `hf-release` as the 24th, ADR-004 D1).

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

## 4. What is NOT included in v0.5.0

Per ADR-001 D1 + ADR-002 D1 / D11 + ADR-003 D2 / D3 / D6 + ADR-004 D2 / D3 (P-Honest, "narrow but hard"):

- All 6 originally-deferred ops/release skills (`hf-shipping-and-launch`, `hf-ci-cd-and-automation`, `hf-security-hardening`, `hf-performance-gate`, `hf-deprecation-and-migration`, `hf-debugging-and-error-recovery`) remain out of scope. v0.4.0 added a **new** skill `hf-release` (release-tier engineer-level version cut), and v0.5.0 added a **closeout HTML companion report** to `hf-finalize` — neither is one of the 6 original deferred ops/release skills, and neither replaces `hf-shipping-and-launch`; all three slices are orthogonal (closeout reviewer experience vs. version cut vs. ship to production). `/release` does **not** deploy. The v0.5.0 closeout HTML is a **visual rendering** of the closeout pack, **not** a deployment record.
- No `/hotfix` or `/gate` slash command (use natural language + `/hf` to let the router branch into `hf-hotfix` / `hf-increment`; gates are pulled by the canonical next action, not pushed by the user).
- No `/ship-to-prod` or similar deploy command — deployment is v0.6+ planned `hf-shipping-and-launch`, **not yet implemented**.
- No 4-client expansion (Gemini CLI / Windsurf / GitHub Copilot / Kiro) — Cursor was added in v0.3.0; the other 4 stay deferred to v0.6+.
- No 3 user-facing personas (`hf-staff-reviewer` / `hf-qa-engineer` / `hf-security-auditor`) — ADR-002 D11 revoked; ADR-004 D3 / ADR-005 D5 keep deferred to v0.6+ (and neither ADR-004 nor ADR-005 introduce personas).
- `hf-release` does **not** enter the router transition map — it is a standalone release-tier skill, decoupled from the main chain (ADR-004 D3). The router does not know it exists.
- `hf-release` does **not** auto-execute `git tag` or `git push --tags`. The skill produces a readiness pack only; tag operations are project-maintainer actions.
- The SKILL.md anatomy audit script `scripts/audit-skill-anatomy.py` is still **advisory** (does not block PR merge in maintainer workflows; ADR-003 D8 / ADR-004 inherits this stance).

These constraints are intentional. They keep the surface area small enough for the v0.5.0 pre-release to be honest about what it does and does not cover.

## 5. Where to look when something is wrong

| Symptom | Look at |
|---|---|
| Slash command not visible after install | `.claude-plugin/plugin.json` `commands` path; reinstall plugin |
| Router routes to the wrong node | `skills/hf-workflow-router/SKILL.md` + `skills/hf-workflow-router/references/profile-node-and-transition-map.md` |
| `/build` refuses to start TDD | No `Current Active Task` is locked; run `/plan` first |
| `/ship` keeps bouncing back | A gate (regression / doc-freshness / completion) failed; follow the canonical next action it returned |
| Reviewer wants to edit the artifact under review | That violates author/reviewer separation — file an issue |

## 6. Cross-references

- ADR-004 (v0.4.0 release scope: hf-release standalone skill + /release command): `docs/decisions/ADR-004-hf-release-skill.md`
- ADR-005 (v0.5.0 release scope: hf-finalize closeout HTML companion + skills/hf-finalize/scripts/render-closeout-html.py): `docs/decisions/ADR-005-release-scope-v0.5.0.md`
- ADR-003 (v0.3.0 release scope: Cursor-only client expansion): `docs/decisions/ADR-003-release-scope-v0.3.0.md`
- ADR-002 (v0.2.0 release scope, with D11 narrowing): `docs/decisions/ADR-002-release-scope-v0.2.0.md`
- ADR-001 (v0.1.0 release scope): `docs/decisions/ADR-001-release-scope-v0.1.0.md`
- `hf-release` skill: `skills/hf-release/SKILL.md`
- Repository overview: `README.md` (English) / `README.zh-CN.md` (Chinese)
- Other supported client setups: `docs/opencode-setup.md` / `docs/cursor-setup.md`
