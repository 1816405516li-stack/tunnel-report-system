"""Major visual sections for the Streamlit home page."""

from __future__ import annotations

from html import escape as escape_html
import time

import streamlit as st

from generators.monthly_report import DEFAULT_CATEGORIES
from pages.components.home_actions import (
    get_fault_result,
    get_monthly_generation_result,
    html,
    native_button,
    render_generation_progress_box,
    run_monthly_generation,
    show_placeholder,
    show_upload_feedback,
)
from pages.components.home_formatters import date_range_metric_html
from services.monthly_workflow import process_fault_upload
from utils.files import upload_fingerprint


def render_parse_progress(bar_holder, percent_holder, percent: int) -> None:
    percent = max(0, min(percent, 100))
    bar_holder.empty()
    percent_holder.empty()
    with bar_holder.container():
        html(
            f'<div style="height:40px;display:grid;align-items:center;">'
            f'<div class="bar"><span style="width:{percent}%"></span></div></div>'
        )
    with percent_holder.container():
        html(f'<div class="percent" style="height:40px;display:grid;align-items:center;text-align:right;">{percent}%</div>')


def render_title_action_bar() -> None:
    with st.container(key="hero_action_bar"):
        actions = st.columns(4, gap="small")
        with actions[0]:
            if st.button("▦\n模板管理", key="top_template_manage", width="stretch"):
                st.session_state.pop("active_title_panel", None)
                show_placeholder("模板管理")
        with actions[1]:
            if st.button("☷\n规则中心", key="top_rule_config", width="stretch"):
                st.session_state["active_title_panel"] = "rule-center"
                st.rerun()
        with actions[2]:
            if st.button("▤\n系统日志", key="top_run_logs", width="stretch"):
                st.session_state["active_title_panel"] = "run-logs"
                st.rerun()
        with actions[3]:
            if st.button("ⓘ\n关于系统", key="top_about_system", width="stretch"):
                st.session_state["active_title_panel"] = "about-system"
                st.rerun()


def render_hero_section() -> None:
    fault_result = get_fault_result()
    generation_result = get_monthly_generation_result(fault_result)
    month = (fault_result or generation_result or {}).get("month")
    month_label = str(month) if month else "待解析"
    output_label = (generation_result or {}).get("output_dir")
    if not output_label:
        output_label = f"outputs/monthly_reports/{month}" if month else "outputs/monthly_reports"
    task_label = "已生成" if generation_result else ("待生成" if fault_result else "等待解析")

    with st.container(key="hero_card"):
        header_left, header_right = st.columns([1.45, 1], gap="medium")
        with header_left:
            html(
                """
<div class="brand-row">
    <div class="brand-icon">♜</div>
    <div>
        <h1>隧道机电月报自动化系统</h1>
        <div class="subtitle">上传故障单，自动生成总月报、单隧道月报、巡查记录、检查记录及故障记录单</div>
    </div>
</div>
"""
            )
        with header_right:
            render_title_action_bar()
        html(
            f"""
<div class="status-row">
    <div class="status-pill"><span class="mini">▣</span>当前月份：{escape_html(month_label)}</div>
    <div class="status-pill"><span class="mini check">✓</span>模板状态：正常</div>
    <div class="status-pill"><span class="mini">▣</span>输出目录：{escape_html(str(output_label))}</div>
    <div class="status-pill"><span class="mini">◌</span>当前任务：{escape_html(task_label)}</div>
</div>
"""
        )


