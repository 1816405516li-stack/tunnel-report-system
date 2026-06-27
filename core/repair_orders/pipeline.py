"""End-to-end reusable processing for device repair-order workbooks."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from core.repair_orders.reader import read_repair_order_excel
from core.repair_orders.settings import DEFAULT_TUNNEL_CODES
from core.repair_orders.standardize import prepare_standard_faults
from core.repair_orders.storage import save_datasets, save_manifest
from core.report_data import build_report_datasets
from core.report_data.dates import filter_month, infer_month


@dataclass(frozen=True)
class PipelineResult:
    """Summary returned after a workbook is parsed and datasets are saved."""

    source_path: str
    processed_dir: str
    month: str
    raw_rows: int
    fault_rows: int
    tunnel_count: int
    tunnels: list[str]
    date_start: str
    date_end: str
    files: dict[str, str]
    issues: list[str]


def process_device_repair_workbook(
    source_file: str | Path | Any,
    output_root: str | Path,
    sheet_name: str | int = 0,
    target_month: str | None = None,
    tunnel_codes: dict[str, str] | None = None,
) -> PipelineResult:
    """Read, clean, classify, split, and save reusable report datasets."""
    tunnel_codes = tunnel_codes or DEFAULT_TUNNEL_CODES
    output_root = Path(output_root)

    raw_data = read_repair_order_excel(source_file, sheet_name=sheet_name)
    standard_faults, issues = prepare_standard_faults(raw_data, tunnel_codes)
    if standard_faults.empty:
        raise ValueError("未从设备维修单中识别到有效故障记录。")

    month = target_month or infer_month(standard_faults)
    standard_faults = filter_month(standard_faults, month)
    if standard_faults.empty:
        raise ValueError(f"设备维修单中没有 {month} 的有效故障记录。")

    processed_dir = output_root / month
    processed_dir.mkdir(parents=True, exist_ok=True)

    datasets = build_report_datasets(standard_faults, month, tunnel_codes)
    files = save_datasets(datasets, processed_dir)
    manifest = build_manifest(source_file, processed_dir, month, raw_data, standard_faults, files, issues)
    files["处理清单"] = save_manifest(manifest, processed_dir)
    manifest["files"] = files

    return PipelineResult(**manifest)


def build_manifest(
    source_file: str | Path | Any,
    processed_dir: Path,
    month: str,
    raw_data: pd.DataFrame,
    standard_faults: pd.DataFrame,
    files: dict[str, str],
    issues: list[str],
) -> dict[str, Any]:
    """Build a JSON-serializable processing manifest."""
    fault_dates = pd.to_datetime(standard_faults["故障日期"], errors="coerce")
    tunnels = sorted(standard_faults["隧道名称"].dropna().unique().tolist())
    return {
        "source_path": str(getattr(source_file, "name", source_file)),
        "processed_dir": str(processed_dir),
        "month": month,
        "raw_rows": int(len(raw_data)),
        "fault_rows": int(len(standard_faults)),
        "tunnel_count": int(len(tunnels)),
        "tunnels": tunnels,
        "date_start": fault_dates.min().date().isoformat(),
        "date_end": fault_dates.max().date().isoformat(),
        "files": dict(files),
        "issues": issues,
    }
