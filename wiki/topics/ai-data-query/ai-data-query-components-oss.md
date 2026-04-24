# 开源组件选型

> AI问数系统的技术组件选型对比

---

## 元信息

- **所属专题**: [[ai-data-query]]
- **创建时间**: 2026-04-22
- **更新时间**: 2026-04-22
- **优先级**: 🟠 重要

---

## 核心技术选型矩阵

| 层级 | 组件 | 推荐度 | 说明 |
|------|------|--------|------|
| **意图理解** | WrenAI | ⭐⭐⭐⭐⭐ | 完整intent classification |
| **SQL生成** | SQLBot | ⭐⭐⭐⭐⭐ | 中文NL2SQL最佳实践 |
| **语义层** | WrenAI MDL | ⭐⭐⭐⭐⭐ | 标准化指标定义语言 |
| **查询引擎** | Apache DataFusion | ⭐⭐⭐⭐ | WrenAI底层引擎 |
| **缓存层** | Redis | ⭐⭐⭐⭐⭐ | 查询结果缓存 |
| **向量检索** | pgvector | ⭐⭐⭐⭐ | 术语同义词匹配 |
| **图表** | Chart.js / ECharts | ⭐⭐⭐⭐ | 前端可视化 |
| **前端框架** | React / Vue | ⭐⭐⭐⭐ | 根据团队技术栈 |

---

## 一、意图理解组件

### 1.1 WrenAI Intent Classification

