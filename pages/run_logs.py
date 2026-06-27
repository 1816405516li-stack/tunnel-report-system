"""System-log popup page for the tunnel monthly report system."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import streamlit as st

from config.settings import OUTPUTS_DIR, WORKSPACE_DIR


def _latest_files(root: Path, limit: int = 12) -> list[Path]:
    if not root.exists():
        return []
    return sorted(
        (path for path in root.rglob("*") if path.is_file() and path.name != ".gitkeep"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )[:limit]


def _format_size(size: int) -> str:
    if size < 1024:
        return f"{size} B"
    if size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"
    return f"{size / 1024 / 1024:.1f} MB"


def _file_rows(files: list[Path]) -> list[dict[str, str]]:
    rows = []
    for path in files:
        stat = path.stat()
        rows.append(
            {
                "时间": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                "文件": path.name,
                "大小": _format_size(stat.st_size),
                "位置": str(path.parent),
            }
        )
    return rows


def render_run_logs_page() -> None:
    """Render the runtime log popup page."""
    fault_result = st.session_state.get("fault_pipeline_result")
    generation_result = st.session_state.get("monthly_generation_result")

    st.markdown(
        """
        <div class="popup-page">
            <div class="popup-kicker">系统日志</div>
            <h2>本次会话与最近输出</h2>
            <p>这里汇总当前页面会话状态、最近生成结果和工作目录中的最新文件，便于快速检查处理进度。</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    status_rows = [
        {"项目": "设备维修单解析", "状态": "已完成" if fault_result else "等待上传或解析"},
        {"项目": "月报文件生成", "状态": "已完成" if generation_result else "等待生成"},
        {"项目": "日志刷新时间", "状态": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
    ]
    st.dataframe(status_rows, width="stretch", hide_index=True)

    if fault_result:
        st.markdown("#### 解析摘要")
        st.dataframe(
            [
                {"项目": "故障记录数", "内容": fault_result.get("fault_rows", 0)},
                {"项目": "涉及隧道数", "内容": fault_result.get("tunnel_count", 0)},
                {"项目": "日期范围", "内容": f"{fault_result.get('date_start', '')} 至 {fault_result.get('date_end', '')}"},
                {"项目": "中间数据目录", "内容": fault_result.get("processed_dir", "")},
            ],
            width="stretch",
            hide_index=True,
        )

    if generation_result:
        st.markdown("#### 生成摘要")
        category_rows = []
        for name, item in (generation_result.get("category_stats") or {}).items():
            category_rows.append(
                {
                    "类别": name,
                    "文件数": item.get("file_count", 0),
                    "目录": item.get("output_dir", ""),
                }
            )
        st.dataframe(category_rows, width="stretch", hide_index=True)

    st.markdown("#### 最近输出文件")
    output_rows = _file_rows(_latest_files(OUTPUTS_DIR))
    if output_rows:
        st.dataframe(output_rows, width="stretch", hide_index=True)
    else:
        st.info("暂未找到输出文件。")

    st.markdown("#### 最近工作文件")
    workspace_rows = _file_rows(_latest_files(WORKSPACE_DIR))
    if workspace_rows:
        st.dataframe(workspace_rows, width="stretch", hide_index=True)
    else:
        st.info("暂未找到工作文件。")
