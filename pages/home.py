"""Streamlit home page for the tunnel monthly report automation system."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from generators.monthly_report import DEFAULT_CATEGORIES
from pages.about_system import render_about_system_page
from pages.run_logs import render_run_logs_page
from pages.home_formatters import date_range_metric_html
from pages.home_actions import (
    get_fault_result,
    get_monthly_generation_result,
    html,
    native_button,
    process_uploaded_fault_file,
    render_generation_progress_box,
    render_generation_stats,
    render_open_result_folder_button,
    run_monthly_generation,
    show_placeholder,
    show_upload_feedback,
)
from pages.home_styles import CSS



MONTHLY_GENERATION_ACTIONS = [
    ("total", "生成总月报表"),
    ("single_tunnel", "生成单隧道月报表"),
    ("daily", "生成日常巡查记录表"),
    ("frequent", "生成经常性检查记录表"),
    ("fault_record", "生成设备故障记录单"),
    ("all", "一键生成全部月报文件"),
]


def render_flow(result: dict | None, has_upload: bool) -> None:
    if result:
        states = [
            ("1", "上传文件", "已完成", "done", "✓"),
            ("2", "解析数据", "已完成", "done", "✓"),
            ("3", "清洗数据", "已完成", "done", "✓"),
            ("4", "整理数据", "已完成", "done", "✓"),
        ]
    elif has_upload:
        states = [
            ("1", "上传文件", "已完成", "done", "✓"),
            ("2", "解析数据", "待开始", "todo", "◴"),
            ("3", "清洗数据", "未开始", "todo", "⌛"),
            ("4", "整理数据", "未开始", "todo", "⇩"),
        ]
    else:
        states = [
            ("1", "上传文件", "等待上传", "active", "◌"),
            ("2", "解析数据", "未开始", "todo", "◴"),
            ("3", "清洗数据", "未开始", "todo", "⌛"),
            ("4", "整理数据", "未开始", "todo", "⇩"),
        ]

    step_html = []
    for index, (num, name, status, css, icon) in enumerate(states):
        step_html.append(
            f'<div class="step {css}"><div class="num">{num}</div>'
            f'<div><div class="step-name">{name}</div><div class="step-status">{status}</div></div>'
            f'<div class="check">{icon}</div></div>'
        )
        if index < len(states) - 1:
            step_html.append('<div class="arrow">›</div>')

    html(
        f"""
<section class="flow-card">
    <div class="module-title" style="margin-bottom:12px;color:#171717;"><span style="color:#743cff;">⌘</span> 当前处理流程</div>
    <div class="flow-grid">
        {''.join(step_html)}
    </div>
</section>
"""
    )


def render_dataset_outputs(result: dict | None) -> None:
    if result:
        rows = "".join(
            f"<div class='dataset-item'><span class='check'>✓</span><div>{name}：{Path(path).name}</div></div>"
            for name, path in result["files"].items()
            if name
            in {
                "机电设施故障月报表_总表_数据",
                "机电设施故障月报表_分隧道表_数据",
                "机电日常巡查记录表_数据",
                "机电经常性检查记录表_数据",
                "隧道机电设备故障记录单_数据",
            }
        )
        rows_html = f"<div class='dataset-list'>{rows}</div>"
        dir_html = f"<div class='dataset-dir'>保存目录：{result['processed_dir']}</div>"
        body_html = f"<div class='dataset-strip'>{rows_html}{dir_html}</div>"
    else:
        body_html = "<span style='color:#6b7280;'>• 暂无中间数据，请先完成解析。</span>"

    html(
        f"""
<section class="flow-card">
    <div class="module-title" style="margin-bottom:12px;color:#171717;"><span style="color:#743cff;">⌘</span> 当前生成中间数据</div>
    {body_html}
