"""Intermediate data for 机电日常巡查记录表."""

from __future__ import annotations

from datetime import timedelta

import pandas as pd

from core.repair_orders.schema import REPAIR_PENDING_TEXT
from core.repair_orders.text import combine_reason_and_action
from core.report_data.dates import month_bounds, parse_date


def build_daily_inspection_data(monthly_total: pd.DataFrame, month: str) -> pd.DataFrame:
    """Expand faults into day-level daily inspection records."""
    month_start, month_end = month_bounds(month)
    rows = []
    for _, row in monthly_total.iterrows():
        fault_date = parse_date(row["故障日期"]) or month_start
        repair_date = parse_date(row["修复时间"]) or month_end
        active_end = min(max(repair_date, fault_date), month_end)
        current = max(fault_date, month_start)
        while current <= active_end:
            is_repair_day = repair_date == current
            rows.append(
                {
                    "隧道名称": row["隧道名称"],
                    "隧道编码": row["隧道编码"],
                    "检查日期": current.isoformat(),
                    "检查项目": _daily_category(row),
                    "设备名称": row["设备名称"],
                    "故障地点": row["故障地点"],
                    "养护单位检查情况描述": _inspection_description(row),
                    "采取措施": (
                        combine_reason_and_action(row["故障原因"], row["处置措施"])
                        if is_repair_day and row["处置措施"]
                        else REPAIR_PENDING_TEXT
                    ),
                    "故障编号": row["故障编号"],
                    "源表行号": row["源表行号"],
                }
            )
            current += timedelta(days=1)
    return pd.DataFrame(rows)


def _daily_category(row: pd.Series) -> str:
    device_name = str(row["设备名称"] or "")
    summary = str(row["故障现象"] or "")
    reason = str(row["故障原因"] or "")
    action = str(row["处置措施"] or "")
    device_class = str(row["设备分类"] or "")
    combined = f"{device_name}{summary}{device_class}"
    device_only = f"{device_name}{device_class}"
    if _contains_any(combined, ["LED", "照明"]):
        return "照明设施"
    if _contains_any(combined, ["射流风机", "风机"]):
        return "通风设施"
    if device_name == "紧急电话" and _contains_any(f"{reason}{action}", ["空开", "断电", "电源"]):
        return "供配电设施"
    if "供配电" in device_class or _contains_any(device_only, ["EPS", "UPS", "电力监控", "门禁", "电线", "配电房", "高压柜", "低压柜", "高低压柜", "配电箱", "电缆"]):
        return "供配电设施"
    if "消防" in device_class or _contains_any(combined, ["火灾报警", "手动报警", "手报", "防火卷帘门", "给水", "水管", "水池", "消防"]):
        return "消防与救援设施"
    if _contains_any(
        combined,
        [
            "车道指示器",
            "交通信号灯",
            "摄像机",
            "服务器",
            "录像",
            "PLC",
            "存储阵列",
            "光纤",
            "光缆",
            "尾纤",
            "紧急电话",
            "直流屏",
            "情报板",
            "监控",
            "通信",
        ],
    ):
        return "监控与通信设施"
    return str(row["设备分类"] or "监控与通信设施")


def _contains_any(value: str, keywords: list[str]) -> bool:
    return any(keyword in value for keyword in keywords)


def _inspection_description(row: pd.Series) -> str:
    location = row["故障地点"]
    summary = row["故障现象"]
    if location and isinstance(summary, str):
        summary = summary.replace(str(location), "").strip(" ，,。；;、")
    return f"{row['设备名称']}（{location}）{summary}"
