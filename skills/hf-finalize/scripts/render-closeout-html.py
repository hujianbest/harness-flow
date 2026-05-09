#!/usr/bin/env python3
"""HarnessFlow closeout HTML report renderer.

Reads `<feature-dir>/closeout.md` plus a few sibling artifacts (progress.md,
verification/*.md, evidence/*.log) and writes a self-contained
`<feature-dir>/closeout.html` work-summary report.

Design goals
============

- Pure Python stdlib (no external dependencies, works in any env that already
  runs `audit-skill-anatomy.py`).
- Single-file output: embedded CSS, no external CDN, no JS framework. A tiny
  inline `<script>` provides client-side filter/sort on the evidence matrix.
- Sync-on-presence: missing inputs degrade gracefully (panels collapse to
  "未提供" instead of crashing).
- Visual companion to closeout.md, NOT a replacement: closeout.md is still
  the canonical machine-readable record.

System Manifesto (vocalize the system, hf-ui-design § 6.5)
==========================================================

The visual treatment is governed by the following design system declarations
so future edits don't drift into the AI-default SaaS-dashboard slop tropes
listed in `skills/hf-ui-design/references/anti-slop-checklist.md`:

- Style positioning: 工程交付物的"严肃克制" — like an RFC / postmortem /
  commit log, NOT a marketing dashboard. Typography-led, not chrome-led.
- Layout: single column, max 880px content width.
- Background: ONE surface tone for both page and panels; sections separated
  by hairline borders + 56px breathing space, never by elevation shadow.
- Color (OKLCH-derived): neutral cool-gray surface scale + ONE restrained
  accent (engineering indigo, NOT default violet/sky); status family shares
  one chroma value across hues so they read as a set.
- Typography: system stack (explicit reason: zero network requests, broad
  CJK coverage, self-contained HTML); display headings sit 28-36px with
  -0.01em tracking; body 15px / 1.6; numbers `tabular-nums`.
- Heading vs image division: information-dense doc → typography wins;
  the hero shows a quote-style conclusion, not a decorative graphic.
- Global constraints (only 1-3 stops each):
  - radius: 4 / 8 / 12 px — three stops, no 16/20px adhoc
  - shadow: none in default flow (single token reserved for future sticky)
  - motion: ONE easing token (`cubic-bezier(0.2, 0, 0.2, 1)`)
  - border: 1px hairline only

Anti-slop checks consumed (anti-slop-checklist.md § 1-3):
  S1 渐变滥用 — no gradients
  S2 左竖线 callout — quote uses typography, not border-left bar
  S3 默认字体 — system stack with explicit rationale above
  S4 默认紫/蓝 — accent is OKLCH(48% 0.13 250), restrained indigo, not violet
  S5 装饰 SVG / emoji icons — only geometric primitives (dots, rings, bars)
  S6 千篇一律 dashboard — single-column typography-led, not nav+rail+grid
  S7 glassmorphism — none
  S8 浮起卡片 — no box-shadow on cards; hairline borders only

Accessibility (hf-ui-design § 7 + a11y-checklist):
  - WCAG 2.2 AA contrast: ink-1 vs surface-0 ≥ 7:1; ink-3 captions ≥ 4.5:1
  - Focus visible: 2px accent outline + 2px offset on all interactive elements
  - prefers-reduced-motion respected
  - prefers-color-scheme: light / dark both supported
  - Decorative dots wrapped in aria-hidden; status text duplicated in cell
  - Print stylesheet expands the evidence table and drops toolbars

Usage
=====

    python3 skills/hf-finalize/scripts/render-closeout-html.py <feature-dir>
    python3 skills/hf-finalize/scripts/render-closeout-html.py <feature-dir> --output path.html

Note on script location (since v0.5.0):

This script lives under `skills/hf-finalize/scripts/` (the **skill-owned**
tools convention introduced in ADR-005 D10) rather than the repo-root
`scripts/` directory. `scripts/` at repo root is reserved for **maintainer
cross-cutting tools** (e.g. `audit-skill-anatomy.py` which audits ALL skills).
A tool that is invoked by exactly one skill and is part of that skill's hard
gate ships physically with the skill, so vendoring `skills/hf-finalize/`
into a project gives you everything needed to run hf-finalize step 6A —
including this renderer. This also makes OpenCode `.opencode/skills/`
softlinks and Cursor `.cursor/rules/` integrations transparently pick the
script up alongside the skill it belongs to.

Exit codes:
    0 - HTML rendered (closeout.md may be partial; missing fields are tolerated)
    1 - closeout.md missing or unreadable
    2 - script error / bad arguments
"""

from __future__ import annotations

import argparse
import datetime as _dt
import html as _html
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Data containers
# ---------------------------------------------------------------------------


@dataclass
class EvidenceRow:
    artifact: str = ""
    record_path: str = ""
    status: str = ""
    notes: str = ""

    @property
    def status_kind(self) -> str:
        s = self.status.lower()
        if "n/a" in s or "skip" in s or "skipped" in s:
            return "na"
        if "miss" in s or "缺" in s or "fail" in s or "失败" in s:
            return "missing"
        if "present" in s or "通过" in s or "pass" in s or "ok" in s or "已" in s:
            return "present"
        return "unknown"


@dataclass
class TestStats:
    files_passed: Optional[int] = None
    files_total: Optional[int] = None
    tests_passed: Optional[int] = None
    tests_total: Optional[int] = None
    duration_ms: Optional[float] = None
    source_log: Optional[str] = None
    raw_summary: Optional[str] = None

    @property
    def pass_rate(self) -> Optional[float]:
        if self.tests_total and self.tests_total > 0 and self.tests_passed is not None:
            return self.tests_passed / self.tests_total
        return None

    def is_empty(self) -> bool:
        return all(
            v is None
            for v in (
                self.files_passed,
                self.files_total,
                self.tests_passed,
                self.tests_total,
                self.duration_ms,
                self.raw_summary,
            )
        )


@dataclass
class CoverageStats:
    lines: Optional[float] = None
    statements: Optional[float] = None
    functions: Optional[float] = None
    branches: Optional[float] = None
    source: Optional[str] = None  # description of where it came from

    def is_empty(self) -> bool:
        return all(
            v is None
            for v in (self.lines, self.statements, self.functions, self.branches)
        )

    def items(self) -> List[Tuple[str, float]]:
        out: List[Tuple[str, float]] = []
        for label, val in (
            ("Lines", self.lines),
            ("Statements", self.statements),
            ("Functions", self.functions),
            ("Branches", self.branches),
        ):
            if val is not None:
                out.append((label, val))
        return out


@dataclass
class ClosoutPack:
    feature_slug: str = ""
    feature_dir: str = ""
    raw_markdown: str = ""

    closeout_type: str = ""
    scope: str = ""
    conclusion: str = ""
    based_on_completion: str = ""
    based_on_regression: str = ""

    evidence: List[EvidenceRow] = field(default_factory=list)

    state_sync: Dict[str, str] = field(default_factory=dict)
    release_docs_sync: Dict[str, str] = field(default_factory=dict)
    updated_long_term_assets: List[str] = field(default_factory=list)
    status_fields_synced: List[str] = field(default_factory=list)
    handoff: Dict[str, str] = field(default_factory=dict)
    limits_notes: List[str] = field(default_factory=list)

    test_stats: TestStats = field(default_factory=TestStats)
    coverage: CoverageStats = field(default_factory=CoverageStats)
    workflow_trace: List[Tuple[str, str]] = field(default_factory=list)
    # workflow_trace: list of (node_name, status_short)

    generated_at: str = ""

    def closeout_type_kind(self) -> str:
        t = self.closeout_type.lower().replace("`", "").strip()
        if "workflow" in t:
            return "workflow-closeout"
        if "blocked" in t:
            return "blocked"
        if "task" in t:
            return "task-closeout"
        return "unknown"


