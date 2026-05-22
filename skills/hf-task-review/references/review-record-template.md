# Task Review Record Template (file mode)

本模板仅用于 `hf-task-review` 的 **file mode**（verdict ≠ `通过`、含 HIGH+ findings、或项目 `Audit Mode: file`）。
默认 **snapshot mode** 不落本文件，由父会话把 ≤ 10 行 snapshot 写到 `features/<active>/progress.md` 的 `## Task NNN Review Snapshot` 段。

## 保存路径

默认：`features/<active>/reviews/task-review-task-NNN.md`
同 task 多轮回流：`features/<active>/reviews/task-review-task-NNN-r2.md` / `-r3.md` ...

若项目声明了等价路径，按映射保存。

## 记录结构

```markdown
# Task Review — Task NNN — Round R

## Metadata
- Task ID: TASK-NNN
- Risk Tag: trivial | standard | high-risk
- Profile: lightweight | standard | full
- Remediation Round Count: 1 | 2 | 3
- Audit Mode: snapshot-allowed | file
- Workspace Isolation: in-place | worktree-required | worktree-active
- Worktree Path / Branch: <若适用>

## Upstream Evidence Consumed
- 实现交接块: <progress.md 锚点>
- Refactor Note: <progress.md 锚点>
- 任务卡 (tasks.md): <锚点>
- spec / design 锚点: <仅 task 直接锚定的段>
- 项目缺陷模式 / 风险清单: <若存在>

## Sub-dimension Scores

### A. Test Quality (TT / TA)
| 维度 | 分数 (0-10) | 备注 |
|---|---|---|
| TT1 Fail-first 有效性 | | |
| TT2 行为/验收映射 | | |
| TT3 风险覆盖 | | |
| TT4 测试设计质量 | | |
| TT5 新鲜证据完整性 | | |
| TT6 下游就绪度 | | |

### B. Code Quality (CR / CA)
| 维度 | 分数 (0-10) | 备注 |
|---|---|---|
| CR1 正确性 | | |
| CR2 设计一致性 | | |
| CR3 状态/错误/安全 | | |
| CR4 可读性 | | |
| CR5 范围守卫 | | |
| CR6 下游追溯就绪 | | |
| CR7 架构健康与重构纪律 | | （含 CR7.1-7.5 子维度，若任一 < 6 单独列出）|
| CR8 UI 实现一致性 | | （非触碰 UI 时写 N/A） |
| CR9 Comment 质量 / AI Slop | | |

### C. Task-Level Traceability (TZ task-local 子集)
| 维度 | 分数 (0-10) | 备注 |
|---|---|---|
| TZ3 本 task 实现 → 认领的 FR / Acceptance | | |
| TZ4 触碰工件 ↔ 任务卡 Files 段 | | |
| TZ6 本 task 测试 ↔ 任务卡测试设计种子 | | |

## Findings

按 sub_dimension 分组列出。每条 finding 必带 severity / classification / rule_id。

### test_quality
- [critical|important|minor][USER-INPUT|LLM-FIXABLE][TT5] <一行说明>

### code_quality
- [critical|important|minor][USER-INPUT|LLM-FIXABLE][CR7.3] <一行说明>

### task_traceability
- [critical|important|minor][USER-INPUT|LLM-FIXABLE][TZ3] <一行说明>

## 整体结论

通过 | 需修改 | 阻塞

## 下一步
- 通过 → `hf-regression-gate`
- 需修改 → `hf-test-driven-dev`
- 阻塞（可回实现补救） → `hf-test-driven-dev`
- 阻塞（escalation-bypass / 重编排 / 第 3 轮 budget 耗尽） → `hf-workflow-router`（`reroute_via_router=true`）
```

## 结构化返回 JSON

正常返回示例（v0.7 字段集）：

```json
{
  "conclusion": "需修改",
  "next_action_or_recommended_skill": "hf-test-driven-dev",
  "record_mode": "file",
  "record_path": "features/003-foo/reviews/task-review-task-005-r2.md",
  "key_findings": [
    "[important][LLM-FIXABLE][CR7.3] handler 直接调用 infra 层，违反 dependency rule",
    "[important][LLM-FIXABLE][TT3] 风险清单中 race 场景未覆盖"
  ],
  "finding_breakdown": {
    "test_quality": [
      {"severity": "important", "classification": "LLM-FIXABLE", "rule_id": "TT3", "summary": "race 场景未覆盖"}
    ],
    "code_quality": [
      {"severity": "important", "classification": "LLM-FIXABLE", "rule_id": "CR7.3", "summary": "handler 直接调用 infra 层"}
    ],
    "task_traceability": []
  },
  "remediation_round_count": 2,
  "needs_human_confirmation": false,
  "reroute_via_router": false
}
```

Snapshot mode 返回示例（`通过` + 无 HIGH+ findings）：

```json
{
  "conclusion": "通过",
  "next_action_or_recommended_skill": "hf-regression-gate",
  "record_mode": "snapshot",
  "record_path": "features/003-foo/progress.md#task-005-review-snapshot",
  "key_findings": [],
  "finding_breakdown": {
    "test_quality": [],
    "code_quality": [],
    "task_traceability": []
  },
  "snapshot_lines": [
    "Task ID: TASK-005",
    "Scores: test 8/8/9/8/9/8 | code 9/8/9/8/9/8/9/N-A/9 | trace 9/9/9",
    "Verdict: 通过",
    "Non-blocking notes: none",
    "Next: hf-regression-gate"
  ],
  "remediation_round_count": 1,
  "needs_human_confirmation": false,
  "reroute_via_router": false
}
```

Escalation 阻塞示例：

```json
{
  "conclusion": "阻塞",
  "next_action_or_recommended_skill": "hf-workflow-router",
  "record_mode": "file",
  "record_path": "features/003-foo/reviews/task-review-task-005-r1.md",
  "key_findings": [
    "[critical][USER-INPUT][CA8] 实现跨 3 个模块引入新的 dependency direction，触发 escalation-bypass"
  ],
  "finding_breakdown": {
    "test_quality": [],
    "code_quality": [
      {"severity": "critical", "classification": "USER-INPUT", "rule_id": "CA8", "summary": "跨模块结构性变更未走 hf-increment"}
    ],
    "task_traceability": []
  },
  "remediation_round_count": 1,
  "needs_human_confirmation": false,
  "reroute_via_router": true
}
```

第 3 轮 budget 耗尽示例：

```json
{
  "conclusion": "阻塞",
  "next_action_or_recommended_skill": "hf-workflow-router",
  "record_mode": "file",
  "record_path": "features/003-foo/reviews/task-review-task-005-r3.md",
  "key_findings": [
    "[important][LLM-FIXABLE][TT3] 第 3 轮回流仍未覆盖 race 场景；remediation budget 已耗尽"
  ],
  "remediation_round_count": 3,
  "needs_human_confirmation": false,
  "reroute_via_router": true
}
```
