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


def test_full_mvp_flow() -> None:
    headers = _auth_headers()

    me = client.get('/api/v1/auth/me', headers=headers)
    assert me.status_code == 200
    assert me.json()['username'] == 'admin'

    user_list = client.get('/api/v1/system/users', headers=headers)
    assert user_list.status_code == 200
    assert len(user_list.json()) >= 1

    create_project = client.post(
        "/api/v1/project/create",
        headers=headers,
        json={"name": "MVP Project 2"},
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

    history = client.get('/api/v1/run/history?limit=10', headers=headers)
    assert history.status_code == 200
    assert len(history.json()) >= 1

    report = client.get(f"/api/v1/report/{run_id}", headers=headers)
    assert report.status_code == 200
    assert report.json()["run_id"] == run_id

    schedule = client.post(
        "/api/v1/task/schedule/create",
        headers=headers,
        json={
            "name": "smoke-api-2",
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
