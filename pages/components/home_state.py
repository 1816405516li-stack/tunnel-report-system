"""Session state and style loading for the Streamlit home page."""

from __future__ import annotations

import importlib

import streamlit as st

from pages.styles import home_styles


UI_STATE_VERSION = "2026-06-28-standard-fault-preview-dialog-v1"
STALE_UI_KEYS = (
    "rule_center_field_source_table",
    "rule_center_field_source_table_v2",
    "show_standard_fault_preview",
    "gen_monthly_total",
    "gen_monthly_single_tunnel",
    "gen_monthly_daily",
    "gen_monthly_frequent",
    "gen_monthly_fault_record",
    "monthly_generation_pending",
    "monthly_generation_running",
)


def current_css() -> str:
    """Reload CSS during Streamlit reruns so style edits show immediately."""
    return importlib.reload(home_styles).CSS


def init_page_state() -> None:
    """Initialize and clean stale UI-only state."""
    if st.session_state.get("_ui_state_version") != UI_STATE_VERSION:
        for key in STALE_UI_KEYS:
            st.session_state.pop(key, None)
        st.session_state["_ui_state_version"] = UI_STATE_VERSION
    if "active_title_panel" not in st.session_state:
        st.session_state["active_title_panel"] = None

