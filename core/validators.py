"""Validate cleaned and normalized data."""

from core.models import ValidationIssue


REQUIRED_FIELDS = {
    "tunnel_name": "隧道名称",
    "fault_time": "故障时间",
    "device_name": "设备名称",
    "fault_description": "故障描述",
}


def validate_month_data(month_data):
    """Return data quality issues for normalized monthly fault data."""
    issues = []

    for field, label in REQUIRED_FIELDS.items():
        if field not in month_data.columns:
            issues.append(ValidationIssue(None, field, f"缺少字段：{label}", "error"))
            continue

        missing_rows = month_data[month_data[field].isna()]["source_row"].tolist()
        for row in missing_rows[:20]:
            issues.append(ValidationIssue(int(row), field, f"{label}为空", "error"))
        if len(missing_rows) > 20:
            issues.append(ValidationIssue(None, field, f"{label}还有 {len(missing_rows) - 20} 行为空", "warning"))

    if {"fault_time", "repair_time"}.issubset(month_data.columns):
        repaired_before_fault = month_data[
            month_data["fault_time"].notna()
            & month_data["repair_time"].notna()
            & (month_data["repair_time"] < month_data["fault_time"])
        ]
        for _, row in repaired_before_fault.iterrows():
            issues.append(ValidationIssue(int(row["source_row"]), "repair_time", "修复时间早于故障时间", "error"))

    return issues
