---
title: topic 02 agent architecture
author: 尼克·弗瑞 🕵️
product_domain: PD-TOPIC
doc_type: 其他
tags: [topics, ai-agent]
date: 2026-05-23
---

# Agent 核心架构与产品设计

> Topic: Agent架构设计 | 模块三
> 标签：Agent / Plan-Act-Reflect / 记忆体系 / Skill工程
> 状态：已完善

---

## 一、Agent 基础范式

### 1.1 Plan-Act-Reflect 标准三环节

```
┌─────────────────────────────────────────────────────────────────────┐
│                      Agent 核心循环                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│         ┌─────────┐                                                 │
│         │  Plan   │  规划：任务分解、工具选择、步骤规划              │
│         └────┬────┘                                                 │
│              ▼                                                       │
│         ┌─────────┐                                                 │
│         │  Act    │  执行：调用工具、获取结果、状态更新              │
│         └────┬────┘                                                 │
│              ▼                                                       │
│         ┌─────────┐                                                 │
│         │ Reflect │  反思：结果校验、资产沉淀、迭代优化              │
│         └────┬────┘                                                 │
│              │                                                       │
│              ▼                                                       │
│         ┌─────────┐                                                 │
│         │  Loop   │  循环：直到任务完成或达到最大轮次                 │
│         └─────────┘                                                 │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

| 环节 | 核心职责 | 输出 |
|:---|:---|:---|
| **Plan** | 任务分解、工具选择、步骤规划 | 执行计划 |
| **Act** | 调用工具、获取结果、状态更新 | 执行结果 |
| **Reflect** | 结果校验、错误识别、资产沉淀 | 反思报告 + 优化 |

### 1.2 三环节详细设计

#### Plan（规划）

```python
# Plan 环节伪代码
async def plan(task, context):
    # 1. 理解任务目标
    goal = understand_task(task)
    
    # 2. 分解任务为子任务
    subtasks = decompose(goal)
    
    # 3. 选择工具
    tools = select_tools(subtasks)
    
    # 4. 规划执行顺序
    execution_order = plan_order(tools)
    
    return ExecutionPlan(
        goal=goal,
        subtasks=subtasks,
        tools=tools,
        order=execution_order
    )
```

#### Act（执行）

```python
# Act 环节伪代码
async def act(plan, tools):
    results = []
    for step in plan.order:
        # 1. 调用工具
        tool = tools[step.tool_name]
        result = await tool.execute(step.params)
        
        # 2. 检查结果
        if not validate(result):
            # 异常处理
            result = await handle_error(result, step)
        
        # 3. 更新状态
        state.update(step, result)
        results.append(result)
    
    return results
```

#### Reflect（反思）

```python
# Reflect 环节伪代码
async def reflect(goal, results, context):
    # 1. 结果自省
    introspection = compare_goal_with_results(goal, results)
    
    # 2. 过程复盘
    process_review = review_process(context.execution_history)
    
    # 3. 资产沉淀
    await沉淀_to_memory(introspection, process_review)
    await沉淀_to_knowledge_base(introspection)
    await沉淀_to_skill_rules(process_review)
    
    return ReflectReport(
        introspection=introspection,
        process_review=process_review
    )
