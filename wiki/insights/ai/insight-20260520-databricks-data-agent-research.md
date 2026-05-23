---
能力框架: #tech-understanding
来源: 网络搜索研究 | 研究时间: 2026-05-20 | 分类: Data Infrastructure / Data Agent
Insight ID: insight-20260520-databricks-data-agent-research
维护者: 尼克·弗瑞 | 更新: 2026-05-20

---

## 📌 执行摘要

**研究主题**：Databricks Data Agent 架构解析

**核心问题**：
- Databricks Data Agent的产品定位是什么？
- 核心架构和完整链路是怎样的？
- 与"外挂+知识库"方案有何本质区别？

**核心结论**：
Databricks Data Agent不是单一产品，而是基于Data Intelligence Platform的Agent能力体系。其本质是把Lakehouse变成Agent的感知和行动底座，让数据治理和Agent能力天然融合，而非在外部接一个知识库。

---

## 一、产品定位

### 1.1 产品组成

Databricks Data Agent是一个**Agent能力体系**，包含以下核心组件：

| 组件 | 定位 | 说明 |
|:---|:---|:---|
| **Mosaic AI Agent Framework** | 核心框架 | 构建、评估、部署生产级AI Agent的原生平台 |
| **Agent Bricks** | 快速构建 | 面向企业知识问答的Agent构建工具 |
| **Unity Catalog** | 治理底座 | 元数据管理、权限控制、AI治理 |
| **Unity AI Gateway** | 访问控制 | LLM访问控制、MCP服务器治理 |
| **Knowledge Assistant** | 知识问答 | 基于Instructed Retrieval的企业知识助手 |

### 1.2 核心定位

> 让企业能够构建基于**自有数据**的、可治理的、可迭代的生产级AI Agent

---

## 二、核心架构

### 2.1 四层架构

```
┌────────────────────────────────────────────────────────────────┐
│                        User / Application                        │
└────────────────────────────────────────────────────────────────┘
                                 ↓
┌────────────────────────────────────────────────────────────────┐
│                      Unity AI Gateway                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │
│  │LLM Access│  │MCP Server│  │ Rate    │  │ Audit Logs   │  │
│  │Control   │  │Governance│  │ Limits   │  │              │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────┘  │
└────────────────────────────────────────────────────────────────┘
                                 ↓
┌────────────────────────────────────────────────────────────────┐
│                    Mosaic AI Agent Framework                     │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐              │
│  │   Agent   │  │   Tools    │  │   Memory   │              │
│  │ (LangGraph│  │ (UC Funcs) │  │            │              │
│  │  /LangChain)│ │            │  │            │              │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘              │
│        └────────────────┼────────────────┘                      │
│                         ↓                                       │
│  ┌─────────────────────────────────────────────┐             │
│  │         MLflow Tracing (可观测性)            │              │
│  └─────────────────────────────────────────────┘              │
└────────────────────────────────────────────────────────────────┘
                                 ↓
┌────────────────────────────────────────────────────────────────┐
│                    Mosaic AI Model Serving                       │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐              │
│  │  LLM       │  │Vector     │  │ GenAI     │              │
│  │  Endpoints │  │Search     │  │ Evaluation │              │
│  └────────────┘  └────────────┘  └────────────┘              │
└────────────────────────────────────────────────────────────────┘
                                 ↓
┌────────────────────────────────────────────────────────────────┐
│                      Unity Catalog                              │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐              │
│  │ Metadata   │  │ Lineage    │  │ Security   │              │
│  │ (Tables,   │  │            │  │ (ACLs,     │              │
│  │  Files)    │  │            │  │  Columns)   │              │
│  └────────────┘  └────────────┘  └────────────┘              │
└────────────────────────────────────────────────────────────────┘
                                 ↓
┌────────────────────────────────────────────────────────────────┐
│                       Delta Lake / Lakehouse                    │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐              │
│  │ Structured │  │ Unstruct- │  │ Streaming  │              │
│  │ Data       │  │ ured Data │  │ Data       │              │
│  └────────────┘  └────────────┘  └────────────┘              │
└────────────────────────────────────────────────────────────────┘
```

### 2.2 数据层

```
Delta Lake / Lakehouse
    ↓
Unity Catalog（元数据管理）
    ↓
Mosaic AI Vector Search（向量检索）
```

### 2.3 治理层

```
Unity Catalog
├── 元数据管理（表、文件、血缘）
├── 权限控制（列级、行级安全）
└── AI Governance
    ├── LLM访问控制
    ├── MCP服务器管理
    └── Agent行为审计
```

