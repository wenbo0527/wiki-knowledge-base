---
title: insight 20260428 simon willison code is cheap
author: 尼克·弗瑞 🕵️
product_domain: PD-INSIGHT
doc_type: 其他
tags: [insights, technology]
date: 2026-05-23
---

# Insight: Simon Willison - Writing Code is Cheap 代码变得廉价
能力框架: capability-value-closed-loop capability-requirement-decision

> **来源**: Simon Willison's Weblog（Agentic Engineering Patterns指南）  
> **作者**: Simon Willison（Django联合作者）  
> **发布日期**: 2026-02-23  
> **评级**: ⭐⭐⭐⭐ (4/5)  
> **标签**: #AgenticEngineering #代码成本 #工程习惯 #技术债 #效率革命

---

## 执行摘要

Simon Willison的核心洞察：**代码变得廉价了**。这是采用Agentic Engineering实践的最大挑战——我们需要彻底改变工程习惯，从"代码很贵"到"代码廉价"的认知转变。

---

## 核心观点

> "The biggest challenge in adopting agentic engineering practices is getting comfortable with the consequences of the fact that **writing code is cheap now**."

**采用Agentic Engineering的最大挑战**：接受"写代码现在很廉价"这一事实带来的后果。

---

## 代码成本的历史对比

| 维度 | 传统模式 | AI时代 |
|------|----------|--------|
| **代码生产成本** | 昂贵（几百行代码需要一整天） | 几乎免费 |
| **并行能力** | 单线执行 | 多Agent同时工作 |
| **决策考量** | 权衡投入产出 | "先prompt再说" |

### 宏观层面的变化

以前：
- 花大量时间设计、估算、规划项目
- 产品功能根据"投入时间能产出多少价值"来评估
- 功能必须N倍回报开发成本才值得做

### 微观层面的变化

以前每天数百个决策都基于：
- "重构这个函数值得花一个小时吗？"
- "要写文档吗？"
- "这个边界情况值得加测试吗？"
- "值得为这个建一个调试界面吗？"

---

## 好代码仍然有成本

### 关键区分

> "Delivering new code has dropped in price to almost free... but delivering **good code** remains significantly more expensive than that."

**新代码交付成本几乎为零——但交付好代码的成本仍然要高得多。**

### 好代码的定义

| 标准 | 说明 |
|------|------|
| **代码能工作** | 做它该做的事，没有bug |
| **我们知道代码能工作** | 采取了步骤向自己和他人证明代码是适合用途的 |
| **解决正确的问题** | 不仅仅是正确地解决问题 |
| **错误处理** | 优雅且可预测地处理错误情况 |
| **简洁** | 只做需要的事，且以人和机器都能理解和维护的方式 |
| **测试保护** | 测试证明它现在能工作，且作为回归测试套件避免未来悄悄破坏 |
| **文档** | 适当的文档水平，且反映系统当前状态 |
| **设计** | 为未来变化提供便利（YAGNI vs 过度设计） |
| **其他"ilities"** | 可访问性、可测试性、可靠性、安全性、可维护性、可观察性、可扩展性、可用性 |

---

## 新习惯养成

### 核心建议

> "any time our instinct says 'don't build that, it's not worth the time' fire off a prompt anyway, in an asynchronous agent session where the worst that can happen is you check ten minutes later and find that it wasn't worth the tokens."

**新习惯**：任何时候当你本能说"不值得花时间做那个"时，还是发一个prompt——在异步agent session中，最坏情况是你十分钟后检查发现不值得花token。

### 并行Agent的影响

> "The ability to run parallel agents makes this even harder to evaluate, since one human engineer can now be implementing, refactoring, testing and documenting code in multiple places at the same time."

**并行Agent能力**让评估变得更难——一个工程师现在可以同时实现、重构、测试和文档化多处代码。

---

## 关键洞察

### 范式转变

| 从 | 到 |
|----|----|
| 代码很贵 | 代码廉价 |
| 谨慎规划 | 先做再说 |
| 避免技术债 | 随时清理技术债 |
| 单线执行 | 多Agent并行 |

### 实践意义

1. **小改动也值得做**——AI让"清理小代码异味"的成本几乎为零
2. **多尝试**——可以并行测试多个方案
3. **快速原型**——快速验证想法

---

## 相关文档

- [[insight-20260428-simon-willison-better-code|AI should help us produce better code]] (同来源)
- [[insight-20260428-simon-willison-hoard-things|Hoard things you know how to do]] (同来源)
- [[topic-ai-native/ai-programming/vibe-coding|Vibe Coding专题]]

---

## 参考来源

- [Simon Willison Code is Cheap原文](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/)

---

**记录时间**: 2026-04-28 08:30  
**记录者**: 尼克·弗瑞 (Nick Fury)  
**状态**: ✅ 已引入Wiki

