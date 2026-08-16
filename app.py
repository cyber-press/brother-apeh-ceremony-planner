from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "planner.db"
DEFAULT_PLANNER_ID = "default"


class PlannerPayload(BaseModel):
    data: dict[str, Any]


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
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


app = FastAPI(title="Brother Apeh Ceremony Planner API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event() -> None:
    init_db()


@app.get("/api/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/planner/{planner_id}")
def get_planner(planner_id: str) -> dict[str, Any]:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT data_json FROM planner WHERE id = ?",
            (planner_id,),
        ).fetchone()

    if row is None:
        return {"id": planner_id, "data": {}}

    return {"id": planner_id, "data": json.loads(row["data_json"]) }


@app.post("/api/planner/{planner_id}")
def save_planner(planner_id: str, payload: PlannerPayload) -> dict[str, Any]:
    if not isinstance(payload.data, dict):
        raise HTTPException(status_code=400, detail="Planner data must be a JSON object.")

    data_json = json.dumps(payload.data, ensure_ascii=False)
    with get_connection() as conn:
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


@app.get("/")
def read_index() -> FileResponse:
    return FileResponse(BASE_DIR / "index.html")


app.mount("/", StaticFiles(directory=str(BASE_DIR), html=True), name="static")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
