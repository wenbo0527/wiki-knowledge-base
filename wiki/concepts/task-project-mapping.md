---
title: task project mapping
author: 尼克·弗瑞 🕵️
product_domain: PD-CONCEPT
doc_type: 其他
tags: [concepts]
date: 2026-06-30
---

# 任务项目标记规范 v1.1

> **制定日期**: 2026-05-27
> **制定者**: 派蒙（大总管）
> **状态**: ✅ 已确认

---

## 📋 背景

2026-05-27 文博确认了5个项目体系 + 日志复盘机制。

---

## 🎯 5个官方项目

| 项目ID | 项目名称 | 负责人 | 说明 |
|:------|:---------|:------|:-----|
| `AI-PM` | AI辅助产品管理 | Tony | 产品PRD、Demo、功能开发 |
| `AI-TRANSITION` | 文博的AI转型之路 | Nick | 简历、行业研究、能力展示 |
| `KB` | 知识底座 | Nick | Wiki整理、情报收集、日志记录 |
| `AI-OUTPUT` | AI能力输出 | 待定 | ~~Nick不做，2026-05-27确认~~ |
| `AGENT-INFRA` | Agent底座维护 | 派蒙 | Agent通信、Skill管理、技术债、CC升级 |

---

## 🏷️ 标签→项目映射表

| 现有标签 | → | 归属项目 | 说明 |
|---------|---|---------|:-----|
| Epic走查 | | AI-PM | Epic走查是产品管理工作 |
| PRD相关 | | AI-PM | PRD是产品管理产出 |
| 客户360 | | AI-PM | 客户360是产品功能 |
| 问小数 | | AI-PM | 问小数是产品Demo功能 |
| Demo Trace | | AI-PM | Demo是产品展示 |
| 人工电销 | | AI-PM | 人工电销是产品功能 |
| 简历v1.x | | AI-TRANSITION | 简历是转型展示 |
| 行业研究 | | AI-TRANSITION | 行业研究是转型能力 |
| Wiki整理 | | KB | Wiki是知识管理 |
| Nick-晨间/日间/每日 | | KB | 情报收集是知识输入 |
| ~~Nick-每周~~ | → | ~~NICK-OUTPUT~~ | 输出找其他工具，Nick只做输入 |
| GET笔记 | | KB | GET笔记是知识输入 |
| CC升级项目 | | AGENT-INFRA | CC框架是Agent协作基础设施 |
| Phase-X | | AGENT-INFRA | Skill是Agent能力单元 |
| 技术债 | | AGENT-INFRA | 技术债属于基础设施维护 |
| code-review/修复 | | AGENT-INFRA | Agent Skill修复 |
| git-workflow/修复 | | AGENT-INFRA | Agent Skill修复 |

---

## 📝 日志/复盘机制（2026-05-27 新增）

### 共享只读目录

| 目录 | 路径 | 说明 |
|:-----|:-----|:-----|
| 共享根目录 | `~/.openclaw/memory_share/` | 软链接集中管理 |
| 派蒙 | `memory_share/paimon_daily` | 只读 |
| Tony | `memory_share/tony_daily` | 只读 |
| Nick | `memory_share/nick_daily` | 只读 |
| 钟离 | `memory_share/zhongli_daily` | 只读 |
| 阿加莘 | `memory_share/agatha_daily` | 只读 |
| 老六 | `memory_share/laoliu_daily` | 只读 |

### 落地流程

```
1. 各Agent → 每日写 memory/daily/
2. 派蒙Cron(21:00) → 通过 memory_share/ 读取所有Agent日志
3. Nick → 协助整理到 Wiki
4. 派蒙 → 每日复盘 + 月度报告
5. 所有活跃Agent → 参与复盘（Tony/Nick/Zhongli/阿加莘/老六等）
```

---

## ✅ 确认记录

| 日期 | 确认人 | 内容 |
|:-----|:-------|:-----|
| 2026-05-27 | 文博 | 确认方案B映射表和执行计划 |
| 2026-05-27 | 文博 | NICK-OUTPUT改为AI-OUTPUT，Nick只做输入，输出找其他工具替换 |
| 2026-05-27 | 文博 | 同意分层方案：日志归KB，复盘归派蒙统筹；每日复盘，全员参与 |
| 2026-05-27 | 文博 | 确认各Agent写"做的不好"时必须用 `**原因**` 标注原因 |