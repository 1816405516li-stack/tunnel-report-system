# 隧道机电月报系统

这是一个本地 Streamlit 网页小系统，用于处理每月隧道机电维护资料，并按固定模板生成相关 Excel 报表。

当前阶段只搭建项目结构、目录、占位文件和基础说明文档，不实现具体业务逻辑。

## 系统目标

用户后续可以在网页中上传每月资料，系统读取、清洗、校验和整理数据后，自动生成对应月份的隧道机电月报相关文件。

## 计划支持的文件

- 初始故障单 Excel 文件
- 隧道账单表
- 往月电费表
- 长期复用的模板、基础资料、规则、映射表和依据文件

## 计划支持的成果文件

- 总月报表
- 每个单独隧道月报表
- 机电日常巡查记录表
- 机电经常性检查记录表
- 设备故障记录单
- 当月电费表

## 推荐目录结构

```text
tunnel-report-system/
├─ app.py
├─ run.bat
├─ requirements.txt
├─ README.md
├─ .gitignore
├─ pages/
├─ core/
├─ generators/
├─ resources/
├─ workspace/
├─ outputs/
├─ logs/
├─ config/
├─ backups/
└─ docs/
```

## 目录说明

- `app.py`：系统入口文件，用于启动 Streamlit 网页系统。
- `run.bat`：Windows 一键启动脚本，后续可双击启动系统。
- `requirements.txt`：Python 依赖列表。
- `pages/`：网页页面目录，放 Streamlit 的各个功能页面。
- `core/`：核心数据处理目录，负责读取、清洗、校验、标准化、拆分、计算和文件管理。
- `generators/`：Excel 生成器目录，按报表类型拆分生成逻辑。
- `resources/`：固定资料库目录，放模板、基础资料、规则、映射表和依据文件。
- `workspace/`：临时工作区目录，放每次运行时上传的文件、中间数据和预览数据。
- `outputs/`：最终输出目录，放系统生成的正式成果文件。
- `logs/`：日志目录，记录系统运行、错误和用户操作。
- `config/`：配置文件目录，放系统路径、输出命名、页面设置等配置。
- `backups/`：备份目录，用于备份模板、基础资料和重要输出结果。
- `docs/`：文档目录，放系统说明、规则说明、字段说明和更新记录。

## core 设计思路

`core` 不直接生成 Excel，它只负责把来源文件变成干净、可校验、可复用的标准数据。

- `importers.py`：读取上传的 Excel、PDF 或其他来源文件。
- `cleaners.py`：清洗空行、异常字段、日期和文本。
- `normalizers.py`：把不同来源字段统一成系统内部字段。
- `validators.py`：检查必填字段、月份、隧道名称、数量、日期范围等。
- `splitters.py`：按隧道、月份、报表类型拆分标准数据。
- `calculators.py`：做月报统计、电费对比、数量汇总等计算。
- `rules.py`：读取长期复用规则和映射。
- `models.py`：定义内部数据结构。
- `file_manager.py`：管理上传文件、中间文件、输出文件和备份。
- `paths.py`：统一管理项目路径。

这样后面业务变复杂时，页面只负责交互，生成器只负责写模板，核心规则集中在 `core`，不容易乱。

## generators 设计思路

`generators` 只负责根据清洗后的标准数据和模板生成 Excel。

- `monthly_report.py`：生成总月报表。
- `single_tunnel_report.py`：生成单独隧道月报表。
- `daily_inspection.py`：生成机电日常巡查记录表。
- `frequent_inspection.py`：生成机电经常性检查记录表。
- `fault_record.py`：生成设备故障记录单。
- `electricity_bill.py`：生成当月电费表。

## 运行方法

安装依赖：

```powershell
pip install -r requirements.txt
```

启动系统：

```powershell
streamlit run app.py
```

也可以在 Windows 中双击 `run.bat` 启动。
