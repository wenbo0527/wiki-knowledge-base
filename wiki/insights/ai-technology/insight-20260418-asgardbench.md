# AsgardBench: 视觉 Grounding 交互式规划基准

> **来源**: Microsoft Research Blog
> **发布时间**: 2026-04-18
> **评分**: 83/100
> **标签**: Embodied AI、Vision-Language、Agent Planning、Benchmark

---

## 概述

AsgardBench 是微软研究院发布的 benchmark，用于评估 **embodied AI** 系统的"视觉 grounding 交互式规划"能力。

**核心问题**：现有 benchmark 同时测试感知、导航、物理控制，难以隔离 AI agent 是否真正利用视觉做决策。

---

## 核心问题

Imagine a robot tasked with cleaning a kitchen. It needs to observe its environment, decide what to do, and adjust when things don't go as expected.

例如：
- 杯子可能是干净的、脏的、或装满咖啡
- 水槽可能有许多其他物品
- 同样的指令需要根据任务展开情况执行不同的动作序列

这就是 **embodied AI** 的领域：感知环境并在其中行动的智能系统。

---

## 工作原理

```
┌─────────────────────────────────────────────────────────────┐
│                      AsgardBench 工作流                      │
├─────────────────────────────────────────────────────────────┤
│  1. Agent 提出完整任务步骤序列                               │
│  2. 只执行第一步                                             │
│  3. 接收新图像 + 简单成功/失败信号                            │
│  4. 迫使 Agent 在每步重新评估和修订计划                       │
│  5. 内置总步骤数和重复动作限制，防止无限循环                   │
└─────────────────────────────────────────────────────────────┘
```

**关键**：因为环境只提供简单反馈，agent 必须能够：
- 注意它所感知的内容（例如杯子是否脏、水龙头是否开着）
- 从一步到下一步跟踪任务进度

---

## 关键发现

### 1. 视觉输入至关重要
> "High-performing models require visual grounding to consistently succeed."

- **视觉输入使大多数模型成功率翻倍**
- 最强视觉模型即使给 text-only agent 详细反馈，仍优于它们

### 2. Benchmark 要求不可替代
AsgardBench 需要**基于感知的推理**，text-only 无法复制。

### 3. 当前模型共同失败点
| 失败类型 | 示例 |
|----------|------|
| 不可执行动作 | 试图清洁不在水槽的杯子 |
| 重复循环 | 陷入重复动作循环 |
| 视觉误判 | 误判微妙视觉线索（开/关，干净/脏） |
| 进度丢失 | 丢失任务进度跟踪 |

---

## 三大改进方向

1. **更细粒度的视觉区分能力**
   - 在杂乱场景中区分细微视觉细节

2. **更可靠的任务进度跟踪**
   - 在多步骤中可靠跟踪变化

3. **任务中途计划修订能力**
   - 学习在任务中途修订计划，而非按脚本推进

---

## 技术细节

### Benchmark 设计
- **反馈类型**：无反馈、最小反馈、详细反馈
- **评估维度**：感知能力、记忆能力、规划能力
- **成功指标**：不仅看是否成功，还看适应能力

### 数据来源
- 基于 AI2-THOR 社区的模拟平台
- 可复现的 embodied 评估

---

## 相关研究人员

| 作者 | 职位 |
|------|------|
| Andrea Tupini | Research Software Engineer |
| Lars Liden | Principal Research Software Engineer Manager |
| Reuben Tan | Researcher |
| Yu Wang | Principal RSDE |
| Jianfeng Gao | Technical Fellow & Corporate Vice President |

---

## 参考资料

- [AsgardBench 官方博客](https://www.microsoft.com/en-us/research/blog/asgardbench-a-benchmark-for-visually-grounded-interactive-planning/)
- Azure AI Foundry Labs

---

## 相关专题

- [[ai-agent|AI Agent 专题]]
- [[computer-vision|Vision-Language 专题]]
- [[robotics|机器人学专题]]

---

*Insight 创建: 2026-04-18*
*来源: Microsoft Research Blog*
*评估人: 尼克·弗瑞*
