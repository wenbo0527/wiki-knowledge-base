# AI Agent

> 自动生成框架 | 生成时间: 2026-04-29

## 主题概述

ai-agent 相关内容的综合主题。

## 核心概念

| 概念 | 说明 |
|------|------|
| **Sub-Agent** | 隔离式并行架构，适用于独立任务 |
| **Agent Team** | 共享式协作架构，适用于强依赖任务 |
| **Context Boundary** | 决定架构选择的核心维度 |
| **Graph Memory** | 基于图的智能体记忆技术 |

## 最佳实践

- **架构选型判断框架**：子任务是否需共享上下文 → 决定Sub-Agent或Agent Team
- **上下文卫生管理**：Subagent作为独立工作区，避免80k token噪音积累
- **Graph Memory**：显式关系建模，支持因果推理和多跳查询

## 工具资源

| 工具 | 用途 |
|------|------|
| **Mem0** | 全流程图记忆管理，时序感知 |
| **Graphiti(Zep)** | 时序知识图谱，双时间建模 |
| **Cognee** | 可查询图嵌入，复杂推理 |
| **LangMem** | LangChain生态集成 |

## 相关Insights

- Insight: 吴恩达 - 最快的团队，人人都是产品经理 (20260506)
- Insight: Simon Willison - Linear Walkthroughs 代码理解模式 (20260506)
- Insight: Simon Willison - Hoard Things You Know 如何囤积知识 (20260506)
- Insight: UModel - 用知识图谱构建 Agent 原生的代码理解能力 (20260506)
- AI大神三大根本性分歧：136条访谈精华提炼 (20260506)
- Insight: Simon Willison - Writing Code is Cheap 代码变得廉价 (20260506)
- Insight: Simon Willison - AI Should Help Us Produce Better Code (20260506)
- Insight: 小红书数据架构演进 - Big AI Data时代的新一代增量计算 (20260506)
- Insight: Simon Willison - Anti-patterns 反模式警示 (20260506)
- Insight: Agent+MCP+Skills 重构自动化测试 (20260506)
- Insight: Simon Willison - Subagents 子代理模式 (20260506)

<!-- 自动关联的insights将在这里列出 -->
---

*本框架由 B2 每日主题扩展脚本自动生成*
