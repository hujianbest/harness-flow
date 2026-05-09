#!/usr/bin/env python3
"""HarnessFlow closeout HTML report renderer.

Reads `<feature-dir>/closeout.md` plus a few sibling artifacts (progress.md,
verification/*.md, evidence/*.log) and writes a self-contained
`<feature-dir>/closeout.html` work-summary report.

Design goals:

- Pure Python stdlib (no external dependencies, works in any env that already
  runs `audit-skill-anatomy.py`).
- Single-file output: embedded CSS, no external CDN, no JS framework. A tiny
  inline `<script>` provides client-side filter/sort on the evidence matrix.
- Sync-on-presence: missing inputs degrade gracefully (panels collapse to
  "未提供" instead of crashing).
- Visual companion to closeout.md, NOT a replacement: closeout.md is still
  the canonical machine-readable record.

Usage:
    python3 scripts/render-closeout-html.py <feature-dir>
    python3 scripts/render-closeout-html.py <feature-dir> --output path.html

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


_CSS = """
:root {
  --bg: #0f172a;
  --bg-elev: #1e293b;
  --bg-elev-2: #273449;
  --fg: #e2e8f0;
  --fg-mute: #94a3b8;
  --accent: #38bdf8;
  --accent-2: #818cf8;
  --ok: #22c55e;
  --warn: #f59e0b;
  --err: #ef4444;
  --na: #64748b;
  --border: #334155;
  --radius: 10px;
  --radius-sm: 6px;
  --shadow: 0 4px 24px rgba(0,0,0,0.35);
}
@media (prefers-color-scheme: light) {
  :root {
    --bg: #f8fafc;
    --bg-elev: #ffffff;
    --bg-elev-2: #f1f5f9;
    --fg: #0f172a;
    --fg-mute: #475569;
    --accent: #0284c7;
    --accent-2: #4f46e5;
    --border: #e2e8f0;
    --shadow: 0 4px 24px rgba(15,23,42,0.08);
  }
}
* { box-sizing: border-box; }
html, body {
  margin: 0; padding: 0;
  background: var(--bg);
  color: var(--fg);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC",
               "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  font-size: 14px;
  line-height: 1.55;
}
.wrap { max-width: 1080px; margin: 0 auto; padding: 32px 24px 64px; }
header.hero {
  background: linear-gradient(135deg, var(--bg-elev) 0%, var(--bg-elev-2) 100%);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 28px 32px;
  margin-bottom: 24px;
  box-shadow: var(--shadow);
}
header.hero h1 {
  margin: 0 0 8px; font-size: 22px; font-weight: 600;
  display: flex; align-items: center; gap: 12px; flex-wrap: wrap;
}
header.hero .subtitle { color: var(--fg-mute); font-size: 13px; }
header.hero .conclusion {
  margin-top: 14px; padding: 12px 14px;
  background: var(--bg); border-radius: var(--radius-sm);
  border-left: 3px solid var(--accent);
}
.badge {
  display: inline-block; padding: 2px 10px; border-radius: 999px;
  font-size: 12px; font-weight: 600; line-height: 1.6;
  background: var(--bg-elev-2); color: var(--fg);
  border: 1px solid var(--border);
}
.badge.workflow-closeout { background: rgba(34,197,94,0.15); color: #4ade80; border-color: rgba(34,197,94,0.4); }
.badge.task-closeout    { background: rgba(56,189,248,0.15); color: var(--accent); border-color: rgba(56,189,248,0.4); }
.badge.blocked          { background: rgba(239,68,68,0.15);  color: #f87171; border-color: rgba(239,68,68,0.4); }
.badge.unknown          { background: rgba(100,116,139,0.15); color: var(--fg-mute); border-color: var(--border); }
.badge.status-present { background: rgba(34,197,94,0.15); color: #4ade80; border-color: rgba(34,197,94,0.4); }
.badge.status-na      { background: rgba(100,116,139,0.15); color: var(--fg-mute); border-color: var(--border); }
.badge.status-missing { background: rgba(239,68,68,0.15);  color: #f87171; border-color: rgba(239,68,68,0.4); }
.badge.status-unknown { background: rgba(245,158,11,0.15); color: var(--warn); border-color: rgba(245,158,11,0.4); }

.grid { display: grid; gap: 20px; grid-template-columns: 1fr 1fr; }
@media (max-width: 720px) { .grid { grid-template-columns: 1fr; } }

section.panel {
  background: var(--bg-elev);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 18px 20px;
  margin-bottom: 20px;
  box-shadow: var(--shadow);
}
section.panel > h2 {
  margin: 0 0 14px; font-size: 15px; font-weight: 600;
  display: flex; align-items: center; gap: 10px;
  color: var(--fg);
  border-bottom: 1px solid var(--border);
  padding-bottom: 8px;
}
section.panel > h2 .count { color: var(--fg-mute); font-weight: 400; font-size: 12px; }

dl.kv { margin: 0; display: grid; grid-template-columns: max-content 1fr; gap: 6px 16px; }
dl.kv dt { color: var(--fg-mute); font-size: 12px; }
dl.kv dd { margin: 0; font-size: 13px; word-break: break-word; }
dl.kv dd code { background: var(--bg-elev-2); padding: 1px 6px; border-radius: 4px; font-size: 12px; }

ul.assets { list-style: none; padding: 0; margin: 0; }
ul.assets li {
  padding: 6px 10px; background: var(--bg-elev-2);
  border-radius: var(--radius-sm); margin-bottom: 6px;
  font-size: 12.5px; word-break: break-word;
}
ul.assets li code { background: transparent; padding: 0; }

ul.notes { padding-left: 18px; margin: 0; }
ul.notes li { margin-bottom: 6px; font-size: 13px; }

table.evidence {
  width: 100%; border-collapse: collapse; font-size: 12.5px;
}
table.evidence th, table.evidence td {
  text-align: left; padding: 8px 10px; border-bottom: 1px solid var(--border);
  vertical-align: top;
}
table.evidence th {
  background: var(--bg-elev-2); color: var(--fg-mute); font-weight: 500;
  cursor: pointer; user-select: none;
}
table.evidence th.sorted-asc::after { content: "  \\25B2"; }
table.evidence th.sorted-desc::after { content: "  \\25BC"; }
table.evidence td code { font-size: 12px; }
table.evidence tr.hidden { display: none; }

.evidence-toolbar {
  display: flex; gap: 12px; align-items: center;
  margin-bottom: 12px; flex-wrap: wrap;
}
.evidence-toolbar input[type="search"] {
  flex: 1 1 220px; padding: 6px 10px;
  background: var(--bg-elev-2); color: var(--fg);
  border: 1px solid var(--border); border-radius: var(--radius-sm);
  font-size: 13px;
}
.evidence-toolbar select {
  padding: 6px 10px; background: var(--bg-elev-2); color: var(--fg);
  border: 1px solid var(--border); border-radius: var(--radius-sm);
  font-size: 13px;
}

.timeline {
  display: flex; gap: 0; flex-wrap: wrap;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 14px;
  background: var(--bg-elev-2);
}
.timeline .node {
  display: flex; align-items: center; gap: 8px;
  padding: 8px 12px; margin: 4px 4px;
  background: var(--bg-elev); border-radius: var(--radius-sm);
  border: 1px solid var(--border);
  font-size: 12.5px;
  position: relative;
}
.timeline .node .dot {
  width: 8px; height: 8px; border-radius: 50%;
  background: var(--ok);
}
.timeline .node.na .dot { background: var(--na); }
.timeline .node.missing .dot { background: var(--err); }
.timeline .node .label { font-weight: 500; }
.timeline .node .id { color: var(--fg-mute); font-size: 11px; }
.timeline .node .arrow {
  color: var(--fg-mute); margin: 0 4px;
}

.cov-grid { display: grid; gap: 12px; grid-template-columns: 1fr 1fr; }
@media (max-width: 540px) { .cov-grid { grid-template-columns: 1fr; } }
.cov-item .row { display: flex; justify-content: space-between; font-size: 12px; color: var(--fg-mute); margin-bottom: 4px; }
.cov-item .bar {
  height: 10px; background: var(--bg-elev-2);
  border-radius: 999px; overflow: hidden;
  border: 1px solid var(--border);
}
.cov-item .bar > span {
  display: block; height: 100%;
  background: linear-gradient(90deg, var(--accent), var(--accent-2));
  border-radius: 999px;
}
.cov-item .bar > span.low { background: linear-gradient(90deg, #f59e0b, #ef4444); }
.cov-item .bar > span.med { background: linear-gradient(90deg, #facc15, #f59e0b); }
.cov-item .bar > span.high { background: linear-gradient(90deg, #22c55e, #38bdf8); }

.empty {
  padding: 16px; color: var(--fg-mute); font-size: 13px;
  border: 1px dashed var(--border); border-radius: var(--radius-sm);
  text-align: center;
}

.tests-summary {
  display: flex; flex-wrap: wrap; gap: 14px; margin-bottom: 14px;
}
.stat-pill {
  flex: 1 1 140px; min-width: 120px;
  padding: 12px 14px; background: var(--bg-elev-2);
  border-radius: var(--radius-sm); border: 1px solid var(--border);
}
.stat-pill .num { font-size: 22px; font-weight: 700; color: var(--fg); }
.stat-pill .lbl { color: var(--fg-mute); font-size: 12px; margin-top: 2px; }

footer.meta {
  margin-top: 24px; color: var(--fg-mute); font-size: 12px;
  text-align: center;
}
footer.meta a { color: var(--accent); text-decoration: none; }
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


def _coverage_class(pct: float) -> str:
    if pct < 50:
        return "low"
    if pct < 80:
        return "med"
    return "high"


def _render_hero(pack: ClosoutPack) -> str:
    kind = pack.closeout_type_kind()
    type_label = pack.closeout_type or "未填写"
    conclusion = pack.conclusion or "未填写"
    return f"""
<header class="hero">
  <h1>
    <span>Closeout 报告</span>
    <span class="badge {_e(kind)}">{_e(type_label)}</span>
  </h1>
  <div class="subtitle">
    Feature: <code>{_e(pack.feature_slug)}</code>
    <span style="margin: 0 8px;">·</span>
    Generated: {_e(pack.generated_at)}
  </div>
  <div class="conclusion">
    <strong>Conclusion · </strong>{_e(conclusion)}
  </div>
</header>
"""


def _render_summary_panel(pack: ClosoutPack) -> str:
    items = [
        ("Closeout Type", pack.closeout_type or "—"),
        ("Scope", pack.scope or "—"),
        ("Completion Record", pack.based_on_completion or "—"),
        ("Regression Record", pack.based_on_regression or "—"),
    ]
    rows = "".join(
        f"<dt>{_e(k)}</dt><dd>{_e(v)}</dd>" for k, v in items
    )
    return f"""
<section class="panel">
  <h2>Summary</h2>
  <dl class="kv">{rows}</dl>
</section>
"""


def _render_workflow_timeline(pack: ClosoutPack) -> str:
    if not pack.workflow_trace:
        return ""
    parts: List[str] = []
    for i, (node_id, label, status) in enumerate(pack.workflow_trace):
        if i > 0:
            parts.append('<div class="arrow">→</div>')
        parts.append(
            f'<div class="node {_e(status)}">'
            f'<span class="dot"></span>'
            f'<span class="label">{_e(label)}</span>'
            f'<span class="id">{_e(node_id)}</span>'
            "</div>"
        )
    return f"""
<section class="panel">
  <h2>Workflow Trace <span class="count">{len(pack.workflow_trace)} 节点</span></h2>
  <div class="timeline">{"".join(parts)}</div>
</section>
"""


def _render_test_panel(pack: ClosoutPack) -> str:
    s = pack.test_stats
    cov = pack.coverage

    if s.is_empty() and cov.is_empty():
        return f"""
<section class="panel">
  <h2>Tests &amp; Coverage</h2>
  <div class="empty">未在 evidence/ 与 verification/ 下发现测试或覆盖率证据。<br>
  如需展示，请在 evidence/regression-*.log 中保留测试运行原始输出，或在 verification/coverage.json 写入覆盖率汇总。</div>
</section>
"""

    pills: List[str] = []
    if s.tests_total is not None:
        pills.append(
            f'<div class="stat-pill"><div class="num">{s.tests_passed}/{s.tests_total}</div>'
            f'<div class="lbl">Tests Passed</div></div>'
        )
    if s.files_total is not None:
        pills.append(
            f'<div class="stat-pill"><div class="num">{s.files_passed}/{s.files_total}</div>'
            f'<div class="lbl">Test Files</div></div>'
        )
    if s.duration_ms is not None:
        if s.duration_ms < 1000:
            dur = f"{s.duration_ms:.0f} ms"
        else:
            dur = f"{s.duration_ms / 1000:.2f} s"
        pills.append(
            f'<div class="stat-pill"><div class="num">{_e(dur)}</div>'
            f'<div class="lbl">Duration</div></div>'
        )
    if s.pass_rate is not None:
        pills.append(
            f'<div class="stat-pill"><div class="num">{s.pass_rate * 100:.1f}%</div>'
            f'<div class="lbl">Pass Rate</div></div>'
        )

    cov_html = ""
    if not cov.is_empty():
        items = []
        for label, val in cov.items():
            cls = _coverage_class(val)
            items.append(
                f'<div class="cov-item">'
                f'<div class="row"><span>{_e(label)}</span><span>{val:.1f}%</span></div>'
                f'<div class="bar"><span class="{cls}" style="width: {min(val, 100):.1f}%;"></span></div>'
                "</div>"
            )
        source_label = (
            f'<div class="subtitle" style="color:var(--fg-mute); font-size:12px; margin-top:8px;">'
            f"覆盖率数据源：<code>{_e(cov.source)}</code></div>"
            if cov.source else ""
        )
        cov_html = (
            '<h3 style="margin: 18px 0 10px; font-size: 13px; color: var(--fg-mute);">Code Coverage</h3>'
            f'<div class="cov-grid">{"".join(items)}</div>{source_label}'
        )
    elif not s.is_empty():
        cov_html = (
            '<div class="empty" style="margin-top: 12px;">未提供覆盖率数据。'
            '在 verification/coverage.json 或 evidence 日志中带上 Lines/Statements/Functions/Branches 即可。</div>'
        )

    pills_html = (
        f'<div class="tests-summary">{"".join(pills)}</div>' if pills else ""
    )
    src_html = (
        f'<div class="subtitle" style="color:var(--fg-mute); font-size:12px;">数据源：<code>{_e(s.source_log or "")}</code></div>'
        if s.source_log else ""
    )

    return f"""
<section class="panel">
  <h2>Tests &amp; Coverage</h2>
  {pills_html}
  {src_html}
  {cov_html}
</section>
"""


def _render_evidence_table(pack: ClosoutPack) -> str:
    if not pack.evidence:
        return f"""
<section class="panel">
  <h2>Evidence Matrix</h2>
  <div class="empty">closeout.md 中未发现 Evidence Matrix 内容。</div>
</section>
"""
    rows: List[str] = []
    for r in pack.evidence:
        kind = r.status_kind
        rows.append(
            f'<tr data-status="{_e(kind)}">'
            f"<td>{_e(r.artifact)}</td>"
            f"<td><code>{_e(r.record_path)}</code></td>"
            f'<td><span class="badge status-{_e(kind)}">{_e(r.status or "—")}</span></td>'
            f"<td>{_e(r.notes)}</td>"
            "</tr>"
        )
    return f"""
<section class="panel">
  <h2>Evidence Matrix <span class="count">{len(pack.evidence)} 条</span></h2>
  <div class="evidence-toolbar">
    <input id="evidence-search" type="search" placeholder="搜索工件、路径、备注…" />
    <select id="evidence-status">
      <option value="">全部状态</option>
      <option value="present">present</option>
      <option value="na">N/A</option>
      <option value="missing">missing</option>
      <option value="unknown">未识别</option>
    </select>
  </div>
  <table class="evidence">
    <thead>
      <tr>
        <th>Artifact</th><th>Record Path</th><th>Status</th><th>Notes</th>
      </tr>
    </thead>
    <tbody>{"".join(rows)}</tbody>
  </table>
</section>
"""


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
        f"<dt>{_e(k)}</dt><dd>{_e(pack.state_sync.get(k, '—'))}</dd>"
        for k in keys
    )
    return f"""
<section class="panel">
  <h2>State Sync</h2>
  <dl class="kv">{rows}</dl>
</section>
"""


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

    # Render KV rows; for `Status Fields Synced` we prefer inline value if any,
    # else show "见下方列表" when sub-bullets exist.
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
            f'<dt>Status Fields Synced</dt><dd>'
            f'<span style="color: var(--fg-mute);">见下方列表</span></dd>'
        )

    rows = "".join(kv_rows)

    assets_html = ""
    if pack.updated_long_term_assets:
        items = "".join(
            f"<li>{_e(a)}</li>" for a in pack.updated_long_term_assets
        )
        assets_html = (
            '<h3 style="margin: 16px 0 8px; font-size: 13px; color: var(--fg-mute);">'
            f"Updated Long-Term Assets ({len(pack.updated_long_term_assets)})</h3>"
            f'<ul class="assets">{items}</ul>'
        )

    sfs_html = ""
    if pack.status_fields_synced:
        items = "".join(
            f"<li>{_e(a)}</li>" for a in pack.status_fields_synced
        )
        sfs_html = (
            '<h3 style="margin: 16px 0 8px; font-size: 13px; color: var(--fg-mute);">'
            f"Status Fields Synced ({len(pack.status_fields_synced)})</h3>"
            f'<ul class="assets">{items}</ul>'
        )

    return f"""
<section class="panel">
  <h2>Release / Docs Sync</h2>
  <dl class="kv">{rows}</dl>
  {assets_html}
  {sfs_html}
</section>
"""


def _render_handoff_panel(pack: ClosoutPack) -> str:
    keys = [
        "Remaining Approved Tasks",
        "Next Action Or Recommended Skill",
        "PR / Branch Status",
    ]
    if not any(pack.handoff.get(k) for k in keys) and not pack.limits_notes:
        return ""
    rows = "".join(
        f"<dt>{_e(k)}</dt><dd>{_e(pack.handoff.get(k, '—'))}</dd>"
        for k in keys
    )
    notes_html = ""
    if pack.limits_notes:
        items = "".join(f"<li>{_e(n)}</li>" for n in pack.limits_notes)
        notes_html = (
            '<h3 style="margin: 16px 0 8px; font-size: 13px; color: var(--fg-mute);">'
            f"Limits / Open Notes ({len(pack.limits_notes)})</h3>"
            f'<ul class="notes">{items}</ul>'
        )
    return f"""
<section class="panel">
  <h2>Handoff</h2>
  <dl class="kv">{rows}</dl>
  {notes_html}
</section>
"""


def render_html(pack: ClosoutPack) -> str:
    body = "\n".join(
        block for block in (
            _render_hero(pack),
            _render_workflow_timeline(pack),
            _render_summary_panel(pack),
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
<meta name="generator" content="hf-finalize render-closeout-html.py" />
<title>{_e(title)}</title>
<style>{_CSS}</style>
</head>
<body>
<div class="wrap">
{body}
<footer class="meta">
  HarnessFlow closeout report · 由 <code>scripts/render-closeout-html.py</code> 自 <code>{_e(pack.feature_slug)}/closeout.md</code> 生成 ·
  <a href="closeout.md">查看原始 Markdown</a>
</footer>
</div>
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
