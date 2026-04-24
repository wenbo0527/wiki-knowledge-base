# 结果解释与NLG

> 将查询结果转换为业务人员易理解的自然语言

---

## 元信息

- **所属专题**: [[ai-data-query]]
- **创建时间**: 2026-04-22
- **优先级**: 🟠 重要组件

---

## 核心价值

```
原始数据:
┌──────────┬─────────┐
│ 日期      │ 销售额   │
├──────────┼─────────┤
│ 2026-03  │ 1,234,567│
│ 2026-02  │ 1,098,765│
└──────────┴─────────┘

↓ NLG转换

业务语言:
📈 3月销售额123.5万元，环比增长12.4%
📊 为近6个月最高
⚠️ 但仍低于季度目标(150万)的82%
```

---

## 自然语言生成

### 基础模板

```python
class ResultExplainer:
    def explain(self, query: Query, result: QueryResult) -> str:
        parts = []
        
        # 1. 描述查询范围
        parts.append(self.describe_scope(query))
        
        # 2. 描述数据概况
        parts.append(self.describe_data(result))
        
        # 3. 描述趋势/变化
        if result.has_comparison():
            parts.append(self.describe_change(result))
            
        # 4. 标注异常
        parts.append(self.annotate_anomalies(result))
        
        return "\n".join(parts)
        
    def describe_scope(self, query: Query) -> str:
        time_range = query.time_range
        metric = query.metric.name
        return f"{time_range}的{metric}如下:"
        
    def describe_data(self, result: QueryResult) -> str:
        total = result.sum()
        count = result.count()
        return f"共{count}条记录，合计{total_formatted(total)}"
        
    def describe_change(self, result: QueryResult) -> str:
        change = result.change_percent()
        trend = "增长" if change > 0 else "下降"
        return f"较上期{trend}{abs(change)}%"
```

### 变化描述规则

| 变化幅度 | 描述词 | emoji |
|----------|--------|-------|
| >50% | 大幅增长/下降 | 📈📉 |
| 10-50% | 显著增长/下降 | ↑↓ |
| 0-10% | 小幅增长/下降 | ↗↘ |
| ≈0% | 基本持平 | ➡️ |

---

## 异常标注

### 自动检测规则

```python
class AnomalyDetector:
    def detect(self, result: QueryResult) -> list[str]:
        anomalies = []
        
        # 1. 零值检测
        if result.has_zeros():
            anomalies.append("⚠️ 部分数据为0")
            
        # 2. 空值检测
        if result.has_nulls():
            anomalies.append("⚠️ 存在空值记录")
            
        # 3. 极端值检测
        if result.has_outliers():
            anomalies.append("⚠️ 存在偏离较大的值")
            
        # 4. 缺失日期检测
        if result.has_missing_dates():
            anomalies.append("⚠️ 存在日期缺失")
            
        # 5. 环比异常
        if result.has_unusual_change():
            change = result.change_percent()
            if abs(change) > 100:
                anomalies.append(f"🚨 环比变化异常 ({change}%)")
                
        return anomalies
```

### 标注示例

```
┌─────────────────────────────────────────────────────────────┐
│  📊 3月销售汇总                                            │
│                                                             │
│  销售额: ¥1,234,567 (+12.4% ↑)                            │
│  订单数: 5,678 笔 (+8.2% ↑)                               │
│  客单价: ¥217.5 (+3.9% ↗)                                 │
│                                                             │
│  ⚠️ 注意:                                                   │
│  • 3月15日数据缺失                                          │
│  • 华北区销售额环比下降15%                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 图表推荐引擎

### 智能选图

```python
class ChartRecommender:
    CHART_RULES = {
        # 趋势 → 折线图
        ('time', 'trend'): 'line',
        
        # 构成 → 饼图/柱状图
        ('category', 'composition'): 'pie',
        
        # 对比 → 柱状图
        ('category', 'compare'): 'bar',
        
        # 分布 → 直方图
        ('numeric', 'distribution'): 'histogram',
        
        # 关系 → 散点图
        ('x_numeric', 'y_numeric'): 'scatter',
    }
    
    def recommend(self, query: Query, result: QueryResult) -> ChartConfig:
        dimension_type = self.get_dimension_type(query.dimension)
        purpose = self.get_purpose(query)
        
        chart_type = self.CHART_RULES.get(
            (dimension_type, purpose),
            'table'  # 默认表格
        )
        
        return ChartConfig(
            type=chart_type,
            x_field=query.dimension,
            y_field=query.metric,
            title=self.generate_title(query),
        )
