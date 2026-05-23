# agent-task-board

> Skill 档案

## 基本信息

| 字段 | 内容 |
|:-----|:-----|
| **版本** | - |
| **分类** | 🌍 通用 |
| **负责人** | Tony |
| **来源** | 自建 |
| **用途** | 基于 SQLite 的任务系统，支持创建、查询、更新任务 |
| **状态** | ✅ 就绪 |

## 评分信息

| 维度 | 分值 |
|:-----|:----:|
| **实用性** | -/25 |
| **稳定性** | -/25 |
| **易用性** | -/25 |
| **安全性** | -/25 |
| **总分** | -/100 |
| **等级** | - |

## 使用场景

- 查看任务列表
- 创建新任务
- 更新任务状态

## 使用指南

```bash
python3 ~/.openclaw/skills/agent-task-board/agent_task_board.py list --status pending
python3 ~/.openclaw/skills/agent-task-board/agent_task_board.py create --title "xxx" --type SOP --assignee Tony
```

## 关联 Skill

- agent-daily-report

## 更新记录

| 日期 | 版本 | 变更 | 执行人 |
|:-----|:-----|:-----|:-------|
| 2026-05-22 | v1.0 | 初始版本 | 派蒙 |