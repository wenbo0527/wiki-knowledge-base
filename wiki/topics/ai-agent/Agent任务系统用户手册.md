---
title: Agent任务系统用户手册
author: 尼克·弗瑞 🕵️
product_domain: PD-TOPIC
doc_type: 其他
tags: [topics, ai-agent]
date: 2026-05-23
---

# Agent 任务系统用户手册

> **版本**: v1.1
> **更新**: 2026-05-18
> **维护者**: Tony Stark

---

## 一、系统概述

### 1.1 是什么

基于 SQLite 的轻量任务管理系统，支持多 Agent 自助创建和更新任务。

### 1.2 与其他系统的关系

| 系统 | 管理什么 | 用途 |
|:---|:---|:---|
| **任务系统** | Agent 工作任务 | 谁做、什么时候做 |
| **Neo4j** | Epic/Feature/Story | 产品需求结构 |
| **Wiki/SOP** | 文档规范 | 怎么做 |

**注意**：三个系统独立运作，不需要关联。

---

## 二、Agent SOP 框架

### 2.1 SOP 目录

```
SOP/
├── 产品管理类/
│   ├── SOP-S3-需求分析.md
│   └── SOP-S5-PRD生成与开发指导.md
├── 协调管理类/
│   ├── Paimon-S1-任务接收.md
│   └── Paimon-S2-任务跟踪.md
├── 情报研究类/
│   ├── Nick-S1-情报收集.md
│   └── Nick-S2-情报分析.md
└── 技术评审类/
    ├── Zhongli-S1-技术方案评审.md
    └── Zhongli-S2-代码审查.md
```

### 2.2 SOP → 任务映射

| SOP | 任务前缀 | 执行者 |
|:---|:---|:---|
| Paimon-S1 | 任务接收 | 派蒙 |
| Nick-S1 | 情报收集 | 尼克 |
| Nick-S2 | 情报分析 | 尼克 |
| Zhongli-S1 | 技术评审 | 钟离 |
| Zhongli-S2 | 代码审查 | 钟离 |

---

## 三、任务类型

| 类型 | 说明 | SOP 适用 |
|:---|:---|:---:|
| SOP | 标准操作流程任务 | ✅ |
| PRD | 产品需求文档 | ✅ |
| 研究 | 行业研究/情报分析 | ✅ |
| 代码 | 开发/评审任务 | ✅ |
| 支持 | 临时支持 | ❌ |
| 其他 | 其他任务 | ❌ |

---

## 四、任务字段

| 字段 | 说明 | 必填 |
|:---|:---|:---:|
| id | 任务ID（自动生成） | 自动 |
| title | 任务标题 | ✅ |
| type | 任务类型 | ✅ |
| assignee | 负责人 | ✅ |
| created_by | 创建者 | ✅ |
| priority | 优先级 (P0/P1/P2/P3) | ❌ |
| deadline | 截止日期 | ❌ |
| depends_on | 依赖任务 | ❌ |
| description | 任务描述 | ❌ |
| sop_step | SOP步骤 | ❌ |
| project | 项目/主题 | ❌ |
| output_path | 产出文档路径 | ❌ |

---

## 五、CLI 使用

### 5.1 创建任务

```bash
python3 task_tool.py create \
  --title "任务标题" \
  --type SOP/PRD/研究/代码/支持/其他 \
  --assignee Tony/Nick/Zhongli/Paimon \
  --created-by Paimon \
  --priority P1 \
  --sop-step SOP-S3 \
  --project 项目名称 \
  --depends-on TASK-xxx
```

### 5.2 查询任务

```bash
# 查看自己任务
python3 task_tool.py list --assignee Tony

# 查看所有任务
python3 task_tool.py list

# 按状态筛选
python3 task_tool.py list --status pending

# 按类型筛选
python3 task_tool.py list --type PRD
```

### 5.3 更新状态

```bash
python3 task_tool.py update \
  --id TASK-20260518-xxx \
  --updater Tony \
  --status done
```

---

## 六、状态流转

```
pending → in_progress → done → closed
    ↓
 blocked
```

| 状态 | 说明 |
|:---|:---|
| 🔴 pending | 待处理 |
| 🟠 in_progress | 进行中 |
| ⚫ blocked | 阻塞 |
| 🟡 done | 已完成 |
| 🟢 closed | 已关闭 |

---

## 七、各 Agent 使用场景

### 7.1 Tony (产品管理)

```bash
# PRD 任务
python3 task_tool.py create \
  --title "PRD编写: 周期回溯" \
  --type PRD \
  --assignee Tony \
  --created-by Paimon \
  --sop-step SOP-S5 \
  --project 周期回溯增强 \
  --depends-on TASK-xxx
```

### 7.2 Nick (情报研究)

```bash
# 研究任务
python3 task_tool.py create \
  --title "行业研究: 2026年营销趋势" \
  --type 研究 \
  --assignee Nick \
  --created-by Paimon \
  --sop-step Nick-S1 \
  --project 营销行业研究
```

### 7.3 Zhongli (技术评审)

```bash
# 技术评审任务
python3 task_tool.py create \
  --title "技术评审: XXX技术方案" \
  --type 代码 \
  --assignee Zhongli \
  --created-by Tony \
  --sop-step Zhongli-S1 \
  --project Epic名称
```

### 7.4 Paimon (任务协调)

```bash
# 查看所有待办
python3 task_tool.py list --status pending

# 查看某人任务
python3 task_tool.py list --assignee Tony

# 查看逾期任务
# (需自行筛选 deadline)
```

---

## 八、SOP 执行后创建任务

| SOP | 完成后的动作 |
|:---|:---|
| SOP-S3 | 创建"PRD编写"任务 |
| SOP-S5 | 创建"开发排期"任务 |
| Nick-S1 | 创建"情报分析"任务 |
| Zhongli-S1 | 创建"代码审查"任务 |

---

## 九、常见问题

### Q: 任务与 Neo4j 需要关联吗？

A: 不需要。Neo4j 管理产品结构（Epic/Feature），任务系统管理 Agent 工作。两者独立运作。

### Q: SOP 字段是必须填的吗？

A: 不是。SOP 是 Tony/Nick/Zhongli 执行时的规范指导，任务系统不需要强制校验。

### Q: 周期性任务怎么管理？

A: 目前任务系统支持 `deadline` 字段。周期性任务的 recurrence 字段待开发。

---

## 十、相关文档

| 文档 | 路径 |
|:---|:---|
| SOP-产品管理 | `.../SOP/产品管理类/` |
| SOP-协调管理 | `.../SOP/协调管理类/` |
| SOP-情报研究 | `.../SOP/情报研究类/` |
| SOP-技术评审 | `.../SOP/技术评审类/` |

---

*最后更新: 2026-05-18*
