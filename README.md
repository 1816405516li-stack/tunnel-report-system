# 隧道机电月报自动化系统

这是一个本地运行的 Streamlit 工具，用于整理隧道机电维修单、电费资料和长期模板，并生成月度报表数据及 Excel 成果文件。

## 当前能力

- 上传并解析设备维修单 Excel。
- 清洗、标准化维修单中的隧道、设备、时间、桩号、故障描述和处置措施等字段。
- 按规则生成 5 类月报中间数据。
- 基于长期模板生成总月报、单隧道月报、日常巡查表、经常性检查表和故障记录单。
- 对生成结果做基础打开校验。

## 仓库内容

```text
app.py                         # Streamlit 入口
pages/home.py                  # 页面和交互
config/                        # 项目配置
core/repair_orders/            # 维修单读取、清洗、标准化
core/report_data/              # 月报中间数据构建
generators/monthly_reports/    # Excel 月报生成器
resources/mappings/            # 隧道、户号等映射
resources/rules/               # 报表生成规则
resources/templates/monthly/   # 长期复用 Excel 模板
docs/                          # 项目说明文档
```

## 本地目录

以下目录只用于本机运行。GitHub 上只保留空目录占位文件，目录里的实际运行数据不上传：

- `workspace/`：上传文件、预览数据、临时处理文件。
- `outputs/`：生成出来的月报、压缩包和成果文件。
- `永新东养护站隧道机电月报（2026.06）/`：本地月报成品资料目录。

长期复用的空白模板保存在 `resources/templates/monthly/`，会随项目上传。

## 数据流程

1. 在页面上传设备维修单 Excel。
2. `core.repair_orders` 读取、清洗并标准化原始维修单。
3. `core.report_data` 生成月报中间数据。
4. `generators.monthly_reports` 把标准数据写入 Excel 模板。
5. 生成结果保存到本地 `outputs/`，成果文件不进入版本库。

## 运行

```powershell
pip install -r requirements.txt
streamlit run app.py
```

也可以双击 `run.bat` 启动。
