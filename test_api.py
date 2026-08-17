import os
import tempfile
from pathlib import Path

from fastapi.testclient import TestClient


def test_shared_state_and_conflict():
    with tempfile.TemporaryDirectory() as tmp:
        os.environ["PLANNER_DB_PATH"] = str(Path(tmp) / "planner.db")
        os.environ["PLANNER_ACCESS_KEY"] = "test-key"
        os.environ["PLANNER_ALLOWED_ORIGINS"] = "http://localhost:5500"

        # Import after environment is configured.
        import importlib
        import app.main as main
        importlib.reload(main)

        headers = {"X-Planner-Key": "test-key"}
        with TestClient(main.app) as client:
            assert client.get("/health").status_code == 200

            create = client.put(
                "/api/planners/brother-apeh-master",
                headers=headers,
                json={"expected_version": 0, "data": {"deceasedName": "Mathias Apeh"}},
            )
            assert create.status_code == 200
            assert create.json()["version"] == 1

            read = client.get("/api/planners/brother-apeh-master", headers=headers)
            assert read.status_code == 200
            assert read.json()["data"]["deceasedName"] == "Mathias Apeh"

            update = client.put(
                "/api/planners/brother-apeh-master",
                headers=headers,
                json={"expected_version": 1, "data": {"deceasedName": "Mathias Apeh", "title": "Mr."}},
            )
            assert update.status_code == 200
            assert update.json()["version"] == 2

            stale = client.put(
                "/api/planners/brother-apeh-master",
                headers=headers,
                json={"expected_version": 1, "data": {"title": "Dr."}},
            )
            assert stale.status_code == 409
            assert stale.json()["detail"]["current"]["version"] == 2
