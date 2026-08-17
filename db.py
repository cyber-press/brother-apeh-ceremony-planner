import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class VersionConflict(Exception):
    def __init__(self, current: dict[str, Any]):
        super().__init__("Planner state has changed on the server.")
        self.current = current


class PlannerStore:
    def __init__(self, database_path: str):
        self.database_path = str(Path(database_path).expanduser())

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.database_path, timeout=10, isolation_level=None)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        conn.execute("PRAGMA busy_timeout=5000;")
        return conn

    def initialize(self) -> None:
        with self.connect() as conn:
            conn.execute(
                '''
                CREATE TABLE IF NOT EXISTS planner_state (
                    planner_id TEXT PRIMARY KEY,
                    version INTEGER NOT NULL,
                    data_json TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    updated_by TEXT
                )
                '''
            )

    @staticmethod
    def _row_to_state(row: sqlite3.Row) -> dict[str, Any]:
        return {
            "planner_id": row["planner_id"],
            "version": int(row["version"]),
            "updated_at": row["updated_at"],
            "updated_by": row["updated_by"],
            "data": json.loads(row["data_json"]),
        }

    def get(self, planner_id: str) -> dict[str, Any] | None:
        with self.connect() as conn:
            row = conn.execute(
                "SELECT planner_id, version, data_json, updated_at, updated_by "
                "FROM planner_state WHERE planner_id = ?",
                (planner_id,),
            ).fetchone()
            return self._row_to_state(row) if row else None

    def put(
        self,
        planner_id: str,
        expected_version: int,
        data: dict[str, Any],
        client_name: str | None,
    ) -> dict[str, Any]:
        now = datetime.now(timezone.utc).isoformat()
        payload = json.dumps(data, separators=(",", ":"), ensure_ascii=False)

        conn = self.connect()
        try:
            conn.execute("BEGIN IMMEDIATE")
            row = conn.execute(
                "SELECT planner_id, version, data_json, updated_at, updated_by "
                "FROM planner_state WHERE planner_id = ?",
                (planner_id,),
            ).fetchone()

            if row is None:
                if expected_version != 0:
                    conn.execute("ROLLBACK")
                    raise VersionConflict({
                        "planner_id": planner_id,
                        "version": 0,
                        "updated_at": "",
                        "updated_by": None,
                        "data": {},
                    })
                version = 1
                conn.execute(
                    "INSERT INTO planner_state "
                    "(planner_id, version, data_json, updated_at, updated_by) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (planner_id, version, payload, now, client_name),
                )
            else:
                current = self._row_to_state(row)
                if int(row["version"]) != expected_version:
                    conn.execute("ROLLBACK")
                    raise VersionConflict(current)
                version = int(row["version"]) + 1
                conn.execute(
                    "UPDATE planner_state "
                    "SET version = ?, data_json = ?, updated_at = ?, updated_by = ? "
                    "WHERE planner_id = ?",
                    (version, payload, now, client_name, planner_id),
                )

            conn.execute("COMMIT")
            return {
                "planner_id": planner_id,
                "version": version,
                "updated_at": now,
                "updated_by": client_name,
                "data": data,
            }
        except Exception:
            try:
                conn.execute("ROLLBACK")
            except sqlite3.Error:
                pass
            raise
        finally:
            conn.close()
