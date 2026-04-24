# 意图理解与指标映射 - 深度探索

> 解析业务人员自然语言查询，映射到具体字段和指标

---

## 元信息

- **所属专题**: [[ai-data-query]]
- **创建时间**: 2026-04-22
- **更新时间**: 2026-04-22
- **探索深度**: 深度（已分析SQLBot⭐5967 + dateparser⭐2804）
- **优先级**: 🔴 核心组件

---

## 核心问题

业务人员说"看一下上个月的销售"，系统需要知道：
1. **上个月** = 具体日期范围（某月1号到最后一天）
2. **销售** = 哪个表 + 哪个字段
3. **颗粒度** = 日聚合/月聚合/品类?

---

## 一、业界深度调研

### 1.1 SQLBot (⭐5967) - 中文智能问数标杆

**来源**: DataEase开源团队
**定位**: 基于大模型和RAG的智能问数系统
**语言**: JavaScript/Node.js (后端Python)

**核心发现**:

```
┌─────────────────────────────────────────────────────────────┐
│                 SQLBot 架构                                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  用户问题 ──► Terminology RAG ──► LLM Prompt ──► SQL        │
│                    │                    │                    │
│                    ▼                    ▼                    │
│              术语库检索          时间格式规范                 │
│              (pgvector)         (yyyy-MM-dd)               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**时间处理方式**:
```yaml
# SQLBot Prompt中的时间注入
<background-infos>
  <current-time>2025-08-08 11:23:00</current-time>
</background-infos>

# 规则要求:
- 如果是日期，没有指定具体格式 → yyyy-MM-dd
- 如果是年月，没有指定具体格式 → yyyy-MM
- 如果是年，没有指定具体格式 → yyyy
- 必须适配对应数据库引擎的语法
```

**术语系统设计**:
```python
class Terminology(SQLModel, table=True):
    id: Optional[int]
    word: Optional[str]           # 主术语
    pid: Optional[int]             # 父ID (用于同义词层级)
    description: Optional[str]     # 术语描述/计算公式
    embedding: Optional[List[float]]  # 向量嵌入 (pgvector)
    specific_ds: Optional[bool]    # 是否特定数据源
    datasource_ids: Optional[list[int]]  # 关联数据源
```

**关键洞察**: SQLBot选择让LLM处理时间解析，而不是预处理。

---

### 1.2 dateparser (⭐2804) - Python时间解析库

**支持的中文时间表达式**:
```python
>>> import dateparser
>>> dateparser.parse('2小时前')
datetime.datetime(2018, 5, 31, 20, 30)  # 假设当前22:30

>>> dateparser.parse('上个月')
datetime.datetime(2018, 4, 1)  # 或具体范围

>>> dateparser.parse('2024年3月')
datetime.datetime(2024, 3, 1)

# 支持200+语言 locale
```

**优点**:
- 支持多语言（含中文）
- 自动检测语言
- 支持相对时间表达式

**缺点**:
- 较重，依赖多
- 不返回日期范围，只返回单个日期

---

## 二、意图理解流程

```
用户输入: "看一下上个月华北区的销售额"
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│                    意图理解四步法                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Step 1: 时间表达式解析                                     │
│     输入: "上个月"                                          │
│     输出: {start: 2026-03-01, end: 2026-03-31}           │
│     方案: dateparser + 自定义中文扩展                        │
│                                                              │
│  Step 2: 地域/筛选条件提取                                  │
│     输入: "华北区"                                          │
│     输出: {field: 'region', operator: '=', value: '华北'} │
│     方案: 指标库枚举值匹配                                   │
│                                                              │
│  Step 3: 指标识别                                          │
│     输入: "销售额"                                          │
│     输出: {name: '销售额', field: 'amount', agg: 'SUM'}  │
│     方案: 术语库映射                                         │
│                                                              │
│  Step 4: 意图分类                                          │
│     输入: 完整query                                         │
│     输出: {type: 'metric_query', confidence: 0.95}        │
│     方案: 规则 + LLM fallback                               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 三、时间表达式解析 - 两种路径

