#!/usr/bin/env python3
"""Install HarnessFlow assets into agent client project directories."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


TARGETS = {"both", "cursor", "opencode"}
MODES = {"copy", "symlink"}


def install(target: str, dest: str | Path, mode: str = "copy", source: str | Path | None = None) -> None:
    """Install HarnessFlow for a client target into dest."""
    source_root = Path(source) if source is not None else Path(__file__).resolve().parent.parent
    dest_root = Path(dest)

    if target not in TARGETS:
        raise ValueError(f"unsupported target: {target}")
    if mode not in MODES:
        raise ValueError(f"unsupported mode: {mode}")
    if dest_root.exists() and not dest_root.is_dir():
        raise NotADirectoryError(dest_root)
    dest_root.mkdir(parents=True, exist_ok=True)

    targets = ("cursor", "opencode") if target == "both" else (target,)
    for client in targets:
        if client == "cursor":
            _install_cursor(source_root, dest_root, mode)
        elif client == "opencode":
            _install_opencode(source_root, dest_root, mode)


def _install_cursor(source_root: Path, dest_root: Path, mode: str) -> None:
    skills_src = source_root / "skills"
    rule_src = source_root / ".cursor" / "rules" / "harness-flow.mdc"
    if not skills_src.is_dir():
        raise FileNotFoundError(f"missing skills directory: {skills_src}")
    if not rule_src.is_file():
        raise FileNotFoundError(f"missing Cursor rule: {rule_src}")

    cursor_root = dest_root / ".cursor"
    skills_dest = cursor_root / "harness-flow-skills"
    rules_dest = cursor_root / "rules"

    _sync_skill_dirs(skills_src, skills_dest, mode)
    rules_dest.mkdir(parents=True, exist_ok=True)
    rule_text = _rewrite_cursor_rule(rule_src.read_text(encoding="utf-8"))
    (rules_dest / "harness-flow.mdc").write_text(rule_text, encoding="utf-8")


def _install_opencode(source_root: Path, dest_root: Path, mode: str) -> None:
    skills_src = source_root / "skills"
    if not skills_src.is_dir():
        raise FileNotFoundError(f"missing skills directory: {skills_src}")

    _sync_skill_dirs(skills_src, dest_root / ".opencode" / "skills", mode)


def _sync_skill_dirs(skills_src: Path, skills_dest: Path, mode: str) -> None:
    skills_dest.mkdir(parents=True, exist_ok=True)
    for skill_dir in sorted(p for p in skills_src.iterdir() if (p / "SKILL.md").is_file()):
        target_dir = skills_dest / skill_dir.name
        if target_dir.exists():
            if target_dir.is_symlink() or target_dir.is_file():
                target_dir.unlink()
            else:
                shutil.rmtree(target_dir)
        if mode == "copy":
            shutil.copytree(skill_dir, target_dir)
        elif mode == "symlink":
            target_dir.symlink_to(skill_dir, target_is_directory=True)
        else:
            raise ValueError(f"unsupported mode: {mode}")


def _rewrite_cursor_rule(rule_text: str) -> str:
    return rule_text.replace("skills/", ".cursor/harness-flow-skills/")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=sorted(TARGETS), required=True)
    parser.add_argument("--dest", required=True)
    parser.add_argument("--mode", choices=sorted(MODES), default="copy")
    args = parser.parse_args(argv)

    install(target=args.target, dest=args.dest, mode=args.mode)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
