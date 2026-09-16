from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SQLITE_PATH = PROJECT_ROOT / "nsm.db"


def database_url() -> str:
    return f"sqlite:///{SQLITE_PATH.as_posix()}"
