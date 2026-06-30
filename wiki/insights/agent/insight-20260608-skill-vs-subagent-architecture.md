# Agent 架构讨论：Skill vs Sub-Agent 与知识底座选型

> **类型**: Insight（架构决策）  
> **来源**: Get笔记 2026-06-05 入库  
> **作者**: 尼克·弗瑞 🕵️  
> **日期**: 2026-06-08  
> **Tags**: #skill #sub-agent #architecture #knowledge-base

---

## 一句话洞察

> **Agent 架构的核心决策不是"用不用多 Agent"，而是"什么场景用 Skill（轻量），什么场景用 Sub-Agent（独立）"**——这是我们 4 Agent 团队（Nick/钟离/托尼/派蒙）+ 团队 2（5 Agent）必须明确划清的边界。

## Skill vs Sub-Agent 决策框架

| 维度 | Skill（轻量）| Sub-Agent（独立）|
|:---|:---|:---|
| **复杂度** | 单步/少步 | 多步/长链 |
| **状态** | 无状态/弱状态 | 强状态/独立记忆 |
| **复用度** | 高（≥10 次）| 中（≥3 个任务）|
| **工具数** | ≤ 5 个工具 | > 5 个工具 |
| **决策权** | 编排 Agent | 自主决策 |
| **成本** | 低 | 中-高 |

## 决策树

```
任务来了
  │
  ├─ 任务能用 ≤5 步描述清楚？
  │   ├─ 是 → Skill
  │   └─ 否 → 继续问
  │
  ├─ 需要独立记忆/状态？
  │   ├─ 否 → Skill
  │   └─ 是 → Sub-Agent
  │
  └─ 工具调用 > 5 个？
      ├─ 否 → Skill
      └─ 是 → Sub-Agent
```

## 我们团队的应用场景

| 场景 | 应该用 | 现状 |
|:---|:---|:---|
| 抓取 RSS 简报 | Skill | ✅ Skill |
| 写完整 Wiki 文档 | Sub-Agent | ✅ Sub-Agent（钟离） |
| 单条 Insight 落盘 | Skill | ✅ Skill |
| 5 Agent 协作跑评测 | Sub-Agent × 5 | ✅ 团队 2 |
| 派单协调 | Sub-Agent（派蒙）| ✅ |

## 知识底座选型（同步讨论）

| 方案 | 适合 | 我们的选择 |
|:---|:---|:---:|
| **向量检索**（RAG）| 海量文档 + 模糊查 | ✅ 已用 Chroma+bge-m3 |
| **知识图谱**（KG）| 实体关系 + 复杂推理 | 🟡 Neo4j 备而未用 |
| **混合** | 大规模生产 | 🟢 未来方向 |

## 落地动作

- [ ] 给团队 2 写 `Skill vs Sub-Agent` 决策树（图示）
- [ ] 调研 4 Agent 各自任务分布，统计 Skill/Sub-Agent 比例
- [ ] 写 `wiki/concepts/agent/skill-vs-subagent-decision.md`
- [ ] 7/1 前做一次"该不该拆 Sub-Agent"复盘

## 引用

- **Get 笔记 ID**: 第 59 条（Agent 架构讨论日志）
- **可复用位置**: Agent 架构 / 决策树 / 团队 1+2 应用

## 关联文档

- [[insight-20260608-harness-engineering-third-paradigm|Harness Engineering 范式]]
- [[../ai/insight-20260608-claude-code-context-three-paradigms|Claude Code 上下文三范式]]

---

*维护: 尼克·弗瑞 🕵️ | 2026-06-08*
