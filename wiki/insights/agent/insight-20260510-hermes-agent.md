---
title: insight 20260510 hermes agent
author: 尼克·弗瑞 🕵️
product_domain: PD-INSIGHT
doc_type: 其他
tags: [insights, agent]
date: 2026-05-23
---

# Hermes Agent：自进化革命
能力框架: capability-requirement-decision capability-data-driven

> **来源**: Get笔记个人笔记 | **发布时间**: 2026-05-10 | **分类**: Agent / Self-Evolution
> **Insight ID**: insight-20260510-hermes-agent
> **维护者**: 尼克·弗瑞 | **更新**: 2026-05-11

---

## 📌 一句话判断

> Hermes Agent两个月内GitHub获103K+ stars，通过GEPA自进化引擎实现"让AI记住学到的内容并持续改进"，从"一次性工具"到"自进化智能体"的突破。GEPA已被ICLR 2026接收为Oral论文。

---

## 项目概况

| 维度 | 数据 |
|:---|:---|
| 开发方 | Nous Research |
| 开源时间 | 2026年2月25日 |
| GitHub | 103K+ stars |
| 增速 | 超过LangChain和AutoGen历史同期增长总和 |
| v0.8.0发布 | 当日新增6400星 |
| 协议 | MIT开源协议 |
| 部署门槛 | 最低$5/月VPS |

---

## GEPA自进化引擎

### 核心技术

**GEPA（Genetic-Pareto Prompt Evolution）算法**，已被ICLR 2026接收为Oral论文

### 工作流程

1. 读取Agent当前的技能描述、工具说明、系统提示
2. 根据真实执行记录自动生成评估数据集
3. 分析失败原因（不仅判断成败，还识别具体失败因素）
4. 提出改良版本
5. 候选版本通过测试套件
6. 最佳版本以PR形式提交审核

### 性能指标

| 维度 | GEPA表现 | 对比基准 |
|:---|:---|:---|
| 任务性能提升 | 平均高出6%（最大差距20个百分点） | GRPO |
| 训练数据效率 | 仅需1/35 | GRPO |
| 数学测试 | 高出12% | MIPROv2在AIME-2025 |
| 优化成本 | $2-10/次 | 无需GPU集群 |

---

## 三层记忆体系

### 模仿人类记忆结构

| 记忆类型 | 技术实现 | 核心能力 |
|:---|:---|:---|
| 会话记忆 | SQLite+FTS5 | 语义搜索历史对话 |
| 持久长期记忆 | MEMORY.md | 2200字符限制，存储项目环境、踩坑记录 |
| 程序性技能记忆 | SKILL.md | Agent自建的操作手册 |

---

## Curator策展人机制

解决技能只进不出的问题，AI Agent领域首个技能生命周期管理系统。

### 工作流程

1. **确定性状态机**（不消耗模型推理资源）：
   - 30天未调用 → 标记stale
   - 90天未调用 → 移入归档

2. **模型审查**（每7天一次）：
   - 合并重叠技能
   - 更新过时内容

---

## 对OpenClaw的启示

社区动向：开发者从OpenClaw大规模迁移至Hermes Agent

核心差异：OpenClaw专注编程任务，Hermes专注"让AI学会持续改进"

---

## 🔗 关联专题

- [[Agent Engineering]] - Agent工程
- [[Self-Evolution]] - 自进化
- [[Skills System]] - Skill系统

---

## 🏷️ 标签

`#HermesAgent` `#NousResearch` `#GEPA` `#自进化` `#ICLR2026` `#Agent` `#技能管理`

---

*本文档由尼克·弗瑞基于Get笔记整理*
*情报是决策的基础。我不收集信息，我生产洞察。*
