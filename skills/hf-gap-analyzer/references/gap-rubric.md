# Gap Rubric — 6 维度详细

> 作者侧 self-check 的扫描清单。每维度按 (问题 → 触发信号 → suggested treat) 三段。每条 finding 必带 anchor（具体行号或段落引用）+ severity（critical / important / minor）+ suggested treat。

## 1. Implicit Intent（作者脑里有但纸上没有）

**问题**：作者实现某个选择有内在理由，但没写下来；下游 design / implementation 节点不知道为什么这样选，可能盲目改掉。

**触发信号**：
- 出现"我们这样做"但无"为什么"
- 选了某种技术 / 某个数字 / 某种命名，但没写 alternative + rationale
- "暂时这样"/"先这样"等弱表述（暗示有想法但没整理）

**Suggested treat**：把隐含理由显式化为 §X 决策段或 ADR；spec 阶段不锁实现，但要锁"为什么这条 FR 是 MUST 而不是 SHOULD"

## 2. AI Slop（生成式语言痕迹）

**问题**：行文充满典型 LLM 生成痕迹，影响可读性 + 暴露未经审阅。

**触发信号（中英双语）**：

| 类别 | 英文模式 | 中文模式 |
|---|---|---|
| 冗余形容词 | `\b(simply\|obviously\|clearly\|just\|merely\|notably)\b` | "显然"/"显而易见"/"非常"/"特别"/"尤其"/"事实上" |
| 解释性自然语言注释 | `// (Import the\|Define the\|Initialize the\|Increment the)` | 描述代码做了什么的 docstring（应描述 *为什么*） |
| 标点 | em-dash `—` / en-dash `–` | （中文用全角）"——"过度使用 |
| 过渡词 | `\b(moreover\|furthermore\|in fact\|in addition)\b` | "此外"/"而且"/"另外"/"再者"成段堆砌 |
| 对称排比 | "first..., second..., third..., finally..." 模板化 | "第一...第二...第三..."固定句式 |

**Suggested treat**：删冗余、压缩到信息密度 / 字符比 ≥ 0.8；保留必要的中文逻辑连词

## 3. Missing Acceptance（FR / NFR 缺可测试 acceptance）

**问题**：requirement 写了 statement 但没 acceptance criteria，design / tasks / TDD 阶段无法判断"做完了没"。

**触发信号**：
- FR Statement 含"应该正确处理"/"应当合理"/"良好支持"等模糊词
- NFR 没有数字阈值（性能 / 容量 / 时延等）
- BDD 形式缺 Given / When / Then 任一段
- Acceptance 写"详见 design"但 design 还没写

**Suggested treat**：补 Acceptance 段；NFR 用 ISO 25010 + QAS 5 要素；用可机械判断的二元结论而非"基本满足"

## 4. Unaddressed Edge Cases（漏写负路径 / 边界 / 失败模式）

**问题**：主路径写完但忘了 negative path / boundary / concurrent / failure mode。

**触发信号**：
- 只描述 happy path
- 接口设计但无超时 / 重试 / 回滚
- 集合操作但无空集 / 单元素 / 大集合 case
- 多线程 / 多会话但无并发模型
- 权限 / 认证但无 unauthorized 场景

**Suggested treat**：补 negative path acceptance；at minimum 列出 timeout / retry / rollback / 并发 / 权限差异 5 类常见 edge case

## 5. Scope Creep（写了已声明 out-of-scope 的事）

**问题**：当前轮 FR / NFR / 任务隐式触碰了 spec §Scope Out / 仓库级 ADR 永久封禁项 / 上游已声明 deferred 的内容。

**触发信号**：
- 引用 v0.7 / v0.8 / 后续版本计划项作为本轮验收依据
- 改动 docs/principles/{soul,methodology-coherence,skill-anatomy}.md（v0.6 全周期不动）
- 引入 OMO Team Mode / Hephaestus / Hashline runtime 等永久封禁项
- 触碰已声明的"未升级 18 个 skill"

**Suggested treat**：要么把项推回 spec / ADR 作为新 in-scope 项（走 hf-increment 入口），要么从本轮删除

## 6. Dangling Reference（引用了不存在的 ADR / 文件 / 节点）

**问题**：引用 `docs/decisions/ADR-099-foo.md` 但该 ADR 不存在；或引用 `hf-shipping-and-launch` 但该 skill 已永久删除。

**触发信号**：
- ADR-NNN 引用：`grep -l 'ADR-NNN' docs/decisions/` 无返回
- skill 引用：`ls skills/<name>/SKILL.md` 不存在
- 文件路径：`ls <path>` 不存在
- 章节锚点：`grep '## <section>' <file>` 无返回

**Suggested treat**：删除 / 改为现有引用 / 把 dangling target 加到 Open Questions 列为 design 阶段补

## Finding 模板

写 `<artifact>.gap-notes.md` 时每条 finding 用如下结构：

```markdown
## Finding F<NNN>

- dimension: <Implicit Intent | AI Slop | Missing Acceptance | Unaddressed Edge Cases | Scope Creep | Dangling Reference>
- severity: <critical | important | minor>
- anchor: <artifact 内的行号或段落引用，如 "spec.md §7 FR-002 line 45">
- problem: <简述发现>
- suggested-treat: <作者可选择的修复方向>
- status: <pending | accepted | rejected-with-reason: ...>  ← 作者吸收时填
```

## gap-notes 文件结构

```markdown
# Gap Notes — <artifact-path>

- analyzed-at: <ISO 8601>
- analyzer: <agent / session>
- artifact-version: <git commit short SHA 或 round-N>
- dimensions-scanned: 6/6
- findings-total: <N>
- findings-by-severity: critical=X important=Y minor=Z

## Finding F001
...

## Finding F002
...

## 作者吸收摘要

- accepted: F001, F003, F005
- rejected: F002 (reason: ...), F004 (reason: ...)
- 修原 artifact 后的 commit / round 号: <ref>
```

## 例子

参见 features/002-omo-inspired-v0.6/ 后续会话中作者主动 invoke gap-analyzer 时产生的 `spec.md.gap-notes.md` / `design.md.gap-notes.md` 实例（dogfood）。本轮 features/002 spec/design/tasks 已经完成 review 不再 retroactively 跑 gap-analyzer；从下一个 v0.6 feature 起作者可在写完草稿后主动调本 skill。
