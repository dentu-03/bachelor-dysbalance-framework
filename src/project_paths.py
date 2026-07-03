from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

CONFIG_DIR = PROJECT_ROOT / "configs"
METADATA_DIR = PROJECT_ROOT / "metadata"
REPORTS_DIR = PROJECT_ROOT / "reports"
MODELS_DIR = PROJECT_ROOT / "models"


def ensure_project_directories() -> None:
    """Create the standard project output directories if they do not exist."""
    for path in [
        RAW_DATA_DIR,
        INTERIM_DATA_DIR,
        PROCESSED_DATA_DIR,
        CONFIG_DIR,
        METADATA_DIR,
        REPORTS_DIR,
        MODELS_DIR,
    ]:
        path.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    ensure_project_directories()
    print(f"Project root: {PROJECT_ROOT}")
