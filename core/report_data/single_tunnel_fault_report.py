"""Intermediate data for 机电设施故障月报表(分隧道表)."""

from __future__ import annotations

import pandas as pd


def build_single_tunnel_fault_report_data(
    monthly_total: pd.DataFrame,
    tunnel_codes: dict[str, str],
) -> pd.DataFrame:
    """Build one reusable table containing all tunnel-specific rows."""
    rows = []
    for tunnel_name, tunnel_code in tunnel_codes.items():
        tunnel_rows = monthly_total[monthly_total["隧道名称"] == tunnel_name]
        if tunnel_rows.empty:
            rows.append(
                {
                    "隧道名称": tunnel_name,
                    "隧道编码": tunnel_code,
                    "是否空表": True,
                    "故障设备数量": 0,
                    "更换设备数量": 0,
                }
            )
            continue

        for _, row in tunnel_rows.iterrows():
            item = row.to_dict()
            item["是否空表"] = False
            item["故障设备数量"] = int(tunnel_rows["故障台数"].sum())
            item["更换设备数量"] = int(tunnel_rows["更换设备台数"].sum())
            rows.append(item)
    return pd.DataFrame(rows)
