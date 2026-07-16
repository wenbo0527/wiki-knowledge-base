---
title: insight 20260521 harness engineering overview
author: 尼克·弗瑞 🕵️
product_domain: PD-INSIGHT
doc_type: 其他
tags: [insights, agent, harness-engineering]
date: 2026-05-23
---

# Harness Engineering综述：从模型到制度化管理

> **版本**: v1.0
> **日期**: 2026-05-21
> **作者**: 尼克·弗瑞
> **分类**: AI Agent / Harness / Engineering
> **Tags**: #harness #engineering #workflow #management
> **方法论**: 框架驱动

---

## 一、核心框架

### 1.1 核心公式

```
Agent = Model（模型）+ Harness（运行环境）
```

| 组件 | 职责 |
|:---|:---|
| **Model** | 提供智能 |
| **Harness** | 让智能变得有用 |

**关键洞察**：改变Harness比换模型更有效。

### 1.2 四块拼图模型

| 拼图 | 说明 | 作用 |
|:---|:---|:---|
| **约束与流程** | 边界和规则 | 让AI在规矩里干活 |
| **反馈** | 判卷和验证 | 干完以后谁来判卷 |
| **知识库** | 索引和记忆 | 同一功能不被反复重写 |
| **进化** | 持续改进 | 人与AI共同驱动Harness改版 |

---

## 二、制度化管理理念

### 核心原则

| 原则 | 说明 |
|:---|:---|
| **AI不是助手** | 是执行力极强但必须被制度化管理的团队 |
| **制度化管理** | 不能指望它天生懂规矩，自己长出流程意识 |
| **要给边界** | 给AI边界、分工、门禁、反馈闭环 |
| **人设计系统** | 人负责设计系统，AI负责执行 |
| **人负责结果** | 人对最终结果负责 |

### 最小可用形态

| 步骤 | 动作 |
|:---:|:---|
| **1** | 先看当前最大的痛点在哪里 |
| **2** | 先补最关键的一层 |
| **3** | 让系统先跑起来 |
| **4** | 在真实问题里继续补强 |

---

## 三、设计原则

### 3.1 三条核心原则

| 原则 | 说明 |
|:---|:---|
| **用Claude已经会的** | 底层工具越通用，Claude发挥空间越大 |
| **什么时候该停手** | 问自己"我还能停掉什么？" |
| **边界要谨慎** | 该设的边界要设，但要精准 |

### 3.2 Dead Weight陷阱

```
问题出现 → 搭建Harness解决 → 模型变强 → Harness变成dead weight
     ↑                                                    ↓
     └────────────── 应该拆掉，而不是永久保留 ──────────────┘
```

**核心原则**: Build to delete. 造了就要敢拆。

### 3.3 建设顺序

| 顺序 | 组件 | 职责 |
|:---:|:---|:---:|
| **1** | **Harness** | 系统"脊梁"，故障可观测/可阻断/可回滚 |
| **2** | **Skill** | 降低执行方差，提升可预测性 |
| **3** | **Memory** | 避免过早记忆噪声 |
| **4** | **Multi-agent Protocol** | 协作规范 |

---

## 四、相关文档

| 文档 | 说明 |
|:---|:---|
| [insight-20260421-anthropic-harness-guide.md](insight-20260421-anthropic-harness-guide.md) | Anthropic官方指南 |
| [insight-20260423-harness-engineering-complete-guide.md](insight-20260423-harness-engineering-complete-guide.md) | 完整指南 |
| [insight-20260430-agent-harness-context-management.md](insight-20260430-agent-harness-context-management.md) | 上下文管理 |
| [insight-20260521-harness-engineering-practice.md](insight-20260521-harness-engineering-practice.md) | 实战指南 |
| [insight-20260521-agent-harness-context-management.md](../agent/insight-20260521-agent-harness-context-management.md) | 会话压缩与工作集 |

---

*维护者: 尼克·弗瑞*
*日期: 2026-05-21*
*版本: v1.0*