# ---------------------------------------------------------------------------
# Markdown parsing helpers
# ---------------------------------------------------------------------------


_SECTION_RE = re.compile(r"^##\s+(?P<title>.+?)\s*$")


def _split_sections(md_text: str) -> Dict[str, str]:
    """Return mapping of `## Title` -> body text (between this and next H2).

    Only top-level H2 sections are split; H3 and deeper stay inside their parent.
    """
    sections: Dict[str, str] = {}
    current_title: Optional[str] = None
    current_buf: List[str] = []
    for line in md_text.splitlines():
        m = _SECTION_RE.match(line)
        if m:
            if current_title is not None:
                sections[current_title] = "\n".join(current_buf).strip()
            current_title = m.group("title").strip()
            current_buf = []
        else:
            if current_title is not None:
                current_buf.append(line)
    if current_title is not None:
        sections[current_title] = "\n".join(current_buf).strip()
    return sections


_BULLET_KV_RE = re.compile(r"^\s*-\s+(?P<key>[^:：]+?)\s*[:：]\s*(?P<value>.*?)\s*$")


def _parse_bullet_kv(body: str) -> Dict[str, str]:
    """Parse `- Key: value` bullets from a section body."""
    out: Dict[str, str] = {}
    for raw_line in body.splitlines():
        line = raw_line.rstrip()
        m = _BULLET_KV_RE.match(line)
        if not m:
            continue
        key = m.group("key").strip()
        val = m.group("value").strip()
        # If value already exists, append (multi-line values rare in our schema)
        if key in out and val:
            out[key] = out[key] + " " + val
        else:
            out[key] = val
    return out


def _strip_md_code(s: str) -> str:
    s = s.strip()
    if s.startswith("`") and s.endswith("`") and len(s) >= 2:
        return s[1:-1].strip()
    return s


def _parse_evidence_matrix(body: str) -> List[EvidenceRow]:
    """Try table-form first, then bullet-form fallback."""
    rows: List[EvidenceRow] = []

    table_lines = [
        ln for ln in body.splitlines() if ln.strip().startswith("|")
    ]
    if len(table_lines) >= 2:
        # Heuristic: first line is header, second is divider, rest are rows.
        header_cells = [
            c.strip().lower()
            for c in table_lines[0].strip().strip("|").split("|")
        ]
        # find indexes
        def _idx(*names: str) -> Optional[int]:
            for n in names:
                for i, h in enumerate(header_cells):
                    if n in h:
                        return i
            return None

        i_artifact = _idx("artifact", "工件")
        i_path = _idx("record path", "path", "路径")
        i_status = _idx("status", "状态")
        i_notes = _idx("notes", "备注")

        for raw in table_lines[2:]:
            cells = [c.strip() for c in raw.strip().strip("|").split("|")]
            if not any(cells):
                continue
            row = EvidenceRow()
            if i_artifact is not None and i_artifact < len(cells):
                row.artifact = cells[i_artifact]
            if i_path is not None and i_path < len(cells):
                row.record_path = _strip_md_code(cells[i_path])
            if i_status is not None and i_status < len(cells):
                row.status = _strip_md_code(cells[i_status])
            if i_notes is not None and i_notes < len(cells):
                row.notes = cells[i_notes]
            if row.artifact or row.record_path:
                rows.append(row)
        if rows:
            return rows

    # Bullet-form fallback: groups of `- Artifact:`, `- Record Path:`, `- Status:`, `- Notes:`
    current = EvidenceRow()
    for raw_line in body.splitlines():
        m = _BULLET_KV_RE.match(raw_line)
        if not m:
            continue
        k = m.group("key").strip().lower()
        v = m.group("value").strip()
        if "artifact" in k or "工件" in k:
            if current.artifact or current.record_path:
                rows.append(current)
                current = EvidenceRow()
            current.artifact = v
        elif "record path" in k or "path" in k or "路径" in k:
            current.record_path = _strip_md_code(v)
        elif "status" in k or "状态" in k:
            current.status = _strip_md_code(v)
        elif "notes" in k or "备注" in k:
            current.notes = v
    if current.artifact or current.record_path:
        rows.append(current)
    return rows


def _parse_sub_bullets(body: str, header_pattern: str) -> List[str]:
    """Extract indented sub-bullets under a top-level bullet whose key
    matches `header_pattern` (case-insensitive).

    A "top-level bullet" is any line starting at column 0 with `- `; once we
    enter the matching section we stop at the next such line so we don't
    spill into sibling bullets.
    """
    items: List[str] = []
    inside = False
    header_re = re.compile(
        r"^-\s*" + header_pattern + r"\s*[:：]?", re.IGNORECASE
    )
    for raw in body.splitlines():
        stripped = raw.strip()
        if not inside:
            if header_re.match(stripped):
                inside = True
                continue
        else:
            if re.match(r"^-\s+", raw):
                break
            m = re.match(r"^\s+-\s+(.*)$", raw)
            if m:
                items.append(m.group(1).strip())
            elif stripped == "":
                continue
            elif stripped.startswith("##"):
                break
    return items


def _parse_updated_assets(release_body: str) -> List[str]:
    """Extract sub-bullets under `Updated Long-Term Assets`."""
    return _parse_sub_bullets(release_body, r"Updated Long-?Term Assets")


def _parse_status_fields_synced(release_body: str) -> List[str]:
    """Extract sub-bullets under `Status Fields Synced`."""
    return _parse_sub_bullets(release_body, r"Status Fields Synced")


def _parse_limits_notes(handoff_body: str) -> List[str]:
    """Extract sub-bullets under `Limits / Open Notes`.

    Also handles inline values: `- Limits / Open Notes: some value`.
    """
    notes = _parse_sub_bullets(handoff_body, r"Limits\s*/\s*Open Notes")
    for raw in handoff_body.splitlines():
        m = re.match(
            r"^-\s*Limits\s*/\s*Open Notes\s*[:：]\s*(.+)$",
            raw.strip(),
            re.IGNORECASE,
        )
        if m and m.group(1).strip():
            notes.insert(0, m.group(1).strip())
            break
    return notes


# ---------------------------------------------------------------------------
# Test stats / coverage extraction
# ---------------------------------------------------------------------------


_VITEST_FILES_RE = re.compile(
    r"Test\s+Files\s+(?P<passed>\d+)\s+passed\s*\(\s*(?P<total>\d+)\s*\)",
    re.IGNORECASE,
)
_VITEST_TESTS_RE = re.compile(
    r"\bTests\s+(?P<passed>\d+)\s+passed\s*\(\s*(?P<total>\d+)\s*\)",
    re.IGNORECASE,
)
_DURATION_RE = re.compile(r"Duration\s+(?P<num>\d+(?:\.\d+)?)\s*(?P<unit>ms|s)\b")
_PYTEST_LINE_RE = re.compile(
    r"=+\s*(?P<passed>\d+)\s+passed(?:,\s*\d+\s+\w+)*\s+in\s+(?P<dur>\d+(?:\.\d+)?)s\s*=+",
    re.IGNORECASE,
)
_JEST_TESTS_RE = re.compile(
    r"Tests:\s*(?P<passed>\d+)\s+passed,\s*(?P<total>\d+)\s+total",
    re.IGNORECASE,
)


