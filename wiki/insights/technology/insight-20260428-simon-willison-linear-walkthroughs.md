# Insight: Simon Willison - Linear Walkthroughs 代码理解模式
能力框架: capability-tech-understanding

> **来源**: Simon Willison's Weblog（Agentic Engineering Patterns指南）  
> **作者**: Simon Willison（Django联合作者）  
> **发布日期**: 2026-02-25  
> **评级**: ⭐⭐⭐⭐⭐ (5/5)  
> **标签**: #代码理解 #AgenticEngineering #VibeCoding #SimonWillison #LinearWalkthrough

---

## 执行摘要

Simon Willison（Django联合作者）提出用Coding Agent生成代码"线性导览"（Linear Walkthrough）的模式。他发现Vibe Coding后自己对代码一无所知，于是用Claude Code + 自研工具Showboat 生成了完整的代码理解文档，避免了手动复制代码片段导致的AI幻觉问题。

---

## 背景：Vibe Coding的盲点

Simon Willison的亲身经历：
- 用Claude Code + Opus 4.6 vibe coding了一个SwiftUI幻灯片演示应用
- 代码发布到GitHub后，意识到自己对代码如何工作**一无所知**
- "我用prompt创造了整个东西，但没有关注它写的代码"

### 核心问题

> "我vibe coded了整个应用，但需要理解它实际上是如何工作的"

---

## 解决方案：Linear Walkthroughs

### 核心Prompt模板

Simon给Claude Code的Prompt：

```
Read the source and then plan a linear walkthrough 
of the code that explains how it all works in detail

Then run "uvx showboat –help" to learn showboat - 
use showboat to create a walkthrough.md file in the repo 
and build the walkthrough in there, using showboat note 
for commentary and showboat exec plus sed or grep or cat 
or whatever you need to include snippets of code you 
are talking about
```

### 关键设计：避免幻觉

> "By telling it to use 'sed or grep or cat', I ensured Claude Code would not manually copy snippets - that could introduce a risk of hallucinations or mistakes."

**核心洞察**：让Agent用Shell命令动态获取代码片段，而非手动复制——这样可以确保代码片段100%准确。

---

## Showboat工具

Simon Willison自研的文档生成工具：

| 命令 | 功能 |
|------|------|
| `showboat note` | 添加Markdown注释 |
| `showboat exec` | 执行Shell命令并记录输出 |

**优势**：
- 输出直接是Markdown格式
- 代码片段通过Shell命令获取，保证准确性
- 可追溯每段代码的来源

---

## 三步流程

```
Step 1: 理解代码
   └── 让Agent阅读整个代码库

Step 2: 规划导览结构
   └── 让Agent规划如何线性介绍代码

Step 3: 生成walkthrough.md
   └── 用showboat工具生成文档
       - showboat note: 解释性文字
       - showboat exec + grep/cat: 代码片段
```

---

## 应用场景

| 场景 | 说明 |
|------|------|
| **Vibe Coding后理解** | 快速掌握自己"vibe coded"的代码如何工作 |
| **新项目上手** | 快速理解新代码库的结构和逻辑 |
| **代码审查** | 结构化理解他人代码，生成审查报告 |
| **知识传承** | 为团队生成标准化的代码导览文档 |
| **遗留系统** | 用Agent帮助理解老旧的代码库 |

---

## 与其他方案对比

| 方案 | 代表 | 核心思路 | 优势 | 局限 |
|------|------|----------|------|------|
| **Linear Walkthroughs** | Simon Willison | Agent生成结构化文档 | 零预处理、完整理解 | 依赖Agent能力 |
| **RAG向量检索** | Copilot | 语义搜索代码片段 | 快速定位 | 无结构感知 |
| **UModel知识图谱** | 阿里云 | 构建代码关系图 | 结构推理 | 需要预建图 |

---

## 核心金句

> "I vibe coded the whole thing without paying any attention to the code it was writing."

> "By telling it to use 'sed or grep or cat', I ensured Claude Code would not manually copy snippets."

> "Frontier models with the right agent harness can construct a detailed walkthrough to help you understand how code works."

---

## 关联文档

- [[insight-20260423-umodel-code-knowledge-graph|UModel代码知识图谱]] (阿里云方案)
- [[insight-20260419-harness-engineering|Harness Engineering]] (Harness层)
- [[topic-ai-native/ai-programming/vibe-coding|Vibe Coding专题]]

---

## 参考来源

- [Simon Willison原文](https://simonwillison.net/guides/agentic-engineering-patterns/linear-walkthroughs/)
- Showboat工具: `uvx showboat`

---

**记录时间**: 2026-04-28 08:10  
**记录者**: 尼克·弗瑞 (Nick Fury)  
**状态**: ✅ 已引入Wiki

