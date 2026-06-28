"""Data helpers for standard-fault preview and field tracing."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from core.repair_orders.text import combine_reason_and_action


PREVIEW_COLUMNS = [
    "源表行号",
    "隧道名称",
    "故障日期",
    "故障地点",
    "设备名称",
    "故障现象",
    "故障原因",
    "处置措施",
    "原因及处理",
    "修复时间",
]


def standard_faults_path(fault_result: dict[str, Any] | None) -> Path | None:
    if not fault_result:
        return None
    files = fault_result.get("files") or {}
    path = files.get("标准故障明细")
    return Path(path) if path else None


def load_standard_faults_preview(fault_result: dict[str, Any] | None) -> pd.DataFrame:
    """Load standard fault rows and add preview-only derived fields."""
    path = standard_faults_path(fault_result)
    if not path or not path.exists():
        return pd.DataFrame()
    data = pd.read_csv(path, encoding="utf-8-sig").fillna("")
    if {"故障原因", "处置措施"}.issubset(data.columns):
        data["原因及处理"] = [
            combine_reason_and_action(reason, action)
            for reason, action in zip(data["故障原因"], data["处置措施"])
        ]
    return data


def visible_preview_columns(data: pd.DataFrame) -> list[str]:
    return [column for column in PREVIEW_COLUMNS if column in data.columns]


def build_trace_rows(row: pd.Series) -> list[dict[str, str]]:
    """Explain how key report fields were derived for one fault row."""
    return [
        {
            "字段": "故障现象",
            "生成结果": str(row.get("故障现象", "")),
            "来源字段": "设备维修单：故障描述",
            "使用规则": "去掉重复隧道名和已单独成列的故障地点，保留新故障表达。",
        },
        {
            "字段": "处置措施",
            "生成结果": str(row.get("处置措施", "")),
            "来源字段": "设备维修单：维修内容 / 确认处理措施",
            "使用规则": "优先维修内容；缺失时使用确认处理措施；清理空格和结尾标点。",
        },
        {
            "字段": "原因及处理",
            "生成结果": str(row.get("原因及处理", "")),
            "来源字段": "标准故障明细：故障原因 + 处置措施",
            "使用规则": "合并原因和措施；如果处置措施已经包含原因，不重复拼接。",
        },
        {
            "字段": "故障地点",
            "生成结果": str(row.get("故障地点", "")),
            "来源字段": "设备维修单：故障描述 / 设备桩号 / 方向",
            "使用规则": "优先识别故障描述中的 YK/ZK 桩号；否则回退到设备桩号和方向。",
        },
    ]
