from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
BOOTSTRAP_DIR = PROJECT_ROOT / "bootstrap"
RESOURCES_DIR = BOOTSTRAP_DIR / "resources"
COMMANDS_DIR = BOOTSTRAP_DIR / "commands"
SERVICES_DIR = BOOTSTRAP_DIR / "services"
UTILS_DIR = BOOTSTRAP_DIR / "utils"
LOGS_DIR = BOOTSTRAP_DIR / "logs"
