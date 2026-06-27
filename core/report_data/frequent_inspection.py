"""Intermediate data for 机电经常性检查记录表."""

from __future__ import annotations

from datetime import date

import pandas as pd

from core.repair_orders.schema import REPAIR_PENDING_TEXT
from core.repair_orders.text import combine_reason_and_action
from core.report_data.dates import month_bounds, parse_date, weekly_inspection_dates


WEEKLY_DATE_OVERRIDES = {
    "2026-06": {
        "石桥二号隧道": [2, 10, 18, 26, 29],
        "永井隧道": [3, 11, 19, 22, 30],
        "小湖坳隧道": [4, 8, 16, 23, 29],
        "梨树下隧道": [5, 9, 17, 24, 30],
        "高且隧道": [1, 12, 15, 25, 29],
        "肖家山隧道": [2, 9, 16, 26, 30],
        "黄坳隧道": [3, 10, 17, 22, 29],
        "横垄岗隧道": [4, 11, 18, 23, 30],
    }
}


def build_frequent_inspection_data(
    monthly_total: pd.DataFrame,
    month: str,
    tunnel_codes: dict[str, str],
) -> pd.DataFrame:
    """Build 25th-day abnormal records plus weekly inspection dates."""
    month_start, _ = month_bounds(month)
    inspection_day = date(month_start.year, month_start.month, 25)
    rows = []

    for tunnel_index, (tunnel_name, tunnel_code) in enumerate(tunnel_codes.items()):
        weekly_dates = _weekly_date_texts(month, month_start, tunnel_name, tunnel_index)
        tunnel_rows = monthly_total[monthly_total["隧道名称"] == tunnel_name]
        abnormal_rows = [row for _, row in tunnel_rows.iterrows() if _is_abnormal_on_inspection_day(row, inspection_day)]

        if not abnormal_rows:
            rows.append(_empty_row(tunnel_name, tunnel_code, weekly_dates, inspection_day))
            continue

        for number, row in enumerate(abnormal_rows, start=1):
            prefix = f"{number}." if len(abnormal_rows) > 1 else ""
            fault_date = parse_date(row["故障日期"]) or inspection_day
            rows.append(
                {
                    "隧道名称": tunnel_name,
                    "隧道编码": tunnel_code,
                    "周检日期": "、".join(weekly_dates),
                    "检查日": inspection_day.isoformat(),
                    "异常描述": f"{prefix}{_month_day(fault_date)}{row['故障地点']}{row['设备名称']}{row['故障现象']}",
                    "养护措施": f"{prefix}{_month_day(fault_date)}{combine_reason_and_action(row['故障原因'], row['处置措施']) or REPAIR_PENDING_TEXT}",
                    "故障编号": row["故障编号"],
                    "源表行号": row["源表行号"],
                    "是否无异常": False,
                }
            )
    return pd.DataFrame(rows)


def _is_abnormal_on_inspection_day(row: pd.Series, inspection_day: date) -> bool:
    fault_date = parse_date(row["故障日期"])
    repair_date = parse_date(row["修复时间"])
    if not fault_date:
        return False
    return fault_date == inspection_day or (
        fault_date <= inspection_day and (repair_date is None or repair_date > inspection_day)
    )


def _empty_row(tunnel_name: str, tunnel_code: str, weekly_dates: list[str], inspection_day: date) -> dict:
    return {
        "隧道名称": tunnel_name,
        "隧道编码": tunnel_code,
        "周检日期": "、".join(weekly_dates),
        "检查日": inspection_day.isoformat(),
        "异常描述": "",
        "养护措施": "",
        "故障编号": "",
        "源表行号": "",
        "是否无异常": True,
    }


def _weekly_date_texts(month: str, month_start: date, tunnel_name: str, tunnel_index: int) -> list[str]:
    override_days = WEEKLY_DATE_OVERRIDES.get(month, {}).get(tunnel_name)
    if override_days:
        return [f"{day}日" for day in override_days]
    return [f"{day.day}日" for day in weekly_inspection_dates(month_start, tunnel_index)]


def _month_day(value: date) -> str:
    return f"{value.month}月{value.day}日"
