# Andrej Karpathy

> AI研究员，特斯拉前Autopilot负责人，OpenAI创始成员

---

## 元信息

- **创建时间**: 2026-04-08
- **更新时间**: 2026-04-08
- **类型**: person
- **标签**: #AI #deep-learning #researcher #openai #tesla

## 简介

Andrej Karpathy 是著名的AI研究员和计算机科学家，斯坦福大学博士（导师：李飞飞），曾在Tesla担任AI总监，在OpenAI担任研究员。现已离开，专注于教育内容。

## 关键成就

| 成就 | 年份 | 说明 |
|------|------|------|
| DeepMind实习 | 2011 | 本科阶段 |
| Stanford PhD | 2011-2016 | 李飞飞教授指导下研究CNN/RNN |
| OpenAI研究员 | 2015-2017 | 创始成员 |
| Tesla AI总监 | 2017-2022 | 负责Autopilot |
| 回归OpenAI | 2022-2024 | 再次离开 |
| 教育事业 | 持续 | YouTube教学 |

## 核心贡献

### 开源项目

| 项目 | Stars | 说明 |
|------|-------|------|
| [llm.c](https://github.com/karpathy/llm.c) | 32k+ | 纯C/CUDA训练LLM |
| [nanoGPT](https://github.com/karpathy/nanoGPT) | 14k+ | 最小GPT实现 |
| [nanochat](https://github.com/karpathy/nanochat) | 9k+ | 端到端ChatGPT |
| [microGPT](https://github.com/karpathy/microgpt) | 5k+ | 200行Python实现GPT |

### YouTube教学

- **Neural Networks: Zero to Hero** - 从零到英雄系列
- **Building a GPT Tokenizer** - 分词器实现
- **Let's build GPT** - 从零实现GPT

### 博客文章

| 文章 | 日期 | 说明 |
|------|------|------|
| [microgpt](https://karpathy.github.io/2026/02/12/microgpt/) | 2026-02-12 | 200行Python实现GPT |
| [Deep Neural Nets: 33 years ago and 33 years from now](https://karpathy.github.io/2022/03/14/lecun1989/) | 2022 | 神经网络历史对比 |
| [A Recipe for Training Neural Networks](https://karpathy.github.io/2019/04/25/recipe/) | 2019 | ⭐ 训练神经网络食谱 |

## 核心观点

### LLM Wiki模式 🆕

Karpathy提出了一种新的**LLM知识管理范式**：

> "传统RAG每次查询都重新检索，无积累。LLM Wiki让知识编译一次，持续更新。"

**核心思想**：
- 不只是检索，而是**编译**知识
- 建立**持久wiki**，不是一次性问答
- 交叉引用已建立，矛盾已标记

**三层架构**：
1. Raw Sources - 原始资料（不可变）
2. Wiki - LLM生成的Markdown（可更新）
3. Schema - 工作流约定（CLAUDE.md）

### 其他观点

- **数据质量**: "数据质量决定模型上限"
- **Tokenization**: BPE是核心，词表大小影响性能
- **极简实现**: 用最少代码理解核心原理

## 相关页面

- [[llm-wiki-pattern]] - LLM Wiki模式
- [[llm-agent]] - AI Agent
- [[rag]] - RAG技术

## 来源引用

- [Karpathy GitHub](https://github.com/karpathy)
- [Karpathy Blog](https://karpathy.github.io/)
- [Karpathy YouTube](https://www.youtube.com/@AndrejKarpathy)

---

*最后更新: 2026-04-08*
*维护者: 尼克·弗瑞*