"""Streamlit home page for the tunnel monthly report automation system."""

from __future__ import annotations

import streamlit as st

from pages.components.home_actions import html
from pages.components.home_dialogs import render_requested_panel_dialog
from pages.components.home_results import render_dataset_outputs, render_result_preview_section
from pages.components.home_sections import (
    render_generation_sections,
    render_hero_section,
    render_monthly_sections,
)
from pages.components.home_state import current_css, init_page_state


def main() -> None:
    st.set_page_config(
        page_title="隧道机电月报自动化系统",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    html(current_css())
    init_page_state()
    render_requested_panel_dialog()
    render_hero_section()

    fault_result, _ = render_monthly_sections()

    render_dataset_outputs(fault_result)
    monthly_generation_result = render_generation_sections(fault_result)
    render_result_preview_section(monthly_generation_result)


if __name__ == "__main__":
    main()
