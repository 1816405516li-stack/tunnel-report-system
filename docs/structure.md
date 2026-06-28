# 项目结构说明

项目按页面交互、核心数据处理、Excel 生成器、固定资料库和本地运行目录分层。

## 页面层

`app.py` 是 Streamlit 启动入口，实际运行 `pages/home.py`。

`pages/home.py` 只负责首页组合和页面初始化。

`pages/components/` 保存首页组件、弹窗路由、结果区块、状态管理和展示格式化函数。

`pages/components/panels/` 保存关于系统、规则中心、系统日志、标准故障预览等弹窗内容。

`pages/styles/` 保存页面 CSS。

## 服务层

`services/` 负责不依赖 Streamlit 的业务流程封装，例如上传维修单落盘、调用解析流程、调用月报生成流程。

`utils/` 保存跨层可复用的小工具函数，例如安全文件名、上传文件大小和上传指纹。

## 核心层

`core/repair_orders/` 负责把设备维修单整理成稳定的内部数据。

`core/report_data/` 负责把内部数据转换成各类月报所需的标准数据表。

## 生成层

`generators/monthly_reports/` 负责把标准数据写入 Excel 模板，生成总月报、单隧道月报、日常巡查表、经常性检查表和故障记录单。

## 资料库

`resources/` 保存长期复用材料：

- `templates/monthly/`：Excel 空白模板。
- `rules/`：各类报表生成规则。
- `mappings/`：隧道等映射表。

## 本地运行目录

`workspace/` 保存上传、预览和临时处理文件。

`outputs/` 保存生成出来的正式成果文件。

这些目录属于本机运行数据。仓库只保留 `.gitkeep` 占位文件，实际上传文件、临时文件和成果文件不上传到 GitHub。
