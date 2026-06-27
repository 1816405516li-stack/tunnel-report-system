"""About page content for the tunnel monthly report system."""

from __future__ import annotations

from datetime import datetime

import streamlit as st

from config.settings import APP_NAME, OUTPUTS_DIR, RESOURCES_DIR, WORKSPACE_DIR


def render_about_system_page() -> None:
    """Render the about-system popup page."""
    st.markdown(
        f"""
        <div class="popup-page">
            <div class="popup-kicker">关于系统</div>
            <h2>{APP_NAME}</h2>
            <p>
                本系统用于整理隧道机电设备维修单、电费资料和月度模板，
                按既定规则生成总月报、单隧道月报、日常巡查记录、经常性检查记录和设备故障记录单。
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    overview = {
        "当前版本": "月报生成基础版",
        "运行日期": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "模板目录": str(RESOURCES_DIR / "templates"),
        "工作目录": str(WORKSPACE_DIR),
        "输出目录": str(OUTPUTS_DIR),
    }
    st.table(overview)

    st.markdown("#### 模块范围")
    st.markdown(
        "- 故障维修单解析、清洗、标准化\n"
        "- 月报模板规则加载与生成\n"
        "- 总表、单隧道表、日常表、经常表、故障记录单输出\n"
        "- 电费资料入口与后续电费统计扩展"
    )

    st.markdown("#### 结构原则")
    st.markdown(
        "- `core` 负责数据读取、清洗、校验和通用规则\n"
        "- `generators` 负责各类月报文件生成\n"
        "- `resources` 保存模板、规则和映射数据\n"
        "- `workspace` 保存本次处理过程文件\n"
        "- `outputs` 保存最终生成成果"
    )
