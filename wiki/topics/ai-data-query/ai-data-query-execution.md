# 查询执行与优化

> 高效、安全地执行SQL查询

---

## 元信息

- **所属专题**: [[ai-data-query]]
- **创建时间**: 2026-04-22
- **优先级**: 🔴 核心组件

---

## 核心功能

```
SQL Query → 连接池 → 查询执行 → 结果缓存 → 返回前端
                ↓
            限流保护
                ↓
            超时控制
```

---

## 查询执行器

### 基础实现

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

class QueryExecutor:
    def __init__(self, dsn: str, pool_size: int = 5):
        self.engine = create_engine(
            dsn,
            poolclass=QueuePool,
            pool_size=pool_size,
            max_overflow=10,
            pool_pre_ping=True,
            pool_recycle=3600,
        )
        
    def execute(self, sql: str, timeout: int = 30) -> QueryResult:
        with self.engine.connect() as conn:
            # 设置查询超时
            result = conn.execute(text(sql))
            return result.fetchall()
```

### 查询超时控制

```python
import signal

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Query timeout")

def execute_with_timeout(sql: str, timeout: int = 30):
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)
    try:
        result = execute(sql)
    finally:
        signal.alarm(0)
    return result
```

---

## 缓存策略

### 多级缓存

```
┌─────────────────────────────────────────────────────────────┐
│                    多级缓存架构                               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  L1: 内存缓存 (进程内)                                       │
│      └── 最近查询结果, TTL=5分钟                             │
│                                                              │
│  L2: Redis缓存 (分布式)                                     │
│      └── 热点查询结果, TTL=30分钟                            │
│                                                              │
│  L3: 结果物化                                                │
│      └── 定期预计算, 适用于日报/周报                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 缓存键设计

```python
def make_cache_key(sql: str, params: dict) -> str:
    """生成缓存键"""
    # 标准化SQL
    normalized_sql = normalize_sql(sql)
    # 合并参数
    key = hash(normalized_sql + str(sorted(params.items())))
    return f"query:{key}"

def normalize_sql(sql: str) -> str:
    """标准化SQL以提高缓存命中率"""
    # 移除多余空格
    # 统一大小写
    # 标准化日期格式
    return sql.strip().upper()
```

---

## 限流保护

### 限流策略

```python
from collections import defaultdict
import time

class RateLimiter:
    def __init__(self, max_per_minute: int = 60):
        self.max_per_minute = max_per_minute
        self.requests = defaultdict(list)
        
    def is_allowed(self, user_id: str) -> bool:
        now = time.time()
        # 清理超过1分钟的记录
        self.requests[user_id] = [
            t for t in self.requests[user_id]
            if now - t < 60
        ]
        
        if len(self.requests[user_id]) >= self.max_per_minute:
            return False
            
        self.requests[user_id].append(now)
        return True
```

### 并发控制

| 策略 | 说明 | 适用场景 |
|------|------|----------|
| 连接池 | 复用DB连接 | 高并发 |
| 查询队列 | FIFO排队执行 | 高优先级场景 |
| 熔断器 | 连续失败时暂停 | 保护数据库 |

---

## 查询优化

### 自动优化规则

```python
OPTIMIZATION_RULES = [
    # 1. 添加LIMIT
    {"pattern": r"SELECT .* (?!LIMIT)", "fix": "LIMIT 1000"},
    
    # 2. 确保有索引
    {"check": "EXPLAIN", "threshold": 10000},
    
    # 3. 大查询降级
    {"pattern": r"GROUP BY.*ORDER BY NULL", "fix": "保持原样"},
]
```

### 慢查询识别

```python
# 记录慢查询日志
SLOW_QUERY_THRESHOLD = 5.0  # 5秒

def log_slow_query(sql: str, duration: float):
    if duration > SLOW_QUERY_THRESHOLD:
        logger.warning(f"Slow query ({duration}s): {sql}")
```

---

## 数据安全

### 权限控制

```python
class PermissionChecker:
    def check(self, user_id: str, table: str, sql: str) -> bool:
        # 1. 检查用户是否有表访问权限
        if not self.user_table_access[user_id].get(table):
            return False
            
        # 2. 检查SQL是否只包含SELECT
        if not sql.strip().upper().startswith('SELECT'):
            return False
            
        # 3. 检查是否访问禁止字段
        forbidden = self.forbidden_fields.get(table, [])
        for field in forbidden:
            if field in sql:
                return False
                
        return True
```

### 行级权限

```python
# 示例: 用户只能看自己区域的数据
def add_row_filter(sql: str, user_id: str) -> str:
    user_region = get_user_region(user_id)
    if user_region:
        # 动态添加WHERE条件
        return f"{sql} AND region = '{user_region}'"
    return sql
```

