# Insight: Harness Engineering完整指南（2026年必修课）

> **来源**: AI辅助软件开发伍斌 公众号
> **发布时间**: 2026-04-23 08:21
> **原文链接**: https://mp.weixin.qq.com/s/8JewG1UMM5lIowLBGIpYjw
> **标签**: AI编程, Harness Engineering, Agent工程
> **评级**: ⭐⭐⭐⭐⭐

---

## 一句话总结

AI编程的核心不是模型，而是Harness（运行环境）——改变Harness比换模型更有效。

---

## 核心公式

```
AI Agent = Model（模型）+ Harness（运行环境）

Harness（中文常译作"挽具"或"智能体环境"）
= 围绕AI模型构建的一切
= 工具 + 指令 + 状态管理 + 验证机制 + 运行时基础设施
```

> "The model contains the intelligence and the harness is the system that makes that intelligence useful."
> — LangChain《The Anatomy of an Agent Harness》

---

## 背景痛点：为什么需要这个概念？

随着Claude、Codex等大语言模型在2024-2025年被广泛用于实际软件开发，工程师们普遍遭遇了4类难以用"更好的提示词"解决的深层问题：

| 痛点 | 表现 | 根因 |
|------|------|------|
| **Agent反复犯同类错误** | 每次新会话从零开始，没有记忆 | 缺乏持久化机制 |
| **长任务跨上下文窗口失败** | 上下文窗口结束时Agent记忆归零 | 单次上下文限制 |
| **模型性能与运行环境强耦合** | 同一模型在不同环境下性能差异巨大 | 环境比模型更重要 |
| **缺乏系统性工程方法论** | 提示工程没回答"如何持续可靠工作" | 方法论缺失 |

---

## 发展脉络

| 时间 | 机构/人 | 事件 |
|------|---------|------|
| 2025-11 | Anthropic | Justin Young发表《Effective harnesses for long-running agents》，提出双Agent架构 |
| 2026-02-05 | Mitchell Hashimoto | 正式命名"Harness Engineering"，提出简单/复杂问题分类处理 |
| 2026-02-11 | OpenAI | Ryan Lopopolo发表《Harness engineering: leveraging Codex in an agent-first world》 |
| 2026-02-17 | Thoughtworks | Birgitta Böckeler提出计算型/推理型控制分类 |
| 2026-03-10 | LangChain | Vivek Trivedy提出"Agent = Model + Harness"公式，Terminal Bench证明改变Harness排名从前30到前5 |
| 2026-03-24 | Anthropic | Prithvi Rajasekaran引入生成器-评估器双Agent架构和冲刺合同机制 |
| 2026-04-02 | Thoughtworks | Birgitta Böckeler在martinfowler.com发表，将控制论引入，提出前馈导引+反馈传感框架 |

---

## 核心理论框架

### 1. Agent = Model + Harness

| 组件 | 职责 |
|------|------|
| Model（模型） | 提供智能 |
| Harness（运行环境） | 让智能变得有用 |

**关键洞察**：顶尖外科医生光有技术不够，还需要手术室、器械、助手、术后流程——AI也一样。

### 2. 前馈导引 + 反馈传感（Thoughtworks）

```
         前馈导引（Feedforward）
    ─────────────────────────────>
    
    [Agent] ──────────────> [任务完成]
    
    <─────────────────────────────
         反馈传感（Feedback）
```

| 机制 | 作用 |
|------|------|
| 前馈导引 | 在行动前给出明确指令和约束 |
| 反馈传感 | 在行动后检测结果并调整 |

### 3. 简单问题 vs 复杂问题（Mitchell Hashimoto）

| 类型 | 处理方式 | 示例 |
|------|----------|------|
| **简单问题** | 直接更新AGENTS.md，每行对应一个不良行为 | "不要用XXX API，用YYY替代" |
| **复杂问题** | 编写专用工具 + 更新文档告知Agent | 截图脚本、过滤测试运行器 |

### 4. 生成器-评估器双Agent架构（Anthropic）

| Agent | 职责 |
|-------|------|
| 生成器Agent | 负责编码实现 |
| 评估器Agent | 负责验证和反馈 |

---

## Harness的类型

### 计算型 vs 推理型控制

| 类型 | 特点 | 适用场景 |
|------|------|----------|
| **计算型** | 精确控制，规则驱动 | 数据处理、格式转换 |
| **推理型** | 灵活控制，引导驱动 | 需求分析、架构设计 |

### LangChain的Harness定义（最宽泛）

Harness = 除模型以外的一切：
- 文件系统
- 工具（Tools）
- 沙箱（Sandbox）
- 编排（Orchestration）
- 运行时基础设施

---

## 实践指南

### 关键原则

1. **环境比模型更重要**
   - Terminal Bench 2.0数据：改变Harness排名从前30到前5
   - OpenAI经验：3名工程师5个月零行人工代码构建100万行系统

2. **Harness需要工程化**
   - 不是"更好的提示词"
   - 而是"让模型持续可靠工作的系统"

3. **渐进式改进**
   - 每次发现Agent犯错，花时间设计解决方案
   - 让这个Agent永远不再犯这个错误

### 实践技巧

| 场景 | 技巧 |
|------|------|
| 记忆持久化 | 使用progress文件跨会话保存状态 |
| 错误防止 | AGENTS.md中每行对应一个已知不良行为 |
| 长任务拆分 | 双Agent架构：生成器+评估器 |
| 进度追踪 | 使用JSON特性列表跟踪完成情况 |
| 质量门控 | Sprint Contract：定义"完成"的标准 |

---

## 相关资源

| 来源 | 链接 |
|------|------|
| Anthropic原文 | https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents |
| Mitchell原文 | https://mitchellh.com/writing/my-ai-adoption-journey |
| OpenAI原文 | https://openai.com/index/harness-engineering/ |
| LangChain原文 | https://www.langchain.com/blog/the-anatomy-of-an-agent-harness |
| Thoughtworks原文 | https://martinfowler.com/articles/harness-engineering.html |

---

## 关联Insight

- [[insight-20260419-harness-engineering]] - Harness Engineering早期版本
- [[insight-20260417-mitchell-ai-adoption-journey]] - Mitchell六阶段采纳模型
- [[insight-20260419-harness-agent]] - Harness Agent架构
- [[insight-20260422-context-compression-methodology]] - 上下文压缩方法论（相关）

---

## 关联专题

- [[ai-native/agent-engineering]] - Agent工程化实践
- [[ai-programming/vibe-coding]] - Vibe Coding上下文管理
- [[ai-programming/README]] - AI编程专题

---

*本文档由尼克·弗瑞整理 | 2026-04-23*
*基于11篇原始资料：OpenAI、Anthropic、Thoughtworks、LangChain、HumanLayer、Inngest及学术论文*