def _parse_test_log(text: str) -> TestStats:
    stats = TestStats()

    m = _VITEST_FILES_RE.search(text)
    if m:
        stats.files_passed = int(m.group("passed"))
        stats.files_total = int(m.group("total"))
    m = _VITEST_TESTS_RE.search(text)
    if m:
        stats.tests_passed = int(m.group("passed"))
        stats.tests_total = int(m.group("total"))
    m = _JEST_TESTS_RE.search(text)
    if m and stats.tests_passed is None:
        stats.tests_passed = int(m.group("passed"))
        stats.tests_total = int(m.group("total"))
    m = _PYTEST_LINE_RE.search(text)
    if m:
        if stats.tests_passed is None:
            stats.tests_passed = int(m.group("passed"))
            stats.tests_total = int(m.group("passed"))
        if stats.duration_ms is None:
            stats.duration_ms = float(m.group("dur")) * 1000.0

    m = _DURATION_RE.search(text)
    if m and stats.duration_ms is None:
        n = float(m.group("num"))
        stats.duration_ms = n if m.group("unit") == "ms" else n * 1000.0

    if stats.tests_total is not None:
        stats.raw_summary = (
            f"Tests {stats.tests_passed}/{stats.tests_total} passed"
        )
    return stats


_COVERAGE_KV_RE = re.compile(
    r"^\s*[-*]?\s*(?P<key>Lines?|Statements?|Functions?|Branches?)\s*[:：]\s*"
    r"(?P<num>\d+(?:\.\d+)?)\s*%?",
    re.IGNORECASE,
)
# Also accept a vitest/istanbul-style table line:
# `All files | 92.5 | 88.0 | 100 | 92.5`  (Stmts | Branch | Funcs | Lines)
_ISTANBUL_TABLE_RE = re.compile(
    r"^\s*All\s+files\s*\|\s*(?P<stmts>\d+(?:\.\d+)?)\s*\|\s*"
    r"(?P<branch>\d+(?:\.\d+)?)\s*\|\s*(?P<funcs>\d+(?:\.\d+)?)\s*\|\s*"
    r"(?P<lines>\d+(?:\.\d+)?)",
    re.IGNORECASE,
)


def _parse_coverage(text: str, source_label: Optional[str] = None) -> CoverageStats:
    cov = CoverageStats(source=source_label)
    for line in text.splitlines():
        m = _ISTANBUL_TABLE_RE.match(line)
        if m:
            cov.statements = float(m.group("stmts"))
            cov.branches = float(m.group("branch"))
            cov.functions = float(m.group("funcs"))
            cov.lines = float(m.group("lines"))
            return cov
        m = _COVERAGE_KV_RE.match(line)
        if m:
            key = m.group("key").lower()
            val = float(m.group("num"))
            if key.startswith("line"):
                cov.lines = val
            elif key.startswith("statement") or key.startswith("stmt"):
                cov.statements = val
            elif key.startswith("function") or key.startswith("func"):
                cov.functions = val
            elif key.startswith("branch"):
                cov.branches = val
    return cov


def _gather_test_evidence(feature_dir: Path) -> Tuple[TestStats, CoverageStats]:
    """Look at sibling evidence/*.log + verification/regression-*.md for stats."""
    stats = TestStats()
    cov = CoverageStats()

    evidence_dir = feature_dir / "evidence"
    candidate_logs: List[Path] = []
    if evidence_dir.is_dir():
        # Prefer regression-* logs, then green logs, then any .log
        regression_logs = sorted(evidence_dir.glob("regression-*.log"))
        green_logs = sorted(evidence_dir.glob("*green*.log"))
        candidate_logs.extend(regression_logs)
        candidate_logs.extend(green_logs)
        for p in sorted(evidence_dir.glob("*.log")):
            if p not in candidate_logs:
                candidate_logs.append(p)

    for path in candidate_logs:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if stats.is_empty():
            parsed = _parse_test_log(text)
            if not parsed.is_empty():
                parsed.source_log = str(path.relative_to(feature_dir))
                stats = parsed
        if cov.is_empty():
            parsed_cov = _parse_coverage(
                text, source_label=str(path.relative_to(feature_dir))
            )
            if not parsed_cov.is_empty():
                cov = parsed_cov
        if not stats.is_empty() and not cov.is_empty():
            break

    # Also scan verification/*.md for explicit "Coverage:" fields written by humans.
    verification_dir = feature_dir / "verification"
    if cov.is_empty() and verification_dir.is_dir():
        for path in sorted(verification_dir.glob("*.md")):
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            parsed_cov = _parse_coverage(
                text, source_label=str(path.relative_to(feature_dir))
            )
            if not parsed_cov.is_empty():
                cov = parsed_cov
                break

    # Optional explicit coverage file (project-level convention).
    cov_json = feature_dir / "verification" / "coverage.json"
    if cov.is_empty() and cov_json.is_file():
        try:
            data = json.loads(cov_json.read_text(encoding="utf-8"))
            total = data.get("total") or data.get("Total") or data
            for label, attr in (
                ("lines", "lines"),
                ("statements", "statements"),
                ("functions", "functions"),
                ("branches", "branches"),
            ):
                v = total.get(label) if isinstance(total, dict) else None
                if isinstance(v, dict):
                    pct = v.get("pct")
                    if isinstance(pct, (int, float)):
                        setattr(cov, attr, float(pct))
                elif isinstance(v, (int, float)):
                    setattr(cov, attr, float(v))
            if not cov.is_empty():
                cov.source = str(cov_json.relative_to(feature_dir))
        except (OSError, json.JSONDecodeError, AttributeError):
            pass

    return stats, cov


# ---------------------------------------------------------------------------
# Workflow trace (from progress.md + evidence matrix)
# ---------------------------------------------------------------------------


_HF_NODES_ORDER = [
    ("hf-product-discovery", "产品发现"),
    ("hf-discovery-review", "发现评审"),
    ("hf-specify", "规格"),
    ("hf-spec-review", "规格评审"),
    ("hf-design", "设计"),
    ("hf-design-review", "设计评审"),
    ("hf-ui-design", "UI 设计"),
    ("hf-ui-review", "UI 评审"),
    ("hf-tasks", "任务拆分"),
    ("hf-tasks-review", "任务评审"),
    ("hf-test-driven-dev", "TDD 实现"),
    ("hf-test-review", "测试评审"),
    ("hf-code-review", "代码评审"),
    ("hf-traceability-review", "可追溯评审"),
    ("hf-browser-testing", "浏览器测试"),
    ("hf-regression-gate", "回归 gate"),
    ("hf-doc-freshness-gate", "文档 gate"),
    ("hf-completion-gate", "完成 gate"),
    ("hf-finalize", "Finalize"),
]