```

---

## 二、反思环节三大核心能力

### 2.1 结果自省

| 检查项 | 说明 | 发现问题 |
|:---|:---|:---|
| **口径验证** | 输出的数据是否符合业务口径 | 数据错误、指标混淆 |
| **逻辑验证** | 推理过程是否正确 | 逻辑漏洞、推理错误 |
| **工具选错** | 是否选择了正确的工具 | 工具误用、路径错误 |
| **步骤冗余** | 是否有不必要的步骤 | 效率低下、重复劳动 |

### 2.2 过程复盘

| 复盘维度 | 说明 |
|:---|:---|
| **规划路径** | Plan 阶段的决策是否合理 |
| **工具选择** | 工具选型是否正确 |
| **上下文使用** | 上下文加载是否合理 |
| **Token 消耗** | Token 使用是否合理 |

### 2.3 资产沉淀

| 沉淀类型 | 说明 | 落地方式 |
|:---|:---|:---|
| **修正记忆** | 修正会话/任务记忆中的错误 | 写入 MEMORY.md |
| **规则迭代** | 迭代 Skill 规则、Prompt 样例 | 更新 SKILL.md |
| **知识补充** | 补充知识库缺失条目 | 写入知识库 |
| **失败归档** | 归档失败 Case 到评测库 | 版本回归测试 |

---

## 三、Agent 设计黄金原则

### 3.1 三大原则

| 原则 | 说明 | 反例 |
|:---|:---|:---|
| **准确优先 > 应答速度** | 金融场景准确比快速回答更重要 | 快速回答但数据错误 |
| **模糊不猜 > 臆测回答** | 信息不全时主动反问，不臆测 | 假设用户意图，答非所问 |
| **主动反问 > 沉默处理** | 边界模糊时主动澄清 | 不知道就沉默 |

### 3.2 文博的实践

> "准确比回答重要，分不清楚的情况不要猜要去问"

```
┌─────────────────────────────────────────────────────────────┐
│                   反问收敛规则                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  触发条件：                                                  │
│  ├── 关键字段缺失（产品、日期、口径）                      │
│  ├── 歧义表达（同一个词有多个含义）                        │
│  └── 上下文不足无法决策                                    │
│                                                              │
│  收敛机制：                                                  │
│  ├── 最多追问 3 次                                        │
│  ├── 3 次后引导用户明确或定义指标                          │
│  └── 记录「无法回答」原因到评测库                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 四、记忆体系

### 4.1 四层记忆隔离

| 层级 | 名称 | 说明 | 生命周期 | 存储位置 |
|:---|:---|:---|:---|:---|
| **L1** | 全局公共记忆 | 共享知识、通用规则 | 永久 | MEMORY.md |
| **L2** | 任务记忆 | 当前任务上下文 | 任务周期 | Task Context |
| **L3** | 会话记忆 | 当前会话历史 | 会话周期 | Session JSONL |
| **L4** | 知识库 | 持久化知识 | 持久 | Vector DB |

### 4.2 记忆生命周期

```
┌─────────────────────────────────────────────────────────────────────┐
│                      记忆生命周期                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   短期记忆                    长期记忆                    归档       │
│  ┌──────────┐              ┌──────────┐              ┌──────────┐ │
│  │ 会话历史  │ ───────▶    │ MEMORY.md │ ───────▶    │ 归档库   │ │
│  │ 工具结果  │   定期提升   │ 核心知识  │   定期沉淀   │ 历史沉淀 │ │
│  │ 临时信息  │              │ 规则沉淀  │              │          │ │
│  └──────────┘              └──────────┘              └──────────┘ │
│                                                                      │
│   触发条件：                    触发条件：                  触发条件：│
│   • 每轮对话                   • 每日复盘                   • >90天 │
│   • 工具调用                   • 任务完成                   • 失效知识 │
│   • 重要决策                   • 显著洞察                   • 低频内容 │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 4.3 记忆压缩与成本控制

| 机制 | 说明 | 触发条件 |
|:---|:---|:---|
| **摘要压缩** | 将长记忆压缩为摘要 | Token 超 60% 窗口 |
| **过期清理** | 删除失效、过时信息 | TTL 过期 |
| **低频淘汰** | 淘汰长期未访问内容 | 访问频率 < 阈值 |
| **重要性锚定** | 核心记忆强化，边缘记忆弱化 | 人工标注/使用频率 |

---

## 五、Skill 工程体系

### 5.1 Skill vs Prompt 本质区别

| 维度 | Prompt | Skill |
|:---|:---|:---|
| **定义方式** | 一次性提示词 | SKILL.md + 配置文件 |
| **复用性** | 低，每次新建 | 高，可版本化管理 |
| **生命周期** | 无管理 | 全生命周期管理 |
| **触发方式** | 手动调用 | 条件触发/自动路由 |
| **能力范围** | 单次输出 | 多步骤、工具编排 |

### 5.2 Skill 全生命周期

```
┌─────────────────────────────────────────────────────────────────────┐
│                      Skill 全生命周期                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────┐    ┌──────┐    ┌──────┐    ┌──────┐    ┌──────┐   │
│  │ 创建  │───▶│ 准入  │───▶│ 规范  │───▶│ 评分  │───▶│ 监控  │   │
│  └──────┘    └──────┘    └──────┘    └──────┘    └──────┘   │
│                                                           │         │
│                                                   ┌──────┴──────┐ │
│                                                   ▼              ▼ │
│                                              ┌──────┐    ┌──────┐ │
│                                              │ 合并  │───▶│ 下线  │ │
│                                              └──────┘    └──────┘ │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

