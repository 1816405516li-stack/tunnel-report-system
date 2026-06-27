"""Basic project settings."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

PAGES_DIR = PROJECT_ROOT / "pages"
CORE_DIR = PROJECT_ROOT / "core"
GENERATORS_DIR = PROJECT_ROOT / "generators"
RESOURCES_DIR = PROJECT_ROOT / "resources"
WORKSPACE_DIR = PROJECT_ROOT / "workspace"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
LOGS_DIR = PROJECT_ROOT / "logs"
BACKUPS_DIR = PROJECT_ROOT / "backups"
DOCS_DIR = PROJECT_ROOT / "docs"

APP_NAME = "隧道机电月报自动化系统"
