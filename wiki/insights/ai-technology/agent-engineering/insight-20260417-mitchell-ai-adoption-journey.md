# Mitchell Hashimoto：AI采纳六阶段模型

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

### 阶段4：Outsource the Slam Dunks

**核心观点**：把简单、高频、模式化的任务交给后台Agent处理。

**目标**：让自己专注于需要深度思考的工作。

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

---

## 🔑 核心原则总结

### Mitchell 的关键洞察

1. **摩擦是正常的**：采用新工具必然经历低效期，不能因此放弃
2. **技能需要刻意练习**：看别人说和自己做有本质区别
3. **任务拆分至关重要**：不要"draw the owl"（一步登天）
4. **错必工程化**：每次错误都要形成系统改进，不能只是修复表面
5. **约束产生效率**：明确的边界让Agent更快收敛

### 对模型能力的态度

> "现代编程模型（如Opus、Codex）专门训练过偏向使用工具，这不同于对话模型。由于模型创新速度快，需要不断重新评估这一判断。"

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
*整理时间：2026-04-17*
*来源：Mitchell Hashimoto 博客*
