# ADR-005: HarnessFlow v0.5.0 引入 closeout HTML 工作总结报告（hf-finalize 视觉伴生）

- 状态：起草中（2026-05-09 锁定）
- 决策人：用户（架构师角色）
- 工程团队：HF（按 `docs/principles/soul.md` 协作契约执行）
- 关联文档：
  - `docs/decisions/ADR-001-release-scope-v0.1.0.md`（Pillar C "P-Honest，窄而硬" 立场）
  - `docs/decisions/ADR-002-release-scope-v0.2.0.md`（D11 校准 / 撤回 R3/R4/R5 立场延续）
  - `docs/decisions/ADR-003-release-scope-v0.3.0.md`（D2 显式延后 6 项 ops/release skill；D4 主链终点保持 `hf-finalize`）
  - `docs/decisions/ADR-004-hf-release-skill.md`（D1 引入 `hf-release` standalone skill；D2 与 `hf-shipping-and-launch` 正交不替代；D9 不刷新 writeonce demo）
  - `skills/hf-finalize/SKILL.md`（本版**唯一** skill 修订对象——新增 step 6A "产出 closeout HTML 工作总结报告"）
  - `skills/hf-finalize/references/finalize-closeout-pack-template.md`（追加 HTML Companion Report 段）
  - `scripts/render-closeout-html.py`（本版**唯一**新增脚本——把 closeout pack 渲染为视觉伴生 HTML）
  - `features/release-v0.5.0/release-pack.md`（本版 release pack）

## 背景

v0.4.0（ADR-004）以 "首个 release-tier 独立 skill" 节奏新增 `hf-release`，把 23 → 24 `hf-*`，slash 命令 6 → 7。v0.4.0 GA 之后，HF 自身的 dogfood 节奏与用户反馈集中在一类**单 feature closeout 评审体验**问题：

> （2026-05-09 用户反馈原话）"我希望 hf-finalize 的 closeout 能有一份 html 工作总结报告。能直观的表达这次工作流的报告，要包含代码测试覆盖率等信息，比 markdown 格式更可读和直观。"

把这句话拆成 3 个工程动作：

1. `hf-finalize` 落盘的 `closeout.md` 是 canonical 机器可读契约（schema 由 `references/finalize-closeout-pack-template.md` 锁定），但对**人类 reviewer / 干系人**而言信息密度高、对比关系散落、可读性弱
2. 工程交付物的 reviewer 期望的是 RFC / postmortem 风格的视觉报告：closeout 类型 / conclusion 一眼可读、HF 主链节点可视化轨迹、tests + coverage 量化呈现、evidence matrix 可搜索可排序
3. 现有 `closeout.md` 已包含 ①③ 所需的全部事实——所需的不是新的"事实采集"，而是一层**视觉渲染**

`hf-finalize` 当前只输出 `closeout.md` + 状态字段同步；不输出任何视觉化制品。`hf-release` 的 v0.4.0 范围（ADR-004 D1 / D2 / D5）显式停在"工程级 release 切片"层，**不**承担单 feature 的视觉化呈现。本 ADR 在 ① 不引入新 skill、② 不动主链 FSM、③ 不动 router transition map 的前提下，给 `hf-finalize` 加一份必出的视觉伴生制品 + 配套的 stdlib-only 渲染脚本。

本版本工作面规模与 v0.3.0 patch 量级相当——1 个新增 Python 脚本（< 800 行）+ 1 处 SKILL.md 工作流补丁（新增 step 6A）+ 1 处模板文件追加段 + 配套版本号 / 文档同步。

本 ADR 一次性锁定 v0.5.0 范围的 9 项决策。

## 决策

### Decision 1 — `hf-finalize` 新增"closeout HTML 工作总结报告"必出制品

