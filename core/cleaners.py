"""Clean raw tunnel report data."""

import pandas as pd


def clean_fault_data(raw_data):
    """Drop empty rows and normalize simple text cells."""
    data = raw_data.copy()
    data = data.dropna(axis=0, how="all").dropna(axis=1, how="all")
    data.columns = [str(column).strip() for column in data.columns]
    data = data.loc[:, [column for column in data.columns if column and column != "nan"]]

    for column in data.columns:
        data[column] = data[column].map(_clean_cell)

    data = data.dropna(axis=0, how="all").reset_index(drop=True)
    data.insert(0, "source_row", data.index + 2)
    return data


def _clean_cell(value):
    if pd.isna(value):
        return pd.NA
    if isinstance(value, str):
        value = " ".join(value.replace("\u3000", " ").split())
        return value if value else pd.NA
    return value
