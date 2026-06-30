# 数字社区项目 - Wiki 索引

**项目**: data-community
**维护者**: 派蒙（大总管）/ data_community_pm / Tony Stark
**最后更新**: 2026-06-02 17:30
**当前状态**: 权益中心 REQ-20260601-001 v2.0 冲刺完成

---

## 📁 核心文档

### 业务需求
- [REQ-20260601-001 大额低息定价折扣 v4.0](业务需求入口/REQ-20260601-001-大额低息定价折扣.md)

### 产品 PRD
- [PRD-大额低息定价折扣 v1.1](产品PRD/PRD-大额低息定价折扣v1.1.md)
- [PRD-权益中心 v1.0](产品PRD/PRD-权益中心v1.0.md)

### Demo 实现报告
- [Demo实现程度报告 v2.0 (2026-06-02 17:30)](产品PRD/Demo实现程度报告-2026-06-02-v2.md) ⭐
- [Demo实现程度报告 v1.0 (2026-06-02 14:49)](产品PRD/Demo实现程度报告-2026-06-02.md)

### 技术方案
- [权益中心架构设计](技术方案/)

---

## 📊 9 场景实现状态（v2.0）

| # | 场景 | FP | 状态 | Demo URL |
|:--:|:---|:---|:---:|:---|
| 1 | 创建定价折扣券模板 | TYPE-005 | ✅ | /benefit/template/create |
| 2 | 按产品筛选券模板 | TYPE-006 | ✅ | /benefit/template |
| 3 | 按产品查看库存 | REDEEM-005 | ✅ | /benefit/inventory |
| 4 | 产品库存预警 | REDEEM-006 | 🟡 | /benefit/inventory (轻量版) |
| 5 | 创建券包（指定产品）| GRANT-005 | ✅ | /benefit/package |
| 6 | 发放（存量作废）| GRANT-007 | ✅ | /benefit/package (弹窗) |
| 7 | 跟踪外部渠道下发结果 | REDEEM-007 | ✅ | /benefit/management (模拟按钮) |
| 8 | 主动作废 | REDEEM-008 | ✅ | /benefit/management/detail |
| 9 | 业务边界 | GRANT-006 | ⚪ | 核心系统 |

**整体完成度**: ~85% (7/9 完整 + 1 部分)

---

## 🚀 Demo 部署

- **URL**: https://118.196.79.130:8443/mkt/
- **账号**: admin / 123456
- **入口**: 营销 → 权益中心
- **状态**: ✅ 已部署 + 已验证

### 演示路径（10 分钟）
1. 营销 → 权益中心 → 券模板 → 新建 → 选「定价折扣券」→ 选产品
2. 券模板列表 → 产品筛选 → 选 JD_001 / MT_001
3. 券库存 → 产品筛选
4. 券库存 → 阈值输入 → 列表 🔴 标识
5. 券包管理 → 新建 → 选产品（必填）
6. 券包管理 → 发放 → 存量检查弹窗
7. 券管理 → 列表 → 「模拟京东回调成功」按钮
8. 券管理 → 详情 → 「作废」按钮

---

## 📋 今日变更（2026-06-02）

### v1.0 → v2.0 增量（15:00-17:30）
- 8 个 P0 任务完成（场景 5/6/7 + arch P0 修复 + 部署）
- 1 个 P1 进行中（场景 4 轻量版）

### 关键 Bug 修复
1. mkt-app 路由 + 部署路径（nginx alias 错）
2. detail.vue 路由未注册（孤儿文件）
3. scp 后权限 403
4. index.html hash 与 assets 不一致
5. mock 字段缺失（invalidated_time/product_id 等）

### 踩坑（沉淀到 PM AGENTS.md）
- 改 vue 前要确认被 import
- 部署前确认 nginx alias 路径
- scp 后必 chown + chmod
- dev 完必 curl + grep 验证

---

## 🛠️ 技术栈

- **框架**: Vue 3.4 + Vite 5 + TypeScript + Arco Design 2.55
- **状态**: Pinia / Vuex（mkt-app 仍是 vuex@3）
- **子应用**: risk/mkt/dex/admin/dmt/dfd
- **代码量**: ~41 万行 (Vue + TS)
- **部署**: 118.196.79.130:8443 (6 子应用)

---

## 🆕 v2.1 待办（6 个 P1/P2）

| 任务 | 估时 | 优先级 |
|:---|:---:|:---:|
| 场景 4 完整版（配置页 + 按产品）| 1.5h | P1 |
| 场景 6 真实 KAFKA 接收 | 2h | P1 |
| 场景 7 真实回调（非 mock）| 1.5h | P1 |
| 拆 template/create.vue 1543 行 | 2h | P1 |
| alert/ 目录补全 | 1h | P1 |
| types vs mock 字段对齐 | 1h | P2 |

---

## 👥 Agent 团队 2

| Agent | 角色 | Main Session |
|:---|:---|:---|
| data_community_pm | 项目经理 | agent:data_community_pm:main |
| data_community_arch | 架构师 | agent:data_community_arch:main |
| data_community_dev | 开发 | agent:data_community_dev:main |
| data_community_qa | QA + DevOps | agent:data_community_qa:main |
| data_community_doc | 文档 | agent:data_community_doc:main |

---

*最后更新: 2026-06-02 17:30*