---
title: CDP事件统计 · 主索引（双向检索）
author: 钟离 🏛️
product_domain: PD-DEX
doc_type: 产品-代码双向索引
tags: [cdp, 事件统计, feishu双向引用, digital-community]
date: 2026-07-20
version: v1.0
status: active
PRD_baseline: 2026-07-20-PRD-CDP事件统计v1.0-rc.1.r4.md
UI_baseline: 2026-07-20-UI修改清单-CDP事件统计demo-v1.0-rc.2.md
---

# CDP事件统计 · 主索引（PRD ↔ 代码双向检索 v1.0）

> **创建者**: 钟离（CTO 视角）
> **触发**: 文博 2026-07-20 13:55 飞书拍板"直接对接钟离 + Wiki 落库 + 支持搜索"
> **承接**: Tony Stark（PRD Owner）
> **承接方**: data_community_pm（数字社区 PM）派工 subagent 执行 3 天
> **基线**: PRD r4 + UI 修改清单 rc.2 + 部署 mkt 7-16 + dex 7-14

---

## §1 6 Feature 全景图（按规范 ID 命名）

按 **ID 命名规范 v1.0** 的 `FEAT-{域}-{Epic}-{特性}` 格式重新编号（替代 Tony 文档中的 F-001 写法）：

| 规范 ID | Tony 文档编号 | 业务名称 | 代码主文件 | mock | 部署版本 | 状态 |
|:---|:---|:---|:---|:---|:---|:---:|
| **FEAT-DEX-EVENT-001** | F-001 | 事件统计 | `apps/dex-app/.../sample-stats.vue` | `apps/dex-app/src/mock/event.ts`（9 行空）| dex 7-14 ⚠️ | 🟠 待修复 TD-4 |
| **FEAT-DEX-EVENT-003** | F-003 | 事件血缘 · 第一阶段 | `apps/dex-app/.../event-sample-stats.vue` | （同 event.ts）| dex 7-14 ⚠️ | 🟡 建议废弃 |
| **FEAT-DEX-EVENT-005** | F-005 | 事件注册预览 | `apps/dex-app/.../event-management.vue` | （同 event.ts）| dex 7-14 ⚠️ | 🟠 TD-2 阻塞 |
| **FEAT-MKT-MA-007** | F-007 | MA 任务上线校验 | `apps/mkt-app/.../marketing/tasks/index.vue` | （无 mock）| mkt 7-16 ✅ | 🟡 TD-5 部分修复 |
| **FEAT-DEX-EVENT-008** | F-008 | 虚拟事件下线校验 | `apps/dex-app/.../virtual-events.vue` | （同 event.ts）| dex 7-14 ⚠️ | 🔴 TD-1 handleOffline 未定义 |
| **FEAT-COM-TAG-009** | F-009 | 标签计算规则 | `data_community/.../tag-system/tag-management.vue` | （无 mock）| dex 7-14 ⚠️ | 🟠 TD-6 缺计算状态 |

**规范应用说明**：原 Tony 文档 F-001/F-003/... 不符合 ID 命名规范 v1.0（`FEAT-{域}-{Epic}-{特性}`）。本文档已重编号。后续 PRD 必带规范 ID。

---

## §2 双向引用入口（搜索支持）

### 2.1 从 PRD 找代码

```
搜索词 → 落库位置
─────────────────────────────────
"事件统计"  → FEAT-DEX-EVENT-001 → sample-stats.vue
"事件血缘"  → FEAT-DEX-EVENT-003 → event-sample-stats.vue (建议废弃)
"事件注册"  → FEAT-DEX-EVENT-005 → event-management.vue
"MA 上线"   → FEAT-MKT-MA-007   → mkt-app/marketing/tasks/index.vue
"下线校验"  → FEAT-DEX-EVENT-008 → virtual-events.vue
"标签计算"  → FEAT-COM-TAG-009  → tag-management.vue
```

### 2.2 从代码找 PRD

