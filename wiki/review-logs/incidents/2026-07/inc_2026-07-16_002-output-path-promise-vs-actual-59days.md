# INC-2026-07-16-002: 6 任务 close output_path 信约 ≠ 实际 · 候选 #117+#129+#172 第 17 次复发

## 现象

**触发时间**: 2026-07-16 08:10 CST（候选 #235 派单回执 v1.1 阶段 · 6 TASK ID 实证时发现）

**实证链**：

| 任务 TASK ID | 状态 (sqlite) | output_path | 实际文件落档 |
|:--|:--|:--|:--:|
| TASK-20260518-3E5CEBF6 | **closed** @ 2026-07-15 15:29:41 | memory/lessons/les_2026-07-15_001-deadlock-close-59days.md | ❌ |
| TASK-20260518-7BF5931F | **closed** @ 2026-07-15 15:29:41 | memory/lessons/les_2026-07-15_002-deadlock-close-59days.md | ❌ |
| TASK-20260518-698D059B | **closed** @ 2026-07-15 15:29:41 | memory/lessons/les_2026-07-15_003-deadlock-close-59days.md | ❌ |
| TASK-20260518-8E29C662 | **closed** @ 2026-07-15 15:29:41 | memory/lessons/les_2026-07-15_004-deadlock-close-59days.md | ❌ |
| TASK-20260518-67DF1855 | **closed** @ 2026-07-15 15:29:41 | memory/lessons/les_2026-07-15_005-deadlock-close-59days.md | ❌ |
| TASK-20260518-306F1CB3 | **closed** @ 2026-07-15 15:29:41 | memory/lessons/les_2026-07-15_006-deadlock-close-59days.md | ❌ |

**实证来源**：

```bash
sqlite3 /Users/wenbo/Documents/05_AgentOutput/agent_work/agent_tasks.db \
  "SELECT id, status, output_path FROM tasks WHERE id LIKE 'TASK-20260518-%'"

# 输出: 6 任务 closed @ 2026-07-15 15:29:41 + 6 个 output_path 全部填写
# 但 find /Users/wenbo/Documents/05_AgentOutput -name "les_2026-07-15_001-deadlock*" → 0 命中
# find /Users/wenbo/.openclaw -name "les_2026-07-15_00*deadlock*" → 0 命中
```

**Nick workspace lessons 目录**：

```
/Users/wenbo/Documents/05_AgentOutput/agent_work/Nick/lessons/
  └── 2026-07-06_lessons_L24-L26.md  ← 唯一文件，无 deadlock-close
```

## 根因

**候选 #117+#129+#172 失守链第 17 次复发**：

7-15 15:29:41 钟离触发候选 #235 清理时，task_tool 批量关闭 6 任务：
- ✅ status='closed' 写入 sqlite db
- ✅ output_path 字段填写 `memory/lessons/les_2026-07-15_00*-deadlock-close-59days.md`
- ❌ **实际 lessons 文件没有真的落档**（"信约 ≠ 实际"）

钟离候选 #235 v1.0 文档（15:06 CST）写的"立即清理（24h 内）"包括：
> 1. **拍 close 6 个 Nick 任务**（59 天 · 候选 #129 防御）

但**"拍 close"在 task_tool 层面只更新 db status，没真正写文件**——除非 close 命令带 `--write-lesson` 之类的参数（task_tool.py v2.0-rc.1 没有这种参数）。

**候选类别**：
- 候选 #117（write byte 不可信）的延伸 = close 字段写 ≠ lessons 文件真的写
- 候选 #129（信约 ≠ 实际）的延伸 = db 信约 ≠ 文件实际
- 候选 #172（派单边界）的延伸 = 钟离级联派 close 但 lessons 落地 owner 未明确

## 修复（按 L-15 + L-30 + L-31 + 候选 #117+#129+#172）

### 短期（今 4h 自治窗口内 · 8:10 → 14:01）

1. ✅ INC-2026-07-16-002 落档（本文件）
2. ✅ lesson-2026-07-16-deadlock-lessons-rescue 落档到 `review-logs/lessons/by-agent/nick_fury/`
3. ⏳ **写 6 个 deadlock-close-59days lessons 实际文件**——按 task_tool output_path 路径补写
4. ⏳ sessions_send 派蒙回执 v1.2：6/6 实际 closed（候选 #235 第①项天然闭环）+ INC-002 新立 + lessons 补写 plan

