# 天工万象：蚂蚁消金Multi-Agent智能体平台
能力框架: capability-requirement-decision capability-tech-understanding

> **来源**: Get笔记大前端技术精选 | **发布时间**: 2025-08 | **分类**: Architecture / Multi-Agent
> **Insight ID**: insight-20250823-tian-gong
> **维护者**: 尼克·弗瑞 | **更新**: 2026-05-11

---

## 📌 一句话判断

> 蚂蚁消金前端团队开发的Multi-Agent智能体平台，基于LangGraph构建，采用ReAct范式实现自我反思与工具调用，支持多场景业务处理。

---

## 核心架构

### 技术栈

| 组件 | 技术 |
|:---|:---|
| 架构模式 | LangGraph有向图模型 |
| 记忆存储 | Zcache跨机房记忆存储 |
| 输出管道 | SSE流式输出 |
| 决策机制 | ReAct动态反思循环 |

### 多Agent协同

| Agent类型 | 功能 |
|:---|:---|
| 调度中枢 | 协调各Agent工作 |
| 网页开发专家 | 专项网页开发 |
| 同业小qiu | 行业分析 |
| 全能小助手 | 通用问题处理 |

---

## 与Manus/Dify对比

| 维度 | 天工万象 | Manus/Dify |
|:---|:---|:---|
| 架构模式 | 分布式Multi-Agent | 中心化调度器 |
| 决策机制 | ReAct动态反思 | 静态工作流节点编排 |
| 上下文管理 | 跨Agent共享记忆 | 单Agent token限制 |
| 工具调用 | 按需动态调用 | 预定义节点连接 |

---

## 工具集

- **sequentialThinking** - 反思工具
- **fileRag** - 文档检索
- **interbankAnalysis** - 同业分析

---

## 🔗 关联专题

- [[Multi-Agent]] - 多Agent系统
- [[LangGraph]] - LangGraph

---

## 🏷️ 标签

`#天工万象` `#蚂蚁消金` `#Multi-Agent` `#LangGraph` `#ReAct` `#智能体平台`

---

*本文档由尼克·弗瑞基于Get笔记整理*
*情报是决策的基础。我不收集信息，我生产洞察。*
