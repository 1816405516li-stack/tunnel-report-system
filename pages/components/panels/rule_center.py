"""Rule-center popup page for transparent report generation rules."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import streamlit as st

from core.rules import RULES_DIR, RULE_FILES, load_rules


ORIGINAL_SOURCE = "设备维修单"

RULE_LABELS = {
    "monthly_fault_report": "机电设施故障月报表（总表）",
    "single_tunnel_fault_report": "机电设施故障月报表（分隧道表）",
    "daily_inspection": "机电日常巡查记录表",
    "frequent_inspection": "机电经常性检查记录表",
    "fault_record": "隧道机电设备故障记录单",
}

FIELD_SOURCES = {
    "monthly_fault_report": [
        ("隧道名称", "设备维修单：故障发生位置 / 所在位置", "标准化识别隧道名称"),
        ("隧道编码", "隧道映射表 + 设备维修单位置编码", "优先使用系统隧道编码映射"),
        ("故障日期", "设备维修单：报修时间", "取报修日期"),
        ("故障时间", "设备维修单：报修时间", "保留完整时间"),
        ("故障地点", "设备维修单：故障描述 / 设备桩号 / 方向", "优先识别描述中的 YK/ZK 桩号"),
        ("设备分类", "设备维修单：系统类型 / 设备类型 / 故障原因 / 处置措施", "按设备分类函数判断"),
        ("设备名称", "设备维修单：设备类型 / 设备名称", "优先设备类型"),
        ("故障现象", "设备维修单：故障描述", "去掉重复隧道名和已单独成列的故障地点"),
        ("故障原因", "设备维修单：故障原因 / 排查过程", "优先故障原因"),
        ("处置措施", "设备维修单：维修内容 / 确认处理措施", "优先维修内容"),
        ("修复时间", "设备维修单：现场维修完成时间 / 节点提交时间 / 验收时间", "按可用时间回退"),
        ("故障台数", "设备维修单每条有效故障记录", "每条记录计 1"),
        ("更换设备台数", "设备维修单：是否更换 / 更换配件 / 维修内容", "排除重启、重装合闸等非更换动作"),
        ("故障天数", "报修时间 + 修复时间", "包含首尾，最少 1 天"),
        ("维修人员", "设备维修单：维修人员", "原值清洗"),
        ("报修人", "设备维修单：报修人", "原值清洗"),
        ("更换配件名称", "设备维修单：更换配件名称 / 维修内容", "从更换片段提取"),
        ("是否修复", "设备维修单：是否修复", "原值清洗"),
        ("源表行号", "设备维修单原始行号", "用于追溯"),
    ],
    "single_tunnel_fault_report": [
        ("隧道名称", "总表标准故障明细", "按隧道拆分"),
        ("隧道编码", "总表标准故障明细", "沿用总表编码"),
        ("故障日期", "总表标准故障明细：故障日期", "写入分隧道表日期"),
        ("故障地点", "总表标准故障明细：故障地点", "沿用总表地点"),
        ("设备名称", "总表标准故障明细：设备名称", "沿用总表设备名称"),
        ("故障或事故概要", "总表标准故障明细：故障现象", "沿用通用文本整理结果"),
        ("原因及处理", "总表标准故障明细：故障原因 + 处置措施", "合并并去重"),
        ("修复时间", "总表标准故障明细：修复时间", "写入修复日期"),
        ("备注", "总表标准故障明细：备注", "沿用流程时间备注"),
        ("故障设备数量", "本隧道故障台数汇总", "只统计当前隧道"),
        ("更换设备数量", "本隧道更换设备台数汇总", "只统计当前隧道"),
    ],
    "daily_inspection": [
        ("隧道名称 / 隧道编码", "总表标准故障明细", "沿用总表隧道信息"),
        ("检查日期", "故障日期 + 修复时间 + 目标月份", "从故障发生日至修复日逐日展开"),
        ("检查项目", "设备名称 + 设备分类 + 故障现象 + 原因/处置", "按日常巡查分类规则判断"),
        ("设备名称", "总表标准故障明细：设备名称", "沿用总表设备名称"),
        ("故障地点", "总表标准故障明细：故障地点", "沿用总表地点"),
        ("养护单位检查情况描述", "设备名称 + 故障地点 + 故障现象", "组合成巡查描述"),
        ("采取措施", "故障原因 + 处置措施 / 待修复固定语", "修复日写处理结果，未修复日写待修复"),
        ("故障编号 / 源表行号", "总表标准故障明细", "用于追溯"),
    ],
    "frequent_inspection": [
        ("隧道名称 / 隧道编码", "隧道清单 + 总表标准故障明细", "每座隧道生成一份"),
        ("周检日期", "目标月份 + 周检规则", "按每月周检日期规则生成"),
        ("检查日", "目标月份 25 日", "固定检查日"),
        ("异常描述", "总表标准故障明细：故障日期 + 故障地点 + 设备名称 + 故障现象", "只纳入 25 日仍需反映的故障"),
        ("养护措施", "总表标准故障明细：故障原因 + 处置措施", "合并并去重"),
        ("是否无异常", "当前隧道 25 日异常判断结果", "没有异常时生成空表标记"),
        ("故障编号 / 源表行号", "总表标准故障明细", "用于追溯"),
    ],
    "fault_record": [
        ("隧道名称 / 隧道编码", "总表标准故障明细", "沿用总表隧道信息"),
        ("故障时间 C3", "总表标准故障明细：故障时间", "写入故障时间"),
        ("报修时间 E3", "总表标准故障明细：故障时间", "当前与故障时间一致"),
        ("设备位置 C4", "总表标准故障明细：故障地点", "沿用总表地点"),
        ("报修人 E4", "总表标准故障明细：报修人", "沿用总表报修人"),
        ("设备名称 C5", "总表标准故障明细：设备名称", "沿用总表设备名称"),
        ("修复时限要求 E5", "故障时间", "按故障时间加 3 天生成"),
        ("到场时间 C7", "总表标准故障明细：派工时间", "沿用派工时间"),
        ("维修人员 E7", "总表标准故障明细：维修人员", "沿用维修人员"),
        ("故障现象 C6", "总表标准故障明细：故障现象", "去掉重复地点后写入"),
        ("故障原因和维修记录 C8", "总表标准故障明细：故障原因 + 处置措施", "合并并去重"),
        ("备件名称 / 数量", "总表标准故障明细：更换配件名称 + 更换设备台数", "有更换时填写"),
        ("处理结果", "总表标准故障明细：修复时间 + 更换设备台数", "判断已修复和是否更换配件"),
        ("源表行号", "总表标准故障明细", "用于追溯"),
    ],
}


def render_rule_center_page() -> None:
    """Render a read-only overview of reusable project rules."""
    rules = load_rules()

    st.markdown(
        """
        <div class="popup-page">
            <div class="popup-kicker">规则中心</div>
            <h2>月报生成规则透明化</h2>
            <p>
                这里区分两种来源：原始事实来源始终是设备维修单；
                生成输入来源表示某张表在系统内部直接读取哪一份标准数据。
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _render_rule_overview(rules)
    _render_source_columns_by_table()
    _render_text_rules()
    _render_generation_rules(rules)
    _render_rule_files()
    _render_next_quality_checks()


