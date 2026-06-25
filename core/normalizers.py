"""Normalize source fields into the system field schema."""

import pandas as pd


FIELD_ALIASES = {
    "tunnel_name": ["隧道", "隧道名称", "所属隧道", "线路名称"],
    "pile_number": ["桩号", "位置", "故障位置", "具体位置", "安装位置"],
    "fault_time": ["故障时间", "发生时间", "报修时间", "发现时间", "故障日期"],
    "repair_time": ["修复时间", "恢复时间", "完成时间", "处理时间"],
    "device_name": ["设备", "设备名称", "设施名称", "故障设备", "机电设备"],
    "fault_description": ["故障描述", "故障现象", "故障内容", "问题描述", "异常情况"],
    "handling_measure": ["处理措施", "处置措施", "维修情况", "处理情况", "修复措施"],
    "fault_count": ["故障数量", "设备数量", "故障设备数"],
    "replacement_count": ["更换数量", "更换数", "更换设备数", "备件数量"],
}


def normalize_fault_fields(clean_data):
    """Map common source columns to the system fault schema."""
    matched_columns = _match_columns(clean_data.columns)
    normalized = pd.DataFrame()
    normalized["source_row"] = clean_data.get("source_row", clean_data.index + 2)

    for field in FIELD_ALIASES:
        source_column = matched_columns.get(field)
        normalized[field] = clean_data[source_column] if source_column else pd.NA

    normalized["fault_time"] = pd.to_datetime(normalized["fault_time"], errors="coerce")
    normalized["repair_time"] = pd.to_datetime(normalized["repair_time"], errors="coerce")
    normalized["fault_count"] = pd.to_numeric(normalized["fault_count"], errors="coerce")
    normalized["replacement_count"] = pd.to_numeric(normalized["replacement_count"], errors="coerce")

    return normalized, matched_columns


def _match_columns(columns):
    normalized_names = {_normalize_name(column): column for column in columns}
    matches = {}

    for field, aliases in FIELD_ALIASES.items():
        for alias in aliases:
            alias_key = _normalize_name(alias)
            if alias_key in normalized_names:
                matches[field] = normalized_names[alias_key]
                break
        if field in matches:
            continue
        for column_key, original_column in normalized_names.items():
            if any(_should_use_partial_match(alias, column_key) for alias in aliases):
                matches[field] = original_column
                break

    return matches


def _normalize_name(value):
    return str(value).replace(" ", "").replace("_", "").replace("-", "").lower()


def _should_use_partial_match(alias, column_key):
    alias_key = _normalize_name(alias)
    return len(alias_key) > 2 and alias_key in column_key
