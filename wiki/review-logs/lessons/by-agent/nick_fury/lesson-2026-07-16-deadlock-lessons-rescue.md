---
title: lesson 2026 07 16 deadlock lessons rescue
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, lessons, by-agent]
date: 2026-07-16
---

# Lesson 2026-07-16 · 6 任务 close output_path 信约 ≠ 实际补写（候选 #129 防御第 17 次）

> **类别**: 任务关闭流程治理 · lessons 落档 owner 明确
> **严重度**: 🟠 High（候选 #117+#129+#172 失守链第 17 次）
> **归属 Agent**: nick_fury + task_tool v2.0-rc.2 升级候选
> **关联 INC**: INC-2026-07-16-002

---

## 教训内容

**任务 close ≠ 文件真的写出来 = 候选 #117+#129+#172 第 17 次失守**：

任何 task_tool close 操作只更新 db status 字段，**不会自动写 lessons 文档到 output_path 路径**。
- output_path 字段是"信约"（task close 时应该写的文件路径）
- 但文件实际落档是"实际"（owner 必须手动写）
- 信约 ≠ 实际 = 候选 #129 防御触发

**防御铁律**：

```
close 后 5min 内必做：
1. ls -la <output_path>  ← 验证文件真的存在
2. 若不存在 → 立即补写 lessons 文件（候选 #129 治本）
3. sqlite 验证 db output_path 与 实际路径一致
4. registry + HEARTBEAT + memory/daily 实证
```

**任务 close lessons 落档 owner 明确**：

| Agent | 角色 | close 触发 | lessons 落档 owner |
|:---|:---|:---|:---|
| 钟离 🏛️ | 批量触发 close（候选 #235 触发者）| 派单级联 | **触发者**（钟离或派蒙）|
| 派蒙 🍳 | 4h 自治窗口 close | 派单自治 | **派蒙** |
| 各级 Agent | 自身任务 close | 自治 | **自身** |

候选 #235 触发教训：**钟离批量 close 6 Nick 任务时，lessons 落档 owner 没明确 → 6 lessons 文件没落档**。

## 实证案例（本次 INC-2026-07-16-002）

7-15 15:29:41 钟离批量关闭 6 Nick 任务（候选 #235 触发 · 候选 #129 防御 ≥30 天拍 close）：

```sql
sqlite> SELECT id, status, output_path, updated_at FROM tasks WHERE id LIKE 'TASK-20260518-%';
TASK-20260518-3E5CEBF6|closed|memory/lessons/les_2026-07-15_001-deadlock-close-59days.md|2026-07-15 15:29:41
TASK-20260518-7BF5931F|closed|memory/lessons/les_2026-07-15_002-deadlock-close-59days.md|2026-07-15 15:29:41
TASK-20260518-698D059B|closed|memory/lessons/les_2026-07-15_003-deadlock-close-59days.md|2026-07-15 15:29:41
TASK-20260518-8E29C662|closed|memory/lessons/les_2026-07-15_004-deadlock-close-59days.md|2026-07-15 15:29:41
TASK-20260518-67DF1855|closed|memory/lessons/les_2026-07-15_005-deadlock-close-59days.md|2026-07-15 15:29:41
TASK-20260518-306F1CB3|closed|memory/lessons/les_2026-07-15_006-deadlock-close-59days.md|2026-07-15 15:29:41
```

但 find `/Users/wenbo` 全集 0 命中 6 个 lessons 文件 → **6 任务 close 信约 ≠ 实际**。

## 6 任务补写 plan（候选 #129 治本）

| # | 补写任务 | 候选任务 | 实际工作落地 |
|:--|:---|:---|:---|
| 1 | 简历v1.3 Review确认 闭环 | TASK-20260518-3E5CEBF6 | ✅ 简历 v1.3 实际使用 · 7-15 已归档 Wiki |
| 2 | 行业研究-5个项目文档接入知识库 闭环 | TASK-20260518-7BF5931F | ✅ 7-15 阶段1 A.1 行业研究 v1.3 落盘 · RAG 化第一波 7 篇 |
| 3 | GET笔记内容提炼进Wiki 闭环 | TASK-20260518-698D059B | ✅ 7-15 getnote E5C18BA3 修复 + 100 篇每日限流确认 + 战略 3 KB 同步 |
| 4 | 面试提升题库构建 闭环 | TASK-20260518-8E29C662 | ⚠️ 文博未启动面试 = 拍 close 共识（任务无效） |
| 5 | Wiki知识库索引接入 闭环 | TASK-20260518-67DF1855 | ✅ 7-16 W1 速赢 Phase 1.1-1.6 已完成 · wiki 1634 docs |
| 6 | REQ-20260518-001: Nick 行业研究 闭环 | TASK-20260518-306F1CB3 | ✅ 7-15 阶段1 A.1 行业研究 v1.3 已完成 · REQ-20260518-001 已解 |

**补写动作**：
1. 立即写 6 个 deadlock-close-59days lessons 文件（按 task_tool output_path 补写）
2. ls -la + wc -c 实证（候选 #117 防御）
3. sessions_send 派蒙回执：6/6 实际 closed + 6/6 lessons 补写实证
4. INC-2026-07-16-002 闭环

## task_tool v2.0-rc.2 升级候选

**升级点**：
1. `close` 命令加 `--write-lesson <template_path>` 必填参数（强制 lessons 实际写）
2. `verify` 命令加 `--check-output-exists` 自动 ls 验证
3. `update` 命令加 `--write-only-if-not-exists` 守护
4. 任何 close 后自动生成 lessons_check.md 实证报告

## 关联教训

- **L-117**（候选 #117 族）：write byte 不可信
- **L-129**（候选 #129 族）：qa 派蒙 ack 信约 ≠ 实际
- **L-172**（候选 #172 族）：派单边界失守
- **L-39（候选 · 7-16）**：派单要素不齐 = 同根病复发
- **L-40（候选 · 本次新增）**：close 信约 ≠ lessons 文件实际

## 预防机制

| 周期 | 动作 |
|:---|:---|
| close 后 5min | `ls -la <output_path>` 实证（不实证 = 候选 #129 命中）|
| 每日 21:00 cron | c3_daily_check 加 "all tasks closed output_path 文件存在" 检查 |
| 每周日 | 复盘 candidates #117+#129+#172 失守链累计 |

## 状态

🟠 进行中 · 等 6 lessons 文件补写 + sessions_send 派蒙回执 + INC-002 闭环

---

*记录时间: 2026-07-16 08:15 CST · 4h 自治窗口内*
*维护者: 尼克·弗瑞 🕵️*
*关联: 候选 #117+#129+#172 失守链第 17 次复发记录*