### 6 lessons 补写 plan（候选 #129 治本）

| # | 文件路径 | 标题 | 候选任务 5W1H |
|:--|:---|:---|:---|
| 1 | `memory/lessons/les_2026-07-15_001-deadlock-close-59days.md` | 简历v1.3 Review确认 闭环 | TASK-20260518-3E5CEBF6 · 59 天 pending · 7-15 closed · 简历仍用 v1.3 |
| 2 | `les_2026-07-15_002-deadlock-close-59days.md` | 行业研究-5个项目文档接入知识库 闭环 | TASK-20260518-7BF5931F · 59 天 · 7-15 closed · 7-15 阶段1 A.1 已 RAG 化 |
| 3 | `les_2026-07-15_003-deadlock-close-59days.md` | GET笔记内容提炼进Wiki 闭环 | TASK-20260518-698D059B · 59 天 · 7-15 closed · 7-15 getnote E5C18BA3 修复 + 100 篇限流确认 |
| 4 | `les_2026-07-15_004-deadlock-close-59days.md` | 面试提升题库构建 闭环 | TASK-20260518-8E29C662 · 59 天 · 7-15 closed · 文博未启动 = 拍 close 共识 |
| 5 | `les_2026-07-15_005-deadlock-close-59days.md` | Wiki知识库索引接入 闭环 | TASK-20260518-67DF1855 · 59 天 · 7-15 closed · W1 速赢 Phase 1.1-1.6 已完成 |
| 6 | `les_2026-07-15_006-deadlock-close-59days.md` | REQ-20260518-001: Nick 行业研究 闭环 | TASK-20260518-306F1CB3 · 59 天 · 7-15 closed · 7-15 阶段1 A.1 行业研究 v1.3 已出 |

**路径补写规则（L-31 + L-16）**：
- 路径以 Nick 工作区 `memory/lessons/` 为准（相对路径锚点）
- 实际落到 `/Users/wenbo/Documents/05_AgentOutput/agent_work/Nick/memory/lessons/les_2026-07-15_00*-deadlock-close-59days.md`
- 写后必 `ls -la` 实证（候选 #117 byte 漏算防御）

### 中长期（候选 #235 v1.1 升级候选）

- task_tool v2.0-rc.2 升级：close 命令加 `--write-lesson <template>` 必填参数
- 候选 #235 派单模板 v1.1：close 输出 = db status + 实际文件落档 + lessons 链接
- 候选 #129 防御 v3.2：≥30 天 pending 自动 close 时必须 trigger lessons 落档

## 教训（L-40 候选 · 待 7-19 周日复盘正式编号）

**L-40（候选 · 待编号）**:

**db 信约 ≠ 文件实际 = 候选 #117+#129+#172 第 17 次**：
- task_tool close = db status 更新 ≠ lessons 文件落档
- output_path 字段填了 ≠ 文件真的写出来了
- 防御：任何 close 命令后必 `ls -la <expected_path>` 实证
- 治理：task_tool v2.0-rc.2 必加 `--write-lesson` 强制参数

## 关联

- INC-2026-07-16-001（派单要素不齐 · 候选 #129 同根病）
- INC-2026-07-04-002（候选 #117 write byte 不可信 · ls/wc 实证）
- 候选 #172 v3.0 · 钟离级联派 close · lessons 落地 owner 未明确
- 候选 #235 v1.1 文档（钟离 7-15 15:06 CST + 7-16 07:55 CST 修订）
- HEARTBEAT.md §十三（候选 #235 派单回执 v1.0）

## 状态

🟠 进行中 · 等待 6 lessons 实际文件落档 + 10:30 早检派蒙回执 + 14:01 截止诚实归零

---

*记录时间: 2026-07-16 08:10 CST · 4h 自治窗口内*
*维护者: 尼克·弗瑞 🕵️*
*数据源: sqlite3 task_tool db + find 全集实证 + task_tool.py get 命令*
*候选 #117+#129+#172 失守链第 17 次复发*