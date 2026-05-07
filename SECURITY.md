# Security Policy

## Scope

HarnessFlow is a Markdown-based skill pack for AI coding agents. It does **not** ship runtime code that touches user machines, networks, or data on its own — agents that load these skills do. The security surface that this policy actually covers is therefore narrow:

- Skill content authored under `skills/`
- Setup paths described under `docs/claude-code-setup.md` and `docs/opencode-setup.md`
- The `.claude-plugin/` plugin manifest registered with Claude Code's marketplace
- The `examples/writeonce/` quickstart demo (a self-contained Node.js project under that directory)

Runtime behavior of any agent (Claude Code, OpenCode, Cursor, etc.) that loads HarnessFlow is **out of scope** for this policy — please report runtime issues to the agent vendor instead.

## Supported Versions

HarnessFlow follows SemVer. `v0.2.1` is the current pre-release (see [`CHANGELOG.md`](CHANGELOG.md)).

| Version | Supported for security fixes |
|---|---|
| `0.2.x` (current pre-release; latest `0.2.1`) | Best-effort; fixes shipped via patch releases on the `main` branch |
| `0.1.x` (previous pre-release) | Best-effort, security-only; users encouraged to upgrade to `0.2.x` |
| `< 0.1.0` | Not applicable (no prior public release) |

When `v1.0.0` ships, this table will be updated with a formal support window.

## Reporting a Vulnerability

If you believe you have found a security issue in HarnessFlow itself (not in an agent that loads it), please report it **privately**:

- Preferred: open a [GitHub Security Advisory](https://github.com/hujianbest/harness-flow/security/advisories/new) on this repository.
- Alternative: open a regular issue with the title `SECURITY: <short description>` and **omit details about exploitation**; a maintainer will follow up to move the discussion private.

When reporting, please include:

1. The affected file path or skill name (`skills/<name>/SKILL.md`, `examples/writeonce/src/...`, `.claude-plugin/...`, etc.).
2. A description of the issue and the impact you observed.
3. Reproduction steps if possible.
4. Any suggested mitigation.

Please do **not** disclose publicly until a fix is published or 90 days have elapsed since the report — whichever comes first. We will acknowledge receipt as soon as we can; given HarnessFlow currently has a single maintainer, please allow time for triage.

## Out of Scope

The following are **not** security issues for this repository, even though they may look adjacent:

- An agent (Claude Code, OpenCode, Cursor, etc.) misinterpreting a skill or producing unsafe code at runtime — that is an agent-vendor or user-prompt issue.
- A user vendoring HarnessFlow into a private workspace and then exposing secrets via their own configuration.
- The WriteOnce demo's Medium / Zhihu / WeChat MP adapters performing real network calls — they don't (per ADR-0003); the `Node20FetchHttpClient` exists for a hypothetical future integration and is not exercised by tests.
- The fact that v0.1.0 explicitly does **not** ship release / ops / monitoring skills (per [`docs/decisions/ADR-001-release-scope-v0.1.0.md`](docs/decisions/ADR-001-release-scope-v0.1.0.md) D1). This is a documented scope choice, not a security gap.

## Coordination

If a reported issue overlaps with another agent vendor (e.g. a Claude Code plugin manifest schema concern), we will coordinate disclosure with the relevant vendor before publishing a fix. We will credit reporters in `CHANGELOG.md` unless requested otherwise.