### 路径A：Prompt注入（SQLBot方案）⭐推荐

**原理**: 在Prompt中注入当前时间，让LLM自己解析时间

```python
def build_time_injection_prompt(current_time: datetime) -> str:
    """构建时间注入的Prompt片段"""
    return f'''
<background-infos>
  <current-time>{current_time.strftime('%Y-%m-%d %H:%M:%S')}</current-time>
</background-infos>

时间格式规则:
- 如果没有指定具体格式，日期使用 yyyy-MM-dd
- 如果是年月，使用 yyyy-MM
- 如果是年，使用 yyyy
'''
```

**优点**:
- 简单，不需要预处理
- LLM可以理解复杂时间表达

**缺点**:
- 依赖LLM能力，不够稳定
- 每次请求都要传时间

---

### 路径B：预处理解析（混合方案）⭐⭐更精确

**原理**: 先用Python解析时间表达式，再传给LLM

```python
from dateparser.search import search_dates
from datetime import datetime, timedelta
import re

class TimeExpressionParser:
    """支持中文的时间表达式解析"""
    
    # 中文相对时间模式
    CHINESE_PATTERNS = {
        # 相对时间
        r'上*个月': lambda: get_last_month_range(),
        r'本月': lambda: get_current_month_range(),
        r'下*个月': lambda: get_next_month_range(),
        r'上周': lambda: get_last_week_range(),
        r'本周': lambda: get_current_week_range(),
        r'最近(\d+)天': lambda m: get_recent_days(int(m.group(1))),
        r'最近(\d+)周': lambda m: get_recent_weeks(int(m.group(1))),
        r'最近(\d+)个月': lambda m: get_recent_months(int(m.group(1))),
        
        # 绝对时间
        r'(\d{4})年(\d{1,2})月(\d{1,2})日?': 
            lambda m: (f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}", 
                      f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"),
        r'(\d{4})-(\d{1,2})-(\d{1,2})': 
            lambda m: (m.group(0), m.group(0)),
    }
    
    def parse(self, text: str, reference_time: datetime = None) -> dict:
        """解析时间表达式"""
        ref = reference_time or datetime.now()
        result = {'type': 'time', 'original': text}
        
        # 1. 先尝试中文自定义模式
        for pattern, handler in self.CHINESE_PATTERNS.items():
            match = re.search(pattern, text)
            if match:
                try:
                    date_range = handler(match)
                    if isinstance(date_range, dict):
                        result.update(date_range)
                    else:
                        result['value'] = date_range
                    result['parsed_by'] = 'chinese_pattern'
                    result['success'] = True
                    return result
                except:
                    continue
                
        # 2. 回退到dateparser
        dates = search_dates(text, languages=['zh', 'en'])
        if dates:
            result['value'] = dates[0][1]
            result['parsed_by'] = 'dateparser'
            result['success'] = True
            return result
            
        result['success'] = False
        return result


def get_last_month_range() -> dict:
    """获取上月的日期范围"""
    today = datetime.now()
    first_of_month = datetime(today.year, today.month, 1)
    last_month_end = first_of_month - timedelta(days=1)
    last_month_start = datetime(last_month_end.year, last_month_end.month, 1)
    return {
        'start': last_month_start.strftime('%Y-%m-%d'),
        'end': last_month_end.strftime('%Y-%m-%d'),
        'label': '上月'
    }

def get_current_month_range() -> dict:
    """获取本月的日期范围"""
    today = datetime.now()
    first_of_month = datetime(today.year, today.month, 1)
    last_day = calendar.monthrange(today.year, today.month)[1]
    last_of_month = datetime(today.year, today.month, last_day)
    return {
        'start': first_of_month.strftime('%Y-%m-%d'),
        'end': last_of_month.strftime('%Y-%m-%d'),
        'label': '本月'
    }
```