---

## WrenAI wren-engine参考

### 架构

```
wren-engine (Rust + Apache DataFusion)
    │
    ├── MDL解析 (Metric Definition Layer)
    ├── 查询规划 (Query Planning)
    ├── 语义优化 (Semantic Optimization)
    └── 跨数据源执行 (Federated Query)
```

### 特点

| 特性 | 说明 |
|------|------|
| 多数据源 | 15+连接器 |
| 查询优化 | Apache DataFusion |
| 语义层 | MDL定义 |

---

## 组件清单

| 子组件 | 实现 | 状态 |
|--------|------|------|
| 连接池管理 | SQLAlchemy | 📝 待设计 |
| 查询执行器 | 原生+sqlalchemy | 📝 待设计 |
| 超时控制 | signal/alarm | 📝 待设计 |
| 结果缓存 | Redis/LRU | 📝 待设计 |
| 限流器 | Python | 📝 待设计 |
| 慢查询日志 | logging | 📝 待设计 |

---

## 相关页面

- [[ai-data-query-sql-generator]] - SQL生成
- [[ai-data-query-result-explanation]] - 结果解释

---

*最后更新: 2026-04-22*

---

## 深度探索补充

### 1. SQLAlchemy连接池深度配置

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool, NullPool

# 生产环境推荐配置
engine = create_engine(
    "postgresql://user:pass@localhost/db",
    
    # 连接池配置
    poolclass=QueuePool,
    pool_size=20,              # 基础连接数
    max_overflow=30,           # 最多额外30个连接
    pool_timeout=30,           # 获取连接超时(秒)
    pool_recycle=1800,         # 30分钟后回收连接
    pool_pre_ping=True,        # 使用前检测连接
    
    # 执行配置
    execution_options={
        "statement_timeout": 30000,  # 30秒超时 (PostgreSQL)
        "query_timeout": 30,         # 查询超时
    }
)

# 测试环境: 无连接池
test_engine = create_engine(
    "sqlite:///:memory:",
    poolclass=NullPool        # 每次创建新连接
)
```

### 2. 查询超时实现 (跨数据库)

```python
import signal
from functools import wraps
from contextlib import contextmanager

class QueryTimeout(Exception):
    """查询超时异常"""
    pass

@contextmanager
def query_timeout(seconds: int):
    """上下文管理器实现查询超时"""
    def handler(signum, frame):
        raise QueryTimeout(f"Query exceeded {seconds} seconds")
    
    # 仅在Unix系统有效
    if hasattr(signal, 'SIGALRM'):
        old_handler = signal.signal(signal.SIGALRM, handler)
        signal.alarm(seconds)
    
    try:
        yield
    finally:
        if hasattr(signal, 'SIGALRM'):
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old_handler)

# 使用示例
def execute_with_timeout(sql: str, timeout: int = 30):
    try:
        with query_timeout(timeout):
            return execute(sql)
    except QueryTimeout:
        logger.warning(f"Query timeout after {timeout}s: {sql[:100]}")
        return None
```

### 3. PostgreSQL-specific超时设置

```python
from sqlalchemy import text

# PostgreSQL使用 statement_timeout
POSTGRES_TIMEOUT_SQL = """
SET statement_timeout = '30s';
SET lock_timeout = '10s';
SET idle_in_transaction_session_timeout = '60s';
"""

def execute_with_postgres_timeout(sql: str, conn, timeout_ms: int = 30000):
    """PostgreSQL查询超时实现"""
    # 设置超时
    conn.execute(text(f"SET statement_timeout = '{timeout_ms}ms'"))
    
    try:
        result = conn.execute(text(sql))
        return result.fetchall()
    except Exception as e:
        if 'statement timeout' in str(e):
            raise QueryTimeout(f"Query exceeded {timeout_ms}ms")
        raise
    finally:
        # 重置超时
        conn.execute(text("SET statement_timeout = '0'"))
```

### 4. Redis缓存实现

```python
import redis
import json
import hashlib
from typing import Optional, Any

