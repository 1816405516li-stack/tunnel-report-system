"""Intermediate data for 隧道机电设备故障记录单."""

from __future__ import annotations

from datetime import datetime, time, timedelta

import pandas as pd

from core.repair_orders.text import combine_reason_and_action


def build_fault_record_data(monthly_total: pd.DataFrame) -> pd.DataFrame:
    """Map monthly fault rows to fault-record-form fields."""
    rows = []
    for _, row in monthly_total.iterrows():
        replacement_count = int(row["更换设备台数"] or 0)
        rows.append(
            {
                "故障编号": row["故障编号"],
                "隧道名称": row["隧道名称"],
                "隧道编码": row["隧道编码"],
                "故障时间_C3": row["故障时间"],
                "报修时间_E3": row["故障时间"],
                "设备位置_C4": row["故障地点"],
                "报修人_E4": row["报修人"],
                "设备名称_C5": row["设备名称"],
                "修复时限要求_E5": _fault_record_deadline(row["故障时间"]),
                "到场时间_C7": row["派工时间"],
                "维修人员_E7": row["维修人员"],
                "故障现象_C6": _fault_record_summary(row["故障地点"], row["故障现象"]),
                "故障原因和维修记录_C8": combine_reason_and_action(row["故障原因"], row["处置措施"]),
                "处置措施": row["处置措施"],
                "备件名称_C10": row["更换配件名称"] if replacement_count else "",
                "型号规格_D10": "",
                "备件数量_E10": replacement_count if replacement_count else "",
                "处理结果_已修复": bool(row["修复时间"]),
                "处理结果_更换配件": replacement_count > 0,
                "源表行号": row["源表行号"],
            }
        )
    return pd.DataFrame(rows)


def _fault_record_deadline(value: object) -> str:
    parsed = pd.to_datetime(value, errors="coerce")
    if pd.isna(parsed):
        return ""
    deadline = datetime.combine(parsed.date() + timedelta(days=3), time(18, 0))
    return deadline.strftime("%Y-%m-%d %H:%M:%S")


def _fault_record_summary(location: object, summary: object) -> str:
    location_text = str(location or "")
    summary_text = str(summary or "")
    if location_text and summary_text.startswith(location_text):
        return summary_text[len(location_text) :].strip(" ，,、")
    return summary_text
