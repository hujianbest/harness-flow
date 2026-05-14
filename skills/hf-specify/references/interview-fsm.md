# `hf-specify` Interview FSM (5-state)

> 启发自 OMO Prometheus interview state machine（`code-yeongyu/oh-my-openagent` `src/agents/prometheus/interview-mode.ts`）。把 spec 草稿过程显式状态化，会话被打断后可从 `spec.intake.md` 工件恢复"问到第几个澄清问题了"。

## 5 状态

| State | 含义 | 进入条件 | 退出条件 |
|---|---|---|---|
| **Interview** | 对架构师 / 用户提问，澄清需求 | 新 spec 任务起点；或 ClearanceCheck 判定需要更多澄清 | 收到答复 → Research（如需查证）或直接 ClearanceCheck（如无需查证）|
| **Research** | 读 spec / design / ADR / 代码库 / 外部 doc 收集证据，回答 Interview 提出的实现性问题 | Interview 收到含"待查证"性质的回答 | 收到足够 finding → ClearanceCheck |
| **ClearanceCheck** | 检查"是否还有未澄清项"——核心目标 / 范围 / 边界 / 关键决策 / 测试策略 5 项 boolean | Research 完成或 Interview 答复无需查证 | 全 clear → PlanGeneration；不全 clear → 回 Interview / Research（OQ-005 收口：允许回退）|
| **PlanGeneration** | 把累计 intake 翻译成 spec.md 草稿 | ClearanceCheck 全 clear | spec.md 落盘 → Done |
| **Done** | spec.md 草稿就绪，待 hf-spec-review | PlanGeneration 完成 | 不再回退；spec.md 提交 review 流程接管 |

## 状态机图

```
[*] ─────────────► Interview
                      │
                      │ (answer received)
                      ▼
                   Research
                      │
                      │ (findings collected)
                      ▼
                ClearanceCheck
                  │ │ │
       (unclear)  │ │ │ (more research needed)
                  │ │ └────────────► Research (loop)
                  │ │
                  │ └────────────────► Interview (loop, OQ-005 ✓)
                  │
                  │ (all clear)
                  ▼
              PlanGeneration
                    │
                    │ (spec.md written)
                    ▼
                  Done ──► [hf-spec-review]
```

## OQ-005 收口

- **允许 ClearanceCheck → Research 回退**（发现需要更多查证）
- **允许 ClearanceCheck → Interview 回退**（发现需要更多澄清）
- **禁止 PlanGeneration → 回退**（PlanGeneration 完成即冻结，等价于"草稿写完了"；如需返工，由 hf-spec-review verdict=`需修改` 触发新一轮 hf-specify session）
- **禁止 Done → 回退**（Done 等价于"提交 review"，回退由 review 节点决定）

## 与 OMO Prometheus 的差异

| OMO Prometheus | HF hf-specify FSM |
|---|---|
| 实现：runtime LLM agent（Claude / GPT）按 prompt 内 FSM 描述自驱 | 实现：纯 markdown FSM + spec.intake.md 工件持久化；agent 按本 reference 与 SKILL.md Workflow 步骤对照 |
| 持久化：`.sisyphus/notepads/{plan-name}/` 5 markdown | 持久化：`features/<f>/spec.intake.md` 单文件 + 既有 `notepads/` 5 文件复用 |
| 回退：Prometheus 自决 | 回退：本 FSM 显式列允许 / 禁止的转移 |
| Done：Prometheus 完成后由 Sisyphus 接管 | Done：hf-spec-review 节点接管 |

## 持久化协议

每个状态切换都必须更新 `features/<active>/spec.intake.md` 的 `Status` 字段 + 对应 trail 段（Question Trail / Research Trail / Clearance Checks）。schema 详见 `references/spec-intake-template.md`。

会话被打断后，下次 hf-specify session 进入时**先**读 `spec.intake.md`：
- 若 `Status == Done` → 跳过 FSM，直接进 hf-spec-review
- 否则按 `Status` 字段恢复到对应状态继续

## 与 hf-gap-analyzer 的协作

`hf-gap-analyzer` 在 PlanGeneration 完成（spec.md 写完）后、hf-spec-review 之前由作者主动调用做 author-side self-check。本 FSM 在 PlanGeneration → Done 之间允许 author 插入一次 gap-analyzer 调用（不算回退，算 self-check pass-through）。