| 阶段 | 说明 | 产出 |
|:---|:---|:---|
| **创建** | 定义 Skill 能力、触发条件、工具列表 | SKILL.md |
| **准入** | 评审、规范检查、能力验证 | 准入报告 |
| **规范** | 命名规范、参数规范、输出规范 | 规范文档 |
| **评分** | 使用率、成功率、用户满意度评估 | 评分报告 |
| **监控** | 调用链路、质量追踪、异常告警 | 监控面板 |
| **合并** | 相似 Skill 合并、功能整合 | 合并报告 |
| **下线** | 优雅下线、兼容处理、文档归档 | 下线报告 |

### 5.3 Skill 原子化与场景模板

```
┌─────────────────────────────────────────────────────────────────────┐
│                   Skill 层级设计                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  L1: 原子 Skill（不可再分）                                        │
│  ├── Read(file)           → 读取文件                              │
│  ├── Bash(cmd)            → 执行命令                               │
│  ├── Edit(file, ...)      → 编辑文件                              │
│  └── Search(pattern)      → 搜索内容                              │
│                                                                      │
│  L2: 组合 Skill（多个原子 Skill 组合）                            │
│  ├── code_review           → Read + Search + Bash(test)           │
│  ├── requirement_parse     → Read + Edit + Search                  │
│  └── document_generate     → Read + Search + Edit                  │
│                                                                      │
│  L3: 场景模板（面向特定场景的 Skill 组合）                        │
│  ├── 问数 Skill           → requirement_parse + sql_execute        │
│  ├── 文档解析 Skill       → file_read + knowledge_base_write      │
│  └── 代码生成 Skill        → requirement_parse + code_write        │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 六、工具与编排

### 6.1 Tools 原子能力标准

| 标准 | 说明 | 示例 |
|:---|:---|:---|
| **单一职责** | 每个 Tool 只做一件事 | Read(file) 只读文件 |
| **入参明确** | 入参类型、范围、约束清晰 | `file: string, line_start?: number` |
| **出参可预期** | 出参格式固定，错误码明确 | `{ content: string, error?: string }` |
| **幂等性** | 多次调用结果一致 | Read 幂等，Write 不幂等 |
| **可观测** | 日志、耗时、错误码完整 | 调用链路可追踪 |

### 6.2 多步骤任务编排

```python
# 多步骤编排示例
class TaskOrchestrator:
    def __init__(self):
        self.tools = {}
        self.error_handlers = {}
    
    async def execute(self, task):
        plan = await self.plan(task)
        
        for step in plan.steps:
            try:
                result = await self.execute_step(step)
                
                # 分支判断
                if self.should_branch(result):
                    branch_plan = await self.plan_branch(result)
                    await self.execute(branch_plan)
                
                # 失败重试
                if not result.success and step.max_retries > 0:
                    await self.retry(step)
                
            except Exception as e:
                # 异常兜底
                result = await self.error_handlers[step.type](e)
        
        return result
    
    async def retry(self, step, strategy="exponential_backoff"):
        """指数退避重试"""
        for attempt in range(step.max_retries):
            delay = min(2 ** attempt * 0.1, 5)  # 0.1s, 0.2s, 0.4s...
            await asyncio.sleep(delay)
            result = await self.execute_step(step)
            if result.success:
                return result
        return Failure("Max retries exceeded")
```

### 6.3 编排模式

| 模式 | 说明 | 适用场景 |
|:---|:---|:---|
| **顺序编排** | 步骤按顺序执行 | 线性任务 |
| **并行编排** | 步骤并行执行 | 独立子任务 |
| **分支编排** | 根据条件选择分支 | 判断决策类 |
| **循环编排** | 重复执行直到满足条件 | 迭代优化类 |
| **回环编排** | 执行结果反馈到起始 | 收敛类任务 |

---

## 七、相关文档

- [RAG 全链路架构](./topic-03-rag-architecture.md)
- [多 Agent 协作](./topic-04-multi-agent.md)
- [企业 Agent 平台](./topic-06-enterprise-agent.md)

---

标签：Agent / Plan-Act-Reflect / 记忆体系 / Skill工程
归档：topics/ai-agent/
