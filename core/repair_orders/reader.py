"""Read and lightly clean device repair-order workbooks."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from core.repair_orders.text import clean_cell


def read_repair_order_excel(source_file: str | Path | Any, sheet_name: str | int = 0) -> pd.DataFrame:
    """Read an Excel repair-order sheet as object values."""
    return pd.read_excel(source_file, sheet_name=sheet_name, dtype=object)


def clean_raw_repair_orders(raw_data: pd.DataFrame) -> pd.DataFrame:
    """Drop empty rows/columns and normalize basic whitespace."""
    data = raw_data.copy()
    data = data.dropna(axis=0, how="all").dropna(axis=1, how="all")
    data.columns = [str(column).strip() for column in data.columns]
    for column in data.columns:
        data[column] = data[column].map(clean_cell)
    return data.reset_index(drop=True)


def filter_tunnel_rows(data: pd.DataFrame) -> pd.DataFrame:
    """Keep rows whose first-level location type is tunnel when that field exists."""
    if "位置类型（一级场景）" not in data.columns:
        return data
    mask = data["位置类型（一级场景）"].fillna("").astype(str).str.contains("隧道", na=False)
    return data[mask].reset_index(drop=True)
