"""Streamlit home page for the tunnel monthly report automation system."""

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

MONTHLY_GENERATION_ACTIONS = [
    ("total", "生成总月报表"),
    ("single_tunnel", "生成单隧道月报表"),
    ("daily", "生成日常巡查记录表"),
    ("frequent", "生成经常性检查记录表"),
    ("fault_record", "生成设备故障记录单"),
    ("all", "一键生成全部月报文件"),
]

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #f8f4ef;
    --panel: rgba(255, 255, 255, 0.92);
    --text: #171717;
    --muted: #6b7280;
    --line: #ece4dc;
    --blue: #2563eb;
    --purple: #6d5dfc;
    --orange: #f05a28;
    --green: #16a34a;
    --gray: #9ca3af;
    --shadow: 0 14px 35px rgba(57, 41, 22, 0.08);
    --section-gap: 10px;
}

html, body, [class*="css"] {
    font-family: "Noto Sans SC", "Microsoft YaHei", "PingFang SC", sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 8% 0%, rgba(255, 246, 233, 0.75), transparent 34%),
        linear-gradient(180deg, #fbf7f1 0%, #f7f3ed 100%);
    color: var(--text);
}

.block-container {
    max-width: 1800px;
    padding: 10px 22px 16px;
}

header[data-testid="stHeader"], [data-testid="stToolbar"] {
    display: none;
}

[data-testid="stSidebar"], [data-testid="stSidebarNav"], [data-testid="collapsedControl"] {
    display: none;
}

div[data-testid="stVerticalBlock"] {
    gap: var(--section-gap);
}

div[data-testid="stMainBlockContainer"],
div[data-testid="stAppViewContainer"],
div[data-testid="stLayoutWrapper"],
div[data-testid="stElementContainer"],
div[data-testid="stVerticalBlock"],
div[data-testid="stColumn"] {
    width: 100% !important;
    max-width: 100% !important;
    min-width: 0 !important;
    box-sizing: border-box !important;
}

div[data-testid="stColumn"] {
    flex: 1 1 0% !important;
    width: auto !important;
    align-self: stretch !important;
    display: flex !important;
    flex-direction: column !important;
}

div[data-testid="stHorizontalBlock"] {
    align-items: stretch !important;
}

div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] > div {
    flex: 1 1 auto !important;
    height: 100% !important;
}

div[class*="st-emotion-cache-18kf3ut"],
div[class*="st-emotion-cache-tn0cau"],
div[class*="st-emotion-cache-wfksaw"],
div[class*="st-emotion-cache-3pwa5w"] {
    width: 100% !important;
    max-width: 100% !important;
    min-width: 0 !important;
    box-sizing: border-box !important;
}

.hero, .soft-card, .flow-card, .result-card {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 18px;
    box-shadow: var(--shadow);
    margin: 0 0 var(--section-gap);
}

.hero {
    display: grid;
    grid-template-columns: 1.45fr 1fr;
    gap: 18px;
    align-items: center;
    padding: 22px 26px 14px;
}

.brand-row {
    display: flex;
    gap: 20px;
    align-items: center;
}

.brand-icon {
    width: 76px;
    height: 76px;
    display: grid;
    place-items: center;
    border-radius: 18px;
    color: #fff;
    background: linear-gradient(135deg, #6548ff 0%, #b047c7 52%, #ed6030 100%);
    box-shadow: 0 14px 28px rgba(101, 72, 255, 0.23);
    font-size: 39px;
}

.hero h1 {
    margin: 0;
    font-size: clamp(30px, 2.8vw, 46px);
    line-height: 1.08;
    letter-spacing: 0;
    font-weight: 800;
}

.subtitle {
    margin-top: 10px;
    color: #555b66;
    font-size: 16px;
    font-weight: 500;
}

.top-actions {
    display: grid;
    grid-template-columns: repeat(5, minmax(92px, 1fr));
    gap: 14px;
}

.action-box {
    min-height: 72px;
    width: 100%;
    border: 1px solid #eadfd4;
    border-radius: 14px;
    display: grid;
    place-items: center;
    text-align: center;
    color: #1f2937;
    background: rgba(255, 255, 255, 0.72);
    font-weight: 700;
    font-size: 14px;
    cursor: pointer;
    font-family: inherit;
}

.action-box .icon {
    display: block;
    margin-bottom: 4px;
    font-size: 22px;
}

.status-row {
    grid-column: 1 / -1;
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    padding-left: 100px;
    margin-top: -4px;
}

.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    height: 38px;
    padding: 0 18px;
    border: 1px solid #eadfd4;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.72);
    color: #303641;
    font-size: 14px;
    font-weight: 700;
}

.status-pill .mini {
    color: var(--blue);
    font-size: 17px;
}

.module-title {
    display: inline-flex;
    align-items: center;
    width: fit-content;
    max-width: 100%;
    gap: 6px;
    margin: 0 0 4px;
    font-size: 18px;
    font-weight: 800;
    white-space: nowrap;
    flex-wrap: nowrap;
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    margin-bottom: 10px;
}

.section-header .module-title {
    margin-bottom: 0;
}

.section-tools {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
    justify-content: flex-end;
}

.value-badge {
    min-width: 104px;
    height: 28px;
    padding: 0 10px;
    border-radius: 10px;
    border: 1px solid #eadfd4;
    background: #ffffff;
    color: #374151;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 800;
    white-space: nowrap;
}

.section-panel {
    background: #ffffff;
    border: 1px solid #efe6de;
    border-radius: 14px;
    padding: 14px;
}

.parse-toolbar {
    display: grid;
    grid-template-columns: 190px 138px 1fr 72px;
    align-items: center;
    gap: 16px;
    margin-bottom: 14px;
}