`hf-finalize` 的 workflow 在 step 6（产出 closeout pack）之后**必须**额外执行 step 6A：调用 `scripts/render-closeout-html.py <feature-dir>` 渲染 `features/<active>/closeout.html`，作为 `closeout.md` 的视觉伴生制品。Hard Gates / Verification / Output Contract / Red Flags 同步加入这一条。

理由：

- 满足 v0.4.0 GA 后用户反馈中的最高频缺口（视觉化 closeout 评审体验）
- HTML 报告与 `closeout.md` 是**渲染关系**而非平行事实——渲染脚本读 closeout.md + 已落盘 evidence/*.log + verification/*.md（+ 可选 `verification/coverage.json`），不允许在 HTML 中加入 `closeout.md` 之外的 conclusion / 测试数据 / 覆盖率（"sync-on-presence + 不引入新事实" 立场）
- 工件目录结构不变（HTML 与 MD 同目录），不破坏既有 router / hf-release 对 `features/<active>/` 路径假设
- 缺覆盖率数据时 HTML 显式渲染"未提供"，**不阻塞** closeout（与 `hf-doc-freshness-gate` 的 sync-on-presence 立场同向）

### Decision 2 — 渲染脚本以 `scripts/render-closeout-html.py` 落地，仅依赖 Python stdlib

新增 `scripts/render-closeout-html.py`：

- **零外部依赖**：仅用 Python 3 stdlib（`re` / `argparse` / `dataclasses` / `html` / `json` / `pathlib`）。与 `scripts/audit-skill-anatomy.py` 同款约束，任何已能跑 audit 的环境都能跑这个脚本
- **自包含输出**：单文件 HTML，嵌入式 CSS / 极小 vanilla JS / 离线可读 / 无 CDN / 暗亮主题 / 可打印
- **解析协议内联**：不引入 Markdown 解析依赖；用正则识别 closeout pack schema 的 H2 段（`Closeout Summary` / `Evidence Matrix` / `State Sync` / `Release / Docs Sync` / `Handoff`）+ 表格 / bullet 双形态 evidence rows
- **配套测试**：`scripts/test_render_closeout_html.py` 17 个单元测试覆盖 markdown 解析两种形态 / vitest+jest+pytest 日志 / coverage.json + 内联 KV / 完整与 blocked 渲染 / sub-bullet 不溢出到 sibling section / Status Fields Synced 子项渲染 / HTML 转义 / CLI exit code

理由：

- 与 v0.4.0 已建立的 "纯 Python stdlib 工具型脚本" 路径（`audit-skill-anatomy.py`）一致，最小化新增维护面
- 单文件 HTML + 嵌入式 CSS 满足"可打印 / 可邮件转发 / 可作为 PR 附件 / 可归档"的 reviewer 现实使用场景
- 不引入 Node.js / SSG / Markdown 渲染库等任何前端工具链，避免把 HF 仓库变成"半个前端项目"

### Decision 3 — 视觉系统按 `hf-ui-design` 方法论自检设计，反 AI slop 立场显式入档

视觉系统不走"AI 默认审美"。具体落地：

- 在脚本顶部 docstring 段写出 **"System Manifesto" (vocalize the system, hf-ui-design § 6.5)**，固化本报告的设计语汇（风格定位 / layout / color / typography / 节奏锚点 / 全局约束 / a11y / print），让未来维护者不退回 SaaS dashboard 默认审美
- 显式按 `skills/hf-ui-design/references/anti-slop-checklist.md` 第 1-3 节 8 条（S1 渐变 / S2 左竖线 callout / S3 默认字体 / S4 默认蓝/紫 / S5 装饰 SVG + emoji / S6 千篇一律 dashboard / S7 glassmorphism / S8 浮起卡片）逐条规避或显式辩护，记入脚本 docstring 的"Anti-slop checks consumed"段
- WCAG 2.2 AA 对比度 + `:focus-visible` 焦点可见 + `prefers-reduced-motion` + `prefers-color-scheme` 暗亮主题 + 打印样式（隐藏 toolbar、展开折叠行）

理由：

- HTML 报告是 HF 自身**第一次**对外的 reviewer-facing 视觉产物（hf-finalize 之前只输出纯文本 / 纯 Markdown）。视觉决策一旦上线就难以回退，必须按 `hf-ui-design` 方法论而不是凭脚本作者审美直觉
- 反 AI slop 立场显式入档，避免后续维护 PR 通过"小调整""加点视觉吸引力"渐进侵入默认 SaaS 审美

### Decision 4 — `hf-finalize` 是本版**唯一**修订的 skill；不动其它 23 个 skill

v0.5.0 仅对 `skills/hf-finalize/SKILL.md` 加 step 6A + Hard Gates / Verification / Red Flags / Reference Guide 一行；对 `skills/hf-finalize/references/finalize-closeout-pack-template.md` 追加"HTML Companion Report"段。其余 23 个 skill（含 v0.4.0 新引入的 `hf-release`）在本版**不**做内容修订。

理由：

- 本 ADR 范围是"给 closeout 增加视觉伴生制品"，是 `hf-finalize` 的**输出契约**新增一条；不涉及上游 spec / design / tasks / TDD / reviews / gates 的契约变化
- v0.4.0 ADR-004 已显式声明 23 → 24 不替代既有；本版同向，24 → 24 不变
- 不在 `hf-release` 的 §8 pre-release engineering checklist 里加"必须有 closeout.html"——`hf-release` 是 read-only 消费 closeout 制品，对单 feature 制品集的 schema 由 `hf-finalize` 决定（`hf-release` 不应反向约束 `hf-finalize` 的输出）

### Decision 5 — 不引入新 skill、不动主链 FSM、不动 router transition map、不动 entry shell bias 表

v0.5.0 skill 集合规模**不变**：仍是 24 `hf-*` + `using-hf-workflow`。Slash 命令面**不变**：仍是 7 条（`/spec` / `/plan` / `/build` / `/review` / `/ship` / `/closeout` / `/release`）。客户端面**不变**：仍是 Claude Code + OpenCode + Cursor 3 家。

理由：

- 用户反馈是 "hf-finalize 加 HTML 伴生报告"——颗粒度是"已存在 skill 的输出契约扩展"，不是"新工作流节点"
- 加 `hf-html-report` 之类的独立 skill 会引入"何时调用""谁是上游""是否进 router""与 hf-finalize 关系"等不必要的契约决策；step 6A 直接绑死在 `hf-finalize` 内反而最简洁
- entry shell `using-hf-workflow` § 5 entry bias 表不动——HTML 报告不是用户直接表达的意图，是 closeout 的副产品

### Decision 6 — 版本号按 SemVer minor bump 到 v0.5.0；继续标 pre-release

v0.5.0 相对 v0.4.0 是 **minor** bump。理由：

- 含 backward-compatible 新功能（HTML 伴生报告 + 新脚本）
- **不**含 breaking change：
  - `closeout.md` schema 不变；旧 closeout pack 仍可被 `hf-release` 正常消费
  - 旧 feature 目录（含已 close 的 walking-skeleton）补跑 `render-closeout-html.py` 即可生成 HTML，不需要修订任何已落盘工件
  - hf-finalize 加 step 6A 是 hard gate 的**严化**而非 schema 变化；旧仓库升级到 v0.5.0 后下次执行 hf-finalize 才会触发新 gate，对历史 closeout 不追溯
- 仍勾 **pre-release**：主链覆盖未达 100%（5 项原 deferred ops/release skill 仍延后；ADR-004 D2 立场不变）；客户端面无质变（仍 3 家）；与 ADR-001 D6 / ADR-002 D6 / ADR-003 D5 / ADR-004 D8 同向

### Decision 7 — 5 项原 deferred ops/release skill 继续延后，roadmap 标签从 "v0.5+" 漂移到 "v0.6+"

v0.5.0 **不**引入 `hf-shipping-and-launch` / `hf-ci-cd-and-automation` / `hf-security-hardening` / `hf-performance-gate` / `hf-deprecation-and-migration` / `hf-debugging-and-error-recovery` 中的任何一项（注意：v0.4.0 文档将这 6 项写为 "deferred to v0.5+"——v0.4.0 实际新增的 `hf-release` 不属于这 6 项）。

本版的"v0.5.0 漂移到 v0.6+"是 **诚实承认 roadmap 演化**：v0.4.0 ADR-004 D9 与 GA 后用户反馈 prioritize 了"hf-finalize 视觉化 reviewer 体验"而非"开始 ops 切面"，所以这 5 项继续延后。

理由：

- 与 ADR-001 D1 / ADR-002 D1 / ADR-003 D2 / ADR-004 D2 "P-Honest，窄而硬" 立场一致：**不**承诺没做的事，宁可推迟 roadmap 也不在 release notes 里塞空头支票
- 5 项 ops/release skill 的设计上限是"上线时刻"切面（feature flag / staged rollout / 监控 / 回滚 / SLO / 安全 headers / 性能基线 / debug-error-recovery / deprecation 流），与 v0.5.0 的"reviewer 体验改进"不在同一象限，不应该被本版强行打包

### Decision 8 — 不刷新 `examples/writeonce/` demo evidence trail；用 walking-skeleton 现有 closeout 验证渲染脚本

walking-skeleton 现有 `closeout.md` 已是 v0.1.0 demo 唯一 feature；本版**不**对 demo 做事实层修订（与 ADR-003 D10 / ADR-004 D9 同向），仅**新增** `examples/writeonce/features/001-walking-skeleton/closeout.html` 作为渲染脚本对真实 closeout pack 的"reference 实现样例"。

理由：

- demo 的 walking-skeleton closeout 是 v0.1.0 范围一次性产出的真实工件；不应该被 v0.5.0 release 反向修订
- 新增的 `closeout.html` 是渲染产物，对 demo 的事实层零侵入
- 渲染脚本针对 walking-skeleton 真实 closeout pack 跑通 = 脚本对真实场景可用的**最小可信证明**

### Decision 9 — 不自动执行 `git tag`；不部署；不做上线侧动作

v0.5.0 release 严格停在工程级 closeout：本 ADR 与本版 release pack 显式声明**不做**：

- `git tag v0.5.0` / `git push --tags`（由项目维护者按 `hf-release` D7 + 本 ADR 立场手工执行）
- 部署 / staged rollout / 监控仪表盘 / SLO 配置 / 回滚 procedure / health check / CDN / DNS / SSL 配置 / 上线后观察窗口
- WriteOnce demo 真实集成 Medium / Zhihu / WeChat MP（仍按 ADR-001 D9 / writeonce ADR-0003 立场，HTTP 走 RecordingHttpClient）

理由：

- 与 ADR-001 D1 / ADR-002 D1 / ADR-003 D2 / ADR-004 D2 / D9 完全一致；`hf-release` 范围内不动 ops 立场不变
- 项目自身的发布流程 = `hf-release` 跑完后由维护者执行 `git tag`，与 v0.4.0 一致

## Tradeoffs（已考虑的备选 + 拒绝理由）

| 决策点 | 备选方案 | 拒绝理由 |
|---|---|---|
| D1 输出契约 | HTML 不必出，作为可选脚本（用户想看再跑） | 可选制品在多 reviewer / 多 PR 流转中容易"忘了渲染"；hard gate 才能保证每个 closeout 都自带视觉伴生 |
| D1 渲染时机 | 由 `hf-release` 在版本切片时一次性渲染所有候选 feature 的 HTML | 把单 feature 制品的责任错放在 release-tier skill；违反 ADR-004 D5 standalone 立场（hf-release 不应反向修改 hf-finalize 输出） |
| D2 实现栈 | Node.js + Markdown 解析库 + 静态站点生成器 | 把 HF 仓库变成"半个前端项目"；与 v0.4.0 已建立的"纯 Python stdlib 脚本工具链"路径冲突；新增 `node_modules` 维护面 |
| D2 输出形态 | 多文件 HTML（CSS / JS / assets 分离） | reviewer 现实场景需要单文件可邮件转发 / 可作为 PR 附件 / 可归档；多文件分发摩擦大 |
| D3 视觉系统 | 直接套 Bootstrap / shadcn / Tailwind 默认主题 | 落入 anti-slop S3 / S4 / S6 / S8 默认审美；reviewer 一眼识别为"AI 默认产物"，损害专业感 |
| D3 视觉系统 | 不做 anti-slop 自检，靠脚本作者审美直觉 | 视觉决策一旦上线难以回退；不显式入档则后续维护 PR 难拒绝渐进侵入 |
| D4 修订面 | 同时修订 hf-completion-gate / hf-doc-freshness-gate 让它们也产 HTML 报告 | 这两个 gate 输出的是 verification 记录而非 closeout 总结；视觉化收益小，scope creep 大 |
| D5 skill 集合 | 加 `hf-html-report` 作为 hf-finalize 的下游 skill | 引入不必要的"何时调用""与 hf-finalize 关系"契约决策；step 6A 直接绑死最简洁 |
| D6 版本号 | 标 v0.4.1 patch | 引入新功能（HTML 伴生报告 + 新脚本）+ hard gate 严化，不是 backward-compatible bug fix；patch 不诚实 |
| D6 pre-release | 直接 GA / 跨 v1.0 | 主链覆盖仍未达 100%；客户端面无质变；不应跨 v1.0 |
| D7 deferred 标签 | 把 5 项 ops/release skill 中的 1-2 项纳入 v0.5.0 一并做 | scope creep 大；本版工作面已是"hf-finalize 视觉化 + release"，再叠 ops 切面会拖长发版周期 |
| D8 demo 刷新 | 重写 walking-skeleton 走一遍 v0.5.0 新工作流 | 与 ADR-003 D10 / ADR-004 D9 同向：demo 是 v0.1.0 范围一次性产出的真实工件，不应被 v0.5.0 反向修订；只新增渲染产物即可 |
| D9 ops | 把 `git tag v0.5.0 && git push --tags` 写进 release pack 的"已完成"段 | 违反 ADR-004 D7 + `hf-release` Hard Gate "不自动执行 git tag"立场；tag 由项目维护者手工触发 |

## Consequences（影响）

正面：

- **Reviewer 体验**：closeout 现在自带视觉伴生报告，PR / Slack / 邮件分享时不再需要 reviewer 自己 mentally render Markdown bullets；HF 主链节点可视化轨迹 + tests 量化呈现 + evidence matrix 可搜索可排序 → reviewer 决策成本下降
- **工程 hygiene**：渲染脚本是 HF 自己 dogfood 的"对外视觉化第一案"，为后续可能的 release pack 视觉化 / traceability 视觉化等扩展打底
- **Anti-slop 立场显式入档**：未来维护 PR 难绕过 anti-slop-checklist 自检，HF 自身的视觉决策有"可冷读的章程"
- **Backward compat**：旧 closeout pack 不需要任何修订；旧 feature 目录补跑脚本即可生成 HTML

负面：

- **Hard gate 严化**：升级到 v0.5.0 的 HF 仓库下次执行 `hf-finalize` 必须额外跑一次脚本；CI / 本地工作流加 1 步
- **覆盖率数据采集仍由项目自定**：脚本只**消费**已经在 `verification/coverage.json` 或日志里存在的覆盖率数据，是否采集由各项目自定。HF 自身**不**强制项目跑 `--coverage`（避免侵入项目测试入口）
- **roadmap 漂移**：5 项 ops/release skill 从 "deferred to v0.5+" 漂移到 "deferred to v0.6+"；与 v0.4.0 ADR-004 在文档措辞上有 1 个版本号的差异，需要在 README / setup docs / SECURITY / CONTRIBUTING 里逐处同步

## v0.6+ Roadmap（仍 deferred）

- 5 项原 deferred ops/release skills（`hf-shipping-and-launch` / `hf-ci-cd-and-automation` / `hf-security-hardening` / `hf-performance-gate` / `hf-deprecation-and-migration` / `hf-debugging-and-error-recovery`）继续延后
- 4 家剩余客户端扩展（Gemini CLI / Windsurf / GitHub Copilot / Kiro）+ Gemini CLI 的 6+1 条 slash 命令
- 3 个 user-facing personas（`hf-staff-reviewer` / `hf-qa-engineer` / `hf-security-auditor`）
- `examples/writeonce/` demo evidence trail 下次主链节点变更或 release-tier dogfood 同步触发
- `audit-skill-anatomy.py` 升级为 hard gate（视 SKILL.md 漂移率）
- 真实环境 install smoke 硬门禁（视客户端面铺开节奏 / 真实事故触发再启动）
- HTML 报告若用户反馈"想要更多视觉切片"（如 release pack HTML / cross-feature traceability HTML），再独立评估并 ADR

## Implementation R1 / R2 / R3

R1（已完成）：`scripts/render-closeout-html.py` + `scripts/test_render_closeout_html.py` 落地；17 单元测试全绿；`audit-skill-anatomy.py` + `test_audit_skill_anatomy.py` 不退化。

R2（已完成）：`skills/hf-finalize/SKILL.md` step 6A + Hard Gates / Verification / Red Flags / Reference Guide 同步；`references/finalize-closeout-pack-template.md` 追加 HTML Companion Report 段；浏览器手动验证（hero / workflow trace rail / coverage rings / evidence search filter / release docs sync / handoff）覆盖完成；anti-slop S1-S8 自检全过。

R3（本 ADR + release）：版本号 / 文档同步（plugin.json / marketplace.json / SECURITY.md / CONTRIBUTING.md / .cursor/rules/harness-flow.mdc / README.md / README.zh-CN.md / 3 个 setup 文档）+ ADR-005 锁定 + features/release-v0.5.0/ release pack 落盘 + CHANGELOG `[0.5.0]` 段写入。

## Notes

- v0.5.0 是 v0.4.0 之后的第二个 minor release，体现"先把 release-tier 切片做出来、再回头补 reviewer 视觉化"的节奏：v0.4.0 是引入 release-tier 标识（hf-release，23 → 24 skills），v0.5.0 是 reviewer 体验切面（hf-finalize 输出契约扩展，24 不变）。两个版本都**不**触动主链 FSM 与 router transition map。
- 本 release 是 1 新增脚本（< 800 行）+ 1 SKILL.md 工作流补丁 + 1 模板段追加 + 元数据 / 文档同步，工作面规模与 v0.3.0 patch 量级相当。
- `hf-release` 在本版未修订；本版 release pack 是 HF 自身**第二次** dogfood `hf-release`（v0.4.0 是首次 dogfood），用以验证 `references/release-scope-adr-template.md` / `release-pack-template.md` / `pre-release-engineering-checklist.md` 在"小颗粒度 minor release"场景下仍然实用。
- 与 v0.4.0 的关系：v0.4.0 解决"如何切版本"，v0.5.0 解决"切版本之前如何让单 feature 的 closeout 评审更直观"；正交关系明确，互不替代。
- 与 ADR-004 D9（不刷新 writeonce demo）的关系：本 ADR D8 同向——demo 现有 closeout 不修订，仅新增渲染产物 closeout.html 作为脚本可用性的 reference 实现。
