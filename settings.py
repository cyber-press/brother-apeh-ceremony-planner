import os
from dataclasses import dataclass
from pathlib import Path


def _origins() -> list[str]:
    raw = os.getenv(
        "PLANNER_ALLOWED_ORIGINS",
        "http://127.0.0.1:5500,http://localhost:5500,https://cyber-press.github.io",
    )
    return [item.strip().rstrip("/") for item in raw.split(",") if item.strip()]


@dataclass(frozen=True)
class Settings:
    database_path: str = os.getenv("PLANNER_DB_PATH", "./data/planner.db")
    access_key: str = os.getenv("PLANNER_ACCESS_KEY", "change-me-before-production")
    allowed_origins: tuple[str, ...] = tuple(_origins())

    def ensure_database_parent(self) -> None:
        Path(self.database_path).expanduser().resolve().parent.mkdir(parents=True, exist_ok=True)
