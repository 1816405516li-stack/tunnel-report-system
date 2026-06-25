"""Read source files into raw data objects."""

from pathlib import Path

import pandas as pd


EXCEL_SUFFIXES = {".xls", ".xlsx", ".xlsm"}


def list_excel_sheets(file_path):
    """Return worksheet names for an Excel workbook."""
    return pd.ExcelFile(file_path).sheet_names


def load_source_file(file_path, sheet_name=0):
    """Load an Excel or CSV source file into a DataFrame."""
    suffix = Path(getattr(file_path, "name", file_path)).suffix.lower()

    if suffix in EXCEL_SUFFIXES:
        return pd.read_excel(file_path, sheet_name=sheet_name, dtype=object)
    if suffix == ".csv":
        return pd.read_csv(file_path, dtype=object)

    raise ValueError(f"Unsupported source file type: {suffix or 'unknown'}")
