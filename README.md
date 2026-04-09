# L-Tester Pro 设计蓝图（接口 + Web + App 自动化测试平台）

> 目标：基于 **FastAPI + MySQL ORM + Airtest + Playwright + Vue3** 构建企业级自动化测试平台，覆盖接口、Web、App 全链路测试，并支持云真机、定时任务、权限与加解密工具。

## 1. 项目定位

该项目是一个“可直接落地 + 可学习二开”的前后端分离平台，重点解决：

- 接口自动化、Web 自动化、App 自动化三套能力分散的问题
- 测试任务调度、执行、报告、告警缺乏统一闭环的问题
- 多角色协作下权限隔离和资产管理困难的问题

## 2. 技术栈规划

### 后端（Python）

- FastAPI：API 网关、鉴权、任务调度入口
- MySQL + SQLAlchemy（或 SQLModel）：核心数据持久化
- APScheduler：定时任务与调度编排
- Playwright：Web 自动化执行
- Airtest + ADB：App 自动化执行及设备控制
- 自研 API 自动化引擎：接口测试用例、变量、断言、前后置处理
- 权限体系（RBAC）+ JWT：细粒度菜单/按钮级权限

### 前端（Vue3）

- Vue3 + TypeScript + Element Plus
- UnoCSS：快速样式与响应式适配
- 适配终端：Mobile / iPad / PC
- ECharts：统计看板与趋势图

## 3. 总体架构

```text
[Web / Mobile / iPad]
         |
      Vue3 UI
         |
     FastAPI API
         |
+----------------------------+
| 业务服务层（模块化）       |
| - 认证与权限              |
| - 项目/环境/变量管理      |
| - 用例管理                |
| - 任务编排与调度          |
| - 报告与告警              |
+----------------------------+
     |         |          |
  MySQL     Redis      MinIO(可选)
     |
+----------------------------------+
| 执行引擎层                        |
| - API Engine（自研）             |
| - Web Runner（Playwright）       |
| - App Runner（Airtest + ADB）    |
+----------------------------------+
```

## 4. 核心模块设计

1. **组织与权限（RBAC）**
   - 用户、角色、菜单、按钮权限、数据权限域（项目维度）

2. **项目空间**
   - 项目、环境、全局变量、密钥、测试资源（设备/浏览器配置）

3. **接口自动化模块**
   - 场景集、测试用例、步骤编排、提取器、断言器、参数化

4. **Web 自动化模块**
   - Playwright 脚本管理、录制/上传、执行配置（浏览器、分辨率、并发）

5. **App 自动化模块**
   - Airtest 脚本管理、ADB 设备列表、云真机连接、日志采集

6. **任务调度中心**
   - 立即执行、定时执行、重试策略、失败告警（企微/钉钉/邮件）

7. **测试报告中心**
   - 执行明细、截图/视频、趋势分析、失败聚类

8. **工具箱**
   - 常用编解码、签名算法（MD5/SHA/HMAC）、AES/RSA 加解密

## 5. 数据库核心模型（建议）

- `sys_user` / `sys_role` / `sys_menu` / `sys_user_role`
- `proj_project` / `proj_env` / `proj_variable`
- `api_case` / `api_case_step` / `api_assertion` / `api_extractor`
- `web_case` / `app_case`
- `device_host` / `device_instance`
- `task_plan` / `task_schedule` / `task_run`
- `report_summary` / `report_detail`
- `tool_secret`（敏感数据统一加密存储）

## 6. 后端目录建议

```text
backend/
  app/
    main.py
    core/
      config.py
      security.py
      database.py
      scheduler.py
    api/
      v1/
        auth.py
        project.py
        testcase_api.py
        testcase_web.py
        testcase_app.py
        task.py
        report.py
        tool_crypto.py
    models/
    schemas/
    services/
      auth/
      project/
      engine_api/
      engine_web/
      engine_app/
      scheduler/
    runners/
      api_runner/
      web_runner/
      app_runner/
    utils/
```

## 7. 前端目录建议

```text
frontend/
  src/
    api/
    views/
      dashboard/
      project/
      case-api/
      case-web/
      case-app/
      task/
      report/
      system/
      toolbox/
    components/
    stores/
    router/
    layouts/
    styles/
```

## 8. API 设计建议（示例）

- `POST /api/v1/auth/login`
- `GET /api/v1/project/list`
- `POST /api/v1/api-case/run`
- `POST /api/v1/web-case/run`
- `POST /api/v1/app-case/run`
- `POST /api/v1/task/schedule/create`
- `GET /api/v1/report/{run_id}`
- `POST /api/v1/tool/crypto/encrypt`

## 9. 执行链路设计（统一 Runner 协议）

- 请求入参统一为 `RunRequest`
- 执行输出统一为 `RunResult`
- 报告存储统一为 `ReportArtifact`

通过统一协议可实现：
- API/Web/App 引擎共享调度中心
- 报告格式统一，便于前端展示和趋势统计
- 可扩展插件（如性能测试 Runner）

## 10. 分阶段落地计划

### Phase 1：基础平台（2-3 周）
- 认证与 RBAC
- 项目/环境/变量管理
- 接口自动化 MVP

### Phase 2：多引擎接入（2-4 周）
- Web Playwright 执行链路
- App Airtest + 设备管理
- 统一报告中心

### Phase 3：企业化能力（2-3 周）
- 调度中心 + 告警
- 云真机与并发执行
- 操作审计、数据权限、灰度发布

## 11. 与参考源码的映射策略

你提供的参考：
- 后端：`l-tester`
- 前端：`l-vue-ui`

