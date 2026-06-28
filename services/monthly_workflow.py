"""Business workflow wrappers for repair-order parsing and report generation."""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime
from typing import Callable, Iterable

from config.settings import OUTPUTS_DIR, RESOURCES_DIR, WORKSPACE_DIR
from core.repair_orders import PipelineResult, load_tunnel_codes, process_device_repair_workbook
from generators.monthly_report import generate_monthly_reports
from utils.files import safe_file_name


UPLOAD_DIR = WORKSPACE_DIR / "uploads"
PROCESSED_DIR = WORKSPACE_DIR / "processed"
TUNNEL_MAPPING_PATH = RESOURCES_DIR / "mappings" / "tunnels.json"
ProgressCallback = Callable[[int, int, str], None]


def process_fault_upload(uploaded_file) -> dict:
    """Persist an uploaded repair-order workbook and run the parsing pipeline."""
    if uploaded_file is None:
        raise ValueError("请先上传设备维修单 Excel。")

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    source_path = UPLOAD_DIR / f"{datetime.now():%Y%m%d_%H%M%S}_{safe_file_name(uploaded_file.name)}"
    source_path.write_bytes(uploaded_file.getvalue())

    tunnel_codes = load_tunnel_codes(TUNNEL_MAPPING_PATH)
    result: PipelineResult = process_device_repair_workbook(
        source_path,
        PROCESSED_DIR,
        tunnel_codes=tunnel_codes,
    )
    return asdict(result)


def generate_monthly_report_files(
    fault_result: dict,
    categories: Iterable[str],
    progress_callback: ProgressCallback | None = None,
) -> dict:
    """Generate monthly report workbooks from a processed repair-order manifest."""
    return generate_monthly_reports(
        fault_result,
        OUTPUTS_DIR,
        categories=categories,
        progress_callback=progress_callback,
    ).to_dict()
