"""Text, date, and location helpers for repair-order data."""

from __future__ import annotations

import re
from datetime import date, datetime
from typing import Any

import pandas as pd


PILE_RE = re.compile(r"(?<![A-Z])([YZ]?K)\s*(\d{1,4})\s*\+\s*(\d{1,4})", re.IGNORECASE)
TEXT_REPLACEMENTS = {
    "车都指示器": "车道指示器",
}
KNOWN_TUNNEL_NAMES = (
    "石桥二号隧道",
    "永井隧道",
    "小湖坳隧道",
    "遂川小湖坳隧道",
    "梨树下隧道",
    "高且隧道",
    "肖家山隧道",
    "黄坳隧道",
    "横垄岗隧道",
)


def clean_cell(value: Any) -> Any:
    """Clean one raw cell while preserving non-text values."""
    if pd.isna(value):
        return pd.NA
    if isinstance(value, str):
        value = " ".join(value.replace("\u3000", " ").split())
        return value if value else pd.NA
    return value


def text(value: Any) -> str:
    """Return a compact string, treating missing values as empty."""
    if value is None or pd.isna(value):
        return ""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value).strip()


def normalize_report_text(value: Any, strip_terminal_punctuation: bool = True) -> str:
    """Normalize source wording used in final report cells."""
    output = text(value)
    for old, new in TEXT_REPLACEMENTS.items():
        output = output.replace(old, new)
    output = output.replace("++", "+")
    output = re.sub(r"[、，,]{2,}", "、", output)
    output = output.strip(" \t\r\n")
    if strip_terminal_punctuation:
        output = output.rstrip("。；;，, ")
    return output


def combine_reason_and_action(reason: Any, action: Any) -> str:
    """Return the combined reason-and-action wording used outside the total report."""
    reason_text = normalize_report_text(reason)
    action_text = normalize_report_text(action)
    if reason_text and action_text and reason_text not in action_text:
        return f"{reason_text}，{action_text}"
    return action_text or reason_text


def to_datetime(value: Any) -> datetime | None:
    """Parse a source date-time value."""
    if value is None or pd.isna(value):
        return None
    parsed = pd.to_datetime(value, errors="coerce")
    if pd.isna(parsed):
        return None
    return parsed.to_pydatetime()


def to_date(value: Any) -> date | None:
    """Parse a source value into a date."""
    parsed = to_datetime(value)
    return parsed.date() if parsed else None


def format_datetime(value: datetime | None) -> str:
    """Format date-time values for CSV storage."""
    return value.strftime("%Y-%m-%d %H:%M:%S") if value else ""


def format_flow_remark(
    report_time: datetime | None,
    dispatch_time: datetime | None,
    repair_time: datetime | None,
) -> str:
    """Format monthly report remarks from repair-order flow times."""
    parts = [
        ("上报时间", report_time),
        ("接单时间", dispatch_time),
        ("修缮时间", repair_time),
    ]
    return " ".join(f"{label} {_format_compact_flow_time(value)}" for label, value in parts if value)


def normalize_tunnel_name(value: Any, tunnel_codes: dict[str, str]) -> str:
    """Normalize known tunnel aliases to the configured tunnel name."""
    raw = text(value)
    aliases = {
        "遂川小湖坳隧道": "小湖坳隧道",
        "小湖坳": "小湖坳隧道",
        "石桥二号": "石桥二号隧道",
        "永井": "永井隧道",
        "梨树下": "梨树下隧道",
        "高且": "高且隧道",
        "肖家山": "肖家山隧道",
        "黄坳": "黄坳隧道",
        "横垄岗": "横垄岗隧道",
    }
    if raw in tunnel_codes:
        return raw
    for key, name in aliases.items():
        if key in raw:
            return name
    return raw


def extract_fault_location(description: Any, pile_number: Any, direction: Any) -> str:
    """Pick the most specific YK/ZK pile location from description or device pile."""
    description_text = normalize_report_text(description, strip_terminal_punctuation=False)
    description_locations = _format_pile_matches(description_text, fallback_direction=f"{text(direction)} {description_text}")
    if description_locations:
        return "、".join(description_locations)

    pile_text = normalize_report_text(pile_number, strip_terminal_punctuation=False)
    pile_locations = _format_pile_matches(pile_text, fallback_direction=text(direction))
    if pile_locations:
        return "、".join(pile_locations)
    return pile_text


def make_fault_summary(tunnel_name: str, fault_location: str, description: Any, device_name: str) -> str:
    """Create concise monthly-report fault text without repeating tunnel/location."""
    summary = normalize_report_text(description)
    if tunnel_name:
        summary = re.sub(re.escape(tunnel_name) + r"(?!、)", "", summary)
    summary = normalize_report_text(summary)
    summary = _prefix_location_when_needed(fault_location, summary)
    return summary or f"{device_name}故障"


def extract_part_name(handling: Any) -> str:
    """Extract a simple replacement part name from handling text."""
    handling_text = text(handling)
    match = re.search(r"更换([^，。,；;、]+)", handling_text)
    if not match:
        return ""
    part = match.group(1)
    part = re.split(r"后|并|，|。|,|；|;", part)[0]
    return part.strip()


def format_month_day(value: date) -> str:
    """Format a date as M月D日."""
    return f"{value.month}月{value.day}日"


def _format_compact_flow_time(value: datetime) -> str:
    return value.strftime("%m%d%H%M")


def _format_pile_matches(value: str, fallback_direction: str | None) -> list[str]:
    locations: list[str] = []
    seen: set[str] = set()
    for match in PILE_RE.finditer(value):
        location = _format_pile_match(match, fallback_direction=fallback_direction)
        if location not in seen:
            locations.append(location)
            seen.add(location)
    return locations


def _format_pile_match(match: re.Match, fallback_direction: str | None) -> str:
    prefix, main, sub = match.groups()
    prefix = prefix.upper()
    if prefix == "K":
        prefix = _direction_prefix(fallback_direction)
    return f"{prefix}{main}+{sub}"


def _direction_prefix(direction: str | None) -> str:
    if not direction:
        return "ZK"
    cleaned = text(direction)
    upper = cleaned.upper()
    if any(word in cleaned for word in ("下行", "右洞", "右幅", "右")) or upper in {"Y", "YK"}:
        return "YK"
    if any(word in cleaned for word in ("上行", "左洞", "左幅", "左")) or upper in {"Z", "ZK"}:
        return "ZK"
    return "ZK"


def _prefix_location_when_needed(fault_location: str, summary: str) -> str:
    if not fault_location or not summary or PILE_RE.search(summary):
        return summary
    exact_or_suffix = (
        "视频图像离线",
        "情报板故障",
        "紧急电话离线",
        "紧急电话广播离线",
        "给水管线漏水",
        "车行横洞卷帘门故障",
        "射流风机故障",
        "车道指示器故障",
    )
    if summary in exact_or_suffix:
        return f"{fault_location}{summary}"
    return summary


def _mentions_multiple_tunnels(value: str) -> bool:
    return sum(1 for tunnel_name in KNOWN_TUNNEL_NAMES if tunnel_name in value) > 1
