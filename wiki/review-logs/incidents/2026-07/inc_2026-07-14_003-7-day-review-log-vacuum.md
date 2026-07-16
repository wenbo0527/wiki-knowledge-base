---
title: inc 2026 07 14 003 7 day review log vacuum
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, incidents, 2026-07]
date: 2026-07-15
---

# 🔴 Incident 003: review-logs 7-4~7-13 共 11 天真空（落盘≠被引用·路径错位）

| 字段 | 值 |
|:---|:---|
| **ID** | inc_2026-07-14_003 |
| **严重级别** | 🔴 Critical |
| **状态** | ✅ Closed |
| **发现时间** | 2026-07-14 13:55 |
| **发现者** | wenbo 主动疑问 "Wiki 是什么进展 好久没关心了" |
| **负责人** | nick_fury |
| **最后更新** | 2026-07-14 14:05 |

---

## 问题描述

文博 13:43 飞书问"最新 Wiki 是什么进展 好久没关心了" → nick_fury grep review-logs 发现 7-3 → 7-13 共 **11 天真空**（review-logs 子目录无新 INC/lesson）。

**最初假设**：C-3 21:00 自检 cron 失灵 / 11 天无事件发生。

**实际根因**：**事件都发生了，INC/lesson 也写了，但写在错误路径**——
- `05_AgentOutput/agent_work/Nick/INC/` （不是 Wiki review-logs）
- `05_AgentOutput/agent_work/Nick/lessons/` （不是 Wiki review-logs 子目录）
- `review-logs/` 根目录（不是 incidents/2026-07/ 子目录）
- `wiki_backup_20260523/` 备份目录（已过时）

## 影响分析

| 维度 | 真实情况 |
|:---|:---|
| **真空天数** | 11 天（7-3 → 7-13） |
| **被漏的事件** | 至少 **6 个重大 INC**（7-6 RSS 真空 7 天 / 7-8 getnote 静默失败 / 7-10 launchd 2/3 通道 5 天 / 7-12 数据 pipeline 真空 / 7-13 3 个 plist exit 1 连续 2 天 Critical） |
| **被漏的 lessons** | 至少 **L-24/L-25/L-26**（已写入 05_AgentOutput 但不在 Wiki）+ 7-8 / 7-10 / 7-12 / 7-13 的 lessons 全部未沉淀 |
| **C-3 cron** | ✅ 21:00 / 09:00 100% ratio（每天 daily 都有写，7-1 起无 alert）|
| **Wiki 索引** | 13044 chunks ✅ 正常增长（6 周 +50%） |
| **实际伤害** | **7-6 RSS 7 天真空 + 修复** 在 Wiki **找不到** —— 同类问题再发生时无法快速查"上次怎么修的" |

## 根因分析

### 双层根因

**根因 1：INC/lesson 归档路径不规范**
- 7-6 INC 写在 `/05_AgentOutput/agent_work/Nick/INC/INC-2026-07-06-001_technical_report_repeat.md`
- 7-6 lessons 写在 `/05_AgentOutput/agent_work/Nick/lessons/2026-07-06_lessons_L24-L26.md`
- Wiki `_index.md` 规定的路径是 `review-logs/incidents/YYYY-MM/` 和 `review-logs/lessons/by-agent/{agent}/`
- AGENTS.md §0 "全局路径配置" 写了"所有输出文件必须保存到 05_AgentOutput"——但 **Nick 团队 INC/lesson 不属于"输出文件"，属于 Wiki 沉淀**

**根因 2：路径检查机制缺失**
- C-3 21:00 自检 cron 只检查 `daily/` 落盘，不检查 `review-logs/` 新文档
- 没有脚本监控 review-logs 7 天/30 天有没有新 INC/lesson
- _registry.md / _nick_registry.md 没有强制更新机制

### 11 天 vacuum 期间 daily 提到的真事件

