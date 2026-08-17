from typing import Any
from pydantic import BaseModel, Field


class PlannerWrite(BaseModel):
    expected_version: int = Field(default=0, ge=0)
    data: dict[str, Any]
    client_name: str | None = Field(default=None, max_length=120)


class PlannerState(BaseModel):
    planner_id: str
    version: int
    updated_at: str
    updated_by: str | None = None
    data: dict[str, Any]


class HealthResponse(BaseModel):
    ok: bool = True
    service: str = "brother-apeh-planner-api"
