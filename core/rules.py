"""Load reusable rules, mappings, and reference data."""

from __future__ import annotations

import json
from pathlib import Path


RULES_DIR = Path(__file__).resolve().parents[1] / "resources" / "rules"

RULE_FILES = {
    "monthly_fault_report": "monthly_fault_report.json",
    "single_tunnel_fault_report": "single_tunnel_fault_report.json",
    "daily_inspection": "daily_inspection.json",
    "frequent_inspection": "frequent_inspection.json",
    "fault_record": "fault_record.json",
}


def load_rules(table: str | None = None) -> dict:
    """Load one table rule set, or all table rule sets when table is omitted."""
    if table is not None:
        try:
            file_name = RULE_FILES[table]
        except KeyError as exc:
            known = ", ".join(sorted(RULE_FILES))
            raise KeyError(f"Unknown rule table: {table}. Known tables: {known}") from exc
        return _load_json(RULES_DIR / file_name)

    return {name: _load_json(RULES_DIR / file_name) for name, file_name in RULE_FILES.items()}


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)
