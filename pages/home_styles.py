"""CSS used by the Streamlit home page."""

from __future__ import annotations


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

.st-key-hero_card {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 18px;
    box-shadow: var(--shadow);
    margin: 0 0 var(--section-gap);
    padding: 20px 24px 22px;
}

.st-key-hero_card > div {
    gap: 14px;
}

.st-key-hero_card div[data-testid="stHorizontalBlock"] {
    align-items: center !important;
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

.hero h1,
.st-key-hero_card h1 {
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
    grid-template-columns: repeat(4, minmax(92px, 1fr));
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
    text-decoration: none;
    box-sizing: border-box;
}

.action-box .icon {
    display: block;
    margin-bottom: 4px;
    font-size: 22px;
}

.action-box:hover {
    border-color: #d8c6b4;
    color: #171717;
    background: rgba(255, 255, 255, 0.92);
}

.st-key-hero_action_bar {
    margin: 0;
    width: 100%;
}

.st-key-hero_action_bar div[data-testid="stHorizontalBlock"] {
    gap: 10px;
}

.st-key-hero_action_bar [data-testid="stButton"] {
    height: 58px;
}

.st-key-hero_action_bar button,
.st-key-hero_action_bar [data-testid="stBaseButton-secondary"] {
    height: 58px !important;
    min-height: 58px !important;
    width: 100% !important;
    padding: 0 !important;
    border: 1px solid #eadfd4 !important;
    border-radius: 14px !important;
    display: grid !important;
    place-items: center !important;
    text-align: center !important;
    color: #1f2937 !important;
    background: rgba(255, 255, 255, 0.72) !important;
    font-family: inherit !important;
    box-shadow: none !important;
}

.st-key-hero_action_bar button:hover,
.st-key-hero_action_bar [data-testid="stBaseButton-secondary"]:hover {
    border-color: #d8c6b4 !important;
    color: #171717 !important;
    background: rgba(255, 255, 255, 0.92) !important;
}

.st-key-hero_action_bar button p {
    white-space: pre-line !important;
    text-align: center !important;
    font-size: 13px !important;
    font-weight: 800 !important;
    line-height: 1.45 !important;
}

.st-key-hero_action_bar button p::first-line {
    font-size: 19px;
    line-height: 1.2;
}

.popup-page h2 {
    margin: 2px 0 8px;
    font-size: 28px;
    line-height: 1.2;
}

.popup-page p {
    margin: 0 0 14px;
    color: #4b5563;
    line-height: 1.75;
}

.popup-kicker {
    color: #6d5dfc;
    font-size: 14px;
    font-weight: 800;
    margin-bottom: 4px;
}

.status-row {
    grid-column: 1 / -1;
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    padding-left: 100px;
    padding-top: 24px;
    margin-top: 0;
    clear: both;
}

.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    min-height: 38px;
    height: auto;
    padding: 7px 18px;
    border: 1px solid #eadfd4;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.72);
    color: #303641;
    font-size: 14px;
    font-weight: 700;
    line-height: 1.35;
    white-space: nowrap;
    box-sizing: border-box;
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
    grid-template-columns: minmax(0, 0.9fr) minmax(0, 0.9fr) minmax(148px, 1.25fr) minmax(0, 0.95fr);
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

.metric-card > div:last-child {
    min-width: 0;
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

.metric-icon.loading {
    color: var(--blue);
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

.date-range {
    display: grid;
    gap: 3px;
    font-size: 15px;
    line-height: 1.2;
}

.date-main {
    display: flex;
    flex-wrap: wrap;
    align-items: baseline;
    gap: 4px;
    min-width: 0;
    white-space: normal;
    overflow-wrap: anywhere;
    word-break: break-word;
}

.date-main.pending {
    font-size: 18px;
}

.date-separator {
    color: #6b7280;
    font-size: 12px;
    font-weight: 700;
}

.metric-hint {
    display: block;
    color: #6b7280;
    font-size: 12px;
    font-weight: 700;
    line-height: 1.25;
}

.metric-value.green, .check {
    color: var(--green);
}

.metric-value.pending {
    color: var(--blue);
}

.metric-value.red, .trend {
    color: #ff1f1f;
}

.flow-card {
    padding: 14px 16px;
    margin: 0 0 var(--section-gap);
    position: relative;
    z-index: 0;
    width: 100%;
    box-sizing: border-box;
    clear: both;
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
    display: grid;
    grid-template-columns: minmax(0, 1fr) 24px minmax(0, 1fr) 24px minmax(0, 1fr) 24px minmax(0, 1fr);
    gap: 8px;
    align-items: stretch;
}

.step {
    min-height: 72px;
    min-width: 0;
    border: 1px solid #eee2d8;
    border-radius: 12px;
    background: #fff;
    display: grid;
    grid-template-columns: 30px minmax(0, 1fr) 24px;
    align-items: center;
    gap: 8px;
    padding: 7px 10px;
    white-space: nowrap;
    box-sizing: border-box;
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
    display: grid;
    place-items: center;
    color: #4b5563;
    font-size: 24px;
    min-width: 0;
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
    position: absolute;
    top: 76px;
    left: 0;
    right: 0;
    z-index: 2;
    white-space: pre;
    text-align: center;
    color: #111827;
    font-size: 16px;
    font-weight: 800;
    line-height: 1.55;
    padding: 0 16px;
}

.st-key-power_uploader_last_month_table div[data-testid="stFileUploader"] section::before {
    content: "上传上月电费表\\A用于核对上月电费金额和用电情况\\A.xlsx / .xls / .pdf";
    position: absolute;
    top: 58px;
    left: 0;
    right: 0;
    z-index: 2;
    white-space: pre;
    text-align: center;
    color: #111827;
    font-size: 13px;
    font-weight: 800;
    line-height: 1.35;
    padding: 0 14px;
}

.st-key-power_uploader_this_month_bill div[data-testid="stFileUploader"] section::before {
    content: "上传本月账单\\A用于生成本月电费统计表\\A.xlsx / .xls / .pdf";
    position: absolute;
    top: 58px;
    left: 0;
    right: 0;
    z-index: 2;
    white-space: pre;
    text-align: center;
    color: #111827;
    font-size: 13px;
    font-weight: 800;
    line-height: 1.35;
    padding: 0 14px;
}

.st-key-fault_uploader div[data-testid="stFileUploader"] section::after {
    content: "↥";
    position: absolute;
    top: 14px;
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
    z-index: 1;
}

.st-key-power_uploader_last_month_table div[data-testid="stFileUploader"] section::after,
.st-key-power_uploader_this_month_bill div[data-testid="stFileUploader"] section::after {
    content: "↥";
    position: absolute;
    top: 10px;
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
    height: 226px !important;
    min-height: 226px !important;
    max-height: 226px !important;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.st-key-fault_header_card > div[data-testid="stVerticalBlock"],
.st-key-fault_uploads_card > div[data-testid="stVerticalBlock"],
.st-key-power_header_card > div[data-testid="stVerticalBlock"],
.st-key-power_uploads_card > div[data-testid="stVerticalBlock"] {
    gap: 8px;
    flex: 1 1 auto;
    height: 100% !important;
    min-height: 0 !important;
    max-height: 100% !important;
}

.st-key-fault_header_box,
.st-key-power_header_box {
    flex: 0 0 206px;
    height: 206px !important;
    min-height: 206px !important;
    max-height: 206px !important;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.st-key-fault_header_box > div[data-testid="stVerticalBlock"],
.st-key-power_header_box > div[data-testid="stVerticalBlock"] {
    flex: 1 1 auto;
    height: 100% !important;
    min-height: 0 !important;
    max-height: 100% !important;
    overflow: hidden;
}

.st-key-fault_uploader div[data-testid="stFileUploader"] section {
    min-height: 150px;
}

.st-key-fault_uploader div[data-testid="stFileUploader"] section button {
    min-height: 150px;
}

.st-key-fault_parse_card,
.st-key-power_parse_card {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 18px;
    box-shadow: var(--shadow);
    padding: 14px 18px 12px;
    margin: 0 0 var(--section-gap);
    height: 252px !important;
    min-height: 252px !important;
    max-height: 252px !important;
    overflow: hidden;
}

.st-key-fault_parse_card > div[data-testid="stVerticalBlock"],
.st-key-power_parse_card > div[data-testid="stVerticalBlock"] {
    gap: 12px;
    height: 100% !important;
    min-height: 0 !important;
    max-height: 100% !important;
    overflow: hidden;
}

.st-key-fault_parse_panel,
.st-key-power_parse_panel {
    background: #ffffff;
    border: 1px solid #efe6de;
    border-radius: 14px;
    padding: 12px 14px;
    height: 178px !important;
    min-height: 178px !important;
    max-height: 178px !important;
    overflow: hidden;
}

.st-key-fault_parse_panel > div[data-testid="stVerticalBlock"],
.st-key-power_parse_panel > div[data-testid="stVerticalBlock"] {
    gap: 14px;
    height: 100% !important;
    min-height: 0 !important;
    max-height: 100% !important;
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

.st-key-preview_standard_faults .stButton > button {
    min-height: 34px;
    background: rgba(255, 255, 255, 0.82);
    color: #374151;
    border: 1px solid #eadfd4;
    box-shadow: none;
}

.st-key-preview_standard_faults .stButton > button:hover {
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
    .st-key-hero_action_bar {
        margin: 0 0 10px;
        width: 100%;
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
