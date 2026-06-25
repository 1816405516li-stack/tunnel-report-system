"""Tunnel report system entry point."""

import streamlit as st


st.set_page_config(
    page_title="隧道机电月报系统",
    page_icon="📊",
    layout="wide",
)

st.title("隧道机电月报系统")
st.caption("上传每月资料，整理数据，并按模板生成隧道机电维护相关 Excel 文件。")

st.subheader("当前阶段")
st.info("项目结构已搭建。本阶段只保留页面和处理模块占位，暂不实现具体业务逻辑。")

st.subheader("后续功能")
st.markdown(
    """
- 上传初始故障单、隧道账单表、往月电费表等来源文件
- 清洗、校验、标准化并拆分隧道月度数据
- 生成总月报、单独隧道月报、日常巡查、经常性检查、故障记录单
- 生成当月电费表
- 读取长期复用的模板、规则、映射表和依据文件
"""
)
