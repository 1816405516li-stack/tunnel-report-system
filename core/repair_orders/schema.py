"""Shared schema for cleaned device repair-order fault records."""

STANDARD_FAULT_COLUMNS = [
    "故障编号",
    "隧道名称",
    "隧道编码",
    "故障日期",
    "故障时间",
    "故障地点",
    "设备分类",
    "设备名称",
    "故障现象",
    "故障原因",
    "处置措施",
    "派工时间",
    "到场时间",
    "计划修复时间",
    "修复时间",
    "备注",
    "故障台数",
    "更换设备台数",
    "故障天数",
    "维修人员",
    "报修人",
    "更换配件名称",
    "是否修复",
    "源表行号",
]

REPAIR_PENDING_TEXT = "已报维护组，待修复"
