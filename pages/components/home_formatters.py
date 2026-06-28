"""Pure formatting helpers for the Streamlit home page."""

from __future__ import annotations

from datetime import datetime


def format_metric_date(value: object) -> str:
    if not value:
        return ""
    text = str(value).strip()
    if not text:
        return ""
    try:
        return datetime.fromisoformat(text).strftime("%Y-%m-%d")
    except ValueError:
        return text[:10]


def date_range_metric_html(fault_result: dict | None, has_upload: bool) -> str:
    if not fault_result:
        if has_upload:
            return '<span class="date-main pending">已选择文件</span><span class="metric-hint">点击开始解析后更新</span>'
        return '<span class="date-main pending">待上传</span><span class="metric-hint">上传维修单后解析</span>'

    date_start = format_metric_date(fault_result.get("date_start"))
    date_end = format_metric_date(fault_result.get("date_end"))
    if date_start and date_end:
        if date_start == date_end:
            range_text = date_start
        else:
            range_text = f'{date_start}<span class="date-separator">至</span>{date_end}'
    else:
        range_text = "日期待确认"

    return f'<span class="date-main">{range_text}</span>'