---

## 三、完整链路和关键流程

### 3.1 链路对比

| 模式 | 链路 |
|:---|:---|
| **传统RAG** | User Query → Embedding → Vector Search → Retrieved Docs → LLM → Response |
| **Databricks Agent** | User Query → Intent Recognition → Tool Selection → Execution → Response Generation → Evaluation |

### 3.2 Databricks Agent完整链路

```
User Query
    ↓
┌─────────────────────────────────────────────────────────────┐
│ 1. Intent Recognition（意图识别）                            │
│    - 判断是知识问答、代码生成、还是数据查询                  │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. Tool Selection（工具选择）                                │
│    - 从Unity Catalog中选择合适的UC Function/Tool            │
│    - 可选：Vector Search / SQL Query / API Call             │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. Execution（执行）                                        │
│    - 执行选定的工具                                         │
│    - 实时向量搜索或结构化数据查询                            │
│    - MLflow记录完整执行轨迹                                 │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. Response Generation（响应生成）                           │
│    - 结合检索结果和LLM能力                                  │
│    - 可选：多轮对话、迭代优化                               │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. Evaluation（评估）                                       │
│    - AI Judges评估质量                                      │
│    - 幻觉检测、安全检查                                      │
│    - 人类反馈收集                                          │
└─────────────────────────────────────────────────────────────┘
    ↓
Response + Trace → Feedback Loop → Iteration
```

### 3.3 Knowledge Assistant专项流程

```
Query → Instructed Retrieval（而非传统RAG）
    ↓
智能判断：
- 查哪类知识（文档/代码/数据库）
- 用什么chunk策略
- 如何排序和过滤
    ↓
生成答案 + 标注来源
```

---

## 四、核心解决的问题

| 问题 | 解决方案 |
|:---|:---|
| **数据访问安全** | Unity Catalog统一治理，列级/行级权限 |
| **Agent行为失控** | Unity AI Gateway控制LLM访问、MCP服务器权限 |
| **质量不可控** | MLflow Tracing + AI Judges全链路可观测 |
| **幻觉问题** | 事实性引用（Groundness）+ 知识库溯源 |
| **迭代效率低** | 快速评估→反馈→重训的闭环 |
| **多Agent协作** | MCP协议 + Agent间标准通信 |
| **外部知识库割裂** | 与Delta Lake实时同步的向量索引 |

---

## 五、与"外挂+知识库"方案的核心差异

### 5.1 方案对比

| 维度 | 外挂+知识库方案 | Databricks Data Agent |
|:---|:---|:---|
| **数据管理** | 独立知识库，需手动同步 | 与Delta Lake实时同步 |
| **元数据治理** | 割裂（两套体系） | 统一（Unity Catalog） |
| **权限控制** | 知识库ACL + LLM侧控制 | 列级/行级权限透传到Agent |
| **检索方式** | 纯向量检索（Top-K） | Instructed Retrieval（智能判断） |
| **执行能力** | 仅RAG（检索→生成） | Agent可执行工具（查询/计算/操作） |
| **可观测性** | 黑盒，难以定位问题 | MLflow Tracing全链路 |
| **治理深度** | 输入输出审计 | Agent每步操作审计 |
| **数据新鲜度** | 定期同步，有延迟 | Delta Lake实时 |
| **多Agent协作** | 各自为战 | MCP协议统一调度 |

### 5.2 核心差异解读

| 差异点 | 外挂方案 | Databricks方案 |
|:---|:---|:---|
| **数据地位** | 外部依赖 | 第一公民 |
| **治理方式** | 事后审计 | 原生嵌入 |
| **Agent能力** | 有限（只能问） | 完整（能查能改能操作） |
| **数据新鲜度** | 定期同步 | 实时 |

### 5.3 本质区别

**1. "原生" vs "外挂"**
- 外挂方案：知识库是独立系统，Agent需要调用外部API获取知识
- Databricks方案：数据就在Lakehouse中，Agent天然能访问，无需额外的数据管道

**2. "检索" vs "执行"**
- 传统RAG：Query → Retrieve → Generate（只能回答问题）
- Data Agent：Query → Think → Act（能执行操作：查数据、改配置、发消息）

**3. "事后治理" vs "原生治理"**
- 外挂方案：安全审计是事后分析
- Databricks方案：权限在数据层就控制住了，Agent无法访问未授权数据

