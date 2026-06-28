"""Load CSS used by the Streamlit home page."""

from __future__ import annotations

from pathlib import Path


CSS_PATH = Path(__file__).with_name("home.css")
CSS = CSS_PATH.read_text(encoding="utf-8")
