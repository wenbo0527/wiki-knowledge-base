# WrenAI 架构分析

> 最完整的开源GenBI Agent架构参考

---

## 元信息

- **所属专题**: [[ai-data-query]]
- **创建时间**: 2026-04-22
- **参考价值**: ⭐⭐⭐⭐⭐

---

## 项目概览

| 维度 | 信息 |
|------|------|
| **GitHub** | Canner/WrenAI |
| **Stars** | ⭐ 14.9k |
| **最近更新** | 2026-04-21 (3天前) |
| **语言** | Python + Rust |
| **License** | GPL-3.0 |

---

## 核心定位

> "Ask your database anything in plain English. Wren AI generates accurate SQL, charts, and BI insights — backed by a semantic layer that keeps LLM outputs grounded and trustworthy."

**关键词**: Semantic Layer (MDL) + GenBI

---

## 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    WrenAI 架构图                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐ │
│  │                    wren-ui (Frontend)                 │ │
│  │                    Next.js + Apollo GraphQL            │ │
│  │              语义建模UI + BFF (Backend for Frontend)  │ │
│  └──────────────────────────────────────────────────────┘ │
│                            │                                │
│                            ▼                                │
│  ┌──────────────────────────────────────────────────────┐ │
│  │              wren-ai-service (AI Service)             │ │
│  │                    Python/FastAPI                       │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐    │ │
│  │  │ Intent      │ │ Vector      │ │ LLM         │    │ │
│  │  │ Classification│ Retrieval  │ │ Prompting   │    │ │
│  │  │ (意图分类)  │ │ (Qdrant)   │ │ (SQL生成)  │    │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘    │ │
│  │  ┌─────────────────────────────────────────────┐    │ │
│  │  │           SQL Correction Loop                │    │ │
│  │  │              (最多3次重试)                   │    │ │
│  │  └─────────────────────────────────────────────┘    │ │
│  └──────────────────────────────────────────────────────┘ │
│                            │                                │
│                            ▼                                │
│  ┌──────────────────────────────────────────────────────┐ │
│  │                 wren-engine (Query Engine)            │ │
│  │                   Rust + Apache DataFusion             │ │
│  │  ┌─────────────────────────────────────────────────┐  │ │
│  │  │           MDL (Metric Definition Layer)         │  │ │
│  │  │    业务指标定义 | 维度 | 关联关系 | 权限控制     │  │ │
│  │  └─────────────────────────────────────────────────┘  │ │
│  └──────────────────────────────────────────────────────┘ │
│                            │                                │
│              ┌─────────────┼─────────────┐                 │
│              ▼             ▼             ▼                 │
│         ┌────────┐   ┌────────┐   ┌────────┐              │
│         │BigQuery│   │Snowflake│  │Postgres│  ...        │
│         └────────┘   └────────┘   └────────┘              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 核心组件分析

### 1. Semantic Layer (MDL)

**核心价值**: 解决"LLM生成SQL语义不准确"的问题

```yaml
# MDL示例
models:
  - name: sales
    table: public.sales
    
    metrics:
      - name: revenue
        sql: "SUM(amount)"
        description: 含税销售额
        
      - name: order_count
        sql: "COUNT(*)"
        description: 订单数量
        
    dimensions:
      - name: region
        sql: region
        description: 区域
        
      - name: created_date
        sql: "DATE(created_at)"
        description: 销售日期
```

**为什么重要**:
- "revenue" join哪个表？
- "active user" 用什么过滤条件？
- Semantic Layer 直接告诉LLM答案

### 2. wren-ai-service Pipeline

```
用户问题
    │
    ├── 1️⃣ Intent Classification (意图分类)
    │       是查询问题? 闲聊? 还是其他?
    │
    ├── 2️⃣ Vector Retrieval (向量检索)
    │       从Qdrant检索相似Q&A对
    │
    ├── 3️⃣ LLM Prompting
    │       组装prompt + 历史检索结果
    │
    ├── 4️⃣ SQL Generation
    │       生成SQL + 参数
    │
    └── 5️⃣ SQL Correction Loop
            语法错误 → 重试 (最多3次)
```

### 3. wren-engine (Rust)

| 特性 | 说明 |
|------|------|
| **语言** | Rust (高性能) |
| **核心** | Apache DataFusion |
| **支持数据源** | 15+ 连接器 |
| **查询优化** | 自动优化执行计划 |

---

## 与本场景的匹配度

### 高匹配组件

| WrenAI组件 | 本场景用途 | 匹配度 |
|------------|-----------|--------|
| MDL语义层 | 业务指标定义 | ⭐⭐⭐⭐⭐ |
| SQL生成 | 模板+LLM | ⭐⭐⭐⭐ |
| SQL校验 | 白名单+重试 | ⭐⭐⭐⭐ |
| 结果解释 | GenBI Insights | ⭐⭐⭐ |

### 本场景不需要的

| WrenAI组件 | 原因 |
|------------|------|
| 多数据源连接 | 单表场景不需要 |
| 复杂查询优化 | 数据量有限 |
| 权限细粒度控制 | MVP阶段简化 |

---

## 借鉴价值

### 可以直接用的

1. **MDL定义格式**: YAML定义指标和维度
2. **SQL生成流程**: 意图分类 → RAG → LLM → 纠错
3. **图表生成**: Chart.js集成方式

### 需要简化的

1. **多数据源**: 只需支持1-2种常用数据库
2. **语义层**: 单表场景简化版即可
3. **前端UI**: MVP只需简单对话界面

### 需要自研的

1. **交互式分析**: 下钻/筛选/对比
2. **流式输出**: SSE中文支持
3. **图表交互**: 更丰富的交互能力

---

## 设计建议

### 基于WrenAI的裁剪方案

```
MVP阶段:
    │
    ├── 保留
    │     ├── wren-engine 的查询执行思路
    │     ├── MDL 的指标定义格式 (简化版)
    │     └── SQL生成+纠错流程
    │
    ├── 简化
    │     ├── 只支持1-2种数据库
    │     ├── 去掉多数据源连接池
    │     └── 简化意图分类
    │
    └── 新增
          ├── 交互式分析UI
          ├── 流式结果展示
          └── 业务友好的指标映射
```

---

## 参考链接

- [WrenAI GitHub](https://github.com/Canner/WrenAI)
- [WrenAI Docs](https://docs.getwren.ai)
- [wren-engine](https://github.com/Canner/wren-engine)

---

## 相关页面

- [[ai-data-query-sql-generator]] - SQL生成层
- [[ai-data-query-semantic-layer]] - 语义层设计

---

*最后更新: 2026-04-22*
