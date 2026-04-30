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

- Insight: Agent Harness上下文管理 - 从聊天记录到工作集的范式转变 (20260430)
- Insight: Karpathy Autoresearch - 自主AI研究框架 (20260430)
- Insight: Claude Code Subagents深度解析 - 上下文卫生管理 (20260430)
- Insight: 基于图的智能体记忆技术 - 架构、应用与实践框架 (20260430)
- Insight: 为Agent设计产品 - 从"界面工具"到"运行底座"的范式转变 (20260430)
- Insight: 多智能体架构设计指南 - 从上下文边界到协作模式 (20260430)

<!-- 自动关联的insights将在这里列出 -->
---

*本框架由 B2 每日主题扩展脚本自动生成*