</section>
"""
    )


def init_page_state() -> None:
    if "power_price_confirmed" not in st.session_state:
        st.session_state["power_price_confirmed"] = 0.85
    if "power_price_input" not in st.session_state:
        st.session_state["power_price_input"] = st.session_state["power_price_confirmed"]
    if "active_title_panel" not in st.session_state:
        st.session_state["active_title_panel"] = None


@st.dialog("关于系统", width="large")
def about_system_dialog() -> None:
    render_about_system_page()
    if st.button("关闭", key="close_about_system", width="stretch"):
        st.session_state["active_title_panel"] = None
        st.rerun()


@st.dialog("系统日志", width="large")
def run_logs_dialog() -> None:
    render_run_logs_page()
    if st.button("关闭", key="close_run_logs", width="stretch"):
        st.session_state["active_title_panel"] = None
        st.rerun()


def render_requested_panel_dialog() -> None:
    panel = st.session_state.pop("active_title_panel", None)
    if panel == "about-system":
        about_system_dialog()
    elif panel == "run-logs":
        run_logs_dialog()


def render_title_action_bar() -> None:
    with st.container(key="hero_action_bar"):
        actions = st.columns(4, gap="small")
        with actions[0]:
            if st.button("▦\n模板管理", key="top_template_manage", width="stretch"):
                st.session_state.pop("active_title_panel", None)
                show_placeholder("模板管理")
        with actions[1]:
            if st.button("☷\n规则配置", key="top_rule_config", width="stretch"):
                st.session_state.pop("active_title_panel", None)
                show_placeholder("规则配置")
        with actions[2]:
            if st.button("▤\n系统日志", key="top_run_logs", width="stretch"):
                st.session_state["active_title_panel"] = "run-logs"
                st.rerun()
        with actions[3]:
            if st.button("ⓘ\n关于系统", key="top_about_system", width="stretch"):
                st.session_state["active_title_panel"] = "about-system"
                st.rerun()


def render_hero_section() -> None:
    with st.container(key="hero_card"):
        header_left, header_right = st.columns([1.45, 1], gap="medium")
        with header_left:
            html(
                """
<div class="brand-row">
    <div class="brand-icon">♜</div>
    <div>
        <h1>隧道机电月报自动化系统</h1>
        <div class="subtitle">上传故障单、电费账单，自动生成总月报、单隧道月报、巡查记录、检查记录及电费统计表</div>
    </div>
</div>
"""
            )
        with header_right:
            render_title_action_bar()
        html(
            """
