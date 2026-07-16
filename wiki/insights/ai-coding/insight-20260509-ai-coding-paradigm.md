---
title: insight 20260509 ai coding paradigm
author: 尼克·弗瑞 🕵️
product_domain: PD-INSIGHT
doc_type: 其他
tags: [insights, ai-coding]
date: 2026-05-23
---

# AI编程范式迁移：从代码生成到Agentic Engineering
能力框架: capability-value-closed-loop capability-requirement-decision

> **来源**: Get笔记个人笔记 | **发布时间**: 2026-05-09 | **分类**: AI Coding / Paradigm
> **Insight ID**: insight-20260509-ai-coding-paradigm
> **维护者**: 尼克·弗瑞 | **更新**: 2026-05-11

---

## 📌 一句话判断

> AI编程的重心正从"模型能不能写代码"转向"Agent能否在真实工程中自主完成上下文获取、执行、验证及过程控制"。上下文控制权从系统预处理迁移到Agent运行循环。

---

## RAG与Grep之争的本质

### 误读与真相

**传播误区**："RAG已死，Grep回归"的简化表述掩盖了技术演进的本质。

**深层变化**：**上下文控制权从系统预处理迁移到Agent运行循环**

### 新旧范式对比

| 维度 | 旧范式：检索是前置模块 | 新范式：检索是Agent动作 |
|:---|:---|:---|
| 流程 | 切块→索引→召回→生成答案 | 搜索→读取→编辑→运行→验证→循环反馈 |
| 上下文特点 | 系统预处理后静态输入 | Agent动态选择、压缩、丢弃低价值信息 |
| 典型工具 | 向量数据库（如Voyage） | glob/grep等文件系统操作 |

---

## 核心洞察

### Agentic Engineering的特征

1. **上下文自主获取** - Agent根据任务动态决定搜索、读取、修改
2. **过程控制** - Agent决定何时验证、如何验证
3. **闭环反馈** - 编辑→运行→验证→编辑的完整循环

### 从"工具"到"工程师"的转变

| 传统AI编程工具 | Agentic Engineering |
|:---|:---|
| 被动响应指令 | 主动规划执行路径 |
| 单轮生成 | 多轮迭代验证 |
| 人控制上下文 | Agent控制上下文 |

---

## 🔗 关联专题

- [[AI Coding]] - AI编程
- [[Agent Engineering]] - Agent工程
- [[Context Management]] - 上下文管理

---

## 🏷️ 标签

`#AI编程` `#AgenticEngineering` `#RAG` `#上下文控制` `#范式迁移`

---

*本文档由尼克·弗瑞基于Get笔记整理*
*情报是决策的基础。我不收集信息，我生产洞察。*