**Prompt中的使用**:
```python
def build_sql_prompt(query: str, time_info: dict) -> str:
    """构建SQL生成的Prompt"""
    time_block = ""
    if time_info.get('success'):
        time_block = f"""
<time-information>
  <parsed-time>
    开始日期: {time_info.get('start', 'N/A')}
    结束日期: {time_info.get('end', 'N/A')}
    时间标签: {time_info.get('label', 'N/A')}
  </parsed-time>
</time-information>
"""
    
    prompt = f"""
用户问题: {query}
{time_block}

请根据上述信息生成SQL。
"""
    return prompt
```

---

## 四、指标映射层

### 4.1 指标库设计 - 对标SQLBot术语系统

```yaml
# metric_library.yaml
version: "1.0"

tables:
  sales:
    physical_name: sales
    display_name: 销售表
    fields:
      - name: amount
        display_name: 销售额
        synonyms: [收入, 营收, 销售收入]
        type: decimal
        unit: 元
      - name: quantity
        display_name: 销售数量
        synonyms: [订单量, 销售量]
        type: int
        unit: 件
      - name: order_id
        display_name: 订单ID
        type: string
      - name: region
        display_name: 区域
        type: enum
        enum_values:
          - 华北区
          - 华东区
          - 华南区
          - 西部区
      - name: product_category
        display_name: 品类
        type: string
      - name: create_time
        display_name: 创建时间
        type: datetime

metrics:
  - name: 销售额
    display_names:
      - 销售额
      - 收入
      - 营收
      - 销售收入
    table: sales
    field: amount
    agg: SUM
    format: currency
    description: 含税销售额

  - name: 订单数
    display_names:
      - 订单数
      - 订单量
      - 订单数量
    table: sales
    field: order_id
    agg: COUNT_DISTINCT
    format: integer

  - name: 客单价
    display_names:
      - 客单价
      - 平均订单金额
    calculation: 销售额/订单数
    format: currency
    description: 平均每笔订单金额

dimensions:
  - name: 时间
    field: create_time
    type: datetime
    drill_levels:
      - 年
      - 季度
      - 月
      - 周
      - 日

  - name: 区域
    field: region
    type: enum
    drill_levels:
      - 大区
      - 省份
      - 城市

  - name: 品类
    field: product_category
    type: string
    drill_levels:
      - 一级分类
      - 二级分类
      - 商品
```

### 4.2 指标映射器实现

```python
class MetricMapper:
    """指标映射器 - 将业务术语映射到物理字段"""
    
    def __init__(self, metric_lib: dict):
        self.metrics = {m['name']: m for m in metric_lib['metrics']}
        self._build_reverse_index()
        
    def _build_reverse_index(self):
        """构建反向索引(业务名→指标)"""
        self.display_to_metric = {}
        for metric in self.metrics.values():
            # 主名称
            self.display_to_metric[metric['name']] = metric
            # 同义词
            for dn in metric.get('display_names', []):
                self.display_to_metric[dn] = metric
                
    def map(self, business_term: str) -> dict | None:
        """映射业务术语到指标定义"""
        return self.display_to_metric.get(business_term)
    
    def map_query(self, query_text: str) -> dict:
        """从查询文本中提取并映射指标"""
        result = {
            'metrics': [],
            'filters': [],
            'dimensions': []
        }
        
        # 1. 指标匹配
        for business_term, metric in self.display_to_metric.items():
            if business_term in query_text:
                if metric not in result['metrics']:
                    result['metrics'].append(metric)
        
        # 2. 筛选条件提取 (枚举值匹配)
        for table_name, table in self.metric_lib.get('tables', {}).items():
            for field in table.get('fields', []):
                if field.get('type') == 'enum':
                    for enum_val in field.get('enum_values', []):
                        if enum_val in query_text:
                            result['filters'].append({
                                'field': field['name'],
                                'operator': '=',
                                'value': enum_val
                            })
                                
        return result
```

