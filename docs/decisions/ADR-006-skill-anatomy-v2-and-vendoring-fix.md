# ADR-006: HF skill anatomy v2 — 引入 `skills/<name>/scripts/` 子目录约定（v0.5.1 vendoring fix）

- 状态：起草中（2026-05-09 锁定）
- 决策人：用户（架构师角色）
- 工程团队：HF（按 `docs/principles/soul.md` 协作契约执行）
- 关联文档：
  - `docs/decisions/ADR-005-release-scope-v0.5.0.md`（v0.5.0 引入 `scripts/render-closeout-html.py`，但物理位置放在仓库根 `scripts/`——这是本 ADR 修正的 vendoring 缺陷）
  - `docs/decisions/ADR-002-release-scope-v0.2.0.md`（D5 引入 `scripts/audit-skill-anatomy.py` 作为维护者跨 skill 工具的先例）
  - `skills/hf-finalize/SKILL.md` step 6A（v0.5.0 引入；本 ADR 让 step 6A 的 hard gate 工具与 skill 同 vendor）
  - `scripts/audit-skill-anatomy.py`（仓库根 `scripts/` 保留给跨 skill 维护者工具的代表）

## 背景

v0.5.0（ADR-005）给 `hf-finalize` 引入了 closeout HTML 工作总结报告 + 配套 stdlib-only 渲染脚本 `scripts/render-closeout-html.py`，并把它写成 step 6A 的 hard gate（每次 closeout 必须额外执行该脚本生成 `closeout.html`）。脚本的物理位置选在仓库根 `scripts/`，沿用了 v0.2.0 ADR-002 D5 引入 `scripts/audit-skill-anatomy.py` 的先例。

v0.5.0 GA 后立即发现这是一个 vendoring 缺陷。HF 三种官方集成路径在 vendoring 树里携带的目录范围不同：

| 集成路径 | 是否携带仓库根 `scripts/` | step 6A hard gate 是否能跑 |
|---|---|---|
| Claude Code 插件（marketplace install 整个 git repo） | ✅ | ✅ |
| OpenCode `.opencode/skills/` → `../skills/` 软链接 | ❌ | ❌ |
| Cursor `.cursor/rules/` + 复制 `skills/` | ⚠️ 视用户操作 | ⚠️ 半数情况断 |
| README / CONTRIBUTING.md 描述的 "vendor by copying `skills/`" | ❌ | ❌ |

也就是说 **3 种官方集成路径里有 2 种** hf-finalize 的 step 6A hard gate 跑不通——脚本不在 vendoring 树里。这不是审美问题，是真实功能性缺陷。

错判的根源：v0.4.0 / v0.5.0 把"维护者跨 skill 工具"（`audit-skill-anatomy.py`）与"用户工具"（`render-closeout-html.py`）放在同一个 `scripts/` 目录，混淆了**工具受众**这一关键边界：

- `audit-skill-anatomy.py`：受众是 HF 仓库自身的 contributor，用户侧不需要跑；放仓库根 `scripts/` 没问题（用户的 vendor 树本来就不需要它）
- `render-closeout-html.py`：受众是每一个用 hf-finalize 的项目，用户每次 closeout 都要跑；必须随 hf-finalize 一起 vendor

`hf-release` 在 v0.5.0 dogfood pre-release-checklist V6（项目级元数据同步）通过了，但当时只校验了"plugin.json / SECURITY.md / CHANGELOG 等版本号同步"，没有校验"用户工具是否在 vendoring 路径上"。这是 v0.4.0 / v0.5.0 工程上没看到的盲点。

本 ADR 一次性锁定 v0.5.1 patch release 范围的 4 项决策，把 HF skill anatomy 从 v0.2.0 起的 3 类子目录扩展为 4 类，物理迁移 hf-finalize 的脚本。

## 决策

### Decision 1 — HF skill anatomy 扩展为 4 类子目录；引入 `skills/<name>/scripts/`

HF skill anatomy 自 v0.2.0 起约定的 3 类子目录（`SKILL.md` + `references/` + `evals/`）在 v0.5.1 扩展为 **4 类**，新增 `skills/<name>/scripts/` 作为 **skill-owned 工具** 子目录：

- `SKILL.md`（必出）—— skill 行为契约
- `references/`（按需）—— 模板 / 参考材料
- `evals/`（按需）—— eval 用例
- `scripts/`（按需，**v0.5.1 新增**）—— **本 skill** 专属的工具型脚本（典型场景：被本 skill hard gate 调用且不被其它 skill 复用的 stdlib-only 渲染 / 校验 / 转换脚本）

仓库根 `scripts/` 目录的语义同步收紧为 **跨 skill 的维护者工具**：

- 仓库根 `scripts/`：维护者跨 skill 工具（典型：`audit-skill-anatomy.py` 审计所有 skill 的 anatomy 合规；`test_audit_skill_anatomy.py` 配套测试）。**用户侧不需要跑**
- `skills/<name>/scripts/`：单一 skill 的 hard gate 工具（典型：`skills/hf-finalize/scripts/render-closeout-html.py` 渲染 closeout HTML）。**用户每次跑该 skill 都要跑**

