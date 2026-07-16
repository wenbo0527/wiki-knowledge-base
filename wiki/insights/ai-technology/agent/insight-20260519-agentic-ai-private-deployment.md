---
能力框架: "#tech-understanding #product-design"
来源: "微信公众号 | 发布时间: 2026-05-19 | 分类: AI Technology / Agent Engineering"
Insight ID: insight-20260519-agentic-ai-private-deployment
维护者: "尼克·弗瑞 | 更新: 2026-05-20"
title: insight 20260519 agentic ai private deployment
author: 尼克·弗瑞 🕵️
product_domain: PD-INSIGHT
doc_type: 其他
tags: [insights, ai-technology, agent]
date: 2026-05-23
---


## 📌 执行摘要

**核心目标**：通过LLM后训练技术，基于Manus或开源灵思框架，提升小模型在复杂任务中的性能，实现私有化环境下更小、更可控模型的高效部署。

**测试效果**：

| 模型 | Crash Rate | 总评分（满分10分） |
|:---|:---|:---|
| **Lightspeed-14B** | **10%** | **6.97** |
| GPT-4 | 16% | 6.69 |
| Qwen3-235B | 23% | 6.11 |
| DeepSeek-V3 | 26% | 4.67 |

**核心发现**：14B小模型通过后训练可达甚至超越超大模型水平

---

## 🔬 Agentic AI特点

| 能力 | 说明 |
|:---|:---|
| **自主路径规划** | 根据任务目标和资源自主规划解决路径 |
| **自主工具使用** | 通过function calling与外部系统交互 |
| **自主反思能力** | 判断信息充分性、检查错误并改进策略 |

**与Chat/Workflow AI对比**：对逻辑推理、上下文理解、工具调用及指令跟随能力要求更高

---

## 🏗️ 数据合成与训练流程

```
Query生成 → Diverse resources → Trajectory Generation → End-to-end scoring → Reject fitting → SFT+DPO训练
```

### 核心步骤

1. **Query生成**：生成多样化目标任务
2. **Diverse resources**：丰富目标所需资源，确保数据多样性
3. **Trajectory Generation**：运行agent框架生成结果及中间prompt-response对
4. **End-to-end scoring**：端到端打分筛选高质量数据
5. **Reject fitting**：选取打分最高的20%数据用于SFT训练
6. **SFT+DPO训练**：先监督微调，再通过DPO强化学习

### 评估方法

采用**process level compare**方法，对每个步骤独立优化，追求当前步骤最优动作。

**多维度评估体系**：
- 生成评估维度（脚本结构、节奏控制、技术指导质量）
- 制定各维度打分标准（1-10分）
- 大模型根据标准对答案打分并综合评分

---

## 🎯 关键挑战与解决

### 多维度自动化评估

**测试结论**：
- 模型易打高分，需重点关注不足部分扣分
- few-shot能更好匹配人工打分
- **multi dimension方法效果最佳**

### SFT监督数据生成

| 数据要求 | 具体措施 |
|:---|:---|
| **准确性** | 确保工具选择正确、参数使用正确、任务交接合理 |
| **多样性** | 覆盖多行业/问题类型/主题；引入多样化工具 |

### DPO数据合成

1. 模型生成n个response
2. **规则判断**：检查JSON格式合规性、SOP完整性、幻觉问题
3. **模型评分**：大模型对通过规则检查的response打分
4. **构建对比数据**：将分数差异显著的response配对作为DPO训练数据

### DPO训练优化

采用**校准DPO loss**：
- 使better response的reward持续增大（保持正值）
- 使worse response的reward尽可能小（接近负值）
- 扩大两者的reward差值（margin）

**效果改进**：降低crash rate、提升整体评分、解决SFT后存在的SOP不完整问题

---

## 💡 关键洞察

1. **小模型可通过后训练超越大模型**：在特定Agentic任务上，14B模型超过GPT-4
2. **数据质量比数量更重要**：选取打分最高的20%数据
3. **Process level compare优于结果级ORM**：对每个步骤独立优化
4. **DPO训练解决SFT遗留问题**：SFT后流程中断、JSON格式错误等

---

## 📅 未来规划

1. **模型开源**：计划开源14B模型，降低私有化部署门槛
2. **丰富工具与任务**：扩展编程场景、实现分析型网页生成等复杂任务
3. **多维度评估**：引入视觉模型评估HTML输出，通过测试用例评估软件生成效果
