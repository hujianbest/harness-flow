# HarnessFlow

[English](README.md) | [Chinese](README.zh-CN.md)

High-quality engineering workflows for AI agents.

HarnessFlow is a skill pack for AI agents that brings structure, quality discipline, and clear handoffs to software engineering work. It combines a spec-anchored SDD model with a gated TDD execution loop so agents can move through planning, implementation, review, verification, and closeout with explicit stages instead of ad hoc prompt chains.

## Overview

This repository currently focuses on the HarnessFlow coding workflow pack. The current pack covers:

- public entry and workflow discovery
- upstream product discovery authoring and review
- runtime routing and recovery
- spec, design, and task authoring
- task-by-task test-driven implementation
- test, code, and traceability reviews
- regression and completion gates
- hotfix, increment, and finalize flows

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
- **Fagan-style structured reviews** for review nodes
- **end-to-end traceability** for spec -> design -> tasks -> implementation -> verification
- **fresh evidence** as a first-class completion rule
- **PMBOK-style closeout thinking** for finalize and handoff

## Methodology By Skill

Every HF skill makes its methodology explicit in its own `SKILL.md`. At the pack level, the current methodology map looks like this:

### Entry and routing

| Skill | Core methodology |
|-------|------------------|
| `using-hf-workflow` | Front Controller Pattern, Evidence-Based Dispatch, Separation of Concerns |
| `hf-workflow-router` | Finite State Machine Routing, Evidence-Based Decision Making, Escalation Pattern |

### Upstream discovery

| Skill | Core methodology |
|-------|------------------|
| `hf-product-discovery` | Problem Framing, Hypothesis-Driven Discovery, Opportunity / Wedge Mapping, Assumption Surfacing |
| `hf-discovery-review` | Structured Walkthrough, Checklist-Based Review, Separation of Author/Reviewer Roles, Evidence-Based Verdict |

### Authoring

| Skill | Core methodology |
|-------|------------------|
| `hf-specify` | EARS, BDD / Gherkin, MoSCoW Prioritization, Socratic Elicitation, INVEST |
| `hf-spec-review` | Structured Walkthrough, Checklist-Based Review, Separation of Author/Reviewer Roles, Evidence-Based Verdict |
| `hf-design` | ADR, C4 Model, Risk-Driven Architecture, YAGNI + Complexity Matching, ARC42 |
| `hf-design-review` | ATAM, Structured Walkthrough, Separation of Author/Reviewer Roles, Traceability to Spec |
| `hf-ui-design` | Information Architecture, Atomic Design, Design System / Design Tokens, Nielsen Heuristics, WCAG 2.2 AA, Interaction State Inventory, ADR |
| `hf-ui-review` | ATAM (adapted to UI), Nielsen Heuristic Evaluation, Structured Walkthrough, Separation of Author/Reviewer Roles, Traceability to Spec |
| `hf-tasks` | WBS, INVEST Criteria, Dependency Graph + Critical Path, Definition of Done |
| `hf-tasks-review` | INVEST Validation, Dependency Graph Validation, Traceability Matrix, Structured Walkthrough |

### Execution and reviews

| Skill | Core methodology |
|-------|------------------|
| `hf-test-driven-dev` | TDD, Walking Skeleton, Test Design Before Implementation, Fresh Evidence Principle |
| `hf-test-review` | Fail-First Validation, Coverage Categories, Bug-Pattern-Driven Testing, Structured Walkthrough |
| `hf-code-review` | Fagan Code Inspection, Design Conformance Check, Defense-in-Depth Review, Separation of Author/Reviewer Roles |
| `hf-traceability-review` | End-to-End Traceability, Zigzag Validation, Impact Analysis |

### Gates and closeout

| Skill | Core methodology |
|-------|------------------|
| `hf-regression-gate` | Regression Testing Best Practice, Impact-Based Testing, Fresh Evidence Principle |
| `hf-completion-gate` | Definition of Done, Evidence Bundle Pattern, Profile-Aware Rigor |
| `hf-finalize` | Project Closeout, Release Readiness Review, Handoff Pack Pattern |

### Branches and learning