def _render_rule_overview(rules: dict[str, dict[str, Any]]) -> None:
    st.markdown("#### 规则清单")
    rows = []
    for key, rule in rules.items():
        rows.append(
            {
                "规则名称": RULE_LABELS.get(key, key),
                "原始事实来源": ORIGINAL_SOURCE,
                "生成输入来源": _generation_source_label(key, rule),
                "用途": _compact_value(rule.get("purpose", "")),
                "数据文件": _compact_value(rule.get("dataset_file", "")),
            }
        )
    st.dataframe(rows, width="stretch", hide_index=True)


def _render_source_columns_by_table() -> None:
    st.markdown("#### 字段来源（按表）")
    tabs = st.tabs([RULE_LABELS[key] for key in FIELD_SOURCES])
    for tab, table_key in zip(tabs, FIELD_SOURCES, strict=True):
        with tab:
            rows = [
                {"结果字段": field, "字段来源": source, "处理说明": note}
                for field, source, note in FIELD_SOURCES[table_key]
            ]
            st.dataframe(rows, width="stretch", hide_index=True)


def _render_text_rules() -> None:
    st.markdown("#### 文本整理规则")
    rows = [
        {
            "处理对象": "故障现象",
            "通用规则": "从故障描述生成，去掉已单独成列的隧道名和故障地点，保留新的故障表达。",
            "代码位置": "core/repair_orders/report_text.py",
        },
        {
            "处理对象": "处置措施",
            "通用规则": "优先使用维修内容，缺失时使用确认处理措施，并做空格和结尾标点整理。",
            "代码位置": "core/repair_orders/standardize.py",
        },
        {
            "处理对象": "原因及处理",
            "通用规则": "合并故障原因和处置措施；如果处置措施已经包含原因，不重复拼接。",
            "代码位置": "core/repair_orders/report_text.py",
        },
        {
            "处理对象": "故障地点",
            "通用规则": "优先识别故障描述中的 YK/ZK 桩号；只有 K 前缀时按方向补齐；否则回退到设备桩号。",
            "代码位置": "core/repair_orders/text.py",
        },
    ]
    st.dataframe(rows, width="stretch", hide_index=True)