建议先做“模块映射表”：
1. 先将参考项目的路由、菜单、表结构抽取成清单
2. 对照本方案生成目标版本的领域模型
3. 保留可复用模块，重写执行引擎抽象层，避免强耦合

## 12. 下一步建议

1. 先初始化 monorepo（backend + frontend + docs）
2. 先打通登录、项目、接口执行、报告闭环
3. 再逐步接入 Web 和 App 引擎
4. 最后补齐云真机、告警、权限细节与高可用能力

---

如果你愿意，我可以在这个仓库下一步直接给你生成：
- FastAPI 后端骨架（含 RBAC、调度、Runner 抽象）
- Vue3 前端后台模板骨架（多端响应式）
- 初版 MySQL 表结构 SQL + 初始化脚本

## 13. 项目部署事项（Backend + Frontend）

### 13.1 环境要求

- Python 3.11+
- Node.js 20+
- MySQL 8.0+（开发阶段可先用 SQLite）
- Redis（建议，用于缓存与任务队列扩展）

### 13.2 后端部署步骤

1. 配置环境变量（建议放在 `backend/.env`）：
   - `LT_DATABASE_URL=mysql+pymysql://user:pwd@127.0.0.1:3306/ltester`
   - `LT_JWT_SECRET=please_change_me`
2. 安装依赖并启动：

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

3. 首次启动会自动建表并初始化：
   - 默认管理员：`admin / admin123`（上线前必须修改）

### 13.3 前端部署步骤

```bash
cd frontend
npm install
npm run build
```

- 构建产物在 `frontend/dist`，可由 Nginx 托管。
- 通过 `VITE_API_BASE` 指向后端地址，例如：
  - `VITE_API_BASE=https://your-domain.com/api/v1`

### 13.4 Nginx 反向代理示例

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /data/ltester/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### 13.5 上线前检查清单

- [ ] 修改默认管理员密码
- [ ] 使用 MySQL 替代 SQLite
- [ ] 配置 HTTPS 与跨域策略
- [ ] 配置日志归档与监控告警
- [ ] 压测关键接口（登录、执行、报告查询）

## 14. 当前版本已完成能力（MVP）

### 后端（已落地）

- [x] FastAPI 接口服务骨架
- [x] SQLAlchemy 持久化（用户、项目、任务、执行记录）
- [x] JWT 登录鉴权与受保护接口
- [x] API/Web/App 统一执行入口（Runner 分发）
- [x] 执行结果入库与报告查询
- [x] 定时任务创建与调度器注册
- [x] 启动自动建表 + admin/demo 数据初始化

### 前端（已落地）

- [x] Vue3 + TS + Element Plus + UnoCSS 工程初始化
- [x] 登录页 + 登录态存储
- [x] 路由守卫（未登录拦截）
- [x] 仪表盘页面
- [x] 项目管理页（列表 + 新增）
- [x] 执行中心页（触发 API/Web/App 执行并展示结果）

### 下一步（企业增强）

- [ ] 权限细化到菜单/按钮/数据域
- [ ] Airtest/Playwright 真执行器替换当前示例 Runner
- [ ] 分布式 worker 与云真机池对接
- [ ] 完整告警链路与统计看板（趋势/稳定性）

## 15. 新增完善项（本次迭代）

- 后端新增 `auth/me` 当前用户接口
- 后端新增 `system/users` 管理员用户列表接口（RBAC 角色校验）
- 后端新增 `run/history` 执行历史接口
- 前端新增“用户管理”页面（仅管理员菜单可见）
- 前端执行中心新增历史列表展示

## 16. 一步到位启动（Docker Compose）

如果你希望快速完整体验（后端 + 前端 + MySQL），可直接使用：

```bash
docker compose up --build -d
```

默认端口：
- 前端：`http://127.0.0.1:5173`
- 后端：`http://127.0.0.1:8000`
- MySQL：`127.0.0.1:3306`

建议启动后执行以下验证：
1. 登录 `admin/admin123`
2. 创建项目
3. 执行一次 API 用例
4. 查看执行历史与报告
5. 创建定时任务并手动触发

## 17. 本次继续完善（具体项目能力）

- 新增“接口用例管理”模块：接口用例 CRUD + 一键执行
- 新增后端 `api-case` 相关接口：`/api-case/list|create|run/{id}|delete`
- 前端新增“接口用例”页面并接入后端
- 后端部署文档补充到 `backend/DEPLOY.md`，并提供 `requirements.txt` 兼容传统部署

## 18. 常见启动问题

### Q1: 数据库需要我手动创建吗？
- 默认 SQLite：不需要，启动自动创建。
- 使用 MySQL：建议用 docker-compose 自动创建，或手动 `CREATE DATABASE ltester;`。

### Q2: 登录时报 `OPTIONS /api/v1/auth/login 405`
- 这是前后端跨域预检请求。
- 当前版本已内置 CORS 中间件。
- 请在后端 `.env` 增加：
  - `LT_CORS_ORIGINS=http://127.0.0.1:5173,http://localhost:5173`
- 然后重启后端服务。

## 19. 继续完善（环境管理模块）

本次新增了“环境管理（Environment）”能力：
- 后端新增环境管理接口：`/api/v1/env/list|create|delete`
- 启动自动为首个项目注入默认环境（dev）
- 前端新增“环境管理”页面并接入 CRUD

这样 API 用例、执行中心、定时任务都可以逐步接入环境维度能力。

## 20. 继续完善（接口断言能力）

- 接口用例新增断言字段：`expected_status`、`expected_keyword`
- API Runner 新增模拟断言步骤：状态码断言 + 关键字断言
- 前端接口用例页面支持配置断言并展示执行通过/失败