**4. "静态索引" vs "动态数据"**
- 外挂方案：知识库定期同步，有数据新鲜度问题
- Databricks方案：向量索引与Delta Lake实时同步，数据即最新

---

## 六、六维能力拆解

### 6.1 感知（Perception）

> Agent如何获取和理解信息

| 感知类型 | 数据来源 | 技术实现 |
|:---|:---|:---|
| **结构化数据** | Delta Lake表 | SQL查询 + UC权限过滤 |
| **非结构化文档** | Files (PDF/MD/TXT) | Vector Search语义检索 |
| **代码资产** | Repositories | 代码索引 + 语义搜索 |
| **API/函数** | UC Functions | 函数注册表 + MCP协议 |
| **实时数据** | Streaming表 | Spark Structured Streaming |

### 6.2 推理（Reasoning）

> Agent如何思考和决策

| 推理模式 | 场景 | 技术实现 |
|:---|:---|:---|
| **ReAct** | 单步问答 | Thought → Action → Observation |
| **LangGraph** | 复杂多步任务 | 状态图 + 条件分支 |
| **Chain-of-Thought** | 需要解释的推理 | 显式推理步骤 |
| **Tool Calling** | 函数执行 | LLM生成函数调用 |

### 6.3 行动（Action）

> Agent能做什么

| 行动类型 | 说明 |
|:---|:---|
| **Data Actions** | SQL查询、向量检索、读写Delta Lake、数据转换 |
| **Business Actions** | UC Functions（Python业务逻辑）、MCP工具、API调用 |
| **Content Actions** | 文档生成、代码生成、报告创建 |

### 6.4 反思（Reflection）

> Agent如何自我改进

| 反思机制 | 说明 |
|:---|:---|
| **MLflow Tracing** | 记录每个步骤的输入/输出、时间、错误 |
| **AI Judges** | Groundness（防幻觉）、Relevance、Safety、Completeness评估 |
| **迭代改进** | 评估→发现问题→优化Prompt/工具→重新生成 |

### 6.5 记忆（Memory）

> Agent如何存储和利用历史信息

| 记忆层级 | 说明 |
|:---|:---|
| **Short-term** | 当前会话、对话历史、工作变量 |
| **Session** | 用户偏好、任务模式、最近结果 |
| **Long-term** | 向量索引（知识库）、UC元数据（表结构、血缘）、Artifact Store（生成物） |

### 6.6 协作（Collaboration）

> Agent如何与其他Agent或系统协作

| 协作模式 | 说明 |
|:---|:---|
| **Sequential** | 顺序执行，上游输出作为下游输入 |
| **Parallel** | 并行执行，结果汇总 |
| **Hierarchical** | 主Agent调度子Agent |
| **Collaborative** | 共享上下文，协作推理 |

---

## 七、关键概念

### 7.1 Instructed Retrieval vs Traditional RAG

| Traditional RAG | Instructed Retrieval |
|:---|:---|
| 固定chunk策略 | 智能选择chunk策略 |
| Top-K检索 | 相关性+重要性综合排序 |
| 被动检索 | 根据问题意图主动判断 |

### 7.2 Unity AI Gateway

2026年4月新发布，核心能力：
- 控制哪些Agent可以访问哪些LLM
- 治理MCP服务器的使用权限
- 审计Agent的每一次LLM调用

### 7.3 UC Functions

将Python函数注册为可治理的Agent工具：
- 在UC中注册 → 权限天然受控
- 审计日志 → 每次调用可追溯
- 版本管理 → 可回滚

---

## 八、总结

**Databricks Data Agent的本质**：
不是再造一个知识库，而是把**Lakehouse变成Agent的感知和行动底座**，让数据治理和Agent能力天然融合。

**核心价值主张**：
- 数据即感知（实时感知Delta Lake所有数据）
- 权限即边界（UC元数据天然是权限边界）
- 工具即注册（UC Functions天然是可治理的工具）

**与外挂方案的核心区别**：

| 维度 | 外挂+知识库 | Databricks |
|:---|:---|:---|
| 数据地位 | 外部依赖 | 第一公民 |
| 治理方式 | 事后审计 | 原生嵌入 |
| Agent能力 | 有限（只能问） | 完整（能查能改能操作） |
| 数据新鲜度 | 定期同步 | 实时 |

---

## 参考资料

- Mosaic AI Agent Framework Documentation
- Unity Catalog AI Governance
- Unity AI Gateway (2026.04)
- Databricks Enterprise AI Agent Trends Report 2026
- Agent Bricks Documentation
