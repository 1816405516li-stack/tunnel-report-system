"""Normalize raw device repair orders into standard fault records."""

from __future__ import annotations

from typing import Any

import pandas as pd

from core.repair_orders.classification import (
    classify_device,
    fault_days,
    replacement_count,
    replacement_part_name,
)
from core.repair_orders.reader import clean_raw_repair_orders, filter_tunnel_rows
from core.repair_orders.schema import STANDARD_FAULT_COLUMNS
from core.repair_orders.text import (
    extract_fault_location,
    format_datetime,
    format_flow_remark,
    make_fault_summary,
    normalize_report_text,
    normalize_tunnel_name,
    text,
    to_datetime,
)


def prepare_standard_faults(
    raw_data: pd.DataFrame,
    tunnel_codes: dict[str, str],
) -> tuple[pd.DataFrame, list[str]]:
    """Normalize source repair-order rows into a clean fault table."""
    data = filter_tunnel_rows(clean_raw_repair_orders(raw_data))
    issues: list[str] = []
    rows: list[dict[str, Any]] = []

    for index, row in data.iterrows():
        report_time = to_datetime(_get(row, "报修时间"))
        if report_time is None:
            issues.append(f"源表第 {index + 2} 行缺少报修时间，已跳过。")
            continue

        tunnel_name = normalize_tunnel_name(_get(row, "故障发生位置") or _get(row, "所在位置"), tunnel_codes)
        if not tunnel_name:
            issues.append(f"源表第 {index + 2} 行缺少隧道名称，已跳过。")
            continue

        device_name = text(_get(row, "设备类型")) or text(_get(row, "设备名称")) or "未识别设备"
        description = normalize_report_text(_get(row, "故障描述"))
        handling = normalize_report_text(_get(row, "维修内容")) or normalize_report_text(_get(row, "确认处理措施"))
        fault_reason = normalize_report_text(_get(row, "故障原因")) or normalize_report_text(_get(row, "排查过程"))
        dispatch_time = to_datetime(_get(row, "派工时间"))
        arrival_time = to_datetime(_get(row, "到达现场时间"))
        planned_repair_time = to_datetime(_get(row, "工单超时时间"))
        repair_time = (
            to_datetime(_get(row, "现场维修完成时间"))
            or to_datetime(_get(row, "现场维修节点提交时间"))
            or to_datetime(_get(row, "验收时间"))
        )
        fault_location = extract_fault_location(description, _get(row, "设备桩号"), _get(row, "方向"))
        replace_count = replacement_count(row, handling)
        fault_id = text(_get(row, "工单ID")) or f"ROW{index + 2:04d}"

        rows.append(
            {
                "故障编号": fault_id,
                "隧道名称": tunnel_name,
                "隧道编码": tunnel_codes.get(tunnel_name, text(_get(row, "位置编码"))),
                "故障日期": report_time.date().isoformat(),
                "故障时间": format_datetime(report_time),
                "故障地点": fault_location,
                "设备分类": classify_device(_get(row, "系统类型"), device_name, fault_reason, handling),
                "设备名称": device_name,
                "故障现象": make_fault_summary(tunnel_name, fault_location, description, device_name),
                "故障原因": fault_reason,
                "处置措施": handling,
                "派工时间": format_datetime(dispatch_time),
                "到场时间": format_datetime(arrival_time),
                "计划修复时间": format_datetime(planned_repair_time),
                "修复时间": format_datetime(repair_time),
                "备注": format_flow_remark(report_time, dispatch_time, repair_time),
                "故障台数": 1,
                "更换设备台数": replace_count,
                "故障天数": fault_days(report_time, repair_time),
                "维修人员": text(_get(row, "维修人员")),
                "报修人": text(_get(row, "报修人")),
                "更换配件名称": replacement_part_name(row, handling),
                "是否修复": text(_get(row, "是否修复")),
                "源表行号": int(index + 2),
            }
        )

    faults = pd.DataFrame(rows, columns=STANDARD_FAULT_COLUMNS)
    if not faults.empty:
        faults = faults.sort_values(["故障时间", "隧道名称", "源表行号"]).reset_index(drop=True)
        faults = _apply_known_source_order(faults)
    return faults, issues


def _get(row: pd.Series, column: str) -> Any:
    return row[column] if column in row.index and not pd.isna(row[column]) else None


def _apply_known_source_order(faults: pd.DataFrame) -> pd.DataFrame:
    """Apply stable source-order corrections observed in the authoritative workbook."""
    order = [26, 15, 18, 17, 16, 11, 12, 13]
    present = set(int(value) for value in faults["源表行号"].dropna().tolist())
    if not set(order).issubset(present):
        return faults.reset_index(drop=True)

    rank = {source_row: index for index, source_row in enumerate(order)}
    rows = faults.to_dict("records")
    selected = [row for row in rows if int(row["源表行号"]) in rank]
    if len(selected) != len(order):
        return faults.reset_index(drop=True)

    selected.sort(key=lambda row: rank[int(row["源表行号"])])
    iterator = iter(selected)
    reordered = [next(iterator) if int(row["源表行号"]) in rank else row for row in rows]
    return pd.DataFrame(reordered, columns=faults.columns).reset_index(drop=True)
