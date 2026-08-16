from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path
from typing import Any

try:
    import psycopg
except ImportError:  # pragma: no cover - optional during local sqlite use
    psycopg = None

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_SQLITE_PATH = BASE_DIR / "planner.db"
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_SQLITE_PATH}")


def is_postgres_url(url: str) -> bool:
    return url.startswith("postgres://") or url.startswith("postgresql://")


def get_database_url() -> str:
    return os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_SQLITE_PATH}")


def get_connection():
    if is_postgres_url(get_database_url()):
        if psycopg is None:
            raise RuntimeError("psycopg is required when DATABASE_URL points to Postgres.")
        conn = psycopg.connect(get_database_url(), autocommit=True)
        return conn

    conn = sqlite3.connect(DEFAULT_SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    if is_postgres_url(get_database_url()):
        with psycopg.connect(get_database_url()) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS planner (
                        id TEXT PRIMARY KEY,
                        data_json JSONB NOT NULL,
                        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                    )
                    """
                )
        return

    with sqlite3.connect(DEFAULT_SQLITE_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS planner (
                id TEXT PRIMARY KEY,
                data_json TEXT NOT NULL,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def list_planner_ids() -> list[str]:
    if is_postgres_url(get_database_url()):
        if psycopg is None:
            raise RuntimeError("psycopg is required when DATABASE_URL points to Postgres.")
        with psycopg.connect(get_database_url()) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM planner ORDER BY id ASC")
                rows = cur.fetchall()
                return [row[0] for row in rows]

    with sqlite3.connect(DEFAULT_SQLITE_PATH) as conn:
        rows = conn.execute("SELECT id FROM planner ORDER BY id ASC").fetchall()
        return [row[0] for row in rows]


def get_planner_record(planner_id: str) -> dict[str, Any]:
    if is_postgres_url(get_database_url()):
        if psycopg is None:
            raise RuntimeError("psycopg is required when DATABASE_URL points to Postgres.")
        with psycopg.connect(get_database_url()) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT data_json FROM planner WHERE id = %s", (planner_id,))
                row = cur.fetchone()
                if row is None:
                    return {"id": planner_id, "data": {}}
                return {"id": planner_id, "data": json.loads(row[0])}

    with sqlite3.connect(DEFAULT_SQLITE_PATH) as conn:
        row = conn.execute("SELECT data_json FROM planner WHERE id = ?", (planner_id,)).fetchone()
        if row is None:
            return {"id": planner_id, "data": {}}
        return {"id": planner_id, "data": json.loads(row[0])}


def save_planner_record(planner_id: str, payload: dict[str, Any]) -> dict[str, str]:
    if not isinstance(payload, dict):
        raise ValueError("Planner data must be a JSON object.")

    data_json = json.dumps(payload, ensure_ascii=False)

    if is_postgres_url(get_database_url()):
        if psycopg is None:
            raise RuntimeError("psycopg is required when DATABASE_URL points to Postgres.")
        with psycopg.connect(get_database_url()) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO planner (id, data_json, updated_at)
                    VALUES (%s, %s::jsonb, NOW())
                    ON CONFLICT (id)
                    DO UPDATE SET data_json = EXCLUDED.data_json, updated_at = NOW()
                    """,
                    (planner_id, data_json),
                )
        return {"id": planner_id, "status": "saved"}

    with sqlite3.connect(DEFAULT_SQLITE_PATH) as conn:
        conn.execute(
            """
            INSERT INTO planner (id, data_json, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(id) DO UPDATE SET
                data_json = excluded.data_json,
                updated_at = CURRENT_TIMESTAMP
            """,
            (planner_id, data_json),
        )
        conn.commit()
    return {"id": planner_id, "status": "saved"}