| Skill | Core methodology |
|-------|------------------|
| `hf-hotfix` | Root Cause Analysis / 5 Whys, Minimal Safe Fix Boundary, Blameless Post-Mortem Mindset |
| `hf-increment` | Change Impact Analysis, Re-entry Pattern, Baseline-before-Change, Separation of Analysis and Implementation |
| `hf-bug-patterns` | Defect Pattern Catalog, Blameless Post-Mortem / Learning Review, Human-In-The-Loop Knowledge Curation |

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
| `hf-test-driven-dev` | It is where implementation claims must be proven against running behavior, so TDD and fresh evidence are central instead of optional. |
| `hf-code-review` | Passing tests is not enough to prove correctness, robustness, or safety, so inspection and defense-in-depth methods belong here. |
| `hf-completion-gate` | Completion is a judgment over combined artifacts, not a single test result, so definition-of-done and evidence-bundle thinking fit this node. |
| `hf-finalize` | Workflow closure includes state sync, release notes, and handoff, so closeout methods belong here instead of in implementation or gates. |

## Installation

HarnessFlow is currently distributed as source. Clone the repository and keep the pack layout intact.

```bash
git clone <repo-url> HarnessFlow
cd HarnessFlow
```

Keep these directories together:

- `skills/`
- `skills/docs/`
- `skills/templates/`
- `docs/principles/`

If you vendor HarnessFlow into another skill workspace, copy the full pack structure rather than only isolated `hf-*` folders, because the skills share pack-level docs and templates.

There is not yet a one-command registry install for this pack.

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
`hf-increment` instead of forcing the normal path. If recurring mistakes emerge,
`hf-bug-patterns` remains an optional knowledge-capture side path rather than a
mandatory gate.

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
  -> hf-workflow-router
  -> hf-specify
  -> hf-spec-review
  -> hf-design  (|| hf-ui-design if the spec declares a UI surface)
  -> hf-design-review  (|| hf-ui-review)
  -> hf-tasks
  -> hf-tasks-review
  -> hf-test-driven-dev
  -> hf-test-review
  -> hf-code-review
  -> hf-traceability-review
  -> hf-regression-gate
  -> hf-completion-gate
  -> hf-finalize
```

When the spec declares a UI surface, the router activates `hf-ui-design` as a **conditional peer inside the design stage**. `hf-design` covers architecture, modules, API contracts, data models, and backend NFRs; `hf-ui-design` covers information architecture, user flows, interaction states, visual tokens, Atomic component mapping, and frontend a11y / i18n / responsive concerns. Both drafts go through their own independent review, and a joint `设计真人确认` is only opened after both `hf-design-review` and `hf-ui-review` return `通过`. See `skills/hf-workflow-router/references/ui-surface-activation.md` for the activation rules and Design Execution Modes (`parallel` / `architecture-first` / `ui-first`).

The router can also branch into `hf-hotfix` and `hf-increment` when the request is really a defect recovery or a scope change rather than normal forward progress.

## Design Principles

HarnessFlow is built around a few strong defaults:

- specs anchor intent
- routing follows on-disk evidence, not chat memory
- one active task is implemented at a time
- review and gates are first-class nodes
- quality claims require fresh evidence
- closeout is part of engineering, not an afterthought

## Repository Layout

```text
skills/
  using-hf-workflow/
  hf-workflow-router/
  hf-*/
  docs/
  templates/

docs/principles/
  hf-sdd-tdd-skill-design.md
  skill-anatomy.md
```

- `skills/` contains the installable workflow skills.
- `skills/docs/` contains shared guidance used across the pack.
- `skills/templates/` contains reusable record and handoff templates.
- `docs/principles/` contains the higher-level design rationale behind the pack.

## Start Here

If you want to understand the pack quickly, read these files first:

1. `skills/using-hf-workflow/SKILL.md`
2. `skills/hf-workflow-router/SKILL.md`
3. `docs/principles/hf-sdd-tdd-skill-design.md`
4. `docs/principles/skill-anatomy.md`

## Who It Is For

HarnessFlow is for teams and builders who want AI agents to do real engineering work with more rigor. It is especially useful when you want:

- stronger workflow boundaries
- reviewable intermediate states
- better traceability across artifacts
- safer multi-step execution in real repositories
- clearer recovery between sessions

## Current Status

HarnessFlow is currently centered on a coding workflow pack. The repository contains the current HF skill family, shared docs, templates, and supporting principles for that pack.
