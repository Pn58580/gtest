from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_login_and_run() -> None:
    login = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert login.status_code == 200
    assert login.json()["access_token"]

    run = client.post(
        "/api/v1/run",
        json={
            "project_id": 1,
            "case_id": 1,
            "engine": "api",
            "triggered_by": "admin",
            "params": {"base_url": "https://example.com"},
        },
    )
    assert run.status_code == 200
    body = run.json()
    assert body["engine"] == "api"
    assert body["status"] == "passed"
    assert len(body["steps"]) >= 1
