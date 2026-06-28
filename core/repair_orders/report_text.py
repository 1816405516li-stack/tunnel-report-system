"""Reusable report-text policies for device repair-order fields.

This module owns wording rules that should stay valid across months.  Keep
month-specific calibration out of this layer so future repair-order text is
standardized from source facts, not from one historical workbook.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

import pandas as pd


COMMA = "\u3001"
JOIN_PUNCTUATION = "\uff0c"
PILE_RE = re.compile(r"(?<![A-Z])([YZ]?K)\s*(\d{1,4})\s*\+\s*(\d{1,4})", re.IGNORECASE)


@dataclass(frozen=True)
class ReportTextPolicy:
    """Editable rules for month-agnostic report text normalization."""

    replacements: Mapping[str, str] = field(default_factory=dict)
    fallback_fault_suffix: str = "\u6545\u969c"
    duplicate_separators: str = r"[\u3001\uff0c,]{2,}"
    action_joiner: str = JOIN_PUNCTUATION


DEFAULT_POLICY = ReportTextPolicy()


def text(value: Any) -> str:
    """Return compact text while treating missing spreadsheet values as empty."""
    if value is None or pd.isna(value):
        return ""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value).strip()


def normalize_report_text(
    value: Any,
    *,
    strip_terminal_punctuation: bool = True,
    policy: ReportTextPolicy = DEFAULT_POLICY,
) -> str:
    """Normalize wording without applying month-specific substitutions."""
    output = text(value)
    for old, new in policy.replacements.items():
        output = output.replace(old, new)
    output = output.replace("++", "+")
    output = re.sub(policy.duplicate_separators, COMMA, output)
    output = re.sub(r"\s+", " ", output).strip()
    if strip_terminal_punctuation:
        output = _strip_edge_non_text(output)
    return output


def _strip_edge_non_text(value: str) -> str:
    """Strip leading/trailing punctuation or symbols without enumerating them."""
    start = 0
    end = len(value)
    while start < end and not _is_text_boundary(value[start]):
        start += 1
    while end > start and not _is_text_boundary(value[end - 1]):
        end -= 1
    return value[start:end].strip()


def _is_text_boundary(char: str) -> bool:
    category = unicodedata.category(char)
    return category.startswith("L") or category.startswith("N")


def build_fault_phenomenon(
    *,
    tunnel_name: Any,
    fault_location: Any,
    description: Any,
    device_name: Any,
    known_tunnel_names: Sequence[str] = (),
    policy: ReportTextPolicy = DEFAULT_POLICY,
) -> str:
    """Create a concise fault phenomenon from the source description.

    The summary removes duplicated tunnel and location text because those are
    already carried by separate report columns.  It deliberately avoids
    device-specific phrase tables so new months can pass through naturally.
    """
    summary = normalize_report_text(description, policy=policy)
    summary = strip_known_tunnel_names(summary, tunnel_name, known_tunnel_names, policy=policy)
    summary = strip_report_location(summary, fault_location, policy=policy)
    summary = normalize_report_text(summary, policy=policy)
    if summary:
        return summary

    fallback_device = normalize_report_text(device_name, policy=policy)
    return f"{fallback_device}{policy.fallback_fault_suffix}" if fallback_device else policy.fallback_fault_suffix


def combine_reason_and_action(
    reason: Any,
    action: Any,
    *,
    policy: ReportTextPolicy = DEFAULT_POLICY,
) -> str:
    """Combine cause and handling text without repeating equivalent wording."""
    reason_text = normalize_report_text(reason, policy=policy)
    action_text = normalize_report_text(action, policy=policy)
    if not reason_text:
        return action_text
    if not action_text:
        return reason_text
    if _contains_equivalent_phrase(action_text, reason_text):
        return action_text
    return f"{reason_text}{policy.action_joiner}{action_text}"


def strip_known_tunnel_names(
    value: str,
    tunnel_name: Any,
    known_tunnel_names: Sequence[str] = (),
    *,
    policy: ReportTextPolicy = DEFAULT_POLICY,
) -> str:
    """Remove tunnel names from wording when the tunnel is already a column."""
    output = value
    candidates = [normalize_report_text(tunnel_name, policy=policy)]
    candidates.extend(normalize_report_text(name, policy=policy) for name in known_tunnel_names)
    for candidate in sorted({item for item in candidates if item}, key=len, reverse=True):
        output = re.sub(re.escape(candidate) + r"(?!\u3001)", "", output)
    return normalize_report_text(output, policy=policy)


def strip_report_location(
    value: str,
    fault_location: Any,
    *,
    policy: ReportTextPolicy = DEFAULT_POLICY,
) -> str:
    """Remove report-location text from a phenomenon when it is duplicated."""
    summary = normalize_report_text(value, policy=policy)
    location_text = normalize_report_text(fault_location, strip_terminal_punctuation=False, policy=policy)
    if not summary or not location_text:
        return summary

    for location in _split_locations(location_text):
        summary = _remove_location_once(summary, location, policy=policy)
    return normalize_report_text(summary, policy=policy)


def _split_locations(value: str) -> list[str]:
    locations = [part.strip() for part in re.split(r"[\u3001\uff0c,;；\s]+", value) if part.strip()]
    return sorted(set(locations), key=len, reverse=True)


def _remove_location_once(
    summary: str,
    location: str,
    *,
    policy: ReportTextPolicy,
) -> str:
    if not location:
        return summary
    if summary.startswith(location):
        return normalize_report_text(summary[len(location) :], policy=policy)

    # Some source descriptions place the pile number between tunnel and event.
    # Remove only one exact location mention; leave other details untouched.
    return normalize_report_text(summary.replace(location, "", 1), policy=policy)


def _contains_equivalent_phrase(container: str, phrase: str) -> bool:
    if phrase in container:
        return True
    compact_container = re.sub(r"[\s\u3001\uff0c,.;；。]+", "", container)
    compact_phrase = re.sub(r"[\s\u3001\uff0c,.;；。]+", "", phrase)
    return bool(compact_phrase and compact_phrase in compact_container)
