"""Quality checks for standardized repair-order fault rows."""

from __future__ import annotations

import re
from typing import Any

import pandas as pd


PILE_PATTERN = re.compile(r"(?:Y?K|ZK)\s*\d{1,4}\s*\+\s*\d{1,4}", re.IGNORECASE)
LONG_REASON_ACTION_LIMIT = 80


def build_quality_issues(data: pd.DataFrame) -> list[dict[str, Any]]:
    """Return non-blocking quality reminders for standardized fault rows."""
    issues: list[dict[str, Any]] = []

    def add_issue(check_name: str, mask: pd.Series, suggestion: str) -> None:
        matched = data[mask.fillna(False)]
        if matched.empty:
            return
        examples = [row_label(row, int(index)) for index, row in matched.head(5).iterrows()]
        issues.append(
            {
                "检查项": check_name,
                "数量": int(len(matched)),
                "建议": suggestion,
                "涉及记录": "；".join(examples),
            }
        )

    if "故障现象" in data.columns:
        add_issue("故障现象为空", data["故障现象"].map(is_blank), "检查原始故障描述是否缺失。")
    if "处置措施" in data.columns:
        add_issue("处置措施为空", data["处置措施"].map(is_blank), "生成前建议补充维修内容或确认处理措施。")
    if "故障地点" in data.columns:
        location_text = data["故障地点"].astype(str)
        add_issue("故障地点为空", location_text.map(is_blank), "检查故障描述、设备桩号和方向。")
        add_issue(
            "故障地点未识别到桩号",
            ~location_text.map(lambda value: bool(PILE_PATTERN.search(value))),
            "检查设备桩号或故障描述是否需要补充。",
        )
    if "设备名称" in data.columns:
        add_issue("设备名称为空", data["设备名称"].map(is_blank), "检查设备类型或设备名称字段。")
    if "修复时间" in data.columns:
        add_issue("修复时间为空", data["修复时间"].map(is_blank), "确认是否仍在处理中，或补充修复时间。")
    if "设备分类" in data.columns:
        add_issue("设备分类为空", data["设备分类"].map(is_blank), "补充设备分类判断规则。")
    if "原因及处理" in data.columns:
        reason_action = data["原因及处理"].astype(str)
        add_issue(
            "原因及处理过长",
            reason_action.str.len() > LONG_REASON_ACTION_LIMIT,
            "建议人工确认月报表达是否足够简洁。",
        )
        add_issue(
            "原因及处理疑似重复",
            reason_action.map(has_repeated_clause),
            "检查原因和处置措施是否重复拼接。",
        )
    if "源表行号" in data.columns:
        source_rows = data["源表行号"].astype(str).str.strip()
        add_issue("同一源表行号重复", source_rows.duplicated(keep=False) & source_rows.ne(""), "检查是否重复解析同一原始行。")

    duplicate_columns = ["隧道名称", "设备名称", "故障日期", "故障地点", "故障现象", "故障原因", "处置措施"]
    if all(column in data.columns for column in duplicate_columns):
        duplicate_mask = _build_exact_duplicate_mask(data, duplicate_columns)
        add_issue("疑似重复故障记录", duplicate_mask, "同隧道、同设备、同日且故障内容一致，请检查是否重复解析。")

    return issues


def is_blank(value: object) -> bool:
    return str(value or "").strip() == ""


def row_label(row: pd.Series, index: int) -> str:
    return (
        f"{preview_row_number(row.get('源表行号', ''), index)} | "
        f"{row.get('隧道名称', '')} | {row.get('设备名称', '')} | {row.get('故障日期', '')}"
    )


def preview_row_number(value: object, index: int) -> str:
    text = str(value or "").strip()
    if not text:
        return str(index + 1)
    try:
        return str(int(float(text)))
    except ValueError:
        return text


def has_repeated_clause(value: object) -> bool:
    text = str(value or "").strip()
    if not text:
        return False
    parts = [part.strip() for part in re.split(r"[，,；;。]+", text) if part.strip()]
    return len(parts) != len(set(parts))


def _build_exact_duplicate_mask(data: pd.DataFrame, columns: list[str]) -> pd.Series:
    normalized = data[columns].apply(lambda column: column.map(_normalize_duplicate_part))
    has_complete_key = normalized.ne("").all(axis=1)
    duplicate_key = normalized.agg("|".join, axis=1)
    return has_complete_key & duplicate_key.duplicated(keep=False)


def _normalize_duplicate_part(value: object) -> str:
    return re.sub(r"\s+", "", str(value or "").strip())
