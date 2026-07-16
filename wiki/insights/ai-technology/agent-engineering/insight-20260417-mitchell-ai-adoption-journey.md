---
title: insight 20260417 mitchell ai adoption journey
author: 尼克·弗瑞 🕵️
product_domain: PD-INSIGHT
doc_type: 其他
tags: [insights, ai-technology, agent-engineering]
date: 2026-04-24
---

# Mitchell Hashimoto：AI采纳六阶段模型
能力框架: capability-value-closed-loop capability-tech-understanding

> 来源：Mitchell Hashimoto 博客 (2026-02-05)
> 原文：https://mitchellh.com/writing/my-ai-adoption-journey
> 整理时间：2026-04-17

## 📌 基本信息

| 属性 | 值 |
|------|-----|
| **作者** | Mitchell Hashimoto |
| **身份** | HashiCorp联合创始人、Terraform缔造者 |
| **发布时间** | 2026-02-05 |
| **标签** | `#harness` `#ai-adoption` `#practitioner` |

---

## 🎯 六阶段采纳模型

Mitchell Hashimoto 将个人AI采纳分为六个阶段，这是业内首个完整的实践路径框架。

### 阶段一览

| 阶段 | 名称 | 核心动作 | 关键洞察 |
|:---:|------|----------|----------|
| 1 | **Drop the Chatbot** | 停用聊天界面，改用Agent | 聊天界面效率低，Agent才能做实事 |
| 2 | **Reproduce Your Own Work** | 强迫Agent重做一遍手动工作 | 做两遍才能形成技能，摩擦是正常的 |
| 3 | **End-of-Day Agents** | 下班跑Agent，第二天来收获 | 利用时间差，warm start |
| 4 | **Outsource the Slam Dunks** | 简单任务交给后台Agent | 专注深度工作 |
| 5 | **Engineer the Harness** | 错必工程化 | 每次错误都要系统化解决 |
| 6 | **Always Have an Agent Running** | 常驻Agent | 持续产出 |

---

## 各阶段详解

### 阶段1：Drop the Chatbot

**核心观点**：立即停止通过聊天界面（如ChatGPT、Gemini网页版）进行编程。

**问题**：
- 结果依赖模型训练知识，无法控制
- 纠正错误需要人类反复告知
- 效率明显低于自己动手

**例外**：聊天界面仍有日常价值，但编程工作不适用。

### 阶段2：Reproduce Your Own Work

**核心观点**：强迫自己用Agent重新做一遍手动完成的工作，哪怕做两遍。

**关键洞察**：
- 一次成功的Session不足以形成技能
- 必须刻意练习才能建立直觉
- 摩擦是正常的，不能因此放弃

**具体做法**：
1. 手动完成工作
2. 在不看手动方案的情况下，让Agent重做
3. 对比结果，优化Agent配置

**技能形成发现**：
- 把任务拆分为清晰的子任务
- 模糊请求要分离规划和执行

### 阶段3：End-of-Day Agents

**核心观点**：下班前给Agent分配任务，第二天早上来收获结果。

**价值**：利用非工作时间进行AI工作，实现"warm start"。

**具体任务类型**：
1. **Deep Research Sessions**：让Agent调研特定领域，如"找出某语言所有特定许可证的库，并对每个库的生产活跃度、社会情绪做多页摘要"
2. **Parallel Agents for Vague Ideas**：并行启动多个Agent探索模糊想法，不期待产出可交付成果，但可能在第二天发现未知的未知
3. **Issue/PR Triage via gh CLI**：用GitHub CLI自动分类Issue和PR，只要求报告不要求回复，筛选高价值/低难度任务

> **注意**：大多数Agent在半小时内完成，无需通宵跑。关键是让Agent在个人效率低谷期（下班前）启动，带来第二天"warm start"。

---

### 阶段4：Outsource the Slam Dunks

**核心观点**：把简单、高频、模式化的任务交给后台Agent处理。

**目标**：让自己专注于需要深度思考的工作。

**关键操作**：每天从夜间分类报告筛选出"Agent几乎肯定能解决好"的问题，后台逐一运行（不并行），同时自己做深度工作。

**⚠️ 重要原则：关闭Agent桌面通知**
> "Context switching is very expensive. Be in control of when YOU interrupt the agent, not the other way around."

Agent不应主动打扰你。在自然工作间隙检查进度，而非被通知打断。

**Skill Formation平衡**：把任务交给Agent意味着放弃该任务的技能形成，但你仍在深度工作中继续形成技能——关键是有意识地选择把哪些任务留给自己。

### 阶段5：Engineer the Harness ⭐（核心）

**核心定义**：
> "每当你发现Agent犯了一个错误，你就花时间去工程化一个解决方案，让它再也不会犯同样的错。"

**核心洞察**：
- Agent最大的问题不是能力不够，而是不听话
- 每次错误都要转化为系统改进
- Ghostty项目实战：AGENTS.md的每一行都对应一次Agent不良行为

**实战案例（Ghostty）**：
```
那个文件(AGENTS.md)里的每一行都基于一次Agent的不良行为，
而且几乎完全解决了这些问题。
```

### 阶段6：Always Have an Agent Running

**核心观点**：保持至少一个Agent持续运行，持续产出。

**目标**：最大化Agent利用率，实现持续价值交付。

**实践状态**：目前 Mitchell 每天约10-20%的时间有后台Agent运行，正在努力提升。

**与深度模型结合**：他偏好结合慢速、深思模型（如AMP的deep mode，本质是GPT-5.2-Codex），这类模型可能需要30+分钟做小改动，但产出质量很高。

**核心逻辑**：不是为跑Agent而跑Agent，而是持续问自己"现在有什么任务值得委托给Agent？"并持续改善工作流和工具以创造委托任务流——这本身也是重要的工作。

---

## 🔑 核心原则总结

### Mitchell 的关键洞察

1. **摩擦是正常的**：采用新工具必然经历低效期，不能因此放弃
2. **技能需要刻意练习**：看别人说和自己做有本质区别
3. **任务拆分至关重要**：不要"draw the owl"（一步登天）
4. **错必工程化**：每次错误都要形成系统改进，不能只是修复表面
5. **约束产生效率**：明确的边界让Agent更快收敛
6. **主动委托**：持续问有什么可以委托，而非等有明确任务才跑Agent

### 对模型能力的态度

> "现代编程模型（如Opus、Codex）专门训练过偏向使用工具，这不同于对话模型。由于模型创新速度快，需要不断重新评估这一判断。"

### ⚠️ 对Junior开发者的警示

Mitchell 在脚注中特别提到：

> "The skill formation issues particularly in juniors without a strong grasp of fundamentals deeply worries me, however."

**含义**：如果初级开发者没有扎实的 fundamentals 就大量依赖Agent，会导致技能形成障碍——他们无法判断Agent输出的质量，也无法在Agent失败时独立修正。这是一个需要正视的结构性风险。

---

## 🔗 关联知识

- [[insight-20260417-harness-engineering]] - Harness Engineering总体介绍
- [[insight-20260417-harness-engineering-deep-research]] - 深度情报汇总
- [[topics/ai-native/agent-engineering]] - Agent工程实践入口

---

## 📚 参考资源

| 资源 | 链接 |
|------|------|
| 原文博客 | https://mitchellh.com/writing/my-ai-adoption-journey |

---

*维护者：尼克·弗瑞*
*深化补充：2026-05-04*
*整理时间：2026-04-17*
*来源：Mitchell Hashimoto 博客*
