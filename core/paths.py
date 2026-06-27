"""Shared project path helpers."""

from config.settings import (
    BACKUPS_DIR,
    LOGS_DIR,
    OUTPUTS_DIR,
    RESOURCES_DIR,
    WORKSPACE_DIR,
)


def ensure_base_directories():
    """Return the base directories used by the application."""
    return {
        "resources": RESOURCES_DIR,
        "workspace": WORKSPACE_DIR,
        "outputs": OUTPUTS_DIR,
        "logs": LOGS_DIR,
        "backups": BACKUPS_DIR,
    }
