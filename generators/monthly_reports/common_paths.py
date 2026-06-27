"""Paths shared by monthly report modules without importing runtime helpers."""

from config.settings import RESOURCES_DIR


TEMPLATE_DIR = RESOURCES_DIR / "templates" / "monthly"
TEMPLATE_BY_PROFILE = {
    "total": TEMPLATE_DIR / "机电设施故障月报表（总表）.xlsx",
    "single_tunnel": TEMPLATE_DIR / "机电设施故障月报表（单隧道）.xlsx",
    "daily": TEMPLATE_DIR / "机电日常巡查记录表.xlsx",
    "frequent": TEMPLATE_DIR / "机电经常性检查记录表.xlsx",
    "fault_record": TEMPLATE_DIR / "隧道机电设备故障记录单.xlsx",
}
