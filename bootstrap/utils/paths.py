from pathlib import Path

file_path = Path(__file__).resolve()
file_path_p1 = file_path.parent
file_path_p2 = file_path_p1.parent
file_path_p3 = file_path_p2.parent

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
BOOTSTRAP_DIR = PROJECT_ROOT / "bootstrap"
RESOURCES_DIR = BOOTSTRAP_DIR / "resources"
COMMANDS_DIR = BOOTSTRAP_DIR / "commands"
SERVICES_DIR = BOOTSTRAP_DIR / "services"
UTILS_DIR = BOOTSTRAP_DIR / "utils"
LOGS_DIR = BOOTSTRAP_DIR / "logs"

print(f"Project root: {PROJECT_ROOT}")
print(f"__file__ path resolve: {file_path}")
print(f"__file__ path p1: {file_path_p1}")
print(f"__file__ path p2: {file_path_p2}")
print(f"__file__ path p3: {file_path_p3}")