<div class="status-row">
    <div class="status-pill"><span class="mini">▣</span>当前月份：2026年6月</div>
    <div class="status-pill"><span class="mini check">✓</span>模板状态：正常</div>
    <div class="status-pill"><span class="mini">▣</span>输出目录：outputs/2026-06</div>
    <div class="status-pill"><span class="mini">◴</span>当前任务：等待生成</div>
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

    with st.container(key="fault_parse_card"):
        html('<div class="module-title">▧ 月报解析处理区</div>')
        with st.container(key="fault_parse_panel"):
            with st.container():
                cols = st.columns([0.22, 0.16, 0.50, 0.12], gap="small")
                with cols[0]:
                    parse_clicked = native_button("开始解析", "parse_fault", toast=False)
                with cols[1]:
                    html('<div class="progress-label notranslate" translate="no" style="height:40px;display:grid;align-items:center;">月报解析进度</div>')
                with cols[2]:
                    progress_value = 100 if fault_result else (25 if has_fault_upload else 0)
                    html(f'<div style="height:40px;display:grid;align-items:center;"><div class="bar"><span style="width:{progress_value}%"></span></div></div>')
                with cols[3]:
                    html(f'<div class="percent" style="height:40px;display:grid;align-items:center;text-align:right;">{progress_value}%</div>')

            if parse_clicked:
                if not uploaded_fault_file:
                    st.warning("请先上传设备维修单 Excel。")
                else:
                    with st.spinner("正在读取、清洗并整理设备维修单数据..."):
                        fault_result = process_uploaded_fault_file(uploaded_fault_file)
                        st.session_state["fault_pipeline_result"] = fault_result
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
                    <div class="metric-card"><div class="metric-icon">≡</div><div><div class="metric-label">已解析故障数</div><div class="metric-value">{parsed_count} 条</div></div></div>
                    <div class="metric-card"><div class="metric-icon">⌂</div><div><div class="metric-label">涉及</div><div class="metric-value">{tunnel_count} 座隧道</div></div></div>
                    <div class="metric-card date-card"><div class="metric-icon">▣</div><div><div class="metric-label">日期范围</div><div class="metric-value date-range">{date_range_html}</div></div></div>
                    <div class="metric-card"><div class="metric-icon {status_icon_class}">{status_icon}</div><div><div class="metric-label">状态</div><div class="metric-value {status_value_class}">{parse_status}</div></div></div>
                </div>
                """
            )
    return fault_result, has_fault_upload


def render_power_sections() -> None:
    with st.container(key="power_header_card"):
        with st.container(key="power_header_box"):
            with st.container():
                header_row = st.columns([0.36, 0.22, 0.10, 0.32], gap="small")
                with header_row[0]:
                    html('<div class="module-title" style="color:#171717;margin-bottom:2px;height:24px;display:inline-flex;align-items:center;"><span style="color:#5a39ff;">ϟ</span> 电费处理区</div>')
                with header_row[1]:
                    with st.container():
                        st.number_input(
                            "本月电费单价（元/度）",
                            min_value=0.0,
                            step=0.01,
                            format="%.2f",
                            key="power_price_input",
                            label_visibility="collapsed",
                        )
                with header_row[2]:
                    with st.container():
                        confirm_price = native_button("确定", "confirm_power_price", toast=False)
                with header_row[3]:
                    html(f'<div class="value-badge" style="margin-left:auto;justify-content:flex-start;padding-left:0;border:none;background:transparent;box-shadow:none;width:100%;text-align:left;">当前单价：{st.session_state["power_price_confirmed"]:.2f} 元/度</div>')
            with st.container():
                up1, up2 = st.columns(2, gap="small")
                with up1:
                    with st.container(key="power_uploader_last_month_table"):
                        last_month_table = st.file_uploader(
                            "上传上月电费表",
                            type=["xlsx", "xls", "pdf"],
                            key="last_month_table",
                            label_visibility="collapsed",
                        )
                        show_upload_feedback(last_month_table, "上月电费表", "电费解析功能接入后即可继续处理。")
                with up2:
                    with st.container(key="power_uploader_this_month_bill"):
                        this_month_bill = st.file_uploader(
                            "上传本月账单",
                            type=["xlsx", "xls", "pdf"],
                            key="this_month_bill",
                            label_visibility="collapsed",
                        )
                        show_upload_feedback(this_month_bill, "本月账单", "电费解析功能接入后即可继续处理。")
            if confirm_price:
                st.session_state["power_price_confirmed"] = float(st.session_state["power_price_input"])
                st.toast(f'本月电费单价已更新为 {st.session_state["power_price_confirmed"]:.2f} 元/度', icon="✅")
                st.rerun()

    with st.container(key="power_parse_card"):
        html('<div class="module-title" style="color:#171717;"><span style="color:#5a39ff;">ϟ</span> 电费解析处理区</div>')
        with st.container(key="power_parse_panel"):
            has_power_upload = bool(st.session_state.get("last_month_table") or st.session_state.get("this_month_bill"))
            power_progress_value = 25 if has_power_upload else 0
            power_status = "等待解析" if has_power_upload else "等待上传"
            with st.container():
                e1, e2, e3, e4 = st.columns([0.22, 0.16, 0.50, 0.12], gap="small")
                with e1:
                    native_button("开始解析", "parse_power")
                with e2:
                    html('<div class="progress-label notranslate" translate="no" style="height:40px;display:grid;align-items:center;">电费解析进度</div>')
                with e3:
                    html(f'<div style="height:40px;display:grid;align-items:center;"><div class="bar"><span style="width:{power_progress_value}%"></span></div></div>')
                with e4:
                    html(f'<div class="percent" style="height:40px;display:grid;align-items:center;text-align:right;">{power_progress_value}%</div>')
            html(
                f"""
                <div class="metric-grid">
                    <div class="metric-card"><div class="metric-icon check">ϟ</div><div><div class="metric-label">本月总用电量</div><div class="metric-value">待解析</div></div></div>
                    <div class="metric-card"><div class="metric-icon" style="color:#6d37ff;">￥</div><div><div class="metric-label">本月电费金额</div><div class="metric-value">待解析</div></div></div>
                    <div class="metric-card"><div class="metric-icon" style="color:#f97316;">♨</div><div><div class="metric-label">上月电费金额</div><div class="metric-value">待解析</div></div></div>
                    <div class="metric-card"><div class="metric-icon trend">↗</div><div><div class="metric-label">状态</div><div class="metric-value green">{power_status}</div></div></div>
                </div>
                """
            )


def render_generation_sections(fault_result: dict | None) -> dict | None:
    html('<div class="lower-sections">')
    lower_left, lower_right = st.columns([1, 1], gap="small")

    with lower_left:
        with st.container(key="monthly_generation_card"):
            html('<div class="module-title">▧ 月报生成</div>')
            current_result = get_monthly_generation_result(fault_result)
            selected_action: tuple[str, ...] | None = None
            button_rows = [MONTHLY_GENERATION_ACTIONS[:3], MONTHLY_GENERATION_ACTIONS[3:]]
            for button_row in button_rows:
                cols = st.columns(3, gap="small")
                for col, (category, label) in zip(cols, button_row):
                    with col:
                        clicked = st.button(
                            label,
                            key=f"gen_monthly_{category}",
                            disabled=fault_result is None,
                            width="stretch",
                        )
                        if clicked:
                            selected_action = DEFAULT_CATEGORIES if category == "all" else (category,)

            if selected_action:
                current_result = run_monthly_generation(fault_result, tuple(selected_action)) if fault_result else None

            render_generation_progress_box(current_result)
            html('<div class="summary-title">生成预览</div>')
            render_generation_stats(current_result)
            html('<div class="summary-title">生成结果</div>')
            render_open_result_folder_button(current_result)
    with lower_right:
        html(
            """
            <div class="soft-card lower-card">
                <div class="module-title"><span style="color:#5a39ff;">ϟ</span> 电费生成</div>
                <div class="electric-grid">
                    <div class="inner-panel">
                        <div class="summary-title">生成流程状态</div>
                        <div class="timeline">
                            <div class="timeline-item"><span class="dot"></span>待读取账单</div>
                            <div class="timeline-item"><span class="dot"></span>待计算用电量</div>
                            <div class="timeline-item"><span class="dot"></span>待套用电费单价</div>
                            <div class="timeline-item"><span class="dot"></span>待生成电费表</div>
                            <div class="timeline-item"><span class="dot"></span>生成完成</div>
                        </div>
                    </div>
                    <div>
                        <div class="inner-panel" style="margin-bottom:10px;">
                            <div class="generate-head">
                                <div class="summary-title">电费生成进度</div>
                                <div class="percent red" style="font-size:20px;">0%</div>
                            </div>
                            <div class="bar" style="margin:8px 0;"><span style="width:0%;"></span></div>
                            <div style="color:#6b7280;font-size:14px;">已完成：0 / 3 个任务</div>
                        </div>
                        <div class="inner-panel">
                            <div class="summary-title">当前输出</div>
                            <div class="output-lines">
                                文件名称：待生成<br>
                                生成时间：暂无<br>
                                状态：等待生成
                            </div>
                        </div>
                    </div>
                    <div class="electric-action">
                        <button class="large-main" onclick="alert('生成本月电费表：功能开发中')">生成本月电费表</button>
                    </div>
                </div>
            </div>
            """
        )
    html("</div>")
    return get_monthly_generation_result(fault_result)


def render_result_preview_section(fault_result: dict | None, monthly_generation_result: dict | None) -> None:
    stats = (monthly_generation_result or {}).get("category_stats") or {}
    parsed_status = "已整理待生成" if fault_result else "待整理"

    def monthly_status_for(category: str) -> str:
        item = stats.get(category)
        if item:
            return f"已生成 {item.get('file_count', 0)} 个文件"
        return parsed_status

    monthly_status = monthly_status_for("total")
    single_count = monthly_status_for("single_tunnel")
    daily_status = monthly_status_for("daily")
    frequent_status = monthly_status_for("frequent")
    record_status = monthly_status_for("fault_record")
    if not monthly_generation_result and fault_result:
        record_status = f"已整理 {fault_result['fault_rows']} 条故障记录，待生成"
    last_time = (monthly_generation_result or {}).get("generated_at") or ("已恢复最近解析结果" if fault_result else "暂无")

    html(
        f"""
