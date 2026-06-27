"""Date helpers for report intermediate data."""

from __future__ import annotations

from calendar import monthrange
from datetime import date, timedelta

import pandas as pd

from core.repair_orders.text import to_datetime


def month_bounds(month: str) -> tuple[date, date]:
    """Return first and last day for YYYY-MM."""
    year, month_num = [int(part) for part in month.split("-")]
    last_day = monthrange(year, month_num)[1]
    return date(year, month_num, 1), date(year, month_num, last_day)


def filter_month(data: pd.DataFrame, month: str, date_column: str = "故障日期") -> pd.DataFrame:
    """Filter a standard fault table to one report month."""
    month_start, month_end = month_bounds(month)
    dates = pd.to_datetime(data[date_column], errors="coerce").dt.date
    return data[(dates >= month_start) & (dates <= month_end)].reset_index(drop=True)


def infer_month(data: pd.DataFrame, date_column: str = "故障日期") -> str:
    """Infer report month from the earliest valid date in a table."""
    dates = pd.to_datetime(data[date_column], errors="coerce").dropna()
    if dates.empty:
        raise ValueError("无法从故障日期判断月份。")
    first = dates.min()
    return f"{first.year:04d}-{first.month:02d}"


def parse_date(value) -> date | None:
    """Parse a stored date or datetime value to date."""
    parsed = to_datetime(value)
    return parsed.date() if parsed else None


def weekly_inspection_dates(month_start: date, tunnel_index: int) -> list[date]:
    """Choose one workday in each Monday week for frequent inspection."""
    _, month_end = month_bounds(f"{month_start.year:04d}-{month_start.month:02d}")
    current = month_start
    mondays = []
    while current <= month_end:
        if current.weekday() == 0:
            mondays.append(current)
        current += timedelta(days=1)

    dates = []
    for week_index, monday in enumerate(mondays):
        offset = (tunnel_index + week_index) % 5
        candidate = monday + timedelta(days=offset)
        if candidate.month != month_start.month:
            candidate = monday
        dates.append(candidate)
    return dates
