"""Build all reusable report intermediate datasets."""

from __future__ import annotations

import pandas as pd

from core.report_data.daily_inspection import build_daily_inspection_data
from core.report_data.fault_record import build_fault_record_data
from core.report_data.frequent_inspection import build_frequent_inspection_data
from core.report_data.monthly_fault_report import build_monthly_fault_report_data
from core.report_data.single_tunnel_fault_report import build_single_tunnel_fault_report_data
from core.report_data.tunnel_manifest import build_tunnel_manifest


def build_report_datasets(
    standard_faults: pd.DataFrame,
    month: str,
    tunnel_codes: dict[str, str],
) -> dict[str, pd.DataFrame]:
    """Create all downstream datasets needed by future Excel generators."""
    monthly_total = build_monthly_fault_report_data(standard_faults)
    return {
        "标准故障明细": monthly_total,
        "机电设施故障月报表_总表_数据": monthly_total,
        "机电设施故障月报表_分隧道表_数据": build_single_tunnel_fault_report_data(monthly_total, tunnel_codes),
        "机电日常巡查记录表_数据": build_daily_inspection_data(monthly_total, month),
        "机电经常性检查记录表_数据": build_frequent_inspection_data(monthly_total, month, tunnel_codes),
        "隧道机电设备故障记录单_数据": build_fault_record_data(monthly_total),
        "隧道清单": build_tunnel_manifest(monthly_total, tunnel_codes),
    }
