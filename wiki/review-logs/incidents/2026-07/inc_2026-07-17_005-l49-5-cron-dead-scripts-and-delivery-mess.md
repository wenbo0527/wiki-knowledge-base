---
title: inc 2026 07 17 005 l49 5 cron dead scripts and delivery mess
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, incidents, 2026-07]
date: 2026-07-17
---

# INC-2026-07-17-005: L-49.5 升级 + L-35.1 全集复查 · 揭穿 38 个 OpenClaw cron 历史遗留问题

## 现象

- **触发时间**: 2026-07-17 14:18 CST（用户授权"请修复"→ 修 wiki.monthly·refresher 揭穿更深根因）
- **发现时间**: 2026-07-17 14:21 CST（候选 #C 防退化脚本升级版揭穿 38 个问题）
- **首跑来源**: `scripts/sunday_cron_health_check.py`（升级版查 cron_jobs 全集 78 个）
- **总问题数**: 38 个（涉及 50+ 个 OpenClaw cron 的 1/2）

| 类别 | 数量 | 说明 |
|:---|:---:|:---|
| **L-49.5 死脚本** | **9 个** | disabled cron argv 指向不存在脚本 |
| **L-35.1 disabled cron delivery 错配** | **27 个** | 28 个 disabled cron 中 27 个 channel=last + to 空 |
| **L-35.1 enabled cron delivery 错配** | **2 个** | 钟离的 2 个 cron（to 没 user: 前缀）|

## 根因分析

### L-49.5 死脚本清单（9 个 argv 路径不存在）

| cron | enabled | argv 死脚本路径 |
|:--|:--:|:--|
| `bestpractice.daily.append` | ❌ | `skills/best-practice-daily/daily_append.py` |
| `morning·rss·etf·push` | ❌ | `scripts/morning_rss_etf_push.py` |
| `rss.organize` | ❌ | `skills/rss-intelligence/scripts/organizer.py` |
| `wiki.daily·expander` | ❌ | `skills/rss-intelligence/scripts/daily_expander.py` |
| `wiki.ingest` | ❌ | `skills/rss-intelligence/scripts/wiki_ingestor.py` |
| `wiki.monthly·refresher` | ❌ | `skills/rss-intelligence/scripts/monthly_refresher.py` |
| `wiki.weekly·synthesizer` | ❌ | `skills/rss-intelligence/scripts/weekly_synthesizer.py` |
| `投资纪律-每日汇总` | ❌ | `scripts/daily_investment_summary.py` |
| `投资纪律-周报` | ❌ | `scripts/daily_investment_summary.py` |

**根因**：7-1 改造时这些脚本被合并/删除/重命名，但 OpenClaw cron argv **没同步更新**——L-34 不彻底。

### L-35.1 disabled cron delivery 错配（27 个）

**根因**：7-15 INC-001 治本时只 grep 当时 enabled 的 25 个 cron delivery 错配，没查 disabled 的 28 个 disabled cron（它们当时不在视野）。这 28 个 disabled cron 中 27 个 channel=last + to 空（历史 fail-closed）。

**为什么这么多 disabled cron**：
- 7-1 改造 + 7-14 launchd → OpenClaw cron 迁移 + 7-15 INC-001 修复 期间的"禁用但没清理"
- 没有清理流程，禁用 cron 会一直留在 sqlite 里

### L-35.1 enabled cron delivery 错配（2 个 · 钟离）

- `钟离-SOP空闲探活-20260715 (e2288348-1f5e-465b-a2e1-03147c93fa23)`: mode=announce 但 to=`ou_5550e21f10a7585629e3564ca10a3446`（没 user: 前缀）
- `钟离-P0阻塞3级升级-1h-20260716 (907abd47-9f17-44a1-b98d-193fa4d251d8)`: 同上

**根因**：钟离的 cron 创建时 to 字段没加 `user:` 前缀。我（L-35.1）检测出来，但按 SOUL §4 边界守住，**不擅自改钟离的 cron**。

> ⚠️ **偏差修正（钟离 14:39 CST 实证发现）**：原报告里 ID 写成 `ou_5550...ca10`（缺末 6 位 `a3446`），正确完整 ID 是 `ou_5550e21f10a7585629e3564ca10a3446`（34 字符）。完整 ID 已按钟离反馈补齐，且钟离已用完整 ID 完成修复。

## 修复（已完成）

| # | 动作 | 时间 | 实证 |
|:--|:--|:--:|:--|
| 1 | `cron edit wiki.monthly·refresher` delivery 对齐 L-35 | 14:18 | ✅ channel=feishu, to=user:ou_xxx |
| 2 | `cron edit wiki.monthly·refresher --disable` | 14:19 | ✅ enabled=false（避免 7-30 再爆）|
| 3 | L-49 升级 → **L-49.5**（加 Path.exists() 检查脚本路径）| 14:20 | ✅ 揭穿 9 个死脚本 |
| 4 | L-35.1 升级 → 查 cron_jobs 全集（不只是 enabled）| 14:20 | ✅ 揭穿 38 个问题 |

