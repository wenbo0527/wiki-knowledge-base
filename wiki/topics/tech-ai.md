# 科技AI

> AI领域的实践追踪主题页，聚焦**AI Native开发**与**Agent工程化**落地实践

---

## 元信息

- **创建时间**: 2026-04-08
- **更新时间**: 2026-04-09
- **类型**: topic (主入口)
- **标签**: #AI #LLM #agent #vibe-coding #ai-native

## 主题概述

本专题追踪AI领域的工程化落地实践，涵盖：
- **AI Native Programming**: 用AI辅助编程、vibe coding方法论
- **Agent Engineering**: Agent系统架构、框架选型、工程实践
- **AI Application**: AI在各行业的落地案例
- **OpenClaw Practices**: Agent平台运维、团队协作实践

---

## 核心主线

### AI开发方法论演进

```
┌─────────────────────────────────────────────────────────────┐
│  AI开发方法论演进                                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  2022-2023 │ Prompt Engineering (提示词工程)               │
│             │ 用好大模型，单点优化                          │
│                                                              │
│  2024      │ AI Coding (AI辅助编程)                        │
│             │ Copilot、Cursor、V0辅助写代码                 │
│                                                              │
│  2025      │ Vibe Coding (氛围编程)                         │
│             │ 自然语言驱动开发，快速原型验证                 │
│                                                              │
│  2026      │ AI Native (AI原生开发) ← 我们在这里          │
│             │ Agent驱动开发、全流程AI化                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 子专题索引

### 1. [[ai-programming|AI编程实践]] ⭐

**定位**: Vibe Coding、AI辅助编程、Prompt Engineering实践

| 内容 | 说明 |
|------|------|
| **方法论** | Vibe Coding流程、AI结对编程、Prompt模板 |
| **工具链** | Cursor、V0、Copilot、Trae、Windsurf |
| **实战案例** | 托尼·斯塔克的编程实践 |

**核心问题**:
- 如何用AI把需求快速变成可运行代码？
- Prompt怎么写才能让AI输出高质量代码？
- Vibe Coding适合什么场景，不适合什么场景？

---

### 2. [[agent-engineering|Agent工程实践]] ⭐

**定位**: Agent系统架构、框架选型、工程落地

| 内容 | 说明 |
|------|------|
| **框架对比** | LangChain vs LangGraph vs AutoGen vs CrewAI |
| **架构模式** | 单Agent、多Agent协作、分层Agent |
| **工程实践** | 工具调用、记忆系统、规划能力、评估体系 |

**核心问题**:
- 如何构建可靠的Agent系统？
- 多Agent如何协作避免"群聊死锁"？
- Agent输出如何评估和控制？

---

### 3. [[palantir-ontology|本体论工程]] 🆕

**定位**: Palantir本体论方法论、AI知识图谱构建、业务语义映射

| 内容 | 说明 |
|------|------|
| **Palantir三产品** | Gotham → Foundry → AIP演进 |
| **本体论原理** | 物理世界→数字世界语义映射 |
| **工程实践** | 我们的"小本体论"落地方案 |

**核心问题**:
- 如何给AI装上"缰绳"，防止幻觉？
- 如何构建团队共享的业务知识图谱？
- 如何让AI回答"需求相关"问题？

---

### 4. [[ai-application|AI行业应用]] ⭐

**定位**: AI在各行业的落地实践与案例

| 内容 | 说明 |
|------|------|
| **金融AI** | 风控Agent、投研Agent、合规Agent |
| **企业AI** | 客服、销售、管理 |
| **开发工具** | 代码Agent、数据分析Agent |

---

### 5. [[ai-enterprise-implementation|AI企业落地]] 🆕

**定位**: 团队级AI编程推广、工程治理、量化评估

| 内容 | 说明 |
|------|------|
| **核心框架** | SDD-RIPER（持久化上下文 + 审批状态机） |
| **量化收益** | Bug率降18-37%，需求周期1-2周→3-4天 |
| **治理抓手** | 未经Plan Approved不得改代码 |

**核心问题**:
- 如何在团队里推开大模型编程？
- 如何建立质量保障机制？
- 如何量化AI编程的效果？

---

### 6. [[openclaw-practices|OpenClaw实践]]

**定位**: Agent平台运维、多Agent协作、团队管理

| 内容 | 说明 |
|------|------|
| **平台架构** | OpenClaw多Agent系统设计 |
| **协作机制** | Agent间通信、任务分发、结果汇聚 |
| **运维实践** | 监控、日志、容灾 |

---

## 快速导航

| 场景 | 推荐阅读 |
|------|----------|
| **想用AI写代码** | [[ai-programming]] |
| **想构建Agent系统** | [[agent-engineering]] |
| **想了解AI落地案例** | [[ai-application]] |
| **想用OpenClaw** | [[openclaw-practices]] |

---

## 最新洞察

> 来自RSS监控和最佳实践收集

### 2026年热点

| 热点 | 成熟度 | 实践价值 |
|------|--------|----------|
| **Vibe Coding** | ★★★★☆ | 直接可用的效率工具 |
| **多Agent协作** | ★★★☆☆ | 复杂任务分解 |
| **Agent评估** | ★★☆☆☆ | 工程化瓶颈 |
| **AI安全边界** | ★★★☆☆ | 企业落地关键 |

---

## 相关页面

### 内部链接
- [[fintech/llm-finance]] - 金融大模型应用
- [[knowledge-management]] - 知识管理
- [[data-platform]] - 数据中台

### 外部资源
- [Simon Willison](https://simonwillison.net) - AI工具深度评测
- [Lilian Weng](https://lilianweng.github.io) - Agent研究
- [OpenAI Blog](https://openai.com/blog) - 官方动态
- [Anthropic Blog](https://anthropic.com/blog) - Claude最新

---

## 相关实体

- [[apple]] - Apple（AI芯片、端侧AI）
- [[nvidia]] - NVIDIA（AI芯片）
- [[openai]] - OpenAI（GPT系列）
- [[anthropic]] - Anthropic（Claude系列）
- [[deepmind]] - DeepMind（AlphaGo系列）

## 相关洞察

- [[insight-20260409-agent-framework]] - Agent框架选型洞察
- [[insight-20260414-vibe-coding]] - Vibe Coding最佳实践

## 来源

- sources/rss/ - RSS监控文章
- sources/best_practices/ - 最佳实践收集
- projects/instreet/ - Instreet项目实践

---

*最后更新: 2026-04-16*
*维护员: 尼克·弗瑞*
