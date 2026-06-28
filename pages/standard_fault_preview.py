"""Standard-fault preview and field-trace popup UI."""

from __future__ import annotations

import streamlit as st

from core.repair_orders.preview import build_trace_rows, load_standard_faults_preview, visible_preview_columns
from core.repair_orders.quality import build_quality_issues, row_label


def render_standard_fault_preview(fault_result: dict | None) -> None:
    """Render standard fault rows, quality reminders, and field tracing."""
    data = load_standard_faults_preview(fault_result)
    if data.empty:
        st.info("暂无标准故障明细，请先完成设备维修单解析。")
        return

    render_standard_fault_quality_alerts(data)
    st.markdown('<div class="summary-title" style="margin-top:10px;">标准故障明细</div>', unsafe_allow_html=True)
    st.dataframe(data[visible_preview_columns(data)], width="stretch", hide_index=True)

    st.markdown('<div class="summary-title" style="margin-top:10px;">字段追溯</div>', unsafe_allow_html=True)
    row_options = [row_label(row, int(index)) for index, row in data.iterrows()]
    selected_row = st.selectbox(
        "选择要追溯的故障记录",
        list(range(len(row_options))),
        format_func=lambda index: row_options[index],
        key="standard_fault_trace_row",
    )
    st.dataframe(build_trace_rows(data.iloc[int(selected_row)]), width="stretch", hide_index=True)


def render_standard_fault_quality_alerts(data) -> None:
    st.markdown('<div class="summary-title">字段差异/异常提醒</div>', unsafe_allow_html=True)
    issues = build_quality_issues(data)
    if not issues:
        st.success("未发现明显字段异常，可以继续查看明细或生成月报。")
        return

    total_count = sum(int(item["数量"]) for item in issues)
    st.warning(f"发现 {len(issues)} 类提醒，涉及 {total_count} 项记录命中。请生成前重点查看。")
    st.dataframe(issues, width="stretch", hide_index=True)
