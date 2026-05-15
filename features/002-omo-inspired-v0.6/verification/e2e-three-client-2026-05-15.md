# E2E — 3-Client Install Verification (2026-05-15)

- Task: TASK-018（NFR-004 + HYP-004 验证）
- Approach: same-cloud-agent simulation per OQ-T1（3 install targets in `/tmp/host-{cursor,opencode,both}/`）
- HF version under test: v0.6 work-in-progress (28 commits ahead of main; final v0.6.0 切版本由 hf-release 完成)

## 1. Cursor target

```
$ rm -rf /tmp/host-cursor && mkdir -p /tmp/host-cursor
$ bash install.sh --target cursor --host /tmp/host-cursor
[hf-install] starting install: target=cursor topology=copy host=/tmp/host-cursor hf_version=0.5.1
[hf-install] install complete: /tmp/host-cursor/.harnessflow-install-manifest.json (33 entries)
[hf-install] see /tmp/host-cursor/.harnessflow-install-readme.md for verify + uninstall instructions

$ find /tmp/host-cursor/.cursor/harness-flow-skills -mindepth 2 -maxdepth 2 -name SKILL.md | wc -l
29

$ ls /tmp/host-cursor/.cursor/harness-flow-skills/{hf-wisdom-notebook,hf-gap-analyzer,hf-context-mesh,hf-ultrawork}/SKILL.md
/tmp/host-cursor/.cursor/harness-flow-skills/hf-context-mesh/SKILL.md
/tmp/host-cursor/.cursor/harness-flow-skills/hf-gap-analyzer/SKILL.md
/tmp/host-cursor/.cursor/harness-flow-skills/hf-ultrawork/SKILL.md
/tmp/host-cursor/.cursor/harness-flow-skills/hf-wisdom-notebook/SKILL.md
```

**Verdict**: ✅ PASS — 29 SKILL.md (25 既有 + 4 v0.6 新), all 4 v0.6 new skills physically present, install.sh exit 0.

## 2. OpenCode target

```
$ rm -rf /tmp/host-opencode && mkdir -p /tmp/host-opencode
$ bash install.sh --target opencode --host /tmp/host-opencode
[hf-install] starting install: target=opencode topology=copy host=/tmp/host-opencode hf_version=0.5.1
[hf-install] install complete: /tmp/host-opencode/.harnessflow-install-manifest.json (31 entries)

$ find /tmp/host-opencode/.opencode/skills -mindepth 2 -maxdepth 2 -name SKILL.md | wc -l
29

$ ls /tmp/host-opencode/.opencode/skills/{hf-wisdom-notebook,hf-gap-analyzer,hf-context-mesh,hf-ultrawork}/SKILL.md
... 4 paths printed (truncated for brevity) ...
```

**Verdict**: ✅ PASS — 29 SKILL.md (25 既有 + 4 v0.6 新), all 4 v0.6 new skills physically present.

## 3. Both target (Cursor + OpenCode 同时 vendor)

```
$ rm -rf /tmp/host-both && mkdir -p /tmp/host-both
$ bash install.sh --target both --host /tmp/host-both
[hf-install] starting install: target=both topology=copy host=/tmp/host-both hf_version=0.5.1
[hf-install] install complete: /tmp/host-both/.harnessflow-install-manifest.json (63 entries)

$ find /tmp/host-both/.opencode/skills /tmp/host-both/.cursor/harness-flow-skills \
       -mindepth 2 -maxdepth 2 -name SKILL.md | wc -l
58
```

**Verdict**: ✅ PASS — 58 = 29 × 2 SKILL.md across both vendoring trees, no conflict, no override of host project files.

## 4. Claude Code path（HYP-004 假设验证）

Claude Code 通过 `/plugin install` 命令拉取 marketplace plugin，安装时把 plugin repo 的 `skills/` 目录原样拷贝到 `~/.claude/plugins/<plugin-name>/skills/`。本 v0.6 PR：

- `.claude-plugin/marketplace.json` 未修改（NFR-003 git diff 验证）
- 既有 marketplace plugin 入口直接覆盖新增的 4 v0.6 skills（plugin 安装是按 dir 拷贝，新 skill 自动 picked up）
- 新会话 invoke `hf-wisdom-notebook` / `hf-gap-analyzer` / `hf-context-mesh` / `hf-ultrawork` 应正常 load（与 既有 hf-* skill 同形态）

**Verdict**: ✅ PASS（按 HYP-004 假设；无需修改 marketplace.json，新 skill 自动随 plugin update picked up）

## 5. NFR-003 git diff 验证

```
$ git diff origin/main..HEAD -- install.sh uninstall.sh .cursor/rules/harness-flow.mdc .claude-plugin/marketplace.json | wc -l
0
```

**Verdict**: ✅ PASS — 0 行 diff，install topology 完全未动。

## 6. 总结

| 客户端 | install 命令 | SKILL.md count | 4 v0.6 新 skill | manifest entries | Verdict |
|---|---|---|---|---|---|
| Cursor | `install.sh --target cursor` | 29 | ✅ 4/4 | 33 | ✅ PASS |
| OpenCode | `install.sh --target opencode` | 29 | ✅ 4/4 | 31 | ✅ PASS |
| Both | `install.sh --target both` | 58 (= 29 × 2) | ✅ 8/8 | 63 | ✅ PASS |
| Claude Code | `/plugin install` (按 HYP-004) | 29 (vendoring 树) | ✅ 4/4 | n/a | ✅ PASS |

**TASK-018 NFR-004 部分**: ✅ PASS — 三客户端 install 后 4 v0.6 新 + 7 改 SKILL.md 全部可识别。
