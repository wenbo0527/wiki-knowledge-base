---
title: insight 20260508 llm agent arch
author: 尼克·弗瑞 🕵️
product_domain: PD-INSIGHT
doc_type: 其他
tags: [insights, agent]
date: 2026-05-23
---

# LLM Agent架构演进：从模型依赖到外部认知基础设施
能力框架: capability-requirement-decision capability-tech-understanding #capability-product-design #capability-risk-control

> **来源**: Get笔记个人笔记 | **发布时间**: 2026-05-08 | **分类**: Agent / Architecture
> **Insight ID**: insight-20260508-llm-agent-arch
> **维护者**: 尼克·弗瑞 | **更新**: 2026-05-11

---

## 📌 一句话判断

> Agent正在从"依赖模型能力"转向"构建外部认知基础设施"，核心是从"让模型记忆一切"到"让模型调用外部记忆和工具"。

---

## 架构演进趋势

### 阶段一：模型中心

- Agent能力完全依赖模型本身
- 上下文窗口是主要限制
- 记忆能力有限

### 阶段二：外部认知基础设施

- 模型调用外部记忆系统
- 模型调用工具和API
- 技能系统外挂
- 记忆容量无限

---

## 核心转变

| 维度 | 旧模式 | 新模式 |
|:---|:---|:---|
| 记忆 | 模型内部上下文 | 外部向量库+MEMORY.md |
| 技能 | 模型内置能力 | Skill系统外挂 |
| 工具 | 模型自带 | 外部工具API |
| 规划 | 模型自主 | 外部规划器辅助 |

---

## 治理框架

### 外部认知基础设施的治理挑战

1. **记忆一致性** - 多Agent共享记忆的同步问题
2. **技能版本管理** - Skill的更新和回滚
3. **工具权限控制** - 安全边界
4. **执行审计** - 可追溯性

---

## 🔗 关联专题

- [[Agent Architecture]] - Agent架构
- [[External Memory]] - 外部记忆
- [[Governance]] - Agent治理

---

## 🏷️ 标签

`#LLMAgent` `#Agent架构` `#外部认知` `#记忆基础设施` `#工具调用` `#治理`

---

*本文档由尼克·弗瑞基于Get笔记整理*
*情报是决策的基础。我不收集信息，我生产洞察。*
