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

    users = client.get('/api/v1/system/users', headers=headers)
    assert users.status_code == 200

    create_project = client.post(
        "/api/v1/project/create",
        headers=headers,
        json={"name": "One Shot Project"},
    )
    assert create_project.status_code == 200
    project_id = create_project.json()['id']

    projects = client.get("/api/v1/project/list", headers=headers)
    assert projects.status_code == 200
    assert len(projects.json()) >= 1

    run = client.post(
        "/api/v1/run",
        headers=headers,
        json={
            "project_id": project_id,
            "case_id": 1,
            "engine": "api",
            "triggered_by": "",
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

    recent = client.get('/api/v1/report/recent?limit=10', headers=headers)
    assert recent.status_code == 200
    assert len(recent.json()) >= 1

    schedule = client.post(
        "/api/v1/task/schedule/create",
        headers=headers,
        json={
            "name": "one-shot-smoke",
            "cron": "*/5 * * * *",
            "engine": "api",
            "project_id": project_id,
            "case_id": 1,
        },
    )
    assert schedule.status_code == 200
    schedule_id = schedule.json()['id']

    trigger = client.post(f"/api/v1/task/schedule/{schedule_id}/trigger", headers=headers)
    assert trigger.status_code == 200

    schedule_list = client.get("/api/v1/task/schedule/list", headers=headers)
    assert schedule_list.status_code == 200

    delete_schedule = client.delete(f"/api/v1/task/schedule/{schedule_id}", headers=headers)
    assert delete_schedule.status_code == 200

    enc = client.post('/api/v1/tool/crypto/encrypt', json={'plaintext': 'abc123'})
    assert enc.status_code == 200
    cipher = enc.json()['ciphertext']

    dec = client.post('/api/v1/tool/crypto/decrypt', json={'ciphertext': cipher})
    assert dec.status_code == 200
    assert dec.json()['plaintext'] == 'abc123'

    delete_project = client.delete(f"/api/v1/project/{project_id}", headers=headers)
    assert delete_project.status_code == 200