def _render_generation_rules(rules: dict[str, dict[str, Any]]) -> None:
    st.markdown("#### 报表生成规则")
    rows = []
    for key, rule in rules.items():
        for group_name in ("cleaning_rules", "rules", "generation_scope", "spare_part_rule", "result_rule"):
            group = rule.get(group_name)
            if not isinstance(group, dict):
                continue
            for item_key, item_value in group.items():
                rows.append(
                    {
                        "报表": RULE_LABELS.get(key, key),
                        "规则组": group_name,
                        "规则项": item_key,
                        "内容": _compact_value(item_value),
                    }
                )
    st.dataframe(rows, width="stretch", hide_index=True)


def _render_rule_files() -> None:
    st.markdown("#### 规则文件")
    rows = []
    for key, file_name in RULE_FILES.items():
        path = RULES_DIR / file_name
        rows.append(
            {
                "规则名称": RULE_LABELS.get(key, key),
                "文件": file_name,
                "位置": str(path),
                "状态": "已加载" if Path(path).exists() else "缺失",
            }
        )
    st.dataframe(rows, width="stretch", hide_index=True)


def _render_next_quality_checks() -> None:
    st.markdown("#### 待接入质检项")
    rows = [
        {"检查项": "故障现象为空", "作用": "生成前提醒补充原始维修单内容"},
        {"检查项": "处置措施为空", "作用": "避免总表和分隧道表出现空处理结果"},
        {"检查项": "故障地点未识别到桩号", "作用": "提醒人工确认设备位置是否完整"},
        {"检查项": "原因及处理过长或重复", "作用": "提醒检查月报文字是否简洁"},
        {"检查项": "设备分类无法识别", "作用": "提醒补充设备分类规则"},
    ]
    st.dataframe(rows, width="stretch", hide_index=True)


def _generation_source_label(key: str, rule: dict[str, Any]) -> str:
    if key == "monthly_fault_report":
        return ORIGINAL_SOURCE
    return _compact_value(rule.get("source", "")) or "标准故障明细"


def _compact_value(value: Any) -> str:
    if isinstance(value, list):
        return " / ".join(str(item) for item in value)
    if isinstance(value, dict):
        return "；".join(f"{key}: {_compact_value(item)}" for key, item in value.items())
    if isinstance(value, bool):
        return "是" if value else "否"
    return str(value or "")
