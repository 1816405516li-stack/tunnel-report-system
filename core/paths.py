"""Shared project path helpers."""

from config.settings import (
    BACKUPS_DIR,
    LOGS_DIR,
    OUTPUTS_DIR,
    RESOURCES_DIR,
    WORKSPACE_DIR,
)


def ensure_base_directories():
    """Placeholder for checking required directories."""
    return {
        "resources": RESOURCES_DIR,
        "workspace": WORKSPACE_DIR,
        "outputs": OUTPUTS_DIR,
        "logs": LOGS_DIR,
        "backups": BACKUPS_DIR,
    }
