---
name: hf-to-spec
description: 把当前会话综合为规格并落入特性目录/issue tracker,不访谈。HarnessFlow 主链第三步;进入前 gate check --to to-spec。完成后必须经 hf-review 规格评审才能进 architecture。
---

# To Spec

综合已有对话与代码库理解产出 spec。**不要访谈**——只综合已知。

## HarnessFlow 桥接

1. `hf_gate.py check --feature features/<id> --to to-spec`,RESULT 写入 progress。FAIL 停。
2. Tracker 未配置时默认把 spec 写入 `features/<id>/spec.md`;若已 `hf-setup-skills` 则按其 issue-tracker 发布。
3. 写完后走 `hf-review`(规格 checklist) → `reviews/spec-review.md` + 用户确认/`auto-approved`。
4. 通过后才能 `check --to to-architecture`。

## Process

1. Explore the repo if needed. Use `CONTEXT.md` vocabulary; respect ADRs.

2. Sketch test seams. Prefer existing seams; highest seam possible; fewer is better (ideal: one). Check seams with the user (`auto`: record assumption if you must choose).

3. Write the spec with the template below. Apply `ready-for-agent` when publishing to a real tracker.

## Spec template

## Problem Statement

The problem from the user's perspective.

## Solution

The solution from the user's perspective.

## User Stories

A LONG numbered list:

1. As an \<actor\>, I want a \<feature\>, so that \<benefit\>

## Implementation Decisions

Modules/interfaces touched, technical clarifications, schema/API contracts. No stale file-path laundry lists. Prototype snippets that encode a decision may be inlined and marked as such.

## Testing Decisions

What a good test is (external behavior); which modules/seams; prior art in the repo.

## Out of Scope

## Further Notes

文末加:

```markdown
- 用户确认:
```
