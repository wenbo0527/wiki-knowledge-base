---
title: README
author: 尼克·弗瑞 🕵️
product_domain: PD-PROJECT
doc_type: 其他
tags: [projects, ai-product-management]
date: 2026-06-30
---

# AI辅助产品管理

> 项目 README - 派蒙大总管维护
> 版本：v1.4
> 更新：2026-05-28（每日更新第4次 - 07:53）

---

## 📋 项目基本信息

| 字段 | 内容 |
|------|------|
| **项目名称** | AI辅助产品管理 |
| **第一性原理目标** | 用 AI 辅助实现产品管理全流程的效率提升和质量保障 |
| **负责人** | Tony |
| **参与 Agent** | Tony（产品）、钟离（开发） |
| **当前阶段** | 🚧 开发中 |
| **创建时间** | 2026-05-26 |
| **最后更新** | 2026-05-28 07:53 |

---

## 🎯 第一性原理目标

用 AI 辅助实现产品管理全流程的效率提升和质量保障

**解决的核心问题**：
- 手工撰写 PRD，效率低
- 需求分散在多个系统，难以追踪
- 产品实践难以复用和沉淀

---

## 📦 产出物

| 产出物类型 | 路径/地址 | 说明 |
|------------|-----------|------|
| **PRD 文档** | Neo4j 图数据库 | 产品域 Epic/Feature/Story |
| **Demo 地址** | https://118.196.79.130:8443/home/ | 数字社区产品 Demo（7个应用） |
| **产品管理后端** | `/Users/wenbo/Documents/project/product_managment/` | Tony |
| **数字社区前端** | `/Users/wenbo/Documents/project/data_community/` | Tony |
| **AI查询服务** | `/Users/wenbo/Documents/project/ai-query/` | Tony |
| **portal-shell** | `/Users/wenbo/Documents/project/portal-shell/` | 钟离主仓库 |

---

## 📊 Demo 应用列表

| 应用 | URL | 状态 |
|:---|:---|:---:|
| portal-shell（统一入口） | https://118.196.79.130:8443/home/ | ✅ 43个页面全部200 |
| risk-app | https://118.196.79.130:8443/risk/ | ✅ 15个功能页面 |
| mkt-app | https://118.196.79.130:8443/mkt/ | ✅ 14个功能页面 |
| dex-app（含客户360） | https://118.196.79.130:8443/dex/ | ✅ 6个功能页面 |
| admin-app | https://118.196.79.130:8443/admin/ | ✅ 4个功能页面 |
| dmt-app | https://118.196.79.130:8443/dmt/ | ✅ 3个功能页面 |
| dfd-app | https://118.196.79.130:8443/dfd/ | ✅ 8个功能页面 |

---

## 📊 Epic 状态（来自 Neo4j）

| 状态 | 数量 | 说明 |
|:---:|---:|:---|
| DRAFT | 1 | `EPIC-RISK-EXT-ARCHIVE`（外数档案管理） |
| NULL（待修复） | 23 | 早期 Epic 无状态字段 |

⚠️ **问题**：24个 Epic 中 23个 `status=NULL`，项目进度看板无法取数。

---

## 📊 今日进展（2026-05-27）

### Tony（2026-05-27 日报）

| 完成项 | 详情 |
|:---|:---|
| SOP流程更新 | Demo-first + TDD双轨制（数字社区项目） |
| 营销画布-策略融合 交互方案 | v1.3（CDP规则构建器优化 AND/OR在条件之间） |
| Epic走查清理 | 关闭23个Epic走查任务（通过）+ 4个重复任务 |

**Demo构建清单（营销画布）**：
| 组件 | 优先级 | 说明 |
|:---|:---:|:---|
| CDPRuleBuilderForm.vue | P1 | CDP人群规则构建器 |
| SMSConfigForm.vue | P1 | 短信配置 |
| AICallConfigForm.vue | P1 | AI外呼配置（含挂短）|
| ManualCallConfigForm.vue | P1 | 人工外呼配置（含挂短）|
| CouponSelectorForm.vue | P2 | 券包选择器 |
| AppQuotaNodeConfigDrawer.vue | P2 | 营运额度节点（全新）|