class QueryCache:
    """SQL查询结果缓存"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        self.redis = redis.from_url(redis_url, decode_responses=True)
        self.default_ttl = 300  # 5分钟
        
    def _make_key(self, sql: str, params: dict = None) -> str:
        """生成缓存键"""
        content = sql.strip().upper()
        if params:
            content += json.dumps(params, sort_keys=True)
        return f"sql_cache:{hashlib.md5(content.encode()).hexdigest()}"
    
    def get(self, sql: str, params: dict = None) -> Optional[Any]:
        """获取缓存"""
        key = self._make_key(sql, params)
        data = self.redis.get(key)
        if data:
            return json.loads(data)
        return None
    
    def set(
        self, 
        sql: str, 
        result: Any, 
        params: dict = None,
        ttl: int = None
    ) -> None:
        """设置缓存"""
        key = self._make_key(sql, params)
        ttl = ttl or self.default_ttl
        self.redis.setex(key, ttl, json.dumps(result))
    
    def invalidate(self, pattern: str = "*") -> int:
        """清除匹配的缓存"""
        keys = self.redis.keys(f"sql_cache:{pattern}")
        if keys:
            return self.redis.delete(*keys)
        return 0
```

### 5. 多级缓存架构

```
┌─────────────────────────────────────────────────────────────┐
│                 多级缓存查询流程                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Query ──► L1_内存 ──► L2_Redis ──► DB执行                 │
│              │              │                               │
│           命中返回         命中返回                          │
│              │              │                               │
│              ▼              ▼                               │
│           获取数据      获取数据                             │
│              │              │                               │
│              └──────┬───────┘                               │
│                     ▼                                        │
│                  回填L1                                      │
│                     │                                        │
│                     ▼                                        │
│                  返回数据                                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

```python
from functools import lru_cache
from threading import Lock

class MultiLevelCache:
    """多级缓存"""
    
    def __init__(self, redis_cache: QueryCache):
        self.redis = redis_cache
        self.local_cache = {}  # 进程内LRU
        self.local_lock = Lock()
        self.local_max_size = 100
        
    def get(self, sql: str, params: dict = None) -> Optional[Any]:
        """获取缓存，优先L1再L2"""
        
        # L1: 进程内缓存
        key = self.redis._make_key(sql, params)
        with self.local_lock:
            if key in self.local_cache:
                return self.local_cache[key]
        
        # L2: Redis缓存
        result = self.redis.get(sql, params)
        if result:
            # 回填L1
            with self.local_lock:
                self.local_cache[key] = result
                if len(self.local_cache) > self.local_max_size:
                    # 简单LRU：删除最早的
                    self.local_cache.pop(next(iter(self.local_cache)))
        
        return result
```

### 6. 限流器实现

```python
import time
from collections import defaultdict, deque
from threading import Lock

class SlidingWindowRateLimiter:
    """滑动窗口限流器"""
    
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(deque)
        self.lock = Lock()
        
    def is_allowed(self, key: str) -> bool:
        """检查是否允许请求"""
        now = time.time()
        cutoff = now - self.window_seconds
        
        with self.lock:
            # 清理过期的请求记录
            self.requests[key] = deque(
                t for t in self.requests[key]
                if t > cutoff
            )
            
            # 检查是否超限
            if len(self.requests[key]) >= self.max_requests:
                return False
                
            # 记录本次请求
            self.requests[key].append(now)
            return True
            
    def get_wait_time(self, key: str) -> float:
        """获取需要等待的时间(秒)"""
        with self.lock:
            if key not in self.requests or not self.requests[key]:
                return 0
                
            oldest = self.requests[key][0]
            wait_time = oldest + self.window_seconds - time.time()
            return max(0, wait_time)

# 使用示例
limiter = SlidingWindowRateLimiter(max_requests=60, window_seconds=60)  # 60次/分钟

def execute_with_rate_limit(sql: str):
    if not limiter.is_allowed("user_123"):
        wait = limiter.get_wait_time("user_123")
        raise RateLimitExceeded(f"Rate limit exceeded. Retry in {wait:.1f}s")
    return execute(sql)
```

### 7. 熔断器模式

```python
import time
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"      # 正常
    OPEN = "open"          # 熔断
    HALF_OPEN = "half_open"  # 半开

class CircuitBreaker:
    """熔断器 - 保护数据库不被过载"""
    
    def __init__(
        self,
        failure_threshold: int = 5,      # 失败多少次后熔断
        timeout_seconds: int = 60,        # 熔断多久后尝试恢复
        success_threshold: int = 2       # 半开后成功多少次恢复
    ):
        self.failure_threshold = failure_threshold
        self.timeout_seconds = timeout_seconds
        self.success_threshold = success_threshold
        
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        
    def call(self, func, *args, **kwargs):
        """执行函数，带熔断保护"""
        
        # 检查熔断状态
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.timeout_seconds:
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
            
    def _on_success(self):
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
                self.success_count = 0
        else:
            self.failure_count = 0
            
    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
```

### 8. 行级权限实现

```python
class RowLevelSecurity:
    """行级权限控制"""
    
    def __init__(self, user_context_provider):
        self.get_user_context = user_context_provider
        
    def add_row_filter(self, sql: str, user_id: str, table: str) -> str:
        """为SQL添加行级过滤条件"""
        
        # 获取用户的行级权限规则
        rules = self._get_user_row_rules(user_id, table)
        
        if not rules:
            return sql  # 无规则，原样返回
            
        # 构建过滤条件
        conditions = []
        for rule in rules:
            field = rule['field']
            value = rule['value']
            operator = rule.get('operator', '=')
            conditions.append(f"{field} {operator} '{value}'")
        
        filter_clause = " AND ".join(conditions)
        
        # 将过滤条件添加到WHERE或创建子查询
        if 'WHERE' in sql.upper():
            # 假设只有一个WHERE
            sql = sql.replace('WHERE', f'WHERE ({filter_clause}) AND', 1)
        else:
            # 无WHERE，添加到末尾
            sql = f"{sql} WHERE {filter_clause}"
            
        return sql
        
    def _get_user_row_rules(self, user_id: str, table: str) -> list:
        """获取用户的行级权限规则"""
        # 从配置/数据库获取
        # 这里简化实现
        rules_map = {
            'sales': {
                'user_001': [{'field': 'region', 'value': '华北'}],
                'user_002': [{'field': 'region', 'value': '华东'}],
            }
        }
        return rules_map.get(table, {}).get(user_id, [])
```

### 9. 查询执行监控

```python
import time
import logging
from functools import wraps

logger = logging.getLogger(__name__)

# 慢查询阈值配置
SLOW_QUERY_THRESHOLD_SECONDS = 5.0

def execute_with_monitoring(sql: str, conn):
    """执行SQL并监控"""
    
    start_time = time.time()
    row_count = 0
    error = None
    
    try:
        result = conn.execute(text(sql))
        rows = result.fetchall()
        row_count = len(rows)
        duration = time.time() - start_time
        
        # 记录慢查询
        if duration > SLOW_QUERY_THRESHOLD_SECONDS:
            logger.warning(
                f"SLOW_QUERY: duration={duration:.2f}s, rows={row_count}, "
                f"sql={sql[:200]}"
            )
            
        # 记录执行统计
        logger.info(
            f"QUERY_EXEC: duration={duration:.3f}s, rows={row_count}"
        )
        
        return rows
        
    except Exception as e:
        duration = time.time() - start_time
        error = str(e)
        logger.error(
            f"QUERY_ERROR: duration={duration:.2f}s, error={error}, "
            f"sql={sql[:200]}"
        )
        raise
```

### 10. 实战：完整查询执行器

```python
class QueryExecutor:
    """完整的查询执行器"""
    
    def __init__(
        self,
        db_url: str,
        redis_url: str = None,
        rate_limit: tuple = (60, 60),  # 60次/分钟
        query_timeout: int = 30,
        circuit_breaker: dict = None
    ):
        # 连接池
        self.engine = create_engine(
            db_url,
            poolclass=QueuePool,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True
        )
        
        # 缓存
        self.cache = QueryCache(redis_url) if redis_url else None
        
        # 限流
        self.rate_limiter = SlidingWindowRateLimiter(*rate_limit)
        
        # 超时
        self.query_timeout = query_timeout
        
        # 熔断
        if circuit_breaker:
            self.circuit_breaker = CircuitBreaker(**circuit_breaker)
        else:
            self.circuit_breaker = None
            
        # 行级权限
        self.row_security = RowLevelSecurity(self._get_user_context)
        
    def execute(
        self,
        sql: str,
        user_id: str,
        params: dict = None,
        bypass_cache: bool = False
    ) -> dict:
        """执行查询"""
        
        # 1. 限流检查
        if not self.rate_limiter.is_allowed(user_id):
            return {'success': False, 'error': 'rate_limit_exceeded'}
            
        # 2. 缓存检查
        if not bypass_cache and self.cache:
            cached = self.cache.get(sql, params)
            if cached:
                return {'success': True, 'data': cached, 'cached': True}
                
        # 3. 熔断检查
        if self.circuit_breaker:
            if self.circuit_breaker.state == CircuitState.OPEN:
                return {'success': False, 'error': 'service_unavailable'}
                
        # 4. 添加行级权限
        sql = self.row_security.add_row_filter(sql, user_id, self._detect_table(sql))
        
        # 5. 执行查询
        try:
            with self.engine.connect() as conn:
                result = self.execute_with_monitoring(sql, conn)
                
            # 6. 写入缓存
            if self.cache and result.get('success'):
                self.cache.set(sql, result['data'], params)
                
            return result
            
        except QueryTimeout:
            return {'success': False, 'error': 'query_timeout'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
```

---

**下一步**: 探索组件4「结果解释与NLG」