---

## 五、意图分类

### 5.1 意图类型定义

```python
class IntentType(Enum):
    """支持的用户意图"""
    METRIC_QUERY = "metric_query"        # 指标查询
    DRILL_DOWN = "drill_down"            # 下钻分析
    COMPARE = "compare"                  # 对比分析
    RANKING = "ranking"                  # 排名查询
    TREND = "trend"                      # 趋势查询
    DISTRIBUTION = "distribution"        # 分布查询
    UNKNOWN = "unknown"                 # 未知
```

### 5.2 意图分类器

```python
class IntentClassifier:
    """基于规则的意图分类器"""
    
    INTENTS = {
        'drill_down': ['下钻', '细分', '拆分', '看看.*构成', '放大'],
        'compare': ['对比', '比较', '同比', '环比', '和.*差', 'vs', '对比'],
        'ranking': ['top', '排名', '前.*', '最高', '最低', '最好', '最差', 'TOP'],
        'trend': ['趋势', '走势', '变化', '增长', '下降', '趋势'],
        'distribution': ['分布', '占比', '构成', '比例'],
    }
    
    def classify(self, query: str) -> tuple[IntentType, float]:
        query_lower = query.lower()
        
        for intent, patterns in self.INTENTS.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    return IntentType(intent), 0.9
                    
        # 默认指标查询
        if any(kw in query_lower for kw in ['销售', '订单', '客户', '收入', '数据', '查看', '看看']):
            return IntentType.METRIC_QUERY, 0.8
            
        return IntentType.UNKNOWN, 0.5
```

### 5.3 LLM辅助分类 (复杂场景)

```python
class LLMIntentClassifier:
    """使用LLM进行意图分类"""
    
    SYSTEM_PROMPT = """你是一个BI查询意图分类器。
    
    用户输入可能是:
    - 指标查询:
    - 指标查询: "看一下3月销售额"
    - 下钻分析: "看看各区域的销售"
    - 对比分析: "和2月对比一下"
    - 排名查询: "销售额TOP10的商品"
    - 趋势查询: "最近3个月的销售趋势"
    - 分布查询: "各品类销售占比"
    
    请分类并返回JSON格式:
    {
        "intent": "metric_query/drill_down/compare/ranking/trend/distribution",
        "entities": {
            "time": "时间表达",
            "metric": "指标名称", 
            "dimension": "维度名称",
            "filter": "筛选条件"
        },
        "confidence": 0.0-1.0
    }
    """
    
    def classify(self, query: str) -> dict:
        response = self.llm.chat(
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": query}
            ],
            response_format="json"
        )
        return json.loads(response)
```

---

## 六、上下文管理

### 6.1 对话上下文

```python
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

@dataclass
class QueryContext:
    """当前查询的上下文"""
    user_id: str
    current_table: Optional[str] = None
    current_metrics: list = field(default_factory=list)
    current_filters: dict = field(default_factory=dict)
    current_time_range: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

class ConversationContextManager:
    """对话上下文管理器"""
    
    MAX_HISTORY = 10
    
    def __init__(self):
        self.sessions = {}  # user_id -> list[QueryContext]
        
    def get_context(self, user_id: str) -> Optional[QueryContext]:
        """获取用户当前上下文"""
        return self.sessions.get(user_id, [None])[-1] if user_id in self.sessions else None
        
    def update_context(self, user_id: str, query: 'StructuredQuery'):
        """更新用户上下文"""
        if user_id not in self.sessions:
            self.sessions[user_id] = []
            
        ctx = QueryContext(
            user_id=user_id,
            current_table=query.table,
            current_metrics=query.metrics,
            current_filters=query.filters,
            current_time_range=query.time_range
        )
        
        self.sessions[user_id].append(ctx)
        
        # 保持最近N条
        if len(self.sessions[user_id]) > self.MAX_HISTORY:
            self.sessions[user_id].pop(0)
            
    def resolve_reference(self, user_id: str, reference: str) -> dict:
        """解析代词引用 (如 '加上华北呢')"""
        ctx = self.get_context(user_id)
        if not ctx:
            return {}
            
        # 简化实现：基于上下文的引用解析
        if reference in ['它', '这个', '该']:
            return {
                'table': ctx.current_table,
                'metrics': ctx.current_metrics,
            }
            
        # 增量引用
        if reference.startswith('加上') or reference.startswith('再加'):
            return {'additional_filter': reference[2:]}
            
        return {}
```

