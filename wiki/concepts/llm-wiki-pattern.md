# LLM Wiki Pattern

> Karpathy提出的LLM知识管理新范式：持久、增量、有机的Wiki

---

## 元信息

- **创建时间**: 2026-04-08
- **更新时间**: 2026-04-08
- **类型**: concept
- **标签**: #knowledge-management #LLM #Karpathy

## 核心定义

LLM Wiki Pattern是由Andrej Karpathy提出的一种**个人知识管理系统**范式，通过LLM增量构建和维护一个持久的、结构化的、互联的Markdown Wiki。

## 核心理念

> "知识应该被编译一次，然后保持最新，而不是每次查询时重新推导。"
> — Karpathy

### 对比：传统RAG vs LLM Wiki

| 维度 | 传统RAG | LLM Wiki |
|------|---------|----------|
| **知识状态** | 每次重新检索 | 持久积累 |
| **交叉引用** | 无 | 已建立 |
| **矛盾处理** | 未标注 | 已标记 |
| **综合** | 每次重新综合 | 已完成 |
| **积累性** | 无 | 持续丰富 |

## 三层架构

```
┌─────────────────────────────────────┐
│  Layer 1: Raw Sources              │
│  - 原始文档、URL、书籍              │
│  - 不可变，作为真相来源             │
├─────────────────────────────────────┤
│  Layer 2: The Wiki                 │
│  - LLM生成的Markdown文件            │
│  - 实体页、概念页、主题页           │
│  - 可更新，LLM完全拥有              │
├─────────────────────────────────────┤
│  Layer 3: The Schema               │
│  - CLAUDE.md/AGENTS.md              │
│  - 定义结构、约定、工作流            │
│  - 与LLM共同演进                    │
└─────────────────────────────────────┘
```

## 三种操作

### 1. Ingest（消化）

当你添加新资料时：
1. LLM阅读源文档
2. 识别关键实体和概念
3. 创建/更新相关Wiki页面
4. 更新index.md
5. 记录到log.md

**关键**：单条source可能涉及10-15个Wiki页面

### 2. Query（查询）

当用户提问时：
1. LLM读取index.md找到相关页面
2. 阅读相关页面的摘要
3. 综合生成回答
4. **如果回答有价值，存入insights/作为新页面**

### 3. Lint（健康检查）

定期检查：
- 矛盾：同一实体在不同页面的描述是否矛盾
- 过时：时间超过3个月且未更新的页面
- 孤立：没有任何引用的页面
- 缺失：重要概念无专属页面

## 两种特殊文件

### index.md - 内容索引

```markdown
# Wiki Index

## Entities
- [[nvidia]] - NVIDIA公司
- [[openai]] - OpenAI公司

## Concepts
- [[llm-wiki-pattern]] - LLM Wiki模式
- [[rag]] - RAG技术

## Topics
- [[tech-ai]] - 科技AI主题
```

### log.md - 操作日志

```markdown
## [2026-04-08] ingest | RSS Daily 20260408
- 新增: NVIDIA实体页
- 更新: AI主题页
- 涉及: sources/rss/daily/20260408.md
```

## Wiki页面类型

| 类型 | 说明 | 示例 |
|------|------|------|
| **Entity** | 实体 | `nvidia.md`, `openai.md` |
| **Concept** | 概念 | `llm-wiki-pattern.md` |
| **Topic** | 主题 | `tech-ai.md`, `investment.md` |
| **Insight** | 洞察 | `insight-20260408-analysis.md` |
| **Temporal** | 时序 | `weekly-2026-W15.md` |

## 页面模板

```markdown
# Title

> 一句话概括

## 元信息
- **创建时间**: YYYY-MM-DD
- **更新时间**: YYYY-MM-DD
- **类型**: entity/concept/topic/insight
- **标签**: #tag1, #tag2

## 摘要
一两句话概括核心内容。

## 详细内容

## 相关页面
- 相关页面（待补充）

## 来源引用
- [source](url) - 引用说明
```

## 应用场景

| 场景 | 说明 |
|------|------|
| **个人成长** | 目标、健康、心理追踪 |
| **研究** | 深入研究某主题数周/数月 |
| **读书** | 构建角色页、主题页、情节线 |
| **团队** | 内部Wiki，Slack/会议LLM维护 |
| **竞争分析** | 持续追踪竞争对手动态 |

## 在尼克·弗瑞系统中的应用

| 现有系统 | → Wiki | 说明 |
|----------|--------|------|
| RSS每日简报 | `sources/rss/` | 原始资料 |
| 最佳实践收集 | `sources/best_practices/` | 原始素材 |
| ETF数据 | `sources/etf/` | 历史行情 |
| **知识Wiki** | `wiki/` | 🆕 新增 |

## 相关页面

- [[karpathy]] - Andrej Karpathy
- [[rag]] - RAG技术
- [[knowledge-management]] - 知识管理主题

## 来源引用

- [Karpathy LLM Wiki Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

---

*最后更新: 2026-04-08*
*维护者: 尼克·弗瑞*