"""Persist processed repair-order datasets."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


DATASET_FILES = {
    "标准故障明细": "standard_faults.csv",
    "机电设施故障月报表_总表_数据": "monthly_fault_report_total.csv",
    "机电设施故障月报表_分隧道表_数据": "single_tunnel_fault_reports.csv",
    "机电日常巡查记录表_数据": "daily_inspection_records.csv",
    "机电经常性检查记录表_数据": "frequent_inspection_records.csv",
    "隧道机电设备故障记录单_数据": "fault_record_forms.csv",
    "隧道清单": "tunnel_manifest.csv",
}


def save_datasets(datasets: dict[str, pd.DataFrame], processed_dir: Path) -> dict[str, str]:
    """Save each intermediate dataset as UTF-8 CSV."""
    files = {}
    for name, data in datasets.items():
        path = processed_dir / DATASET_FILES[name]
        data.to_csv(path, index=False, encoding="utf-8-sig")
        files[name] = str(path)
    return files


def save_manifest(manifest: dict[str, Any], processed_dir: Path) -> str:
    """Write the processing manifest and return its path."""
    path = processed_dir / "manifest.json"
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(path)
