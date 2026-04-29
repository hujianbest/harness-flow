# HarnessFlow on Claude Code

HarnessFlow v0.1.0 ships a Claude Code plugin so you can install the skill pack from the marketplace and use 6 short slash commands.

> **Scope (v0.1.0 pre-release).** v0.1.0 only officially supports **Claude Code** and **OpenCode**. Other clients (Cursor / Gemini CLI / Windsurf / GitHub Copilot / Kiro) are deferred to v0.2+. The HarnessFlow main chain ends at `hf-finalize` (engineering-level closeout); release / ops / monitoring / metrics-feedback are intentionally out of scope for this version. See ADR-001 D1 / D3.

## 1. Marketplace install (recommended)

```text
/plugin marketplace add hujianbest/harness-flow
/plugin install harness-flow@harness-flow
```

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

> **SSH errors during marketplace add?** The marketplace clones repositories over SSH by default. If you do not have SSH keys set up on GitHub, either [add an SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account), or rewrite git fetches to HTTPS:
>
> ```bash
> git config --global url."https://github.com/".insteadOf "git@github.com:"
> ```

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
- `skills/` — the 24 self-contained `hf-*` skills + `using-hf-workflow`.

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

## 4. What is NOT included in v0.1.0

Per ADR-001 D1 (P-Honest, "narrow but hard"):

- No release / deployment / ops skills (no `hf-shipping-and-launch`, `hf-ci-cd-and-automation`, `hf-security-hardening`, `hf-performance-gate`, `hf-deprecation-and-migration`, `hf-debugging-and-error-recovery`, `hf-browser-runtime-evidence` in v0.1.0).
- No `/hotfix` or `/gate` slash command (use natural language + `/hf` to let the router branch into `hf-hotfix` / `hf-increment`; gates are pulled by the canonical next action, not pushed by the user).
- No automated SKILL.md anatomy audit script (R1 was concluded by ADR-001 D11).

These constraints are intentional. They keep the surface area small enough for the v0.1.0 pre-release to be honest about what it does and does not cover.

## 5. Where to look when something is wrong

| Symptom | Look at |
|---|---|
| Slash command not visible after install | `.claude-plugin/plugin.json` `commands` path; reinstall plugin |
| Router routes to the wrong node | `skills/hf-workflow-router/SKILL.md` + `skills/hf-workflow-router/references/profile-node-and-transition-map.md` |
| `/build` refuses to start TDD | No `Current Active Task` is locked; run `/plan` first |
| `/ship` keeps bouncing back | A gate (regression / doc-freshness / completion) failed; follow the canonical next action it returned |
| Reviewer wants to edit the artifact under review | That violates author/reviewer separation — file an issue |

## 6. Cross-references

- ADR-001 (release scope decisions): `docs/decisions/ADR-001-release-scope-v0.1.0.md`
- Repository overview: `README.md` (English) / `README.zh-CN.md` (Chinese)
- OpenCode setup: `docs/opencode-setup.md`
