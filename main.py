import secrets
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from .db import PlannerStore, VersionConflict
from .schemas import HealthResponse, PlannerState, PlannerWrite
from .settings import Settings


settings = Settings()
settings.ensure_database_parent()
store = PlannerStore(settings.database_path)


@asynccontextmanager
async def lifespan(_: FastAPI):
    store.initialize()
    yield


app = FastAPI(
    title="Brother Apeh Planner API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.allowed_origins),
    allow_credentials=False,
    allow_methods=["GET", "PUT", "OPTIONS"],
    allow_headers=["Content-Type", "X-Planner-Key"],
)


def require_access_key(
    x_planner_key: str | None = Header(default=None, alias="X-Planner-Key"),
) -> None:
    if not x_planner_key or not secrets.compare_digest(x_planner_key, settings.access_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid planner access key.",
        )


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse()


@app.get(
    "/api/planners/{planner_id}",
    response_model=PlannerState,
    dependencies=[Depends(require_access_key)],
)
def get_planner(planner_id: str) -> PlannerState:
    state = store.get(planner_id)
    if state is None:
        raise HTTPException(status_code=404, detail="Planner has not been created yet.")
    return PlannerState(**state)


@app.put(
    "/api/planners/{planner_id}",
    response_model=PlannerState,
    dependencies=[Depends(require_access_key)],
)
def put_planner(planner_id: str, body: PlannerWrite) -> PlannerState:
    try:
        state = store.put(
            planner_id=planner_id,
            expected_version=body.expected_version,
            data=body.data,
            client_name=body.client_name,
        )
        return PlannerState(**state)
    except VersionConflict as exc:
        raise HTTPException(
            status_code=409,
            detail={
                "message": "Another user saved a newer copy.",
                "current": exc.current,
            },
        ) from exc
