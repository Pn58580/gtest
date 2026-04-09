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

    create_project = client.post(
        "/api/v1/project/create",
        headers=headers,
        json={"name": "One Shot Project"},
    )
    assert create_project.status_code == 200
    project_id = create_project.json()['id']

    create_case = client.post(
        '/api/v1/api-case/create',
        headers=headers,
        json={
            'project_id': project_id,
            'name': 'Smoke Case',
            'method': 'GET',
            'path': '/health',
            'body': '{}',
        },
    )
    assert create_case.status_code == 200
    case_id = create_case.json()['id']

    case_list = client.get('/api/v1/api-case/list', headers=headers)
    assert case_list.status_code == 200

    case_run = client.post(f'/api/v1/api-case/run/{case_id}', headers=headers)
    assert case_run.status_code == 200

    run_id = case_run.json()['run_id']

    report = client.get(f"/api/v1/report/{run_id}", headers=headers)
    assert report.status_code == 200

    schedule = client.post(
        "/api/v1/task/schedule/create",
        headers=headers,
        json={
            "name": "one-shot-smoke",
            "cron": "*/5 * * * *",
            "engine": "api",
            "project_id": project_id,
            "case_id": case_id,
        },
    )
    assert schedule.status_code == 200
    schedule_id = schedule.json()['id']

    trigger = client.post(f"/api/v1/task/schedule/{schedule_id}/trigger", headers=headers)
    assert trigger.status_code == 200

    enc = client.post('/api/v1/tool/crypto/encrypt', json={'plaintext': 'abc123'})
    assert enc.status_code == 200

    dec = client.post('/api/v1/tool/crypto/decrypt', json={'ciphertext': enc.json()['ciphertext']})
    assert dec.status_code == 200

    assert client.delete(f"/api/v1/task/schedule/{schedule_id}", headers=headers).status_code == 200
    assert client.delete(f"/api/v1/api-case/{case_id}", headers=headers).status_code == 200
    assert client.delete(f"/api/v1/project/{project_id}", headers=headers).status_code == 200
