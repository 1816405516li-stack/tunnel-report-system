"""Internal data models."""

from dataclasses import dataclass


@dataclass
class ReportMonth:
    """Target report month."""

    year: int
    month: int


@dataclass
class ValidationIssue:
    """One data quality issue found during preparation."""

    row: int | None
    field: str
    message: str
    severity: str = "warning"