| 日期 | daily 提到的事件 | 实际 INC 沉淀 |
|:---|:---|:---|
| 7-4 | launchd 18 plist 实战验证 | ❌ 无 |
| 7-5 | INC-001 闭环 + 22 plist 日志 L-16 待办 | ❌ 无 |
| 7-6 | **INC-2026-07-06-001**（RSS 真空 7 天·B 方案修复）| ⚠️ 写在 `/05_AgentOutput/`（**不在 Wiki**）|
| 7-7 | INC-001 闭环确认 | ❌ 无 |
| 7-8 | **3 数据异常**（getnote 静默失败 / intelligence.json mock / 字段错位）| ❌ 无 |
| 7-10 | **launchd 2/3 通道 5 天持续** | ❌ 无 |
| 7-12 | **3 个 plist exit 1 + 数据 pipeline 真空** | ❌ 无 |
| 7-13 | **3 个 plist exit 1 连续 2 天 · 升级 🔴 Critical** | ❌ 无 |

### 关键问题

> **写错路径 = 等于没写**。INC 在 `/05_AgentOutput/` 时 Wiki 索引不到、AGENTS.md 不引用、7 天后根本想不起来在哪。**等于把经验扔进垃圾桶**。

## 解决措施

### 立即归档（已做 13:55-13:56）

| 文档 | 旧路径 | 新路径 |
|:---|:---|:---|
| INC-2026-07-06-001 | `/05_AgentOutput/agent_work/Nick/INC/` | `review-logs/incidents/2026-07/inc_2026-07-06-001-tech-report-repeat-rss-vacuum.md` |
| L-24/L-25/L-26 | `/05_AgentOutput/agent_work/Nick/lessons/` | `review-logs/lessons/by-agent/nick_fury/lesson-2026-07-06-rss-tech-pipeline-4-layer-bug.md` |
| INC-2026-07-14-001 | `review-logs/根` | `review-logs/incidents/2026-07/` |
| INC-2026-07-14-002 | `review-logs/根` | `review-logs/incidents/2026-07/` |
| L-28/L-29 | `review-logs/lessons/根` | `review-logs/lessons/by-agent/nick_fury/` |
| L-30 | `review-logs/lessons/根` | `review-logs/lessons/by-agent/nick_fury/` |

### 防复发（待办）

| # | 动作 | 时间 | 优先级 |
|:-:|:---|:---:|:---:|
| 1 | **L-31 沉淀**: INC/lesson 必须立即归档到 review-logs 子目录 | 立即 | 🔴 |
| 2 | **c3_daily_check.py 升级**: 21:00 cron 加 review-logs 7/30 天真空检查 | 今晚 | 🟠 |
| 3 | **AGENTS.md §0 修正**: 区分"Agent 输出文件"（05_AgentOutput）和"Wiki 沉淀"（review-logs）| 今晚 | 🟠 |
| 4 | **历史扫描**: 7-8 / 7-10 / 7-12 / 7-13 的 4 个 INC 重新写（被漏掉的）| 本周 | 🟡 |
| 5 | **建 `_nick_registry.md`**: nick 团队 lessons/INC 索引 | 已建（13:52）| ✅ |

## 关联文档

- Lesson L-28: 多源兜底必须 raise
- Lesson L-29: 自检必须区分"输出成功"和"输入真实"
- **Lesson L-31 (新增)**: INC/lesson 必须立即归档到 review-logs 子目录
- INC-001 (hardcoded 预设) / INC-002 (fetcher 算法)

---

## 后续行动

- [x] 揭穿根因: 写错路径 ≠ 没写
- [x] INC-2026-07-06-001 + L-24/L-25/L-26 归档
- [x] 今日 4 文档移到规范路径
- [x] _nick_registry.md 建立
- [x] INC-003 写盘
- [x] L-31 沉淀
- [ ] c3_daily_check.py 升级（review-logs 真空检查）
- [ ] AGENTS.md §0 修正
- [ ] 7-8 / 7-10 / 7-12 / 7-13 四个 INC 补写

---

*Created: 2026-07-14 13:55 | Updated: 2026-07-14 14:05 | Closed*