## 教训族 L-49.5（argv 必查脚本路径存在性）

| 编号 | 教训 |
|:---|:---|
| **L-49.5.1** | cron argv 必含 4 项（原 3 项 + **脚本路径存在性**）：路径存在 + 可执行 + 无 hardcoded 时间戳/ID/用户 |
| **L-49.5.2** | 任何 cron 涉及日期/ID/用户参数必 grep `hardcoded\|fixed\|static`（防退化）|
| **L-49.5.3** | 写新 cron 必先 `python3 -c "from pathlib import Path; print(Path('<path>').exists())"` 验证 |
| **L-49.5.4** | scripts 改造必查 OpenClaw cron argv 全集（含 disabled · L-34 不彻底治本）|

## 关联

- **INC-2026-07-15-001**（OpenClaw cron 25 任务 fail-closed）—— L-35 原版（只查 enabled）
- **INC-2026-07-17-002**（etf.hegang argv 硬编码）—— L-49 原版（只查 hardcoded，没查路径）
- **INC-2026-07-17-003**（getnote delivery channel=last）—— L-35.1 原版（首跑发现的同类）
- **L-49.5**（新增 · argv 必查脚本路径存在性 · L-49 升级版）
- **scripts/sunday_cron_health_check.py**（升级版 14:20 · 集成 5 项 check：L-48/L-49.5/L-35.1/L-13.1）

## 决策点（待文博）

| 选项 | 范围 | 风险 |
|:--|:--|:--|
| **A 不修** | 等下次周日 cron 告警再处理 | 🟢 拖 2 天 |
| **B 批量删** | 9 个 disabled 死脚本 cron + 27 个 disabled delivery 错配 cron 全删 | 🟡 数据丢失风险（建议先备份 sqlite）|
| **C 部分清** | 只删 9 个 disabled 死脚本 cron（最危险）+ 保留 delivery 错配 disabled cron | 🟢 平衡 |
| **D escalate** | 把 2 个钟离的 cron 错配通过 sessions_send 给钟离 | 🟢 跨 agent 协作 |

---

## 闭环实证（2026-07-17 14:39 CST · 钟离反馈 + 双源验证）

### 钟离 L-35.1 修复回执（14:39 CST sessions_send 收悉）

钟离收到 INC-005 escalate 后，已完成 2 个 enabled cron delivery 修复：

| # | cron | job_id | 修复前 to | 修复后 to |
|:--|:--|:--|:--|:--|
| 1 | 钟离-SOP空闲探活-20260715 | `e2288348-1f5e-465b-a2e1-03147c93fa23` | `ou_5550...3446` ❌ | `user:ou_5550...3446` ✅ |
| 2 | 钟离-P0阻塞3级升级-1h-20260716 | `907abd47-9f17-44a1-b98d-193fa4d251d8` | `ou_5550...3446` ❌ | `user:ou_5550...3446` ✅ |

### Nick 双源验证（14:44 CST · L-37 + L-38 治本）

| 数据源 | 结果 |
|:--|:--|
| **gateway API**（`cron get`）| 2/2 to=`user:ou_5550e21f10a7585629e3564ca10a3446` ✅ |
| **sqlite**（cron_jobs 表 delivery_to 字段）| 2/2 to=`user:ou_5550e21f10a7585629e3564ca10a3446` ✅ |
| mode / channel / enabled | announce / feishu / true（保留未动）✅ |

### 偏差修正（L-49.8 治本）

- 原 INC-005 报告里 ID 写为 `ou_5550e21f10a7585629e3564ca10`（**缺末 6 位 a3446**）
- 钟离指出后已补完，本节上方表格的 ID 全部用完整 34 字符 open_id

### INC-005 闭环状态

| 子项 | 状态 | 闭环证据 |
|:--|:--:|:--|
| L-49.5 9 死脚本 | ✅ 已删 | 候选 #C（14:29 文博决策）|
| L-35.1 disabled cron delivery 错配 | ✅ 保留不动 | 候选 #C 决策（disabled 不发 push）|
| L-35.1 enabled cron delivery 错配（钟离）| ✅ 已修 | 双源实证 14:44 |
| INC-005 ID 偏差 | ✅ 已补完 | 钟离 14:39 反馈 |

### 关联产物

- **INC-2026-07-17-006**（决策 C 闭环 · 9 死脚本删 · 78→69 cron）
- **INC-2026-07-17-007**（INC-006 纠错 + escalate 钟离 · L-49.7）
- **lesson-2026-07-17-l49-8-id-must-be-cite-complete**（ID 引用必完整 · 本次回执驱动新增）

---

*🕵️ 尼克·弗瑞 · 2026-07-17 14:44 CST · 双源验证闭环 · 候选 #C 全集闭环*