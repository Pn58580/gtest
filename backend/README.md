# Backend Quick Start

## Run locally (pyproject)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --reload
```

## Run locally (requirements.txt)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 常见问题

- **数据库需不需要手动创建？**
  - SQLite 默认不需要，会自动创建 `ltester.db`。
  - MySQL 需要库存在，推荐使用 `docker compose` 自动创建。

- **登录时报 `OPTIONS /api/v1/auth/login 405`？**
  - 这是 CORS 预检问题。
  - 在 `.env` 配置 `LT_CORS_ORIGINS=http://127.0.0.1:5173,http://localhost:5173` 后重启后端。

## Run tests

```bash
cd backend
pytest
```

更多部署细节见：`backend/DEPLOY.md`。