```

### 图表选择矩阵

| 数据特征 | 目的 | 推荐图表 |
|----------|------|----------|
| 时间序列 | 展示趋势 | 折线图 |
| 类别对比 | 比较大小 | 柱状图 |
| 占比构成 | 显示份额 | 饼图/环形图 |
| 数值分布 | 了解分布 | 直方图 |
| 双变量关系 | 探索关联 | 散点图 |
| 多维数据 | 综合展示 | 表格 |

---

## 数据解读助手

### 追问推荐

```python
class FollowUpRecommender:
    def get_suggestions(self, query: Query, result: QueryResult) -> list[str]:
        suggestions = []
        
        # 基于结果的智能推荐
        if result.count() > 100:
            suggestions.append("📊 放大看某个分类")
            suggestions.append("🔍 查看TOP10明细")
            
        if result.has_change():
            suggestions.append("📈 追溯变化原因")
            suggestions.append("👥 对比各区域表现")
            
        if result.has_anomaly():
            suggestions.append("⚠️ 排查异常数据")
            suggestions.append("📋 导出异常明细")
            
        # 基于历史查询的推荐
        suggestions.extend(self.get_history_based_suggestions(query))
        
        return suggestions[:4]  # 最多返回4个
```

### 推荐示例

```
系统: "3月销售额123.5万元，环比增长12.4%"

你可能还想问:
  📊 看看各品类的销售占比
  👥 对比华北/华东/华南区域
  📈 为什么3月15日数据缺失
  🔍 查看销售额TOP10的客户
```

---

## DataLine图表实现参考

### Chart.js集成

```javascript
// DataLine的图表生成
class ChartGeneratorTool {
    async generate_chart(query_result, chart_type, request) {
        // 1. 验证数据格式
        this.validate_for_chart(query_result);
        
        // 2. 生成Chart.js配置
        const config = {
            type: chart_type,
            data: {
                labels: query_result.labels,
                datasets: [{
                    data: query_result.values,
                }]
            }
        };
        
        // 3. 渲染图表
        return renderChart(config);
    }
}
```

### 支持的图表类型

| 类型 | DataLine支持 | 说明 |
|------|-------------|------|
| 折线图 | ✅ | 时间趋势 |
| 柱状图 | ✅ | 对比分析 |
| 饼图 | ✅ | 占比展示 |
| 环形图 | ✅ | 占比展示 |
| 散点图 | ✅ | 关系探索 |

---

## 组件清单

| 子组件 | 实现 | 状态 |
|--------|------|------|
| 结果描述生成器 | 模板+规则 | 📝 待设计 |
| 变化描述器 | 规则引擎 | 📝 待设计 |
| 异常检测器 | 统计规则 | 📝 待设计 |
| 图表推荐器 | 规则+ML | 📝 待设计 |
| 追问推荐器 | 历史+规则 | 📝 待设计 |

---

## 相关页面

- [[ai-data-query-execution]] - 查询执行
- [[ai-data-query-interactive]] - 交互式分析

---

*最后更新: 2026-04-22*

---

## 深度探索补充

### 1. SQLBot图表生成Prompt (来源: ⭐5967)

SQLBot的图表生成Prompt非常完善，是中文智能问数的优秀参考：

```
┌─────────────────────────────────────────────────────────────┐
│          SQLBot 图表生成Prompt架构                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  输入:                                                       │
│  ├── <user-question> 用户问题                               │
│  ├── <sql> 生成的SQL                                        │
│  ├── <m-schema> 表结构信息                                  │
│  └── <chart-type> 推荐的图表类型                            │
│                                                              │
│  处理流程:                                                   │
│  1. 分析SQL，结合问题确认指标/维度/分类                       │
│  2. 应用Rules规则                                            │
│  3. 检查字段是否存在                                         │
│  4. 确认展示名称                                             │
│  5. 生成JSON配置                                             │
│  6. 校验JSON格式                                             │
│                                                              │
│  输出:                                                       │
│  └── JSON配置 {type, title, axis, series}                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 2. 图表选择规则

| 图表类型 | 使用场景 | SQL特征 |
|----------|----------|---------|
| **table** | 原始数据查看 | SELECT多条记录 |
| **line** | 时间趋势 | GROUP BY时间字段 |
| **column** | 分类对比(时间轴) | GROUP BY分类+时间 |
| **bar** | 分类对比(横向) | GROUP BY分类 |
| **pie** | 占比展示 | GROUP BY分类+聚合 |

### 3. SQLBot图表配置JSON格式

