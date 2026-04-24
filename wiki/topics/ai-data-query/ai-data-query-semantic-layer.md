# 语义层设计

> 定义业务指标与数据库字段的映射关系

---

## 元信息

- **所属专题**: [[ai-data-query]]
- **创建时间**: 2026-04-22
- **优先级**: 🔴 核心组件

---

## 核心问题

业务人员说"销售额"，系统需要知道：
1. **销售额** = 哪个表？
2. **销售额** = 哪个字段？
3. **销售额** = 怎么计算（SUM/COUNT/AVG）？
4. **销售额** = 时间范围怎么定？

---

## 语义层架构

```
┌─────────────────────────────────────────────────────────────┐
│                    语义层三层架构                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 业务指标层 (Metric Layer)                            │   │
│  │                                                      │   │
│  │ 销售额 = SUM(order.amount)                           │   │
│  │ 订单数 = COUNT(order.id)                             │   │
│  │ 客单价 = AVG(order.amount)                           │   │
│  │                                                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│                           ▼                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 业务术语层 (Terminology Layer)                       │   │
│  │                                                      │   │
│  │ 销售额 = 收入 = 营收 = GMV (同义词)                   │   │
│  │ 客户 = 用户 = 买家 (同义词)                           │   │
│  │                                                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│                           ▼                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 物理模型层 (Physical Layer)                          │   │
│  │                                                      │   │
│  │ order.amount (MySQL)                                 │   │
│  │ fact_sales.sales_amount (ClickHouse)                │   │
│  │                                                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## WrenAI MDL 语义模型

**参考**: WrenAI的MDL (Metric Definition Language)

### 模型定义示例

```yaml
# mdl.yaml
models:
  - name: orders
    table: orders
    
    dimensions:
      - name: order_date
        field: order_date
        type: time
        granularity: day
        
      - name: region
        field: region
        type: string
        
      - name: product_category
        field: category
        type: string
        
    metrics:
      - name: sales_amount
        field: amount
        aggregation: sum
        description: 销售额
        
      - name: order_count
        field: id
        aggregation: count
        description: 订单数
        
      - name: avg_order_amount
        field: amount
        aggregation: avg
        description: 平均客单价

relationships:
  - type: many_to_one
    source: orders
    target: customers
    condition: orders.customer_id = customers.id
    
  - type: many_to_one
    source: orders
    target: products
    condition: orders.product_id = products.id
```

---

## 指标定义规范

### 命名规范

| 类型 | 命名规则 | 示例 |
|------|----------|------|
| 维度 | snake_case | `order_date`, `region` |
| 指标 | snake_case | `sales_amount`, `order_count` |
| 同义词 | 用`,`分隔 | `销售额,收入,营收` |

### 字段类型

| 类型 | 说明 | 示例 |
|------|------|------|
| time | 时间维度 | `2024-01-01` |
| string | 字符串维度 | `华北`, `华东` |
| number | 数值维度 | `1500.00` |
| boolean | 布尔维度 | `true/false` |

### 聚合方式

| 聚合 | 说明 | 使用场景 |
|------|------|----------|
| sum | 求和 | 销售额、订单数 |
| avg | 平均 | 平均客单价、平均时长 |
| count |计数 | 独立用户数、订单数 |
| count_distinct | 去重计数 | 独立客户数 |
| max | 最大值 | 最大订单金额 |
| min | 最小值 | 最小订单金额 |

---

## 同义词管理

### YAML配置

```yaml
# terminology.yaml
terminology:
  sales:
    - 销售额
    - 收入
    - 营收
    - GMV
    - 总金额
    
  customer:
    - 客户
    - 用户
    - 买家
    - 消费者
    
  order:
    - 订单
    - 交易
    - 购买记录
