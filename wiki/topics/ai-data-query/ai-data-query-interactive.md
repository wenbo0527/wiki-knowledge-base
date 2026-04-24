# 交互式分析能力

> 支持用户对查询结果进行深入分析和探索

---

## 元信息

- **所属专题**: [[ai-data-query]]
- **创建时间**: 2026-04-22
- **优先级**: 🔴 核心组件

---

## 交互能力矩阵

```
┌─────────────────────────────────────────────────────────────┐
│                    交互式分析能力                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  🔽 下钻 (Drill Down)                                       │
│     从汇总数据 → 下一层级明细                                │
│     例: 月 → 日, 品类 → 单品                                │
│                                                              │
│  🔍 筛选 (Filter)                                           │
│     动态条件过滤                                             │
│     例: 只看华北区, 只看3月                                  │
│                                                              │
│  📊 对比 (Compare)                                           │
│     多维度对比分析                                           │
│     例: 同比/环比, A/B组对比                                 │
│                                                              │
│  📥 导出 (Export)                                            │
│     结果数据导出                                             │
│     支持Excel/CSV/PDF                                        │
│                                                              │
│  💬 追问 (Follow-up)                                        │
│     智能问题推荐                                             │
│     基于当前结果的追问建议                                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 下钻分析 (Drill Down)

### 下钻路径

```
销售总额
    │
    ├── 按月份
    │     └── 3月 → 每天明细
    │
    ├── 按区域
    │     └── 华北区 → 各省份
    │
    └── 按品类
          └── 电子产品 → 各类子品类
```

### 实现机制

```python
class DrillDownHandler:
    def handle(self, current_query: Query, drill_path: str) -> Query:
        # 1. 解析下钻路径
        # 2. 修改GROUP BY维度
        # 3. 添加筛选条件(如果是过滤型下钻)
        # 4. 返回新查询
        
        new_query = current_query.copy()
        
        if drill_path == 'by_day':
            new_query.group_by = f"DATE({current_query.time_field})"
            new_query.time_granularity = 'day'
            
        elif drill_path == 'by_region':
            new_query.group_by = 'region'
            
        return new_query
```

### UI交互

```
┌─────────────────────────────────────────────────────────────┐
│  📊 3月销售: ¥1,234,567                                   │
│                                                             │
│  按区域 ▼  |  按月份  |  按品类                           │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ 华北区     ████████████████████    456,789 (+15%)  │  │
│  │ 华东区     ████████████████████    523,456 (+10%)  │  │
│  │ 华南区     ████████████████        234,567 (+8%)   │  │
│  │ 西部区     ████████████            120,345 (+5%)   │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
│  [ 双击区域可下钻到省份 ]                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 动态筛选 (Filter)

### 筛选类型

| 筛选类型 | 控件 | 示例 |
|-----------|------|------|
| 时间筛选 | 日期选择器 | 选择月份/日期范围 |
| 枚举筛选 | 下拉多选 | 区域/品类 |
| 数值筛选 | 滑块/输入 | 销售额>10000 |
| 文本筛选 | 搜索框 | 客户名称包含"XX" |

### 筛选状态管理

```python
class FilterState:
    def __init__(self):
        self.filters = {}
        
    def add_filter(self, field: str, operator: str, value: Any):
        self.filters[field] = {
            'operator': operator,  # =, >, <, IN, LIKE, BETWEEN
            'value': value
        }
        
    def to_sql_where(self) -> str:
        # 将筛选状态转换为SQL WHERE子句
        clauses = []
        for field, filter_def in self.filters.items():
            op = filter_def['operator']
            val = filter_def['value']
            clauses.append(f"{field} {op} {val}")
        return " AND ".join(clauses) if clauses else "1=1"
```

### 筛选UI组件