```python
# 表格配置
table_config = {
    "type": "table",
    "title": "标题",
    "columns": [
        {"name": "中文列名1", "value": "sql_alias_1"},
        {"name": "中文列名2", "value": "sql_alias_2"},
    ]
}

# 柱状图配置 (有时间/分类x轴)
column_config = {
    "type": "column",
    "title": "月度销售额",
    "axis": {
        "x": {"name": "月份", "value": "month"},
        "y": [{"name": "销售额", "value": "sales_amount"}],
    },
    "series": {"name": "产品类别", "value": "category"}  # 可选
}

# 折线图配置 (趋势)
line_config = {
    "type": "line",
    "title": "销售趋势",
    "axis": {
        "x": {"name": "日期", "value": "date"},
        "y": [
            {"name": "收入", "value": "income"},
            {"name": "支出", "value": "expense"}
        ],
        "multi-quota": {"name": "财务指标", "value": ["income", "expense"]}
    }
}

# 饼图配置 (占比)
pie_config = {
    "type": "pie",
    "title": "销售占比",
    "axis": {
        "y": {"name": "销售额", "value": "sales_amount"},
        "series": {"name": "产品类别", "value": "category"}
    }
}
```

### 4. 图表字段决策流程

```
┌─────────────────────────────────────────────────────────────┐
│              图表配置决策流程 (SQLBot)                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Step 1: SQL中是否有分类字段(非时间/非数值的离散字段)?       │
│           │                                                 │
│           ├─ 是 ──► 必须使用series ──► y轴只能有一个指标    │
│           │                                                 │
│           └─ 否 ──► Step 2                                 │
│                    │                                        │
│                    ▼                                        │
│           Step 2: 是否有多个指标字段?                       │
│                    │                                        │
│                    ├─ 是 ──► 使用multi-quota              │
│                    │                                        │
│                    └─ 否 ──► 直接配置y轴                   │
│                                                              │
│  ⚠️ 重要: series和multi-quota互斥，不能同时存在            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 5. 数据洞察生成Prompt

```python
INSIGHT_GENERATION_PROMPT = """
你是数据分析助手，根据查询结果生成数据洞察。

查询结果:
{query_result}

用户问题: {question}
指标: {metric}
时间范围: {time_range}

请生成包含以下内容的洞察:
1. 数据概要: 用一句话描述查询结果的核心发现
2. 关键数字: 突出显示最重要的数字
3. 变化趋势: 如果有对比数据，说明变化
4. 异常标注: 如果有异常值，标注出来
5. 业务解读: 从业务角度解读数据

输出格式(中文):
---
📊 数据概要: ...

💡 关键发现:
   • ...
   • ...

📈 趋势变化:
   • ...

⚠️ 需要关注:
   • ...
---
"""

def generate_insight(query_result: dict, question: str) -> str:
    """生成数据洞察"""
    
    # 1. 计算基本统计
    total = sum(query_result.get('values', []))
    count = len(query_result.get('values', []))
    avg = total / count if count > 0 else 0
    
    # 2. 检测趋势
    values = query_result.get('values', [])
    if len(values) >= 2:
        change_pct = (values[-1] - values[0]) / values[0] * 100
    else:
        change_pct = 0
        
    # 3. 检测异常
    anomalies = detect_anomalies(values)
    
    # 4. 生成洞察
    insight = f"""
📊 数据概要: 共查询到{count}条记录，合计{total:,.0f}。

💡 关键发现:
   • 平均值: {avg:,.0f}
   • 最大值: {max(values) if values else 0:,.0f}
   • 最小值: {min(values) if values else 0:,.0f}

📈 趋势变化:
   • 变化率: {change_pct:+.1f}%
   • 趋势: {'增长' if change_pct > 0 else '下降' if change_pct < 0 else '持平'}

{"⚠️ 需要关注: 检测到" + str(len(anomalies)) + "个异常值" if anomalies else ''}
"""
    return insight.strip()
```

### 6. NLG数值格式化

```python
class NumberFormatter:
    """数值格式化工具"""
    
    @staticmethod
    def format_currency(value: float, currency: str = "¥") -> str:
        """格式化货币"""
        if abs(value) >= 1_000_000:
            return f"{currency}{value/1_000_000:.1f}百万"
        elif abs(value) >= 1_000:
            return f"{currency}{value/1_000:.1f}万"
        else:
            return f"{currency}{value:,.0f}"
    
    @staticmethod
    def format_percent(value: float, decimals: int = 1) -> str:
        """格式化百分比"""
        return f"{value:+.{decimals}f}%"
    
    @staticmethod
    def format_change(current: float, previous: float) -> str:
        """格式化变化"""
        if previous == 0:
            return "N/A"
        change = (current - previous) / previous * 100
        direction = "↑" if change > 0 else "↓" if change < 0 else "→"
        return f"{abs(change):.1f}% {direction}"
    
    @staticmethod
    def describe_magnitude(value: float) -> str:
        """描述数量级"""
        abs_value = abs(value)
        if abs_value >= 1_000_000_000:
            return f"{value/1_000_000_000:.1f}十亿"
        elif abs_value >= 10_000_000:
            return f"{value/10_000_000:.1f}千万"
        elif abs_value >= 1_000_000:
            return f"{value/1_000_000:.1f}百万"
        elif abs_value >= 1_000:
            return f"{value/1_000:.1f}千"
        else:
            return f"{value:.0f}"
