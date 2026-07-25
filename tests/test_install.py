import json
import tempfile
import unittest
from pathlib import Path

from scripts import install


ROOT = Path(__file__).resolve().parent.parent


class InstallCursorTests(unittest.TestCase):
    def test_cursor_copy_installs_rule_and_skills_idempotently(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "project"

            install.install(target="cursor", dest=dest, mode="copy", source=ROOT)
            install.install(target="cursor", dest=dest, mode="copy", source=ROOT)

            cursor_skills = dest / ".cursor" / "harness-flow-skills"
            rule = dest / ".cursor" / "rules" / "harness-flow.mdc"

            self.assertTrue((cursor_skills / "hf-workflow" / "SKILL.md").is_file())
            self.assertTrue((cursor_skills / "hf-workflow" / "scripts" / "hf_gate.py").is_file())
            self.assertTrue(rule.is_file())

            rule_text = rule.read_text(encoding="utf-8")
            self.assertIn(".cursor/harness-flow-skills/hf-workflow/SKILL.md", rule_text)
            self.assertIn(".cursor/harness-flow-skills/hf-workflow/scripts/hf_gate.py", rule_text)
            self.assertNotIn("`skills/hf-workflow/SKILL.md`", rule_text)


class InstallOpenCodeTests(unittest.TestCase):
    def test_opencode_copy_installs_skills_and_preserves_user_skills(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "project"
            custom_skill = dest / ".opencode" / "skills" / "custom-skill"
            custom_skill.mkdir(parents=True)
            (custom_skill / "SKILL.md").write_text("---\nname: custom-skill\n---\n", encoding="utf-8")

            install.install(target="opencode", dest=dest, mode="copy", source=ROOT)
            install.install(target="opencode", dest=dest, mode="copy", source=ROOT)

            opencode_skills = dest / ".opencode" / "skills"

            self.assertTrue((opencode_skills / "hf-workflow" / "SKILL.md").is_file())
            self.assertTrue((opencode_skills / "hf-workflow" / "scripts" / "hf_gate.py").is_file())
            self.assertTrue((opencode_skills / "custom-skill" / "SKILL.md").is_file())


class InstallWrapperAndSymlinkTests(unittest.TestCase):
    def test_both_target_symlinks_cursor_and_opencode_skills(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "project"

            install.install(target="both", dest=dest, mode="symlink", source=ROOT)

            cursor_skill = dest / ".cursor" / "harness-flow-skills" / "hf-workflow"
            opencode_skill = dest / ".opencode" / "skills" / "hf-workflow"

            self.assertTrue(cursor_skill.is_symlink())
            self.assertTrue((cursor_skill / "SKILL.md").is_file())
            self.assertTrue(opencode_skill.is_symlink())
            self.assertTrue((opencode_skill / "SKILL.md").is_file())

    def test_wrapper_scripts_delegate_to_python_installer(self):
        shell_wrapper = ROOT / "install.sh"
        powershell_wrapper = ROOT / "install.ps1"

        self.assertTrue(shell_wrapper.is_file())
        self.assertTrue(powershell_wrapper.is_file())
        self.assertIn("scripts/install.py", shell_wrapper.read_text(encoding="utf-8"))
        self.assertIn("scripts/install.py", powershell_wrapper.read_text(encoding="utf-8"))


class ReleaseDocsTests(unittest.TestCase):
    def test_release_docs_and_metadata_include_install_scripts(self):
        plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        marketplace = (ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        security = (ROOT / "SECURITY.md").read_text(encoding="utf-8")

        self.assertEqual("4.0.0", plugin["version"])
        self.assertIn("HarnessFlow v4.0.0", marketplace)
        self.assertIn("install.py", marketplace)

        self.assertIn("python scripts/install.py --target cursor", readme)
        self.assertIn("python scripts/install.py --target opencode", readme)
        self.assertIn("install.ps1 -Target both", readme)

        self.assertIn("python scripts/install.py --target cursor", readme_zh)
        self.assertIn("python scripts/install.py --target opencode", readme_zh)
        self.assertIn("install.ps1 -Target both", readme_zh)

        self.assertIn("## [4.0.0] - 2026-07-25", changelog)
        self.assertIn("[Unreleased]: https://github.com/hujianbest/harness-flow/compare/v4.0.0...HEAD", changelog)
        self.assertIn("[4.0.0]: https://github.com/hujianbest/harness-flow/compare/v3.1.0...v4.0.0", changelog)
        self.assertIn("[3.1.0]: https://github.com/hujianbest/harness-flow/compare/v3.0.0...v3.1.0", changelog)

        self.assertIn("scripts/install.py", security)
        self.assertIn(".cursor/", security)
        self.assertIn(".opencode/", security)


if __name__ == "__main__":
    unittest.main()