```
┌─────────────────────────────────────────────────────────────┐
│  🔍 筛选                                                    │
│                                                             │
│  时间: [2026-03-01] ~ [2026-03-31]  [本月] [上月]        │
│                                                             │
│  区域: ☑ 华北区  ☑ 华东区  ☐ 华南区  ☐ 西部区           │
│                                                             │
│  品类: [电子产品      ▼] [全选] [清空]                    │
│                                                             │
│  销售额: [> 10000] 元                                      │
│                                                             │
│  [ 应用筛选 ]  [ 重置 ]                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 多维对比 (Compare)

### 对比模式

| 模式 | 说明 | SQL实现 |
|------|------|---------|
| 同比 | vs去年同期 | `WHERE year = YEAR(DATE_SUB(now(), INTERVAL 1 YEAR))` |
| 环比 | vs上期 | `WHERE month = MONTH(DATE_SUB(now(), INTERVAL 1 MONTH))` |
| 计划vs实际 | 对比目标 | JOIN计划表 |
| A/B组 | 实验对比 | `WHERE group IN ('A', 'B')` |

### 对比视图

```
┌─────────────────────────────────────────────────────────────┐
│  📊 3月 vs 2月 销售对比                                    │
│                                                             │
│         3月        2月       变化                          │
│  销售额  1,234,567  1,098,765  +12.4% 📈                 │
│  订单数     5,678      5,234    +8.5% 📈                 │
│  客单价      217.5       209.9    +3.6% ↗                  │
│                                                             │
│  [ 切换对比: 同比 | 环比 | 计划 ]                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 数据导出 (Export)

### 导出格式

| 格式 | 适用场景 | 实现 |
|------|----------|------|
| Excel (.xlsx) | 进一步分析 | openpyxl |
| CSV | 数据导入 | pandas |
| PDF | 报告分享 | reportlab/weasyprint |
| JSON | API调用 | 原生json |

### 导出配置

```python
class ExportConfig:
    def __init__(self):
        self.format = 'xlsx'  # xlsx, csv, pdf, json
        self.include_metadata = True  # 包含查询条件
        self.include_chart = False    # 包含图表
        self.max_rows = 10000         # 最大行数
        self.filename = None          # 自定义文件名
```

---

## 流式交互

### SSE流式返回

```python
from fastapi import FastAPI
from sse_starlette.sse import EventSourceResponse

@app.get("/query/stream")
async def query_stream(query: Query):
    async def event_generator():
        # 分批返回结果
        for batch in query.execute_batches():
            yield {
                'event': 'data',
                'data': json.dumps(batch)
            }
            
        # 发送完成信号
        yield {
            'event': 'done',
            'data': json.dumps({'status': 'complete'})
        }
        
    return EventSourceResponse(event_generator())
```

### 前端处理

```javascript
// 前端流式接收
const eventSource = new EventSource('/query/stream?sql=...');

eventSource.addEventListener('data', (event) => {
    const batch = JSON.parse(event.data);
    updateTable(batch);
});

eventSource.addEventListener('done', (event) => {
    hideLoading();
    showSuccess('查询完成');
});
```

---

## 分析场景模板

### 常用分析套路

```yaml
analysis_templates:
  - name: 月度销售分析
    steps:
      - 查询本月销售额/订单数/客单价
      - 环比上月
      - 展示各区域占比
      - 标注TOP3区域
      - 给出销售趋势图
      
  - name: 异常数据排查
    steps:
      - 筛选异常数据
      - 展示明细
      - 支持导出
      - 提供追问建议
```

---

## 组件清单

| 子组件 | 实现 | 状态 |
|--------|------|------|
| 下钻处理器 | Python | 📝 待设计 |
| 筛选状态管理 | React Context | 📝 待设计 |
| 对比计算器 | Python | 📝 待设计 |
| 导出服务 | openpyxl/pandas | 📝 待设计 |
| 流式返回 | SSE | 📝 待设计 |
| 分析模板 | YAML配置 | 📝 待设计 |

---

## 相关页面

- [[ai-data-query-result-explanation]] - 结果解释
- [[ai-data-query-intent]] - 意图理解

---

*最后更新: 2026-04-22*

---

## 深度探索补充

### 1. 多轮对话状态管理