def _derive_workflow_trace(pack: ClosoutPack) -> List[Tuple[str, str, str]]:
    """Return list of (node_id, label, status) where status ∈ {present, na, missing}.

    Heuristic: a node is `present` if any evidence record path mentions a known
    artifact-folder convention for it; `na` if any evidence row says N/A and
    matches that node; `missing` otherwise (only shown for nodes the project
    actually touched).
    """
    # Pre-build evidence text blob for cheap substring search
    ev_blob = " | ".join(
        f"{r.artifact} :: {r.record_path} :: {r.status} :: {r.notes}"
        for r in pack.evidence
    ).lower()

    trace: List[Tuple[str, str, str]] = []
    for node_id, label in _HF_NODES_ORDER:
        keywords = _node_keywords(node_id)
        hit = False
        na = False
        for kw in keywords:
            if kw in ev_blob:
                hit = True
                # Look for explicit N/A marker near the keyword
                # crude: any row with this keyword whose status is N/A
                for r in pack.evidence:
                    txt = f"{r.artifact} {r.record_path} {r.notes}".lower()
                    if kw in txt and r.status_kind == "na":
                        na = True
                        break
                break
        if not hit:
            continue
        trace.append((node_id, label, "na" if na else "present"))

    # Always append finalize itself if not already in trace, since this report
    # is generated AT finalize time.
    if not any(n[0] == "hf-finalize" for n in trace):
        trace.append(("hf-finalize", "Finalize", "present"))
    return trace


def _node_keywords(node_id: str) -> List[str]:
    """Lowercase keywords whose presence in evidence implies node ran."""
    base = [node_id]
    extra = {
        "hf-product-discovery": ["discovery"],
        "hf-discovery-review": ["discovery-review", "discovery review"],
        "hf-specify": ["spec.md", "spec/", "/spec.", "spec\u00a0"],
        "hf-spec-review": ["spec-review", "spec review"],
        "hf-design": ["design.md", "design/"],
        "hf-design-review": ["design-review", "design review"],
        "hf-ui-design": ["ui-design", "ui design", "ui-spec"],
        "hf-ui-review": ["ui-review", "ui review"],
        "hf-tasks": ["tasks.md", "task-board"],
        "hf-tasks-review": ["tasks-review", "tasks review"],
        "hf-test-driven-dev": ["red", "green", "task-001", "tdd"],
        "hf-test-review": ["test-review", "test review"],
        "hf-code-review": ["code-review", "code review"],
        "hf-traceability-review": ["traceability"],
        "hf-browser-testing": ["browser-testing", "browser testing"],
        "hf-regression-gate": ["regression"],
        "hf-doc-freshness-gate": ["doc-freshness", "doc freshness"],
        "hf-completion-gate": ["completion"],
        "hf-finalize": ["closeout", "finalize"],
    }
    return base + extra.get(node_id, [])


# ---------------------------------------------------------------------------
# Closeout pack assembly
# ---------------------------------------------------------------------------


def parse_closeout(feature_dir: Path) -> ClosoutPack:
    closeout_md = feature_dir / "closeout.md"
    if not closeout_md.is_file():
        raise FileNotFoundError(f"closeout.md not found at {closeout_md}")

    text = closeout_md.read_text(encoding="utf-8")
    sections = _split_sections(text)

    pack = ClosoutPack(
        feature_slug=feature_dir.name,
        feature_dir=str(feature_dir),
        raw_markdown=text,
        generated_at=_dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
    )

    summary = _parse_bullet_kv(sections.get("Closeout Summary", ""))
    pack.closeout_type = _strip_md_code(summary.get("Closeout Type", ""))
    pack.scope = summary.get("Scope", "")
    pack.conclusion = summary.get("Conclusion", "")
    pack.based_on_completion = _strip_md_code(
        summary.get("Based On Completion Record", "")
    )
    pack.based_on_regression = _strip_md_code(
        summary.get("Based On Regression Record", "")
    )

    pack.evidence = _parse_evidence_matrix(sections.get("Evidence Matrix", ""))

    pack.state_sync = _parse_bullet_kv(sections.get("State Sync", ""))
    release_body = sections.get("Release / Docs Sync", "")
    pack.release_docs_sync = _parse_bullet_kv(release_body)
    pack.updated_long_term_assets = _parse_updated_assets(release_body)
    pack.status_fields_synced = _parse_status_fields_synced(release_body)
    pack.handoff = _parse_bullet_kv(sections.get("Handoff", ""))
    pack.limits_notes = _parse_limits_notes(sections.get("Handoff", ""))

    pack.test_stats, pack.coverage = _gather_test_evidence(feature_dir)
    pack.workflow_trace = _derive_workflow_trace(pack)
    return pack


# ---------------------------------------------------------------------------
# HTML rendering
# ---------------------------------------------------------------------------


