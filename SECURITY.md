# Security Policy

## Scope

HarnessFlow is a Markdown-based skill suite for AI coding agents. It does **not** ship runtime code that touches user machines, networks, or data on its own — agents that load these skills do. The security surface that this policy covers is therefore narrow:

- Skill content authored under `skills/` (core `hf-*` skills and `ext-*` extensions)
- The `scripts/validate_skills.py` validation script
- The `.claude-plugin/` plugin manifest registered with Claude Code's marketplace
- The `.cursor/rules/harness-flow.mdc` rule loaded by Cursor's rules system

Runtime behavior of any agent (Claude Code, OpenCode, Cursor, etc.) that loads HarnessFlow is **out of scope** for this policy — please report runtime issues to the agent vendor instead.

## Supported Versions

HarnessFlow follows SemVer. `v2.0.0` is the current stable release (see [`CHANGELOG.md`](CHANGELOG.md)).

| Version | Supported for security fixes |
|---|---|
| `2.0.x` (current stable) | Supported; fixes shipped via patch releases on the `main` branch |
| `1.0.x` and older | Best-effort, security-only; users encouraged to upgrade to `2.0.x` |

## Reporting a Vulnerability

If you believe you have found a security issue in HarnessFlow itself (not in an agent that loads it), please report it **privately**:

- Preferred: open a [GitHub Security Advisory](https://github.com/hujianbest/harness-flow/security/advisories/new) on this repository.
- Alternative: open a regular issue with the title `SECURITY: <short description>` and **omit details about exploitation**; a maintainer will follow up to move the discussion private.

When reporting, please include:

1. The affected file path or skill name (`skills/<name>/SKILL.md`, `.claude-plugin/...`, etc.).
2. A description of the issue and the impact you observed.
3. Reproduction steps if possible.
4. Any suggested mitigation.

Please do **not** disclose publicly until a fix is published or 90 days have elapsed since the report — whichever comes first. We will acknowledge receipt as soon as we can; given HarnessFlow currently has a single maintainer, please allow time for triage.

## Out of Scope

The following are **not** security issues for this repository, even though they may look adjacent:

- An agent (Claude Code, OpenCode, Cursor, etc.) misinterpreting a skill or producing unsafe code at runtime — that is an agent-vendor or user-prompt issue.
- A user vendoring HarnessFlow into a private workspace and then exposing secrets via their own configuration.
- The fact that HarnessFlow deliberately stops at engineering delivery (`hf-ship`) and ships no deployment / monitoring / rollback skills. This is a documented scope choice, not a security gap.

## Coordination

If a reported issue overlaps with another agent vendor (e.g. a Claude Code plugin manifest schema concern), we will coordinate disclosure with the relevant vendor before publishing a fix. We will credit reporters in `CHANGELOG.md` unless requested otherwise.