```python
from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class ConversationState(Enum):
    IDLE = "idle"                    # 空闲，等待问题
    WAITING_QUERY = "waiting_query" # 等待查询执行
    RESULT_READY = "result_ready"   # 结果就绪
    FOLLOW_UP = "follow_up"         # 追问中

@dataclass
class AnalysisSession:
    """分析会话 - 管理多轮对话状态"""
    
    session_id: str
    user_id: str
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    # 状态
    state: ConversationState = ConversationState.IDLE
    
    # 查询上下文
    current_query: Optional['StructuredQuery'] = None
    current_result: Optional['QueryResult'] = None
    current_chart_config: Optional[dict] = None
    
    # 历史
    query_history: List['QueryRecord'] = field(default_factory=list)
    
    # 筛选状态
    active_filters: dict = field(default_factory=dict)
    
    # 分析偏好
    preferred_chart_type: Optional[str] = None
    default_time_range: str = "本月"
    
    def update_to_result(self, query: 'StructuredQuery', result: 'QueryResult'):
        """更新到结果就绪状态"""
        self.current_query = query
        self.current_result = result
        self.state = ConversationState.RESULT_READY
        self.updated_at = datetime.now()
        
    def add_filter(self, field: str, operator: str, value):
        """添加筛选条件"""
        self.active_filters[field] = {
            'operator': operator,
            'value': value,
            'applied': False
        }
        
    def apply_filters(self) -> 'StructuredQuery':
        """应用筛选条件到当前查询"""
        if not self.current_query:
            raise ValueError("No current query to apply filters")
            
        filtered_query = self.current_query.copy()
        for field, filter_def in self.active_filters.items():
            if not filter_def.get('applied'):
                filtered_query.add_filter(
                    field=field,
                    operator=filter_def['operator'],
                    value=filter_def['value']
                )
                filter_def['applied'] = True
                
        return filtered_query
```

### 2. 下钻/上卷处理器

```python
class DrillDownProcessor:
    """下钻/上卷处理器"""
    
    def __init__(self, schema: dict):
        self.schema = schema  # 表结构定义
        
    def get_drill_paths(self, query: 'StructuredQuery') -> List[dict]:
        """获取可用的下钻路径"""
        
        paths = []
        
        # 时间维度下钻
        if query.group_by == 'MONTH(create_time)':
            paths.extend([
                {'label': '按天', 'value': 'day', 'action': 'drill'},
                {'label': '按周', 'value': 'week', 'action': 'drill'},
            ])
        elif query.group_by == 'DATE(create_time)':
            paths.append({'label': '按周聚合', 'value': 'week', 'action': 'rollup'})
            
        # 地域维度下钻
        if 'region' in query.group_by:
            paths.extend([
                {'label': '按省份', 'value': 'province', 'action': 'drill'},
                {'label': '按城市', 'value': 'city', 'action': 'drill'},
            ])
            
        # 品类维度下钻
        if 'category' in query.group_by:
            paths.extend([
                {'label': '按子类', 'value': 'sub_category', 'action': 'drill'},
                {'label': '按商品', 'value': 'product', 'action': 'drill'},
            ])
            
        return paths
        
    def execute_drill(
        self,
        query: 'StructuredQuery',
        drill_path: str,
        drill_value: Any = None
    ) -> 'StructuredQuery':
        """执行下钻操作"""
        
        new_query = query.copy()
        
        if drill_path == 'day':
            new_query.group_by = 'DATE(create_time)'
            new_query.granularity = 'day'
            
        elif drill_path == 'week':
            new_query.group_by = 'YEARWEEK(create_time)'
            new_query.granularity = 'week'
            
        elif drill_path == 'province':
            new_query.group_by = 'province'
            if drill_value:
                # 如果选择了特定省份，下钻到城市
                new_query.add_filter('province', '=', drill_value)
                
        elif drill_path == 'sub_category':
            new_query.group_by = 'sub_category'
            
        elif drill_path == 'product':
            new_query.group_by = 'product_name'
            
        return new_query
        
    def execute_rollup(self, query: 'StructuredQuery') -> 'StructuredQuery':
        """执行上卷操作"""
        
        new_query = query.copy()
        current_group = query.group_by
        
        # 上卷规则
        rollup_map = {
            'DATE(create_time)': 'MONTH(create_time)',
            'MONTH(create_time)': 'YEAR(create_time)',
            'product_name': 'sub_category',
            'sub_category': 'category',
            'city': 'province',
            'province': 'region',
        }
        
        new_group = rollup_map.get(current_group)
        if new_group:
            new_query.group_by = new_group
            # 清除被上卷的筛选
            new_query.clear_filter_for_field(self._get_parent_field(current_group))
            
        return new_query
        
    def _get_parent_field(self, field: str) -> str:
        """获取父维度字段"""
        parent_map = {
            'product_name': 'sub_category',
            'sub_category': 'category',
            'city': 'province',
            'province': 'region',
        }
        return parent_map.get(field, field)
```

### 3. 对比分析处理器

