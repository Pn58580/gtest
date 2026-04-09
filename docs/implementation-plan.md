# 实施清单（可直接拆分任务）

## A. 后端任务拆分

- [ ] 初始化 FastAPI 项目与配置中心
- [ ] 初始化 SQLAlchemy 模型层与迁移（Alembic）
- [ ] 完成 JWT 登录与 RBAC 中间件
- [ ] 完成接口自动化引擎（请求构造/变量提取/断言）
- [ ] 接入 Playwright Web 执行器
- [ ] 接入 Airtest App 执行器 + ADB 设备管理
- [ ] 实现 APScheduler 调度任务与执行重试
- [ ] 实现统一报告模型与日志归档
- [ ] 实现告警通道（WebHook/邮件）

## B. 前端任务拆分

- [ ] 初始化 Vue3 + TS + Element Plus + UnoCSS
- [ ] 搭建登录、仪表盘、菜单权限
- [ ] 项目/环境/变量管理页
- [ ] 接口测试用例管理页
- [ ] Web/App 用例管理页
- [ ] 任务编排与定时任务页
- [ ] 报告详情页（日志、截图、趋势）
- [ ] 工具箱页（编解码/加解密）

## C. DevOps 与工程化

- [ ] Docker Compose 一键启动（MySQL + Redis + Backend + Frontend）
- [ ] pre-commit + Ruff + Mypy + ESLint + Vitest
- [ ] GitHub/Gitee Actions：Lint + Test + Build
- [ ] 初始化测试数据与演示项目

## D. 里程碑验收标准

- [ ] 可创建项目、环境、用例
- [ ] API/Web/App 三类至少各有 1 条执行链路打通
- [ ] 可配置定时任务并查看报告
- [ ] 权限可控制到按钮级别
- [ ] 移动端/iPad/PC 页面可用