def render_monthly_sections() -> tuple[dict | None, bool]:
    with st.container(key="fault_header_card"):
        with st.container(key="fault_header_box"):
            html('<div class="module-title" style="margin-bottom:2px;height:24px;display:flex;align-items:center;"><span style="color:#743cff;">▧</span> 月报处理区</div>')
            html('<div style="min-height:6px;"></div>')
            with st.container(key="fault_uploader"):
                uploaded_fault_file = st.file_uploader("上传设备维修单 Excel", type=["xlsx", "xls"], key="fault_file")
                show_upload_feedback(uploaded_fault_file, "设备维修单")

    fault_result = get_fault_result()
    has_fault_upload = uploaded_fault_file is not None or fault_result is not None
    current_upload_fingerprint = upload_fingerprint(uploaded_fault_file)
    parsed_upload_fingerprint = st.session_state.get("fault_pipeline_upload_fingerprint")
    can_parse_fault = bool(
        current_upload_fingerprint and current_upload_fingerprint != parsed_upload_fingerprint
    )

    with st.container(key="fault_parse_card"):
        html('<div class="module-title">▧ 月报解析处理区</div>')
        with st.container(key="fault_parse_panel"):
            with st.container():
                cols = st.columns([0.16, 0.14, 0.56, 0.10], gap="small")
                with cols[0]:
                    parse_clicked = native_button(
                        "开始解析",
                        "parse_fault",
                        toast=False,
                        disabled=not can_parse_fault,
                    )
                with cols[1]:
                    html('<div class="progress-label notranslate" translate="no" style="height:40px;display:grid;align-items:center;">月报解析进度</div>')
                with cols[2]:
                    progress_value = 100 if fault_result else (25 if has_fault_upload else 0)
                    parse_bar_holder = st.empty()
                with cols[3]:
                    parse_percent_holder = st.empty()
                render_parse_progress(parse_bar_holder, parse_percent_holder, progress_value)

            if parse_clicked:
                for stage_percent in (30, 42, 55):
                    render_parse_progress(parse_bar_holder, parse_percent_holder, stage_percent)
                    time.sleep(0.12)
                with st.spinner("正在读取、清洗并整理设备维修单数据..."):
                    try:
                        fault_result = process_fault_upload(uploaded_fault_file)
                    except Exception as exc:  # pragma: no cover - Streamlit needs readable feedback.
                        st.error(f"设备维修单解析失败：{exc}")
                        return get_fault_result(), has_fault_upload
                    st.session_state["fault_pipeline_result"] = fault_result
                    st.session_state["fault_pipeline_upload_fingerprint"] = current_upload_fingerprint
                    st.session_state.pop("monthly_generation_result", None)
                for stage_percent in (72, 88, 100):
                    render_parse_progress(parse_bar_holder, parse_percent_holder, stage_percent)
                    time.sleep(0.12)
                st.toast("设备维修单解析完成，5 份中间数据已保存。", icon="✅")
                st.rerun()

            fault_result = get_fault_result()
            parsed_count = fault_result["fault_rows"] if fault_result else 0
            tunnel_count = fault_result["tunnel_count"] if fault_result else 0
            date_range_html = date_range_metric_html(fault_result, has_fault_upload)
            parse_status = "整理完成" if fault_result else ("等待解析" if has_fault_upload else "等待上传")
            status_icon = "✓" if fault_result else "◌"
            status_icon_class = "check" if fault_result else "loading"
            status_value_class = "green" if fault_result else "pending"
            html(
                f"""
                <div class="metric-grid">
                    <div class="metric-card"><div class="metric-icon">≋</div><div><div class="metric-label">已解析故障数</div><div class="metric-value">{parsed_count} 条</div></div></div>
                    <div class="metric-card"><div class="metric-icon">⌁</div><div><div class="metric-label">涉及</div><div class="metric-value">{tunnel_count} 座隧道</div></div></div>
                    <div class="metric-card date-card"><div class="metric-icon">▣</div><div><div class="metric-label">日期范围</div><div class="metric-value date-range">{date_range_html}</div></div></div>
                    <div class="metric-card"><div class="metric-icon {status_icon_class}">{status_icon}</div><div><div class="metric-label">状态</div><div class="metric-value {status_value_class}">{parse_status}</div></div></div>
                </div>
                """
            )
    return fault_result, has_fault_upload


def render_generation_sections(fault_result: dict | None) -> dict | None:
    with st.container(key="monthly_generation_card"):
        html('<div class="module-title">▧ 月报生成</div>')
        current_result = get_monthly_generation_result(fault_result)
        generation_running = bool(st.session_state.get("monthly_generation_running"))
        generation_pending = bool(st.session_state.get("monthly_generation_pending"))
        generation_locked = generation_running or generation_pending
        preview_col, generate_col = st.columns(2, gap="small")
        with preview_col:
            if st.button(
                "预览标准故障明细",
                key="preview_standard_faults",
                disabled=fault_result is None or generation_locked,
                width="stretch",
            ):
                st.session_state["active_title_panel"] = "standard-fault-preview"
                st.rerun()
        with generate_col:
            if st.button(
                "一键生成全部月报文件",
                key="gen_monthly_all",
                disabled=fault_result is None or generation_locked,
                width="stretch",
            ):
                st.session_state["monthly_generation_pending"] = True
                st.rerun()

        generation_progress_container = st.empty()
        with generation_progress_container.container():
            render_generation_progress_box(current_result)
        if generation_pending and fault_result:
            st.session_state["monthly_generation_pending"] = False
            st.session_state["monthly_generation_running"] = True
            try:
                current_result = run_monthly_generation(
                    fault_result,
                    DEFAULT_CATEGORIES,
                    progress_container=generation_progress_container,
                )
            finally:
                st.session_state["monthly_generation_running"] = False
    return get_monthly_generation_result(fault_result)
