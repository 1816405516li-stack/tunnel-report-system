"""Configuration for device repair-order parsing."""

from __future__ import annotations

import json
from pathlib import Path


DEFAULT_TUNNEL_CODES = {
    "石桥二号隧道": "S81360830U0110",
    "永井隧道": "S81360830U0160",
    "小湖坳隧道": "S81360827U0160",
    "梨树下隧道": "S81360827U0150",
    "高且隧道": "S81360827U0130",
    "肖家山隧道": "S81360827U0140",
    "黄坳隧道": "S81360827U0240",
    "横垄岗隧道": "S81360827U0240",
}


def load_tunnel_codes(mapping_path: str | Path | None = None) -> dict[str, str]:
    """Load tunnel names and codes from JSON, falling back to defaults."""
    if mapping_path is None:
        return dict(DEFAULT_TUNNEL_CODES)

    path = Path(mapping_path)
    if not path.exists():
        return dict(DEFAULT_TUNNEL_CODES)

    data = json.loads(path.read_text(encoding="utf-8"))
    return {str(name): str(code) for name, code in data.items()}
