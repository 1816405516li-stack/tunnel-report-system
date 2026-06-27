"""Classification and counts for repair-order faults."""

from __future__ import annotations

from datetime import datetime
from typing import Any

import pandas as pd

from core.repair_orders.text import extract_part_name, text


def classify_device(system_type: Any, device_name: str, fault_reason: Any = "", handling: Any = "") -> str:
    """Map source system/device names to report device classes."""
    system = text(system_type)
    combined = f"{system}{device_name}"
    reason_action = f"{text(fault_reason)}{text(handling)}"
    if "火灾报警" in device_name and "手报" not in reason_action:
        return "消防设施"
    if "火灾报警" in device_name and "手报" in reason_action:
        return "监控与通信设施"
    if _contains_any(combined, ["EPS", "UPS", "电力监控", "电线", "配电房", "高压柜", "低压柜", "高低压柜", "配电箱", "电缆"]):
        return "供配电设施"
    if _contains_any(combined, ["LED", "照明灯"]):
        return "照明设施"
    if _contains_any(combined, ["风机"]):
        return "通风设施"
    if _contains_any(combined, ["手动报警", "防火卷帘门", "给水", "水管", "水池", "消防"]):
        return "消防设施"
    if _contains_any(
        combined,
        [
            "电光标志",
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
    if "供配电" in system:
        return "供配电设施"
    if "通风" in system:
        return "通风设施"
    if "照明" in system:
        return "照明设施"
    if "监控" in system or "通信" in system:
        return "监控与通信设施"
    return system or "其他设施"


def _contains_any(value: str, keywords: list[str]) -> bool:
    return any(keyword in value for keyword in keywords)


def replacement_count(row: pd.Series, handling: str) -> int:
    """Return per-record replacement count using repair-order evidence."""
    replaced = text(row["是否更换设备或配件"]) if "是否更换设备或配件" in row.index else ""
    part_name = text(row["更换配件名称"]) if "更换配件名称" in row.index else ""
    handling_text = text(handling)
    if any(word in handling_text for word in ["重启", "重装合闸", "重新配置"]):
        return 0
    if replaced == "是" or part_name or "更换" in handling_text:
        return 1
    return 0


def replacement_part_name(row: pd.Series, handling: str) -> str:
    """Return replacement part name from source field or handling text."""
    part_name = text(row["更换配件名称"]) if "更换配件名称" in row.index else ""
    return part_name or extract_part_name(handling)


def fault_days(start: datetime, end: datetime | None) -> int:
    """Return inclusive fault days, minimum one day."""
    return 1
