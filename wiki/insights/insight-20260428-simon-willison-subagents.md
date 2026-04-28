# Insight: Simon Willison - Subagents 子代理模式

> **来源**: Simon Willison's Weblog（Agentic Engineering Patterns指南）  
> **作者**: Simon Willison（Django联合作者）  
> **发布日期**: 2026-03-17  
> **评级**: ⭐⭐⭐⭐⭐ (5/5)  
> **标签**: #AgenticEngineering #Subagents #Multi-Agent #上下文管理 #并行执行

---

## 执行摘要

Simon Willison详解**Subagents（子代理）模式**：解决LLM上下文窗口限制的核心策略。通过子代理分发任务，获得全新的上下文窗口，避免消耗父代理宝贵的token配额。

---

## 背景：上下文窗口限制

LLM受限于**上下文窗口（Context Limit）**——一次能处理的token数量有限。目前主流模型上下文窗口通常在200K-1M tokens之间，但实际使用中超过200K往往效果下降。

**核心问题**：如何在大任务中管理宝贵的上下文空间？

---

## Subagent模式原理

### 核心概念

当Coding Agent使用Subagent时，它实际上是将一个**全新的自己**派遣出去完成特定目标，拥有一个从新prompt开始的全新上下文窗口。

```
┌─────────────────────────────────────────────────────────┐
│                    Subagent 工作流程                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   父代理 (Parent Agent)                                 │
│   ├── 任务: 实现完整功能                                  │
│   └── 遇到子任务 → 派遣Subagent                         │
│            │                                            │
│            ▼                                            │
│   ┌─────────────────────────────────────────────────┐   │
│   │  Subagent (子代理)                              │   │
│   │  - 全新上下文窗口                               │   │
│   │  - 专注于子任务                                 │   │
│   │  - 使用更快/更便宜的模型 (如Claude Haiku)       │   │
│   └─────────────────────────────────────────────────┘   │
│            │                                            │
│            ▼                                            │
│   父代理汇总结果，继续执行                                │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Claude Code的Explore Subagent

### 实际案例

Claude Code使用Subagent的经典案例——**Explore Subagent**：

当你在一个已有仓库启动新任务时，Claude Code首先需要探索仓库结构，找到相关信息。它通过构建prompt并派遣一个Explore Subagent来执行探索。

**典型Prompt示例**：

```
Find the code that implements the diff view for "chapters" 
in this Django blog. I need to find:
- Templates that render diffs (look for diff-related HTML/CSS)
- Python code that generates diffs (look for difflib usage)
- Any JavaScript related to diff rendering
- CSS styles for the diff view

Search thoroughly - check templates/, static/, blog/ directories.
```

**关键洞察**：模型会"自我提示"——它们对自己使用的prompt策略有很好的直觉。

---

## Subagent的三大类型

### 1. 探索型（Explore）Subagent
- 用于理解代码库结构
- 查找相关文件和代码段
- 为父代理提供上下文信息

### 2. 并行型（Parallel）Subagent
- 父代理同时运行多个Subagent
- 可使用更快/更便宜的模型加速任务
- 适用于互不依赖的文件编辑任务

**示例Prompt**：
```
Use subagents to find and update all of the templates 
that are affected by this change.
```

### 3. 专业型（Specialist）Subagent
- 带自定义System Prompt的Subagent
- 可配备专用工具

| 专业角色 | 用途 |
|----------|------|
| **Code Reviewer** | 审查代码，识别bug、设计弱点 |
| **Test Runner** | 运行测试，仅报告失败详情 |
| **Debugger** | 专门调试问题，隔离复现步骤 |

---

## 使用指南

### 何时使用Subagent

| 场景 | 推荐 |
|------|------|
| 需要探索大型代码库 | ✅ Explore Subagent |
| 编辑多个不相关的文件 | ✅ Parallel Subagent |
| 复杂调试任务 | ✅ Specialist Debugger |
| 简单单文件修改 | ❌ 不需要 |

### 注意事项

> "While it can be tempting to go overboard breaking up tasks across dozens of different specialist subagents, it's important to remember that the main value of subagents is in preserving that valuable root context and managing token-heavy operations."

**核心价值**：Subagent的主要价值在于保护宝贵的根上下文和管理token密集操作。不要过度拆分任务。

---

## 工具支持

| 工具 | 文档链接 |
|------|----------|
| OpenAI Codex | subagents |
| Claude | subagents |
| Gemini CLI | subagents |
| Mistral Vibe | subagents |
| OpenCode | agents |
| VS Code | Subagents |
| Cursor | Subagents |

---

## 关键洞察

### Subagent vs 多Agent系统

| 维度 | Subagent | Multi-Agent |
|------|----------|-------------|
| **上下文** | 子窗口，共享父代理知识 | 完全独立，各自有完整上下文 |
| **通信** | 父子直接通信 | Agent间需要协议通信 |
| **复杂度** | 低 | 高 |
| **适用场景** | 任务分解、上下文管理 | 独立专家协作 |

---

## 相关文档

- [[insight-20260428-simon-willison-anti-patterns|Anti-patterns反模式]] (同来源)
- [[insight-20260428-simon-willison-linear-walkthroughs|Linear Walkthroughs]] (同来源)
- [[insight-20260417-claude-code-agent-farm|Claude Code Agent Farm]]

---

## 参考来源

- [Simon Willison Subagents原文](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/)

---

**记录时间**: 2026-04-28 08:25  
**记录者**: 尼克·弗瑞 (Nick Fury)  
**状态**: ✅ 已引入Wiki

