# Agent 任务系统接入指南

> 版本: v1.0
> 创建: 2026-05-18
> 维护者: Tony Stark

---

## 概述

基于 SQLite 的轻量任务管理系统，支持多 Agent 自助创建和更新任务。

---

## 数据库

| 项目 | 值 |
|:---|:---|
| **路径** | `/System/Volumes/Data/Users/wenbo/Documents/05_AgentOutput/agent_work/agent_tasks.db` |
| **类型** | SQLite |
| **Agent** | Tony (主维护) |

---

## Agent 列表

| Agent | 角色 | 可用操作 |
|:---|:---|:---|
| **Paimon** | 总协调 | 全部 |
| **Tony** | 产品管理 | 创建、查询、更新自己的任务 |
| **Nick** | 情报分析 | 创建、查询、更新自己的任务 |
| **Zhongli** | 技术架构 | 创建、查询、更新自己的任务 |

---

## CLI 使用

### 创建任务

```bash
python3 task_tool.py create \
  --title "任务标题" \
  --type SOP \          # SOP/PRD/研究/代码/支持/其他
  --assignee Tony \      # Paimon/Tony/Nick/Zhongli
  --created-by Paimon \
  --priority P1 \        # P0/P1/P2/P3
  --deadline 2026-05-20 \
  --depends-on TASK-xxx \
  --description "任务描述"
```

### 查询任务

```bash
# 查看自己任务
python3 task_tool.py list --assignee Tony

# 查看所有任务
python3 task_tool.py list

# 按状态筛选
python3 task_tool.py list --status pending

# 按类型筛选
python3 task_tool.py list --type SOP
```

### 更新任务

```bash
# 更新状态
python3 task_tool.py update \
  --id TASK-20260518-xxx \
  --updater Tony \
  --status done

# 更新其他字段
python3 task_tool.py update \
  --id TASK-20260518-xxx \
  --updater Tony \
  --priority P0 \
  --assignee Nick
```

### 查看详情

```bash
python3 task_tool.py get --id TASK-20260518-xxx
```

### 统计

```bash
python3 task_tool.py stats
```

### 删除任务

```bash
python3 task_tool.py delete --id TASK-20260518-xxx
```

---

## 状态流转

```
pending → in_progress → done → closed
    ↓
 blocked (遇到阻塞)
```

| 状态 | 说明 |
|:---|:---|
| 🔴 pending | 待处理 |
| 🟠 in_progress | 进行中 |
| ⚫ blocked | 阻塞 |
| 🟡 done | 已完成 |
| 🟢 closed | 已关闭 |

---

## 优先级

| 优先级 | 说明 |
|:---|:---|
| P0 | 紧急，立即处理 |
| P1 | 重要，24h 内完成 |
| P2 | 普通，72h 内完成 |
| P3 | 常规，有空处理 |

---

## 任务类型

| 类型 | 说明 |
|:---|:---|
| SOP | 标准操作流程 |
| PRD | 产品需求文档 |
| 研究 | 行业/技术研究 |
| 代码 | 代码/评审 |
| 支持 | 支持类任务 |
| 其他 | 其他 |

---

## Python SDK

```python
import sys
sys.path.insert(0, '/System/Volumes/Data/Users/wenbo/Documents/05_AgentOutput/agent_work/Tony')

from task_tool import create_task, get_task, update_status, list_tasks

# 创建任务
task = create_task(
    title="编写 PRD",
    type="PRD",
    assignee="Tony",
    created_by="Paimon",
    priority="P1"
)

# 查询任务
my_tasks = list_tasks(assignee="Tony", status="pending")

# 更新状态
task = update_status("TASK-20260518-xxx", "done", updater="Tony")
```

---

## Wiki 关联

任务系统与 Wiki 的 standard-task 模板配合使用：

- Wiki 的 standard-task 模板用于**任务规划**
- SQLite 用于**执行状态追踪**

详见: [[projects/tasks/standard-task]]

---

*最后更新: 2026-05-18*