```

### 7. 追问推荐Prompt (SQLBot)

```python
GUESS_QUESTION_PROMPT = """
### 你的任务:
根据给定的表结构、用户问题以及以往提问，推测用户接下来可能提问的问题。

### 规则:
1. 推测的问题需要与表结构相关
2. 可以涉及图表展示(table/column/bar/line/pie)
3. 推测问题不能与当前问题重复
4. 如果有历史提问，参考最频繁的问题
5. 忽略"重新生成"相关问题
6. 最多返回{articles_number}个推测问题

### 输出格式(JSON数组):
["推测问题1", "推测问题2", "推测问题3"]

### 如果无法推测:
返回空数组: []

### 表结构:
{schema}

### 当前问题:
{current_question}

### 历史问题(参考):
{history_questions}
"""
```

### 8. 实战：完整结果解释器

```python
class ResultExplainer:
    """完整的结果解释器"""
    
    def __init__(
        self,
        chart_recommender: ChartRecommender,
        anomaly_detector: AnomalyDetector,
        formatter: NumberFormatter
    ):
        self.chart_recommender = chart_recommender
        self.anomaly_detector = anomaly_detector
        self.formatter = formatter
        
    def explain(
        self,
        query: Query,
        sql_result: list,
        chart_type: str = None
    ) -> Explanation:
        """生成完整的查询解释"""
        
        # 1. 格式化数据
        formatted_data = self._format_result(sql_result)
        
        # 2. 计算统计
        stats = self._calculate_stats(formatted_data)
        
        # 3. 生成NL描述
        nl_description = self._generate_description(query, stats)
        
        # 4. 检测异常
        anomalies = self.anomaly_detector.detect(stats['values'])
        
        # 5. 推荐图表
        if not chart_type:
            chart_type = self.chart_recommender.recommend(query, stats)
        
        # 6. 推荐追问
        follow_ups = self._generate_followups(query, stats)
        
        return Explanation(
            summary=nl_description,
            stats=stats,
            anomalies=anomalies,
            chart_config=self._build_chart_config(chart_type, query, stats),
            follow_ups=follow_ups
        )
        
    def _generate_description(
        self,
        query: Query,
        stats: dict
    ) -> str:
        """生成自然语言描述"""
        
        metric = query.metric
        time_range = query.time_range
        
        # 基础描述
        parts = []
        parts.append(f"{time_range}的{metric.name}数据如下:")
        parts.append(f"共{stats['count']}条记录")
        
        # 数值描述
        if metric.format == 'currency':
            total = self.formatter.format_currency(stats['sum'])
            parts.append(f"合计{total}")
        elif metric.format == 'percent':
            parts.append(f"平均{stats['avg']:.1f}%")
        else:
            parts.append(f"合计{stats['sum']:,.0f}")
            
        # 趋势描述
        if stats.get('change_pct') is not None:
            change = stats['change_pct']
            trend = "增长" if change > 0 else "下降" if change < 0 else "持平"
            parts.append(f"较上期{trend}{abs(change):.1f}%")
            
        return "，".join(parts)
        
    def _build_chart_config(
        self,
        chart_type: str,
        query: Query,
        stats: dict
    ) -> dict:
        """构建图表配置"""
        
        if chart_type == 'table':
            return {
                "type": "table",
                "title": f"{query.time_range}{query.metric.name}",
                "columns": [
                    {"name": col['display'] if 'display' in col else col['name'], 
                     "value": col['name']}
                    for col in stats['columns']
                ]
            }
        elif chart_type in ('column', 'bar', 'line'):
            return {
                "type": chart_type,
                "title": f"{query.time_range}{query.metric.name}",
                "axis": {
                    "x": {"name": query.dimension or "日期", "value": "date"},
                    "y": [{"name": query.metric.name, "value": query.metric.field}]
                }
            }
        elif chart_type == 'pie':
            return {
                "type": "pie",
                "title": f"{query.time_range}{query.metric.name}占比",
                "axis": {
                    "y": {"name": query.metric.name, "value": query.metric.field},
                    "series": {"name": query.dimension, "value": "category"}
                }
            }
```

---

**下一步**: 探索组件5「交互式分析能力」
