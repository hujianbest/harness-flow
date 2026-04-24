# ADR-0001: 采用轻量 ADR 记录关键架构决策

accepted（hf-finalize closeout @ 2026-04-23 同步翻转 from `proposed` → `accepted`；上游 design-review 通过 + 设计真人确认 完成）

## 背景

`docs/principles/sdd-artifact-layout.md` 档 0 把 `docs/adr/` 列为不可省的长期资产。HarnessFlow 仓库直到 feature 001-hf-doc-freshness-gate 进入 hf-design 阶段时才首次有"会影响后续任务规划的关键决策"需要被独立记录（pack 之前的演进偏向 prose 原则文档而非显式 ADR）。本文是 HF 仓库的第一个 ADR，承担"启用 ADR pool"的元决策。

## 决策

采用 Michael Nygard 经典 ADR 格式（含状态 / 背景 / 决策 / 备选方案 / 后果 / 可逆性）记录所有"会影响后续 hf-tasks 规划"的架构决策；ADR 落到 `docs/adr/NNNN-<slug>.md`，4 位顺序号、仓库级唯一、永不复用。`features/<NNN>/design.md` 通过 ADR ID 引用，不内联 ADR 全文。新建 ADR 状态写 `proposed`；`hf-design-review` 通过且 `设计真人确认` 完成后翻为 `accepted`，由 `hf-finalize` 在 closeout 阶段同步状态翻转。

## 被考虑的备选方案

- **不显式启用 ADR pool，把所有决策内联在 `design.md`**：被否决，违反 `sdd-artifact-layout.md` 档 0 hard requirement，且 `design.md` 在 closeout 后基本不动，新 feature 无法跨周期引用历史决策。
- **延后到下一 feature 再启用**：被否决，本 feature design 阶段已经产生 3 条结构性决策，延后只会让 ADR-0001 与 ADR-0002+ 在同一时间被仓促创建，破坏档 0 的"启用即生效"语义。

## 后果

- 正面：HF 自身合规 sdd-artifact-layout 档 0；后续 feature 跨周期决策追溯有稳定锚点；`hf-finalize` 的"必须同步项"中"ADR 状态翻转"流程在 hf-doc-freshness-gate workflow closeout 时第一次跑通，验证既有合同。
- 负面：ADR 维护需要纪律，需在每次 design 阶段判断"是否够格成为 ADR"。
- 中性：`design.md` 通过 ID 引用 ADR，cold reader 需多翻一份文件才能看到决策全文。

## 可逆性评估

容易回滚 — 决策本身只引入一个目录与命名约定，未来若改用其他决策记录工具（如 Architecture Haiku），可批量迁移。
