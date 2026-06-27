"""Generate per-tunnel 隧道机电设备故障记录单 workbooks."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font
from openpyxl.worksheet.worksheet import Worksheet

from generators.monthly_reports.common import (
    CATEGORY_LABELS,
    TEMPLATES,
    chinese_deadline_datetime,
    chinese_datetime,
    filter_by_tunnel,
    generation_progress_message,
    iter_tunnels,
    save_and_verify,
    truthy,
    tunnel_dir,
    tunnel_display_name,
)


def generate_fault_record_reports(
    run_dir: Path,
    month: str,
    data: pd.DataFrame,
    manifest: pd.DataFrame,
    artifacts: dict[str, str],
    advance: Callable[[str], None],
) -> dict[str, int | str | bool]:
    """Create one final fault-record workbook per tunnel."""
    created: list[Path] = []
    row_count = 0

    for tunnel_name, tunnel_code in iter_tunnels(manifest, data):
        tunnel_data = filter_by_tunnel(data, tunnel_name)
        row_count += len(tunnel_data)
        workbook = load_workbook(TEMPLATES["fault_record"])
        template_sheet = workbook.worksheets[0]
        while len(workbook.worksheets) > 1:
            workbook.remove(workbook.worksheets[-1])

        if tunnel_data.empty:
            sheet = template_sheet
            sheet.title = "表9.隧道机电设备故障记录单-1"
            clear_fault_record_sheet(sheet, tunnel_name, tunnel_code)
        else:
            for index, (_, row) in enumerate(tunnel_data.iterrows(), start=1):
                sheet = template_sheet if index == 1 else workbook.copy_worksheet(template_sheet)
                sheet.title = f"表9.隧道机电设备故障记录单-{index}"
                fill_fault_record_sheet(sheet, row, tunnel_name, tunnel_code)

        path = tunnel_dir(run_dir, tunnel_name, manifest) / "隧道机电设备故障记录单.xlsx"
        save_and_verify(workbook, path, TEMPLATES["fault_record"], "fault_record")
        created.append(path)
        advance(generation_progress_message("fault_record", tunnel_name))

    artifacts["fault_record"] = str(run_dir)
    return {"label": CATEGORY_LABELS["fault_record"], "file_count": len(created), "row_count": int(row_count), "ready": True}


def fill_fault_record_sheet(sheet: Worksheet, row: pd.Series, tunnel_name: str, tunnel_code: str) -> None:
    """Fill one copied fault-record sheet."""
    has_fault = bool(str(row.get("故障现象_C6", "") or "").strip())
    _set_fault_record_value(
        sheet["A2"],
        f"隧道名称：{tunnel_display_name(tunnel_name)}                                 编号：{tunnel_code}",
        14,
    )
    _set_fault_record_value(sheet["C3"], chinese_datetime(row.get("故障时间_C3")), 10)
    _set_fault_record_value(sheet["E3"], chinese_datetime(row.get("报修时间_E3")), 10)
    _set_fault_record_value(sheet["C4"], row.get("设备位置_C4", ""), 10)
    _set_fault_record_value(sheet["E4"], row.get("报修人_E4", ""), 10)
    _set_fault_record_value(sheet["C5"], row.get("设备名称_C5", ""), 10)
    _set_fault_record_value(sheet["E5"], chinese_deadline_datetime(row.get("修复时限要求_E5")), 10)
    report_block = "故障报修（ √   ）" if has_fault else "故障报修（    ）"
    _set_fault_record_value(sheet["C6"], _fault_report_block(row.get("故障现象_C6", ""), report_block), 10)
    sheet["C6"].alignment = Alignment(horizontal="left", vertical="bottom", wrap_text=True)
    _set_fault_record_value(sheet["C7"], chinese_datetime(row.get("到场时间_C7")), 10)
    _set_fault_record_value(sheet["E7"], "刘伟成、胡小军" if has_fault else "", 10)
    _set_fault_record_value(sheet["C8"], row.get("故障原因和维修记录_C8", ""), 10)
    _set_fault_record_value(sheet["C10"], row.get("备件名称_C10", ""), 10)
    _set_fault_record_value(sheet["D10"], "", 10)
    _set_fault_record_value(sheet["E10"], row.get("备件数量_E10", ""), 10)
    repaired = truthy(row.get("处理结果_已修复"))
    replaced = truthy(row.get("处理结果_更换配件"))
    _set_fault_record_value(sheet["C13"], (
        f"已修复（{_repaired_mark(repaired)}）   "
        f"更换配件（{_replacement_mark(replaced)}）   返厂维修（    ）  "
    ), 10)


def clear_fault_record_sheet(sheet: Worksheet, tunnel_name: str, tunnel_code: str) -> None:
    fill_fault_record_sheet(sheet, pd.Series(dtype=object), tunnel_name, tunnel_code)


def _set_fault_record_value(cell, value, font_size: int) -> None:
    cell.value = value
    cell.font = Font(name=_font_name(value), size=font_size)


def _font_name(value) -> str:
    text = str(value or "")
    return "宋体" if any("\u4e00" <= char <= "\u9fff" for char in text) else "Times New Roman"


def _fault_report_block(description, report_block: str) -> str:
    description_text = str(description or "").strip()
    bottom_line = f"处置措施：故障自处（    ）     {report_block} "
    if not description_text:
        return f"\n\n\n\n\n\n{bottom_line}"
    return f"\n\n\n\n\n{description_text}\n\n\n\n\n{bottom_line}"


def _repaired_mark(checked: bool) -> str:
    return "  √  " if checked else "    "


def _replacement_mark(checked: bool) -> str:
    return " √  " if checked else "    "
