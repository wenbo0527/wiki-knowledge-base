---
title: insight 20260509 sdd
author: 尼克·弗瑞 🕵️
product_domain: PD-INSIGHT
doc_type: 其他
tags: [insights, ai-coding]
date: 2026-05-23
---

# Spec-Driven Development (SDD)：AI编程时代的工程方法论革命
能力框架: capability-requirement-decision capability-tech-understanding #capability-data-driven

> **来源**: Get笔记个人笔记 | **发布时间**: 2026-05-09 | **分类**: AI Coding / Engineering
> **Insight ID**: insight-20260509-sdd
> **维护者**: 尼克·弗瑞 | **更新**: 2026-05-11

---

## 📌 一句话判断

> 将规格说明（Spec）作为唯一真实来源（Single Source of Truth），代码作为其派生产物。5人团队7天完成传统20人数周工作量验证SDD可行性。

---

## "5人7天"震撼实验

**核心成果**：5人团队在7天内完成传统20人数周工作量，成功上线产品QoderWork

### 项目时间线

| 阶段 | 内容 |
|:---|:---|
| DAY 0 | 不写代码，完成四件事：定义MVP边界、拆解模块、撰写模块Spec、汇入Repo Wiki |
| DAY 1-2 | 用Qoder完成架构开发，框架与容器同步推进，系统骨架成型 |
| DAY 3-4 | Spec迭代增量需求，AI自动生成代码并提交PR，人负责Review与合并 |
| DAY 5-6 | 自举式测试（用QoderWork测试自身），发现问题后通过Spec修复 |
| DAY 7 | 正式发布上线 |

**核心问题**：5人能驾驭AI并行推进多任务而不失控的关键在于DAY 0制定的Spec，这构成了整个项目的锚点。

---

## SDD核心定义

### 一句话定义

> Spec-Driven Development：将规格说明（Specification）作为唯一真实来源（Single Source of Truth），代码作为其派生产物。

### 核心思想

先定义**WHAT**（做什么），再让AI实现**HOW**（怎么做）。

**与传统开发的关键差异**：在AI编程时代，Spec质量直接决定代码质量，因为AI不会追问边界情况，只会按上下文推断。

### 时代背景

SDD是AI编程发展的结构性需求，2025年多个方向同时收敛至此：
- **反面参照**：Karpathy的Vibe Coding暴露"不管代码只管vibes"的问题
- **工具支持**：GitHub Spec Kit、AWS SDD-native IDE Kiro、阿里QoderWork

> Microsoft评价："SDD is version control for your thinking"

---

## SDD完整流程

### 四阶段模型

```
Specify（规格定义）-> Plan（方案规划）-> Implement（代码实现）-> Validate（验证确认）
```

| 阶段 | 主导者 | 核心产出 | 关键动作 |
|:---|:---|:---|:---|
| Specify | 人 | spec.md | 定义问题、边界、成功标准 |
| Plan | 人+AI | plan.md | 架构选型、模块划分、接口定义 |
| Implement | AI | 代码+测试 | 按plan逐任务实现 |
| Validate | 人+AI | 测试报告 | 自动化测试+人工Review |

**核心原则**：人定义WHAT，AI实现HOW

---

## 与文博工作的关联

文博正在实践的VIBE CODING需要升级为SDD：
- VIBE CODING：快速Demo生成
- SDD：系统化规格驱动，确保可维护性

---

## 🔗 关联专题

- [[VIBE Coding]] - VIBE CODING实践
- [[AI Coding]] - AI编程
- [[Engineering]] - 工程方法论

---

## 🏷️ 标签

`#SDD` `#Spec-Driven-Development` `#规格驱动开发` `#AI编程` `#工程方法论` `#QoderWork`

---

*本文档由尼克·弗瑞基于Get笔记整理*
*情报是决策的基础。我不收集信息，我生产洞察。*
