"""Small filesystem and upload helpers."""

from __future__ import annotations

from pathlib import Path


def safe_file_name(name: str) -> str:
    """Return the final path component for a user-provided file name."""
    return Path(name).name


def format_file_size(size: int) -> str:
    """Format byte counts for compact UI display."""
    if size >= 1024 * 1024:
        return f"{size / 1024 / 1024:.2f} MB"
    if size >= 1024:
        return f"{size / 1024:.1f} KB"
    return f"{size} B"


def upload_size(uploaded_file) -> int:
    """Read an uploaded file size without assuming one Streamlit version."""
    size = getattr(uploaded_file, "size", None)
    if size is not None:
        return int(size)
    return len(uploaded_file.getvalue())


def upload_fingerprint(uploaded_file) -> str | None:
    """Return a stable enough fingerprint for the currently selected upload."""
    if uploaded_file is None:
        return None
    return f"{uploaded_file.name}:{upload_size(uploaded_file)}"

