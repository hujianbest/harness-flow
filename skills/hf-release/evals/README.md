# hf-release 评测

## Protected Behavior Contracts

这些评测保护 `hf-release` 的以下行为契约：

1. **候选 feature 必须为 `workflow-closeout`**：`task-closeout` / `blocked` 不应入版
2. **release-wide regression 不可降级**：不允许把单 feature 历史 regression 拼贴当 release-wide 通过；缺测试入口时不替用户拍板降低门禁
3. **scope = ADR + candidates 一致性**：scope ADR 与候选清单不一致时必须抛回用户
4. **不写回 router**：本 skill 与 router 解耦；Next Action 不允许是 `hf-workflow-router`
5. **不自动执行 git tag / git push --tags**：tag 操作交项目维护者
6. **不混入 ops 动作**：feature flag / staged rollout / 监控 / 回滚不在本 skill 范围；在 release pack 中标记或承诺这些 = 越权
7. **不假设 HF 提供了部署/上线 skill**：out-of-scope 能力（部署 / staged rollout / 监控 / 回滚）应说"由项目自身 ops 流程承担"，不能编造或假设另一个现成 HF skill 接手
8. **Final Confirmation interactive**：interactive 模式下未确认前不得把 ADR 翻 accepted、不得写 `Next Action: null`

## 文件结构

- `README.md`：本文件
- `evals.json`：测试用例定义
- `fixtures/`：模拟输入工件片段（按需添加）

## 评测策略

每个用例提供 project snapshot（候选 feature closeout 状态 / regression 入口存在性 / 用户口径），让 agent 作为 `hf-release` 决定下一步。expected output 描述应当怎么处理；expectations 列出可观察的断言点。

后续若需要扩展，应覆盖：

- candidate 集合中混入 `task-closeout` 的负例（应拒入）
- regression 失败的负例（应抛回用户，不 mock 通过）
- 用户口径含 ops 动作的负例（应明确告知"不在本 skill 范围"）
- Final Confirmation 未通过时 ADR 状态翻转的负例（应保持 proposed）
- 用户在 OpenCode/Cursor 中通过 NL 触发的正例（不依赖 router）

## 与 audit 的关系

- `scripts/audit-skill-anatomy.py` 检查 SKILL.md 结构合规（advisory）
- 本 evals 目录检查 runtime 行为契约
- 二者不替代、互补：audit 抓写法漂移，evals 抓行为漂移

## v0.4.0 baseline

v0.4.0 引入时仅含 4 条 baseline 用例（见 `evals.json`），覆盖最高优先级行为：

1. 拒绝把 `task-closeout` 当候选
2. 拒绝降级 release-wide regression
3. 不写回 router
4. 不自动 git tag

后续真实使用反馈出现新失败模式时再扩 evals。
