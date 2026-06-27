# 隧道机电月报自动化系统

本项目是一个本地 Streamlit 页面系统。当前阶段已经实现：

- 首页 UI
- 设备维修单 Excel 上传
- 维修单读取、清洗、标准化
- 按后续 5 类表格生成需要整理中间数据

当前暂不生成正式 Excel 成果表。

## 当前结构

```text
app.py
pages/
  home.py
core/
  repair_orders/
    reader.py
    standardize.py
    classification.py
    text.py
    settings.py
    storage.py
    pipeline.py
  report_data/
    monthly_fault_report.py
    single_tunnel_fault_report.py
    daily_inspection.py
    frequent_inspection.py
    fault_record.py
    tunnel_manifest.py
    builder.py
    dates.py
  rules.py
  paths.py
resources/
  mappings/
    tunnels.json
  rules/
    monthly_fault_report.json
    single_tunnel_fault_report.json
    daily_inspection.json
    frequent_inspection.json
    fault_record.json
workspace/
  uploads/
  processed/
outputs/
logs/
config/
```

## 数据流程

1. 页面上传设备维修单 Excel。
2. `core.repair_orders` 读取、清洗、识别隧道、设备、时间、桩号、处置措施等字段。
3. `core.report_data` 按 5 张目标表整理中间数据。
4. 中间数据保存到 `workspace/processed/<月份>/`。

## 已生成的中间数据

处理后会生成：

- `monthly_fault_report_total.csv`：机电设施故障月报表(总表)数据
- `single_tunnel_fault_reports.csv`：机电设施故障月报表(分隧道表)数据
- `daily_inspection_records.csv`：机电日常巡查记录表数据
- `frequent_inspection_records.csv`：机电经常性检查记录表数据
- `fault_record_forms.csv`：隧道机电设备故障记录单数据
- `tunnel_manifest.csv`：隧道清单和空表标记
- `manifest.json`：本次处理清单

## 运行

```powershell
pip install -r requirements.txt
streamlit run app.py
```

也可以双击 `run.bat` 启动。
