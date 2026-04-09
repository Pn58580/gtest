from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def _auth_headers() -> dict[str, str]:
    login = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_project_run_report_and_schedule_flow() -> None:
    headers = _auth_headers()

    create_project = client.post(
        "/api/v1/project/create",
        headers=headers,
        json={"name": "MVP Project"},
    )
    assert create_project.status_code == 200

    projects = client.get("/api/v1/project/list", headers=headers)
    assert projects.status_code == 200
    assert len(projects.json()) >= 1

    run = client.post(
        "/api/v1/run",
        headers=headers,
        json={
            "project_id": 1,
            "case_id": 1,
            "engine": "api",
            "triggered_by": "admin",
            "params": {"base_url": "https://example.com"},
        },
    )
    assert run.status_code == 200
    run_id = run.json()["run_id"]

    report = client.get(f"/api/v1/report/{run_id}", headers=headers)
    assert report.status_code == 200
    assert report.json()["run_id"] == run_id

    schedule = client.post(
        "/api/v1/task/schedule/create",
        headers=headers,
        json={
            "name": "smoke-api",
            "cron": "*/5 * * * *",
            "engine": "api",
            "project_id": 1,
            "case_id": 1,
        },
    )
    assert schedule.status_code == 200

    schedule_list = client.get("/api/v1/task/schedule/list", headers=headers)
    assert schedule_list.status_code == 200
    assert len(schedule_list.json()) >= 1
