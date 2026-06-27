"""Orchestrate all monthly tunnel report workbook generators."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
import json
from pathlib import Path
from typing import Callable, Iterable

import pandas as pd

from generators.monthly_reports.common import (
    CATEGORY_LABELS,
    DATASET_KEYS,
    DEFAULT_CATEGORIES,
    GROUPED_CATEGORIES,
    MonthlyGenerationError,
    ensure_templates_exist,
    iter_tunnels,
    read_csv,
)
from generators.monthly_reports.daily import generate_daily_reports
from generators.monthly_reports.fault_record import generate_fault_record_reports
from generators.monthly_reports.frequent import generate_frequent_reports
from generators.monthly_reports.single_tunnel import generate_single_tunnel_reports
from generators.monthly_reports.total import generate_total_report


ProgressCallback = Callable[[int, int, str], None]


@dataclass(frozen=True)
class MonthlyGenerationResult:
    """Serializable summary for one monthly generation run."""

    month: str
    output_dir: str
    generated_at: str
    completed: int
    total: int
    artifacts: dict[str, str] = field(default_factory=dict)
    category_stats: dict[str, dict[str, int | str | bool]] = field(default_factory=dict)
    preview: dict[str, int | str] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def generate_monthly_reports(
    processed_manifest: dict,
    output_root: str | Path,
    categories: Iterable[str] | None = None,
    progress_callback: ProgressCallback | None = None,
) -> MonthlyGenerationResult:
    """Generate requested final monthly report files."""
    categories = tuple(categories or DEFAULT_CATEGORIES)
    unknown = [category for category in categories if category not in CATEGORY_LABELS]
    if unknown:
        raise MonthlyGenerationError(f"未知生成类型：{', '.join(unknown)}")

    month = str(processed_manifest.get("month") or "").strip()
    if not month:
        raise MonthlyGenerationError("缺少月报月份，请先完成月报解析。")
    ensure_templates_exist(categories)

    datasets = _load_required_datasets(processed_manifest, categories)
    manifest = _load_optional_dataset(processed_manifest, "tunnel_manifest")
    run_dir = Path(output_root) / "monthly_reports" / month / datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir.mkdir(parents=True, exist_ok=True)

    planned_total = _planned_task_count(categories, datasets, manifest)
    completed = 0
    artifacts: dict[str, str] = {}
    category_stats: dict[str, dict[str, int | str | bool]] = {}

    def advance(message: str) -> None:
        nonlocal completed
        completed += 1
        if progress_callback:
            progress_callback(completed, planned_total, message)

    for category in categories:
        if category == "total":
            category_stats[category] = generate_total_report(run_dir, month, datasets[category], artifacts)
            advance("总月报表生成完成")
        elif category == "single_tunnel":
            category_stats[category] = generate_single_tunnel_reports(
                run_dir, month, datasets[category], manifest, artifacts, advance
            )
        elif category == "daily":
            category_stats[category] = generate_daily_reports(run_dir, month, datasets[category], manifest, artifacts, advance)
        elif category == "frequent":
            category_stats[category] = generate_frequent_reports(
                run_dir, month, datasets[category], manifest, artifacts, advance
            )
        elif category == "fault_record":
            category_stats[category] = generate_fault_record_reports(
                run_dir, month, datasets[category], manifest, artifacts, advance
            )

    result = MonthlyGenerationResult(
        month=month,
        output_dir=str(run_dir),
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        completed=completed,
        total=planned_total,
        artifacts=artifacts,
        category_stats=category_stats,
        preview=_build_preview(processed_manifest, category_stats),
    )
    _save_result_manifest(result, run_dir)
    return result


def load_latest_generation_result(output_root: str | Path, month: str | None = None) -> dict | None:
    """Load the most recent generation result manifest if one exists."""
    base_dir = Path(output_root) / "monthly_reports"
    if not base_dir.exists():
        return None
    pattern = f"{month}/*/generation_result.json" if month else "*/*/generation_result.json"
    candidates = sorted(base_dir.glob(pattern), key=lambda path: path.stat().st_mtime, reverse=True)
    if not candidates:
        return None
    try:
        return json.loads(candidates[0].read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _load_required_datasets(processed_manifest: dict, categories: Iterable[str]) -> dict[str, pd.DataFrame]:
    files = processed_manifest.get("files") or {}
    datasets: dict[str, pd.DataFrame] = {}
    for category in categories:
        key = DATASET_KEYS[category]
        path = files.get(key)
        if not path:
            raise MonthlyGenerationError(f"缺少中间数据：{key}，请重新解析月报。")
        datasets[category] = read_csv(path)
    return datasets


def _load_optional_dataset(processed_manifest: dict, dataset_key: str) -> pd.DataFrame:
    path = (processed_manifest.get("files") or {}).get(DATASET_KEYS[dataset_key])
    if not path:
        return pd.DataFrame()
    try:
        return read_csv(path)
    except MonthlyGenerationError:
        return pd.DataFrame()


def _planned_task_count(categories: Iterable[str], datasets: dict[str, pd.DataFrame], manifest: pd.DataFrame) -> int:
    total = 0
    for category in categories:
        if category == "total":
            total += 1
        elif category in GROUPED_CATEGORIES:
            total += len(iter_tunnels(manifest, datasets[category]))
    return max(total, 1)


def _save_result_manifest(result: MonthlyGenerationResult, run_dir: Path) -> None:
    path = run_dir / "generation_result.json"
    path.write_text(json.dumps(result.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")


def _build_preview(processed_manifest: dict, category_stats: dict[str, dict[str, int | str | bool]]) -> dict[str, int | str]:
    return {
        "故障记录数": int(processed_manifest.get("fault_rows") or 0),
        "涉及隧道数": int(processed_manifest.get("tunnel_count") or 0),
        "生成类型数": len(category_stats),
        "生成文件数": sum(int(stats.get("file_count") or 0) for stats in category_stats.values()),
        "生成数据行数": sum(int(stats.get("row_count") or 0) for stats in category_stats.values()),
    }
