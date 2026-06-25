"""Source file upload and first-pass preparation page."""

from datetime import datetime

import pandas as pd
import streamlit as st

from config.settings import WORKSPACE_DIR
from core.cleaners import clean_fault_data
from core.importers import list_excel_sheets, load_source_file
from core.normalizers import normalize_fault_fields
from core.validators import validate_month_data


UPLOAD_DIR = WORKSPACE_DIR / "uploads"
CLEANED_DIR = WORKSPACE_DIR / "cleaned"


st.title("上传资料")

uploaded_file = st.file_uploader(
    "选择初始故障单",
    type=["xlsx", "xls", "xlsm", "csv"],
)

if not uploaded_file:
    st.info("上传一份 Excel 或 CSV 后，系统会先生成可复核的标准化中间表。")
    st.stop()

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
CLEANED_DIR.mkdir(parents=True, exist_ok=True)

source_path = UPLOAD_DIR / uploaded_file.name
source_path.write_bytes(uploaded_file.getvalue())

sheet_name = 0
if source_path.suffix.lower() in {".xls", ".xlsx", ".xlsm"}:
    sheets = list_excel_sheets(source_path)
    sheet_name = st.selectbox("选择工作表", sheets)

raw_data = load_source_file(source_path, sheet_name=sheet_name)
clean_data = clean_fault_data(raw_data)
standard_data, matched_columns = normalize_fault_fields(clean_data)
issues = validate_month_data(standard_data)

st.subheader("字段识别")
mapping_rows = [
    {"标准字段": field, "来源字段": source_column}
    for field, source_column in matched_columns.items()
]
if mapping_rows:
    st.dataframe(pd.DataFrame(mapping_rows), use_container_width=True, hide_index=True)
else:
    st.warning("未识别到常用故障字段，请检查表头是否在第一行。")

st.subheader("标准化预览")
st.dataframe(standard_data.head(100), use_container_width=True, hide_index=True)

st.subheader("校验结果")
if issues:
    issue_rows = [issue.__dict__ for issue in issues]
    st.dataframe(pd.DataFrame(issue_rows), use_container_width=True, hide_index=True)
else:
    st.success("未发现基础字段问题。")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
cleaned_name = f"{source_path.stem}_{timestamp}_standard.csv"
cleaned_path = CLEANED_DIR / cleaned_name
csv_bytes = standard_data.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")

st.download_button(
    "下载标准化中间表",
    data=csv_bytes,
    file_name=cleaned_name,
    mime="text/csv",
)

if st.button("保存到工作区", type="primary"):
    cleaned_path.write_bytes(csv_bytes)
    st.success(f"已保存：{cleaned_path}")
