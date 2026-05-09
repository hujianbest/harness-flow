# Release Scope ADR Template

`hf-release` §3 起草 release scope ADR 时使用。仿 HF 自身 ADR-001/002/003 结构。

## 使用说明

- 默认保存路径：`docs/decisions/ADR-NNN-release-scope-vX.Y.Z.md`
- `NNN` 取项目下一个未占用的 ADR 编号（HF 仓库本身按 001 / 002 / 003 / 004 顺延，项目自定）
- ADR 起草时 `状态` 字段写 `起草中`；`hf-release` §11 Final Confirmation 通过后翻 `已锁定 / accepted`
- 项目若声明了等价 ADR 模板，优先遵循项目约定

## 模板正文

```markdown
# ADR-NNN: <项目名> vX.Y.Z 对外发布范围

- 状态：起草中（YYYY-MM-DD 锁定）
- 决策人：<架构师 / 维护者署名>
- 工程团队：<执行团队>
- 关联文档：
  - <上一版同类 ADR，如果有>
  - <被本版 release 引用的关键 ADR>
  - <项目 soul / principles 文档>
  - <本版 release pack 路径：features/release-vX.Y.Z/release-pack.md>

## 背景

<3–5 段。覆盖：
- 上一版 release（X.Y-1.Z 或 X.Y.Z-1）做了什么、留下了什么 deferred 项
- 本版要解决的真实工程缺口或用户反馈
- 本版工作面盘点（grep 实测：候选 feature 数 / closeout 状态 / regression 入口存在性 / 元数据现状）
- 为什么这次 release 不应该把所有 deferred 项一次清完——P-Honest 立场或项目约束>

本 ADR 一次性锁定 vX.Y.Z 对外发版的 N 项范围决策。

## 决策

### Decision 1 — <核心范围决策（如：本版引入哪些 feature）>

<明确写入哪些 feature-id，不写"等"，不写"包括但不限于">

理由：
- <为什么这些 feature 应该入版>
- <为什么没列入的不入版>
- <与上一版 ADR 的关系：延续 / 撤回 / 强化>

### Decision 2 — <边界声明（如：本版不做什么）>

<显式列出本版 **不做** 的事；越具体越好——避免读者误以为某项已被承诺>

理由：
- <为什么显式排除>
- <这些事在哪个 v0.X+ ADR / 哪个 deferred 节点上承担>

### Decision 3 — <pre-release 标记决策（默认沿用 SemVer + pre-release 立场）>

vX.Y.Z 在项目 release 渠道（GitHub Releases / npm dist-tag / 等）上 **勾选 / 不勾选** pre-release。

理由：
- <主链覆盖是否达 100%>
- <对外承诺面是否有质变>
- <用户场景是否已稳定>

### Decision 4 — <版本号 bump 决策（major / minor / patch）>

X.Y.Z 相对于上一版是 **major / minor / patch** bump。

理由：
- <breaking change 清单（含/不含）>
- <SemVer 2.0.0 决策表落点>

### Decision 5 — <是否引入 / 修改 / 移除 skill 集合（项目自身适用时）>

<HF 类项目专用；普通项目可省略>

### Decision N — <其他范围决策>

...

## Tradeoffs（已考虑的备选 + 拒绝理由）

| 决策点 | 备选方案 | 拒绝理由 |
|---|---|---|
| D1 范围 | <一次清完所有 deferred 项> | <为什么本版不这么做> |
| D2 边界 | <把上线 / ops 也写进本版承诺> | <为什么留给后续 ADR> |
| D3 pre-release | <直接 GA / 跨 v1.0> | <为什么仍保留 pre-release> |
| D4 版本号 | <bump 到不同段> | <为什么按当前段 bump> |
| ... | ... | ... |

## Consequences（影响）

正面：
- <用户层面收益>
- <工程层面收益>
- <承诺面层面收益>
- <与上一版的连续性>

负面：
- <仍未覆盖的缺口>
- <对发现性的影响>
- <对维护成本的影响>
- <已知遗留 known limitations>

## v0.X+ Roadmap（由本版显式延后）

| 条目 | 来源 | 状态 |
|---|---|---|
| <延后项 1> | <来自哪个 ADR / 哪条 decision> | <预计纳入哪个 future 版本> |
| <延后项 2> | ... | ... |
| ... | ... | ... |

## Implementation 计划（R1–RN）

- **R1（ADR）**：本文件起草并锁定。
- **R2（Skill / 实现）**：<本版引入的 skill / 代码改动总览>
- **R3（元数据 + 顶层文档同步）**：<README / setup docs / plugin 元数据 / SECURITY 等同步>
- **R4（CHANGELOG）**：CHANGELOG 切到 `[X.Y.Z]` 段，按 Added / Changed / Decided / Deferred / Notes N 段写完；`[Unreleased]` 重置；版本号链接表加 `[X.Y.Z]`。
- **R5（发版）**：tag `vX.Y.Z`、Release notes 引用本 ADR、是否勾 pre-release 按 D3。
- ... <其余按需>

## Notes

- <本 ADR 与前一版 ADR 的关系（首次 / 延续 / 撤回 / 校准）>
- <本版承诺面与不承诺面的清晰对照（防止读者误读）>
- <forward reference 的状态标注（如本 ADR 引用未来 ADR / 未来版本时，明示其状态）>
```

## 编写约束

- **决策粒度**：每条 Decision 只锁定一件事；不要把"引入新 skill" + "扩展客户端面" 写进同一条。
- **拒绝叠词**：避免"包括但不限于" / "等" / "诸如此类"；范围必须可枚举。
- **forward reference 真实性**：引用尚未交付的能力或项目自身后续工作时必须明示其状态（草稿 / 已批准 / 待规划 / 等），不能写成"另一个现成能力"。
- **D11 风格校准**（可选）：如果起草过程中决策被推翻，新增一条 `D-final` 校准段而不是直接改前面的 Decision；保留撤回痕迹给读者。
- **Tradeoffs 必填**：至少 1 行；表明本版是经过权衡的，不是只有一种走法。
- **Roadmap 必填**：本版显式延后的项目要写清，给后续 ADR 留落点。

## 与 HF 自身 ADR-001/002/003 的差异

HF 自身 ADR 是 release scope ADR 的一个具体实例（HF v0.1.0 / v0.2.0 / v0.3.0 自己的发版决策）。本模板是**给所有 HF 用户**起草项目自身 release scope ADR 用的，因此：

- 决策面允许超出"skill / 客户端 / personas"这种 HF-specific 范围
- 不必引用 `docs/principles/soul.md`（那是 HF 自家宪法层）
- "工作面盘点"建议保留——它是 ADR-001/002/003 共同的高质量实践，逼起草者用 grep 实测代替猜测

如果你的项目不熟悉 ADR 风格，可先读 `docs/decisions/ADR-003-release-scope-v0.3.0.md` 作为完整范例。
