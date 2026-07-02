---
name: Bug report
about: Something in HarnessFlow itself looks broken (skill content, checklists, validation script, plugin manifest)
title: "[bug] "
labels: bug
assignees: ''
---

## Pre-flight

- [ ] I have read `README.md` and confirmed this is not a documented scope choice (e.g. HarnessFlow deliberately ships no deployment / monitoring / rollback skills and stops at `hf-ship`).
- [ ] This is an issue in HarnessFlow's files, not in the runtime behavior of the agent loading them (agent issues go to the agent vendor).

## Where

- [ ] A core skill (`skills/hf-*/`)
- [ ] An extension (`skills/ext-*/`)
- [ ] A review checklist (`skills/hf-review/references/`)
- [ ] `scripts/validate_skills.py`
- [ ] Client wiring (`.cursor/rules/`, `.claude-plugin/`, `.opencode/`)
- [ ] Docs (`README*.md`, `CONTRIBUTING.md`, …)

## What happened

<!-- The broken content or behavior, with file path and, if applicable, the agent transcript excerpt showing the skill being misread. -->

## What you expected

## How to reproduce

<!-- For skill-behavior bugs: the prompt/task you gave the agent and the artifacts present in features/<NNN>-<slug>/ at the time. -->
