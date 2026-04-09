# Backend 部署说明（详细版）

> 你问的重点：**需不需要 `requirements.txt`？**
>
> 结论：
> - 这个项目已经使用 `pyproject.toml` 管理依赖，**理论上不需要** `requirements.txt`。
> - 但为了传统部署/运维习惯（如 `pip install -r requirements.txt`），本仓库也提供了 `requirements.txt`，两者都可以使用。

---

## 1. 方式 A：推荐（pyproject）

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install .
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

开发模式（含 pytest）：

```bash
pip install .[dev]
pytest
```

## 2. 方式 B：传统（requirements.txt）

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 3. 生产环境变量

建议配置（可放 `.env` 或系统环境变量）：

```bash
LT_DATABASE_URL=mysql+pymysql://tester:tester123@127.0.0.1:3306/ltester
LT_JWT_SECRET=please_change_in_prod
```

## 4. 数据库初始化

应用启动时会自动执行：
- 建表（SQLAlchemy metadata）
- 初始化 admin 用户
- 初始化 demo 项目和 demo 接口用例

默认管理员：`admin / admin123`（生产环境务必修改）

## 5. Docker 部署

项目根目录：

```bash
docker compose up --build -d
```

查看日志：

```bash
docker compose logs -f backend
```

停止：

```bash
docker compose down
```
