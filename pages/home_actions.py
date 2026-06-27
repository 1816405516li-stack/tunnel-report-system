"""Home-page actions and small UI helpers."""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime
import os
from pathlib import Path

import streamlit as st

from config.settings import OUTPUTS_DIR, RESOURCES_DIR, WORKSPACE_DIR
from core.repair_orders import PipelineResult, load_tunnel_codes, process_device_repair_workbook
from generators.monthly_report import (
    CATEGORY_LABELS,
    DEFAULT_CATEGORIES,
    MonthlyGenerationError,
    generate_monthly_reports,
)


UPLOAD_DIR = WORKSPACE_DIR / "uploads"
PROCESSED_DIR = WORKSPACE_DIR / "processed"
TUNNEL_MAPPING_PATH = RESOURCES_DIR / "mappings" / "tunnels.json"


def html(block: str) -> None:
    st.markdown(block, unsafe_allow_html=True)


def show_placeholder(name: str) -> None:
    st.toast(f"{name}：功能开发中", icon="ℹ️")


def native_button(label: str, key: str, toast: bool = True, width: str = "stretch") -> bool:
    if st.button(label, key=key, width=width):
        if toast:
            show_placeholder(label)
        return True
    return False


def process_uploaded_fault_file(uploaded_file) -> dict:
    """Save uploaded Excel and run the real repair-order preparation pipeline."""
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = Path(uploaded_file.name).name
    source_path = UPLOAD_DIR / f"{datetime.now():%Y%m%d_%H%M%S}_{safe_name}"
    source_path.write_bytes(uploaded_file.getvalue())
    tunnel_codes = load_tunnel_codes(TUNNEL_MAPPING_PATH)
    result: PipelineResult = process_device_repair_workbook(
        source_path,
        PROCESSED_DIR,
        tunnel_codes=tunnel_codes,
    )
    st.session_state.pop("monthly_generation_result", None)
    return asdict(result)


def get_fault_result() -> dict | None:
    return st.session_state.get("fault_pipeline_result")


def get_monthly_generation_result(fault_result: dict | None = None) -> dict | None:
    return st.session_state.get("monthly_generation_result")


def format_upload_size(uploaded_file) -> str:
    size = getattr(uploaded_file, "size", None)
    if size is None:
        size = len(uploaded_file.getvalue())
    if size >= 1024 * 1024:
        return f"{size / 1024 / 1024:.2f} MB"
    if size >= 1024:
        return f"{size / 1024:.1f} KB"
    return f"{size} B"


def show_upload_feedback(uploaded_file, label: str, next_step: str = "请点击“开始解析”继续。") -> None:
    if not uploaded_file:
        return
    safe_name = Path(uploaded_file.name).name
    st.success(f"{label}已选择：{safe_name}（{format_upload_size(uploaded_file)}）。{next_step}")


def run_monthly_generation(fault_result: dict, categories: tuple[str, ...]) -> dict | None:
    """Generate monthly files and keep Streamlit progress tied to real tasks."""
    progress_holder = st.empty()
    message_holder = st.empty()
    progress_holder.progress(0)
    message_holder.caption("准备生成月报文件...")

    def update_progress(completed: int, total: int, message: str) -> None:
        percent = int(completed / total * 100) if total else 0
        progress_holder.progress(min(percent, 100))
        message_holder.caption(f"{message}（{completed}/{total}）")

    try:
        result = generate_monthly_reports(
            fault_result,
            OUTPUTS_DIR,
            categories=categories,
            progress_callback=update_progress,
        ).to_dict()
    except MonthlyGenerationError as exc:
        progress_holder.progress(0)
        message_holder.empty()
        st.error(str(exc))
        return None
    except Exception as exc:  # pragma: no cover - Streamlit needs a readable fallback.
        progress_holder.progress(0)
        message_holder.empty()
        st.error(f"月报生成失败：{exc}")
        return None

    st.session_state["monthly_generation_result"] = result
    st.success("月报文件已生成并通过打开校验。")
    return result


def render_generation_progress_box(result: dict | None) -> None:
    completed = int(result.get("completed", 0)) if result else 0
    total = int(result.get("total", 0)) if result else 0
    percent = int(completed / total * 100) if total else 0
    generated_at = result.get("generated_at", "暂无") if result else "暂无"
    output_dir = result.get("output_dir", "等待生成") if result else "等待生成"
    status = "生成完成" if percent == 100 and result else "等待生成"
    html(
        f"""
        <div class="generation-box">
            <div class="generate-head">
                <div>
                    <div class="progress-label notranslate" translate="no">生成进度</div>
                    <div style="font-weight:800;">当前状态：{status}</div>
                </div>
                <div class="percent red">{percent}%</div>
            </div>
            <div class="bar" style="margin-top:7px;"><span style="width:{percent}%;"></span></div>
            <div style="color:#6b7280;font-size:14px;margin-top:7px;">已完成：{completed} / {total} 个生成任务</div>
            <div style="color:#6b7280;font-size:13px;margin-top:4px;">最近生成：{generated_at}</div>
            <div style="color:#6b7280;font-size:13px;margin-top:4px;word-break:break-all;">输出目录：{output_dir}</div>
        </div>
        """
    )


def render_generation_stats(result: dict | None) -> None:
    if not result:
        html('<div style="color:#6b7280;font-size:14px;">暂无生成结果，请先点击上方生成按钮。</div>')
        return
    stats = result.get("category_stats") or {}
    rows = []
    for category in DEFAULT_CATEGORIES:
        item = stats.get(category)
        label = CATEGORY_LABELS[category]
        if item:
            rows.append(
                f"<div class='dataset-item'><span class='check'>✓</span>"
                f"<div>{label}：{item.get('file_count', 0)} 个文件，{item.get('row_count', 0)} 行数据</div></div>"
            )
        else:
            rows.append(f"<div class='dataset-item'><span>•</span><div>{label}：未生成</div></div>")
    html(f"<div class='dataset-list'>{''.join(rows)}</div>")


def render_open_result_folder_button(result: dict | None) -> None:
    path_text = result.get("output_dir") if result else None
    path = Path(path_text).resolve() if path_text else None
    enabled = bool(path and path.exists() and path.is_dir())
    if st.button("跳转到文件位置", key="open_monthly_result_folder", disabled=not enabled, width="stretch"):
        try:
            os.startfile(path)  # type: ignore[attr-defined]
            st.toast("已打开生成结果文件夹。", icon="✅")
        except OSError as exc:
            st.error(f"无法打开文件夹：{exc}")
    if enabled:
        st.caption(f"生成目录：{path}")


