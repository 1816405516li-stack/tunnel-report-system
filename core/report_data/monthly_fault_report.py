"""Intermediate data for 机电设施故障月报表(总表)."""

from __future__ import annotations

import pandas as pd

from core.repair_orders.schema import STANDARD_FAULT_COLUMNS


def build_monthly_fault_report_data(standard_faults: pd.DataFrame) -> pd.DataFrame:
    """Return total monthly fault-report rows."""
    return standard_faults[STANDARD_FAULT_COLUMNS].copy()