**待办优先级**：
| 优先级 | 任务 | 说明 |
|:---:|:---|:---|
| P0 | 营运额度节点Demo | AppQuotaNodeConfigDrawer.vue |
| P1 | 触达渠道Demo | SMS/AICall/ManualCallConfigForm |
| P1 | CDP规则构建器Demo | CDPRuleBuilderForm.vue |
| P2 | 权益券包Demo | CouponSelectorForm.vue |

### 钟离（2026-05-27 → 2026-05-28 凌晨日报）

| 完成项 | 详情 |
|:---|:---|
| CC升级项目-S0-001: Skills健康度评估 | ✅ 完成 |
| 修复code-review成功率（50%→100%） | ✅ 完成 |
| 修复git-workflow成功率（50%→100%） | ✅ 完成 |

**P0 任务已全部清零** ✅

---

## 📊 核心教训（Tony复盘）

| 问题 | 教训 |
|:---|:---|
| Batch更新破坏了流程完整性 | 每个Epic必须单独走查后再更新状态，不能Batch处理 |
| 走查日志更新不完整 | 走查完成后必须同时：保存报告+更新任务状态+更新走查日志 |
| 跳过规范检查 | 遵守SKILL.md的Step 1-6执行流程，不跳过任何步骤 |

---

## 📊 技术债（钟离）

| 任务 | 优先级 |
|:---|:---:|
| 可访问性改进-WCAG2.1 | P2 |
| 建立统一API封装标准 | P2 |
| 激活packages共享模块 | P2 |
| mkt-app vuex迁移pinia | P2 |
| 统一Arco Design版本到2.57.0 | P2 |
| mkt-app canvas工具代码重复治理 | P2 |
| 代码注释规范落地 | P3 |
| risk-app大文件拆分 | P3 |
| dfd-app路由Hash改History | P3 |

---

## ⚠️ 阻塞问题

| 问题 | 级别 | 需要支持 |
|:---|:---:|:---|
| Epic status 全NULL（23个） | 🟠 High | 需要批量修复 |
| 触达系统Feature重建 | 🟠 High | 关联4个孤儿Feature |
| 营运额度节点Demo（P0） | 🟠 High | AppQuotaNodeConfigDrawer.vue |

---

## 👥 参与 Agent 角色

| Agent | 角色 | 职责 |
|-------|------|------|
| **Tony** | 产品负责人 | PRD编写、需求拆解、Epic走查 |
| **钟离** | 技术负责人 | 开发实现、代码规范、Demo部署 |

---

## 📊 关键里程碑

| 里程碑 | 目标日期 | 状态 |
|--------|---------|:----:|
| 客户360 v3.0 PRD | 2026-05-25 | ✅ 完成 |
| 客户360 v3.0 PRD 评审 | 2026-05-26 | ✅ 通过 |
| Epic 走查完成 | 2026-05-26 | ✅ 完成（22个） |
| SU贷PRD v1.0 | 2026-05-26 | ✅ 完成 |
| 营销画布-策略融合 交互方案 v1.3 | 2026-05-27 | ✅ 完成 |
| code-review成功率修复 | 2026-05-28 | ✅ 完成 |
| git-workflow成功率修复 | 2026-05-28 | ✅ 完成 |
| Skills健康度评估 | 2026-05-28 | ✅ 完成 |

---

## 📋 明日计划

1. **营销画布触达渠道Demo开发**（SMS/AICall/ManualCallConfigForm）
2. **CDP规则构建器Demo**（CDPRuleBuilderForm.vue）
3. **Epic status批量修复方案制定**

---

*本文件由派蒙大总管维护，每日更新*