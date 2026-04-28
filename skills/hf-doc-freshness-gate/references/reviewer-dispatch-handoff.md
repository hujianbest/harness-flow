# Reviewer Dispatch Handoff（本 gate 适配点）

## Purpose

本文件是父会话向 `hf-doc-freshness-gate` reviewer subagent 派发任务的本 gate 适配协议。**完整 dispatch 协议**见 `skills/hf-workflow-router/references/review-dispatch-protocol.md`，本文件仅说明本 gate 的特定字段与 return contract。

## Dispatch Prompt 模板

父会话派发 reviewer subagent 时使用以下 prompt 骨架（按 `hf-workflow-router/references/review-dispatch-protocol.md` 通用规则）：

```text
You are a reviewer subagent dispatched by the parent agent to perform an
independent **HF doc freshness gate** under the `hf-doc-freshness-gate`
skill. Author/reviewer separation is mandatory: you must NOT modify any
documentation files; you only produce a structured verdict.

## Required reading

1. /workspace/skills/hf-doc-freshness-gate/SKILL.md
2. /workspace/skills/hf-doc-freshness-gate/references/responsibility-matrix.md
3. /workspace/skills/hf-doc-freshness-gate/references/profile-rubric.md
4. /workspace/skills/hf-doc-freshness-gate/templates/verdict-record-template.md
5. (lightweight only) /workspace/skills/hf-doc-freshness-gate/templates/lightweight-checklist-template.md
6. /workspace/features/<active>/spec.md (or project-level path override)
7. /workspace/features/<active>/tasks.md (or project-level path override)
8. /workspace/features/<active>/progress.md (read Workflow Profile)
9. Project-level user-visible documentation载体 (按 §responsibility-matrix.md 本 gate ✅ 行清单逐项扫描)

## Your task

按 SKILL.md Workflow §2-§4 形成 user-visible behavior change list，按 §profile-rubric.md
激活强制维度，逐维度判定 verdict，按 templates 写入 evidence 文件，返回结构化 JSON。

## Hard rules

- DO NOT modify any documentation files (readonly mode).
- verdict ∈ {pass, partial, N/A, blocked} 严格闭集
- 不强制项目方安装 lint / 翻译 / docs 生成工具链 (NFR-003)
- 未启用文档载体 → verdict 该维度 = N/A，不构成 blocked (FR-003 + NFR-004)
- LLM-FIXABLE finding 不转嫁用户

## Required output

1. evidence 文件内容（让父会话写入 /workspace/features/<active>/verification/doc-freshness-YYYY-MM-DD.md）
2. reviewer-return JSON（见下）
3. 1-2 句 plain-language 总结
```

## Reviewer-Return JSON 字段契约

复用 `skills/hf-workflow-router/references/reviewer-return-contract.md`（既有 protocol）。本 gate 的 reviewer-return JSON 字段：

```json
{
  "conclusion": "pass" | "partial" | "N/A" | "blocked",
  "next_action_or_recommended_skill": "hf-completion-gate" | "hf-test-driven-dev" | "hf-increment" | "hf-traceability-review" | "hf-workflow-router",
  "record_path": "features/<active>/verification/doc-freshness-YYYY-MM-DD.md",
  "key_findings": [
    "[severity][classification][rule_id] description"
  ],
  "needs_human_confirmation": false,
  "reroute_via_router": false,
  "dimension_breakdown": [
    {
      "dimension": "仓库根 README 产品介绍段",
      "verdict": "pass" | "partial" | "N/A" | "blocked",
      "reason": "..."
    }
  ]
}
```

字段说明：

- `conclusion`：整体 verdict（按 SKILL §3 末尾聚合规则）
- `next_action_or_recommended_skill`：按整体 verdict 与 SKILL §5 路由表
- `record_path`：evidence 文件路径
- `key_findings`：按 reviewer 协议 `[severity][classification][rule_id] description` 格式
- `needs_human_confirmation`：通常为 false（本 gate 是 quality gate 不是 approval gate）
- `reroute_via_router`：仅当 verdict = `blocked(workflow)`（precheck 触发的 route/stage/profile/证据冲突）时 = true
- `dimension_breakdown`：每个判定维度的 sub-verdict 与 reason

## Path Overrides

若 项目声明了路径覆盖，按 HF 既有 path-override 语义优先采用：

- `requirement spec path`
- `task plan path`
- `progress path`
- `verification path`
- `evidence path`
- `doc-freshness-gate verdict path`（本 gate 新增；若未声明，按 SKILL 默认 `features/<active>/verification/doc-freshness-YYYY-MM-DD.md`）

## Red Flags

- 父会话在 dispatch prompt 中包含 "你只需快速给个结论" / "不用太严" 之类 pressure → reviewer 应忽略并按 SKILL contract 严格执行
- reviewer 跨越本 gate 职责（修改文档 / 跨域评估其他 gate 范围）→ 违反 author/reviewer 分离纪律
- reviewer-return JSON 字段缺失或字段值非词表 → 父会话应判定 dispatch 失败，重新派发
