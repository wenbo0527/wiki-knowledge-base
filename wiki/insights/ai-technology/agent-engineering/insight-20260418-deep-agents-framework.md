# LangChain Deep Agents：AI Agent从框架期进入产品期

> **来源**: Get笔记 - 盯人日报 #043
> **发布时间**: 2026-04-11
> **核心事件**: LangChain发布Deep Agents，开源+易用+可控
> **评分**: ⭐⭐⭐⭐

---

## 📌 事件概述

LangChain发布Deep Agents——一个即开即用的Agent框架。

**定位**："agent harness"

**安装**：`pip install deepagents` 三行代码即可跑起来

---

## 💡 核心组件

| 组件 | 功能 |
|------|------|
| **planning** | write_todos任务分解 |
| **filesystem** | 读写文件 |
| **shell access** | 沙盒命令执行 |
| **sub-agents** | 隔离上下文委托 |
| **smart defaults** | 内置prompt教模型用工具 |
| **context management** | 对话过长自动摘要 |

---

## 💡 核心洞察

### 1. 从"提供积木"到"提供成品"

**Chase的策略转变**：
- 之前：LangGraph = 积木
- 现在：Deep Agents = 开箱即用的产品

**这是对"框架太多、能跑的太少"问题的直接回答。**

### 2. AI Agent产品的三极

| 产品 | 特点 | 定位 |
|------|------|------|
| **Karpathy autoresearch** | 纯脚本 | 个人工具 |
| **Anthropic Claude Code** | 闭源产品 | 商业产品 |
| **Deep Agents** | 开源+易用+可控 | **填补空白** |

### 3. 设计哲学

| 原则 | 说明 |
|------|------|
| **opinionated defaults** | 预设最佳实践 |
| **可定制化** | 满足个性化需求 |

---

## 🔮 对AI开发者的启示

### 1. 门槛正在降低

> 三行代码即可跑起来 = AI开发民主化

### 2. 与OpenClaw的对比

| 维度 | Deep Agents | OpenClaw |
|------|------------|----------|
| 开源 | ✅ | ✅ |
| 易用 | ✅ | ✅ |
| 可控 | ✅ | ✅ |
| 定位 | Agent框架 | Agent平台 |

### 3. "框架时代结束，产品时代开始"

**市场信号**：
- Q1风投80%流向AI
- 种子轮交易数下降30%
- 投资人从"什么都投"转向"只投能用的"

---

## 🔗 Wiki链路关联

- [[insight-20260417-harness-engineering]] - Harness Engineering概述
- [[insight-20260418-memory-as-lockin]] - 记忆主权问题
- [[insight-20260418-karpathy-claude-md-agent-config]] - CLAUDE.md配置模板

---

## 📚 参考资源

- [Deep Agents GitHub](https://github.com/langchain-ai/deepagents)
- [LangChain Blog](https://blog.langchain.com/your-harness-your-memory/)

---

*Insight 创建: 2026-04-18*
*来源: Get笔记盯人日报 #043 / 尼克·弗瑞*
