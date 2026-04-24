# LLM Agent

> 基于大语言模型的自主代理系统

---

## 元信息

- **创建时间**: 2026-04-08
- **更新时间**: 2026-04-08
- **类型**: concept
- **标签**: #AI #LLM #agent #autonomous

## 定义

LLM Agent是将大语言模型作为核心控制器的自主代理系统。LLM作为"大脑"，配合其他关键组件实现自主决策和执行。

## 核心架构

```
┌─────────────────────────────────────┐
│         LLM Agent System            │
│                                     │
│  ┌───────────────────────────────┐ │
│  │     LLM (Core Controller)    │ │
│  └───────────────────────────────┘ │
│              ↓ ↑                    │
│  ┌───────────────────────────────┐ │
│  │         Components            │ │
│  │  • Planning (规划)           │ │
│  │  • Memory (记忆)             │ │
│  │  • Tools (工具)              │ │
│  └───────────────────────────────┘ │
└─────────────────────────────────────┘
```

## 三大组件

### 1. Planning (规划)

| 能力 | 说明 | 示例 |
|------|------|------|
| **子目标分解** | 将大任务分解为可管理的子目标 | CoT, ToT |
| **反思与精炼** | 自我批评，从错误中学习 | Reflexion |
| **自我修正** | 纠正错误行为 | ReAct |

### 2. Memory (记忆)

| 类型 | 说明 | 实现 |
|------|------|------|
| **短期记忆** | 上下文学习 | In-context Learning |
| **长期记忆** | 持久存储 | Vector Store / KG |
| **情景记忆** | 经验回顾 | Retrieval |

### 3. Tools (工具)

| 工具 | 说明 |
|------|------|
| **搜索** | Web Search, API |
| **代码执行** | Python, Shell |
| **文件操作** | Read, Write, Edit |
| **数据库** | SQL, Vector DB |
| **API调用** | REST, GraphQL |

## 代表项目

| 项目 | 说明 | 特点 |
|------|------|------|
| **AutoGPT** | 自主GPT Agent | 工具调用先驱 |
| **GPT-Engineer** | 代码生成Agent | 自动化编程 |
| **BabyAGI** | 任务管理Agent | 简单高效 |
| **Claude Agent** | Anthropic出品 | 安全可靠 |
| **OpenAI Agents SDK** | OpenAI官方 | 标准规范 |

## Agent能力分级

| 级别 | 能力 | 代表 |
|------|------|------|
| **L1** | 基础对话 | ChatGPT |
| **L2** | 工具调用 | GPT-4 + Functions |
| **L3** | 多步推理 | o1, Claude |
| **L4** | 自主规划 | Claude Agent |
| **L5** | 自我改进 | 未来方向 |

## 工作流程

```
用户输入
    ↓
LLM规划 (Planning)
    ↓
执行Action
    ↓
获取Observation
    ↓
反思 (Reflection)
    ↓
┌─ 完成？→ 是 → 输出结果
└─ 完成？→ 否 → 继续循环
```

## 与Karpathy LLM Wiki的关系

> Karpathy提出的LLM Wiki模式是Agent应用的延伸：

| 维度 | LLM Agent | LLM Wiki |
|------|-----------|----------|
| **目标** | 自主执行任务 | 知识积累管理 |
| **核心** | 规划+执行 | 编译+维护 |
| **输出** | 任务结果 | Wiki页面 |

## 相关页面

- [[llm-wiki-pattern]] - LLM Wiki模式
- [[rag]] - RAG技术
- [[karpathy]] - Andrej Karpathy
- [[ai-llm]] - AI/LLM概念

## 来源引用

- [LLM Powered Autonomous Agents - Lilian Weng](https://lilianweng.github.io/posts/2023-06-23-agent/)
- 2023-06-23

---

*最后更新: 2026-04-08*
*维护者: 尼克·弗瑞*