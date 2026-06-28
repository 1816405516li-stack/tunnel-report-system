"""Dialog routing for title-bar panels."""

from __future__ import annotations

import streamlit as st

from pages.components.home_actions import get_fault_result
from pages.components.panels.about_system import render_about_system_page
from pages.components.panels.rule_center import render_rule_center_page
from pages.components.panels.run_logs import render_run_logs_page
from pages.components.panels.standard_fault_preview import render_standard_fault_preview


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


@st.dialog("规则中心", width="large")
def rule_center_dialog() -> None:
    render_rule_center_page()
    if st.button("关闭", key="close_rule_center", width="stretch"):
        st.session_state["active_title_panel"] = None
        st.rerun()


@st.dialog("标准故障明细预览", width="large")
def standard_fault_preview_dialog() -> None:
    render_standard_fault_preview(get_fault_result())
    if st.button("关闭", key="close_standard_fault_preview", width="stretch"):
        st.session_state["active_title_panel"] = None
        st.rerun()


def render_requested_panel_dialog() -> None:
    """Open the requested dialog once, without changing the current page."""
    panel = st.session_state.pop("active_title_panel", None)
    if panel == "about-system":
        about_system_dialog()
    elif panel == "run-logs":
        run_logs_dialog()
    elif panel == "rule-center":
        rule_center_dialog()
    elif panel == "standard-fault-preview":
        standard_fault_preview_dialog()

