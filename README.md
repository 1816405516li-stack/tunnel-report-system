# 隧道机电月报自动化系统

这是一个本地运行的 Python + Streamlit 工具，用于解析设备维修单、整理隧道机电月报数据，并根据长期模板生成月度 Excel 成果文件。

## 当前能力

- 上传并解析设备维修单 Excel。
- 清洗和标准化隧道、设备、时间、桩号、故障描述、处置措施等字段。
- 生成总月报、单隧道月报、日常巡查表、经常性检查表、故障记录单所需的中间数据。
- 基于 `resources/templates/monthly/` 中的长期模板生成 Excel 成果。
- 提供标准故障预览、规则中心、系统日志等页面面板。
- 对部分文本标准化和结果展示逻辑提供自动化测试。

## 仓库结构

```text
app.py                               # Streamlit 启动入口
pages/home.py                        # 首页组合入口
pages/components/                    # 首页组件、弹窗路由和展示区块
pages/components/panels/             # 关于系统、规则中心、系统日志等弹窗内容
pages/styles/                        # 页面样式
services/                            # 不依赖页面的业务流程封装
utils/                               # 通用工具函数
config/                              # 项目配置
core/repair_orders/                  # 维修单读取、清洗、标准化和质量检查
core/report_data/                    # 月报中间数据构建
generators/monthly_reports/          # Excel 月报生成器
resources/mappings/                  # 隧道等映射
resources/rules/                     # 报表生成规则
resources/templates/monthly/         # 长期复用 Excel 模板
scripts/                             # 本地辅助脚本
tests/                               # 自动化测试
workspace/                           # 本地上传、预览和临时处理目录
outputs/                             # 本地生成成果目录
docs/                                # 项目说明文档
```

## 上传范围

本仓库上传项目代码、规则、映射、长期模板、说明文档和测试。

以下内容不上传到 GitHub：

- `永新东养护站隧道机电月报（2026.06）/`：本地月报成品资料目录。
- `outputs/` 里的实际成果文件：GitHub 只保留 `outputs/.gitkeep`，用于显示空目录。
- `workspace/` 里的运行数据：GitHub 只保留必要的 `.gitkeep` 占位文件。
- `logs/`、`backups/`、`.venv/`、`.vscode/` 等本地运行或个人环境目录。

## 数据流程

1. 在页面上传设备维修单 Excel。
2. `services.monthly_workflow` 保存上传文件并调用维修单处理流程。
3. `core.repair_orders` 读取、清洗、标准化并检查原始维修单。
4. `core.report_data` 构建月报中间数据。
5. `generators.monthly_reports` 将标准数据写入 Excel 模板。
6. 生成结果保存到本地 `outputs/`，成果文件不进入版本库。

## 运行

```powershell
pip install -r requirements.txt
streamlit run app.py
```

也可以双击 `run.bat` 启动。

## 测试

```powershell
python -m pytest
```