```
代码文件 → 反向定位
─────────────────────────────────
sample-stats.vue       → FEAT-DEX-EVENT-001 → PRD §3.1
event-sample-stats.vue → FEAT-DEX-EVENT-003 → PRD §3.3（建议废弃）
event-management.vue   → FEAT-DEX-EVENT-005 → PRD §3.5
marketing/tasks/index.vue → FEAT-MKT-MA-007 → PRD §3.7
virtual-events.vue     → FEAT-DEX-EVENT-008 → PRD §3.8
tag-management.vue     → FEAT-COM-TAG-009  → PRD §3.9
```

### 2.3 从 mock 找字段

```
mock 文件 → 所有引用 Feature
─────────────────────────────────
apps/dex-app/src/mock/event.ts (9 行空) → FEAT-001/003/005/008
```

---

## §3 部署版本状态（v15-2.0 第 1/5 条 cat 实证）

| 维度 | mkt | dex |
|:---|:---|:---|
| 部署路径 | `/var/www/html/mkt/` | `/var/www/html/dex/` |
| 部署时间 | **2026-07-16 15:54 +0800** ✅ | **2026-07-14 14:42 +0800** ⚠️ |
| 与 PRD r4 关系 | 拍板前 30min | 拍板前 2d |
| nginx 配置 | `location /mkt/ → :8101` | `location /dex/ → :5180` |
| 部署内容状态 | TD-5 部分修复（5 个 js 含"上线"）| TD-2 mock 不进 dist · TD-1 待 re-deploy 验证 |

**重要观察**：dex 部署陈旧（7-14），与 PRD r4（7-16 拍板）有 2 天延迟。6 Feature 在 dex 上验证 = **必须先 re-deploy**。

---

## §4 6 个未暴露的技术债（grep 实证）

按 ID 命名规范扩展：**TD-** 改为 **TD-{域}-{nnn}** 格式

| 规范 ID | 原 TD | 位置 | 影响 | 修复工期 |
|:---|:---|:---|:---|:---:|
| **TD-DEX-EVENT-001** | TD-1 | `apps/dex-app/.../virtual-events.vue:146` `@click="handleOffline(record)"` 但 script 无此定义 | 点击「下线」按钮 → Vue 报错 | 0.5d |
| **TD-DEX-EVENT-002** | TD-2 | `apps/dex-app/src/mock/event.ts`（9 行空）| sample-stats 调 getSampleStats undefined；表格永远是空 | 1.5d |
| **TD-MKT-MA-003** | TD-3 | dex-app 与 data_community 是两个不完整副本 | 双仓跑出来的效果不一致 | 1d |
| **TD-DEX-EVENT-004** | TD-4 | sample-stats.vue 是 FEAT-001 PRD 描述的 20% 实现 | 缺字段详情/Schema/格式校验/圈选溯源 | 3d（与 #2 合并）|
| **TD-MKT-MA-005** | TD-5 | mkt-app/marketing/tasks 没有「上线」按钮 | 缺 FEAT-007 demo | 3d（与 #4 合并）|
| **TD-COM-TAG-006** | TD-6 | tag-system/tag-management 没有「上线/下线」+ 计算状态 | 缺 FEAT-009 demo | 2.5d（与 #6 合并）|

---

## §5 PRD ↔ Wiki 落库关系

```
PRD 文档 → 本 Wiki 落库
─────────────────────────────────
PRD r4 §3.1 → FEAT-DEX-EVENT-001/F001-事件统计.md
PRD r4 §3.3 → FEAT-DEX-EVENT-003/F003-事件血缘.md
PRD r4 §3.5 → FEAT-DEX-EVENT-005/F005-事件注册预览.md
PRD r4 §3.7 → FEAT-MKT-MA-007/F007-MA上线校验.md
PRD r4 §3.8 → FEAT-DEX-EVENT-008/F008-虚拟事件下线校验.md
PRD r4 §3.9 → FEAT-COM-TAG-009/F009-标签计算规则.md
```

**v15-2.0 守则**：本索引文档维护"双向引用完整性" = 任何 PRD 更新必须同步本索引。

---

## §6 后续阶段（CTO 战略路径）

详见响应中的"战略分析"。

---

*钟离 🏛️ · 2026-07-20 14:14 CST · 候选 #272 v1.0 触发 + 6 Feature 落库 v1.0 · 由 data_community_pm 拆 subagent 补完 5 个 Feature 详情*