"""Internal data model placeholders."""

from dataclasses import dataclass


@dataclass
class ReportMonth:
    """Target report month."""

    year: int
    month: int
