"""Home-page actions and small UI helpers."""

from __future__ import annotations

import os
from pathlib import Path

import streamlit as st

from generators.monthly_report import MonthlyGenerationError
from services.monthly_workflow import generate_monthly_report_files
from utils.files import format_file_size, safe_file_name, upload_size


def html(block: str) -> None:
    st.markdown(block, unsafe_allow_html=True)


def show_placeholder(name: str) -> None:
    st.toast(f"{name}：功能开发中", icon="ℹ️")


def native_button(label: str, key: str, toast: bool = True, width: str = "stretch", disabled: bool = False) -> bool:
    if st.button(label, key=key, width=width, disabled=disabled):
        if toast:
            show_placeholder(label)
        return True
    return False


def get_fault_result() -> dict | None:
    return st.session_state.get("fault_pipeline_result")


def get_monthly_generation_result(fault_result: dict | None = None) -> dict | None:
    return st.session_state.get("monthly_generation_result")


def format_upload_size(uploaded_file) -> str:
    return format_file_size(upload_size(uploaded_file))


def show_upload_feedback(uploaded_file, label: str, next_step: str = "请点击“开始解析”继续。") -> None:
    if not uploaded_file:
        return
    safe_name = safe_file_name(uploaded_file.name)
    st.success(f"{label}已选择：{safe_name}（{format_upload_size(uploaded_file)}）。{next_step}")


def run_monthly_generation(
    fault_result: dict,
    categories: tuple[str, ...],
    progress_container=None,
) -> dict | None:
    """Generate monthly files and keep Streamlit progress tied to real tasks."""
    progress_state = {
        "completed": 0,
        "total": 0,
        "message": "准备生成月报文件...",
        "status": "生成中",
        "generated_at": "生成中",
        "output_dir": "等待生成",
    }

    def render_live_progress() -> None:
        if progress_container is None:
            return
        progress_container.empty()
        with progress_container.container():
            render_generation_progress_box(progress_state)

    render_live_progress()

    def update_progress(completed: int, total: int, message: str) -> None:
        percent = int(completed / total * 100) if total else 0
        progress_state.update(
            {
                "completed": completed,
                "total": total,
                "message": f"{message}（{completed}/{total}）",
                "status": "生成中" if percent < 100 else "生成完成",
            }
        )
        render_live_progress()

    try:
        result = generate_monthly_report_files(
            fault_result,
            categories=categories,
            progress_callback=update_progress,
        )
    except MonthlyGenerationError as exc:
        progress_state.update({"message": str(exc), "status": "生成失败"})
        render_live_progress()
        st.error(str(exc))
        return None
    except Exception as exc:  # pragma: no cover - Streamlit needs a readable fallback.
        error_message = f"月报生成失败：{exc}"
        progress_state.update({"message": error_message, "status": "生成失败"})
        render_live_progress()
        st.error(error_message)
        return None

    st.session_state["monthly_generation_result"] = result
    if progress_container is not None:
        progress_container.empty()
        with progress_container.container():
            render_generation_progress_box(result)
    return result


def render_generation_progress_box(result: dict | None) -> None:
    completed = int(result.get("completed", 0)) if result else 0
    total = int(result.get("total", 0)) if result else 0
    percent = int(completed / total * 100) if total else 0
    generated_at = result.get("generated_at", "暂无") if result else "暂无"
    output_dir = result.get("output_dir", "等待生成") if result else "等待生成"
    status = result.get("status") if result else None
    if not status:
        status = "生成完成" if percent == 100 and result else "等待生成"
    recent_label = result.get("message") if result else None
    if not recent_label:
        recent_label = generated_at
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
            <div style="color:#6b7280;font-size:13px;margin-top:4px;">最近生成：{recent_label}</div>
            <div style="color:#6b7280;font-size:13px;margin-top:4px;word-break:break-all;">输出目录：{output_dir}</div>
        </div>
        """
    )


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


