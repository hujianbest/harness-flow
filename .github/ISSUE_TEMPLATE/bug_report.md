---
name: Bug report
about: Something in HarnessFlow itself looks broken (constitution, playbooks, harness.py, installer, plugin manifest)
title: "[bug] "
labels: bug
assignees: ''
---

## Pre-flight

- [ ] I have read `README.md` and confirmed this is not a documented design choice (e.g. HarnessFlow deliberately prescribes no steps, stages, or templates — only invariants and checkpoints).
- [ ] This is an issue in HarnessFlow's files, not in the runtime behavior of the agent loading them (agent issues go to the agent vendor).

## Where

- [ ] The constitution (`skills/harness/SKILL.md`)
- [ ] A playbook (`skills/harness/references/`)
- [ ] The evidence protocol (`skills/harness/scripts/harness.py`)
- [ ] `scripts/install.py` or `scripts/validate_skills.py`
- [ ] Client wiring (`.cursor/rules/`, `.claude-plugin/`, `.opencode/`)
- [ ] Docs (`README*.md`, `CONTRIBUTING.md`, …)

## What happened

<!-- The broken content or behavior, with file path and, if applicable, the agent transcript excerpt showing the skill being misread. -->

## What you expected

## How to reproduce

<!-- For skill-behavior bugs: the prompt/task you gave the agent and the artifacts present in product/ and work/<slug>/ at the time. -->
