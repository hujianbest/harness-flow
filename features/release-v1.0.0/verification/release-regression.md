# Release Regression — v1.0.0

- Release: `v1.0.0`
- Date: 2026-05-23
- Scope: full repository regression for stable release metadata, skills, agents, commands, install topology, Cursor rule path rewrite, and release pack.
- Conclusion: PASS

## Commands

| Command | Result | Notes |
|---|---|---|
| `python3 scripts/audit-skill-anatomy.py --skills-dir skills` | PASS | 30 skills audited; 0 failures; 0 warnings |
| `python3 -m unittest discover -s tests -p 'test_*.py'` | PASS | 104 tests |
| `python3 scripts/test_audit_skill_anatomy.py` | PASS | 6 tests |
| `python3 skills/hf-wisdom-notebook/scripts/test_validate_wisdom_notebook.py` | PASS | 10 tests |
| `python3 skills/hf-finalize/scripts/test_render_closeout_html.py` | PASS | 17 tests |
| `bash tests/test_install_scripts.sh` | PASS | 14 install/uninstall scenarios |
| `python3 -m json.tool .claude-plugin/plugin.json >/dev/null` | PASS | plugin manifest valid JSON |
| `python3 -m json.tool .claude-plugin/marketplace.json >/dev/null` | PASS | marketplace manifest valid JSON |
| `git diff --check` | PASS | no whitespace errors |

## Freshness

The regression commands were run after v1.0.0 release metadata, `agents/`, `commands/`, setup docs, install scripts, SECURITY, release ADR, and release pack edits were present in the working tree.

## Notes

- No GUI-visible changes; no browser walkthrough required.
- Install regression explicitly verifies `agents/` copy/symlink topology and Cursor installed rule path rewriting for OpenCode and Cursor.