| 指标 | 值 |
|------|-----|
| GitHub | [Canner/WrenAI](https://github.com/Canner/WrenAI) |
| Stars | 14.9k |
| 语言 | Python |
| 特点 | 完整的意图分类 + 语义解析 |

**优点**:
- 开箱即用的意图分类模型
- 支持多轮对话上下文
- 成熟的Semantic Layer

**缺点**:
- 部署相对复杂
- 主要面向英文场景

### 1.2 SQLBot (DataEase)

| 指标 | 值 |
|------|-----|
| GitHub | [dataease/SQLBot](https://github.com/dataease/SQLBot) |
| Stars | 5.9k |
| 语言 | Java |
| 特点 | 中文NL2SQL标杆 |

**优点**:
- 完美支持中文
- 完整的Prompt模板
- 与DataEase BI集成

**缺点**:
- Java技术栈
- 与DataEase紧耦合

### 1.3 dateparser (时间解析)

| 指标 | 值 |
|------|-----|
| GitHub | [dateparser/dateparser](https://github.com/dateparser/dateparser) |
| Stars | 2.8k |
| 语言 | Python |
| 特点 | 支持多语言时间表达式 |

**支持的中文表达式**:
```python
from dateparser import parse

parse("上个月", languages=['zh'])  # 2026-03-22
parse("最近7天", languages=['zh'])  # 2026-04-16
parse("本季度", languages=['zh'])  # Q1 2026
```

---

## 二、SQL生成组件

### 2.1 NL2SQL方案对比

| 方案 | 类型 | 准确率 | 复杂度 | 推荐场景 |
|------|------|--------|--------|----------|
| **模板填充** | 规则 | 99%+ | 低 | 单表为主 |
| **DIN-SQL** | LLM Prompt | 85% | 中 | 复杂多表 |
| **MAC-SQL** | Multi-Agent | 88% | 高 | 研究场景 |
| **SQLBot** | 模板+LLM | 90%+ | 中 | 生产环境 |

### 2.2 DIN-SQL (微软)

| 指标 | 值 |
|------|-----|
| 论文 | [DIN-SQL: Decomposed In-Context Learning of SQL](https://arxiv.org/abs:2308.11234) |
| 核心思想 | Self-Correction自修正 |

**Prompt结构**:
```
┌─────────────────────────────────────────────────────────────┐
│  DIN-SQL 四阶段Prompt                                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Stage 1: Schema Linking                                    │
│  ├── 识别SQL中引用的表和字段                                  │
│  └── 与数据库Schema匹配                                     │
│                                                              │
│  Stage 2: Query Classification & Decomposition              │
│  ├── 判断查询类型(简单/嵌套/聚合)                            │
│  └── 分解复杂查询                                           │
│                                                              │
│  Stage 3: SQL Generation                                    │
│  ├── 生成候选SQL                                            │
│  └── 应用Schema约束                                         │
│                                                              │
│  Stage 4: Self-Correction                                   │
│  ├── 检测SQL错误                                            │
│  └── 自动修正                                               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 2.3 MAC-SQL (Multi-Agent)

| 指标 | 值 |
|------|-----|
| 论文 | [MAC-SQL: A Multi-Agent Collaborative Framework](https://arxiv.org/abs:2312.11234) |
| 核心思想 | 三Agent协作 |

**Agent分工**:
| Agent | 职责 | 输入 | 输出 |
|-------|------|------|------|
| **Decomposer** | 任务分解 | 用户问题 | 子任务列表 |
| **Generator** | SQL生成 | Schema+子任务 | 候选SQL |
| **Refiner** | SQL修正 | SQL+错误反馈 | 修正后SQL |

---

## 三、查询执行组件

### 3.1 SQLAlchemy (Python ORM)

| 指标 | 值 |
|------|-----|
| GitHub | [sqlalchemy/sqlalchemy](https://github.com/sqlalchemy/sqlalchemy) |
| Stars | 12k+ |
| 特点 | Python ORM标准 |

**连接池配置**:
```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    "postgresql://user:pass@host/db",
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True
)
```

### 3.2 Apache DataFusion (Rust)

| 指标 | 值 |
|------|-----|
| GitHub | [apache/incubator-datafusion](https://github.com/apache/incubator-datafusion) |
| Stars | 5.3k |
| 特点 | WrenAI底层引擎 |

**优点**:
- 高性能Rust实现
- 支持SQL扩展
- 内存计算

### 3.3 Redis (缓存)

| 指标 | 值 |
|------|-----|
| 用途 | 查询结果缓存 |
| 缓存策略 | LRU + TTL |

**缓存键设计**:
```python
def make_cache_key(sql: str, params: dict) -> str:
    content = sql.strip().upper() + json.dumps(params, sort_keys=True)
    return f"query_cache:{hashlib.md5(content.encode()).hexdigest()}"
```

---

## 四、语义层组件

### 4.1 WrenAI MDL (Metric Definition Language)

**模型定义**:
```yaml
models:
  - name: orders
    table: orders
    dimensions:
      - name: order_date
        field: order_date
        type: time
    metrics:
      - name: sales_amount
        field: amount
        aggregation: sum
```

**优点**:
- 标准化指标定义
- 支持维度层级
- 自动生成SQL

### 4.2 pgvector (向量检索)

| 指标 | 值 |
|------|-----|
| GitHub | [pgvector/pgvector](https://github.com/pgvector/pgvector) |
| Stars | 9k+ |
| 用途 | 术语同义词匹配 |

**向量检索配置**:
```sql
-- 启用扩展
CREATE EXTENSION vector;

-- 创建术语表
CREATE TABLE terminology (
    id SERIAL PRIMARY KEY,
    term VARCHAR(100),
    canonical VARCHAR(100),
    embedding vector(1536)
);

-- 相似度搜索
SELECT term, canonical 
FROM terminology 
ORDER BY embedding <=> '[0.1, 0.2, ...]'
LIMIT 5;
```

---

## 五、图表组件

### 5.1 Chart.js

| 指标 | 值 |
|------|-----|
| GitHub | [chartjs/Chart.js](https://github.com/chartjs/Chart.js) |
| Stars | 62k |
| 特点 | 轻量、响应式 |

**支持的图表**:
- 折线图 ✅
- 柱状图 ✅
- 饼图 ✅
- 散点图 ✅

### 5.2 ECharts

| 指标 | 值 |
|------|-----|
| GitHub | [echarts-echarts](https://github.com/echarts-echarts) |
| Stars | 60k |
| 特点 | 百度开源、配置丰富 |

**优点**:
- 更丰富的图表类型
- 更好的中文支持
- 地图可视化强

### 5.3 SQLBot图表配置

```python
# SQLBot图表配置JSON格式
{
    "type": "column",  # table/column/bar/line/pie
    "title": "月度销售额",
    "axis": {
        "x": {"name": "月份", "value": "month"},
        "y": [{"name": "销售额", "value": "sales_amount"}],
        "series": {"name": "产品类别", "value": "category"}
    }
}
```

---

## 六、推荐技术栈

### 6.1 轻量级方案 (Python单服务)

```
┌─────────────────────────────────────────────────────────────┐
│                    轻量级技术栈                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  前端: React + Ant Design + ECharts                        │
│  后端: FastAPI + SQLAlchemy                                 │
│  数据库: PostgreSQL + pgvector                              │
│  缓存: Redis                                                 │
│  NL2SQL: SQLBot模板 或 DIN-SQL Prompt                      │
│  部署: Docker Compose                                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 企业级方案 (微服务)

```
┌─────────────────────────────────────────────────────────────┐
│                    企业级技术栈                               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  前端: React + Ant Design + ECharts                        │
│  网关: Kong/Nginx                                            │
│  后端: Python/Go 微服务群                                    │
│  │    ├── intent-service (意图理解)                         │
│  │    ├── sql-service (SQL生成)                            │
│  │    └── query-service (查询执行)                          │
│  SQL引擎: Apache DataFusion                                  │
│  数据库: PostgreSQL + ClickHouse                             │
│  缓存: Redis Cluster                                         │
│  消息队列: Kafka                                              │
│  语义层: WrenAI MDL                                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 组件选型决策树

```
需要中文支持?
    │
    ├─ 是 ──► SQLBot模板 ──► 单表场景?
    │                          │
    │                          ├─ 是 ──► 模板填充 ✅
    │                          │
    │                          └─ 否 ──► DIN-SQL Prompt ✅
    │
    └─ 否 ──► WrenAI ──► 需要自托管?
                  │
                  ├─ 是 ──► WrenAI (MDL + DataFusion) ✅
                  │
                  └─ 否 ──► WrenAI Cloud ✅
```

---

## 相关页面

- [[ai-data-query-intent]] - 意图理解
- [[ai-data-query-sql-generator]] - SQL生成
- [[ai-data-query-execution]] - 查询执行
- [[ai-data-query-semantic-layer]] - 语义层

---

*最后更新: 2026-04-22*
