# HarnessFlow

[English](README.md) | [中文](README.zh-CN.md)

**用约束涌现的方式与 AI 代理一起做软件产品：七条不变量、三个用户检查点、落盘的产品事实源——墙内方法完全自由。**

HarnessFlow v4 建立在一条第一性原理之上：**在验证便宜的地方设约束，在验证昂贵的地方给自由。** 文件是否在盘上、命令是否退出 0、用户是否批准了决定——验证便宜，所以成为硬约束；代理是否按"正确顺序"计划、是否用了"正确模板"、是否走了第 3.2 步——验证昂贵且与产品质量几乎无关，所以 v4 刻意一概不规定。约束选对了，好的工作方式会自己涌现，不需要有人替代理写剧本。

## 七条不变量

宪法（[skills/harness/SKILL.md](skills/harness/SKILL.md)）是唯一有约束力的文件。任何时刻违反任何一条，恢复它就是最优先的工作：

1. **真相在盘上。** 关于产品的一切持久事实——意图、现状、决策、证据——存在于 `product/` 与 `work/` 的文件里。聊天是草稿纸；任何新会话只靠磁盘冷启动。
2. **主张须有证据。** 任何"能用 / 通过 / 已修复"必须指向 `harness.py run` 产生的机器输出，附可复现命令。没有证据的主张视为未发生。
3. **先立信号，后动产品。** 改产品之前，可证伪的成功信号已写在 `work/<slug>/signal.md`。形式自由——测试、冒烟脚本、可核对的界面状态——但必须先于实现存在。
4. **主线常青。** `product/state.md` 记录的验证入口任何时刻真实可跑。它坏了，修它优先于一切新工作。
5. **决策权分层。** 用户拥有"做什么、要不要"（意图、取舍、对外承诺、不可逆动作）；代理拥有"怎么做"（设计、工具、顺序、方法），重要选择记入 `product/decisions.md`。归属不明的决定归用户。
6. **独立视角。** 未经"未参与产出的视角"检验（新上下文评审或用户），任何工作不得宣告完成，结论落盘 `work/<slug>/review.md`。作者不给自己的作业打分。
7. **可逆优先。** 优先可回滚路径；不可逆动作必经放行检查点。

## 三个检查点（用户主权的全部）

| 检查点 | 触发时机 | 代理交出什么 |
|---|---|---|
| 意图 | 开始新产品，或实质改变 `product/intent.md` | intent 草稿或差异，等确认 |
| 取舍 | 选择将改变用户可见行为，或与意图冲突 | 选项 + 推荐，等选择 |
| 放行 | 任何不可逆或对外动作之前 | 动作 + 证据 + 回滚方案，等放行 |

三个检查点之外，代理从不请求许可——直接做。自动模式下，意图与取舍可由代理按 intent.md 代行（记入 decisions.md）；放行永远等用户。

## 产品事实源

```
product/
  intent.md     为谁、解决什么、成功标志、明确不做什么 —— 用户主权文件
  state.md      产品现在能做什么、如何运行、验证入口、已知问题
  decisions.md  追加式决策日志（日期、决策、理由、可逆性）
  backlog.md    候选工作与未决问题
work/<slug>/    一条工作线一个目录
  signal.md     可证伪的成功信号（先于实现存在）
  evidence/     harness.py run 产生的机器输出（手工编辑 = 造假）
  review.md     独立视角的检验结论
```

所有文件不限定内部格式——写给下一个冷启动的读者，而不是写给模板。

## 证据协议

唯一的脚本 [skills/harness/scripts/harness.py](skills/harness/scripts/harness.py)（纯 stdlib），只记录、不裁决：

```bash
# 建立产品事实源骨架（从不覆盖已有文件）：
python3 skills/harness/scripts/harness.py init

# 运行任何用于支撑主张的命令，原始输出 + 退出码 + 内容哈希落盘：
python3 skills/harness/scripts/harness.py run --work work/rate-limit --label signal-red -- pytest tests/

# 校验证据完整性（重算哈希必须匹配，随手篡改会被大声暴露）：
python3 skills/harness/scripts/harness.py check --work work/rate-limit
```

不再有 `gate check --to <stage>`——因为不再有阶段。风险缩放是涌现的：改 typo 时不变量成本近乎为零；数据迁移会被不变量 3、6、7 自然逼出规格、评审与回滚方案。这是约束设计的性质，不是档位表的条文。

## 手册（建议，永远不是法律）

`skills/harness/references/` 附四份手册：[塑形](skills/harness/references/shaping.md)（想法 → intent.md）、[构建](skills/harness/references/building.md)（增量与信号）、[评审](skills/harness/references/reviewing.md)（独立评审怎么做）、[放行](skills/harness/references/releasing.md)（发布与沉淀）。偏离手册不需要批准；违反不变量永远不行。

## 安装

HarnessFlow 是纯 Markdown + 一个 stdlib Python 脚本。Cursor 与 OpenCode 推荐使用安装器：

```bash
python scripts/install.py --target cursor --dest /path/to/project
python scripts/install.py --target opencode --dest /path/to/project
python scripts/install.py --target both --dest /path/to/project
./install.sh --target both --dest /path/to/project
./install.ps1 -Target both -Dest C:\path\to\project
```

追加 `--mode symlink` 可让目标项目跟随当前 checkout。

- **Cursor**：安装到 `.cursor/harness-flow-skills/`，并写入路径已重写的 `.cursor/rules/harness-flow.mdc`。
- **Claude Code**：作为插件安装（`/plugin marketplace add <本仓库>`），或直接 vendor `skills/`。
- **OpenCode / 其他**：安装到 `.opencode/skills/`，保留用户自定义 skills。

然后自然地提需求即可："我想要一个把 Markdown 发布到博客的 CLI。" 代理加载宪法，从 `product/` 冷启动，在不变量之内自由工作。

## 设计原则

- **约束结果，不约束步骤。** 框架只校验验证便宜的东西（文件、退出码、用户批准），对方法保持沉默。
- **证据即机器输出。** "测试全绿"是散文；带退出码、哈希封口的日志才是证据。
- **主权可枚举。** 恰好三个检查点属于用户，其余一切归代理裁量——这正是自治可以安全的原因。
- **流程开销是涌现的，不是配置的。** 没有风险档位、没有阶段门禁；不变量自动为风险定价。
- **全部法律一口气读完。** 一份不到 120 行的宪法；手册是选读。

## License

MIT