### 6.2 追问场景处理

```
场景1: 简单追问
─────────────────────────────────
用户: 看一下3月的销售
      ↓
系统: table=sales, time=2026-03, metric=销售额
      
用户: 加上华北呢?
      ↓
系统: +filter[region]=华北 (复用上次的table和metric)

场景2: 时间推进
─────────────────────────────────
用户: 看看4月数据
      ↓
系统: time=2026-04 (保持table=sales不变)

场景3: 对比请求
─────────────────────────────────
用户: 和2月对比一下
      ↓
系统: 增加time_compare=2026-02, intent=compare
```

---

## 七、组件实现清单

### 推荐技术选型

| 子组件 | 推荐方案 | 备选 | 理由 |
|--------|----------|------|------|
| 时间解析 | dateparser + 自定义中文 | Prompt注入 | 支持多语言，扩展性强 |
| 指标映射 | YAML配置 + 内存索引 | 向量检索(pgvector) | 简单场景YAML足够 |
| 意图分类 | 规则 + LLM fallback | 纯LLM | 单表场景规则足够 |
| 上下文管理 | 内存 + Redis持久化 | 纯Redis | MVP阶段内存优先 |
| 同义词扩展 | 指标库内嵌 | 独立同义词库 | 与指标绑定更直观 |

### 目录结构建议

```
ai_data_query/
├── intent/
│   ├── __init__.py
│   ├── time_parser.py       # 时间表达式解析
│   ├── metric_mapper.py     # 指标映射
│   ├── intent_classifier.py  # 意图分类
│   ├── context_manager.py   # 上下文管理
│   └── config/
│       ├── time_words.yaml  # 时间词库
│       └── metric_library.yaml # 指标库
```

---

## 八、MVP实现路线

### Phase 1: 最小可用 (1-2周)

```python
# 核心功能
1. 时间解析: 手动支持 [今天/昨天/本月/上月/最近N天]
2. 指标映射: YAML配置，只支持3-5个核心指标
3. 意图分类: 规则匹配 (if '对比' in query → compare)
4. 上下文: 简单内存存储

# 示例
def parse_query(query: str) -> StructuredQuery:
    if '上个月' in query and '销售' in query:
        return StructuredQuery(
            table='sales',
            metrics=['销售额'],
            time_range={'start': '2026-03-01', 'end': '2026-03-31'}
        )
```

### Phase 2: 扩展能力 (2-3周)

```python
# 增加功能
1. 时间解析: dateparser支持更多表达式
2. 指标映射: 支持同义词匹配
3. 意图分类: LLM辅助分类
4. 上下文: 追问解析
```

### Phase 3: 完善 (3-4周)

```python
# 增加功能
1. 时间解析: 农历支持
2. 指标映射: 向量检索(pgvector)
3. 上下文: 多轮对话优化
4. 错误修正: SQL执行失败重试
```

---

## 九、参考资料

| 来源 | 链接 | 关键内容 |
|------|------|----------|
| SQLBot | https://github.com/dataease/SQLBot | 中文智能问数系统，术语系统设计 |
| dateparser | https://github.com/scrapinghub/dateparser | Python时间解析库 |
| NL2SQL Handbook | https://github.com/HKUSTDial/NL2SQL_Handbook | NL2SQL最新技术汇总 |

---

**下一步**: 探索组件2「SQL生成与校验」
