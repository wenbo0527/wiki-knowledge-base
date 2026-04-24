# Harrison Chase "记忆即锁定"：Agent时代的新平台战争

> **来源**: Get笔记 - 盯人日报 #044
> **发布时间**: 2026-04-13
> **核心事件**: LangChain发布Deep Agents，Chase提出"Agent记忆主权"概念
> **评分**: ⭐⭐⭐⭐⭐

---

## 📌 事件概述

Harrison Chase在LangChain官方博客发表战略长文《Your Harness, Your Memory》，将Deep Agents的定位从"又一个框架"升级为**"Agent记忆主权"议题**。

**核心论点**：谁控制了Agent harness，谁就控制了用户的记忆，形成强锁定。

---

## 💡 核心洞察

### 1. Agent Harness的不可消失性

**Chase的论据**：
- Claude Code泄露的51.2万行代码证明：Agent harness的复杂度不减反增
- 无论模型多强，都需要harness来管理工具调用、任务分解、上下文
- **"Agent harness是构建Agent的主流方式且不会消失"**

### 2. 记忆作为核心差异化

| 维度 | 传统软件 | Agent |
|------|----------|-------|
| 用户数据 | 文档、数据 | 对话历史、决策模式、偏好 |
| 差异化来源 | 功能特性 | 记忆质量 |
| 锁定方式 | 功能依赖 | 记忆迁移成本 |

### 3. 闭源Harness = 记忆让渡

**Chase的逻辑链**：

```
闭源Agent harness
    ↓
用户记忆存储在第三方服务器
    ↓
记忆成为平台锁定的新形式
    ↓
用户无法迁移到其他Agent
    ↓
形成类似App Store的锁定效应
```

### 4. 开放vs闭源的新战场

| 阵营 | 产品 | 记忆政策 |
|------|------|----------|
| **闭源** | Claude Code、Codex | 记忆存储在平台 |
| **开源** | Deep Agents | 记忆归用户 |

---

## 🔥 "记忆即锁定"的战略意义

### 类比：移动互联网的App Store锁定

| 时代 | 锁定机制 | 受害者 |
|------|----------|--------|
| PC软件 | 许可证激活 | 用户 |
| 移动互联网 | App Store审查+分成 | 开发者 |
| AI Agent时代 | Agent记忆 | 用户+开发者 |

### 对OpenClaw的启示

**OpenClaw作为开源Agent平台**：
- 记忆主权是核心竞争优势
- 用户应该拥有自己的记忆数据
- 可迁移性是关键用户体验

---

## 📊 Harrison Chase的核心论点

### 记忆的三层价值

| 层级 | 内容 | 锁定风险 |
|------|------|----------|
| **短期记忆** | 当前对话上下文 | 低 |
| **中期记忆** | 项目历史、决策 | 中 |
| **长期记忆** | 跨项目偏好、技能 | 高 |

### "开放"的具体含义

**不是**：
- 代码开源就够了
- API开放就够了

**而是**：
- 用户记忆可以完整导出
- 用户可以切换到其他Agent而保留记忆
- 记忆的格式是开放的

---

## 💼 商业影响

### 对AI公司的启示

| 公司 | 当前策略 | 风险 |
|------|----------|------|
| Anthropic | Claude Code闭源 | 面临"记忆锁定"质疑 |
| OpenAI | Codex闭源 | 同上 |
| LangChain | Deep Agents开源 | 差异化机会 |

### 对用户的启示

> 在选择Agent产品时，记忆的归属权和可迁移性将成为关键决策因素。

**评估标准**：
1. 我的记忆能被导出吗？
2. 我能迁移到其他Agent吗？
3. 如果这家公司的商业模式变了，我的记忆还在吗？

---

## 🔗 Wiki链路关联

- [[insight-20260417-harness-engineering]] - Harness Engineering概述
- [[insight-20260418-karpathy-claude-md-agent-config]] - CLAUDE.md配置模板
- [[insight-20260418-skill-development]] - Skill开发方法论
- [[insight-20260418-agent-27-design-patterns]] - Agent设计模式

---

## 📚 参考资源

- [LangChain Blog: Your Harness, Your Memory](https://blog.langchain.com/your-harness-your-memory/)
- [Deep Agents GitHub](https://github.com/langchain-ai/deepagents)

---

*Insight 创建: 2026-04-18*
*来源: Get笔记盯人日报 #044 / 尼克·弗瑞*
