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


def test_cors_preflight_login() -> None:
    response = client.options(
        '/api/v1/auth/login',
        headers={
            'Origin': 'http://127.0.0.1:5173',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'content-type',
        },
    )
    assert response.status_code in (200, 204)


def test_full_mvp_flow() -> None:
    headers = _auth_headers()

    create_project = client.post(
        "/api/v1/project/create",
        headers=headers,
        json={"name": "One Shot Project"},
    )
    assert create_project.status_code == 200
    project_id = create_project.json()['id']

    env_create = client.post(
        '/api/v1/env/create',
        headers=headers,
        json={
            'project_id': project_id,
            'name': 'test',
            'base_url': 'https://example.com',
            'variables_json': '{"a":1}',
        },
    )
    assert env_create.status_code == 200
    env_id = env_create.json()['id']

    env_list = client.get('/api/v1/env/list', headers=headers)
    assert env_list.status_code == 200

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

    case_run = client.post(f'/api/v1/api-case/run/{case_id}', headers=headers)
    assert case_run.status_code == 200


    web_case = client.post(
        '/api/v1/web-case/create',
        headers=headers,
        json={
            'project_id': project_id,
            'name': 'Web Smoke',
            'page_url': 'https://example.com',
            'selector': 'h1',
            'expect_text': 'Example',
        },
    )
    assert web_case.status_code == 200
    web_case_id = web_case.json()['id']

    web_run = client.post(f'/api/v1/web-case/run/{web_case_id}', headers=headers)
    assert web_run.status_code == 200
    assert web_run.json()['engine'] == 'web'


    app_case = client.post(
        '/api/v1/app-case/create',
        headers=headers,
        json={
            'project_id': project_id,
            'name': 'App Smoke',
            'device_id': 'emulator-5554',
            'script_path': 'scripts/login.air',
            'assert_keyword': 'success',
        },
    )
    assert app_case.status_code == 200
    app_case_id = app_case.json()['id']

    app_run = client.post(f'/api/v1/app-case/run/{app_case_id}', headers=headers)
    assert app_run.status_code == 200
    assert app_run.json()['engine'] == 'app'

    fail_case = client.post(
        '/api/v1/api-case/create',
        headers=headers,
        json={
            'project_id': project_id,
            'name': 'Fail Case',
            'method': 'GET',
            'path': '/not-found',
            'body': '{}',
            'expected_status': 200,
            'expected_keyword': 'ok',
        },
    )
    assert fail_case.status_code == 200
    fail_run = client.post(f"/api/v1/api-case/run/{fail_case.json()['id']}", headers=headers)
    assert fail_run.status_code == 200
    assert fail_run.json()['status'] == 'failed'

    run_id = case_run.json()['run_id']
    assert client.get(f"/api/v1/report/{run_id}", headers=headers).status_code == 200

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

    assert client.post(f"/api/v1/task/schedule/{schedule_id}/trigger", headers=headers).status_code == 200
    assert client.post('/api/v1/tool/crypto/encrypt', json={'plaintext': 'abc123'}).status_code == 200

    assert client.delete(f"/api/v1/task/schedule/{schedule_id}", headers=headers).status_code == 200
    assert client.delete(f"/api/v1/api-case/{case_id}", headers=headers).status_code == 200
    assert client.delete(f"/api/v1/web-case/{web_case_id}", headers=headers).status_code == 200
    assert client.delete(f"/api/v1/app-case/{app_case_id}", headers=headers).status_code == 200
    assert client.delete(f"/api/v1/env/{env_id}", headers=headers).status_code == 200
    assert client.delete(f"/api/v1/project/{project_id}", headers=headers).status_code == 200