```python
class CompareProcessor:
    """对比分析处理器"""
    
    def __init__(self, time_parser: 'TimeParser'):
        self.time_parser = time_parser
        
    def generate_compare_query(
        self,
        base_query: 'StructuredQuery',
        compare_type: str,  # 'mom', 'yoy', 'custom'
        compare_value: Any = None
    ) -> 'StructuredQuery':
        """生成对比查询"""
        
        new_query = base_query.copy()
        
        if compare_type == 'mom':  # 环比
            time_range = self.time_parser.get_last_period(
                base_query.time_range,
                granularity='month'
            )
            new_query.time_range = time_range
            new_query._compare_base = base_query  # 保存基准查询
            
        elif compare_type == 'yoy':  # 同比
            time_range = self.time_parser.get_same_period_last_year(
                base_query.time_range
            )
            new_query.time_range = time_range
            new_query._compare_base = base_query
            
        elif compare_type == 'custom':
            new_query.time_range = compare_value
            new_query._compare_base = base_query
            
        return new_query
        
    def merge_results(
        self,
        base_result: 'QueryResult',
        compare_result: 'QueryResult'
    ) -> 'CompareResult':
        """合并对比结果"""
        
        merged = {
            'base': base_result,
            'compare': compare_result,
            'changes': []
        }
        
        # 计算变化
        for base_row, compare_row in zip(base_result.rows, compare_result.rows):
            change = {
                'dimension': base_row.get('dimension'),
                'base_value': base_row.get('value'),
                'compare_value': compare_row.get('value'),
            }
            
            # 计算变化率和绝对变化
            if compare_row.get('value', 0) != 0:
                change['change_pct'] = (
                    (base_row.get('value', 0) - compare_row.get('value', 0))
                    / compare_row.get('value', 0) * 100
                )
            else:
                change['change_pct'] = None
                
            change['change_abs'] = (
                base_row.get('value', 0) - compare_row.get('value', 0)
            )
            
            merged['changes'].append(change)
            
        return CompareResult(**merged)
```

### 4. 智能追问生成器

```python
class FollowUpGenerator:
    """智能追问生成器"""
    
    def __init__(self, history_store: 'QueryHistoryStore'):
        self.history_store = history_store
        
    def generate_suggestions(
        self,
        query: 'StructuredQuery',
        result: 'QueryResult',
        limit: int = 4
    ) -> List[str]:
        """生成追问建议"""
        
        suggestions = []
        
        # 1. 基于当前结果的建议
        suggestions.extend(self._get_result_based_suggestions(query, result))
        
        # 2. 基于历史查询的建议
        suggestions.extend(self._get_history_based_suggestions(query))
        
        # 3. 基于数据特征的建议
        suggestions.extend(self._get_data_driven_suggestions(result))
        
        # 去重并返回前N个
        unique = list(dict.fromkeys(suggestions))
        return unique[:limit]
        
    def _get_result_based_suggestions(
        self,
        query: 'StructuredQuery',
        result: 'QueryResult'
    ) -> List[str]:
        """基于当前结果的建议"""
        
        suggestions = []
        
        # 如果有数据，提供下钻建议
        if result.row_count > 10:
            suggestions.append(f"查看{query.metric.name}的TOP10")
            
        # 如果有分类，提供占比建议
        if query.group_by in ('region', 'category', 'product'):
            suggestions.append(f"看看{self._get_dimension_label(query.group_by)}占比")
            
        # 如果有时间维度，提供趋势建议
        if 'time' in query.group_by:
            suggestions.append("看看最近的趋势变化")
            
        return suggestions
        
    def _get_history_based_suggestions(
        self,
        query: 'StructuredQuery'
    ) -> List[str]:
        """基于历史查询的建议"""
        
        # 获取用户最近的查询
        recent = self.history_store.get_recent(query.user_id, limit=5)
        
        suggestions = []
        for hist in recent:
            # 如果历史查询与当前不同，提议复用
            if hist.query_type != query.intent:
                suggestions.append(f"试试{self._get_intent_label(hist.query_type)}")
                
        return suggestions[:2]  # 最多2个
        
    def _get_data_driven_suggestions(
        self,
        result: 'QueryResult'
    ) -> List[str]:
        """基于数据特征的建议"""
        
        suggestions = []
        
        # 检测异常
        anomalies = self._detect_anomalies(result)
        if anomalies:
            suggestions.append(f"排查异常数据")
            
        # 检测缺失
        if result.has_missing_values():
            suggestions.append("看看缺失数据的原因")
            
        # 检测分布不均
        if result.has_imbalanced_distribution():
            suggestions.append("分析数据分布不均的原因")
            
        return suggestions
        
    def _detect_anomalies(self, result: 'QueryResult') -> List[dict]:
        """检测异常数据点"""
        anomalies = []
        
        values = [r.get('value', 0) for r in result.rows]
        if not values:
            return anomalies
            
        avg = sum(values) / len(values)
        
        for row in result.rows:
            value = row.get('value', 0)
            if value > avg * 3 or (avg != 0 and value < avg * 0.1):
                anomalies.append({
                    'dimension': row.get('dimension'),
                    'value': value,
                    'expected_range': (avg * 0.5, avg * 2)
                })
                
        return anomalies
```