# Design tokens (see module docstring "System Manifesto" for rationale).
# All visual decisions go through tokens; no hard-coded color/size in render
# helpers. OKLCH used for color derivation so dark/light themes share hue.
_CSS = """
:root {
  /* surface scale - off-white, single hue, very low chroma */
  --surface-0: oklch(99% 0.004 250);
  --surface-1: oklch(96.5% 0.005 250);
  --surface-2: oklch(93% 0.006 250);
  /* ink scale - off-black, never #000 */
  --ink-1: oklch(20% 0.012 250);
  --ink-2: oklch(38% 0.012 250);
  --ink-3: oklch(54% 0.012 250);
  --ink-4: oklch(68% 0.010 250);
  /* hairline */
  --line-1: oklch(91% 0.006 250);
  --line-2: oklch(85% 0.008 250);
  /* status - same chroma family, different hue */
  --ok:    oklch(58% 0.14 150);
  --ok-bg: oklch(96% 0.04 150);
  --warn:  oklch(64% 0.16 75);
  --warn-bg: oklch(96% 0.06 75);
  --err:   oklch(55% 0.20 25);
  --err-bg: oklch(96% 0.05 25);
  --na:    oklch(60% 0.005 250);
  --na-bg: oklch(95% 0.004 250);
  /* one accent - restrained engineering indigo, not violet */
  --accent: oklch(48% 0.13 250);
  --accent-soft: oklch(95% 0.03 250);
  /* radii (3 stops only) */
  --r-1: 4px;
  --r-2: 8px;
  --r-3: 12px;
  /* motion (1 easing only) */
  --ease: cubic-bezier(0.2, 0, 0.2, 1);
}
@media (prefers-color-scheme: dark) {
  :root {
    --surface-0: oklch(16% 0.012 250);
    --surface-1: oklch(20% 0.014 250);
    --surface-2: oklch(24% 0.014 250);
    --ink-1: oklch(94% 0.006 250);
    --ink-2: oklch(78% 0.008 250);
    --ink-3: oklch(62% 0.010 250);
    --ink-4: oklch(50% 0.010 250);
    --line-1: oklch(28% 0.012 250);
    --line-2: oklch(36% 0.014 250);
    --ok-bg: oklch(28% 0.06 150);
    --warn-bg: oklch(28% 0.08 75);
    --err-bg: oklch(28% 0.08 25);
    --na-bg: oklch(26% 0.006 250);
    --accent: oklch(72% 0.14 250);
    --accent-soft: oklch(28% 0.06 250);
  }
}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation: none !important; transition: none !important; }
}

* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
html, body {
  margin: 0;
  background: var(--surface-0);
  color: var(--ink-1);
  /* System stack chosen explicitly: zero network requests (self-contained
     single-file HTML), broad CJK coverage on macOS / Windows / Linux,
     no need to pay for an extra font hue we can't use offline. */
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC",
               "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  font-size: 15px;
  line-height: 1.6;
  font-feature-settings: "kern", "liga", "calt";
  -webkit-font-smoothing: antialiased;
}
:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
  border-radius: var(--r-1);
}
::selection { background: var(--accent-soft); color: var(--ink-1); }

a { color: var(--accent); text-decoration: none; border-bottom: 1px solid currentColor; }
a:hover { color: var(--ink-1); }
code, .mono {
  font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas,
               "Liberation Mono", monospace;
  font-size: 0.92em;
  font-variant-numeric: tabular-nums;
}
.tabular { font-variant-numeric: tabular-nums; }

.page { max-width: 880px; margin: 0 auto; padding: 56px 28px 96px; }
@media (max-width: 640px) { .page { padding: 40px 20px 64px; } }

/* ─── Hero ───────────────────────────────────────────── */

.hero { margin-bottom: 64px; }
.hero .eyebrow {
  font-size: 11px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--ink-3);
  font-weight: 500;
  margin: 0 0 12px;
}
.hero h1 {
  margin: 0 0 8px;
  font-size: clamp(28px, 4vw, 36px);
  line-height: 1.15;
  font-weight: 600;
  letter-spacing: -0.01em;
  color: var(--ink-1);
  font-feature-settings: "ss01", "cv01";
}
.hero .feature-id {
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 0.55em;
  font-weight: 400;
  color: var(--ink-3);
  margin-left: 0.6em;
  letter-spacing: 0;
}
.hero .type-line {
  display: flex; align-items: baseline; gap: 12px; flex-wrap: wrap;
  margin: 4px 0 28px;
}
.hero .type-line .label {
  font-size: 13px; color: var(--ink-3);
}
.hero .type-line .verdict {
  font-size: 16px;
  font-weight: 600;
  letter-spacing: -0.005em;
}
.hero .type-line .verdict.workflow-closeout { color: var(--ok); }
.hero .type-line .verdict.task-closeout     { color: var(--accent); }
.hero .type-line .verdict.blocked           { color: var(--err); }
.hero .type-line .verdict.unknown           { color: var(--ink-3); }
.hero blockquote {
  margin: 0 0 28px;
  padding: 0;
  font-size: 18px;
  line-height: 1.55;
  color: var(--ink-1);
  font-weight: 400;
  letter-spacing: -0.005em;
  max-width: 64ch;
}
.hero blockquote::before {
  content: "“";
  display: inline-block;
  font-size: 1.6em;
  line-height: 0;
  vertical-align: -0.18em;
  color: var(--ink-4);
  margin-right: 0.1em;
}
.hero .meta-line {
  display: flex; flex-wrap: wrap; gap: 24px;
  font-size: 13px; color: var(--ink-3);
  border-top: 1px solid var(--line-1);
  padding-top: 16px;
}
.hero .meta-line dt { display: inline; color: var(--ink-4); margin-right: 6px; font-weight: 500; }
.hero .meta-line dd { display: inline; margin: 0; color: var(--ink-2); }

/* ─── Section ────────────────────────────────────────── */

section { margin-bottom: 56px; }
section > header.section-head {
  margin-bottom: 20px;
}
section > header.section-head .eyebrow {
  font-size: 11px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--ink-3);
  font-weight: 500;
  margin: 0 0 6px;
}
section > header.section-head h2 {
  margin: 0;
  font-size: 22px;
  font-weight: 500;
  letter-spacing: -0.01em;
  color: var(--ink-1);
  display: flex; align-items: baseline; gap: 12px;
}
section > header.section-head h2 .count {
  font-size: 13px; font-weight: 400; color: var(--ink-3);
}
section > header.section-head .lede {
  margin: 4px 0 0; color: var(--ink-3); font-size: 13px;
}

/* ─── KV ─────────────────────────────────────────────── */

dl.kv {
  margin: 0;
  display: grid;
  grid-template-columns: minmax(120px, max-content) 1fr;
  gap: 10px 28px;
  border-top: 1px solid var(--line-1);
  padding-top: 14px;
}
dl.kv dt {
  color: var(--ink-3); font-size: 13px; font-weight: 400;
}
dl.kv dd {
  margin: 0; color: var(--ink-1); font-size: 14px; word-break: break-word;
}
dl.kv dd.muted { color: var(--ink-3); font-style: italic; }

/* ─── Workflow Trace ─────────────────────────────────── */

.trace {
  position: relative;
  padding: 4px 0 4px 0;
}
.trace ol {
  list-style: none;
  margin: 0;
  padding: 0 0 0 22px;
  position: relative;
}
.trace ol::before {
  content: "";
  position: absolute;
  left: 5px; top: 8px; bottom: 8px;
  width: 1px;
  background: var(--line-2);
}
.trace li {
  position: relative;
  padding: 6px 0 6px 20px;
  display: flex; align-items: baseline; gap: 12px;
  flex-wrap: wrap;
}
.trace li::before {
  content: "";
  position: absolute;
  left: -22px; top: 13px;
  width: 11px; height: 11px;
  border-radius: 50%;
  background: var(--surface-0);
  border: 1.5px solid var(--ink-4);
  box-sizing: border-box;
}
.trace li.present::before {
  background: var(--ok); border-color: var(--ok);
}
.trace li.na::before {
  background: var(--surface-0); border-color: var(--ink-4);
}
.trace li.missing::before {
  background: var(--err); border-color: var(--err);
}
.trace li .label {
  color: var(--ink-1); font-weight: 500; font-size: 14px;
}
.trace li.na .label { color: var(--ink-3); }
.trace li .id {
  font-family: ui-monospace, Menlo, monospace;
  font-size: 12px; color: var(--ink-3);
}
.trace li .tag {
  font-size: 11px; letter-spacing: 0.08em; text-transform: uppercase;
  color: var(--ink-4); margin-left: auto;
}

/* ─── Stats / Coverage ──────────────────────────────── */

.stat-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  border-top: 1px solid var(--line-1);
  padding-top: 18px;
  margin-bottom: 28px;
}
@media (max-width: 640px) { .stat-row { grid-template-columns: repeat(2, 1fr); } }
.stat .num {
  font-size: 28px;
  font-weight: 500;
  letter-spacing: -0.02em;
  color: var(--ink-1);
  font-variant-numeric: tabular-nums;
  line-height: 1.1;
}
.stat .num small { font-size: 0.55em; color: var(--ink-3); font-weight: 400; }
.stat .num.ok { color: var(--ok); }
.stat .lbl {
  font-size: 11px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--ink-3);
  margin-top: 6px;
  font-weight: 500;
}

.cov-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  margin-top: 8px;
}
@media (max-width: 640px) { .cov-grid { grid-template-columns: repeat(2, 1fr); } }
.cov-ring {
  display: flex; flex-direction: column; align-items: center;
  gap: 8px;
}
.cov-ring svg { display: block; }
.cov-ring .center {
  font-size: 14px;
  font-weight: 600;
  color: var(--ink-1);
  font-variant-numeric: tabular-nums;
  letter-spacing: -0.01em;
}
.cov-ring .lbl {
  font-size: 11px; letter-spacing: 0.10em; text-transform: uppercase;
  color: var(--ink-3); font-weight: 500;
}
.cov-source { font-size: 12px; color: var(--ink-3); margin-top: 18px; }
.tests-source { font-size: 12px; color: var(--ink-3); margin-top: -16px; margin-bottom: 28px; }

/* ─── Evidence Matrix ───────────────────────────────── */

.evidence-toolbar {
  display: flex; gap: 12px; align-items: center;
  margin-bottom: 14px; flex-wrap: wrap;
}
.evidence-toolbar input[type="search"],
.evidence-toolbar select {
  font: inherit; font-size: 13px;
  padding: 8px 10px;
  background: var(--surface-0);
  color: var(--ink-1);
  border: 1px solid var(--line-2);
  border-radius: var(--r-1);
  transition: border-color 120ms var(--ease);
}
.evidence-toolbar input[type="search"] {
  flex: 1 1 240px;
}
.evidence-toolbar input[type="search"]:focus,
.evidence-toolbar select:focus {
  outline: none; border-color: var(--accent);
}
.evidence-toolbar .legend {
  margin-left: auto; display: flex; gap: 14px;
  font-size: 12px; color: var(--ink-3);
}
.evidence-toolbar .legend .item { display: flex; align-items: center; gap: 6px; }
.evidence-toolbar .legend .dot {
  width: 8px; height: 8px; border-radius: 50%;
}

table.evidence {
  width: 100%; border-collapse: collapse;
  font-size: 13.5px;
}
table.evidence thead th {
  text-align: left;
  font-weight: 500;
  color: var(--ink-3);
  font-size: 11px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  padding: 8px 0;
  border-bottom: 1px solid var(--line-2);
  cursor: pointer;
  user-select: none;
}
table.evidence thead th:not(:first-child) { padding-left: 16px; }
table.evidence thead th.sorted-asc::after  { content: " ↑"; color: var(--accent); }
table.evidence thead th.sorted-desc::after { content: " ↓"; color: var(--accent); }
table.evidence tbody td {
  padding: 12px 0;
  border-bottom: 1px solid var(--line-1);
  vertical-align: top;
  color: var(--ink-1);
}
table.evidence tbody td:not(:first-child) { padding-left: 16px; }
table.evidence tbody tr.hidden { display: none; }
table.evidence tbody tr.na td { color: var(--ink-3); }
table.evidence td.col-status {
  white-space: nowrap;
  font-size: 12px;
  color: var(--ink-2);
}
table.evidence td.col-status .dot {
  display: inline-block; width: 8px; height: 8px;
  border-radius: 50%; margin-right: 8px; vertical-align: 1px;
}
table.evidence .dot.present { background: var(--ok); }
table.evidence .dot.na      { background: var(--surface-0); border: 1.5px solid var(--ink-4); width: 6px; height: 6px; vertical-align: 2px; }
table.evidence .dot.missing { background: var(--err); }
table.evidence .dot.unknown { background: var(--warn); }
table.evidence .dot { background: var(--ink-4); }
.evidence-toolbar .legend .dot.present { background: var(--ok); }
.evidence-toolbar .legend .dot.na      { background: transparent; border: 1.5px solid var(--ink-4); width: 6px; height: 6px; }
.evidence-toolbar .legend .dot.missing { background: var(--err); }
table.evidence td code {
  color: var(--ink-2);
  font-size: 12.5px;
}

/* ─── Lists ─────────────────────────────────────────── */

ul.assets { list-style: none; margin: 0; padding: 0; }
ul.assets li {
  padding: 10px 0;
  font-size: 13.5px;
  color: var(--ink-1);
  border-bottom: 1px solid var(--line-1);
  word-break: break-word;
}
ul.assets li:last-child { border-bottom: none; }
ul.assets li code { color: var(--ink-2); }

.subgroup-head {
  font-size: 11px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--ink-3);
  font-weight: 500;
  margin: 28px 0 8px;
}

ol.notes {
  list-style: none;
  counter-reset: note;
  margin: 0;
  padding: 0;
}
ol.notes li {
  position: relative;
  counter-increment: note;
  padding: 8px 0 8px 28px;
  font-size: 14px;
  color: var(--ink-1);
  border-bottom: 1px solid var(--line-1);
}
ol.notes li:last-child { border-bottom: none; }
ol.notes li::before {
  content: counter(note, decimal-leading-zero);
  position: absolute; left: 0; top: 9px;
  font-size: 11px;
  color: var(--ink-4);
  font-variant-numeric: tabular-nums;
  font-family: ui-monospace, Menlo, monospace;
}

/* ─── Empty state ───────────────────────────────────── */

.empty {
  padding: 18px 0;
  color: var(--ink-3); font-size: 13.5px;
  border-top: 1px solid var(--line-1);
  border-bottom: 1px solid var(--line-1);
  text-align: left;
  line-height: 1.7;
}

/* ─── Footer ────────────────────────────────────────── */

footer.colophon {
  margin-top: 80px;
  padding-top: 24px;
  border-top: 1px solid var(--line-1);
  font-size: 12px;
  color: var(--ink-3);
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 12px;
}
footer.colophon a { color: var(--accent); border-bottom-color: var(--line-2); }

/* ─── Print ─────────────────────────────────────────── */

@media print {
  :root {
    --surface-0: white;
    --surface-1: white;
    --ink-1: #111;
    --ink-2: #333;
    --ink-3: #555;
    --line-1: #ddd;
    --line-2: #bbb;
  }
  body { background: white; }
  .page { padding: 0; max-width: none; }
  .evidence-toolbar { display: none; }
  table.evidence tbody tr.hidden { display: table-row; }
  section { page-break-inside: avoid; }
  footer.colophon { page-break-inside: avoid; }
}
"""


