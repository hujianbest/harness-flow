#!/usr/bin/env python3
"""
TASK-001 verifier: tasks.progress.json schema reference doc + fixtures.

Asserts:
1. skills/hf-test-driven-dev/references/tasks-progress-schema.md exists.
2. The file contains exactly one valid JSON Schema fenced code block.
3. The canonical positive fixture validates against that schema.
4. Three negative fixtures are rejected by that schema.

stdlib only (json + unittest + re + pathlib). No third-party deps.
"""

from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DOC = REPO_ROOT / "skills" / "hf-test-driven-dev" / "references" / "tasks-progress-schema.md"
FIXTURE_DIR = REPO_ROOT / "skills" / "hf-test-driven-dev" / "references" / "tasks-progress-fixtures"


def _extract_first_json_block(md_text: str) -> dict:
    """Pull the first ```json fenced block out of a markdown file."""
    match = re.search(r"```json\s+(\{.*?\})\s+```", md_text, flags=re.DOTALL)
    if not match:
        raise AssertionError("no ```json fenced block found")
    return json.loads(match.group(1))


def _validate(instance: dict, schema: dict) -> tuple[bool, str]:
    """Minimal stdlib JSON Schema subset validator.

    Supports: type, required, properties, enum, pattern, items.
    Anything outside that subset is treated as advisory and ignored.
    """
    expected_type = schema.get("type")
    if expected_type:
        py_type = {
            "object": dict, "array": list, "string": str,
            "integer": int, "number": (int, float), "boolean": bool, "null": type(None),
        }[expected_type]
        if not isinstance(instance, py_type):
            return False, f"expected {expected_type}, got {type(instance).__name__}"

    if isinstance(instance, dict):
        for key in schema.get("required", []):
            if key not in instance:
                return False, f"required key missing: {key}"
        for key, sub_schema in schema.get("properties", {}).items():
            if key in instance:
                ok, why = _validate(instance[key], sub_schema)
                if not ok:
                    return False, f"{key}: {why}"

    if isinstance(instance, list):
        item_schema = schema.get("items")
        if item_schema is not None:
            for idx, item in enumerate(instance):
                ok, why = _validate(item, item_schema)
                if not ok:
                    return False, f"[{idx}]: {why}"

    if "enum" in schema and instance not in schema["enum"]:
        return False, f"value {instance!r} not in enum {schema['enum']}"

    if "pattern" in schema and isinstance(instance, str):
        if not re.match(schema["pattern"], instance):
            return False, f"value {instance!r} does not match pattern {schema['pattern']}"

    return True, "ok"


class TestTasksProgressSchema(unittest.TestCase):
    def test_schema_doc_exists(self):
        self.assertTrue(SCHEMA_DOC.exists(), f"schema doc missing: {SCHEMA_DOC}")

    def test_schema_block_is_valid_json(self):
        schema = _extract_first_json_block(SCHEMA_DOC.read_text(encoding="utf-8"))
        self.assertIsInstance(schema, dict)
        self.assertEqual(schema.get("type"), "object")

    def test_positive_in_progress_validates(self):
        schema = _extract_first_json_block(SCHEMA_DOC.read_text(encoding="utf-8"))
        instance = json.loads((FIXTURE_DIR / "positive-in-progress.json").read_text())
        ok, why = _validate(instance, schema)
        self.assertTrue(ok, f"positive fixture should validate: {why}")

    def test_negative_missing_current_task(self):
        schema = _extract_first_json_block(SCHEMA_DOC.read_text(encoding="utf-8"))
        instance = json.loads((FIXTURE_DIR / "negative-missing-current-task.json").read_text())
        ok, _ = _validate(instance, schema)
        self.assertFalse(ok, "missing current_task should fail")

    def test_negative_invalid_step_format(self):
        schema = _extract_first_json_block(SCHEMA_DOC.read_text(encoding="utf-8"))
        instance = json.loads((FIXTURE_DIR / "negative-invalid-step.json").read_text())
        ok, _ = _validate(instance, schema)
        self.assertFalse(ok, "invalid current_step value should fail")

    def test_negative_step_history_not_array(self):
        schema = _extract_first_json_block(SCHEMA_DOC.read_text(encoding="utf-8"))
        instance = json.loads((FIXTURE_DIR / "negative-step-history-not-array.json").read_text())
        ok, _ = _validate(instance, schema)
        self.assertFalse(ok, "step_history not array should fail")


if __name__ == "__main__":
    unittest.main(verbosity=2)
