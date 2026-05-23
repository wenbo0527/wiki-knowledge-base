# MarketAgentDemo 问数架构设计文档

> 问小数 Agent 核心技术方案 | AI-Query 通用问数引擎

---

## 📑 目录

- [一、背景](#一背景)
- [二、架构设计](#二架构设计)
- [三、解决方案](#三解决方案)
- [四、任务处理流程](#四任务处理流程)
- [五、测试校验方式](#五测试校验方式)
- [六、扩展方案](#六扩展方案)
- [七、文件结构](#七文件结构)
- [八、相关资源](#八相关资源)
- [九、更新日志](#九更新日志)
- [十、指标异动分析算子](#十指标异动分析算子)
- [十一、定量异动归因](#十一定量异动归因)
- [十二、图数据库与业务流程拆解](#十二图数据库与业务流程拆解)
- [十三、扩展能力路线图](#十三扩展能力路线图)
- [十四、配置汇总](#十四配置汇总)
- [十五、Demo vs 生产落地对比](#十五demo-vs-生产落地对比)
- [十六、生产级增强模块实现](#十六生产级增强模块实现)
- [十七、Wiki最佳实践对齐清单](#十七wiki最佳实践对齐清单)
- [十九、生产落地经验分析](#十九生产落地经验分析)
- [二十、RAG知识库设计](#二十rag知识库设计)

---

## 一、背景

### 1.1 业务痛点

在消费金融风控场景中，业务人员频繁需要查询风控数据：
- "华南区逾期率是多少？"
- "按学历看逾期率分布"
- "Vintage账龄分析"

传统方案的问题：
| 痛点 | 说明 |
|------|------|
| **SQL依赖** | 每个查询都需要数据分析师编写SQL，效率低 |
| **模板爆炸** | 每个新指标都需要写新SQL模板，维护成本高 |
| **跨域困难** | 换业务场景时需要重写大量模板 |
| **扩展性差** | 增加新字段/新表时改动范围大 |

### 1.2 解决方案概述

**AI-Query 引擎**：将自然语言转换为 SQL 的通用 NL2SQL 引擎

```
┌──────────────┐    自然语言     ┌──────────────┐
│  业务人员    │ ──────────────→ │   AI-Query   │
└──────────────┘                 │    引擎      │
      ↑                          └──────┬───────┘
      │ SQL结果                            │ SQL
      │                             ┌──────▼───────┐
      │                             │   SQLite/    │
      └──────────────────────────── │  MySQL/Postgres │
                                   └──────────────┘
```

### 1.3 项目信息

| 属性 | 值 |
|------|------|
| **项目名称** | AI-Query (问慧) |
| **版本** | v1.1 |
| **创建时间** | 2026-04-22 |
| **定位** | 通用 NL2SQL Skill |
| **Agent示例** | 问小数 (risk_query) |

---

## 二、架构设计

### 2.1 整体架构

```
┌─────────────────────────────────────────────────────────────────┐
│                         层次架构                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  业务Agent层: 问小数 (RiskQuery)                         │   │
│  │  - SOUL.md: 人设/回复风格                                │   │
│  │  - IDENTITY.md: 职责定义                                 │   │
│  │  - 消费金融风控场景专精                                  │   │
│  │  - 飞书集成: 消息格式适配                                │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            │                                   │
│                            ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Skill层: AI-Query (通用问数)                           │   │
│  │  - 自然语言解析 (QueryParser)                           │   │
│  │  - SQL生成 (SQLBuilder)                                 │   │
│  │  - 查询执行 (QueryEngine)                               │   │
│  │  - 配置驱动 (schema.yaml/aggregation.yaml)              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            │                                   │
│                            ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  数据层: 多数据库支持                                    │   │
│  │  - SQLite (本地测试)                                    │   │
│  │  - MySQL / PostgreSQL / ClickHouse (生产)               │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 核心模块

| 模块 | 文件 | 职责 |
|------|------|------|
| **问题解析器** | `core/parser.py` | 解析自然语言 → 结构化对象 |
| **SQL构建器** | `core/builder.py` | 结构化对象 → SQL语句 |
| **查询引擎** | `core/engine.py` | 调度解析+构建+执行 |
| **飞书处理器** | `scripts/feishu_handler.py` | 飞书消息适配 |

### 2.3 数据流

```
用户问题
   │
   ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  QueryParser │ ──→ │  ParsedQuery │ ──→ │  SQLBuilder  │
│  (解析问题)   │     │  (结构化)     │     │  (生成SQL)   │
└──────────────┘     └──────────────┘     └──────┬───────┘
                                                │
                                                ▼
                           ┌──────────────┐     ┌──────────────┐
                           │   SQLite     │ ←── │  QueryEngine │
                           │   (执行)      │     │  (调度)       │
                           └──────────────┘     └──────┬───────┘
                                                       │
                                                       ▼
                                                  ┌──────────────┐
                                                  │  QueryResult │
                                                  │  (结果对象)  │
                                                  └──────────────┘
```

---

## 三、解决方案

### 3.1 核心设计理念

**"不写SQL模板，也能精准查询"**

| 传统方案 | AI-Query方案 |
|---------|-------------|
| 每个指标写一个SQL模板 | 通用模板 + 动态填充 |
| 换领域需要重写模板 | 换配置即可，无需改代码 |
| 指标固定，难以扩展 | 字段可配置，业务友好 |

### 3.2 配置驱动架构

#### 3.2.1 Schema配置 (`schema.yaml`)

定义表结构和字段映射：

```yaml
tables:
  credit_data:
    table_name: credit_data
    date_field: apply_date
    
    field_mapping:
      serious_dlqin2yrs:
        business: [逾期90天+, 坏账, 严重逾期]
        type: boolean
      
      region:
        business: [地区, 区域, 省份]
        type: category
        values: [华北, 东北, 华东, 华中, 华南, 西南, 西北]
      
      monthly_income:
        business: [月收入, 收入, 月薪]
        type: numeric
        format: currency
```

#### 3.2.2 聚合函数配置 (`aggregation.yaml`)

```yaml
aggregation:
  count:
    keywords: [数量, 个, 次, 共多少]
    sql_func: COUNT
  
  avg:
    keywords: [平均, 均值]
    sql_func: AVG
  
  sum:
    keywords: [总额, 合计]
    sql_func: SUM
```

#### 3.2.3 查询模板配置 (`query_templates.yaml`)

```yaml
basic_templates:
  metric_query:
    name: 指标汇总查询
    template: |
      SELECT {aggregation}({metric_field}) as metric_value
      FROM {table_name}
      {where_clause};

  dimension_query:
    name: 分组指标查询
    template: |
      SELECT {dimension_field} as dimension_value,
             {aggregation}({metric_field}) as metric_value
      FROM {table_name}
      GROUP BY {dimension_field}
      ORDER BY metric_value {sort_order};
```

### 3.3 问题解析逻辑

#### 3.3.1 解析优先级

```
1. 时间表达式  →  parsed.time_condition
2. TOP N       →  parsed.top_n
3. 排序方向    →  parsed.sort_order
4. 筛选条件    →  parsed.filters
5. 指标        →  parsed.metric / metric_field
6. 维度        →  parsed.dimension / dimension_field
7. 多维度      →  parsed.second_dimension
```

#### 3.3.2 模式匹配

| 模式 | 示例 | 解析结果 |
|------|------|----------|
| "按X看Y" | "按地区看逾期率" | dimension=地区, metric=逾期率 |
| "X是多少" | "华南区逾期率是多少" | 筛选=华南, metric=逾期率 |
| "TOP N" | "TOP10的高风险用户" | top_n=10, dimension=风险评分 |
| "最近N天" | "最近7天的交易" | time_condition=N天前 |

### 3.4 SQL生成策略

#### 3.4.1 特殊模板处理

对于**逾期率**和**Vintage**等复杂指标，使用特殊SQL生成逻辑：

```python
# 逾期率特殊处理
def _build_overdue_rate_sql(self, parsed):
    if parsed.dimension:
        sql = f'''
        SELECT {parsed.dimension_field} as dimension_value,
               COUNT(*) as total_users,
               SUM(CASE WHEN serious_dlqin2yrs = 1 THEN 1 ELSE 0 END) as overdue_users,
               ROUND(SUM(CASE WHEN serious_dlqin2yrs = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as overdue_rate
        FROM {parsed.table_name}
        GROUP BY {parsed.dimension_field}
        '''
    else:
        sql = f'''
        SELECT COUNT(*) as total_users,
               SUM(CASE WHEN serious_dlqin2yrs = 1 THEN 1 ELSE 0 END) as overdue_users,
               ROUND(SUM(CASE WHEN serious_dlqin2yrs = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as overdue_rate
        FROM {parsed.table_name}
        '''
    return sql
```

#### 3.4.2 模板填充

通用模板通过占位符填充：

```sql
-- query_templates.yaml 定义
SELECT {aggregation}({metric_field}) as metric_value
FROM {table_name}
{where_clause}
GROUP BY {dimension_field}
ORDER BY metric_value {sort_order}
{limit_clause}
```

---

## 四、任务处理流程

### 4.1 完整流程

```
┌──────────────────────────────────────────────────────────────────┐
│                     问数任务处理流程                              │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  1️⃣ 接收问题                                                     │
│      用户: "华南区逾期率是多少"                                  │
│                                                                   │
│  2️⃣ 解析问题 (QueryParser)                                       │
│      ├─ 识别指标: 逾期率 (serious_dlqin2yrs)                     │
│      ├─ 识别维度: 无                                              │
│      ├─ 识别筛选: region=华南                                    │
│      ├─ 识别聚合: SUM                                            │
│      └─ 输出: ParsedQuery 对象                                    │
│                                                                   │
│  3️⃣ 构建SQL (SQLBuilder)                                         │
│      ├─ 选择模板: overdue_rate_query                             │
│      ├─ 填充变量: region='华南'                                  │
│      └─ 输出: SELECT ... FROM credit_data WHERE region='华南'    │
│                                                                   │
│  4️⃣ SQL预检                                                      │
│      ├─ 检查字段是否存在                                          │
│      ├─ 检查表权限                                                │
│      └─ 输出: warnings (如有问题)                                │
│                                                                   │
│  5️⃣ 执行查询 (QueryEngine)                                        │
│      ├─ 连接数据库                                                │
│      ├─ 执行SQL                                                   │
│      ├─ 获取结果                                                  │
│      └─ 输出: QueryResult                                        │
│                                                                   │
│  6️⃣ 格式化响应                                                    │
│      ├─ 飞书格式适配                                              │
│      ├─ 生成消息卡片                                              │
│      └─ 输出: FeishuQueryHandler.handle_query()                  │
│                                                                   │
│  7️⃣ 返回结果                                                     │
│      📊 逾期率查询结果                                            │
│      - 总用户: 14,286                                            │
│      - 逾期用户: 2,285                                            │
│      - 逾期率: 16.00%                                            │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

### 4.2 代码调用链

```python
# 1. 入口
from scripts.feishu_handler import handle_query

result = handle_query("华南区逾期率是多少")

# 2. FeishuQueryHandler.handle_query()
result = handler.handle_query("华南区逾期率是多少")
# ├─ engine.parser.parse() → ParsedQuery
# ├─ engine.query() → QueryResult
# └─ _format_overdue_response() → formatted message

# 3. QueryEngine.query()
result = self.query(user_query)
# ├─ self.parser.parse() → ParsedQuery
# ├─ self.builder.build_with_validation() → SQL
# └─ self._execute_sql() → data, columns
```

### 4.3 特殊处理：逾期率模板

```python
# parser.py - 识别特殊模板
def _parse_metric_and_dimension(self, query, parsed):
    if '逾期率' in query:
        parsed.use_overdue_template = True  # 特殊标记
        parsed.metric = '逾期率'
        parsed.metric_field = 'serious_dlqin2yrs'
        parsed.table_name = 'credit_data'
```

```python
# builder.py - 构建特殊SQL
def _build_overdue_rate_sql(self, parsed):
    if parsed.use_overdue_template:
        return self._build_overdue_rate_sql(parsed)
    else:
        return self._fill_template(sql_template, parsed)
```

---

## 五、测试校验方式

### 5.1 测试运行器

使用 `test_runner.py` 进行自动化测试：

```bash
# 列出所有测试用例
python3 ~/.openclaw/skills/risk-query-tester/test_runner.py --list

# 运行全部测试
python3 ~/.openclaw/skills/risk-query-tester/test_runner.py --all

# 运行指定测试
python3 ~/.openclaw/skills/risk-query-tester/test_runner.py --id=1
```

### 5.2 测试用例列表

| ID | 测试项 | 预期答案 |
|:--:|:-------|:---------|
| 1 | 整体逾期率 | 16.23% |
| 2 | 总用户数 | 100,000 |
| 3 | 地区逾期率TOP3 | 华北16.46% |
| 4 | 学历逾期率 | 本科16.68% |
| 5 | 婚姻状态逾期率 | 未婚16.79% |
| 6 | 就业状态逾期率 | 自由职业17.56% |
| 7 | 年龄段逾期率 | 30-40岁17.37% |
| 8 | 收入区间逾期率 | 3000以下18.54% |
| 9 | 负债等级逾期率 | 低负债17.06% |
| 10 | 学历+地区交叉 | 本科华北18.36% |
| 11 | 低收入年轻人分析 | 19.69% |
| 12 | 地区+负债交叉 | 西南低18.42% |
| 13 | 贷款状态分布 | 正常75.06% |
| 14 | 贷款金额统计 | 均值52,564 |
| 15 | 逾期贷款特征 | 逾期45.2天 |
| 16 | 交易类型分布 | 消费TOP1 |
| 17 | 商户类别分析 | 娱乐TOP1 |
| 18 | 高风险交易用户 | 5条记录 |
| 19 | 多条件筛选 | 东北23.26% |
| 20 | 风控日报 | 综合指标 |

### 5.3 测试场景覆盖

| 场景类型 | 覆盖测试 |
|----------|----------|
| 简单指标查询 | #1, #2, #14 |
| 分组查询 | #3, #4, #5, #6, #7, #8, #9 |
| 多维度交叉 | #10, #11, #12 |
| 特殊指标 | #13, #15, #16, #17, #18 |
| 多条件筛选 | #19 |
| 综合报表 | #20 |

### 5.4 结果验证

```python
# 测试验证示例
def test_overdue_rate():
    result = query("华南区逾期率")
    assert result.success == True
    assert result.data[0]['overdue_rate'] == '16.00'
    assert result.row_count > 0
```

---

## 六、扩展方案

### 6.1 异动归因

#### 6.1.1 问题定义

当核心指标发生异常波动时，自动分析原因：

```
昨日华南区逾期率从15%上升到18%，原因是什么？
```

#### 6.1.2 实现方案

```
┌─────────────────────────────────────────────────────────────────┐
│                       异动归因流程                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1️⃣ 指标拆解                                                    │
│      逾期率 = 逾期人数 / 总人数                                  │
│              = f(region, education, age, income, ...)           │
│                                                                  │
│  2️⃣ 维度下探                                                    │
│      ├─ 按地区分解: 华南18% vs 其他地区平均15%                   │
│      ├─ 按学历分解: 大专19% vs 其他学历平均14%                   │
│      └─ 按年龄段分解: 30-40岁22% vs 其他年龄段12%                │
│                                                                  │
│  3️⃣ 贡献度计算                                                  │
│      ┌────────────────────────────────────────────────────┐     │
│      │ 贡献度 = (维度逾期率 - 基准逾期率) × 维度用户占比     │     │
│      └────────────────────────────────────────────────────┘     │
│                                                                  │
│  4️⃣ 归因输出                                                    │
│      💡 归因结论:                                                 │
│         - 主因: 华南区大专学历用户占比上升 (+3%)                 │
│         - 次因: 30-40岁用户逾期恶化 (+2%)                        │
│         - 综合影响: +3.2% 逾期率上升                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### 6.1.3 SQL模板

```sql
-- 维度贡献度分析
WITH dimension_breakdown AS (
    SELECT 
        {dimension_field},
        COUNT(*) as total_users,
        SUM(CASE WHEN serious_dlqin2yrs = 1 THEN 1 ELSE 0 END) as overdue_users,
        ROUND(SUM(CASE WHEN serious_dlqin2yrs = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as overdue_rate
    FROM credit_data
    WHERE {time_condition}
    GROUP BY {dimension_field}
),
overall_rate AS (
    SELECT 
        ROUND(SUM(CASE WHEN serious_dlqin2yrs = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as base_rate
    FROM credit_data
    WHERE {time_condition}
)
SELECT 
    d.{dimension_field},
    d.total_users,
    d.overdue_users,
    d.overdue_rate,
    o.base_rate as baseline_rate,
    ROUND((d.overdue_rate - o.base_rate) * d.total_users * 1.0 / 
          (SELECT SUM(total_users) FROM dimension_breakdown), 2) as contribution
FROM dimension_breakdown d, overall_rate o
ORDER BY contribution DESC
```

#### 6.1.4 配置扩展

```yaml
# schema.yaml 新增
advanced_analytics:
  anomaly_detection:
    enabled: true
    sensitivity: 0.05  # 5%以上触发异动告警
  
  attribution:
    dimensions:
      - region
      - education_level
      - age_group
      - income_group
      - employment_status
    max_contributing_factors: 3
```

---

### 6.2 数据分析

#### 6.2.1 分析能力矩阵

| 分析类型 | 能力 | 实现阶段 |
|----------|------|----------|
| **描述性分析** | 分布、均值、极值 | ✅ 已实现 |
| **对比分析** | 维度对比、时间对比 | ✅ 已实现 |
| **趋势分析** | 时间序列、Vintage | ✅ 已实现 |
| **关联分析** | 相关性、特征重要性 | 📝 待实现 |
| **预测分析** | 逾期预测、流失预警 | 📝 待实现 |

#### 6.2.2 描述性分析扩展

```python
# 新增分析维度
descriptive_analytics:
  - type: distribution
    metrics: [age, income, debt_ratio]
    buckets: [10, 20, 30, 40, 50]
  
  - type: percentile
    metrics: [monthly_income, credit_limit, risk_score]
    percentiles: [P10, P25, P50, P75, P90, P99]
  
  - type: correlation
    metrics: [age, income, debt_ratio, revolving_utilization]
    target: serious_dlqin2yrs
```

#### 6.2.3 SQL模板

```sql
-- 描述性统计
SELECT 
    AVG({metric_field}) as mean,
    MIN({metric_field}) as min,
    MAX({metric_field}) as max,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY {metric_field}) as median,
    STDDEV({metric_field}) as std_dev
FROM {table_name}
WHERE {condition}
```

#### 6.2.4 关联分析

```python
# 相关性分析 SQL
correlation_sql = """
SELECT 
    CORR(age, serious_dlqin2yrs) as age_correlation,
    CORR(monthly_income, serious_dlqin2yrs) as income_correlation,
    CORR(debt_ratio, serious_dlqin2yrs) as debt_correlation,
    CORR(revolving_utilization, serious_dlqin2yrs) as utilization_correlation
FROM credit_data
"""
```

---

### 6.3 多表关联

#### 6.3.1 关联场景

当前单表查询已覆盖主要场景，未来扩展多表关联：

| 场景 | 表关系 | 示例 |
|------|--------|------|
| 用户+贷款 | credit_data → loan_records | "有贷款的用户逾期率" |
| 用户+交易 | credit_data → transaction_records | "交易金额超过5万用户的逾期率" |
| 贷款+交易 | loan_records → transaction_records | "有消费贷记录的用户还款情况" |

#### 6.3.2 关联关系定义

```yaml
# schema.yaml 中已定义
relationships:
  - source: credit_data
    target: loan_records
    type: one_to_many
    on: credit_data.user_id = loan_records.user_id
  
  - source: credit_data
    target: transaction_records
    type: one_to_many
    on: credit_data.user_id = transaction_records.user_id
```

#### 6.3.3 多表查询扩展

```python
# parser.py 新增多表识别逻辑
def _parse_multi_table(self, query, parsed):
    """识别是否需要多表关联"""
    tables_required = []
    
    # 检查是否涉及贷款相关查询
    if any(kw in query for kw in ['贷款', '借款', '本金', '月供', '期限']):
        tables_required.append('loan_records')
    
    # 检查是否涉及交易相关查询
    if any(kw in query for kw in ['交易', '消费', '金额', '商户', '渠道']):
        tables_required.append('transaction_records')
    
    if len(tables_required) > 1:
        parsed.multi_table = True
        parsed.related_tables = tables_required
```

#### 6.3.4 SQL生成

```sql
-- 多表关联 SQL 模板
multi_table_query:
  name: 多表关联查询
  description: 关联用户表和贷款/交易表
  template: |
    SELECT 
        c.user_id,
        c.region,
        c.education_level,
        COUNT(l.id) as loan_count,
        SUM(l.loan_amount) as total_loan,
        SUM(CASE WHEN l.loan_status = '逾期' THEN 1 ELSE 0 END) as overdue_loans
    FROM credit_data c
    LEFT JOIN loan_records l ON c.user_id = l.user_id
    {where_clause}
    GROUP BY c.user_id, c.region, c.education_level
    HAVING COUNT(l.id) > 0
    ORDER BY total_loan DESC
    {limit_clause}
```

#### 6.3.5 实现步骤

```
┌─────────────────────────────────────────────────────────────────┐
│                    多表关联扩展计划                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Phase 1: 单表增强 (当前)                                        │
│  ├─ 逾期率查询                                                    │
│  ├─ 分组查询                                                     │
│  └─ Vintage分析                                                  │
│                                                                  │
│  Phase 2: 两表关联 (规划中)                                       │
│  ├─ user_id 关联                                                 │
│  ├─ 贷款信息JOIN                                                 │
│  └─ 交易信息JOIN                                                 │
│                                                                  │
│  Phase 3: 复杂分析 (规划中)                                       │
│  ├─ 窗口函数应用                                                 │
│  ├─ CTEs递归查询                                                 │
│  └─ 实时计算指标                                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 七、文件结构

```
ai-query/
├── SKILL.md                      # Skill定义
├── README.md                     # 项目介绍
├── ROADMAP.md                    # 发展规划
├── INFRASTRUCTURE.md            # 基础设施文档
├── config/
│   ├── schema.yaml              # 表结构配置 ⭐
│   ├── aggregation.yaml        # 聚合函数配置 ⭐
│   ├── time_expressions.yaml    # 时间表达式配置
│   └── query_templates.yaml     # 查询模板配置 ⭐
├── core/
│   ├── __init__.py
│   ├── engine.py               # 查询引擎主类 ⭐
│   ├── parser.py              # 问题解析器 ⭐
│   ├── builder.py             # SQL构建器 ⭐
│   ├── validator.py           # SQL校验器
│   └── formatter.py           # 结果格式化
└── scripts/
    ├── feishu_handler.py       # 飞书集成 ⭐
    ├── schema_discovery.py     # Schema自动发现
    └── interactive.py          # 交互生成

risk_query/ (Agent工作区)
├── scripts/
│   ├── __init__.py
│   ├── ai_query_handler.py     # AI-Query集成 ⭐
│   └── feishu_handler.py       # 飞书处理器 ⭐
├── data/
│   └── risk_enhanced.db       # SQLite数据库 (10万条)
├── docs/
│   └── MarketAgentDemo_问数架构.md  # 本文档
└── memory/
```

---

## 八、相关资源

| 资源 | 位置 |
|------|------|
| **AI-Query项目** | `~/Documents/project/ai-query/` |
| **问小数Agent** | `~/.openclaw/workspace-agents/risk_query/` |
| **知识库专题** | `~/Documents/project/Wiki/wiki/topics/ai-data-query/` |
| **参考项目** | WrenAI, DataLine, SQLBot |

---

## 九、更新日志

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0 | 2026-04-22 | 初始版本，创建项目结构 |
| v1.1 | 2026-04-28 | 优化解析器和SQL构建器 |
| v2.0 | 2026-05-19 | 新增本文档，补充扩展方案 |

---

*本文档由问小数 Agent 生成*
*维护者: 派蒙 & 问小数团队*
*最后更新: 2026-05-19*

---

## 十、指标异动分析算子

### 10.1 算子体系设计

#### 10.1.1 四则运算算子

指标异动分析的核心是将复合指标分解为原子指标的加减乘除：

```yaml
# config/operators.yaml
arithmetic_operators:
  # 加法算子 - 用于指标合并
  add:
    symbol: "+"
    description: 指标相加
    example: "逾期人数 = 30天逾期 + 60天逾期 + 90天逾期"
  
  # 减法算子 - 用于环比/同比
  subtract:
    symbol: "-"
    description: 指标相减
    example: "环比变化 = 本期逾期率 - 上期逾期率"
  
  # 乘法算子 - 用于比率计算
  multiply:
    symbol: "*"
    description: 指标相乘
    example: "风险敞口 = 贷款余额 * 违约概率"
  
  # 除法算子 - 用于比率/占比
  divide:
    symbol: "/"
    description: 指标相除
    example: "逾期率 = 逾期人数 / 总人数"
```

#### 10.1.2 原子指标定义

```yaml
# 消费金融风控原子指标
atomic_metrics:
  # 底层字段
  - name: total_users
    field: user_id
    aggregation: COUNT
    description: 总用户数
  
  - name: overdue_users_30
    field: num_30_59_late
    aggregation: SUM
    description: 30-59天逾期人数
  
  - name: overdue_users_60
    field: num_60_89_late
    aggregation: SUM
    description: 60-89天逾期人数
  
  - name: overdue_users_90
    field: num_90_late
    aggregation: SUM
    description: 90天以上逾期人数
  
  - name: overdue_flag
    field: serious_dlqin2yrs
    aggregation: SUM
    description: 严重逾期标记
  
  - name: loan_balance
    field: outstanding_balance
    aggregation: SUM
    description: 贷款余额
  
  - name: credit_limit
    field: credit_limit
    aggregation: SUM
    description: 信用额度
```

#### 10.1.3 复合指标公式

```yaml
# 复合指标定义 - 使用算子组合原子指标
composite_metrics:
  # 逾期率系
  overdue_rate:
    formula: "overdue_flag / total_users * 100"
    unit: "%"
    description: 整体逾期率
  
  mild_overdue_rate:
    formula: "(overdue_users_30 + overdue_users_60) / total_users * 100"
    unit: "%"
    description: 轻度逾期率(30-89天)
  
  severe_overdue_rate:
    formula: "overdue_users_90 / total_users * 100"
    unit: "%"
    description: 重度逾期率(90天+)
  
  # 资产质量系
  delinquency_rate:
    formula: "overdue_users_30 / total_users * 100"
    unit: "%"
    description: 拖欠率(30天+)
  
  provision_ratio:
    formula: "overdue_flag * avg_loss_given_default / loan_balance * 100"
    unit: "%"
    description: 拨备覆盖率
  
  # 授信风险系
  utilization_rate:
    formula: "loan_balance / credit_limit * 100"
    unit: "%"
    description: 授信利用率
  
  exposure_at_default:
    formula: "overdue_flag * avg_exposure_per_default_user"
    unit: "元"
    description: 违约敞口(EAD)
  
  expected_loss:
    formula: "loan_balance * overdue_rate / 100 * loss_given_default_rate / 100"
    unit: "元"
    description: 预期损失(EL)
```

### 10.2 算子解析引擎

#### 10.2.1 公式解析器

```python
"""
指标公式解析器
将用户定义的公式转换为可执行的SQL
"""

import re
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class Operator:
    """算子定义"""
    symbol: str
    precedence: int
    func: str  # SQL函数


class FormulaParser:
    """公式解析器"""
    
    OPERATORS = {
        '+': Operator('+', 1, ' + '),
        '-': Operator('-', 1, ' - '),
        '*': Operator('*', 2, ' * '),
        '/': Operator('/', 2, ' / '),
        '(': Operator('(', 0, '('),
        ')': Operator(')', 0, ')'),
    }
    
    def __init__(self, metric_registry: Dict):
        self.metric_registry = metric_registry  # 指标注册表
    
    def parse(self, formula: str) -> str:
        """
        解析公式字符串为SQL表达式
        
        Args:
            formula: "overdue_rate - last_period_overdue_rate"
        
        Returns:
            SQL表达式: "(SUM(CASE WHEN serious_dlqin2yrs=1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) - (上期SQL)"
        """
        # 1. 分词
        tokens = self._tokenize(formula)
        
        # 2. 转换为SQL
        sql_parts = []
        for token in tokens:
            if token in self.OPERATORS:
                sql_parts.append(self.OPERATORS[token].func)
            elif token in self.metric_registry:
                sql_parts.append(self._resolve_metric(token))
            elif token.isdigit():
                sql_parts.append(token)
            else:
                sql_parts.append(token)
        
        return ''.join(sql_parts)
    
    def _tokenize(self, formula: str) -> List[str]:
        """分词"""
        # 处理运算符和括号
        tokens = []
        current = ''
        for char in formula:
            if char in '+-*/()':
                if current:
                    tokens.append(current)
                    current = ''
                tokens.append(char)
            elif char == ' ':
                if current:
                    tokens.append(current)
                    current = ''
            else:
                current += char
        if current:
            tokens.append(current)
        return tokens
    
    def _resolve_metric(self, metric_name: str) -> str:
        """解析指标为SQL"""
        metric = self.metric_registry.get(metric_name)
        if not metric:
            return metric_name
        
        if 'formula' in metric:
            # 递归解析复合指标
            return f"({self.parse(metric['formula'])})"
        else:
            # 原子指标转换为SQL
            return self._build_atomic_sql(metric)
    
    def _build_atomic_sql(self, metric: Dict) -> str:
        """构建原子指标SQL"""
        field = metric.get('field', '')
        agg = metric.get('aggregation', 'SUM')
        
        if field == 'serious_dlqin2yrs':
            return f"SUM(CASE WHEN serious_dlqin2yrs=1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*)"
        elif metric.get('aggregation') == 'COUNT':
            return f"COUNT({field})"
        elif metric.get('aggregation') == 'AVG':
            return f"AVG({field})"
        else:
            return f"{agg}({field})"
```

### 10.3 异动分析配置

```yaml
# config/anomaly_detection.yaml
anomaly_detection:
  # 异动检测规则
  rules:
    - name: overdue_rate_spike
      metric: overdue_rate
      condition: "change_pct > 20%"  # 变化超过20%触发
      severity: high
    
    - name: utilization_anomaly
      metric: utilization_rate
      condition: "value > 80% OR change_pct > 15%"
      severity: medium
  
  # 归因维度
  attribution_dimensions:
    - dimension: region
      label: 地区
    
    - dimension: education_level
      label: 学历
    
    - dimension: age_group
      label: 年龄段
    
    - dimension: employment_status
      label: 就业状态
    
    - dimension: income_group
      label: 收入区间
  
  # 归因计算方法
  attribution_methods:
    - name: contribution_analysis
      description: 维度贡献度分析
      formula: "(dim_rate - base_rate) * dim_user_pct"
    
    - name: factor_decomposition
      description: 因子分解法
      formula: "Σ(因子变化 × 其他因子均值)"
    
    - name: ratio_decomposition
      description: 比率分解法
      formula: "A/B = Σ(Ai/ΣAi) / Σ(Bi/ΣBi)"
```

---

## 十一、定量异动归因

### 11.1 归因计算框架

#### 11.1.1 问题定义

当指标发生异动时，自动分解到各维度的贡献度：

```
目标: 解释"昨日华南区逾期率从15%上升到18%"的原因
```

#### 11.1.2 归因公式

```
┌─────────────────────────────────────────────────────────────────┐
│                     异动归因基本公式                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Δ指标 = Σ(各维度贡献度)                                        │
│                                                                  │
│   维度贡献度 = (维度指标值_本期 - 维度指标值_上期) × 维度权重    │
│                                                                  │
│   维度权重 = 维度用户数 / 总用户数                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### 11.1.3 SQL实现

```sql
-- 异动归因 SQL 模板
WITH period_comparison AS (
    -- 本期数据
    SELECT 
        {dimension_field},
        COUNT(*) as current_users,
        SUM(CASE WHEN serious_dlqin2yrs=1 THEN 1 ELSE 0 END) as current_overdue,
        ROUND(SUM(CASE WHEN serious_dlqin2yrs=1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as current_rate
    FROM credit_data
    WHERE {current_period_condition}
    GROUP BY {dimension_field}
),
last_period AS (
    -- 上期数据
    SELECT 
        {dimension_field},
        COUNT(*) as last_users,
        SUM(CASE WHEN serious_dlqin2yrs=1 THEN 1 ELSE 0 END) as last_overdue,
        ROUND(SUM(CASE WHEN serious_dlqin2yrs=1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as last_rate
    FROM credit_data
    WHERE {last_period_condition}
    GROUP BY {dimension_field}
),
overall_current AS (
    SELECT 
        COUNT(*) as total_users,
        SUM(CASE WHEN serious_dlqin2yrs=1 THEN 1 ELSE 0 END) as total_overdue,
        ROUND(SUM(CASE WHEN serious_dlqin2yrs=1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as overall_rate
    FROM credit_data
    WHERE {current_period_condition}
),
overall_last AS (
    SELECT 
        ROUND(SUM(CASE WHEN serious_dlqin2yrs=1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as overall_rate
    FROM credit_data
    WHERE {last_period_condition}
)
SELECT 
    c.{dimension_field} as dimension_value,
    c.current_users,
    c.last_users,
    c.current_rate,
    c.last_rate,
    (c.current_rate - c.last_rate) as rate_change,
    -- 贡献度 = 逾期率变化 × 用户占比
    ROUND((c.current_rate - c.last_rate) * c.current_users * 1.0 / NULLIF(o.total_users, 0), 4) as contribution
FROM period_comparison c
JOIN last_period l ON c.{dimension_field} = l.{dimension_field}
CROSS JOIN overall_current o
ORDER BY ABS((c.current_rate - c.last_rate) * c.current_users) DESC
```

### 11.2 因子分解法

#### 11.2.1 乘积因子分解

对于复合指标 `E = A × B × C`，分解变化：

```python
"""
乘积因子分解法
用于分解如: 预期损失 = 贷款余额 × 逾期率 × 违约损失率
"""

class FactorDecomposer:
    """因子分解器"""
    
    def decompose_multiplicative(
        self,
        current: Dict[str, float],
        last: Dict[str, float]
    ) -> List[Dict]:
        """
        乘积因子分解
        
        Args:
            current: {"loan_balance": 1000000, "overdue_rate": 0.16, "lgd": 0.5}
            last: {"loan_balance": 900000, "overdue_rate": 0.15, "lgd": 0.5}
        
        Returns:
            [{"factor": "loan_balance", "contribution": 16000, "pct": 0.4}, ...]
        """
        current_E = current['loan_balance'] * current['overdue_rate'] * current['lgd']
        last_E = last['loan_balance'] * last['overdue_rate'] * last['lgd']
        total_change = current_E - last_E
        
        results = []
        factors = ['loan_balance', 'overdue_rate', 'lgd']
        
        for i, factor in enumerate(factors):
            # 计算该因子变化导致的贡献
            other_current = [current[f] for j, f in enumerate(factors) if j != i]
            other_last = [last[f] for j, f in enumerate(factors) if j != i]
            
            factor_change = current[factor] - last[factor]
            avg_others = sum(other_current) / len(other_current)  # 使用均值消除歧义
            
            contribution = factor_change * product(avg_others)
            results.append({
                'factor': factor,
                'last_value': last[factor],
                'current_value': current[factor],
                'change': factor_change,
                'contribution': contribution,
                'pct': contribution / total_change if total_change != 0 else 0
            })
        
        return results
    
    def decompose_ratio(
        self,
        current: Dict[str, float],
        last: Dict[str, float]
    ) -> List[Dict]:
        """
        比率因子分解
        
        用于分解如: 逾期率 = 逾期人数 / 总人数
        
        变化 = (本期逾期/本期总数) - (上期逾期/上期总数)
             = (逾期变化/本期总数) + (逾期_上期 × 数量变化/本期_上期)
        """
        results = []
        
        # 分子变化贡献
        numerator_change = current['numerator'] - last['numerator']
        numerator_contribution = numerator_change / current['denominator']
        
        # 分母变化贡献
        denominator_change = current['denominator'] - last['denominator']
        denominator_contribution = -last['numerator'] * denominator_change / (current['denominator'] * last['denominator'])
        
        results.append({
            'factor': 'numerator',
            'contribution': numerator_contribution,
            'description': '逾期人数变化贡献'
        })
        results.append({
            'factor': 'denominator',
            'contribution': denominator_contribution,
            'description': '总人数变化贡献'
        })
        
        return results
```

### 11.3 归因可视化

```python
"""
异动归因报告生成
"""

ATTRIBUTION_REPORT_PROMPT = """
### 异动归因报告模板

### 1. 异动概述
- 指标: {metric_name}
- 本期值: {current_value}
- 上期值: {last_value}
- 变化量: {change_value}
- 变化率: {change_pct}%

### 2. 归因分解

| 维度 | 贡献度 | 贡献占比 |
|------|--------|----------|
{attribution_table}

### 3. 主要发现

{top_findings}

### 4. 建议措施

{recommendations}

---

### 输出格式示例

📊 **逾期率异动归因报告**

🎯 **指标**: 华南区逾期率
- 本期: 18.5% (较上期 +3.5%)
- 上期: 15.0%

📋 **归因分解**:
| 维度 | 贡献度 | 占比 |
|------|--------|------|
| 大专学历 | +2.1% | 60% |
| 30-40岁 | +1.0% | 29% |
| 其他 | +0.4% | 11% |

💡 **主要发现**:
- 华南区大专学历用户占比上升是主因(+2.1%)
- 30-40岁年龄段逾期恶化次之(+1.0%)

⚠️ **建议**:
1. 重点关注华南区大专学历客群
2. 调整该客群授信策略
"""


def generate_attribution_report(
    metric_name: str,
    current_value: float,
    last_value: float,
    attribution: List[Dict]
) -> str:
    """生成归因报告"""
    
    change_value = current_value - last_value
    change_pct = (change_value / last_value * 100) if last_value != 0 else 0
    
    # 构建归因表格
    attribution_table = '\n'.join([
        f"| {a['dimension']} | {a['contribution']:+.2f}% | {a['pct']:.1f}% |"
        for a in attribution[:5]  # TOP5
    ])
    
    # 主要发现
    top_findings = '\n'.join([
        f"- {a['dimension']}维度贡献{a['contribution']:+.2f}%"
        for a in attribution[:3]
    ])
    
    # 建议
    recommendations = '\n'.join([
        f"{i+1}. 重点关注{a['dimension']}维度异常"
        for i, a in enumerate(attribution[:2])
    ])
    
    return ATTRIBUTION_REPORT_PROMPT.format(
        metric_name=metric_name,
        current_value=current_value,
        last_value=last_value,
        change_value=change_value,
        change_pct=change_pct,
        attribution_table=attribution_table,
        top_findings=top_findings,
        recommendations=recommendations
    )
```

---

## 十二、图数据库与业务流程拆解

### 12.1 图数据库架构

#### 12.1.1 Neo4j存储结构

```
┌─────────────────────────────────────────────────────────────────┐
│                    Neo4j 图数据库架构                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  节点类型:                                                       │
│  ┌─────────────┐                                                 │
│  │ :Epic       │  业务Epic(顶层需求)                            │
│  └─────────────┘                                                 │
│         │                                                         │
│         ▼                                                         │
│  ┌─────────────┐                                                 │
│  │ :Feature    │  功能模块                                       │
│  └─────────────┘                                                 │
│         │                                                         │
│         ▼                                                         │
│  ┌─────────────┐                                                 │
│  │ :Story      │  用户故事                                       │
│  └─────────────┘                                                 │
│                                                                  │
│  关系类型:                                                       │
│  - [:CONTAINS]  包含关系                                         │
│  - [:BELONGS_TO] 归属关系                                         │
│  - [:DEPENDS_ON] 依赖关系                                         │
│  - [:RELATED_TO] 关联关系                                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### 12.1.2 指标图谱节点设计

```yaml
# Neo4j 指标图谱 Schema
nodes:
  # 指标节点
  Metric:
    properties:
      - name: uri
        type: string
        description: 唯一标识 "metric:overdue_rate"
      - name: label
        type: string
        description: 显示名称 "逾期率"
      - name: formula
        type: string
        description: 计算公式 "overdue_flag / total_users * 100"
      - name: unit
        type: string
        description: 单位 "%"
      - name: aggregation
        type: string
        description: 聚合方式 "SUM/AVG/COUNT"
      - name: is_atomic
        type: boolean
        description: 是否原子指标
  
  # 维度节点
  Dimension:
    properties:
      - name: uri
        type: string
      - name: label
        type: string
      - name: field
        type: string
        description: 对应数据库字段
      - name: type
        type: string
        description: "category/numeric/time"
  
  # 业务实体节点
  BusinessEntity:
    properties:
      - name: uri
        type: string
      - name: label
        type: string
      - name: entity_type
        type: string
        description: "table/field/process"

edges:
  # 指标依赖关系
  - type: [:DEPENDS_ON]
    from: CompositeMetric
    to: AtomicMetric
    description: 指标依赖
  
  # 维度归属关系
  - type: [:BELONGS_TO]
    from: Metric
    to: Dimension
    description: 指标归属维度
  
  # 业务流程关系
  - type: [:FOLLOWS]
    from: ProcessStep
    to: ProcessStep
    description: 流程顺序
```

### 12.2 业务流程拆解

#### 12.2.1 消费金融业务流程图

```
┌─────────────────────────────────────────────────────────────────┐
│                 消费金融业务流程图                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐ │
│  │ 用户注册  │────→│ 授信评估  │────→│ 额度审批  │────→│ 贷款发放  │ │
│  └──────────┘     └──────────┘     └──────────┘     └──────────┘ │
│       │                │                │                │        │
│       │                │                │                │        │
│       ▼                ▼                ▼                ▼        │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐ │
│  │ 注册量   │     │ 评估量   │     │ 审批量   │     │ 放款量   │ │
│  │ 指标     │     │ 指标     │     │ 指标     │     │ 指标     │ │
│  └──────────┘     └──────────┘     └──────────┘     └──────────┘ │
│                                                                  │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐                  │
│  │ 贷后管理  │────→│ 还款监控  │────→│ 催收管理  │                  │
│  └──────────┘     └──────────┘     └──────────┘                  │
│       │                │                │                         │
│       ▼                ▼                ▼                         │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐                  │
│  │ 逾期率   │     │ 不良率   │     │ 核销率   │                  │
│  │ 指标     │     │ 指标     │     │ 指标     │                  │
│  └──────────┘     └──────────┘     └──────────┘                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### 12.2.2 Neo4j查询示例

```python
"""
Neo4j 图数据库操作
用于业务流程拆解和指标关系查询
"""

from neo4j import GraphDatabase


class IndicatorGraph:
    """指标图谱管理器"""
    
    def __init__(self, uri: str = "bolt://localhost:7687", user: str = "neo4j", password: str = "password123"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def get_metric_dependencies(self, metric_uri: str) -> Dict:
        """
        获取指标依赖链
        
        Args:
            metric_uri: "metric:expected_loss"
        
        Returns:
            {
                "metric": "expected_loss",
                "depends_on": ["overdue_rate", "loan_balance", "lgd"],
                "formula": "loan_balance * overdue_rate * lgd"
            }
        """
        with self.driver.session() as tx:
            result = tx.run("""
                MATCH (m:Metric {uri: $metric_uri})
                OPTIONAL MATCH (m)-[:DEPENDS_ON]->(dep:Metric)
                RETURN 
                    m.uri as metric,
                    m.formula as formula,
                    COLLECT(dep.uri) as dependencies
            """, metric_uri=metric_uri)
            
            record = result.single()
            return {
                'metric': record['metric'],
                'formula': record['formula'],
                'depends_on': [d for d in record['dependencies'] if d]
            }
    
    def get_process_breakdown(self, process_uri: str) -> List[Dict]:
        """
        获取业务流程拆解
        
        Args:
            process_uri: "process:loan_approval"
        
        Returns:
            [{"step": 1, "name": "申请", "metrics": ["申请量"]}, ...]
        """
        with self.driver.session() as tx:
            result = tx.run("""
                MATCH (p:Process {uri: $process_uri})
                MATCH (p)-[:HAS_STEP]->(s:Step)
                OPTIONAL MATCH (s)-[:PRODUCES]->(m:Metric)
                RETURN 
                    s.step_order as step,
                    s.name as step_name,
                    COLLECT(m.uri) as metrics
                ORDER BY step
            """, process_uri=process_uri)
            
            return [dict(record) for record in result]
    
    def calculate_weighted_aggregation(
        self,
        composite_metric_uri: str,
        dimension_filter: str = None
    ) -> Dict:
        """
        基于图关系计算加权聚合指标
        
        Returns:
            计算结果和归因权重
        """
        with self.driver.session() as tx:
            # 1. 获取指标公式
            metric_info = self.get_metric_dependencies(composite_metric_uri)
            
            # 2. 获取维度权重
            weights = tx.run("""
                MATCH (m:Metric {uri: $metric_uri})-[:BELONGS_TO]->(d:Dimension)
                RETURN d.uri as dimension, d.weight as weight
            """, metric_uri=composite_metric_uri)
            
            # 3. 计算加权结果
            # ... SQL计算逻辑
            return result
    
    def find_root_causes(
        self,
        anomaly_metric_uri: str,
        time_range: str
    ) -> List[Dict]:
        """
        异常溯源 - 找到导致指标异常的根本原因
        
        使用图遍历算法找到影响路径
        """
        with self.driver.session() as tx:
            result = tx.run("""
                MATCH path = (cause:Metric)-[:AFFECTS*1..3]->(target:Metric {uri: $anomaly_uri})
                WHERE cause.is_atomic = true
                RETURN 
                    cause.uri as root_cause,
                    cause.label as description,
                    LENGTH(path) as depth,
                    REDUCE(weight = 1.0, r IN relationships(path) | weight * r.impact_weight) AS impact_score
                ORDER BY impact_score DESC
                LIMIT 10
            """, anomaly_uri=anomaly_metric_uri)
            
            return [dict(record) for record in result]
```

### 12.3 指标聚合公式构建

#### 12.3.1 聚合公式定义

```yaml
# 指标聚合公式配置
aggregation_formulas:
  # 顶层复合指标
  expected_loss:
    label: 预期损失
    formula: "loan_exposure * overdue_rate * loss_given_default"
    unit: 元
    
    dependencies:
      - name: loan_exposure
        label: 贷款敞口
        source: credit_data.outstanding_balance
        aggregation: SUM
      
      - name: overdue_rate
        label: 逾期率
        source: derived
        formula: "overdue_flag / total_users"
      
      - name: loss_given_default
        label: 违约损失率
        source: constant  # 通常为固定值如0.5
  
  # 资产质量综合指标
  asset_quality_index:
    label: 资产质量综合指数
    formula: "(overdue_rate * 0.4 + migration_rate * 0.3 + provision_ratio * 0.3)"
    weights:
      overdue_rate: 0.4
      migration_rate: 0.3
      provision_ratio: 0.3
  
  # 客户价值指标
  customer_lifetime_value:
    label: 客户终身价值
    formula: "avg_transaction * transaction_frequency * customer_margin * retention_rate ^ avg_lifetime"
```

#### 12.3.2 动态公式解析器

```python
"""
动态公式解析器
根据图数据库中的指标关系自动构建SQL
"""

class DynamicFormulaBuilder:
    """动态公式构建器"""
    
    def __init__(self, graph: IndicatorGraph, db_connection):
        self.graph = graph
        self.db = db_connection
    
    def build_sql(self, metric_uri: str, time_condition: str = None) -> str:
        """
        根据指标定义构建SQL
        
        Args:
            metric_uri: 指标URI
            time_condition: 时间条件
        
        Returns:
            可执行的SQL语句
        """
        # 1. 获取指标定义
        metric_info = self.graph.get_metric_dependencies(metric_uri)
        
        # 2. 解析公式
        formula = metric_info['formula']
        dependencies = metric_info['depends_on']
        
        # 3. 构建SQL
        sql_parts = ['SELECT']
        
        # 处理每个依赖指标
        sql_expressions = []
        for dep in dependencies:
            dep_sql = self._resolve_dependency(dep, time_condition)
            sql_expressions.append(dep_sql)
        
        # 4. 应用公式运算符
        final_sql = self._apply_formula(formula, sql_expressions)
        
        return final_sql
    
    def _resolve_dependency(self, dep_uri: str, time_condition: str) -> str:
        """解析依赖指标为SQL子查询"""
        
        # 如果是原子指标，直接构建
        if self._is_atomic(dep_uri):
            field = self._get_field_from_metric(dep_uri)
            agg = self._get_aggregation(dep_uri)
            return f"{agg}({field})"
        
        # 如果是复合指标，递归构建子查询
        else:
            sub_metric = self.graph.get_metric_dependencies(dep_uri)
            return f"({self.build_sql(dep_uri, time_condition)})"
    
    def _apply_formula(self, formula: str, expressions: List[str]) -> str:
        """将公式中的占位符替换为实际SQL表达式"""
        # 简化实现：假设 formula 格式为 "A * B + C"
        # 实际需要解析表达式树
        
        result = formula
        for i, expr in enumerate(expressions):
            result = result.replace(chr(65 + i), expr)  # A, B, C...
        
        return f"SELECT {result} as metric_value FROM credit_data"
```

### 12.4 权重计算方法

#### 12.4.1 权重计算配置

```yaml
# config/weight_calculation.yaml
weight_calculation:
  methods:
    # 方法1: 历史数据回归
    regression:
      name: 回归分析权重
      description: 基于历史数据回归计算各因子权重
      config:
        min_samples: 100
        significance_level: 0.05
    
    # 方法2: 熵权法
    entropy_weight:
      name: 熵权法
      description: 基于数据离散程度计算权重
      config:
        normalize: true
        use_log: true
    
    # 方法3: 层次分析法(AHP)
    ahp:
      name: 层次分析法
      description: 专家判断矩阵计算权重
      config:
        consistency_ratio_threshold: 0.1
    
    # 方法4: 业务经验权重
    business_weight:
      name: 业务经验权重
      description: 基于业务人员经验设定
      config:
        override_allowed: true
```

#### 12.4.2 权重计算实现

```python
"""
权重计算器
支持多种权重计算方法
"""

import numpy as np
from scipy import stats


class WeightCalculator:
    """权重计算器"""
    
    def calculate_entropy_weight(self, data_matrix: np.ndarray) -> np.ndarray:
        """
        熵权法计算权重
        
        Args:
            data_matrix: shape (n_samples, n_indicators)
        
        Returns:
            weights: shape (n_indicators,)
        """
        # 1. 标准化
        normalized = self._normalize(data_matrix)
        
        # 2. 计算信息熵
        n_samples, n_indicators = normalized.shape
        p = normalized / normalized.sum(axis=0)  # 比重矩阵
        
        # 避免log(0)
        p = np.where(p > 0, p, 1e-10)
        
        entropy = -np.sum(p * np.log(p), axis=0) / np.log(n_samples)
        
        # 3. 计算权重
        diversity = 1 - entropy
        weights = diversity / diversity.sum()
        
        return weights
    
    def calculate_regression_weight(
        self,
        X: np.ndarray,
        y: np.ndarray
    ) -> Tuple[np.ndarray, float]:
        """
        回归分析计算权重
        
        Args:
            X: shape (n_samples, n_indicators) - 因子数据
            y: shape (n_samples,) - 目标变量
        
        Returns:
            weights: 标准化回归系数
            r_squared: 拟合优度
        """
        # 标准化
        X_std = (X - X.mean(axis=0)) / X.std(axis=0)
        y_std = (y - y.mean()) / y.std()
        
        # 多元线性回归
        coefficients = np.linalg.lstsq(X_std, y_std, rcond=None)[0]
        
        # 标准化系数作为权重
        weights = coefficients / coefficients.sum()
        
        # 计算R²
        y_pred = X_std @ coefficients
        ss_res = np.sum((y_std - y_pred) ** 2)
        ss_tot = np.sum((y_std - y_std.mean()) ** 2)
        r_squared = 1 - ss_res / ss_tot
        
        return weights, r_squared
    
    def calculate_ahp_weight(self, pairwise_matrix: np.ndarray) -> np.ndarray:
        """
        层次分析法(AHP)计算权重
        
        Args:
            pairwise_matrix: 判断矩阵 (n x n)
            pairwise_matrix[i][j] > 1 表示i比j重要
        
        Returns:
            weights: 归一化权重
        """
        n = pairwise_matrix.shape[0]
        
        # 1. 归一化判断矩阵
        col_sum = pairwise_matrix.sum(axis=0)
        normalized = pairwise_matrix / col_sum
        
        # 2. 计算权重向量
        weights = normalized.mean(axis=1)
        weights = weights / weights.sum()
        
        # 3. 计算一致性指标CI
        weighted_sum = (pairwise_matrix * weights).sum(axis=1)
        lambda_max = (weighted_sum / weights).mean()
        ci = (lambda_max - n) / (n - 1)
        
        # 4. 计算一致性比率CR
        ri = {1: 0, 2: 0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45}
        cr = ci / ri.get(n, 1.32)
        
        if cr > 0.1:
            print(f"Warning: CR={cr:.3f} > 0.1, matrix may be inconsistent")
        
        return weights
```

### 12.5 图数据库查询优化

#### 12.5.1 Cypher查询优化

```python
"""
图数据库查询优化
"""

class GraphQueryOptimizer:
    """图查询优化器"""
    
    # 优化规则
    OPTIMIZATION_RULES = [
        {
            'name': '避免全图遍历',
            'pattern': 'MATCH (n) RETURN n',
            'suggestion': '使用标签或属性过滤'
        },
        {
            'name': '使用索引',
            'pattern': 'WHERE n.uri =',
            'suggestion': '确保uri            'suggestion': '确保uri属性已建立索引'
        },
        {
            'name': '限制遍历深度',
            'pattern': '[:AFFECTS*1..3]',
            'suggestion': '使用可变深度避免无限遍历'
        }
    ]
    
    def optimize_query(self, cypher: str) -> str:
        """优化Cypher查询"""
        optimized = cypher
        
        for rule in self.OPTIMIZATION_RULES:
            if rule['pattern'] in cypher:
                # 可以添加分析或自动优化建议
                pass
        
        return optimized
    
    def explain_query_plan(self, cypher: str) -> str:
        """解释查询计划"""
        with self.driver.session() as tx:
            result = tx.run(f"EXPLAIN {cypher}")
            # 返回执行计划
            return str(result.peek())
```

---

## 十三、扩展能力路线图

### 13.1 能力矩阵

| 能力 | 当前状态 | 规划 |
|------|----------|------|
| 简单问数 | ✅ 已实现 | 持续优化 |
| 分组查询 | ✅ 已实现 | 持续优化 |
| 多维度查询 | ✅ 已实现 | 扩展维度 |
| 异动检测 | 📝 设计中 | 补充阈值配置 |
| 异动归因 | 📝 设计中 | 补充SQL模板 |
| 指标公式 | 📝 设计中 | 补充解析器 |
| 图数据库 | 📝 设计中 | Neo4j集成 |
| 多表关联 | 📝 规划中 | JOIN扩展 |
| 预测分析 | 📝 规划中 | ML集成 |

### 13.2 Phase计划

```
┌─────────────────────────────────────────────────────────────────┐
│                    能力扩展Phase计划                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Phase 1: 基础增强 (当前)                                       │
│  ├─ 完善逾期率/Vintage模板                                      │
│  ├─ 增加更多维度支持                                            │
│  └─ 优化解析准确率                                              │
│                                                                  │
│  Phase 2: 异动分析 (下一版本)                                   │
│  ├─ 异动检测算子                                                │
│  ├─ 定量归因计算                                                │
│  ├─ 贡献度可视化                                                │
│  └─ 配置化阈值管理                                              │
│                                                                  │
│  Phase 3: 指标体系 (规划中)                                     │
│  ├─ 指标公式解析                                                │
│  ├─ 算子配置                                                    │
│  ├─ 聚合指标计算                                                │
│  └─ 权重计算方法                                                │
│                                                                  │
│  Phase 4: 图谱集成 (规划中)                                     │
│  ├─ Neo4j图数据库                                              │
│  ├─ 业务流程拆解                                                │
│  ├─ 指标依赖关系                                                │
│  └─ 根因追溯                                                    │
│                                                                  │
│  Phase 5: 高级分析 (规划中)                                     │
│  ├─ 多表关联查询                                                │
│  ├─ 预测模型集成                                                │
│  ├─ 异常模式识别                                                │
│  └─ 自动化报告                                                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 十四、配置汇总

### 14.1 配置文件清单

| 配置文件 | 用途 | 位置 |
|----------|------|------|
| `schema.yaml` | 表结构与字段映射 | `config/` |
| `aggregation.yaml` | 聚合函数配置 | `config/` |
| `query_templates.yaml` | SQL模板 | `config/` |
| `time_expressions.yaml` | 时间表达式 | `config/` |
| `operators.yaml` | 算子定义 | `config/` ⭐新增 |
| `anomaly_detection.yaml` | 异动检测配置 | `config/` ⭐新增 |
| `weight_calculation.yaml` | 权重计算配置 | `config/` ⭐新增 |

### 14.2 核心配置示例

```yaml
# config/operators.yaml (新增)
arithmetic_operators:
  add:
    symbol: "+"
    sql_func: " + "
  subtract:
    symbol: "-"
    sql_func: " - "
  multiply:
    symbol: "*"
    sql_func: " * "
  divide:
    symbol: "/"
    sql_func: " / "

# config/anomaly_detection.yaml (新增)
anomaly_detection:
  rules:
    - name: overdue_rate_spike
      metric: overdue_rate
      condition: "change_pct > 20%"
      severity: high
  attribution_methods:
    - name: contribution_analysis
      formula: "(dim_rate - base_rate) * dim_user_pct"

# config/weight_calculation.yaml (新增)
weight_calculation:
  methods:
    - name: entropy_weight
      description: 基于数据离散程度计算权重
    - name: regression
      description: 基于历史数据回归计算权重
    - name: ahp
      description: 层次分析法专家判断权重
```

---

## 十五、Demo vs 生产落地对比

> 本章节对照 Wiki 最佳实践，明确 Demo 阶段与生产环境的差异

### 15.1 核心差距对照

| 层级 | Demo 阶段 (当前) | 生产环境 (目标) | Wiki最佳实践来源 |
|:---|:---|:---|:---|
| **意图理解** | 模式匹配 (parser.py) | WrenAI Intent Classification | [[ai-data-query-intent]] |
| **SQL生成** | 模板 + 特殊模板 | DIN-SQL 自修正 + MAC-SQL 多Agent | [[ai-data-query-sql-generator]] |
| **校验机制** | SQL预检 (简单) | L1语法 + L2 Schema + L3执行 三层校验 | [[ai-data-query-sql-generator]] |
| **Pre-Processing** | 时间表达式 | Schema Linking + Terminology Mapping | [[ai-data-query-sql-generator]] |
| **Post-Processing** | 格式化响应 | SQL格式化 + 危险检测 + 性能优化 | [[ai-data-query-sql-generator]] |
| **多Agent协作** | 无 | MAC-SQL 三Agent (Decomposer/Generator/Refiner) | [[ai-data-query-components-oss]] |
| **测试体系** | 20个用例 | L1-L5分级 + 边界用例 + 回归测试 | [[ai-data-query-sql-generator]] |
| **指标体系** | 原子 + 复合指标 | 语义层 (MDL) + 血缘追踪 + 版本管理 | [[insight-20260408-metrics-platform]] |

### 15.2 Demo 阶段特点

#### 当前实现

```
┌─────────────────────────────────────────────────────────────┐
│                    Demo 架构 (当前)                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  用户问题                                                    │
│      │                                                       │
│      ▼                                                       │
│  QueryParser (模式匹配)  ←── 简单if-else                     │
│      │                                                       │
│      ▼                                                       │
│  SQLBuilder (模板填充)  ←── 预定义模板                       │
│      │                                                       │
│      ▼                                                       │
│  SQL预检 (简单)         ←── 只检查字段存在                   │
│      │                                                       │
│      ▼                                                       │
│  QueryEngine (执行)     ←── 直接执行                       │
│      │                                                       │
│      ▼                                                       │
│  格式化响应                                                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### Demo 阶段优势

| 优势 | 说明 |
|:---|:---|
| **快速验证** | 2周内可完成 POC |
| **可控性强** | 规则明确，结果可预测 |
| **调试简单** | 问题定位容易 |
| **资源需求低** | 无需 LLM API 调用 |

#### Demo 阶段局限

| 局限 | 说明 | 生产环境要求 |
|:---|:---|:---|
| **覆盖度有限** | 新指标需要写新模板 | 自动泛化 |
| **无法处理复杂查询** | 多表JOIN、子查询困难 | 复杂查询支持 |
| **缺少自修正** | 错误SQL直接失败 | DIN-SQL自修正 |
| **无智能校验** | 简单预检无法发现所有问题 | 三层校验 |
| **无法模糊匹配** | 必须是精确的业务术语 | 同义词扩展 |

---

### 15.3 生产环境要求

#### Wiki 推荐的生产架构

```
┌─────────────────────────────────────────────────────────────────┐
│                    生产架构 (Wiki最佳实践)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  用户问题                                                        │
│      │                                                           │
│      ▼                                                           │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Pre-Processing                                          │    │
│  │ ├── Schema Linking (识别表名/字段名)                    │    │
│  │ ├── Terminology Mapping (业务术语→字段)                │    │
│  │ └── Time Processing (自然语言时间→日期范围)             │    │
│  └─────────────────────────────────────────────────────────┘    │
│      │                                                           │
│      ▼                                                           │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Intent Classification (意图理解)                         │    │
│  │ ├── metric_query (指标查询)                             │    │
│  │ ├── dimension_query (分组查询)                          │    │
│  │ ├── comparison_query (对比查询)                         │    │
│  │ ├── anomaly_query (异动查询)                            │    │
│  │ └── attribution_query (归因查询)                        │    │
│  └─────────────────────────────────────────────────────────┘    │
│      │                                                           │
│      ▼                                                           │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ SQL Generation (DIN-SQL / MAC-SQL)                      │    │
│  │ ├── Decomposer Agent (任务分解)                         │    │
│  │ ├── Generator Agent (SQL生成)                          │    │
│  │ └── Refiner Agent (SQL修正)                             │    │
│  └─────────────────────────────────────────────────────────┘    │
│      │                                                           │
│      ▼                                                           │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Three-Layer Validation (三层校验)                        │    │
│  │ ├── L1: SQLSyntaxValidator (语法校验)                    │    │
│  │ ├── L2: SQLSchemaValidator (Schema校验)                  │    │
│  │ └── L3: SQLExecutionValidator (执行校验)                  │    │
│  └─────────────────────────────────────────────────────────┘    │
│      │                                                           │
│      ▼                                                           │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Post-Processing                                          │    │
│  │ ├── SQL格式化 (美化SQL输出)                              │    │
│  │ ├── 危险检测 (DROP/DELETE/UPDATE拦截)                   │    │
│  │ └── 性能优化 (LIMIT自动添加)                             │    │
│  └─────────────────────────────────────────────────────────┘    │
│      │                                                           │
│      ▼                                                           │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Self-Correction Loop (DIN-SQL自修正)                    │    │
│  │ ├── 错误反馈 → LLM修正 → 重新校验                       │    │
│  │ └── 最大重试3次                                          │    │
│  └─────────────────────────────────────────────────────────┘    │
│      │                                                           │
│      ▼                                                           │
│  QueryEngine (执行)                                              │
│      │                                                           │
│      ▼                                                           │
│  结果解释与可视化                                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### 生产环境核心能力

| 能力 | 说明 | 行业参考 |
|:---|:---|:---|
| **意图分类** | 5种+意图自动识别 | WrenAI Intent Classification |
| **三层校验** | 语法/Schema/执行三重保障 | C3 一致性投票 |
| **DIN-SQL自修正** | 错误自动修正 | DIN-SQL (微软) |
| **MAC-SQL多Agent** | 复杂查询多Agent协作 | MAC-SQL |
| **Schema Linking** | 自动识别Query中的表/字段 | CHESS |
| **Terminology Mapping** | 业务术语→数据库字段 | pgvector向量检索 |
| **L1-L5分级测试** | 边界用例覆盖 | NL2SQL Handbook |

---

### 15.4 演进路线图

```
┌───────────────────────────────────────────────────────────────────────┐
│                        AI-Query 演进路线                              │
├───────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  Phase 1: Demo (当前)                                                  │
│  ├── 状态: ✅ 已完成                                                   │
│  ├── 能力: 模板填充 + 特殊模板 + 简单预检                              │
│  ├── 周期: 2周                                                         │
│  └── 适用: POC验证 + 单表简单查询                                      │
│                                                                        │
│  Phase 2: 生产基础版 (1个月)                                           │
│  ├── 目标: 补充三层校验 + DIN-SQL自修正                               │
│  ├── 新增:                                                            │
│  │   ├── SQLValidator 三层校验                                        │
│  │   ├── DINSQLCorrector 自修正                                       │
│  │   ├── Schema Linking                                               │
│  │   └── Terminology Mapping (pgvector)                               │
│  └── 交付: 准确率 90%+                                                │
│                                                                        │
│  Phase 3: 生产增强版 (2个月)                                           │
│  ├── 目标: 意图分类 + MAC-SQL多Agent                                   │
│  ├── 新增:                                                            │
│  │   ├── IntentClassifier 意图分类                                    │
│  │   ├── MACSQLFramework 多Agent协作                                  │
│  │   ├── AnomalyDetector 异动检测                                      │
│  │   └── AttributionEngine 归因分析                                    │
│  └── 交付: 准确率 95%+                                                │
│                                                                        │
│  Phase 4: 企业级 (3个月)                                               │
│  ├── 目标: 语义层 + 指标中台 + 权限体系                                │
│  ├── 新增:                                                            │
│  │   ├── SemanticLayer 语义层 (MDL)                                    │
│  │   ├── MetricsGovernance 指标治理                                    │
│  │   ├── DataLineage 血缘追踪                                          │
│  │   └── Row-Level Security 行级权限                                   │
│  └── 交付: 企业级 NL2SQL 平台                                          │
│                                                                        │
└───────────────────────────────────────────────────────────────────────┘
```

---

## 十六、生产级增强模块实现

> 以下模块参考 Wiki 最佳实践设计，待在 Phase 2/3 中实现

### 16.1 三层校验机制 (Phase 2)

```python
# core/validator.py - 生产级三层校验
import sqlparse
from dataclasses import dataclass
from typing import Optional, List, Tuple

@dataclass
class ValidationResult:
    """校验结果"""
    valid: bool
    error: str
    layer: str  # L1/L2/L3

class SQLSyntaxValidator:
    """L1: SQL语法校验"""
    
    def validate(self, sql: str) -> ValidationResult:
        """校验SQL语法"""
        try:
            parsed = sqlparse.parse(sql)
            if not parsed:
                return ValidationResult(False, "无法解析SQL", "L1")
            
            stmt = parsed[0]
            if not stmt.get_type():
                return ValidationResult(False, "未识别的SQL类型", "L1")
            
            sql_upper = sql.upper()
            if 'SELECT' not in sql_upper:
                return ValidationResult(False, "缺少SELECT关键字", "L1")
            
            # 危险SQL检测
            dangerous_keywords = ['DROP', 'DELETE', 'TRUNCATE', 'ALTER', 'INSERT', 'UPDATE']
            for keyword in dangerous_keywords:
                if keyword in sql_upper:
                    return ValidationResult(False, f"禁止使用: {keyword}", "L1")
            
            return ValidationResult(True, "OK", "L1")
        except Exception as e:
            return ValidationResult(False, f"语法错误: {str(e)}", "L1")


class SQLSchemaValidator:
    """L2: Schema校验 - 确保表名/字段名存在"""
    
    def __init__(self, schema: dict):
        self.schema = schema  # {table_name: [field_names]}
    
    def validate(self, sql: str) -> ValidationResult:
        """校验SQL中的表名和字段名"""
        # 提取表名
        table_names = self._extract_table_names(sql)
        
        # 检查表名
        for table in table_names:
            if table not in self.schema:
                return ValidationResult(False, f"表名不存在: {table}", "L2")
        
        return ValidationResult(True, "OK", "L2")
    
    def _extract_table_names(self, sql: str) -> List[str]:
        """提取SQL中的表名"""
        import re
        tables = []
        
        # FROM子句
        from_match = re.search(r'FROM\s+(\w+)', sql, re.IGNORECASE)
        if from_match:
            tables.append(from_match.group(1))
        
        # JOIN子句
        join_matches = re.findall(r'JOIN\s+(\w+)', sql, re.IGNORECASE)
        tables.extend(join_matches)
        
        return list(set(tables))


class SQLExecutionValidator:
    """L3: 执行校验 - 确保可以执行且返回结果"""
    
    def __init__(self, db_connection):
        self.db = db_connection
    
    def validate(self, sql: str, max_rows: int = 1000) -> ValidationResult:
        """校验SQL执行"""
        try:
            # 添加LIMIT检查
            if 'LIMIT' not in sql.upper():
                sql = f"{sql} LIMIT {max_rows}"
            
            # 执行SQL
            cursor = self.db.cursor()
            cursor.execute(sql)
            
            # 检查结果
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            
            if not rows:
                return ValidationResult(False, "查询结果为空", "L3")
            
            return ValidationResult(True, "OK", "L3")
        except Exception as e:
            return ValidationResult(False, f"执行错误: {str(e)}", "L3")


class SQLValidator:
    """三层校验总入口"""
    
    def __init__(self, schema: dict, db_connection):
        self.L1 = SQLSyntaxValidator()
        self.L2 = SQLSchemaValidator(schema)
        self.L3 = SQLExecutionValidator(db_connection)
    
    def validate(self, sql: str) -> Tuple[bool, str]:
        """执行三层校验"""
        # L1: 语法校验
        result = self.L1.validate(sql)
        if not result.valid:
            return False, f"[L1] {result.error}"
        
        # L2: Schema校验
        result = self.L2.validate(sql)
        if not result.valid:
            return False, f"[L2] {result.error}"
        
        # L3: 执行校验
        result = self.L3.validate(sql)
        if not result.valid:
            return False, f"[L3] {result.error}"
        
        return True, "OK"
```

### 16.2 DIN-SQL 自修正机制 (Phase 2)

```python
# core/din_sql_corrector.py - DIN-SQL风格自修正
from typing import Tuple

class DINSQLCorrector:
    """DIN-SQL 风格的自修正机制"""
    
    MAX_RETRIES = 3
    
    def __init__(self, llm, validator):
        self.llm = llm  # LLM接口
        self.validator = validator
    
    def generate_with_correction(self, question: str, schema: str, prompt_template: str) -> Tuple[str, bool]:
        """生成SQL并通过自修正提高准确率"""
        
        # Step 1: 生成初始SQL
        prompt = prompt_template.format(question=question, schema=schema)
        sql = self.llm.generate(prompt)
        
        # Step 2: 自修正循环
        for attempt in range(self.MAX_RETRIES):
            valid, error = self.validator.validate(sql)
            
            if valid:
                return sql, True
            
            # 错误反馈修正
            if attempt < self.MAX_RETRIES - 1:
                sql = self._correct(sql, error)
            else:
                return sql, False
        
        return sql, False
    
    def _correct(self, sql: str, error: str) -> str:
        """基于错误反馈修正SQL"""
        correction_prompt = f"""
你生成了以下SQL查询:
{sql}

该查询失败，错误信息:
{error}

请修正SQL中的错误，只返回修正后的SQL，不要其他解释。
"""
        return self.llm.generate(correction_prompt)


# DIN-SQL Self-Correction Prompt
DIN_SQL_CORRECTION_PROMPT = """
You generated the following SQL query:
{sql}

This query failed with error:
{error}

Please fix the SQL query. Rules:
1. Only generate SELECT queries
2. Use the exact table and column names from the schema
3. Return only the corrected SQL, no explanation

Corrected SQL:
"""
```

### 16.3 意图分类层 (Phase 3)

```python
# core/intent_classifier.py - 意图分类
from enum import Enum
from typing import List

class QueryIntent(Enum):
    """查询意图枚举"""
    METRIC_QUERY = "metric_query"           # 指标查询
    DIMENSION_QUERY = "dimension_query"     # 分组查询
    COMPARISON_QUERY = "comparison_query"  # 对比查询
    ANOMALY_QUERY = "anomaly_query"         # 异动查询
    ATTRIBUTION_QUERY = "attribution_query" # 归因查询
    TREND_QUERY = "trend_query"             # 趋势查询
    RANKING_QUERY = "ranking_query"         # 排名查询
    UNKNOWN = "unknown"                      # 未知


class IntentClassifier:
    """意图分类器"""
    
    # 意图关键词映射
    INTENT_PATTERNS = {
        QueryIntent.METRIC_QUERY: ["是多少", "有多少", "统计", "总数"],
        QueryIntent.DIMENSION_QUERY: ["按", "分组", "分布", "拆分"],
        QueryIntent.COMPARISON_QUERY: ["对比", "比较", "差异", "比"],
        QueryIntent.ANOMALY_QUERY: ["异常", "异动", "波动", "突增", "突降"],
        QueryIntent.ATTRIBUTION_QUERY: ["原因", "归因", "为什么", "由于"],
        QueryIntent.TREND_QUERY: ["趋势", "走势", "变化", "增长", "下降"],
        QueryIntent.RANKING_QUERY: ["TOP", "排名", "前", "最高", "最低"],
    }
    
    def classify(self, query: str) -> QueryIntent:
        """分类用户查询的意图"""
        query_lower = query.lower()
        
        # 遍历匹配
        for intent, patterns in self.INTENT_PATTERNS.items():
            for pattern in patterns:
                if pattern in query_lower:
                    return intent
        
        # 默认指标查询
        return QueryIntent.METRIC_QUERY
    
    def extract_params(self, query: str, intent: QueryIntent) -> dict:
        """根据意图提取参数"""
        params = {
            "intent": intent,
            "filters": [],
            "dimensions": [],
            "metrics": [],
            "time_condition": None,
        }
        
        # 根据不同意图使用不同的解析逻辑
        if intent == QueryIntent.ANOMALY_QUERY:
            # 异动查询：提取异常指标和时间范围
            params["is_anomaly"] = True
        elif intent == QueryIntent.ATTRIBUTION_QUERY:
            # 归因查询：提取待归因指标
            params["is_attribution"] = True
        
        return params
```

### 16.4 MAC-SQL 多Agent框架 (Phase 3)

```python
# core/mac_sql_framework.py - MAC-SQL多Agent协作
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class SubTask
@dataclass
class SubTask:
    """子任务"""
    task_id: str
    description: str
    status: str  # pending/in_progress/completed
    result: Optional[str] = None


class DecomposerAgent:
    """MAC-SQL Decomposer Agent - 任务分解"""
    
    def decompose(self, question: str, schema: str) -> List[SubTask]:
        """将复杂问题分解为子任务"""
        
        # 判断是否需要分解
        if self._is_simple_query(question):
            return [SubTask("main", question, "pending")]
        
        # 复杂查询分解
        tasks = []
        
        # 子任务1: 识别主指标
        tasks.append(SubTask("identify_metric", "识别查询的核心指标", "pending"))
        
        # 子任务2: 识别维度
        tasks.append(SubTask("identify_dimension", "识别分组维度", "pending"))
        
        # 子任务3: 确定筛选条件
        tasks.append(SubTask("identify_filters", "确定筛选条件", "pending"))
        
        return tasks
    
    def _is_simple_query(self, question: str) -> bool:
        """判断是否是简单查询"""
        simple_indicators = ["是多少", "有多少", "总数"]
        return any(ind in question for ind in simple_indicators)


class GeneratorAgent:
    """MAC-SQL Generator Agent - SQL生成"""
    
    def __init__(self, llm):
        self.llm = llm
    
    def generate(self, subtask: SubTask, context: dict) -> str:
        """根据子任务生成SQL"""
        
        if subtask.task_id == "main":
            prompt = self._build_prompt(context["question"], context["schema"])
            return self.llm.generate(prompt)
        
        # 子任务SQL生成
        return f"-- SQL for {subtask.task_id}"
    
    def _build_prompt(self, question: str, schema: str) -> str:
        """构建SQL生成Prompt"""
        return f"""
根据用户问题生成SQL查询。

Schema:
{schema}

用户问题: {question}

要求:
1. 只生成SELECT查询
2. 使用提供的表结构和字段名
3. 添加适当的LIMIT限制
"""


class RefinerAgent:
    """MAC-SQL Refiner Agent - SQL修正"""
    
    def __init__(self, validator):
        self.validator = validator
    
    def check(self, sql: str) -> tuple[bool, str]:
        """三重检查"""
        
        # 1. 语法正确性
        if not self._check_syntax(sql):
            return False, "语法错误"
        
        # 2. 执行可行性
        if not self._check_executable(sql):
            return False, "无法执行"
        
        # 3. 结果非空
        if not self._check_result_not_empty(sql):
            return False, "查询结果为空"
        
        return True, "OK"
    
    def fix(self, sql: str, error: str) -> str:
        """基于错误反馈修正SQL"""
        # 这里应该调用LLM进行修正
        return sql


class MACSQLFramework:
    """MAC-SQL 多Agent协作框架"""
    
    def __init__(self, llm, validator):
        self.decomposer = DecomposerAgent()
        self.generator = GeneratorAgent(llm)
        self.refiner = RefinerAgent(validator)
    
    def query(self, question: str, schema: str) -> str:
        """执行多Agent协作查询"""
        
        # Step 1: 任务分解
        tasks = self.decomposer.decompose(question, schema)
        
        # Step 2: SQL生成
        context = {"question": question, "schema": schema}
        sql = self.generator.generate(tasks[0], context)
        
        # Step 3: 校验修正循环
        for _ in range(3):
            valid, error = self.refiner.check(sql)
            if valid:
                return sql
            sql = self.refiner.fix(sql, error)
        
        return sql
```

### 16.5 L1-L5 测试分级体系 (Phase 2)

```python
# tests/test_suite.py - NL2SQL五级挑战体系
"""
NL2SQL 五级测试体系

L1: 简单查询 (单表, 无聚合)
L2: 条件查询 (WHERE, 多条件)
L3: 嵌套查询 (子查询, 多表JOIN)
L4: 复杂推理 (多跳推理, 日期推理)
L5: 企业级 (跨数据库, 权限控制)
"""

TEST_SUITE = {
    "L1_简单查询": [
        {
            "id": "L1_001",
            "question": "总用户数是多少？",
            "expected_sql": "SELECT COUNT(*) FROM credit_data LIMIT 1000",
            "difficulty": "L1",
        },
        {
            "id": "L1_002",
            "question": "昨日华南区交易金额？",
            "expected_sql": "SELECT SUM(amount) FROM transactions WHERE region='华南' AND date='2024-01-01' LIMIT 1000",
            "difficulty": "L1",
        },
    ],
    
    "L2_条件查询": [
        {
            "id": "L2_001",
            "question": "月收入在5000-10000之间的用户数？",
            "expected_sql": "SELECT COUNT(*) FROM credit_data WHERE monthly_income BETWEEN 5000 AND 10000 LIMIT 1000",
            "difficulty": "L2",
        },
        {
            "id": "L2_002",
            "question": "未婚且学历为本科的用户逾期率？",
            "expected_sql": "SELECT ROUND(SUM(CASE WHEN serious_dlqin2yrs=1 THEN 1 ELSE 0 END)*100.0/COUNT(*),2) FROM credit_data WHERE marriage_status='未婚' AND education_level='本科' LIMIT 1000",
            "difficulty": "L2",
        },
    ],
    
    "L3_嵌套查询": [
        {
            "id": "L3_001",
            "question": "找出逾期率高于平均值的地区？",
            "expected_sql": "SELECT region FROM (SELECT region, ROUND(SUM(CASE WHEN serious_dlqin2yrs=1 THEN 1 ELSE 0 END)*100.0/COUNT(*),2) as rate FROM credit_data GROUP BY region) t WHERE rate > (SELECT AVG(rate) FROM (SELECT region, ROUND(SUM(CASE WHEN serious_dlqin2yrs=1 THEN 1 ELSE 0 END)*100.0/COUNT(*),2) as rate FROM credit_data GROUP BY region)) LIMIT 1000",
            "difficulty": "L3",
        },
    ],
    
    "L4_复杂推理": [
        {
            "id": "L4_001",
            "question": "与上月相比，本月各地区逾期率变化？",
            "expected_sql": "复杂多跳推理，测试日期推理能力",
            "difficulty": "L4",
        },
    ],
    
    "L5_企业级": [
        {
            "id": "L5_001",
            "question": "跨数据库关联用户画像表计算VIP用户逾期率？",
            "expected_sql": "跨数据库JOIN + 行级权限控制",
            "difficulty": "L5",
        },
    ],
}


def run_test_suite(level: str = "ALL"):
    """运行测试套件"""
    results = {"passed": 0, "failed": 0, "total": 0}
    
    levels = ["L1", "L2", "L3", "L4", "L5"] if level == "ALL" else [level]
    
    for lvl in levels:
        if lvl not in TEST_SUITE:
            continue
        
        for test_case in TEST_SUITE[lvl]:
            results["total"] += 1
            # 执行测试逻辑
            # if run_test(test_case):
            #     results["passed"] += 1
            # else:
            #     results["failed"] += 1
    
    return results
```

---

## 十七、Wiki最佳实践对齐清单

> 以下是对齐 Wiki 最佳实践的检查清单

### 17.1 已对齐项

| 模块 | Wiki参考文档 | 对齐状态 |
|:---|:---|:---:|
| 配置驱动架构 | [[ai-data-query-sql-generator]] | ✅ 已对齐 |
| 指标体系设计 | [[insight-20260408-metrics-platform]] | ✅ 已对齐 |
| 异动归因设计 | [[insight-20260408-metrics-platform]] | ✅ 已对齐 |
| 五层架构 | [[ai-data-query]] | ✅ 已对齐 |

### 17.2 待对齐项

| 模块 | Wiki参考文档 | 当前状态 | 目标状态 | 优先级 |
|:---|:---|:---|:---|:---:|
| **三层校验** | [[ai-data-query-sql-generator]] | 简单预检 | L1+L2+L3完整校验 | 🔴 高 |
| **DIN-SQL自修正** | [[ai-data-query-sql-generator]] | 无 | 自修正循环 | 🔴 高 |
| **意图分类** | [[ai-data-query-intent]] | 模式匹配 | 意图分类器 | 🟠 中 |
| **Schema Linking** | [[ai-data-query-sql-generator]] | 无 | 自动表字段识别 | 🟠 中 |
| **Terminology Mapping** | [[ai-data-query-components-oss]] | 简单同义词 | pgvector向量检索 | 🟠 中 |
| **MAC-SQL多Agent** | [[ai-data-query-components-oss]] | 无 | 三Agent协作 | 🟡 低 |
| **L1-L5测试分级** | [[ai-data-query-sql-generator]] | 20个用例 | 分级测试套件 | 🟠 中 |
| **语义层(MDL)** | [[insight-20260408-metrics-platform]] | 指标定义 | 完整语义层 | 🟡 低 |

### 17.3 对齐执行计划

> 详细演进路线见 [[#15-4-演进路线图|Section 15.4 演进路线图]]

执行优先级对照：

| 优先级 | 对齐任务 | 所属Phase | 产出 |
|:---:|:---|:---|:---|
| 🔴 | 三层校验 + DIN-SQL自修正 | Phase 2: 生产基础版 | core/validator.py |
| 🔴 | 意图分类 | Phase 3: 生产增强版 | core/intent_classifier.py |
| 🟠 | Schema Linking | Phase 3: 生产增强版 | core/schema_linker.py |
| 🟠 | L1-L5测试分级 | Phase 2: 生产基础版 | tests/test_suite.py |
| 🟠 | Terminology Mapping | Phase 3: 生产增强版 | core/terminology_mapper.py |
| 🟡 | MAC-SQL多Agent | Phase 3: 生产增强版 | core/mac_sql_framework.py |
| 🟡 | 语义层(MDL) | Phase 4: 企业级 | semantic_layer.py |

---

## 十八、总结与下一步行动

### 18.1 当前定位

| 维度 | 状态 | 说明 |
|:---|:---:|:---|
| **Demo能力** | ✅ 已完成 | 模板填充 + 特殊模板 |
| **生产基础** | ⚠️ 需补充 | 三层校验 + DIN-SQL |
| **生产增强** | 📝 规划中 | 意图分类 + MAC-SQL |
| **企业级** | 📝 规划中 | 语义层 + 权限体系 |

### 18.2 提升建议

| 优先级 | 行动项 | 产出 | 周期 |
|:---:|:---|:---|:---:|
| 🔴 | 补充三层校验机制 | core/validator.py | 1周 |
| 🔴 | 增加DIN-SQL自修正 | core/din_sql_corrector.py | 1周 |
| 🟠 | 补充意图分类层 | core/intent_classifier.py | 1周 |
| 🟠 | 建立L1-L5测试分级 | tests/test_suite.py | 1周 |
| 🟠 | 补充Schema Linking | core/schema_linker.py | 1周 |
| 🟡 | 评估MAC-SQL多Agent | core/mac_sql_framework.py | 2周 |

### 18.3 参考资料

| 资料 | 来源 | 说明 |
|:---|:---|:---|
| [[ai-data-query-sql-generator]] | Wiki | SQL生成与校验最佳实践 |
| [[ai-data-query-intent]] | Wiki | 意图理解最佳实践 |
| [[ai-data-query-components-oss]] | Wiki | 开源组件选型 |
| [[ai-data-query]] | Wiki | AI问数系统整体架构 |
| [[insight-20260408-metrics-platform]] | Wiki | 指标中台与语义层 |
| DIN-SQL | 微软论文 | 自修正机制参考 |
| MAC-SQL | 学术论文 | 多Agent协作参考 |
| WrenAI | GitHub ⭐14.9k | 完整NL2SQL实现参考 |

---

## 十九、生产落地经验分析

> 本章节沉淀消费金融风控场景 NL2SQL 落地的实战经验与踩坑记录

### 19.1 消费金融场景特殊性

#### 业务特点

| 特点 | 说明 | 对问数系统的影响 |
|:---|:---|:---|
| **数据敏感性高** | 风控数据涉及用户隐私、资产安全 | 需要严格的权限控制、数据脱敏 |
| **指标口径严格** | 逾期率/坏账率等指标有监管定义 | 必须对齐官方口径，不能自由定义 |
| **时效性要求** | 风控决策需要实时/准实时数据 | 查询延迟需控制在秒级 |
| **多部门协作** | 风控/运营/财务/监管各不相同 | 需要统一的指标中台 |

#### 核心痛点

```
┌─────────────────────────────────────────────────────────────┐
│              消费金融 NL2SQL 落地核心痛点                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1️⃣ 数据质量问题                                            │
│     ├── 字段缺失/格式不统一                                  │
│     ├── 历史数据与当前口径不一致                              │
│     └── 跨系统数据口径冲突                                    │
│                                                              │
│  2️⃣ 业务复杂性                                              │
│     ├── 逾期率定义多样（M1/M2/M3/坏账）                      │
│     ├── 特殊客群需要排除（如疫情期间展期）                    │
│     └── 监管报送口径与业务分析口径不同                        │
│                                                              │
│  3️⃣ 组织协作阻力                                            │
│     ├── 数据团队：担心问数系统降低数据团队价值                │
│     ├── 业务团队：担心数据准确性，不敢用                      │
│     └── 风控团队：对AI生成SQL不信任                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 19.2 指标口径统一经验

#### 问题描述

> "同一个'逾期率'，风控用M3口径，运营用M1口径，财务用账面口径，监管用另一套..."

#### 解决方案：指标定义层

```yaml
# config/metric_definitions.yaml
metrics:
  overdue_rate:
    # 官方监管口径
    regulatory:
      definition: "逾期90天以上贷款余额 / 资产余额"
      standard: " Basel III / 银监办发"
    
    # 风控分析口径
    risk_control:
      definition: "逾期30天以上户数 / 总户数"
      segments:
        M1: "逾期1-30天"
        M2: "逾期31-60天"
        M3: "逾期61-90天"
        NPL: "逾期90天以上（坏账）"
    
    # 财务核算口径
    finance:
      definition: "计提坏账 / 资产余额"
    
    # 业务默认口径
    default: "risk_control"
    
    # 别名映射
    aliases:
      - "坏账率"
      - "不良率"
      - "NPL比率"
```

#### 实施步骤

```
Step 1: 梳理所有指标口径
        ↓
Step 2: 建立指标定义层（YAML/数据库）
        ↓
Step 3: 与数据团队确认官方定义
        ↓
Step 4: 实现口径切换机制
        ↓
Step 5: 用户侧透明，只问"逾期率"自动匹配口径
```

### 19.3 常见踩坑与解决方案

#### 踩坑清单

| # | 踩坑场景 | 问题描述 | 解决方案 |
|:--:|:---|:---|:---|
| 1 | **时间表达歧义** | "上个月"在不同系统可能差一天 | 统一基准时间，明确"统计日"定义 |
| 2 | **空值处理** | NULL与0在业务含义不同 | SQL中使用`COALESCE`显式处理 |
| 3 | **除零错误** | 分母为0导致SQL失败 | 使用`NULLIF(分母, 0)`防护 |
| 4 | **精度丢失** | 百分比计算时小数丢失 | 使用`ROUND(value * 100.0, 2)` |
| 5 | **类型转换** | 字符串数字比较出错 | 显式`CAST`转换类型 |
| 6 | **日期格式** | 不同数据库日期格式不同 | 统一使用`YYYY-MM-DD` |
| 7 | **分母口径** | "总用户"可能是贷款户/注册户/活跃户 | 配置项明确定义 |
| 8 | **数据延迟** | T+1数据导致"今日"查询无结果 | 明确数据时间戳，显示数据日期 |

#### SQL防护模板

```python
# 安全SQL生成模板
SAFE_SQL_TEMPLATE = """
SELECT
    {dimension_expr},
    ROUND(
        SUM(CASE WHEN {metric_flag} = 1 THEN 1 ELSE 0 END) * 100.0 / 
        NULLIF(COUNT(*), 0),  -- 防护除零
        2
    ) as {metric_name}_rate
FROM {table_name}
WHERE 1=1
    {+time_filter}     -- 时间范围明确
    {+dimension_filter}
GROUP BY {dimension_expr}
ORDER BY {metric_name}_rate DESC
LIMIT {limit}
"""

def build_safe_sql(parsed: ParsedQuery) -> str:
    """构建安全的SQL"""
    
    # 1. 防护除零
    if parsed.metric == "overdue_rate":
        # 使用NULLIF防护
        sql = SAFE_SQL_TEMPLATE.format(
            dimension_expr=parsed.dimension_expr,
            metric_flag="serious_dlqin2yrs",
            metric_name="overdue",
            table_name=parsed.table_name,
            time_filter=_build_time_filter(parsed),
            dimension_filter=_build_dimension_filter(parsed),
            limit=parsed.limit or 1000
        )
    
    return sql
```

### 19.4 业务人员接受度提升

#### 问题：业务人员不信任AI生成的SQL

```
┌─────────────────────────────────────────────────────────────┐
│              业务人员接受度提升四步法                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Step 1: 透明化                                             │
│  ├── 显示生成的SQL                                           │
│  ├── 显示指标口径说明                                        │
│  └── 显示数据时间范围                                        │
│                                                              │
│  Step 2: 可验证                                             │
│  ├── 提供数据下载（与BI一致）                                │
│  ├── 提供计算过程说明                                        │
│  └── 支持与历史数据对比                                      │
│                                                              │
│  Step 3: 可纠错                                             │
│  ├── 用户可选择不同口径                                      │
│  ├── 用户可反馈错误                                          │
│  └── 反馈闭环机制                                            │
│                                                              │
│  Step 4: 渐进式                                              │
│  ├── 先给分析师用（高容忍度）                                │
│  ├── 收集问题，迭代优化                                      │
│  └── 逐步推广到业务人员                                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### 用户信任建设

| 策略 | 具体做法 |
|:---|:---|
| **SQL可见** | 每次查询显示"AI生成的SQL"，用户可审查 |
| **口径透明** | 鼠标悬停显示指标定义来源 |
| **数据溯源** | 点击可查看原始数据表和字段 |
| **人工确认** | 高风险查询（涉及拨备/坏账）需二次确认 |
| **反馈机制** | "结果不对？"提供反馈入口 |

### 19.5 数据团队协作模式

#### 问题：数据团队担心问数系统"取代"他们

#### 协作解法

```
┌─────────────────────────────────────────────────────────────┐
│              数据团队 + 问数系统 协作模式                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  数据团队职责:                                               │
│  ├── 维护指标定义层（指标库）                                │
│  ├── 审核SQL模板（质量把关）                                │
│  ├── 处理异常数据（数据质量）                                │
│  └── 提供业务咨询（高价值交互）                              │
│                                                              │
│  问数系统职责:                                              │
│  ├── 承接简单问数（80%场景）                                │
│  ├── 7x24小时服务                                            │
│  └── 数据民主化                                              │
│                                                              │
│  协作收益:                                                   │
│  ├── 数据团队: 从"取数工具人"→"数据专家"                    │
│  ├── 问数系统: 获取专业背书                                  │
│  └── 业务团队: 获得更快服务                                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 二十、RAG知识库设计

> 本章节设计支持业务知识、行业知识检索的 RAG 系统

### 20.1 知识库定位

```
┌─────────────────────────────────────────────────────────────────────┐
│                         AI-Query 知识库架构                          │
├─────────────────────────────────────────────────────────────────────┤
                                                                      │
│    用户问题                                                         │
│        │                                                           │
│        ▼                                                           │
│  ┌─────────────────────────────────────────────────────────┐       │
│  │                    RAG 检索层                             │       │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │       │
│  │  │ 业务知识库  │  │ 行业知识库  │  │ 技术知识库  │      │       │
│  │  │             │  │             │  │             │      │       │
│  │  │ ·指标定义   │  │ ·监管政策   │  │ ·SQL模板   │      │       │
│  │  │ ·口径文档   │  │ ·行业报告   │  │ ·最佳实践   │      │       │
│  │  │ ·业务规则   │  │ ·竞品分析   │  │ ·错误案例   │      │       │
│  │  │ ·术语词典   │  │ ·市场动态   │  │ ·架构设计   │      │       │
│  │  └─────────────┘  └─────────────┘  └─────────────┘      │       │
│  └─────────────────────────────────────────────────────────┘       │
│        │                                                           │
│        ▼                                                           │
│  ┌─────────────────────────────────────────────────────────┐       │
│  │                    知识注入层                             │       │
│  │  ┌─────────────────────────────────────────────────┐    │       │
│  │  │ Query: "华南区逾期率"                           │    │       │
│  │  │                                                 │    │       │
│  │  │ 召回知识:                                        │    │       │
│  │  │ 1. 指标定义: overdue_rate = 逾期户数/总户数     │    │       │
│  │  │ 2. 口径说明: 风控口径 vs 监管口径              │    │       │
│  │  │ 3. 地域维度: 华北区/华东区/华南区/...          │    │       │
│  │  │ 4. 历史案例: "华南区逾期率"查询记录           │    │       │
│  │  └─────────────────────────────────────────────────┘    │       │
│  └─────────────────────────────────────────────────────────┘       │
│        │                                                           │
│        ▼                                                           │
│  ┌─────────────────────────────────────────────────────────┐       │
│  │                    LLM 生成层                            │       │
│  │                                                         │       │
│  │  结合召回知识 + Schema配置 → 生成准确SQL               │       │
│  │                                                         │       │
│  └─────────────────────────────────────────────────────────┘       │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 20.2 业务知识库设计

#### 知识类型

| 知识类型 | 内容 | 示例 |
|:---|:---|:---|
| **指标定义** | 指标名称、计算公式、口径 | 逾期率 = 逾期户数 / 总户数 |
| **口径文档** | 不同场景的指标差异 | 风控口径 vs 监管口径 vs 财务口径 |
| **术语词典** | 业务术语与字段映射 | "华南区" → region IN ('广东', '广西', '海南') |
| **业务规则** | 取数限制、排除条件 | 排除展期客户、排除测试数据 |
| **历史案例** | 常见查询模式 | "按地区看逾期"的惯用维度组合 |

#### 业务知识库Schema

```yaml
# knowledge_base/business_knowledge.yaml
knowledge_base:
  name: business_knowledge
  description: 消费金融风控业务知识库
  
  collections:
    - name: metric_definitions
      description: 指标定义
      schema:
        - field: metric_name
          type: string
          description: 指标名称
        - field: metric_uri
          type: string
          description: 唯一标识符
        - field: formula
          type: string
          description: 计算公式
        - field: regulatory_definition
          type: text
          description: 监管口径说明
        - field: business_definition
          type: text
          description: 业务口径说明
        - field: aliases
          type: list[string]
          description: 别名列表
        - field: related_fields
          type: list[string]
          description: 相关数据库字段
        - field: valid_dimensions
          type: list[string]
          description: 可用维度
          
    - name: terminology
      description: 术语词典
      schema:
        - field: term
          type: string
          description: 术语名称
        - field: canonical_form
          type: string
          description: 标准形式
        - field: synonyms
          type: list[string]
          description: 同义词
        - field: dimension_values
          type: dict
          description: 维度值映射 {"华南区": ["广东", "广西", "海南"]}
        - field: usage_examples
          type: list[string]
          description: 使用示例
          
    - name: business_rules
      description: 业务规则
      schema:
        - field: rule_name
          type: string
          description: 规则名称
        - field: rule_type
          type: string
          enum: [exclusion, filter, calculation]
          description: 规则类型
        - field: description
          type: text
          description: 规则描述
        - field: sql_snippet
          type: string
          description: SQL片段
        - field: applicable_metrics
          type: list[string]
          description: 适用的指标
```

### 20.3 行业知识库设计

#### 知识类型

| 知识类型 | 内容 | 示例 |
|:---|:---|:---|
| **监管政策** | 银保监/央行政策文件 | 《商业银行互联网贷款管理办法》 |
| **行业报告** | 监管评级/年报分析 | 《2025年消费金融行业报告》 |
| **竞品分析** | 竞品功能/定价分析 | 蚂蚁/微众/京东的逾期率对比 |
| **市场动态** | 行业新闻/趋势分析 | "2025年消费金融监管趋严" |
| **合规要求** | 数据安全/隐私保护 | 《个人信息保护法》相关条款 |

#### 行业知识库Schema

```yaml
# knowledge_base/industry_knowledge.yaml
knowledge_base:
  name: industry_knowledge
  description: 金融行业知识库
  
  collections:
    - name: regulatory_policies
      description: 监管政策
      schema:
        - field: policy_name
          type: string
          description: 政策名称
        - field: issuing_authority
          type: string
          description: 发布机构
        - field: effective_date
          type: date
          description: 生效日期
        - field: key_requirements
          type: text
          description: 核心要求
        - field: data_reporting_requirements
          type: text
          description: 数据报送要求
        - field: related_metrics
          type: list[string]
          description: 相关指标
          
    - name: industry_reports
      description: 行业报告
      schema:
        - field: report_title
          type: string
          description: 报告标题
        - field: source
          type: string
          description: 来源机构
        - field: publish_date
          type: date
          description: 发布日期
        - field: key_findings
          type: text
          description: 核心发现
        - field: industry_benchmarks
          type: dict
          description: 行业基准 {"NPL率": "2.5%-4.0%"}
```

### 20.4 RAG检索架构

#### 整体流程

```
┌─────────────────────────────────────────────────────────────────────┐
│                        RAG 检索流程                                  │
├─────────────────────────────────────────────────────────────────────┤
                                                                      │
│  1️⃣ Query理解                                                      │
│     ├── 意图分类（指标查询/规则查询/合规查询）                       │
│     ├── 实体识别（指标名/地区/时间）                                │
│     └── 查询扩展（同义词/相关概念）                                  │
│                                                                      │
│  2️⃣ 混合检索                                                       │
│     ├── 向量检索（语义相似）                                        │
│     │   └── query embedding → top-k similar                         │
│     ├── 关键词检索（BM25）                                          │
│     │   └── extracted keywords → exact match                        │
│     └── 知识图谱检索（关系推理）                                     │
│         └── entity links → graph traversal                          │
│                                                                      │
│  3️⃣ 融合排序（RRF）                                                 │
│     └── Reciprocal Rank Fusion 合并多路结果                          │
│                                                                      │
│  4️⃣ 知识注入                                                        │
│     ├── Prompt组装：system + 召回知识 + user query                  │
│     └── LLM生成：结合知识生成准确回答                               │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

#### RAG实现代码

```python
# knowledge/rag_retriever.py
from dataclasses import dataclass
from typing import List, Optional
import numpy as np

@dataclass
class RetrievedKnowledge:
    """检索到的知识"""
    content: str
    source: str
    score: float
    knowledge_type: str  # metric_definition / terminology / rule / policy

class BusinessKnowledgeRetriever:
    """业务知识检索器"""
    
    def __init__(
        self,

class BusinessKnowledgeRetriever:
    """业务知识检索器"""
    
    def __init__(
        self,
        embedding_model,
        vector_store,
        bm25_index,
        knowledge_graph
    ):
        self.embedding_model = embedding_model
        self.vector_store = vector_store
        self.bm25_index = bm25_index
        self.knowledge_graph = knowledge_graph
    
    def retrieve(
        self,
        query: str,
        knowledge_types: List[str],
        top_k: int = 5
    ) -> List[RetrievedKnowledge]:
        """混合检索"""
        
        results = []
        
        # 1. 向量检索
        query_embedding = self.embedding_model.encode(query)
        vector_results = self.vector_store.search(
            query_embedding,
            filter={"knowledge_type": {"$in": knowledge_types}},
            top_k=top_k
        )
        results.extend(vector_results)
        
        # 2. BM25检索
        bm25_results = self.bm25_index.search(query, top_k=top_k)
        results.extend(bm25_results)
        
        # 3. 知识图谱检索
        entities = self._extract_entities(query)
        for entity in entities:
            kg_results = self.knowledge_graph.query(entity)
            results.extend(kg_results)
        
        # 4. RRF融合排序
        fused_results = self._reciprocal_rank_fusion(results, top_k)
        
        return fused_results
    
    def _reciprocal_rank_fusion(
        self,
        results: List[RetrievedKnowledge],
        k: int = 60
    ) -> List[RetrievedKnowledge]:
        """RRF融合排序"""
        
        # 按来源分组排名
        rankings = {}
        for result in results:
            if result.source not in rankings:
                rankings[result.source] = []
            rankings[result.source].append(result)
        
        # 计算RRF分数
        rrf_scores = {}
        for source, source_results in rankings.items():
            for rank, r in enumerate(source_results):
                score = 1.0 / (k + rank + 1)
                if r not in rrf_scores:
                    rrf_scores[r] = 0
                rrf_scores[r] += score
        
        # 排序返回
        sorted_results = sorted(
            rrf_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:k]
        
        return [r for r, _ in sorted_results]
    
    def _extract_entities(self, query: str) -> List[str]:
        """提取查询中的实体"""
        # 简化实现：提取关键词
        entities = []
        for word in query:
            if len(word) > 2:
                entities.append(word)
        return entities
```

### 20.5 知识注入机制

#### Prompt模板

```python
# knowledge/prompt_builder.py

SYSTEM_PROMPT = """
你是一个金融风控数据分析助手，负责根据用户问题生成准确的SQL查询。

## 背景知识
{knowledge_context}

## 数据库Schema
{schema_context}

## 指标定义
{metric_definitions}

## 查询规则
1. 只生成SELECT查询，禁止增删改
2. 使用提供的表结构和字段名
3. 时间字段格式：YYYY-MM-DD
4. 必须包含LIMIT限制
5. 使用COALESCE处理NULL值
6. 使用NULLIF防护除零错误

## 输出格式
返回JSON格式：
{{"success": true/false, "sql": "SQL语句", "explanation": "解释"}}
"""

def build_prompt(
    user_query: str,
    schema: str,
    retrieved_knowledge: List[RetrievedKnowledge],
    metric_definitions: dict
) -> str:
    """构建带知识的Prompt"""
    
    # 1. 组装知识上下文
    knowledge_context = _build_knowledge_context(retrieved_knowledge)
    
    # 2. 组装指标定义
    metric_def_str = _build_metric_def_string(metric_definitions)
    
    # 3. 组装完整Prompt
    prompt = SYSTEM_PROMPT.format(
        knowledge_context=knowledge_context,
        schema_context=schema,
        metric_definitions=metric_def_str
    )
    
    return prompt

def _build_knowledge_context(
    knowledge: List[RetrievedKnowledge]
) -> str:
    """构建知识上下文"""
    
    context_parts = []
    
    # 按类型分组
    by_type = {}
    for k in knowledge:
        if k.knowledge_type not in by_type:
            by_type[k.knowledge_type] = []
        by_type[k.knowledge_type].append(k)
    
    # 指标定义
    if "metric_definition" in by_type:
        context_parts.append("【指标定义】")
        for k in by_type["metric_definition"]:
            context_parts.append(f"- {k.content}")
    
    # 术语映射
    if "terminology" in by_type:
        context_parts.append("【术语映射】")
        for k in by_type["terminology"]:
            context_parts.append(f"- {k.content}")
    
    # 业务规则
    if "business_rule" in by_type:
        context_parts.append("【业务规则】")
        for k in by_type["business_rule"]:
            context_parts.append(f"- {k.content}")
    
    return "\n".join(context_parts)
```

### 20.6 知识库运营机制

#### 知识更新流程

```
┌─────────────────────────────────────────────────────────────────────┐
│                       知识库运营流程                                 │
├─────────────────────────────────────────────────────────────────────┤
                                                                      │
│  1️⃣ 知识采集                                                      │
│     ├── 人工录入：业务专家/数据团队                                │
│     ├── 自动抽取：从文档/邮件/Slack提取                            │
│     └── 外部导入：监管文件/行业报告                                │
│                                                                      │
│  2️⃣ 知识审核                                                      │
│     ├── 准确性审核：数据团队确认                                    │
│     ├── 一致性检查：与现有知识冲突检测                              │
│     └── 版本管理：变更历史追踪                                      │
│                                                                      │
│  3️⃣ 知识发布                                                      │
│     ├── 向量化处理：生成embeddings                                │
│     ├── 索引更新：向量库 + BM25索引                               │
│     └── 灰度发布：先小范围生效                                    │
│                                                                      │
│  4️⃣ 效果监控                                                      │
│     ├── 查询命中率：有多少查询召回知识                             │
│     ├── 使用反馈：用户对知识准确性的评价                           │
│     └── 问题发现：错误知识报告入口                                 │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

#### 知识质量评估

| 指标 | 说明 | 目标值 |
|:---|:---|:---|
| **覆盖率** | 知识库覆盖的指标/术语比例 | > 90% |
| **准确率** | 知识正确的比例 | > 95% |
| **召回率** | 查询能召回相关知识的比例 | > 80% |
| **时效性** | 新政策/规则入库时间 | < 24h |
| **满意度** | 用户对知识准确性的评价 | > 4.0/5 |

### 20.7 与现有系统的集成

#### 集成架构

```
┌─────────────────────────────────────────────────────────────────────┐
│                    RAG知识库集成架构                                 │
├─────────────────────────────────────────────────────────────────────┤
                                                                      │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐       │
│  │ 业务知识库   │     │ 行业知识库   │     │ 技术知识库   │       │
│  │ (YAML配置)  │     │ (飞书文档)   │     │ (GitHub)    │       │
│  └──────┬───────┘     └──────┬───────┘     └──────┬───────┘       │
│         │                    │                    │                │
│         └────────────────────┼────────────────────┘                │
│                              ▼                                      │
│                    ┌──────────────────┐                            │
│                    │  知识向量数据库   │                            │
│                    │   (ChromaDB)     │                            │
│                    └────────┬─────────┘                            │
│                             │                                       │
│                             ▼                                       │
│                    ┌──────────────────┐                            │
│                    │  QueryParser     │                            │
│                    │  (RAG Retriever)│                            │
│                    └────────┬─────────┘                            │
│                             │                                       │
│                             ▼                                       │
│                    ┌──────────────────┐                            │
│                    │   SQLBuilder    │                            │
│                    │  (知识增强)      │                            │
│                    └────────┬─────────┘                            │
│                             │                                       │
│                             ▼                                       │
│                    ┌──────────────────┐                            │
│                    │   QueryEngine   │                            │
│                    └──────────────────┘                            │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

#### 数据流

```
用户: "华南区逾期率是多少？"
           │
           ▼
QueryParser.parse()
    │
    ├── 意图识别 → metric_query
    │
    ▼
RAGRetriever.retrieve("华南区逾期率")
    │
    ├── 召回: overdue_rate指标定义
    ├── 召回: "华南区" → region IN ('广东','广西','海南')
    └── 召回: 历史查询案例
    │
    ▼
PromptBuilder.build(知识 + Schema + Query)
    │
    ▼
SQLBuilder.build()
    │
    ▼
SELECT region, 
       ROUND(SUM(CASE WHEN serious_dlqin2yrs=1 THEN 1 ELSE 0)*100.0/NULLIF(COUNT(*),0), 2) as overdue_rate
FROM credit_data
WHERE region IN ('广东', '广西', '海南')
GROUP BY region
```

---

*文档版本: v1.2*
*新增章节: 十九 (生产落地经验分析)、二十 (RAG知识库设计)*
*最后更新: 2026-05-19*
*维护者: 尼克·弗瑞*