_JS = """
(function () {
  var input = document.getElementById('evidence-search');
  var sel = document.getElementById('evidence-status');
  var table = document.querySelector('table.evidence');
  if (!table) return;
  var tbody = table.tBodies[0];
  function applyFilter() {
    var q = (input && input.value || '').trim().toLowerCase();
    var s = sel && sel.value || '';
    Array.prototype.forEach.call(tbody.rows, function (row) {
      var text = row.textContent.toLowerCase();
      var rowStatus = row.getAttribute('data-status') || '';
      var matchQ = !q || text.indexOf(q) !== -1;
      var matchS = !s || rowStatus === s;
      row.classList.toggle('hidden', !(matchQ && matchS));
    });
  }
  if (input) input.addEventListener('input', applyFilter);
  if (sel) sel.addEventListener('change', applyFilter);

  var headers = table.tHead ? table.tHead.rows[0].cells : [];
  Array.prototype.forEach.call(headers, function (th, idx) {
    th.addEventListener('click', function () {
      var asc = !th.classList.contains('sorted-asc');
      Array.prototype.forEach.call(headers, function (h) {
        h.classList.remove('sorted-asc');
        h.classList.remove('sorted-desc');
      });
      th.classList.add(asc ? 'sorted-asc' : 'sorted-desc');
      var rows = Array.prototype.slice.call(tbody.rows);
      rows.sort(function (a, b) {
        var av = a.cells[idx] ? a.cells[idx].textContent.trim().toLowerCase() : '';
        var bv = b.cells[idx] ? b.cells[idx].textContent.trim().toLowerCase() : '';
        if (av < bv) return asc ? -1 : 1;
        if (av > bv) return asc ? 1 : -1;
        return 0;
      });
      rows.forEach(function (r) { tbody.appendChild(r); });
    });
  });
})();
"""


def _e(s: str) -> str:
    return _html.escape(s, quote=True)


_TYPE_LABEL = {
    "workflow-closeout": "Workflow Closeout",
    "task-closeout": "Task Closeout",
    "blocked": "Blocked",
    "unknown": "Unspecified",
}


