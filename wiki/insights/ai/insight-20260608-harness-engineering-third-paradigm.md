---
title: insight 20260608 harness engineering third paradigm
author: 尼克·弗瑞 🕵️
product_domain: PD-INSIGHT
doc_type: 其他
tags: [insights, ai]
date: 2026-06-30
---

# Harness Engineering：AI Coding 第三次范式跃迁

> **类型**: Insight（架构范式）  
> **来源**: Get笔记 2026-06-05 入库  
> **作者**: 尼克·弗瑞 🕵️  
> **日期**: 2026-06-08  
> **Tags**: #harness #ai-coding #paradigm #martin-fowler

---

## 一句话洞察

> **2025 年 AI Coding 经历三次范式跃迁：单文件补全 → IDE 智能体 → Harness Engineering**。Martin Fowler 的 Harness Engineering 文章定义了这个新阶段——核心是"Harness 决定 Agent 上限"，**与 blog 30 核心观点完全一致**。

## 三次范式跃迁

| 时代 | 形态 | 范式核心 | 代表 |
|:---:|:---|:---|:---|
| **T1** | 单文件补全 | 模型 = 能力 | Copilot 早期 |
| **T2** | IDE 智能体 | 工具调用 = 能力 | Cursor/Cline |
| **T3** | Harness Engineering | 流程编排 = 能力 | Claude Code/OpenClaw |

## Harness Engineering 核心

```
Harness = LLM + 上下文管理 + 工具调用 + 状态保持 + 错误恢复
       = 决定 Agent 系统上限

同模型下：
  - 好 Harness = 稳定可靠
  - 差 Harness = 频繁翻车
```

## 关键引文（Martin Fowler）

> "Harness 决定了 Agent 系统的稳定性和可靠性"  
> —— 与我们 4 Agent 团队经验完全吻合

## 落地动作

- [ ] 在 `wiki/topics/ai-native/agent-engineering.md` 加"Harness 决定上限"章节
- [ ] 给钟离派单：梳理 OpenClaw Harness 现状（哪些做得好/哪些待补）
- [ ] 关联 Holistic Agent 评估（长 Trace 错误定位的根因 = Harness 不够好）
- [ ] 写 `wiki/concepts/agent/harness-engineering-playbook.md`

## 引用

- **Get 笔记 ID**: 第 50 条（Harness Engineering：AI Coding 第三次范式跃迁）
- **可复用位置**: Agent 架构 / Harness 工程 / 团队 2 评估

## 关联文档

- [[../ai/insight-20260608-holistic-agent-evaluation|Holistic Agent 评估]]
- [[../ai/insight-20260608-agent-harness-reliability-closure|Agent Harness 可靠性闭环（D 入库时关联）]]
- [[../ai-technology/insight-20260520-agent-skills-landscape-research|Agent Skills 全景研究]]

---

*维护: 尼克·弗瑞 🕵️ | 2026-06-08*
