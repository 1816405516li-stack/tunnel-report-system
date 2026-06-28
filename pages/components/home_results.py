"""Result and intermediate dataset sections for the home page."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from generators.monthly_report import CATEGORY_LABELS, DEFAULT_CATEGORIES
from pages.components.home_actions import html, render_open_result_folder_button


VISIBLE_DATASET_KEYS = {
    "机电设施故障月报表_总表_数据",
    "机电设施故障月报表_分隧道表_数据",
    "机电日常巡查记录表_数据",
    "机电经常性检查记录表_数据",
    "隧道机电设备故障记录单_数据",
}


def generation_stats_html(result: dict | None) -> str:
    if not result:
        return '<div style="color:#6b7280;font-size:14px;">暂无生成结果，请先点击上方生成按钮。</div>'
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
    return f"<div class='dataset-list'>{''.join(rows)}</div>"


def render_dataset_outputs(result: dict | None) -> None:
    if result:
        rows = "".join(
            f"<div class='dataset-item'><span class='check'>✓</span><div>{name}：{Path(path).name}</div></div>"
            for name, path in result["files"].items()
            if name in VISIBLE_DATASET_KEYS
        )
        rows_html = f"<div class='dataset-list'>{rows}</div>"
        dir_html = f"<div class='dataset-dir'>保存目录：{result['processed_dir']}</div>"
        body_html = f"<div class='dataset-strip'>{rows_html}{dir_html}</div>"
    else:
        body_html = "<span style='color:#6b7280;'>• 暂无中间数据，请先完成解析。</span>"

    html(
        f"""
<section class="flow-card">
    <div class="module-title" style="margin-bottom:12px;color:#171717;"><span style="color:#743cff;">⌘</span> 当前生成中间数据</div>
    {body_html}
</section>
"""
    )


def render_result_preview_section(monthly_generation_result: dict | None) -> None:
    with st.container(key="result_preview_card", border=True):
        html(
            f"""
            <div class="module-title">◴ 生成结果预览</div>
            {generation_stats_html(monthly_generation_result)}
            """
        )
        render_open_result_folder_button(monthly_generation_result)

