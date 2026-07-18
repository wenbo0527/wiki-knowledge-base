---
title: insight 20260428 simon willison anti patterns
author: 尼克·弗瑞 🕵️
product_domain: PD-INSIGHT
doc_type: 其他
tags: [insights, technology]
date: 2026-05-23
---

# Insight: Simon Willison - Anti-patterns 反模式警示
能力框架: capability-tech-understanding

> **来源**: Simon Willison's Weblog（Agentic Engineering Patterns指南）  
> **作者**: Simon Willison（Django联合作者）  
> **发布日期**: 2026-03-04  
> **评级**: ⭐⭐⭐⭐⭐ (5/5)  
> **标签**: #AgenticEngineering #反模式 #代码审查 #团队协作 #最佳实践

---

## 执行摘要

Simon Willison在Agentic Engineering实践中总结的**反模式警示**。核心原则：**不要把自己都没审查过的代码扔给协作者**。这是AI编程时代最常见也最令人沮丧的错误。

---

## 核心反模式：不要提交未审查的代码

### 问题描述

> "If you open a PR with hundreds (or thousands) of lines of code that an agent produced for you, and you haven't done the work to ensure that code is functional yourself, you are delegating the actual work to other people."

**核心问题**：如果你提交了一个包含数百/数千行AI生成代码的PR，但你自己都没有确保代码能正常工作，那你就是在把实际工作推给别人。

---

## 好PR的特征

Simon提出的**优质Agentic Engineering PR标准**：

| 特征 | 说明 |
|------|------|
| **代码能工作** | 你对代码能正常工作有充分信心 |
| **小而精** | 变更足够小，可以高效审查，不给审查者增加过多认知负担 |
| **提供上下文** | 说明变更要服务于什么更高层次的目标，关联相关issue或规格说明 |
| **自己先审查** | PR描述也需要你自己审阅，不要让别人读你自己都没读过的文字 |

### 黄金原则

> "Your job is to deliver code that works."

**你负责交付能工作的代码** —— 这是你的责任，不是审查者的。

---

## 实践建议

### 如何证明你尽了审查责任

Simon建议在PR中包含以下证据，证明你确实做了额外的工作：

- 📝 手动测试的记录
- 💬 特定实现选择的评论说明
- 📸 功能运行截图
- 🎥 功能运行视频

这些都能有效证明"审查者的时间不会被浪费"。

---

## 关键洞察

### AI编程时代的新责任

| 传统模式 | AI时代新要求 |
|----------|--------------|
| 人类写代码 | AI生成代码 |
| 人类审查AI代码 | **人类必须先验证AI代码** |
| 审查者是质量关卡 | **你自己才是第一道质量关卡** |

### 核心转变

> "Given how easy it is to dump unreviewed code on other people..."

AI让代码生成变得**极其容易**，但这也意味着**责任更重**——你必须确保自己提交给别人的代码是经过你验证的。

---

## 相关文档

- [[insights/technology/insight-20260428-simon-willison-linear-walkthroughs|Linear Walkthroughs]] (同来源)
- [[insights/technology/insight-20260428-simon-willison-subagents|Subagents模式]] (同来源)
- [[topic-ai-native/ai-programming/vibe-coding|Vibe Coding专题]]

---

## 参考来源

- [Simon Willison Anti-patterns原文](https://simonwillison.net/guides/agentic-engineering-patterns/anti-patterns/)

---

**记录时间**: 2026-04-28 08:20  
**记录者**: 尼克·弗瑞 (Nick Fury)  
**状态**: ✅ 已引入Wiki