.soft-card {
    padding: 16px 18px 14px;
    min-height: 100%;
    position: relative;
    z-index: 0;
}

.action-card {
    margin-top: var(--section-gap);
}

.upload-large {
    height: 138px;
    border: 1.5px dashed #f4b8a0;
    border-radius: 10px;
    background: linear-gradient(135deg, rgba(247, 249, 255, 0.95), rgba(255, 250, 245, 0.95));
    display: grid;
    place-items: center;
    text-align: center;
    margin-bottom: 12px;
}

.upload-large .upload-icon {
    width: 50px;
    height: 50px;
    border-radius: 13px;
    background: #fff;
    box-shadow: 0 8px 18px rgba(0, 0, 0, 0.08);
    display: grid;
    place-items: center;
    margin: 0 auto 10px;
    color: #ef3b2d;
    font-size: 25px;
}

.upload-title {
    font-weight: 800;
    font-size: 16px;
}

.upload-note {
    margin-top: 5px;
    color: #6b7280;
    font-size: 14px;
}

.upload-chip {
    padding: 14px 18px;
    min-height: 88px;
    border-radius: 13px;
    border: 1px solid #eee2d8;
    background: linear-gradient(135deg, #fbf5ff, #fff9f0 58%, #f4fbf6);
}

.upload-chip h4 {
    margin: 0 0 6px;
    font-size: 16px;
}

.upload-chip p {
    margin: 0 0 8px;
    color: #6b7280;
    font-size: 13px;
}

.format {
    color: #ff2626;
    font-weight: 800;
    font-size: 13px;
}

.progress-line {
    display: grid;
    grid-template-columns: auto 1fr auto;
    align-items: center;
    gap: 16px;
    margin: 6px 0 8px;
}

.progress-line.compact {
    gap: 12px;
    margin: 2px 0 6px;
}

.progress-label {
    font-weight: 800;
    font-size: 15px;
}

.bar {
    height: 9px;
    border-radius: 999px;
    background: #ececec;
    overflow: hidden;
}

.bar span {
    display: block;
    height: 100%;
    border-radius: inherit;
    background: linear-gradient(90deg, #3974ff, #7f4ef5, #e33628);
}

.bar.green span {
    background: #12aa51;
}

.percent {
    font-weight: 800;
    font-size: 18px;
    color: var(--green);
}

.percent.red {
    color: #ff1f1f;
    font-size: 28px;
}

.summary-title {
    margin: 4px 0 6px;
    font-size: 16px;
    font-weight: 800;
}

.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 12px;
    align-items: stretch;
    grid-auto-rows: minmax(92px, auto);
}

.metric-grid.compact {
    gap: 10px;
}

.metric-card {
    min-height: 92px;
    display: grid;
    grid-template-columns: 42px 1fr;
    gap: 10px;
    align-items: center;
    padding: 9px 12px;
    border: 1px solid #ede5dd;
    border-radius: 14px;
    background: rgba(255, 255, 255, 0.74);
    height: 100%;
    box-sizing: border-box;
}

.metric-grid.compact .metric-card {
    min-height: 62px;
    padding: 8px 10px;
}

.metric-grid.compact .metric-icon {
    width: 34px;
    height: 34px;
    font-size: 20px;
}

.metric-icon {
    width: 38px;
    height: 38px;
    border-radius: 13px;
    display: grid;
    place-items: center;
    background: #f2f6ff;
    color: var(--purple);
    font-size: 22px;
}

.metric-label {
    color: #6b7280;
    font-size: 13px;
    font-weight: 600;
}

.metric-value {
    color: #111827;
    font-size: 20px;
    font-weight: 800;
    line-height: 1.15;
}

.metric-value.green, .check {
    color: var(--green);
}

.metric-value.red, .trend {
    color: #ff1f1f;
}

.flow-card {
    padding: 10px 14px;
    margin: 0 0 var(--section-gap);
    position: relative;
    z-index: 1;
}

.dataset-strip {
    display: grid;
    gap: 10px;
}

.dataset-list {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 8px 24px;
}

.dataset-item {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    color: #2f3b45;
    font-weight: 600;
    font-size: 14px;
    line-height: 1.45;
}

.dataset-dir {
    color: #6b7280;
    font-size: 13px;
}

.flow-grid {
    display: flex;
    flex-wrap: nowrap;
    gap: 10px;
    align-items: stretch;
}

.step {
    flex: 1 1 0;
    min-height: 44px;
    min-width: 0;
    border: 1px solid #eee2d8;
    border-radius: 12px;
    background: #fff;
    display: grid;
    grid-template-columns: 30px 1fr;
    align-items: center;
    gap: 8px;
    padding: 7px 10px;
    white-space: nowrap;
}

.step.done { background: #eefbf1; border-color: #b9e8c4; }
.step.active { background: #f8fbff; border-color: #bdd4ff; }
.step.todo { background: #faf9f7; }

.num {
    width: 25px;
    height: 25px;
    border-radius: 8px;
    display: grid;
    place-items: center;
    color: #fff;
    font-weight: 800;
    background: #80858d;
}

.done .num { background: var(--green); }
.active .num { background: var(--blue); }

.step-name {
    font-weight: 800;
    font-size: 15px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.step-status {
    color: #6b7280;
    font-size: 13px;
    font-weight: 700;
    white-space: nowrap;
}

.done .step-status { color: var(--green); }
.active .step-status { color: var(--blue); }

.arrow {
    text-align: center;
    color: #4b5563;
    font-size: 24px;
}

.button-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 12px 14px;
    margin-bottom: 14px;
}

.fake-button, .primary-button {
    width: 100%;
    height: 34px;
    display: grid;
    place-items: center;
    border-radius: 8px;
    border: 1px solid #eadfd4;
    background: rgba(255, 255, 255, 0.82);
    font-weight: 700;
    color: #374151;
    cursor: pointer;
    font-family: inherit;
}

.primary-button {
    color: #fff;
    border: 0;
    background: linear-gradient(90deg, #5567ff, #7b4df4, #e33b28);
    box-shadow: 0 12px 22px rgba(109, 93, 252, 0.2);
}

.generation-box {
    border: 1px solid #ede5dd;
    border-radius: 13px;
    padding: 14px;
    margin-bottom: 12px;
    background: rgba(255, 255, 255, 0.64);
}

.generate-head {
    display: grid;
    grid-template-columns: 1fr auto;
    align-items: end;
    gap: 12px;
}

.power-upload-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 16px;
    margin-bottom: 10px;
}

.electric-grid {
    display: grid;
    grid-template-columns: 0.95fr 1.1fr 0.8fr;
    gap: 14px;
    min-height: 0;
    align-items: stretch;
}

.inner-panel {
    border: 1px solid #ede5dd;
    border-radius: 13px;
    background: rgba(255, 255, 255, 0.72);
    padding: 14px 16px;
}

.tight-panel {
    padding: 12px 14px;
}

.timeline {
    display: grid;
    gap: 11px;
    margin-top: 12px;
}

.timeline-item {
    display: grid;
    grid-template-columns: 14px 1fr;
    align-items: center;
    gap: 10px;
    color: #303641;
    font-weight: 600;
    font-size: 14px;
}

.dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #c8ccd2;
}

.dot.done { background: var(--green); }
.dot.active { background: var(--blue); }

.output-lines {
    color: #4b5563;
    font-size: 14px;
    line-height: 2.05;
}

.electric-action {
    display: grid;
    grid-template-rows: auto auto;
    align-content: start;
    gap: 14px;
}

.power-actions-card {
    min-height: 414px;
}

.lower-sections {
    margin-top: 0;
    margin-bottom: 0;
}

.lower-card {
    margin-top: 0;
    min-height: 414px;
    margin-bottom: var(--section-gap);
}

.st-key-monthly_generation_card {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 18px;
    box-shadow: var(--shadow);
    padding: 16px 18px 14px;
    margin: 0 0 var(--section-gap);
    min-height: 414px;
    width: 100%;
    box-sizing: border-box;
}

.st-key-monthly_generation_card > div[data-testid="stVerticalBlock"] {
    gap: 12px;
}

.large-main {
    width: 100%;
    height: 54px;
    border: 0;
    border-radius: 13px;
    display: grid;
    place-items: center;
    color: #fff;
    font-weight: 800;
    font-family: inherit;
    cursor: pointer;
    background: linear-gradient(90deg, #5567ff, #7b4df4, #d34431);
    box-shadow: 0 16px 26px rgba(109, 93, 252, 0.2);
}

.result-card {
    padding: 16px 28px;
}

.result-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 18px;
}

.result-box {
    position: relative;
    overflow: hidden;
    min-height: 124px;
    border-radius: 13px;
    border: 1px solid #dcecdf;
    padding: 18px 28px;
}

.result-box.monthly {
    background: linear-gradient(100deg, #eefbf0, #ffffff 68%, #eaf5ff);
}

.result-box.power {
    background: linear-gradient(100deg, #f3fbff, #ffffff 68%, #edf5ff);
}

.result-title {
    color: #087437;
    font-weight: 800;
    margin-bottom: 10px;
}

.power .result-title {
    color: #1263a8;
}

.result-list {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px 34px;
    color: #2f3b45;
    font-weight: 600;
    font-size: 14px;
}

.stamp {
    position: absolute;
    right: 34px;
    bottom: 12px;
    font-size: 72px;
    opacity: 0.12;
}

.last-time {
    text-align: center;
    color: #4b5563;
    font-size: 15px;
    font-weight: 600;
    margin-top: 10px;
}

div[data-testid="stFileUploader"] {
    margin: 8px 0 4px;
}

div[data-testid="stFileUploader"] label {
    display: none;
}

div[data-testid="stFileUploader"] section {
    min-height: 42px;
    padding: 6px 10px;
    border: 1px solid #efe5dc;
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.72);
}

div[data-testid="stFileUploader"] button {
    min-width: 110px;
    min-height: 36px;
    border-radius: 9px;
    border: 1px solid #eadfd4 !important;
    background: #ffffff !important;
    color: #111827 !important;
    box-shadow: none !important;
}

div[data-testid="stFileUploader"] button * {
    color: #111827 !important;
}

div[data-testid="stFileUploader"] small {
    color: #7b8290;
}

.st-key-fault_uploader div[data-testid="stFileUploader"],
.st-key-power_uploader_last_month_table div[data-testid="stFileUploader"],
.st-key-power_uploader_this_month_bill div[data-testid="stFileUploader"] {
    margin: 0 0 12px;
}

.st-key-fault_uploader div[data-testid="stFileUploader"] section,
.st-key-power_uploader_last_month_table div[data-testid="stFileUploader"] section,
.st-key-power_uploader_this_month_bill div[data-testid="stFileUploader"] section {
    position: relative;
    min-height: 138px;
    padding: 0;
    border: 1.5px dashed #f4b8a0;
    border-radius: 10px;
    background: linear-gradient(135deg, rgba(247, 249, 255, 0.95), rgba(255, 250, 245, 0.95));
    display: grid;
    place-items: center;
    overflow: hidden;
}

.st-key-power_uploader_last_month_table div[data-testid="stFileUploader"] section,
.st-key-power_uploader_this_month_bill div[data-testid="stFileUploader"] section {
    min-height: 124px;
}

.st-key-fault_uploader div[data-testid="stFileUploader"] section::before {
    content: "拖拽或点击上传初始故障单 Excel\\A支持 .xlsx / .xls 文件";
    position: relative;
    z-index: 1;
    white-space: pre;
    text-align: center;
    color: #111827;
    font-size: 16px;
    font-weight: 800;
    line-height: 1.9;
    padding-top: 52px;
}

.st-key-power_uploader_last_month_table div[data-testid="stFileUploader"] section::before {
    content: "上传上月电费表\\A用于核对上月电费金额和用电情况\\A.xlsx / .xls / .pdf";
    position: relative;
    z-index: 1;
    white-space: pre;
    text-align: center;
    color: #111827;
    font-size: 13px;
    font-weight: 800;
    line-height: 1.5;
    padding: 58px 14px 0;
}

.st-key-power_uploader_this_month_bill div[data-testid="stFileUploader"] section::before {
    content: "上传本月账单\\A用于生成本月电费统计表\\A.xlsx / .xls / .pdf";
    position: relative;
    z-index: 1;
    white-space: pre;
    text-align: center;
    color: #111827;
    font-size: 13px;
    font-weight: 800;
    line-height: 1.5;
    padding: 58px 14px 0;
}

.st-key-fault_uploader div[data-testid="stFileUploader"] section::after {
    content: "↥";
    position: absolute;
    top: 22px;
    left: 50%;
    width: 50px;
    height: 50px;
    transform: translateX(-50%);
    border-radius: 13px;
    background: rgba(255, 255, 255, 0.92);
    box-shadow: 0 8px 18px rgba(0, 0, 0, 0.08);
    color: #ef3b2d;
    display: grid;
    place-items: center;
    font-size: 24px;
    font-weight: 800;
    z-index: 2;
}

.st-key-power_uploader_last_month_table div[data-testid="stFileUploader"] section::after,
.st-key-power_uploader_this_month_bill div[data-testid="stFileUploader"] section::after {
    content: "↥";
    position: absolute;
    top: 14px;
    left: 50%;
    width: 38px;
    height: 38px;
    transform: translateX(-50%);
    border-radius: 13px;
    background: rgba(255, 255, 255, 0.92);
    box-shadow: 0 8px 18px rgba(0, 0, 0, 0.08);
    color: #ef3b2d;
    display: grid;
    place-items: center;
    font-size: 24px;
    font-weight: 800;
    z-index: 2;
}

.st-key-fault_uploader div[data-testid="stFileUploader"] section > div,
.st-key-power_uploader_last_month_table div[data-testid="stFileUploader"] section > div,
.st-key-power_uploader_this_month_bill div[data-testid="stFileUploader"] section > div {
    display: none;
}

.st-key-fault_uploader div[data-testid="stFileUploader"] section button,
.st-key-power_uploader_last_month_table div[data-testid="stFileUploader"] section button,
.st-key-power_uploader_this_month_bill div[data-testid="stFileUploader"] section button {
    position: absolute;
    inset: 0;
    width: 100% !important;
    height: 100% !important;
    min-height: 138px;
    opacity: 0;
    cursor: pointer;
    z-index: 3;
}

.st-key-power_uploader_last_month_table div[data-testid="stFileUploader"] section button,
.st-key-power_uploader_this_month_bill div[data-testid="stFileUploader"] section button {
    min-height: 124px;
}

div[data-testid="stNumberInput"] label {
    font-weight: 800;
    color: #171717;
    margin-bottom: 2px;
}

div[data-testid="stNumberInput"] input {
    background: rgba(255, 255, 255, 0.92);
    color: #171717;
    border: 1px solid #eadfd4;
    border-radius: 8px 0 0 8px;
    min-height: 44px;
}

div[data-testid="stNumberInput"] button {
    background: rgba(255, 255, 255, 0.92);
    color: #171717;
    border-color: #eadfd4;
    min-height: 44px;
}

.st-key-power_price_input div[data-testid="stNumberInput"] label {
    display: none;
}

.st-key-power_price_input {
    display: flex;
    justify-content: flex-end;
}

.st-key-power_price_input div[data-testid="stNumberInput"] {
    margin-bottom: 0;
    width: 100%;
    max-width: 180px;
    margin-left: auto;
    margin-right: 0;
}

.st-key-power_price_input div[data-testid="stNumberInput"] input {
    min-height: 30px;
    height: 30px;
    border-radius: 8px 0 0 8px;
}

.st-key-power_price_input div[data-testid="stNumberInput"] button {
    min-height: 30px;
    height: 30px;
}

.st-key-confirm_power_price .stButton > button,
.st-key-parse_fault .stButton > button,
.st-key-parse_power .stButton > button {
    min-height: 30px !important;
    height: 30px;
    border-radius: 10px;
}

.st-key-confirm_power_price .stButton > button {
    min-width: 78px !important;
    width: 78px !important;
    padding: 0 10px;
    box-shadow: 0 10px 18px rgba(109, 93, 252, 0.14);
}

.st-key-confirm_power_price {
    display: flex;
    justify-content: center;
}

.st-key-confirm_power_price .stButton {
    margin: 0 auto;
}

.st-key-power_header_box,
.st-key-fault_header_box {
    background: #ffffff;
    border: 1px solid #efe6de;
    border-radius: 12px;
    padding: 6px 10px;
    margin-bottom: 4px;
    width: 100%;
    box-sizing: border-box;
}

.st-key-power_header_box > div[data-testid="stVerticalBlock"],
.st-key-fault_header_box > div[data-testid="stVerticalBlock"] {
    gap: 0;
}

.st-key-fault_header_card,
.st-key-fault_uploads_card,
.st-key-power_header_card,
.st-key-power_uploads_card {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 16px;
    box-shadow: var(--shadow);
    padding: 8px 10px 6px;
    margin: 0 0 calc(var(--section-gap) - 2px);
    width: 100%;
    box-sizing: border-box;
}

.st-key-fault_header_card,
.st-key-power_header_card {
    height: 252px;
    min-height: 252px;
    display: flex;
    flex-direction: column;
}

.st-key-fault_header_card > div[data-testid="stVerticalBlock"],
.st-key-fault_uploads_card > div[data-testid="stVerticalBlock"],
.st-key-power_header_card > div[data-testid="stVerticalBlock"],
.st-key-power_uploads_card > div[data-testid="stVerticalBlock"] {
    gap: 8px;
    flex: 1 1 auto;
    height: 100%;
}

.st-key-fault_header_box,
.st-key-power_header_box {
    flex: 1 1 auto;
    min-height: 226px;
    display: flex;
    flex-direction: column;
}

.st-key-fault_header_box > div[data-testid="stVerticalBlock"],
.st-key-power_header_box > div[data-testid="stVerticalBlock"] {
    flex: 1 1 auto;
    height: 100%;
}

.st-key-fault_uploader div[data-testid="stFileUploader"] section {
    min-height: 176px;
}

.st-key-fault_uploader div[data-testid="stFileUploader"] section button {
    min-height: 176px;
}

.st-key-fault_parse_card,
.st-key-power_parse_card {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 18px;
    box-shadow: var(--shadow);
    padding: 16px 18px 14px;
    margin: 0 0 var(--section-gap);
    min-height: 320px;
}

.st-key-fault_parse_card > div[data-testid="stVerticalBlock"],
.st-key-power_parse_card > div[data-testid="stVerticalBlock"] {
    gap: 12px;
}

.st-key-fault_parse_panel,
.st-key-power_parse_panel {
    background: #ffffff;
    border: 1px solid #efe6de;
    border-radius: 14px;
    padding: 14px;
    min-height: 240px;
}

.st-key-fault_parse_panel > div[data-testid="stVerticalBlock"],
.st-key-power_parse_panel > div[data-testid="stVerticalBlock"] {
    gap: 14px;
}

.stButton > button,
.stDownloadButton > button {
    width: 100%;
    min-height: 40px;
    border-radius: 10px;
    border: 0;
    background: linear-gradient(90deg, #5567ff, #7b4df4, #e33b28);
    color: #ffffff;
    font-weight: 800;
    box-shadow: 0 12px 22px rgba(109, 93, 252, 0.18);
}

.stDownloadButton > button {
    background: rgba(255, 255, 255, 0.82);
    color: #374151;
    border: 1px solid #eadfd4;
    box-shadow: none;
}

.stDownloadButton > button:hover {
    color: #374151;
}

.stDownloadButton > button:disabled,
.stButton > button:disabled {
    background: #f4f1ed !important;
    color: #9ca3af !important;
    border: 1px solid #e7ddd2 !important;
    box-shadow: none !important;
}

.st-key-gen_monthly_total .stButton > button,
.st-key-gen_monthly_single_tunnel .stButton > button,
.st-key-gen_monthly_daily .stButton > button,
.st-key-gen_monthly_frequent .stButton > button,
.st-key-gen_monthly_fault_record .stButton > button {
    min-height: 34px;
    background: rgba(255, 255, 255, 0.82);
    color: #374151;
    border: 1px solid #eadfd4;
    box-shadow: none;
}

.st-key-gen_monthly_total .stButton > button:hover,
.st-key-gen_monthly_single_tunnel .stButton > button:hover,
.st-key-gen_monthly_daily .stButton > button:hover,
.st-key-gen_monthly_frequent .stButton > button:hover,
.st-key-gen_monthly_fault_record .stButton > button:hover {
    color: #374151;
}

.button-right-wrap {
    display: flex;
    justify-content: flex-end;
    width: 100%;
}

.st-key-power_parse_button {
    display: flex !important;
    justify-content: flex-end !important;
    width: 100% !important;
    align-items: flex-end !important;
    padding-top: 0 !important;
    margin-top: 0 !important;
}

.st-key-power_parse_button > div {
    align-self: flex-end !important;
}

.st-key-power_parse_button > div {
    width: auto !important;
    display: flex !important;
    justify-content: flex-end !important;
}

.st-key-power_parse_button .stElementContainer {
    width: auto !important;
    display: flex !important;
    justify-content: flex-end !important;
}

.st-key-power_parse_button .stButton {
    display: flex !important;
    justify-content: flex-end !important;
}

.st-key-power_parse_button .stButton > button {
    width: auto !important;
    min-width: 120px !important;
    min-height: 44px !important;
    padding: 0 16px;
    margin-left: auto !important;
    margin-top: 0 !important;
}

.stButton > button:hover {
    color: #ffffff;
    filter: brightness(1.02);
}

@media (max-width: 1100px) {
    .hero, .result-grid {
        grid-template-columns: 1fr;
    }
    .section-header,
    .section-tools {
        align-items: stretch;
    }
    .section-header {
        flex-direction: column;
    }
    .parse-toolbar,
    .parse-toolbar.compact-power {
        grid-template-columns: 1fr;
        gap: 10px;
    }
    .status-row {
        padding-left: 0;
    }
    .top-actions, .metric-grid, .button-grid, .electric-grid, .power-upload-grid {
        grid-template-columns: 1fr 1fr;
    }
    .flow-grid {
        grid-template-columns: 1fr;
    }
    .arrow {
        display: none;
    }
}
</style>
"""


def html(block: str) -> None:
    st.markdown(block, unsafe_allow_html=True)


def show_placeholder(name: str) -> None:
    st.toast(f"{name}：功能开发中", icon="ℹ️")


def native_button(label: str, key: str, toast: bool = True, use_container_width: bool = True) -> bool:
    if st.button(label, key=key, use_container_width=use_container_width):
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
    if st.button("跳转到文件位置", key="open_monthly_result_folder", disabled=not enabled, use_container_width=True):
        try:
            os.startfile(path)  # type: ignore[attr-defined]
            st.toast("已打开生成结果文件夹。", icon="✅")
        except OSError as exc:
            st.error(f"无法打开文件夹：{exc}")
    if enabled:
        st.caption(f"生成目录：{path}")


def render_flow(result: dict | None, has_upload: bool) -> None:
    if result:
        states = [
            ("1", "上传文件", "已完成", "done", "✓"),
            ("2", "解析数据", "已完成", "done", "✓"),
            ("3", "清洗数据", "已完成", "done", "✓"),
            ("4", "整理数据", "已完成", "done", "✓"),
        ]
    elif has_upload:
        states = [
            ("1", "上传文件", "已完成", "done", "✓"),
            ("2", "解析数据", "待开始", "todo", "◴"),
            ("3", "清洗数据", "未开始", "todo", "⌛"),
            ("4", "整理数据", "未开始", "todo", "⇩"),
        ]
    else:
        states = [
            ("1", "上传文件", "等待上传", "active", "◌"),
            ("2", "解析数据", "未开始", "todo", "◴"),
            ("3", "清洗数据", "未开始", "todo", "⌛"),
            ("4", "整理数据", "未开始", "todo", "⇩"),
        ]

    step_html = []
    for index, (num, name, status, css, icon) in enumerate(states):
        step_html.append(
            f'<div class="step {css}"><div class="num">{num}</div>'
            f'<div><div class="step-name">{name}</div><div class="step-status">{status}</div></div>'
            f'<div class="check">{icon}</div></div>'
        )
        if index < len(states) - 1:
            step_html.append('<div class="arrow">›</div>')

    html(
        f"""
<section class="flow-card">
    <div class="module-title" style="margin-bottom:12px;color:#171717;"><span style="color:#743cff;">⌘</span> 当前处理流程</div>
    <div class="flow-grid">
        {''.join(step_html)}
    </div>
</section>
"""
    )


def render_dataset_outputs(result: dict | None) -> None:
    if result:
        rows = "".join(
            f"<div class='dataset-item'><span class='check'>✓</span><div>{name}：{Path(path).name}</div></div>"
            for name, path in result["files"].items()
            if name
            in {
                "机电设施故障月报表_总表_数据",
                "机电设施故障月报表_分隧道表_数据",
                "机电日常巡查记录表_数据",
                "机电经常性检查记录表_数据",
                "隧道机电设备故障记录单_数据",
            }
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


def init_page_state() -> None:
    if "power_price_confirmed" not in st.session_state:
        st.session_state["power_price_confirmed"] = 0.85
    if "power_price_input" not in st.session_state:
        st.session_state["power_price_input"] = st.session_state["power_price_confirmed"]


def render_hero_section() -> None:
    html(
        """
<section class="hero">
    <div class="brand-row">
        <div class="brand-icon">♜</div>
        <div>
            <h1>隧道机电月报自动化系统</h1>
            <div class="subtitle">上传故障单、电费账单，自动生成总月报、单隧道月报、巡查记录、检查记录及电费统计表</div>
        </div>
    </div>
    <div class="top-actions">
        <button class="action-box" onclick="alert('系统说明：功能开发中')"><span class="icon">ⓘ</span>系统说明</button>
        <button class="action-box" onclick="alert('模板管理：功能开发中')"><span class="icon">▦</span>模板管理</button>
        <button class="action-box" onclick="alert('规则配置：功能开发中')"><span class="icon">☷</span>规则配置</button>
        <button class="action-box" onclick="alert('运行日志：功能开发中')"><span class="icon">▤</span>运行日志</button>
        <button class="action-box" onclick="alert('关于系统：功能开发中')"><span class="icon">ⓘ</span>关于系统</button>
    </div>
    <div class="status-row">
        <div class="status-pill"><span class="mini">▣</span>当前月份：2026年6月</div>
        <div class="status-pill"><span class="mini check">✓</span>模板状态：正常</div>
        <div class="status-pill"><span class="mini">▣</span>输出目录：outputs/2026-06</div>
        <div class="status-pill"><span class="mini">◴</span>当前任务：等待生成</div>
    </div>
</section>
"""
    )


def render_monthly_sections() -> tuple[dict | None, bool]:
    with st.container(key="fault_header_card"):
        with st.container(key="fault_header_box"):
            html('<div class="module-title" style="margin-bottom:2px;height:24px;display:flex;align-items:center;"><span style="color:#743cff;">▧</span> 月报处理区</div>')
            html('<div style="min-height:6px;"></div>')
            with st.container(key="fault_uploader"):
                uploaded_fault_file = st.file_uploader("上传设备维修单 Excel", type=["xlsx", "xls"], key="fault_file")
                show_upload_feedback(uploaded_fault_file, "设备维修单")

    fault_result = get_fault_result()
    has_fault_upload = uploaded_fault_file is not None or fault_result is not None

    with st.container(key="fault_parse_card"):
        html('<div class="module-title">▧ 月报解析处理区</div>')
        with st.container(key="fault_parse_panel"):
            with st.container():
                cols = st.columns([0.22, 0.16, 0.50, 0.12], gap="small")
                with cols[0]:
                    parse_clicked = native_button("开始解析", "parse_fault", toast=False, use_container_width=True)
                with cols[1]:
                    html('<div class="progress-label notranslate" translate="no" style="height:40px;display:grid;align-items:center;">月报解析进度</div>')
                with cols[2]:
                    progress_value = 100 if fault_result else (25 if has_fault_upload else 0)
                    html(f'<div style="height:40px;display:grid;align-items:center;"><div class="bar"><span style="width:{progress_value}%"></span></div></div>')
                with cols[3]:
                    html(f'<div class="percent" style="height:40px;display:grid;align-items:center;text-align:right;">{progress_value}%</div>')

            if parse_clicked:
                if not uploaded_fault_file:
                    st.warning("请先上传设备维修单 Excel。")
                else:
                    with st.spinner("正在读取、清洗并整理设备维修单数据..."):
                        fault_result = process_uploaded_fault_file(uploaded_fault_file)
                        st.session_state["fault_pipeline_result"] = fault_result
                    st.toast("设备维修单解析完成，5 份中间数据已保存。", icon="✅")
                    st.rerun()

            fault_result = get_fault_result()
            parsed_count = fault_result["fault_rows"] if fault_result else 0
            tunnel_count = fault_result["tunnel_count"] if fault_result else 0
            date_start = fault_result["date_start"] if fault_result else "待上传"
            date_end = fault_result["date_end"] if fault_result else "待上传"
            parse_status = "整理完成" if fault_result else ("等待解析" if has_fault_upload else "等待上传")
            html(
                f"""
                <div class="metric-grid">
                    <div class="metric-card"><div class="metric-icon">≡</div><div><div class="metric-label">已解析故障记录</div><div class="metric-value">{parsed_count} 条</div></div></div>
                    <div class="metric-card"><div class="metric-icon">⌂</div><div><div class="metric-label">涉及</div><div class="metric-value">{tunnel_count} 座隧道</div></div></div>
                    <div class="metric-card"><div class="metric-icon">▣</div><div><div class="metric-label">日期范围</div><div class="metric-value" style="font-size:16px;">{date_start}<br>至 {date_end}</div></div></div>
                    <div class="metric-card"><div class="metric-icon check">✓</div><div><div class="metric-label">状态</div><div class="metric-value green">{parse_status}</div></div></div>
                </div>
                """
            )
    return fault_result, has_fault_upload


def render_power_sections() -> None:
    with st.container(key="power_header_card"):
        with st.container(key="power_header_box"):
            with st.container():
                header_row = st.columns([0.36, 0.22, 0.10, 0.32], gap="small")
                with header_row[0]:
                    html('<div class="module-title" style="color:#171717;margin-bottom:2px;height:24px;display:inline-flex;align-items:center;"><span style="color:#5a39ff;">ϟ</span> 电费处理区</div>')
                with header_row[1]:
                    with st.container():
                        st.number_input(
                            "本月电费单价（元/度）",
                            min_value=0.0,
                            step=0.01,
                            format="%.2f",
                            key="power_price_input",
                            label_visibility="collapsed",
                        )
                with header_row[2]:
                    with st.container():
                        confirm_price = native_button("确定", "confirm_power_price", toast=False, use_container_width=True)
                with header_row[3]:
                    html(f'<div class="value-badge" style="margin-left:auto;justify-content:flex-start;padding-left:0;border:none;background:transparent;box-shadow:none;width:100%;text-align:left;">当前单价：{st.session_state["power_price_confirmed"]:.2f} 元/度</div>')
            with st.container():
                up1, up2 = st.columns(2, gap="small")
                with up1:
                    with st.container(key="power_uploader_last_month_table"):
                        last_month_table = st.file_uploader(
                            "上传上月电费表",
                            type=["xlsx", "xls", "pdf"],
                            key="last_month_table",
                            label_visibility="collapsed",
                        )
                        show_upload_feedback(last_month_table, "上月电费表", "电费解析功能接入后即可继续处理。")
                with up2:
                    with st.container(key="power_uploader_this_month_bill"):
                        this_month_bill = st.file_uploader(
                            "上传本月账单",
                            type=["xlsx", "xls", "pdf"],
                            key="this_month_bill",
                            label_visibility="collapsed",
                        )
                        show_upload_feedback(this_month_bill, "本月账单", "电费解析功能接入后即可继续处理。")
            if confirm_price:
                st.session_state["power_price_confirmed"] = float(st.session_state["power_price_input"])
                st.toast(f'本月电费单价已更新为 {st.session_state["power_price_confirmed"]:.2f} 元/度', icon="✅")
                st.rerun()

    with st.container(key="power_parse_card"):
        html('<div class="module-title" style="color:#171717;"><span style="color:#5a39ff;">ϟ</span> 电费解析处理区</div>')
        with st.container(key="power_parse_panel"):
            has_power_upload = bool(st.session_state.get("last_month_table") or st.session_state.get("this_month_bill"))
            power_progress_value = 25 if has_power_upload else 0
            power_status = "等待解析" if has_power_upload else "等待上传"
            with st.container():
                e1, e2, e3, e4 = st.columns([0.22, 0.16, 0.50, 0.12], gap="small")
                with e1:
                    native_button("开始解析", "parse_power", use_container_width=True)
                with e2:
                    html('<div class="progress-label notranslate" translate="no" style="height:40px;display:grid;align-items:center;">电费解析进度</div>')
                with e3:
                    html(f'<div style="height:40px;display:grid;align-items:center;"><div class="bar"><span style="width:{power_progress_value}%"></span></div></div>')
                with e4:
                    html(f'<div class="percent" style="height:40px;display:grid;align-items:center;text-align:right;">{power_progress_value}%</div>')
            html(
                f"""
                <div class="metric-grid">
                    <div class="metric-card"><div class="metric-icon check">ϟ</div><div><div class="metric-label">本月总用电量</div><div class="metric-value">待解析</div></div></div>
                    <div class="metric-card"><div class="metric-icon" style="color:#6d37ff;">￥</div><div><div class="metric-label">本月电费金额</div><div class="metric-value">待解析</div></div></div>
                    <div class="metric-card"><div class="metric-icon" style="color:#f97316;">♨</div><div><div class="metric-label">上月电费金额</div><div class="metric-value">待解析</div></div></div>
                    <div class="metric-card"><div class="metric-icon trend">↗</div><div><div class="metric-label">状态</div><div class="metric-value green">{power_status}</div></div></div>
                </div>
                """
            )


def render_generation_sections(fault_result: dict | None) -> dict | None:
    html('<div class="lower-sections">')
    lower_left, lower_right = st.columns([1, 1], gap="small")

    with lower_left:
        with st.container(key="monthly_generation_card"):
            html('<div class="module-title">▧ 月报生成</div>')
            current_result = get_monthly_generation_result(fault_result)
            selected_action: tuple[str, ...] | None = None
            button_rows = [MONTHLY_GENERATION_ACTIONS[:3], MONTHLY_GENERATION_ACTIONS[3:]]
            for button_row in button_rows:
                cols = st.columns(3, gap="small")
                for col, (category, label) in zip(cols, button_row):
                    with col:
                        clicked = st.button(
                            label,
                            key=f"gen_monthly_{category}",
                            disabled=fault_result is None,
                            use_container_width=True,
                        )
                        if clicked:
                            selected_action = DEFAULT_CATEGORIES if category == "all" else (category,)

            if selected_action:
                current_result = run_monthly_generation(fault_result, tuple(selected_action)) if fault_result else None

            render_generation_progress_box(current_result)
            html('<div class="summary-title">生成预览</div>')
            render_generation_stats(current_result)
            html('<div class="summary-title">生成结果</div>')
            render_open_result_folder_button(current_result)
    with lower_right:
        html(
            """
            <div class="soft-card lower-card">
                <div class="module-title"><span style="color:#5a39ff;">ϟ</span> 电费生成</div>
                <div class="electric-grid">
                    <div class="inner-panel">
                        <div class="summary-title">生成流程状态</div>
                        <div class="timeline">
                            <div class="timeline-item"><span class="dot"></span>待读取账单</div>
                            <div class="timeline-item"><span class="dot"></span>待计算用电量</div>
                            <div class="timeline-item"><span class="dot"></span>待套用电费单价</div>
                            <div class="timeline-item"><span class="dot"></span>待生成电费表</div>
                            <div class="timeline-item"><span class="dot"></span>生成完成</div>
                        </div>
                    </div>
                    <div>
                        <div class="inner-panel" style="margin-bottom:10px;">
                            <div class="generate-head">
                                <div class="summary-title">电费生成进度</div>
                                <div class="percent red" style="font-size:20px;">0%</div>
                            </div>
                            <div class="bar" style="margin:8px 0;"><span style="width:0%;"></span></div>
                            <div style="color:#6b7280;font-size:14px;">已完成：0 / 3 个任务</div>
                        </div>
                        <div class="inner-panel">
                            <div class="summary-title">当前输出</div>
                            <div class="output-lines">
                                文件名称：待生成<br>
                                生成时间：暂无<br>
                                状态：等待生成
                            </div>
                        </div>
                    </div>
                    <div class="electric-action">
                        <button class="large-main" onclick="alert('生成本月电费表：功能开发中')">生成本月电费表</button>
                    </div>
                </div>
            </div>
            """
        )
    html("</div>")
    return get_monthly_generation_result(fault_result)


def render_result_preview_section(fault_result: dict | None, monthly_generation_result: dict | None) -> None:
    stats = (monthly_generation_result or {}).get("category_stats") or {}
    parsed_status = "已整理待生成" if fault_result else "待整理"

    def monthly_status_for(category: str) -> str:
        item = stats.get(category)
        if item:
            return f"已生成 {item.get('file_count', 0)} 个文件"
        return parsed_status

    monthly_status = monthly_status_for("total")
    single_count = monthly_status_for("single_tunnel")
    daily_status = monthly_status_for("daily")
    frequent_status = monthly_status_for("frequent")
    record_status = monthly_status_for("fault_record")
    if not monthly_generation_result and fault_result:
        record_status = f"已整理 {fault_result['fault_rows']} 条故障记录，待生成"
    last_time = (monthly_generation_result or {}).get("generated_at") or ("已恢复最近解析结果" if fault_result else "暂无")

    html(
        f"""
<section class="result-card">
    <div class="module-title">◴ 生成结果预览</div>
    <div class="result-grid">
        <div class="result-box monthly">
            <div class="result-title">月报输出结果</div>
            <div class="result-list">
                <div><span class="check">✓</span> 总月报表数据：{monthly_status}</div>
                <div><span class="check">✓</span> 日常巡查记录表数据：{daily_status}</div>
                <div><span class="check">✓</span> 单隧道月报表数据：{single_count}</div>
                <div><span class="check">✓</span> 经常性检查记录表数据：{frequent_status}</div>
                <div><span class="check">✓</span> 设备故障记录单数据：{record_status}</div>
            </div>
            <div class="stamp">▧</div>
        </div>
        <div class="result-box power">
            <div class="result-title">电费输出结果</div>
            <div class="result-list" style="grid-template-columns:1fr;">
                <div><span class="check">✓</span> 本月电费表：待处理</div>
            </div>
            <div class="stamp">¥</div>
        </div>
    </div>
    <div class="last-time">◷ 最近一次月报结果时间：{last_time}</div>
</section>
"""
    )


def main() -> None:
    st.set_page_config(
        page_title="隧道机电月报自动化系统",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    html(CSS)
    init_page_state()
    render_hero_section()

    left, right = st.columns([1, 1], gap="small")
    with left:
        fault_result, has_fault_upload = render_monthly_sections()
    with right:
        render_power_sections()

    render_dataset_outputs(fault_result)
    render_flow(fault_result, has_fault_upload)
    monthly_generation_result = render_generation_sections(fault_result)
    render_result_preview_section(fault_result, monthly_generation_result)


if __name__ == "__main__":
    main()