<section class="result-card">
    <div class="module-title">◴ 生成结果预览</div>
    <div class="result-grid">
        <div class="result-box monthly">
            <div class="result-title">月报输出结果</div>
            <div class="result-list">
                <div><span class="check">✓</span> 总月报表数据：{monthly_status}</div>
                <div><span class="check">✓</span> 日常巡查记录表数据：{daily_status}</div>
                <div><span class="check">✓</span> 单隧道月报表数据：{single_count}</div>
                <div><span class="check">✓</span> 经常性检查记录表数据：{frequent_status}</div>
                <div><span class="check">✓</span> 设备故障记录单数据：{record_status}</div>
            </div>
            <div class="stamp">▧</div>
        </div>
        <div class="result-box power">
            <div class="result-title">电费输出结果</div>
            <div class="result-list" style="grid-template-columns:1fr;">
                <div><span class="check">✓</span> 本月电费表：待处理</div>
            </div>
            <div class="stamp">¥</div>
        </div>
    </div>
    <div class="last-time">◷ 最近一次月报结果时间：{last_time}</div>
</section>
"""
    )


def main() -> None:
    st.set_page_config(
        page_title="隧道机电月报自动化系统",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    html(CSS)
    init_page_state()
    render_requested_panel_dialog()
    render_hero_section()

    left, right = st.columns([1, 1], gap="small")
    with left:
        fault_result, has_fault_upload = render_monthly_sections()
    with right:
        render_power_sections()

    render_dataset_outputs(fault_result)
    render_flow(fault_result, has_fault_upload)
    monthly_generation_result = render_generation_sections(fault_result)
    render_result_preview_section(fault_result, monthly_generation_result)


if __name__ == "__main__":
    main()