理由：

- **修复 vendoring 缺陷**：把 skill-owned 工具放仓库根 `scripts/` 会破坏 OpenCode / Cursor / "vendor by copying" 三条集成路径下的 hard gate 完整性。把约定锁住能避免后续 skill 重蹈覆辙
- **逻辑耦合反映物理位置**：`render-closeout-html.py` 由 hf-finalize step 6A **唯一调用**，**唯一**消费 hf-finalize 产出的 closeout pack；与 hf-finalize 是 1:1 强耦合。物理放一起反映逻辑放一起，符合 cohesion / locality 工程原则
- **维护者工具与用户工具按受众区分**：这是更稳定的语义边界——v0.4.0 / v0.5.0 没区分清楚是判断失误，本 ADR 修正之
- **不破坏 audit-skill-anatomy.py**：审计脚本只读 `<skill>/SKILL.md`、不遍历子目录；新加的 `skills/*/scripts/` 子目录对它完全透明；不需要给 audit 加白名单。仅在 audit 顶部 docstring 加文档段说明新约定（v0.5.1 已落地）
- **向前兼容**：v0.4.0 / v0.5.0 留下的"3 类子目录"布局仍然合法；本 ADR 只是**新增**一类，不淘汰任何旧约定。其它 23 个 skill 不需要立刻迁移（它们当前没有 skill-owned 工具）；按需后续单独 ADR 迁移

### Decision 2 — v0.5.1 物理迁移 `render-closeout-html.py` + `test_render_closeout_html.py`

把 v0.5.0 误放在仓库根 `scripts/` 的 hf-finalize 工具搬到 `skills/hf-finalize/scripts/`：

- `scripts/render-closeout-html.py` → `skills/hf-finalize/scripts/render-closeout-html.py`
- `scripts/test_render_closeout_html.py` → `skills/hf-finalize/scripts/test_render_closeout_html.py`

同步更新：

- `skills/hf-finalize/SKILL.md` step 6A / Hard Gates / Reference Guide / Verification 中的脚本路径全部改为新位置
- `skills/hf-finalize/references/finalize-closeout-pack-template.md` 中的 2 处脚本路径改为新位置
- 渲染脚本顶部 docstring 加 "Note on script location (since v0.5.0)" 段，解释为什么住在 skill 目录下
- `scripts/audit-skill-anatomy.py` 顶部 docstring 加段说明 4 类子目录约定（行为不变）
- `CHANGELOG.md` 加 [0.5.1] 段引用本 ADR
- 顶层文档（README / setup docs / SECURITY / CONTRIBUTING / cursor rules / marketplace.json）所有脚本路径引用同步为新位置
- v0.5.0 的 `examples/writeonce/features/001-walking-skeleton/closeout.html` 由新位置渲染器重新生成（HTML 仅 footer 1 行路径差异）

理由：

- skill 输出语义 / closeout pack schema / HTML 输出语义**完全不变**——只是脚本物理位置 + 调用路径文本同步
- v0.5.0 已落盘的 `closeout.md` / `closeout.html` 不需要修订；v0.5.0 已落盘的 v0.5.0 release pack（`features/release-v0.5.0/`）也不修订（已是 tagged 历史）
- 升级到 v0.5.1 的项目下次跑 hf-finalize 会自动用新路径；旧路径在迁移后立即失效（不保留 symlink，避免双源混乱）

### Decision 3 — v0.5.1 是 patch release，不是 minor

v0.5.1 是 **patch** bump（v0.5.0 → v0.5.1）。理由：

- 不引入新功能（HTML 伴生报告本身在 v0.5.0 已 GA）
- 不改 closeout.md schema、不改 closeout.html 输出语义
- 修复的是物理位置 / vendoring 链路的工程债务——典型 patch 范畴
- 仍勾 **pre-release** on GitHub Releases（与 v0.4.0 / v0.5.0 同向）
- `.claude-plugin/plugin.json` version `0.5.0` → `0.5.1`；其它顶层版本元数据按需同步（README Scope Note 仍写 v0.5.0 主线，加 v0.5.1 patch 注解；setup docs 顶部句子从 v0.5.0 → v0.5.1）

### Decision 4 — `hf-release` dogfood 第三次；不自动 git tag / 不部署 / 不做 ops

按 `hf-release` SKILL.md 起 v0.5.1 release pack：

- `features/release-v0.5.1/release-pack.md`（主 pack；Status: ready-for-tag）
- `features/release-v0.5.1/verification/release-regression.md`（D2 迁移后 release-wide regression）
- `features/release-v0.5.1/verification/release-traceability.md`（单 candidate trace）
- `features/release-v0.5.1/verification/pre-release-checklist.md`（V6 项现在能正确发现 skill-owned 工具迁移）

仍**不**自动执行 `git tag v0.5.1` / `git push --tags`；不部署；不做 ops——与 ADR-005 D9 / ADR-004 D7 立场一致。

## Tradeoffs（已考虑的备选 + 拒绝理由）

