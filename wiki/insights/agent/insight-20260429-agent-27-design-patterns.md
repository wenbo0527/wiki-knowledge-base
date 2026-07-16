---
title: insight 20260429 agent 27 design patterns
author: 尼克·弗瑞 🕵️
product_domain: PD-INSIGHT
doc_type: 其他
tags: [insights, agent]
date: 2026-05-23
---

# Insight: Agent系统27种设计模式与Harness工程化
能力框架: capability-value-closed-loop capability-tech-understanding #capability-product-design #capability-risk-control #capability-data-driven

> **来源**: Get笔记订阅课程录音
> **原始标题**: Agent系统的27种设计模式与Harness工程化分享
> **授课时间**: 2026-04-17 16:39
> **时长**: 24分46秒
> **方向**: AI Agent / Agent Engineering
> **评级**: ⭐⭐⭐⭐ (4/5)
> **获取时间**: 2026-04-29

---

## 核心洞察

### 1. 设计模式在Agent系统中的核心价值

**设计模式的作用边界**：设计模式无法直接生成大型复杂系统，但可以在编码过程中逐步指导思维，帮助拆解大型系统，识别可复用的设计节点。

**核心定位**：Harness（围绕大模型Agent的外围工程框架）比基础模型更工程师可控，是普通工程师可以主导设计的部分。

> 🚩 **重点**：我们无法管控大模型本身的精度，但可以通过设计Harness系统约束Agent的运行环境，获得更稳定的运行结果。

### 2. Harness系统的核心设计模式分类

#### Agent循环核心模式

| 模式 | 说明 |
|------|------|
| ReAct (Reasoning + Acting) | 交替进行推理和执行 |
| Plan-then-Execute | 先规划后执行 |
| Hierarchical Agents | 层级Agent，分工协作 |
| Self-Critique | Agent自我批判改进 |

#### 工具使用模式

| 模式 | 说明 |
|------|------|
| Tool Use | 调用外部工具 |
| Retrieval Augmented | RAG增强 |
| Memory-Augmented | 记忆增强 |
| Multi-Modal | 多模态处理 |

#### 多Agent协作模式

| 模式 | 说明 |
|------|------|
| Coordinator-Follower | 协调者-执行者 |
| Debate/Tournament | Agent辩论赛 |
| Hierarchical | 层级协作 |
| Broadcasting | 广播式 |

### 3. 27种设计模式全景图

```
Agent系统设计模式
├── Agent循环设计 (7种)
│   ├── ReAct
│   ├── Plan-Then-Execute  
│   ├── Loop-Exit
│   ├── Hierarchical
│   ├── Self-Critique
│   ├── Error-Recovery
│   └── Reflection
├── 工具与知识 (8种)
│   ├── Tool-Use
│   ├── Tool-Creation
│   ├── RAG
│   ├── Memory
│   ├── Knowledge-Graph
│   ├── Multi-Modal
│   ├── Code-Generation
│   └── Search
├── 多Agent协作 (7种)
│   ├── Coordinator
│   ├── Debate
│   ├── Voting
│   ├── Round-Robin
│   ├── Master-Slave
│   ├── Federated
│   └── Hierarchical
├── Harness工程 (5种)
│   ├── Guardrails
│   ├── Caching
│   ├── Fallback
│   ├── Timeout
│   └── Circuit-Breaker
└── 观测与安全 (5种)
    ├── Logging
    ├── Tracing
    ├── Rate-Limiting
    ├── Sandbox
    └── Permission
```

### 4. 对Agent工程化的核心启示

#### 为什么Harness比模型更可控？

| 维度 | 模型 | Harness |
|------|------|---------|
| 确定性 | ❌ 低 | ✅ 高 |
| 可调试性 | ❌ 难 | ✅ 易 |
| 可测试性 | ❌ 黑盒 | ✅ 白盒 |
| 升级影响 | ❌ 扩散 | ✅ 局部 |
| 工程师控制 | ❌ 弱 | ✅ 强 |

#### 设计模式的价值

1. **降低复杂度**：将大型系统拆解为可理解的设计节点
2. **加速开发**：复用经过验证的方案而非从头设计
3. **便于测试**：每个模式可独立测试
4. **知识传承**：将经验编码为可描述的模式

---

## 关联知识

- [[ai-native/agent-engineering]] - Agent工程化专题
- [[insights/insight-20260421-anthropic-harness-guide]] - Anthropic Harness指南
- [[insights/insight-20260417-harness-engineering]] - Harness Engineering核心概念
- [[insights/insight-20260421-openai-skill-evaluation]] - OpenAI Skill评测

---

## 要点总结

1. **Harness > 模型**：在当前阶段，Harness工程比模型选择更能控制系统行为
2. **27种模式**：覆盖Agent循环、工具使用、多Agent协作、Harness工程、观测安全5大类
3. **设计模式是Harness的具体实现**：通过设计模式将Harness理念落地
4. **工程师可控**：设计模式是普通工程师可以主导的领域，而非等待模型进步

---

*尼克·弗瑞 🕵️ | Get笔记订阅引入 | 2026-04-29*
