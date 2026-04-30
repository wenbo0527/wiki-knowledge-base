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

- Insight: 多智能体架构设计指南 - Sub-Agent vs Agent Team (20260430) 🆕
- Insight: Claude Code Subagents深度解析 - 上下文卫生管理 (20260430) 🆕
- Insight: 基于图的智能体记忆技术 - Graph Memory全解析 (20260430) 🆕
- Insight: Agent Harness上下文管理 - Working Set范式 (20260430) 🆕
- Insight: 为Agent设计产品 - 从界面工具到运行底座 (20260430) 🆕
- Insight: MuleRun陈宇森：Vibe Coding与Agent创作新范式 (20260429)
- Insight: Andre Karpathy亲述AI代理革命的范式转变 (20260429)
- Insight: 大模型AI Skill编写、评测迭代与长链路任务实践 (20260429)
- Insight: Agent系统27种设计模式与Harness工程化 (20260429)
- 💡 Insight: BMAD方法论 - AI驱动的敏捷开发框架 (2026-04-28)
- Insight: 18岁AI先锋金豪：主动式AI、记忆系统与模型人格 (20260429)
- 💡 Insight: DeerFlow 2.0 - ByteDance开源Super Agent Harness (2026-04-28)
- 洞察：Playwright CLI + Skills UI自动化测试 — 无障碍树方案 (20260429)
- 洞察：Playwright CLI × Claude Code 企业级自动化测试实践 (20260429)
- Insight: Boris Churnney：Claude Code技术与代码审查新范式 (20260429)
- Everything Claude Code (ECC) 项目研究报告 (20260429)
- 洞察：多Agent Text2SQL 架构 — 企业级 ChatBI 的实现路径 (20260429)
- 研究报告：提升代码Agent现有项目理解能力 (20260429)
- Insight: Claude Code创建者亲述"后编程时代"工作方式 (20260429)

<!-- 自动关联的insights将在这里列出 -->
---

*本框架由 B2 每日主题扩展脚本自动生成*
