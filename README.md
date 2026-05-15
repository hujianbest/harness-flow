# HarnessFlow

[English](README.md) | [Chinese](README.zh-CN.md)

**From idea to shipped product: high-quality engineering workflows for AI agents.**

> ## Scope Note (v0.6.0 pre-release)
>
> - **Version**: `v0.6.0`, marked as a **pre-release** on GitHub Releases. v0.6.0 is a **minor release** on top of v0.5.1 — the first large-scale **author-side discipline upgrade** in HF, translating 5 mechanisms verified in [code-yeongyu/oh-my-openagent (OMO)](https://github.com/code-yeongyu/oh-my-openagent) into HF's methodology layer (Atlas wisdom-notebook / Metis gap-analysis / Momus 4-dim rubric / Prometheus interview FSM / `/init-deep` hierarchical context). Full release scope decisions: [`docs/decisions/ADR-011-release-scope-v0.6.0.md`](docs/decisions/ADR-011-release-scope-v0.6.0.md) (8 decisions); roadmap lock + permanent v0.8 deletion: [`docs/decisions/ADR-008-omo-inspired-roadmap-v0.6-onwards.md`](docs/decisions/ADR-008-omo-inspired-roadmap-v0.6-onwards.md); fast-lane governance: [`docs/decisions/ADR-009-execution-mode-fast-lane-governance.md`](docs/decisions/ADR-009-execution-mode-fast-lane-governance.md); v0.7 runtime sidecar boundary: [`docs/decisions/ADR-010-harnessflow-runtime-sidecar-boundary.md`](docs/decisions/ADR-010-harnessflow-runtime-sidecar-boundary.md).
> - **v0.6.0 scope** — HF skill 总数 **24 → 28**（4 new SKILL.md：[`hf-wisdom-notebook`](skills/hf-wisdom-notebook/SKILL.md) cross-task knowledge accumulation with 5-file strong schema + stdlib python validator / [`hf-gap-analyzer`](skills/hf-gap-analyzer/SKILL.md) author-side self-check with 6-dim rubric / [`hf-context-mesh`](skills/hf-context-mesh/SKILL.md) hierarchical AGENTS.md generator with 3-client × 3-layer template / [`hf-ultrawork`](skills/hf-ultrawork/SKILL.md) explicit-opt-in fast-lane node with 5 non-compressibles enumerated locally + 6 escape conditions). 7 surgical modifications to existing SKILL.md (`hf-tasks-review` momus + N=3 rewrite loop / `hf-specify` 5-state Interview FSM / `hf-workflow-router` step-level recovery + category_hint + wisdom_summary + progress.md schema / `hf-code-review` CR9 AI Slop Detection rubric / `hf-test-driven-dev` FR-002 wisdom-notebook integration / `hf-completion-gate` §6.2 validator call / `using-hf-workflow` step 5 fast-lane row). Slash commands still **7** (no new commands). Constitution layer (`docs/principles/{soul,methodology-coherence,skill-anatomy}.md`) **unchanged**. `install.sh` / `uninstall.sh` / `.cursor/rules/harness-flow.mdc` / `.claude-plugin/marketplace.json` **unchanged** (NFR-003 strict). Three officially-supported clients unchanged (Claude Code / OpenCode / Cursor).
> - **Permanently dropped from roadmap (ADR-008 D1 + ADR-011 D3)**: 6 engineering-tail skills — `hf-shipping-and-launch` / `hf-ci-cd-and-automation` / `hf-security-hardening` / `hf-performance-gate` / `hf-debugging-and-error-recovery` / `hf-deprecation-and-migration`. **Not deferred — never to be implemented.** HF refuses to pretend to be a deployment tool; deployment / staged rollout / monitoring / rollback / health check / post-launch observation are **explicitly out-of-scope**, to be handled by the project's own ops pipelines.
> - **Officially supported clients**: **Claude Code**, **OpenCode**, and **Cursor** (unchanged from v0.3.0). The 4 remaining client expansions (Gemini CLI / Windsurf / GitHub Copilot / Kiro) are deferred to **v0.9** per ADR-011 D5.
> - **v0.7 runtime sidecar (ADR-010)**: an optional `harnessflow-runtime` OpenCode plugin (TypeScript/Bun, modeled on OMO's `src/tools/hashline-edit/` etc.) that adds hash-anchored editing, evidence-bus, progress-store, and 5 lifecycle hook categories. **Decoupled from this v0.6.0 markdown release** — independent npm package, separate version cadence (`compatible_hf_versions` declared per ADR-010 D5). OpenCode users will get the runtime when v0.7 ships; Cursor / Claude Code users stay on the markdown-only path (HYP-002 PASS proves markdown-only fast lane is functional without runtime).
> - **Main chain still ends at `hf-finalize`** — engineering-level closeout for a single feature/workflow. v0.5.0 added a closeout HTML companion (every closeout produces `closeout.html` alongside `closeout.md` per [ADR-005](docs/decisions/ADR-005-release-scope-v0.5.0.md)); v0.6.0 does not change `hf-finalize`'s output contract further. `hf-release` is a release-tier standalone skill that aggregates `workflow-closeout` features into a vX.Y.Z release; it is **not** part of the main chain.
> - This narrow surface is a deliberate choice ("P-Honest, narrow but hard" per ADR-001 D1 / ADR-002 D1 / ADR-003 D2 / ADR-004 D2 / ADR-005 D7 / **ADR-008 D1** / ADR-011 D3). HarnessFlow refuses to disguise "code merged / engineering closeout" as "shipped to production"; the v0.5.0 closeout HTML is a **visual rendering** of the closeout pack, **not** a deployment record; v0.6.0 fast lane is **explicit opt-in** by the architect, **never bypasses** Fagan author/reviewer separation or the 3 gate verdicts.
>
> See `docs/decisions/ADR-011-release-scope-v0.6.0.md` for v0.6.0 release scope; `docs/decisions/ADR-008..010-*.md` for the v0.6 OMO-inspired direction; `docs/decisions/ADR-006-skill-anatomy-v2-and-vendoring-fix.md` for v0.5.1; `docs/decisions/ADR-005-release-scope-v0.5.0.md` for v0.5.0; `docs/decisions/ADR-004-hf-release-skill.md` (hf-release standalone skill), `docs/decisions/ADR-003-release-scope-v0.3.0.md` (Cursor addition), `docs/decisions/ADR-002-release-scope-v0.2.0.md` (含 D11 校准说明) and `docs/decisions/ADR-001-release-scope-v0.1.0.md` for lineage.

HarnessFlow is a skill pack for AI agents that turns the full **idea → insight → architecture → implementation → delivery** arc into structured artifacts, quality discipline, and clear handoffs. Product discovery, specification, architecture design, task breakdown, gated TDD implementation, independent reviews, regression and completion gates, and formal closeout are all first-class stages, so agents move along an explicit "one idea → reviewable direction → reviewable design → executable tasks → shipped product" path instead of relying on ad hoc prompt chains.

## Acknowledgements

HarnessFlow stands on a small set of clearly-attributed engineering and product methods. Each entry below names the source and the `hf-*` skill (or constitution-layer document) where it lands.

| Source | Where it lands in HarnessFlow |
|---|---|
| [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) | `docs/principles/coding-principles.md` (Think Before Coding / Simplicity First (YAGNI) / Surgical Changes / Goal-Driven Execution); inlined into every `hf-*` `SKILL.md` |
| Software Engineering at Google + [Google engineering-practices guide](https://google.github.io/eng-practices/) | review cadence, change sizing, reviewer norms across `hf-*-review` skills |
| Eric Evans — *Domain-Driven Design* | `hf-design` (DDD strategic modeling: bounded context, ubiquitous language, context map) |
| Vaughn Vernon — *Implementing Domain-Driven Design* | `hf-design` (DDD tactical patterns: aggregate, value object, repository, domain service, application service, domain event) |
| Alberto Brandolini — Event Storming | `hf-design` (spec → design bridge) |
| Kent Beck — *Test-Driven Development* + Two Hats | `hf-test-driven-dev` (Canon TDD; Two Hats discipline) |
| Martin Fowler — *Refactoring*, *Patterns of Enterprise Application Architecture*, Front Controller | `hf-test-driven-dev` (refactoring playbook); `using-hf-workflow` (Front Controller); `hf-workflow-router` (FSM dispatch) |
| Robert C. Martin — *Clean Architecture*, SOLID | `hf-test-driven-dev` (architecture conformance check); `hf-code-review` (clean architecture review) |
| Michael Fagan — Fagan Inspection | `hf-discovery-review`, `hf-spec-review`, `hf-design-review`, `hf-ui-review`, `hf-tasks-review`, `hf-test-review`, `hf-code-review`, `hf-traceability-review` |
| Simon Brown — C4 Model | `hf-design` |
| Gernot Starke — ARC42 | `hf-design` |
| ISO/IEC 25010 — Quality Attribute model + Quality Attribute Scenarios | `hf-specify` (NFR framing); `hf-design` (NFR uptake via QAS) |
| Microsoft — STRIDE Threat Modeling | `hf-design` (lightweight threat modeling) |
| Jakob Nielsen — Heuristic Evaluation | `hf-ui-design`, `hf-ui-review` |
| W3C WAI — WCAG 2.2 AA | `hf-ui-design`, `hf-ui-review` |
| PMI — PMBOK (project closeout / handoff) | `hf-finalize` |
| Tony Ulwick / Clayton Christensen — Jobs-to-be-Done | `hf-product-discovery` |
| Teresa Torres — Opportunity Solution Tree | `hf-product-discovery` |
| [code-yeongyu/oh-my-openagent (OMO)](https://github.com/code-yeongyu/oh-my-openagent) — Atlas wisdom-notebook / Metis gap-analysis / Momus 4-dim rubric / Prometheus interview FSM / `/init-deep` hierarchical context / `comment-checker` ai-slop hook / boulder-loop fast-lane mechanics | v0.6 author-side discipline upgrade — `hf-wisdom-notebook` (5-file cross-task knowledge schema) / `hf-gap-analyzer` (6-dim author-side self-check) / `hf-tasks-review` (momus 4-dim rubric + N=3 rewrite loop) / `hf-specify` (5-state Interview FSM + spec.intake.md) / `hf-context-mesh` (3-client × 3-layer AGENTS.md) / `hf-code-review` (CR9 AI Slop Detection rubric) / `hf-ultrawork` (explicit-opt-in fast lane with 5 non-compressibles + 6 escape conditions) |

## Overview

HarnessFlow's primary path covers the full **idea-to-product** arc:

- **Cross-cutting coding principles** (constitution layer, not a workflow node): `docs/principles/coding-principles.md` — Think Before Coding / Simplicity First (YAGNI) / Surgical Changes / Goal-Driven Execution; each `hf-*` skill has absorbed these into its own `SKILL.md`, adapted from [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills)
- **Upstream product discovery**: problem framing, JTBD, Opportunity Solution Tree, RICE / ICE, Desired Outcome / North Star
- **Hypothesis validation**: `hf-experiment` — minimal probes when blocking or low-confidence hypotheses exist
- **Specification**: EARS + BDD + MoSCoW + INVEST + ISO 25010 + Quality Attribute Scenarios + Success Metrics / Key Hypotheses
- **Architecture design**: DDD Strategic Modeling + DDD Tactical Modeling (Aggregate / VO / Repository / Domain Service / Application Service / Domain Event) + Event Storming + C4 + ADR + ARC42 + NFR QAS uptake + lightweight STRIDE + Emergent vs Upfront Patterns governance (GoF intentionally emergent)
- **UI design** (activated when the spec declares a UI surface): IA + Atomic Design + Design Tokens + Nielsen + WCAG 2.2 AA + interaction state inventory
- **Task breakdown**: WBS + INVEST + dependency graph / critical path + Definition of Done
- **Single-task TDD implementation**: Canon TDD + Walking Skeleton + Two Hats + Clean Architecture conformance + fresh evidence
- **Browser runtime evidence** (verify-stage conditional side node, activated when the spec declares a UI surface and the active task touches a frontend surface): three-layer fresh evidence (DOM / Console / Network) + Walking Skeleton scenarios + Observation-not-Verdict (produces observations only; downstream gates decide pass/fail)
- **Independent reviews**: Fagan-style role separation for test / code / traceability / UI / discovery / spec / design / tasks reviews
- **Regression and completion gates**: impact-based regression + evidence bundle + Definition of Done
- **Formal closeout**: PMBOK-style task closeout and workflow closeout
- **Runtime routing and recovery**: `using-hf-workflow` / `hf-workflow-router` resume orchestration from artifacts, not chat memory
- **Side branches and learning loops**: `hf-hotfix` / `hf-increment`

Further evolution toward commercial-grade delivery (release, ops, metrics feedback, team collaboration, long-term architecture health, data / AI product tracks) is planned but not yet landed.

Internally, the current skill family uses the `hf-*` naming convention.

## The HF Method

HarnessFlow is not just a collection of prompts. It is a workflow methodology for agent-driven engineering.

At a high level, HF combines:

- **Spec-anchored SDD**: use specs, design docs, and task plans as structured working artifacts rather than oversized prompts
- **Gated TDD**: implement one `Current Active Task` at a time, require test design first, and keep RED/GREEN evidence fresh
- **Evidence-based routing**: recover the next step from on-disk artifacts instead of relying on chat memory
- **Independent review and gates**: keep test review, code review, traceability review, regression, and completion as separate quality nodes
- **Controlled closeout**: treat task completion and workflow completion as different decisions, with explicit finalize behavior

That gives HF a different shape from most agent workflows: it is optimized for correctness, recoverability, and engineering discipline, not just speed-to-first-code.

### Methodology layers

| Layer | HF methodology | Why it matters |
|-------|----------------|----------------|
| Intent | Spec-anchored SDD | Keeps scope, constraints, and acceptance criteria grounded in readable artifacts. |
| Execution | Gated TDD | Forces implementation to follow test design, RED/GREEN evidence, and one active task at a time. |
| Routing | Evidence-based workflow recovery | Lets the agent resume from repository state instead of informal conversation memory. |
| Review | Structured walkthroughs and traceability checks | Makes quality judgments explicit instead of folding them into implementation. |
| Verification | Regression and completion gates | Separates “it seems done” from “there is enough evidence to declare it done.” |
| Closeout | Formal closeout and handoff | Prevents code changes from ending without state sync, release notes, or workflow closure. |

### Methodology influences

HF draws from a small set of explicit engineering methods:

- Martin Fowler / Thoughtworks style **spec-driven development**
- Kent Beck style **test-driven development**
- Kent Beck / Fowler **Two Hats** discipline and **opportunistic / preparatory refactoring** for continuous architectural and code health during implementation
- Robert C. Martin style **Clean Architecture** conformance and SOLID checks at the implementation node
- **Fagan-style structured reviews** for review nodes
- **end-to-end traceability** for spec -> design -> tasks -> implementation -> verification
- **fresh evidence** as a first-class completion rule
- **PMBOK-style closeout thinking** for finalize and handoff

## Methodology By Skill

Every HF skill makes its methodology explicit in its own `SKILL.md`. At the pack level, the current methodology map looks like this:

### Cross-cutting coding principles (constitution layer)

| Document | Core principles |
|----------|-----------------|
| `docs/principles/coding-principles.md` | Think Before Coding, Simplicity First (YAGNI), Surgical Changes, Goal-Driven Execution — adapted from [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) |

These principles live in the constitution layer (`docs/principles/`) as HF's own design notes; each `hf-*` skill has already absorbed them into its `SKILL.md` so skills do not need to read these files at runtime. They are **not** part of the canonical `Next Action Or Recommended Skill` vocabulary, do **not** add a step to any node's Workflow, and do **not** replace review / gate / approval / finalize judgments.

### Entry and routing

| Skill | Core methodology |
|-------|------------------|
| `using-hf-workflow` | Front Controller Pattern, Evidence-Based Dispatch, Separation of Concerns |
| `hf-workflow-router` | Finite State Machine Routing, Evidence-Based Decision Making, Escalation Pattern |

### Upstream discovery

| Skill | Core methodology |
|-------|------------------|
| `hf-product-discovery` | Problem Framing, Hypothesis-Driven Discovery, Opportunity / Wedge Mapping, Assumption Surfacing, JTBD / Jobs Stories, Opportunity Solution Tree, RICE / ICE / Kano, Desired Outcome / North Star Framing |
| `hf-discovery-review` | Structured Walkthrough, Checklist-Based Review, Separation of Author/Reviewer Roles, Evidence-Based Verdict |
| `hf-experiment` (Phase 0) | Hypothesis-Driven Development, Build-Measure-Learn, Four Types of Assumptions (D/V/F/U), Smallest Testable Probe, Pre-registered Success Threshold |

### Authoring

| Skill | Core methodology |
|-------|------------------|
| `hf-specify` | EARS, BDD / Gherkin, MoSCoW Prioritization, Socratic Elicitation, INVEST, ISO/IEC 25010 + Quality Attribute Scenarios, Success Metrics & Key Hypotheses Framing, RICE / ICE / Kano (carried from discovery), **5-state Interview FSM (v0.6; OMO Prometheus interview-mode 启发) + spec.intake.md persistence** |
| `hf-spec-review` | Structured Walkthrough, Checklist-Based Review, Separation of Author/Reviewer Roles, Evidence-Based Verdict |
| `hf-design` | ADR, C4 Model, Risk-Driven Architecture, YAGNI + Complexity Matching, ARC42, DDD Strategic Modeling (Bounded Context / Ubiquitous Language / Context Map), DDD Tactical Modeling (Aggregate / VO / Repository / Domain Service / Application Service / Domain Event), Event Storming (spec→design bridge), Quality Attribute Scenarios (NFR uptake), Lightweight STRIDE Threat Modeling, Emergent vs Upfront Patterns governance |
| `hf-design-review` | ATAM, Structured Walkthrough, Separation of Author/Reviewer Roles, Traceability to Spec |
| `hf-ui-design` | Information Architecture, Atomic Design, Design System / Design Tokens, Nielsen Heuristics, WCAG 2.2 AA, Interaction State Inventory, ADR |
| `hf-ui-review` | ATAM (adapted to UI), Nielsen Heuristic Evaluation, Structured Walkthrough, Separation of Author/Reviewer Roles, Traceability to Spec |
| `hf-tasks` | WBS, INVEST Criteria, Dependency Graph + Critical Path, Definition of Done |
| `hf-tasks-review` | INVEST Validation, Dependency Graph Validation, Traceability Matrix, Structured Walkthrough, **Momus 4-dim boolean cliff rubric + N=3 rewrite loop (v0.6; OMO Momus 启发；Clarity 100% / Verification 90% / Context 80% / Big Picture 100% / Zero-tolerance 0%；4th rejected-rewrite → 阻塞 → architect escalation, aligned to fast-lane escape #5)** |
| `hf-gap-analyzer` (v0.6 new) | Author-side Self-Check (pre-Fagan; OMO Metis 启发), 6-Dimension Gap Rubric (Implicit Intent / AI Slop / Missing Acceptance / Unaddressed Edge Cases / Scope Creep / Dangling Reference), Anchored Findings, Explicit Absorption Markers — **NOT a Fagan review node**; outputs `<artifact>.gap-notes.md`, author absorbs / rejects each finding before submitting to corresponding review |

### Execution and reviews

| Skill | Core methodology |
|-------|------------------|
| `hf-test-driven-dev` | TDD, Walking Skeleton, Test Design Before Implementation, Fresh Evidence Principle, Two Hats (Beck/Fowler), Opportunistic + Boy Scout Refactoring, Preparatory Refactoring, Clean Architecture Conformance, Escalation Boundary, **Wisdom Notebook 5-file delta per task (v0.6; FR-002 集成 hf-wisdom-notebook) + tasks.progress.json step-level state sync** |
| `hf-test-review` | Fail-First Validation, Coverage Categories, Risk-Based Testing, Structured Walkthrough |
| `hf-code-review` | Fagan Code Inspection, Design Conformance Check, Defense-in-Depth Review, Clean Architecture Conformance Check, Two Hats / Refactoring Hygiene Review, Architectural Smells Detection, Separation of Author/Reviewer Roles, **CR9 AI Slop Detection rubric (v0.6; OMO comment-checker hook 启发；bilingual EN+ZH disallowed pattern lists + 4 exception scopes)** |
| `hf-traceability-review` | End-to-End Traceability, Zigzag Validation, Impact Analysis |
| `hf-browser-testing` (v0.2.0; verify-stage conditional side node) | Three-layer Runtime Evidence (DOM / Console / Network), Walking Skeleton Scenario, Fresh Evidence Principle, Observation-not-Verdict, Author/Reviewer/Gate Separation |

### Gates and closeout

| Skill | Core methodology |
|-------|------------------|
| `hf-regression-gate` | Regression Testing Best Practice, Impact-Based Testing, Fresh Evidence Principle |
| `hf-doc-freshness-gate` | Sync-on-Presence, Profile-Aware Rigor, Evidence Bundle Pattern, Author/Reviewer/Gate Separation |
| `hf-completion-gate` | Definition of Done, Evidence Bundle Pattern, Profile-Aware Rigor, **§6.2 Wisdom Notebook validity check (v0.6; calls `skills/hf-wisdom-notebook/scripts/validate-wisdom-notebook.py`)** |
| `hf-finalize` | Project Closeout, Release Readiness Review, Handoff Pack Pattern, Closeout HTML Companion (v0.5.0+) |

### Cross-task knowledge & fast lane (v0.6 new)

| Skill | Core methodology |
|-------|------------------|
| `hf-wisdom-notebook` (v0.6 new) | Cross-task Knowledge Accumulation (OMO Atlas notepads 启发), Append-only Audit Trail, Schema-Validated Persistence (5-file strong schema: learnings / decisions / issues / verification / problems), Handoff Summary Injection — paired stdlib python validator (`scripts/validate-wisdom-notebook.py`) called by `hf-completion-gate` |
| `hf-context-mesh` (v0.6 new) | Per-Client Template Set (OMO `/init-deep` 启发), 3-Layer Hierarchy (root / mid / leaf), Skeleton-Only Generation, Architect-Driven Client Choice — generates `AGENTS.md` (OpenCode) / `.cursor/rules/*.mdc` (Cursor) / `CLAUDE.md` (Claude Code) skeletons; **never writes conventions on architect's behalf** |
| `hf-ultrawork` (v0.6 new) | Architect-Explicit Opt-in (Execution Mode preference + keyword detection), Decision-Point Interception, Verdict-Then-Escape Check (per ADR-009 D3 第 4 项 6 escape conditions), Approval Artifact Persistence, Append-Only Audit Trail (`progress.md ## Fast Lane Decisions` per ADR-009 D4) — Hard Gates section locally enumerates **5 non-compressibles** (8 Fagan reviews / 3 gate verdicts / closeout pack / approval artifacts disk-write / Hard Gates "stop on unclear standard"); markdown-only declarative path (HYP-002 PASS) — runtime hooks come in v0.7 per ADR-010 |

### Routing & router internals upgraded for v0.6

`hf-workflow-router` (existing, v0.6 surgical upgrade): step-level recovery via `tasks.progress.json` (FR-003) + `category_hint` handoff field (FR-015 SHOULD; aligned to OMO category routing) + `wisdom_summary` injection (last N=3 task summaries ≤ 1500 token, from `notepads/`) + `progress.md ## Wisdom Delta` + `## Fast Lane Decisions` schema standardization (FR-010).

`using-hf-workflow` (existing, v0.6 surgical upgrade): step 5 entry bias table adds 1 row routing `Execution Mode = auto` direct-invokes to `hf-ultrawork` (steps 3 / 6 unchanged per ADR-009 D5; no new slash command).

### Branches and learning

| Skill | Core methodology |
|-------|------------------|
| `hf-hotfix` | Root Cause Analysis / 5 Whys, Minimal Safe Fix Boundary, Blameless Post-Mortem Mindset |
| `hf-increment` | Change Impact Analysis, Re-entry Pattern, Baseline-before-Change, Separation of Analysis and Implementation |

## Why These Methods Are Assigned To These Skills

HF does not assign methods arbitrarily. Each skill gets the methods that best match its job in the workflow.

- Entry and routing nodes use controller, state-machine, and evidence-based methods because their job is to decide where work should go next, not to write artifacts or code.
- Authoring nodes use requirements, architecture, and planning methods because they must turn vague intent into approved, testable, and decomposable artifacts.
- Review nodes use walkthroughs, checklists, inspection, and traceability methods because they exist to make independent quality judgments rather than continue authoring or implementation.
- Implementation uses TDD, walking skeleton, and fresh-evidence rules because this is the point where behavior claims can most easily become false confidence.
- Gates use definition-of-done, evidence-bundle, and impact-based verification methods because they answer a narrower question than review: whether the available evidence is sufficient to move forward or declare completion.
- Branch nodes use RCA and change-impact methods because hotfix and increment work are really about recovering from defects or re-entering the main workflow safely.
- Finalize uses closeout and handoff methods because “the task passed” is different from “the workflow is actually closed.”

### A Few Concrete Examples

| Skill | Why these methods fit |
|-------|-----------------------|
| `hf-specify` | It turns ambiguity into testable requirements, so it needs requirement syntax, prioritization, and elicitation methods rather than implementation methods. |
| `hf-design` | It turns approved intent into structure, interfaces, and tradeoffs, so it needs ADR, C4, and risk-driven architecture methods. |
| `hf-test-driven-dev` | It is where implementation claims must be proven against running behavior, so TDD and fresh evidence are central instead of optional. The same node is also the natural REFACTOR window for keeping clean architecture and clean code healthy, so Two Hats discipline, opportunistic / preparatory refactoring, Clean Architecture conformance, and an explicit escalation boundary live here too. |
| `hf-code-review` | Passing tests is not enough to prove correctness, robustness, or safety, so inspection and defense-in-depth methods belong here. The same node also enforces architectural health and refactoring hygiene by reviewing the implementation node's Refactor Note and checking conformance against the approved design and architectural smells. |
| `hf-completion-gate` | Completion is a judgment over combined artifacts, not a single test result, so definition-of-done and evidence-bundle thinking fit this node. |
| `hf-finalize` | Workflow closure includes state sync, release notes, and handoff, so closeout methods belong here instead of in implementation or gates. |

## Installation

HarnessFlow officially supports **Claude Code**, **OpenCode**, and **Cursor**. This section is about installing HarnessFlow into **your own project** so an AI agent can use it there. All three clients read the same `skills/` tree; they differ only in how they discover it (Claude Code: marketplace plugin + slash commands; OpenCode: `.opencode/skills/` discovery + NL routing; Cursor: `.cursor/rules/harness-flow.mdc` alwaysApply rule + NL routing).

> If you want to develop or contribute to HarnessFlow itself, see [`CONTRIBUTING.md`](CONTRIBUTING.md) — it covers cloning the repo and pointing your client at the working tree.

### Claude Code

Install via marketplace. Use the explicit HTTPS URL with the `.git` suffix to force HTTPS cloning; the `owner/repo` shortcut form would default to SSH and fail without GitHub SSH keys.

```text
/plugin marketplace add https://github.com/hujianbest/harness-flow.git
/plugin install harness-flow@hujianbest-harness-flow
```

This registers the slash commands listed under [Slash Commands](#slash-commands-claude-code).

> The install command is `harness-flow@hujianbest-harness-flow` (plugin name `harness-flow` + marketplace name `hujianbest-harness-flow`), **not** `harness-flow@harness-flow`. Full setup notes including SSH troubleshooting: `docs/claude-code-setup.md`.

### OpenCode and Cursor (install script)

For OpenCode and Cursor, vendor HarnessFlow into your project with the bundled install script. First clone the HarnessFlow repo to any local path, then point the script at your project:

```bash
git clone https://github.com/hujianbest/harness-flow.git /path/to/harness-flow

# OpenCode
bash /path/to/harness-flow/install.sh --target opencode --host /path/to/your/project

# Cursor
bash /path/to/harness-flow/install.sh --target cursor --host /path/to/your/project

# Both at once
bash /path/to/harness-flow/install.sh --target both --host /path/to/your/project

# Symlink topology (follow upstream updates instead of copying)
bash /path/to/harness-flow/install.sh --target both --topology symlink --host /path/to/your/project

# Uninstall later
bash /path/to/harness-flow/uninstall.sh --host /path/to/your/project
```

What the script writes into your project:

- `--target opencode` → `<host>/.opencode/skills/` (so OpenCode's `skill` tool can auto-discover HF; a bare `skills/` at the repo root is **not** picked up by OpenCode).
- `--target cursor` → `<host>/.cursor/harness-flow-skills/` plus `<host>/.cursor/rules/harness-flow.mdc` (an alwaysApply rule that loads `using-hf-workflow` on every Cursor session).
- `<host>/.harnessflow-install-manifest.json` — per-skill manifest so your own skills under `.opencode/skills/` or `.cursor/` survive uninstall.
- `<host>/.harnessflow-install-readme.md` — quick-verify commands and uninstall hints.

Manual fallback (`cp -R` or `ln -s`) and global-install topologies still work. Full install topologies, intent → node mapping, verification, and troubleshooting: `docs/opencode-setup.md` and `docs/cursor-setup.md`.

#### Windows

`install.sh` / `uninstall.sh` are bash scripts. On Windows you have three options:

1. **Git Bash** (recommended; bundled with [Git for Windows](https://git-scm.com/download/win)). Open Git Bash and run the same `bash /path/to/harness-flow/install.sh ...` commands shown above.
2. **PowerShell wrappers**. The repo also ships `install.ps1` / `uninstall.ps1`, which locate bash (Git Bash → `bash` on `PATH` → WSL) and forward all arguments, including translating Windows-style `--host C:\path\to\proj` to a POSIX path:

   ```powershell
   pwsh -File C:\path\to\harness-flow\install.ps1 --target both --host C:\src\my-project
   pwsh -File C:\path\to\harness-flow\uninstall.ps1 --host C:\src\my-project
   ```

3. **WSL**. Run the bash scripts inside your WSL distro the same way you would on Linux.

Caveat: `--topology symlink` on Windows requires Developer Mode enabled (Settings → Privacy & security → For developers) or running the shell elevated. Without that, `ln -s` under Git Bash silently degrades to a copy. Default `--topology copy` works without any of that.

After install, in your project send any natural-language intent and the router will pick the canonical next node from on-disk evidence:

```text
Use HarnessFlow. I want to add rate limiting to our notifications API.
Do not jump straight to code.
```

### Other clients

HarnessFlow skills are plain Markdown, so they may also work with Gemini CLI / Windsurf / GitHub Copilot / Kiro / Codex by referencing `skills/` as instruction files. Those paths are not part of the supported surface and have no setup doc.

### Quickstart Demo: WriteOnce

`examples/writeonce/` is the quickstart demo: a CLI that publishes a Markdown file to Medium (with Zhihu / WeChat MP declared as extension points but not implemented). The demo's deliverable is **the trail of HarnessFlow main-chain artifacts** — every node from `hf-product-discovery` through `hf-finalize` produced a reviewable artifact you can read in `examples/writeonce/`. The walking-skeleton implementation under `examples/writeonce/src/` ships with 23 passing tests (offline, < 400 ms).

Read order:

1. `examples/writeonce/README.md` — demo framing, scope, layout.
2. `examples/writeonce/docs/insights/2026-04-29-writeonce-discovery.md` — `hf-product-discovery` output.
3. `examples/writeonce/features/001-walking-skeleton/README.md` — feature entry + status snapshot.
4. Walk top-to-bottom through `spec.md` → `design.md` → `tasks.md` → `reviews/` → `verification/` → `closeout.md`.

### Repository layout to vendor

When you vendor HarnessFlow into another workspace, copy `skills/` only. Each `hf-*` skill is **self-contained**: its `SKILL.md`, `references/` (templates, rubrics, dispatch protocols, worktree guides) and `evals/` ship together inside the skill folder. There is no top-level `skills/docs/`, `skills/templates/` or `skills/principles/` you also need to keep around.

`docs/principles/` belongs to **the HarnessFlow repository itself** — HF's own design reference, not a runtime dependency, not a release gate, not a SKILL.md compliance baseline. You do **not** need to copy `docs/principles/` when vendoring.

> **Project conventions**: HF skills work with sensible defaults out of the box. If your project needs to override paths, templates, profile rules, execution mode, coverage thresholds or other policies, declare them wherever your repository already keeps such conventions (e.g. a project-level guidelines file, a `CONTRIBUTING.md`, or a host-tool config). Each `hf-*` skill points to "project-level convention (if declared)" — it does not require any particular sidecar file.

## Slash Commands (Claude Code)

The Claude Code plugin ships 7 short aliases. Every command is a **bias**, not a bypass — for the 6 router-bound commands the router still validates upstream preconditions from on-disk artifacts. `/release` is the exception: it **direct invokes** `hf-release` and bypasses the router (`hf-release` is decoupled from the router).

| Command | Bias toward | Notes |
|---|---|---|
| `/hf` | `using-hf-workflow` → `hf-workflow-router` | Default. Use this when you are not sure which node should run next. |
| `/spec` | `hf-specify` | Spec authoring / revision. |
| `/plan` | `hf-design` (and `hf-ui-design` when the spec declares a UI surface) or `hf-tasks` | Combined planning command — design + task breakdown are intentionally one command. |
| `/build` | `hf-test-driven-dev` | Only valid when exactly one `Current Active Task` is locked. |
| `/review` | router dispatches to the matching `hf-*-review` | Reviews are independent nodes with author/reviewer separation. |
| `/ship` | `hf-completion-gate` → `hf-finalize` | The gate decides whether finalize can actually run. Engineering-level closeout only — **not** production deployment. |
| `/release [version]` | **direct invoke** `hf-release` (does **not** go through the router) | Cut a vX.Y.Z engineer-level release: aggregate `workflow-closeout` features, draft scope ADR, run release-wide regression, sync CHANGELOG / release notes / ADR statuses, produce tag-ready pack. Does **not** deploy / staged-rollout / monitor / rollback (those are **explicitly out-of-scope** per ADR-008 D1, not "planned later"). |

Intentionally **not** included:

- No `/hotfix` — natural language + `/hf` lets the router branch into `hf-hotfix` / `hf-increment` for production defects or scope changes.
- No `/gate` — gates are pulled by the canonical next action of the upstream node, not pushed by the user. A `/gate` command would encourage skipping implementation or review.
- No `/ship-to-prod` (or similar deploy command) — deployment / staged rollout / monitoring / rollback are **explicitly out-of-scope** per ADR-008 D1 (HF will not pretend to be a deployment tool; this is a permanent decision, not a deferred one).

OpenCode and Cursor do not ship any slash command files; the same intents are reached via natural language + `using-hf-workflow`. The `using-hf-workflow` entry shell's entry bias table includes a row for "cut a release / tag a version" that direct invokes `hf-release` without going through the router.

## Quick Start

If you only try one prompt, try this:

```text
Use HarnessFlow from this repo. Start with `using-hf-workflow` and route me through the correct HF workflow.
I want to add rate limiting to our notifications API.
Do not jump straight to code.
```

Once that works, try realistic natural-language requests:

```text
Use HarnessFlow to write or revise the spec for rate limiting on the notifications API.
Use HarnessFlow to review this design draft against the approved spec.
Use HarnessFlow to implement the current active task with TDD and fresh evidence.
Use HarnessFlow to review the code for TASK-003.
Use HarnessFlow to decide whether the task is actually complete.
Use HarnessFlow to close out the completed task or workflow.
```

You can also use natural-language prompts:

```text
Use HarnessFlow and continue this repo from the current artifacts.
Use HarnessFlow to review this spec draft.
Use HarnessFlow to implement the current active task.
```

| You say | What HarnessFlow should do |
|---------|----------------------------|
| `Use HarnessFlow and continue this repo from the current artifacts.` | Start from `using-hf-workflow` or `hf-workflow-router` and recover the correct next node from on-disk state. |
| `Use HarnessFlow to figure out whether a product direction is worth pursuing before writing a spec.` | Bias toward `hf-product-discovery`, or hand off to `hf-workflow-router` if the current stage is still unclear. |
| `Use HarnessFlow to write or revise the spec for rate limiting on the notifications API.` | Bias toward `hf-specify`, or hand off to `hf-workflow-router` if the current stage is still unclear. |
| `Use HarnessFlow to review this design draft against the approved spec.` | Direct-invoke `hf-design-review` only if this is truly review-only and the design artifact is ready. |
| `Use HarnessFlow to implement the current active task with TDD and fresh evidence.` | Move toward `hf-test-driven-dev` if a single active task is locked and upstream approvals are in place. |
| `Use HarnessFlow to review the code for TASK-003.` | Route into `hf-code-review` only when the code-review preconditions are actually satisfied; otherwise recover the earlier required node. |
| `Use HarnessFlow to decide whether the task is actually complete.` | Route to `hf-completion-gate` rather than treating completion as a casual chat conclusion. |
| `Use HarnessFlow to close out the completed task or workflow.` | Use `hf-finalize` only when completion already allows closeout; otherwise stay in completion or router logic. |

Let the entry shell and router decide the next node from repository state. This repository does not ship public HF commands.

## See It Work

```text
You:    Use HarnessFlow from this repo. Start with `using-hf-workflow`.
        I want to add rate limiting to our notifications API.

HF:     Routes into `hf-specify`, clarifies scope, and prepares a spec-ready
        handoff instead of jumping straight into implementation.

You:    Use HarnessFlow to review this spec draft.

HF:     Runs `hf-spec-review`. If the spec is approved and the approval step is
        complete, the workflow can move to `hf-design`.

You:    The spec is approved. Use HarnessFlow to produce the design.

HF:     Uses `hf-design` to turn the approved intent into interfaces,
        structure, and technical decisions.

You:    Use HarnessFlow to review this design against the approved spec.

HF:     Runs `hf-design-review`. Only after that review passes and the approval
        step completes does the workflow move toward `hf-tasks`.

You:    Use HarnessFlow to break the design into tasks and prepare the next
        active task.

HF:     Uses `hf-tasks` and `hf-tasks-review`, then the router locks a single
        `Current Active Task` instead of letting multiple tasks drift.

You:    Use HarnessFlow to implement the current active task with TDD.

HF:     Enters `hf-test-driven-dev`, writes the test design first, handles the
        approval step, captures RED/GREEN evidence, and writes a canonical
        next action.

You:    Use HarnessFlow to review the tests, then the code, then the
        traceability for this task.

HF:     Moves through `hf-test-review` -> `hf-code-review` ->
        `hf-traceability-review` as evidence allows.

You:    Use HarnessFlow to run regression and decide whether this task is
        actually complete.

HF:     Uses `hf-regression-gate` and `hf-completion-gate` to decide whether
        the evidence is sufficient.

You:    Use HarnessFlow to close out the completed task.

HF:     If more approved tasks remain, it closes out the task and returns to
        `hf-workflow-router`. If no approved tasks remain and closeout is
        allowed, it enters `hf-finalize` for workflow closeout.
```

The point is not just to "use prompts." HarnessFlow reads artifacts, writes state,
and produces one controlled next move at each step. If the issue is really a
production defect or a scope change, the router can branch into `hf-hotfix` or
`hf-increment` instead of forcing the normal path.

## What Makes It Different

HarnessFlow treats engineering as a controlled workflow rather than a single giant agent step.

The pack explicitly separates:

- entry from runtime routing
- authoring from implementation
- implementation from review and gates
- task completion from workflow closeout

This keeps orchestration, execution, and quality judgment from collapsing into one opaque action.

## Workflow Shape

A typical full flow looks like this:

```text
using-hf-workflow
  -> hf-product-discovery
  -> hf-discovery-review
  -> (optional) hf-experiment     # inserted when blocking / low-confidence hypotheses exist
  -> hf-workflow-router
  -> hf-specify
  -> hf-spec-review
  -> (optional) hf-experiment     # inserted when the spec has unresolved blocking hypotheses
  -> hf-design  (|| hf-ui-design if the spec declares a UI surface)
  -> hf-design-review  (|| hf-ui-review)
  -> hf-tasks
  -> hf-tasks-review
  -> hf-test-driven-dev
  -> (optional) hf-browser-testing  # pulled in by the router when the spec declares a UI surface and the active task touches a frontend surface
  -> hf-test-review
  -> hf-code-review
  -> hf-traceability-review
  -> hf-regression-gate
  -> hf-doc-freshness-gate
  -> hf-completion-gate
  -> hf-finalize
```

> **Scope note**: the current Workflow Shape terminates at `hf-finalize` (engineering-level closeout for **a single feature**; v0.5.0 added a closeout HTML companion report — every closeout now also produces `closeout.html` alongside `closeout.md`). **Release & runtime concerns** split into two layers: (1) **release-tier version cut** (multi-feature → vX.Y.Z scope ADR + release-wide regression + release notes / CHANGELOG aggregation + tag readiness) is covered by the v0.4.0 standalone skill `hf-release`, which is **decoupled** from the main chain (it does not enter this Workflow Shape; it is triggered by `/release` in Claude Code or by the entry shell's bias row in OpenCode / Cursor). (2) **Deployment pipelines, observability, incident response, metric feedback, post-launch operations** are **explicitly out-of-scope** per [ADR-008 D1](docs/decisions/ADR-008-omo-inspired-roadmap-v0.6-onwards.md) — `hf-shipping-and-launch` / `hf-ci-cd-and-automation` / `hf-security-hardening` / `hf-performance-gate` / `hf-debugging-and-error-recovery` / `hf-deprecation-and-migration` are **permanently dropped** from the roadmap (not "planned later"). HF refuses to pretend to be a deployment tool; `hf-release` is "version cut + release docs", **not** "ship to production"; the v0.5.0 closeout HTML is a **visual rendering** of the closeout pack, **not** a deployment record.

`hf-experiment` is a Phase 0 **conditional insertion inside the discovery / spec stage**: it only kicks in when the draft holds blocking or low-confidence assumptions. After the probe result lands, the flow either returns to the original insertion point (assumption cleared) or falls back to the upstream authoring node (assumption falsified). See `hf-workflow-router/references/profile-node-and-transition-map.md` for activation and flow-back rules.

`hf-browser-testing` is a v0.2.0 (ADR-002 D1 / D7) **conditional side node inside the verify stage**. After `hf-test-driven-dev` reaches GREEN, the router pulls it in as the next recommended node only when (1) the spec explicitly declares a UI surface (or `hf-ui-design` is approved) and (2) the active task's impact surface touches a frontend / UI surface. It produces a three-layer fresh evidence bundle (DOM / Console / Network) plus an observations list under `features/<active>/verification/browser-evidence/<task-id>/`. It does **not** issue a verdict, does **not** modify implementation or test code, and does **not** alter the main-chain FSM. Flow-back is mechanical, driven by router-side observation severity counting: `0 blocking + 0 major` → `hf-regression-gate`; `≥ 1 blocking` → back to `hf-test-driven-dev` (with finding); `0 blocking + ≥ 1 major` → dispatched to whichever node is the majority `suggested next` in `observations.md` (typically `hf-test-review` or `hf-ui-review`). When any activation condition is unmet the router skips it and the main chain continues under normal transition rules. Full contract: `skills/hf-browser-testing/SKILL.md` and the `hf-browser-testing 激活与回流` section of `skills/hf-workflow-router/references/profile-node-and-transition-map.md`.

`hf-release` is a v0.4.0 **release-tier standalone skill** that lives **outside** this Workflow Shape. It is invoked when the user wants to cut a vX.Y.Z release after one or more features have been closed via `hf-finalize` (`workflow-closeout`). It reads each candidate feature's `closeout.md`, internalizes the release-wide regression and sync-on-presence protocols, and produces a tag-ready pack at `features/release-vX.Y.Z/release-pack.md`. It does **not** enter the router transition map, does **not** modify the main-chain FSM, and does **not** auto-execute `git tag` (those remain project-maintainer actions). See `skills/hf-release/SKILL.md` and `docs/decisions/ADR-004-hf-release-skill.md` for the full design.

When the spec declares a UI surface, the router activates `hf-ui-design` as a **conditional peer inside the design stage**. `hf-design` covers architecture, modules, API contracts, data models, and backend NFRs; `hf-ui-design` covers information architecture, user flows, interaction states, visual tokens, Atomic component mapping, and frontend a11y / i18n / responsive concerns. Both drafts go through their own independent review, and a joint `设计真人确认` is only opened after both `hf-design-review` and `hf-ui-review` return `通过`. See `skills/hf-workflow-router/references/ui-surface-activation.md` for the activation rules and Design Execution Modes (`parallel` / `architecture-first` / `ui-first`).

The router can also branch into `hf-hotfix` and `hf-increment` when the request is really a defect recovery or a scope change rather than normal forward progress.

## Design Principles

HarnessFlow is built around a few strong defaults:

- specs anchor intent
- routing follows on-disk evidence, not chat memory
- one active task is implemented at a time
- review and gates are first-class nodes
- quality claims require fresh evidence
- architectural and code health are maintained continuously inside the TDD REFACTOR window via Two Hats and an explicit escalation boundary, not deferred to a separate cleanup pass
- closeout is part of engineering, not an afterthought

## Repository Layout

```text
skills/                                # Redistributable skill pack (what you vendor)
  using-hf-workflow/
    SKILL.md
    evals/
  hf-workflow-router/
    SKILL.md
    references/
      workflow-shared-conventions.md   # progress schema / verdict vocab / record_path semantics
      review-dispatch-protocol.md
      reviewer-return-contract.md
      ...
    evals/
  hf-specify/
    SKILL.md
    references/
      spec-template.md
      feature-readme-template.md
      task-progress-template.md
      ...
    evals/
  hf-test-driven-dev/
    SKILL.md
    references/
      worktree-isolation.md            # worktree provisioning / safety / cleanup
      refactoring-playbook.md
      ...
    evals/
  hf-finalize/
    references/
      finalize-closeout-pack-template.md
  hf-regression-gate/
    references/
      verification-record-template.md
  hf-completion-gate/
    references/
      verification-record-template.md
  ... (one self-contained folder per hf-* skill)

docs/principles/                       # HarnessFlow's own design notes (NOT part of the skill pack)
  soul.md
  skill-anatomy.md
  sdd-artifact-layout.md
  ...
```

- `skills/<skill-name>/` is a self-contained skill: its `SKILL.md`, `references/` (templates, rubrics, sub-protocols), and `evals/` ship together. No cross-skill `skills/docs/` or `skills/templates/` directory.
- `docs/principles/` contains the higher-level design rationale behind the pack — these are HF's own design notes. Skills **do not depend on these files at runtime**; they have absorbed the relevant constraints into their own `SKILL.md`.

> **Templates are co-located with their owning skill** under `skills/<skill-name>/references/` (e.g. spec template under `hf-specify/references/`, closeout pack under `hf-finalize/references/`, verification record under each gate's `references/`). When auditing or generating artifacts, look inside the relevant skill's `references/`.

## Start Here

If you want to understand the pack quickly, read these files first:

1. `skills/using-hf-workflow/SKILL.md`
2. `skills/hf-workflow-router/SKILL.md`
3. `docs/principles/hf-sdd-tdd-skill-design.md`
4. `docs/principles/skill-anatomy.md`
5. `docs/principles/architectural-health-during-tdd.md`
6. `docs/principles/methodology-coherence.md` (methodology collaboration rules, anti-substitution pairs, Phase × profile activation matrix)

## Who It Is For

HarnessFlow is for teams and builders who want AI agents to carry **idea-to-product** engineering work with real rigor. It is especially useful when you want:

- structured product insight at idea stage (JTBD / OST / Desired Outcome), not gut calls
- thick architecture design — Bounded Context / Ubiquitous Language / Event Storming / NFR QAS / lightweight threat modeling all captured as reviewable artifacts
- stronger workflow boundaries and reviewable intermediate states
- better traceability across artifacts (discovery → spec → design → tasks → code → tests)
- safer and more recoverable multi-step execution in real repositories
- cross-session recovery driven by artifacts rather than chat memory

## Current Status

HarnessFlow is currently centered on a coding workflow pack. Phase 0 has thickened the product-insight and architecture-design layers (JTBD / OST / RICE / Desired Outcome / QAS / DDD / Event Storming / STRIDE / `hf-experiment`). Continued evolution toward commercial-grade delivery (release, operations, metrics feedback, collaboration, long-term architecture health, and data / AI product tracks) is planned for later phases.

The repository contains the current HF skill family, shared docs, templates, and supporting principles (including the methodology coherence / phase / profile activation map in `docs/principles/methodology-coherence.md`).
