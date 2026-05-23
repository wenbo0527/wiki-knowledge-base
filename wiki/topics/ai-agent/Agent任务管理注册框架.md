# Agent 任务管理注册框架

> **版本**: v1.0
> **日期**: 2026-05-18
> **作者**: Tony Stark
> **状态**: 待完善
> **维护者**: 全体 Agent

---

## 一、框架目标

### 1.1 解决的问题

| 问题 | 现状 | 目标 |
|:---|:---|:---|
| 任务分散 | 飞书/口头/记忆 | 统一系统管理 |
| 进度不透明 | 不知道谁在做啥 | 一键查询 |
| SOP 不执行 | 靠自觉 | 系统提示 |
| 产出不追踪 | 做完不知道在哪 | 关联文档 |

### 1.2 核心理念

**"任务即项目注册，产出即文档沉淀"**

---

## 二、系统架构

### 2.1 两层架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Wiki (SOP + 模板)                        │
│         定义流程规范 / 提供文档模板 / 沉淀产出文档             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     任务系统 (SQLite)                        │
│              任务创建 / 状态更新 / 进度追踪                 │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 系统职责

| 系统 | 职责 | 回答问题 |
|:---|:---|:---|
| **Wiki** | SOP + 模板 + 产出 | 怎么做、产出在哪 |
| **任务系统** | 任务注册 + 跟踪 | 谁做、什么时候做完 |

---

## 三、任务注册规范

### 3.1 注册原则

| 原则 | 说明 |
|:---|:---|
| **必注册** | 所有 Agent 承诺执行的任务 |
| **有产出** | 任务完成后有明确产出 |
| **可追踪** | 有明确的阶段和状态 |

### 3.2 注册时机

| Agent | 注册时机 |
|:---|:---|
| **派蒙** | 接收文博需求时 |
| **Tony** | SOP 步骤完成需创建下一步任务时 |
| **Nick** | 自主发起研究任务时 |
| **钟离** | 接收评审任务时 |

### 3.3 任务生命周期

```
创建 → 进行中 → 已完成 → 已关闭
  ↓
  阻塞 → 升级
```

---

## 四、Agent 任务模板

### 4.1 派蒙 (协调)

```bash
# 任务接收
python3 task_tool.py create \
  --title "任务: {需求名称}" \
  --type 任务 \
  --assignee {Agent} \
  --created-by Paimon \
  --priority P1 \
  --sop-step Paimon-S1 \
  --project {项目名称} \
  --description "{需求描述}"
```

### 4.2 Tony (产品)

```bash
# PRD 编写
python3 task_tool.py create \
  --title "PRD编写: {Epic/Feature}" \
  --type PRD \
  --assignee Tony \
  --created-by Paimon \
  --priority P1 \
  --sop-step SOP-S5 \
  --project {Epic名称} \
  --depends-on {需求分析任务ID} \
  --output-path "{PRD文档路径}"
```

### 4.3 Nick (情报)

```bash
# 研究任务
python3 task_tool.py create \
  --title "研究: {研究主题}" \
  --type 研究 \
  --assignee Nick \
  --created-by Nick \
  --priority P2 \
  --sop-step Nick-S1 \
  --project {研究项目} \
  --description "{研究目标}"
```

### 4.4 钟离 (技术)

```bash
# 技术评审
python3 task_tool.py create \
  --title "评审: {方案名称}" \
  --type 技术 \
  --assignee Zhongli \
  --created-by Tony \
  --priority P1 \
  --sop-step Zhongli-S1 \
  --project {Epic名称} \
  --depends-on {PRD任务ID}
```

---

## 五、SOP 与任务联动

### 5.1 联动规则

| SOP 完成后 | 系统动作 |
|:---|:---|
| SOP-S3 完成 | 创建"PRD编写"任务 |
| SOP-S5 完成 | 创建"开发排期"任务 |
| Nick-S1 完成 | 创建"情报分析"任务 |
| Zhongli-S1 完成 | 创建"代码审查"任务 |

### 5.2 SOP 提示

任务系统在各 Agent 创建任务时，提示应遵循的 SOP：

```
创建任务时提示:
请遵循 {SOP-S5} 流程
产出路径: ________________
```

---

## 六、产出管理

### 6.1 产出定义

每个任务完成后应有明确产出：

| 任务类型 | 产出 |
|:---|:---|
| 需求分析 | 业务需求文档 |
| PRD编写 | PRD文档 |
| 技术评审 | 评审意见 |
| 情报收集 | 情报文档 |
| 代码审查 | 审查报告 |

### 6.2 产出位置规范

```
产出门槛:
  /System/Volumes/Data/Users/wenbo/Documents/
      │
      ├── 文档仓库/                    # Tony/Nick 产出
      │   ├── 产品管理项目/
      │   └── 行业研究/
      │
      └── project/                    # Wiki 协作
          └── Wiki/wiki/
```

---

## 七、查询规范

### 7.1 每日必查

```bash
# 派蒙: 查看所有待办
python3 task_tool.py list --status pending

# Tony: 查看自己的任务
python3 task_tool.py list --assignee Tony --status pending

# Nick: 查看自己的任务
python3 task_tool.py list --assignee Nick --status pending

# 钟离: 查看自己的任务
python3 task_tool.py list --assignee Zhongli --status pending
```

### 7.2 周报统计

```bash
# 统计各 Agent 完成任务
python3 task_tool.py stats
```

---

## 八、异常处理

### 8.1 任务阻塞

| 阻塞原因 | 处理方式 |
|:---|:---|
| 依赖前置任务 | 标记 blocked，等前置完成 |
| 资源不足 | 升级派蒙协调 |
| 技术难题 | 升级钟离支持 |

### 8.2 任务取消

| 情况 | 处理 |
|:---|:---|
| 需求撤销 | 删除任务，关联产出保留 |
| 延期太久 | 关闭任务，后续重新创建 |
| 重复任务 | 合并任务 |

---

## 九、后续优化

| 优化项 | 优先级 | 说明 |
|:---|:---:|:---|
| 周期性任务 recurrence | P2 | 支持日/周/月任务 |
| 任务到期提醒 | P2 | 自动提醒 |
| 产出自动归档 | P3 | 任务完成后归档文档 |
| 产出路径必填 | P1 | 任务创建时必须填写产出路径 |

---

## 十、相关文档

| 文档 | 路径 |
|:---|:---|
| 任务系统用户手册 | [[multi-agent/Agent任务系统用户手册]] |
| SOP-产品管理 | [[产品管理类/SOP-S3-需求分析]] |
| SOP-协调管理 | [[协调管理类/Paimon-S1-任务接收]] |
| SOP-情报研究 | [[情报研究类/Nick-S1-情报收集]] |
| SOP-技术评审 | [[技术评审类/Zhongli-S1-技术方案评审]] |

---

*最后更新: 2026-05-18*
*维护者: 全体 Agent*
