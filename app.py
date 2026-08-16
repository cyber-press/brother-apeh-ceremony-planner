from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from auth import optional_api_key_auth
from database import get_planner_record, init_db, list_planner_ids, save_planner_record

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_PLANNER_ID = os.getenv("DEFAULT_PLANNER_ID", "default")


class PlannerPayload(BaseModel):
    data: dict[str, Any]


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


@app.get("/api/planners")
def list_planners(_: str | None = Depends(optional_api_key_auth)) -> dict[str, list[str]]:
    return {"planners": list_planner_ids()}


@app.get("/api/planner/{planner_id}")
def get_planner(planner_id: str, _: str | None = Depends(optional_api_key_auth)) -> dict[str, Any]:
    return get_planner_record(planner_id)


@app.post("/api/planner/{planner_id}")
def save_planner(
    planner_id: str,
    payload: PlannerPayload,
    _: str | None = Depends(optional_api_key_auth),
) -> dict[str, Any]:
    if not isinstance(payload.data, dict):
        raise HTTPException(status_code=400, detail="Planner data must be a JSON object.")

    return save_planner_record(planner_id, payload.data)


@app.get("/")
def read_index() -> FileResponse:
    return FileResponse(BASE_DIR / "index.html")


app.mount("/", StaticFiles(directory=str(BASE_DIR), html=True), name="static")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=int(os.getenv("PORT", "8000")), reload=True)
