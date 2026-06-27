"""Tunnel manifest data used by downstream generators."""

from __future__ import annotations

import pandas as pd


def build_tunnel_manifest(monthly_total: pd.DataFrame, tunnel_codes: dict[str, str]) -> pd.DataFrame:
    """Build one row per configured tunnel, including no-fault tunnels."""
    rows = []
    for tunnel_name, tunnel_code in tunnel_codes.items():
        tunnel_rows = monthly_total[monthly_total["隧道名称"] == tunnel_name]
        rows.append(
            {
                "隧道名称": tunnel_name,
                "隧道编码": tunnel_code,
                "故障记录数": int(len(tunnel_rows)),
                "故障台数": int(tunnel_rows["故障台数"].sum()) if not tunnel_rows.empty else 0,
                "更换设备台数": int(tunnel_rows["更换设备台数"].sum()) if not tunnel_rows.empty else 0,
                "是否需要生成空表": bool(tunnel_rows.empty),
            }
        )
    return pd.DataFrame(rows)