| 决策点 | 备选方案 | 拒绝理由 |
|---|---|---|
| D1 anatomy | 不动 anatomy；只加 vendoring 文档 patch（README / setup docs 提醒用户额外 vendor `scripts/`） | 把工程缺陷甩给文档；用户漏读就翻车；后续 skill 加 hard gate 工具会重蹈覆辙；治标不治本 |
| D1 anatomy | 引入 symlink：`scripts/render-closeout-html.py` 作为 symlink 指向 `skills/hf-finalize/scripts/render-closeout-html.py` | symlink 在 Windows 上行为不一致；增加维护面；双路径会让用户混淆"哪个是 canonical" |
| D2 路径 | 迁移到 `skills/hf-finalize/tools/` 或 `skills/hf-finalize/bin/` | `scripts/` 与仓库根 `scripts/` 保持同名，语义对齐（"工具型脚本"），最小化心理负担；`tools/` / `bin/` 没有 HF 约定先例 |
| D3 bump | minor（v0.6.0） | 不引入新功能；不破坏既有契约；patch bump 更诚实地反映"修工程债务"性质 |
| D3 bump | 不发版本号，留到 v0.6.0 一起带 | 把已知的 vendoring 漏洞拖一个 minor 周期会让所有早期用户长期卡在不可用状态；patch release 工程上更负责 |
| D4 release pack | 不再为 v0.5.1 起 release pack，复用 v0.5.0 的 | release pack 是 hf-release 对每个版本的契约工件；v0.5.1 是独立 release（即使是 patch），应当有独立 pack——也是 hf-release 第三次 dogfood 验证 patch release 流程的机会 |

## Consequences

正面：

- 修复 OpenCode / Cursor / vendor-by-copying 三条集成路径下 step 6A hard gate 的 vendoring 漏洞——v0.5.1+ 用户不再遇到"脚本找不到"的报错
- 锁住"工具受众"区分边界，未来加 skill-owned 工具有先例可循
- HF 仓库自身第三次 dogfood `hf-release`（前两次为 v0.4.0 / v0.5.0），验证 patch release 流程
- 顶部 docstring 把"为什么住在这里"显式入档，未来维护 PR 难绕过

负面：

- v0.5.0 用户升级到 v0.5.1 后，本地脚本路径有变化——任何 hardcode 了 `scripts/render-closeout-html.py` 的项目级 CI / 别名 / 文档需同步更新（CHANGELOG [0.5.1] migration 段会显式说明）
- v0.5.0 `examples/writeonce/features/001-walking-skeleton/closeout.html` 的 footer 行被改写（脚本路径文本变化），属于已 release 制品的 in-place 修订；按 ADR-005 D8 立场（不刷新 demo 事实层）这只是 HTML 渲染产物刷新，不是 demo 事实层修订，可以接受

## Implementation R1

R1（已完成 / 本 ADR 一并 commit）：

- `scripts/render-closeout-html.py` + `scripts/test_render_closeout_html.py` 物理迁移到 `skills/hf-finalize/scripts/` ✓
- 渲染脚本顶部 docstring 加 "Note on script location" 段 ✓
- `skills/hf-finalize/SKILL.md` + `references/finalize-closeout-pack-template.md` 中所有脚本路径同步 ✓
- `scripts/audit-skill-anatomy.py` 顶部 docstring 加段说明 4 类子目录约定 ✓
- `CHANGELOG.md` [0.5.1] 段 + 版本链接 ✓
- `.claude-plugin/plugin.json` version `0.5.0` → `0.5.1` ✓
- 顶层文档版本号 / 脚本路径同步 ✓
- `features/release-v0.5.1/` release pack + 3 份 verification ✓
- v0.5.0 walking-skeleton closeout.html 由新位置渲染器重新生成 ✓

## Notes

- 本 ADR 是 HF 自身的**首个 patch release ADR**（前 5 个 ADR 都是 minor release scope 决策）。颗粒度上比 ADR-001/002/003/004/005 都小，证明 ADR 模板对 patch 范畴也适用
- 本 ADR 不动 v0.5.0 已 tagged 的工件（`docs/decisions/ADR-005-release-scope-v0.5.0.md` 仍是 9 项决策；`features/release-v0.5.0/` 仍是 v0.5.0 状态）；v0.5.1 引入的 D1 在 ADR-005 起草时确实想过（见 ADR-005 起草过程的设计讨论），但当时没识别出 vendoring 影响。本 ADR 是后置补救
- `examples/writeonce/features/001-walking-skeleton/closeout.html` 的重新渲染是脚本搬位的副作用，不是 demo 事实层修订（与 ADR-005 D8 / ADR-003 D10 / ADR-004 D9 demo-不刷新立场一致——renders 是产物不是事实）
- 后续如果其它 skill 也引入 hard gate 工具（typically: hf-traceability-review 想要可视化跨 feature 链路图、hf-browser-testing 想要本地化的截图比对脚本），按 D1 约定走 `skills/<name>/scripts/`；HF skill anatomy 不需要再扩