def _section(eyebrow: str, title: str, count: Optional[int], body: str,
             lede: str = "") -> str:
    count_html = (
        f' <span class="count">{count}</span>' if count is not None else ""
    )
    lede_html = f'<p class="lede">{_e(lede)}</p>' if lede else ""
    return (
        f'<section>'
        f'<header class="section-head">'
        f'<p class="eyebrow">{_e(eyebrow)}</p>'
        f'<h2>{_e(title)}{count_html}</h2>'
        f'{lede_html}'
        f'</header>'
        f'{body}'
        f'</section>'
    )


def _render_hero(pack: ClosoutPack) -> str:
    kind = pack.closeout_type_kind()
    type_label = _TYPE_LABEL.get(kind, pack.closeout_type or "Unspecified")
    conclusion = pack.conclusion or "未填写。"

    meta_items: List[Tuple[str, str]] = [("Generated", pack.generated_at)]
    if pack.based_on_completion:
        meta_items.append(("Completion", pack.based_on_completion))
    if pack.based_on_regression and "缺失" not in pack.based_on_regression:
        meta_items.append(("Regression", pack.based_on_regression))
    if pack.scope:
        scope_short = pack.scope if len(pack.scope) <= 64 else pack.scope[:62] + "…"
        meta_items.append(("Scope", scope_short))

    meta_html = "".join(
        f'<div><dt>{_e(k)}</dt><dd>{_e(v)}</dd></div>'
        for k, v in meta_items
    )

    return f"""
<header class="hero">
  <p class="eyebrow">Closeout Report</p>
  <h1>{_e(pack.feature_slug)}</h1>
  <div class="type-line">
    <span class="label">结论类型 ·</span>
    <span class="verdict {_e(kind)}">{_e(type_label)}</span>
  </div>
  <blockquote>{_e(conclusion)}</blockquote>
  <dl class="meta-line">{meta_html}</dl>
</header>
"""


def _render_workflow_timeline(pack: ClosoutPack) -> str:
    if not pack.workflow_trace:
        return ""
    items: List[str] = []
    for node_id, label, status in pack.workflow_trace:
        tag_text = {"present": "完成", "na": "N/A", "missing": "缺失"}.get(status, "")
        items.append(
            f'<li class="{_e(status)}">'
            f'<span class="label">{_e(label)}</span>'
            f'<span class="id">{_e(node_id)}</span>'
            f'<span class="tag">{_e(tag_text)}</span>'
            "</li>"
        )
    body = (
        f'<div class="trace"><ol>{"".join(items)}</ol></div>'
    )
    return _section(
        eyebrow="Workflow",
        title="主链节点轨迹",
        count=len(pack.workflow_trace),
        body=body,
        lede="按 evidence matrix 推导出本周期触达的 HF 节点；空心圆点表示按 profile 跳过。",
    )


def _ring_svg(value: float, size: int = 72, stroke: int = 7) -> str:
    """Tiny inline SVG donut chart for one coverage metric."""
    radius = (size - stroke) / 2
    circumference = 2 * 3.14159265 * radius
    pct = max(0.0, min(value, 100.0))
    dash = circumference * pct / 100.0
    cx = cy = size / 2
    # Use semantic accent color for the progress arc; the empty track is hairline.
    return (
        f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" '
        f'role="img" aria-label="{pct:.1f} percent">'
        f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" '
        f'stroke="var(--line-2)" stroke-width="{stroke}" />'
        f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" '
        f'stroke="var(--accent)" stroke-width="{stroke}" '
        f'stroke-linecap="round" '
        f'stroke-dasharray="{dash:.2f} {circumference - dash:.2f}" '
        f'transform="rotate(-90 {cx} {cy})" />'
        f'</svg>'
    )


def _render_test_panel(pack: ClosoutPack) -> str:
    s = pack.test_stats
    cov = pack.coverage

    if s.is_empty() and cov.is_empty():
        empty_body = (
            '<div class="empty">'
            '未在 <code>evidence/</code> 与 <code>verification/</code> 下发现测试或覆盖率证据。'
            '<br>如需展示，可保留 <code>evidence/regression-*.log</code> 或在 '
            '<code>verification/coverage.json</code> 写入覆盖率汇总（pct 字段）。'
            '</div>'
        )
        return _section("Quality", "测试与覆盖率", None, empty_body)

    stat_cells: List[str] = []
    if s.tests_total is not None:
        stat_cells.append(
            f'<div class="stat">'
            f'<div class="num ok"><span class="tabular">{s.tests_passed}</span>'
            f'<small> / {s.tests_total}</small></div>'
            f'<div class="lbl">Tests Passed</div>'
            f'</div>'
        )
    if s.files_total is not None:
        stat_cells.append(
            f'<div class="stat">'
            f'<div class="num"><span class="tabular">{s.files_passed}</span>'
            f'<small> / {s.files_total}</small></div>'
            f'<div class="lbl">Test Files</div>'
            f'</div>'
        )
    if s.duration_ms is not None:
        if s.duration_ms < 1000:
            dur_num, dur_unit = f"{s.duration_ms:.0f}", "ms"
        else:
            dur_num, dur_unit = f"{s.duration_ms / 1000:.2f}", "s"
        stat_cells.append(
            f'<div class="stat">'
            f'<div class="num"><span class="tabular">{_e(dur_num)}</span>'
            f'<small> {dur_unit}</small></div>'
            f'<div class="lbl">Duration</div>'
            f'</div>'
        )
    if s.pass_rate is not None:
        stat_cells.append(
            f'<div class="stat">'
            f'<div class="num ok"><span class="tabular">{s.pass_rate * 100:.1f}</span>'
            f'<small>%</small></div>'
            f'<div class="lbl">Pass Rate</div>'
            f'</div>'
        )

    stat_html = (
        f'<div class="stat-row">{"".join(stat_cells)}</div>' if stat_cells else ""
    )
    src_html = (
        f'<p class="tests-source">数据源 · <code>{_e(s.source_log or "")}</code></p>'
        if s.source_log else ""
    )

    cov_html = ""
    if not cov.is_empty():
        rings: List[str] = []
        for label, val in cov.items():
            rings.append(
                f'<div class="cov-ring">'
                f'<div style="position: relative; width: 72px; height: 72px;">'
                f'{_ring_svg(val)}'
                f'<div style="position: absolute; inset: 0; '
                f'display: flex; align-items: center; justify-content: center;" '
                f'class="center">{val:.0f}'
                f'<small style="font-size:0.6em; color: var(--ink-3);">%</small>'
                f'</div>'
                f'</div>'
                f'<div class="lbl">{_e(label)}</div>'
                f'</div>'
            )
        src = (
            f'<p class="cov-source">覆盖率数据源 · <code>{_e(cov.source)}</code></p>'
            if cov.source else ""
        )
        cov_html = (
            '<p class="subgroup-head">Code Coverage</p>'
            f'<div class="cov-grid">{"".join(rings)}</div>{src}'
        )
    elif not s.is_empty():
        cov_html = (
            '<p class="subgroup-head">Code Coverage</p>'
            '<div class="empty">未提供覆盖率数据。在 '
            '<code>verification/coverage.json</code> 或 evidence 日志中带上 '
            'Lines / Statements / Functions / Branches 即可。</div>'
        )

    body = stat_html + src_html + cov_html
    return _section(
        eyebrow="Quality",
        title="测试与覆盖率",
        count=None,
        body=body,
    )


