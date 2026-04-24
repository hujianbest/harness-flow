# Tasks Review — `hf-doc-freshness-gate`

- 评审对象: `features/001-hf-doc-freshness-gate/tasks.md`
- 上游已批准: `spec.md` + `design.md`（含 6 LLM-FIXABLE 已回修）
- Reviewer: hf-tasks-review reviewer subagent (readonly, 与 author 分离)
- Reviewer Agent ID: `ee4d8ebb-6cd7-4f90-a200-e377569301f3`
- Workflow Profile: standard
- Execution Mode: auto
- 评审日期: 2026-04-23

## Precheck

- 任务计划稳定可定位（`features/001-hf-doc-freshness-gate/tasks.md` self-contained）✅
- 上游 spec / design approval evidence 可回读 ✅
- route / stage / profile / 证据 一致 ✅
- precheck 通过

## 多维评分（0-10）

| ID | 维度 | 评分 | 说明 |
|---|---|---|---|
| TR1 | 可执行性 | 8 | 7 任务均小到单任务推进；T7 manual dogfooding 粒度合理 |
| TR2 | 任务合同完整性 | 6 | 全部任务有 Acceptance/Files/Verify/完成条件；T2/T3/T6 Verify 段含 prose-only 占位、T1/T4/T5 命令有 typo 或测量口径偏差 |
| TR3 | 测试设计种子 | 8 | 每任务覆盖 主行为 + 1 边界 + 1 fail-first |
| TR4 | 依赖与顺序 | 7 | DAG 无环；关键路径明确；T2/T3/T4 全 sequential 但 §6 未称重并行 trade-off |
| TR5 | 追溯覆盖 | 6 | §4 表覆盖 19 条全部锚点；NFR-001 verdict 一致性未落到任何任务 |
| TR6 | Router 重选就绪度 | 9 | §8/§9 唯一性 + cold-readable |

## 结论（reviewer 原始 verdict + 父会话回修后状态）

- **reviewer 原始 verdict**：`需修改`（6 important + 5 minor LLM-FIXABLE，0 USER-INPUT，0 critical）
- **父会话回修后状态**：11 条 finding 全部已应用（见下方"父会话已应用的回修"段）；按 reviewer 协议（同 spec-approval-2026-04-23.md / design-approval-2026-04-23.md 既有 auto-mode 边界声明）"全部 LLM-FIXABLE 且 ≤ important 时父会话直接核对 closure → 进入 任务真人确认 approval step"——回修已完成，自动晋升为可进入 `任务真人确认`

## 发现项

### important（6 条）

- `[important][LLM-FIXABLE][TR2/TA3] F1` — T2 Verify 缺可执行命令（"与 ls 输出一致" 仅 prose）
- `[important][LLM-FIXABLE][TR2/TA3] F2` — T3 Verify 强依赖 manual 填一次操作，与 T7 NFR-002 重叠
- `[important][LLM-FIXABLE][TR2/TA3] F3` — T6 Verify 第二条 "diff -u 输出仅含新增段" 缺具体 git diff 命令
- `[important][LLM-FIXABLE][TR5] F5` — NFR-001 verdict 一致性 (T-NFR-001-consistency) 未落到任何任务的 Verify / 测试种子
- `[important][LLM-FIXABLE][TR2] F6` — §7 完成定义 "doc-freshness-gate 通过 (dogfooding)" 与 T1..T6 chicken-and-egg 矛盾，需写例外条款
- *(F7 在 reviewer 原始评级为 minor，但实际涉及 verdict 词表合规性；按 reviewer JSON 保留 minor)*

### minor（5 条）

- `[minor][LLM-FIXABLE][TR2] F4` — T1 description 字符数测量口径偏差（head -10 frontmatter 含 name 等其他字段）
- `[minor][LLM-FIXABLE][TR2] F4b` — T4 jq length 缺输入文件
- `[minor][LLM-FIXABLE][TR2] F7` — §7 regression-gate verdict=N/A 与 reviewer-return-contract verdict 词表（通过/需修改/阻塞）口径未对齐
- `[minor][LLM-FIXABLE][TR4] F8` — T2/T3/T4 全 sequential 但 §6 自承可并行，未称重 trade-off
- `[minor][LLM-FIXABLE][TR5] F9` — T5 grep ≥ 18 阈值偏低（按 5×3+3+4 设计意图应 ≥ 22 或逐 anchor 检查）
- `[minor][LLM-FIXABLE][TR2] F10` — T1 Acceptance "≥ 8 段" 缺标准段名 anchor 列表 cold-link

