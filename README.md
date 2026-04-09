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
