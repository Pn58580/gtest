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

## 3. 数据库要不要本地先创建？

### 默认方案（SQLite）
- **不需要你手动建库**。
- `LT_DATABASE_URL=sqlite:///./ltester.db` 时，应用启动会自动创建本地 `ltester.db` 文件并建表。

### MySQL 方案
- 需要数据库实例存在。
- 推荐直接用项目根目录 `docker compose up -d mysql`，Compose 会自动创建 `ltester` 数据库和用户。
- 如果你本地已有 MySQL，也可以手动创建：

```sql
CREATE DATABASE ltester DEFAULT CHARACTER SET utf8mb4;
```

## 4. 生产环境变量

建议配置（可放 `.env` 或系统环境变量）：

```bash
LT_DATABASE_URL=mysql+pymysql://tester:tester123@127.0.0.1:3306/ltester
LT_JWT_SECRET=please_change_in_prod
LT_CORS_ORIGINS=http://127.0.0.1:5173,http://localhost:5173
```

## 5. 登录失败 / OPTIONS 405 处理

如果你看到：`OPTIONS /api/v1/auth/login 405`，通常是跨域预检（CORS）问题。

处理方式：
1. 升级到当前版本（已内置 `CORSMiddleware`）。
2. 在 `.env` 中设置前端地址到 `LT_CORS_ORIGINS`。
3. 重启后端。

## 6. 数据库初始化

应用启动时会自动执行：
- 建表（SQLAlchemy metadata）
- 初始化 admin 用户
- 初始化 demo 项目和 demo 接口用例

默认管理员：`admin / admin123`（生产环境务必修改）

## 7. Docker 部署

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

## 8. 升级历史数据库报错（no such column）

如果你升级代码后看到类似：
- `no such column: api_case.expected_status`

说明你的旧 SQLite 文件是老表结构。当前版本已内置轻量自动补字段逻辑，重启后会自动尝试修复。

如果仍异常，可选方案：
1. 备份并删除旧 `ltester.db`，让系统重新建库。
2. 或使用 Alembic（后续建议）管理结构迁移。
