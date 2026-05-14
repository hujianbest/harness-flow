# AI Slop Rubric — `hf-code-review` 子规则

> 启发自 OMO `comment-checker` hook（`code-yeongyu/oh-my-openagent` `src/hooks/comment-checker/`）。把"代码 / 注释 / SKILL.md / 文档中的 LLM 生成痕迹"压成一组可 grep 的禁用模式 + 显式例外段。`hf-code-review` Workflow 的"Comment 质量"子节调用本 rubric。

## 禁用模式

### 注释类（适用于 source code 与 SKILL.md / 设计 doc）

```
# 英文冗余形容词 / 副词（reviewer 用 rg）
\b(simply|obviously|clearly|just|merely|moreover|furthermore|in\s+fact|notably|essentially|basically|literally)\b

# 中文冗余 / 解释性词
(显然|显而易见|很容易|非常|特别地|尤其地|事实上|总的来说|不言而喻|众所周知)

# 解释性自然语言注释（描述代码做了什么，而不是为什么）
//\s+(Import the|Define the|Initialize the|Increment the|Return the|Set the|Get the)\s+\w+
#\s+(Import the|Define the|Initialize the|Increment the|Return the|Set the|Get the)\s+\w+

# em-dash / en-dash（中文用全角破折号 "——"，但 em-dash "—" 与 en-dash "–" 在英文 prose 中是 LLM 痕迹）
[—–]
```

### 代码类（适用于 source code）

```
# 过度抽象（< 3 处使用的 abstract base class / interface）
abstract\s+class\s+\w+   # reviewer 应交叉验证至少有 3 处 subclass / impl

# 命名漂移（同一概念在 2+ 处使用不同变量名）
# reviewer 手动判断，无可 grep 模式
```

## 检测命令（reviewer 使用）

### grep / rg 入口

```bash
# 在改动文件上跑禁用模式扫描
git diff main..HEAD -- '*.ts' '*.py' '*.md' '*.go' '*.rs' '*.js' '*.tsx' '*.jsx' \
  | rg -E '\b(simply|obviously|clearly|just|merely|moreover|furthermore|in\s+fact|notably)\b'

# 在中文 prose 上扫
git diff main..HEAD -- '*.md' '*.zh.md' \
  | grep -E '(显然|显而易见|很容易|非常|特别地|尤其地|事实上|总的来说)'

# em-dash / en-dash
git diff main..HEAD | grep -E '[—–]'

# 解释性自然语言注释
git diff main..HEAD -- '*.ts' '*.js' '*.py' '*.go' '*.rs' \
  | rg '//\s+(Import|Define|Initialize|Increment|Return|Set|Get)\s+the\s+\w+'
```

### 结合 audit-skill-anatomy.py（仅 SKILL.md）

```bash
# audit-skill-anatomy.py 不直接含 ai-slop check（按 skill-anatomy.md 第 9 条 audit 只校 anatomy 合规基线）
# reviewer 在 hf-code-review 节点手动跑上面 grep 命令，找到的命中按 [minor][LLM-FIXABLE][ai-slop-NN] 落 finding
```

## 例外（不算 finding）

### 用户文档允许 plain English

`README.md` / `docs/` / `examples/` / project landing pages 中的"用户面"自然语言**允许**含某些禁用词（如 "simply install" 在 install instructions 是合理表述）。reviewer 判断标准：

- **是用户面文案** → 例外允许
- **是工程内部 / spec / design / SKILL.md / source comment** → 命中即 finding

### 测试断言消息允许说明

```python
self.assertEqual(x, 5, "obviously x should be 5 after init")  # 例外允许：测试断言消息说明
self.assertTrue(result, "clearly the validator must accept this")  # 例外允许
```

测试断言消息是面向 test failure 调试的"为什么期望这个值"说明，与"代码做了什么"的解释性注释不同。

### 双语 / i18n 字符串

`messages.zh-CN.md` / i18n locale files 中 "显然" 等中文词如果是用户面 UX 文案，例外允许。

### Markdown 表格 / 列表中的列名 / 简短标签

```markdown
| 状态 | 说明 |
|---|---|
| pass | clearly succeeded |   ← 例外允许：表格 cell 中的简短英文形容词
```

## reviewer 调用方式

`hf-code-review` Workflow "Comment 质量" 子节：

1. 跑上面 4 条 grep 命令于 PR diff（对照 main / origin）
2. 命中数 > 0 → 逐条按以下决策：
   - 例外段命中？→ 标 `[exempt][ai-slop-NN]` 不计 finding
   - 否则 → 落 `[minor][LLM-FIXABLE][ai-slop-NN]` finding 到 review record
3. 若同一 PR 命中 ≥ 5 条 → 升级为 `[important][LLM-FIXABLE][ai-slop-cluster]` 单条 finding（提示 author 整体过一遍 wording）

## 与 OMO comment-checker 的差异

| OMO comment-checker（`@code-yeongyu/comment-checker` 二进制）| HF ai-slop-rubric |
|---|---|
| 实现：runtime hook 自动 block tool.execute.after | 实现：markdown rubric + reviewer 手动 grep |
| 触发：每次 file edit 后立即检查 | 触发：hf-code-review 节点跑一次 |
| 例外：`// @allow` / `// comment-checker-disable-file` 注释豁免 | 例外：本 rubric "例外" 段（用户文档 / test assertion / i18n / 表格）|
| bypass：可绕过 hook（开 disabled_hooks）| bypass：reviewer 主观判断"是否真 slop"（按"用户面 vs 内部"边界） |

OMO 是 runtime 强制；HF v0.6 是 reviewer-driven 半自动（v0.7 runtime 阶段可挂等价 hook，按 ADR-010 P2 范围）。
