"""Clean local runtime caches before starting the Streamlit app."""

from __future__ import annotations

import shutil
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CACHE_DIR_NAMES = {"__pycache__", ".pytest_cache"}


def main() -> None:
    """Remove only cache folders inside this project."""
    removed = 0
    for path in PROJECT_ROOT.rglob("*"):
        if not path.is_dir() or path.name not in CACHE_DIR_NAMES:
            continue
        if not _is_inside_project(path):
            continue
        shutil.rmtree(path, ignore_errors=True)
        removed += 1
    print(f"Cleaned runtime cache folders: {removed}")


def _is_inside_project(path: Path) -> bool:
    try:
        path.resolve().relative_to(PROJECT_ROOT)
    except ValueError:
        return False
    return True


if __name__ == "__main__":
    main()