### 5. 前端交互组件设计

```typescript
// React Context for analysis session
interface AnalysisContextType {
  // 状态
  session: AnalysisSession | null;
  isLoading: boolean;
  error: string | null;
  
  // 操作
  executeQuery: (query: string) => Promise<void>;
  applyDrillDown: (path: DrillPath) => Promise<void>;
  applyFilter: (filter: Filter) => Promise<void>;
  compare: (compareType: CompareType) => Promise<void>;
  export: (format: ExportFormat) => Promise<void>;
  followUp: (suggestion: string) => Promise<void>;
}

// Hook for components
function useAnalysis() {
  const context = useContext(AnalysisContext);
  
  return {
    // 状态
    result: context.session?.current_result,
    chartConfig: context.session?.current_chart_config,
    filters: context.session?.active_filters,
    canDrillDown: context.session?.current_query?.group_by !== 'product_name',
    canRollUp: context.session?.current_query?.group_by !== 'YEAR(create_time)',
    
    // 操作
    drillDown: context.applyDrillDown,
    rollUp: () => context.applyDrillDown({ action: 'rollup' }),
    setFilter: context.applyFilter,
    clearFilters: () => context.applyFilter(null), // null means clear
    compareWithLastMonth: () => context.compare('mom'),
    compareWithLastYear: () => context.compare('yoy'),
    exportToExcel: () => context.export('xlsx'),
  };
}

// 示例使用
function SalesDashboard() {
  const { result, drillDown, setFilter } = useAnalysis();
  
  return (
    <div>
      <FilterPanel onFilterChange={setFilter} />
      
      {result && (
        <>
          <Chart config={result.chartConfig} data={result.data} />
          
          <DrillDownBar>
            <button onClick={() => drillDown({ path: 'day' })}>
              按天查看
            </button>
            <button onClick={() => drillDown({ path: 'region' })}>
              按区域查看
            </button>
          </DrillDownBar>
          
          <FollowUpSuggestions onSelect={handleFollowUp} />
        </>
      )}
    </div>
  );
}
```

### 6. 实时协作标注

```python
class AnnotationSystem:
    """数据标注系统 - 支持在查询结果上添加注释"""
    
    def __init__(self, storage: 'AnnotationStorage'):
        self.storage = storage
        
    def add_annotation(
        self,
        query_id: str,
        user_id: str,
        annotation: dict
    ) -> str:
        """添加标注"""
        
        annotation_id = self._generate_id()
        
        record = {
            'id': annotation_id,
            'query_id': query_id,
            'user_id': user_id,
            'created_at': datetime.now().isoformat(),
            'content': annotation['content'],
            'type': annotation.get('type', 'comment'),  # comment, alert, flag
            'data_point': annotation.get('data_point'),  # 关联的数据点
            'replies': []
        }
        
        self.storage.save(record)
        return annotation_id
        
    def get_annotations(self, query_id: str) -> List[dict]:
        """获取查询的所有标注"""
        return self.storage.get_by_query(query_id)
        
    def add_reply(
        self,
        annotation_id: str,
        user_id: str,
        content: str
    ):
        """回复标注"""
        annotation = self.storage.get(annotation_id)
        if annotation:
            annotation['replies'].append({
                'user_id': user_id,
                'content': content,
                'created_at': datetime.now().isoformat()
            })
            self.storage.save(annotation)
```

---

**探索完成**: 组件5「交互式分析能力」