```

### 向量检索实现

```python
class TerminologyMatcher:
    """术语匹配器 - 支持同义词匹配"""
    
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.terminology_db = {}
        
    def load_terminology(self, yaml_path: str):
        """加载术语配置"""
        with open(yaml_path) as f:
            data = yaml.safe_load(f)
            
        for canonical, synonyms in data['terminology'].items():
            # 存入向量库
            for synonym in synonyms:
                self.vector_store.add(synonym, canonical)
                self.terminology_db[synonym] = canonical
                
    def match(self, user_input: str) -> Optional[str]:
        """匹配用户输入到标准术语"""
        # 1. 精确匹配
        if user_input in self.terminology_db:
            return self.terminology_db[user_input]
            
        # 2. 向量相似度匹配
        return self.vector_store.search(user_input, top_k=1)
```

---

## 时间语义

### 时间表达式映射

| 用户说法 | 标准时间范围 | SQL |
|----------|-------------|-----|
| 今天 | 2026-04-22 | `DATE = '2026-04-22'` |
| 本月 | 2026-04-01 ~ 2026-04-30 | `MONTH = 4 AND YEAR = 2026` |
| 上个月 | 2026-03-01 ~ 2026-03-31 | `MONTH = 3 AND YEAR = 2026` |
| 最近7天 | 2026-04-16 ~ 2026-04-22 | `DATE >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)` |
| 本季度 | 2026-01-01 ~ 2026-03-31 | `QUARTER = 1 AND YEAR = 2026` |
| 今年 | 2026-01-01 ~ 2026-12-31 | `YEAR = 2026` |

### 时间解析器

```python
from dateparser import parse
from datetime import datetime, timedelta

class TimeExpressionParser:
    """时间表达式解析器"""
    
    def __init__(self):
        self.now = datetime.now()
        
    def parse(self, expression: str) -> dict:
        """解析时间表达式"""
        expression = expression.strip().lower()
        
        # 相对表达式
        if '今天' in expression:
            return self._today()
        elif '昨天' in expression:
            return self._yesterday()
        elif '本月' in expression or '这个月' in expression:
            return self._this_month()
        elif '上个月' in expression:
            return self._last_month()
        elif '最近' in expression:
            days = self._extract_days(expression)
            return self._recent_days(days)
        elif '本季度' in expression:
            return self._this_quarter()
        elif '今年' in expression or '本年度' in expression:
            return self._this_year()
            
        # 绝对日期
        parsed = parse(expression, languages=['zh'])
        if parsed:
            return {
                'start': parsed.strftime('%Y-%m-%d'),
                'end': parsed.strftime('%Y-%m-%d'),
                'granularity': 'day'
            }
            
        return None
        
    def _this_month(self) -> dict:
        start = self.now.replace(day=1)
        # 计算月末
        if self.now.month == 12:
            end = self.now.replace(month=12, day=31)
        else:
            end = self.now.replace(month=self.now.month+1, day=1) - timedelta(days=1)
        return {
            'start': start.strftime('%Y-%m-%d'),
            'end': end.strftime('%Y-%m-%d'),
            'granularity': 'month'
        }
```

---

## 筛选条件语义

### 常见筛选场景

| 筛选类型 | 用户说法 | SQL条件 |
|----------|----------|---------|
| 等于 | "只看华北" | `region = '华北'` |
| 包含 | "包含手机" | `product_name LIKE '%手机%'` |
| 大于 | "金额大于1000" | `amount > 1000` |
| 小于 | "小于500" | `amount < 500` |
| 区间 | "100到500之间" | `amount BETWEEN 100 AND 500` |
| TopN | "TOP10" | `LIMIT 10` |

---

## 组件清单

| 子组件 | 状态 | 说明 |
|--------|------|------|
| 指标定义 | 📝 待设计 | YAML定义 |
| 术语管理 | 📝 待设计 | 同义词+向量检索 |
| 时间解析 | 📝 待设计 | dateparser |
| 筛选条件 | 📝 待设计 | 条件构建器 |

---

## 相关页面

- [[ai-data-query-intent]] - 意图理解
- [[ai-data-query-sql-generator]] - SQL生成

---

*最后更新: 2026-04-22*
