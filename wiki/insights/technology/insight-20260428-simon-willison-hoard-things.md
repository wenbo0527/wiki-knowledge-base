---
title: insight 20260428 simon willison hoard things
author: 尼克·弗瑞 🕵️
product_domain: PD-INSIGHT
doc_type: 其他
tags: [insights, technology]
date: 2026-05-23
---

# Insight: Simon Willison - Hoard Things You Know 如何囤积知识
能力框架: capability-value-closed-loop capability-product-design

> **来源**: Simon Willison's Weblog（Agentic Engineering Patterns指南）  
> **作者**: Simon Willison（Django联合作者）  
> **发布日期**: 2026-02-23  
> **评级**: ⭐⭐⭐⭐ (4/5)  
> **标签**: #AgenticEngineering #知识管理 #个人知识库 #提示词工程 #代码复用

---

## 执行摘要

Simon Willison的软件专业人员成长法则：**囤积你知道如何做的事**。核心观点：积累"我知道这事怎么做"的答案，配合运行代码的证明，是软件专业人员最重要的资产。这些积累会成为Coding Agent的强力输入。

---

## 核心观点

> "A big part of the skill in building software is understanding what's possible and what isn't, and having at least a rough idea of how those things can be accomplished."

构建软件的重要技能是理解什么可能、什么不可能，并至少大致了解如何完成这些事情。

---

## 知识囤积的价值

### 最佳实践

> "The best way to be confident in answers to these questions is to have seen them illustrated by **running code**."

**对这些问题答案最有信心**的方式是看到它们通过**运行代码**来演示。

> "Knowing that something is theoretically possible is not the same as having seen it done for yourself."

知道某事理论上可行 ≠ 亲眼见过它实现。

---

## Simon的知识囤积方式

| 工具 | 内容 |
|------|------|
| **Blog + TIL Blog** | 我弄清楚如何做的各种事情的笔记 |
| **GitHub (1000+ repos)** | 不同项目写的代码，很多是展示关键想法的小概念验证 |
| **tools.simonwillison.net** | LLM辅助工具和原型的最大集合（HTML工具） |
| **simonw/research** | 更大更复杂的例子——让Coding Agent研究问题并带回工作代码和详细报告 |

---

## 重组你的知识库

### 核心策略

将多个现有工作示例组合起来创建新解决方案——这是Simon最喜欢的prompt模式之一。

### 实战案例：PDF OCR工具

**目标**：需要一个简单、基于浏览器的工具，从PDF文件中提取页面文字（特别是扫描版PDF）

**已有的两个知识片段**：
1. 曾实验过 Tesseract.js —— 可在浏览器中运行的OCR库
2. 曾使用 Mozilla PDF.js —— 可以将PDF页面渲染为图片

**组合Prompt**：
```
This code shows how to open a PDF and turn it into an image per page:
[嵌入PDF.js代码]

I want to combine this with Tesseract.js OCR to create a tool that...
```

**结果**：一个浏览器内运行的PDF OCR工具

---

## Coding Agent如何放大知识价值

### 知识 → Agent输入

> "One of my favorite prompting patterns is to tell an agent to build something new by combining two or more existing working examples."

**最喜欢的Prompt模式之一**：告诉Agent通过组合两个或多个现有工作示例来构建新东西。

### 关键洞察

| 资产类型 | 对Agent的价值 |
|----------|---------------|
| 理论知识 | 让Agent知道可能性的边界 |
| 运行过的代码 | 给Agent具体实现参考 |
| 组合示例 | Agent可以用作解决方案的构建块 |

---

## 实践建议

### 如何建立你的知识库

1. **记录每个"原来可以这样"的发现**
2. **保留可运行的代码示例**（不只是笔记）
3. **用LLM扩展你的代码解决方案集合**
4. **组合示例发给Agent**——"我有A和B，能帮我做C吗？"

### 知识复用循环

```
积累知识 → 组合示例 → Agent实现 → 新知识 → 继续积累
```

---

## 关键金句

> "The assets you generate along the way become powerful inputs for your coding agents."

**你一路生成的资产会成为Coding Agent的强力输入。**

---

## 相关文档

- [[insights/technology/insight-20260428-simon-willison-code-is-cheap|Writing code is cheap now]] (同来源)
- [[insights/technology/insight-20260428-simon-willison-better-code|AI should help us produce better code]] (同来源)
- [[topic-knowledge-management/second-brain|第二大脑方法论]]

---

## 参考来源

- [Simon Willison Hoard Things原文](https://simonwillison.net/guides/agentic-engineering-patterns/hoard-things-you-know-how-to-do/)

---

**记录时间**: 2026-04-28 08:35  
**记录者**: 尼克·弗瑞 (Nick Fury)  
**状态**: ✅ 已引入Wiki