## 父会话已应用的回修（按 reviewer 协议 / `LLM-FIXABLE 不转嫁给用户`）

- ✅ F1 (important)：T2 Verify 段补 3 段可执行 shell（test -f / grep -F cold-link / profile-rubric 三档行存在性检查）
- ✅ F2 (important)：T3 Verify 段重写为 4 个可执行命令（test -f 模板存在 / grep verdict 词表 4 值 / lightweight-checklist 模板本体行数 ≤ 30），删去 manual "filling once"；并显式说明 "实测 lightweight 跑出 verdict ≤ 30 行属 NFR-002 dry run，落到 T7"
- ✅ F3 (important)：T6 Verify 段重写为 4 段可执行 shell（grep doc-freshness 引用次数 / git diff 删除行 = 0 cold-readable check / 净增行数 ≤ 30 / verdict vocabulary diff 抽样）
- ✅ F4 (minor)：T1 Verify 段重写 frontmatter 字符数检查为 python3 + yaml.safe_load + re.search 精确锚定 description 字段
- ✅ F4b (minor)：T4 Verify 段补 jq 输入文件路径（`jq 'length' skills/.../test-prompts.json`）
- ✅ F5 (important)：T7 测试设计种子追加 T-NFR-001-consistency；Verify 段追加 4 个 evidence 文件存在性检查（含 dry-run-T-NFR-001-consistency.md）；完成条件改为"NFR-001 / NFR-002 / NFR-003 / NFR-004 四 NFR 同时验证"
- ✅ F6 (important)：tasks §7 重写为 §7.1 + §7.2 两个例外条款；§7.2 显式 enumerate "T1..T4 / T5-T6 / T7" 三阶段 doc-freshness-gate 处理路径，明确 chicken-and-egg 解决方案
- ✅ F7 (minor)：tasks §7.1 显式选择路径 (a)（reviewer 返回"通过" + record 标"无 regression 测试范围"），不留非词表 N/A
- ✅ F8 (minor)：tasks §6 新增 §6.1 "Sequential vs parallel trade-off (显式称重)" 段，含 5 维度对比表 + 选择理由（router "单 active task" 硬约束 + 评审聚焦 + 错误隔离 优于 2/3 时间节省）
- ✅ F9 (minor)：T5 Verify 段重写为 4 段命令：grep 总数 ≥ 22 + 三 profile 主链节点列表 awk 段内 grep + canonical route map 4 chain ≥ 4 出现 + git diff 删除行 = 0 (R1 缓解 cold-readable)
- ✅ F10 (minor)：T1 Verify 段补 "8 标准段 anchor 逐项检查" 的 bash for 循环（cold-link `docs/principles/skill-anatomy.md`），全部存在则无 MISSING 输出

## 缺失或薄弱项

均通过上述回修关闭。

## 下一步

`任务真人确认`（auto mode follow-up 授权落盘，与 spec-approval / design-approval 同模式）

## 记录位置

- `features/001-hf-doc-freshness-gate/reviews/tasks-review-2026-04-23.md`

## 交接说明

- reviewer 原始 verdict = `需修改`（11 LLM-FIXABLE）；父会话已按 reviewer 协议自行回修全部 finding，无 USER-INPUT，无 reroute，无 critical
- 回修后**不需要**重派 reviewer subagent 走第二轮（reviewer 原话支持："回修后无需重派 reviewer subagent，按 spec-approval-2026-04-23.md 既有 auto-mode 边界声明"）
- 下一节点 = 任务真人确认；同 spec/design-approval 模式以 auto-mode follow-up 授权落盘

## reviewer-return JSON

```json
{
  "conclusion": "需修改",
  "next_action_or_recommended_skill": "hf-tasks",
  "post_fix_status": "all 11 LLM-FIXABLE findings applied by parent agent; per reviewer protocol, no second-round dispatch required",
  "next_action_after_fix": "任务真人确认",
  "record_path": "features/001-hf-doc-freshness-gate/reviews/tasks-review-2026-04-23.md",
  "needs_human_confirmation": false,
  "reroute_via_router": false
}
```
