"""Prepared data review page."""

import pandas as pd
import streamlit as st

from config.settings import WORKSPACE_DIR


CLEANED_DIR = WORKSPACE_DIR / "cleaned"


st.title("数据准备")

cleaned_files = sorted(CLEANED_DIR.glob("*_standard.csv"), reverse=True)

if not cleaned_files:
    st.info("还没有标准化中间表。请先到“上传资料”页面上传并保存一份来源文件。")
    st.stop()

selected_file = st.selectbox(
    "选择标准化中间表",
    cleaned_files,
    format_func=lambda path: path.name,
)

data = pd.read_csv(selected_file)

st.caption(f"文件：{selected_file}")
st.metric("记录数", len(data))
st.dataframe(data, use_container_width=True, hide_index=True)