def _render_evidence_table(pack: ClosoutPack) -> str:
    if not pack.evidence:
        body = '<div class="empty">closeout.md 中未发现 Evidence Matrix 内容。</div>'
        return _section("Trace", "证据矩阵", None, body)

    rows: List[str] = []
    for r in pack.evidence:
        kind = r.status_kind
        rows.append(
            f'<tr class="{_e(kind)}" data-status="{_e(kind)}">'
            f'<td class="col-artifact">{_e(r.artifact)}</td>'
            f'<td class="col-path"><code>{_e(r.record_path)}</code></td>'
            f'<td class="col-status">'
            f'<span class="dot {_e(kind)}" aria-hidden="true"></span>'
            f'{_e(r.status or "—")}'
            f'</td>'
            f'<td class="col-notes">{_e(r.notes)}</td>'
            "</tr>"
        )

    body = (
        '<div class="evidence-toolbar">'
        '<input id="evidence-search" type="search" '
        'placeholder="搜索工件、路径、备注…" aria-label="搜索证据" />'
        '<select id="evidence-status" aria-label="按状态过滤">'
        '<option value="">所有状态</option>'
        '<option value="present">present</option>'
        '<option value="na">N/A</option>'
        '<option value="missing">missing</option>'
        '<option value="unknown">unknown</option>'
        '</select>'
        '<div class="legend" aria-hidden="true">'
        '<span class="item"><span class="dot present"></span>present</span>'
        '<span class="item"><span class="dot na"></span>N/A</span>'
        '<span class="item"><span class="dot missing"></span>missing</span>'
        '</div>'
        '</div>'
        '<table class="evidence">'
        '<thead><tr>'
        '<th>工件</th><th>记录路径</th><th>状态</th><th>备注</th>'
        '</tr></thead>'
        f'<tbody>{"".join(rows)}</tbody>'
        '</table>'
    )
    return _section(
        eyebrow="Trace",
        title="证据矩阵",
        count=len(pack.evidence),
        body=body,
    )


def _render_state_panel(pack: ClosoutPack) -> str:
    keys = [
        "Current Stage",
        "Current Active Task",
        "Workspace Isolation",
        "Worktree Path",
        "Worktree Branch",
        "Worktree Disposition",
    ]
    if not any(pack.state_sync.get(k) for k in keys):
        return ""
    rows = "".join(
        f"<dt>{_e(k)}</dt><dd>{_e(pack.state_sync.get(k, '—') or '—')}</dd>"
        for k in keys
    )
    body = f'<dl class="kv">{rows}</dl>'
    return _section("State", "状态收口", None, body)


def _render_release_panel(pack: ClosoutPack) -> str:
    base_keys = [
        "Release Notes Path",
        "CHANGELOG Path",
        "Index Updated",
    ]
    if (
        not any(pack.release_docs_sync.get(k) for k in base_keys)
        and not pack.updated_long_term_assets
        and not pack.status_fields_synced
    ):
        return ""

    kv_rows: List[str] = []
    for k in base_keys:
        v = pack.release_docs_sync.get(k, "—") or "—"
        kv_rows.append(f"<dt>{_e(k)}</dt><dd>{_e(v)}</dd>")

    sfs_inline = pack.release_docs_sync.get("Status Fields Synced", "") or ""
    if sfs_inline:
        kv_rows.append(
            f"<dt>Status Fields Synced</dt><dd>{_e(sfs_inline)}</dd>"
        )
    elif pack.status_fields_synced:
        kv_rows.append(
            '<dt>Status Fields Synced</dt>'
            '<dd class="muted">见下方清单</dd>'
        )

    rows_html = f'<dl class="kv">{"".join(kv_rows)}</dl>'

    assets_html = ""
    if pack.updated_long_term_assets:
        items = "".join(
            f"<li>{_e(a)}</li>" for a in pack.updated_long_term_assets
        )
        assets_html = (
            f'<p class="subgroup-head">Updated Long-Term Assets · {len(pack.updated_long_term_assets)}</p>'
            f'<ul class="assets">{items}</ul>'
        )

    sfs_html = ""
    if pack.status_fields_synced:
        items = "".join(
            f"<li>{_e(a)}</li>" for a in pack.status_fields_synced
        )
        sfs_html = (
            f'<p class="subgroup-head">Status Fields Synced · {len(pack.status_fields_synced)}</p>'
            f'<ul class="assets">{items}</ul>'
        )

    body = rows_html + assets_html + sfs_html
    return _section(
        eyebrow="Release",
        title="发布与长期资产同步",
        count=None,
        body=body,
    )


def _render_handoff_panel(pack: ClosoutPack) -> str:
    keys = [
        "Remaining Approved Tasks",
        "Next Action Or Recommended Skill",
        "PR / Branch Status",
    ]
    if not any(pack.handoff.get(k) for k in keys) and not pack.limits_notes:
        return ""
    rows = "".join(
        f"<dt>{_e(k)}</dt><dd>{_e(pack.handoff.get(k, '—') or '—')}</dd>"
        for k in keys
    )
    body = f'<dl class="kv">{rows}</dl>'
    if pack.limits_notes:
        items = "".join(f"<li>{_e(n)}</li>" for n in pack.limits_notes)
        body += (
            f'<p class="subgroup-head">Limits / Open Notes · {len(pack.limits_notes)}</p>'
            f'<ol class="notes">{items}</ol>'
        )
    return _section(
        eyebrow="Handoff",
        title="交接与遗留",
        count=None,
        body=body,
    )


def render_html(pack: ClosoutPack) -> str:
    body = "\n".join(
        block for block in (
            _render_hero(pack),
            _render_workflow_timeline(pack),
            _render_test_panel(pack),
            _render_evidence_table(pack),
            _render_state_panel(pack),
            _render_release_panel(pack),
            _render_handoff_panel(pack),
        ) if block
    )
    title = f"Closeout · {pack.feature_slug}"
    return f"""<!doctype html>
<html lang="zh-Hans">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="color-scheme" content="light dark" />
<meta name="generator" content="hf-finalize render-closeout-html.py" />
<title>{_e(title)}</title>
<style>{_CSS}</style>
</head>
<body>
<main class="page">
{body}
<footer class="colophon">
  <span>
    HarnessFlow · closeout report · 由 <code>scripts/render-closeout-html.py</code> 自
    <code>{_e(pack.feature_slug)}/closeout.md</code> 渲染
  </span>
  <a href="closeout.md">查看 closeout.md</a>
</footer>
</main>
<script>{_JS}</script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Render a HarnessFlow closeout HTML report from "
            "<feature-dir>/closeout.md and adjacent artifacts."
        )
    )
    parser.add_argument(
        "feature_dir",
        help="Path to the feature directory, e.g. features/001-foo/",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Output HTML path (default: <feature-dir>/closeout.html)",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppress non-error stdout messages.",
    )
    args = parser.parse_args(argv)

    feature_dir = Path(args.feature_dir).resolve()
    if not feature_dir.is_dir():
        print(f"error: feature dir not found: {feature_dir}", file=sys.stderr)
        return 2

    try:
        pack = parse_closeout(feature_dir)
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    output = Path(args.output).resolve() if args.output else feature_dir / "closeout.html"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_html(pack), encoding="utf-8")
    if not args.quiet:
        rel = output
        try:
            rel = output.relative_to(Path.cwd())
        except ValueError:
            pass
        print(f"wrote {rel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
