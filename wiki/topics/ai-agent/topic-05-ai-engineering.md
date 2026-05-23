# AI 产品工程化与稳定性治理

> Topic: AI工程化治理 | 模块五
> 标签：工程化 / 稳定性治理 / 幻觉处理 / 限流熔断
> 状态：已完善

---

## 一、幻觉处理与溯源机制

### 1.1 幻觉三大类型

| 类型 | 本质 | 表现 | 典型案例 |
|:---|:---|:---|:---|
| **知识幻觉** | 知识库无据可查 | 模型编造不存在的知识 | "根据XX文件显示..."（文件不存在） |
| **逻辑幻觉** | 推理过程错误 | 看似合理但逻辑不通 | 数字计算错误、因果倒置 |
| **数值幻觉** | 数字/日期偏差 | 数值与真实不符 | "2025年"说成"2024年"，"100万"说成"90万" |

### 1.2 幻觉治理手段

```
┌─────────────────────────────────────────────────────────────────────┐
│                      幻觉治理体系                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │                    三层治理手段                              │   │
│  ├────────────────────────────────────────────────────────────┤   │
│  │                                                              │   │
│  │  第一层：引文透出                                            │   │
│  │  ├── 要求模型回答时必须引用知识库来源                        │   │
│  │  ├── 格式：[来源：文件名/段落]                              │   │
│  │  └── 效果：可追溯、可核实                                    │   │
│  │                                                              │   │
│  │  第二层：无来源标识                                          │   │
│  │  ├── 知识库无据可查时，明确标注「模型基于常识生成」          │   │
│  │  ├── 输出时加置信度标记（如：⚠️ 低置信度）                 │   │
│  │  └── 效果：用户可识别，不可直接引用                          │   │
│  │                                                              │   │
│  │  第三层：置信度分级                                          │   │
│  │  ├── 🟢 高置信度：知识库有据、逻辑清晰                       │   │
│  │  ├── 🟡 中置信度：知识库部分匹配、逻辑可疑                   │   │
│  │  └── 🔴 低置信度：知识库无据、逻辑存疑                       │   │
│  │                                                              │   │
│  └────────────────────────────────────────────────────────────┘   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.3 溯源机制设计

```python
class CitationTracker:
    """引文透出追踪器"""
    
    def generate_answer(self, query, retrieved_docs):
        # 1. 筛选有据可查的文档
        supported_docs = [doc for doc in retrieved_docs if doc.has_citation]
        
        # 2. 无据可查时明确标注
        if not supported_docs:
            confidence = "low"
            disclaimer = "⚠️ 以下内容为模型基于常识生成，请核实"
        else:
            confidence = "high"
            disclaimer = None
        
        # 3. 生成带引用的回答
        answer = self.build_answer_with_citations(query, supported_docs)
        
        return Answer(
            content=answer,
            confidence=confidence,
            citations=self.extract_citations(supported_docs),
            disclaimer=disclaimer
        )
```

---

## 二、限流、熔断与降级

### 2.1 三层防护体系

```
┌─────────────────────────────────────────────────────────────────────┐
│                    三层防护体系                                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│                        用户请求                                      │
│                            │                                        │
│                            ▼                                        │
│                   ┌─────────────────┐                               │
│                   │     限流层       │  ← 第一节：流量控制           │
│                   │  并发数 / Token  │                               │
│                   └────────┬────────┘                               │
│                            │                                        │
│            ┌───────────────┼───────────────┐                        │
│            │               │               │                        │
│            ▼               ▼               ▼                        │
│      ┌───────────┐  ┌───────────┐  ┌───────────┐                  │
│      │ 正常处理   │  │  排队等待   │  │   拒绝    │                  │
│      └───────────┘  └───────────┘  └───────────┘                  │
│                            │                                        │
│                            ▼                                        │
│                   ┌─────────────────┐                               │
│                   │     熔断层       │  ← 第二节：故障隔离           │
│                   │  错误率 / 超时   │                               │
│                   └────────┬────────┘                               │
│                            │                                        │
│                            ▼                                        │
│                   ┌─────────────────┐                               │
│                   │     降级层       │  ← 第三节：功能简化           │
│                   │  缓存 / 默认值   │                               │
│                   └─────────────────┘                               │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 限流策略

| 策略 | 说明 | 配置参数 | 适用场景 |
|:---|:---|:---|:---|
| **并发数限流** | 同时处理的最大请求数 | `max_concurrent` | 资源有限场景 |
| **Token 配额** | 单位时间的 Token 消耗上限 | `tokens_per_minute` | 成本控制场景 |
| **请求频率限流** | 单位时间的请求次数 | `requests_per_second` | API 限流场景 |
| **排队限流** | 请求排队，超时拒绝 | `queue_size`, `timeout` | 削峰填谷场景 |

```yaml
# 限流配置示例
rate_limit:
  global:
    max_concurrent: 100
    tokens_per_minute: 100000
  
  per_user:
    max_concurrent: 5
    requests_per_minute: 30
  
  per_api_key:
    max_concurrent: 20
    tokens_per_minute: 50000
```

### 2.3 熔断策略

| 策略 | 说明 | 触发条件 | 恢复条件 |
|:---|:---|:---|:---|
| **错误率熔断** | 错误率过高时切断 | 5分钟内错误率>50% | 10秒后半量恢复试探 |
| **超时熔断** | 响应超时时切断 | 超时率>30% | 超时减少后恢复 |
| **资源熔断** | 系统资源不足时切断 | CPU>90%, 内存>85% | 资源降级后恢复 |

```python
class CircuitBreaker:
    def __init__(self):
        self.state = "closed"  # closed, open, half_open
        self.failure_count = 0
        self.success_count = 0
    
    def call(self, func):
        if self.state == "open":
            raise CircuitOpenException()
        
        try:
            result = func()
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise
    
    def on_failure(self):
        self.failure_count += 1
        if self.failure_count > self.threshold:
            self.state = "open"
    
    def on_success(self):
        self.failure_count = 0
        self.state = "closed"
```

### 2.4 降级策略

| 降级类型 | 说明 | 实现方式 | 效果 |
|:---|:---|:---|:---|
| **功能降级** | 关闭非核心功能 | 开关控制 | 保持核心能力 |
| **精度降级** | 使用更小模型 | 模型切换 | 降低质量保能力 |
| **缓存降级** | 返回缓存数据 | 缓存读取 | 返回可能过期数据 |
| **默认回答** | 返回预设回答 | 兜底 Prompt | 保证可回答 |

```yaml
# 降级配置示例
degradation:
  strategy: "cascade"
  
  levels:
    - name: "full"
      model: "gpt-4"
      enabled: true
    
    - name: "balanced"
      model: "gpt-3.5-turbo"
      trigger: "latency > 5s OR error_rate > 10%"
    
    - name: "cache"
      use_cache: true
      trigger: "latency > 10s OR error_rate > 30%"
    
    - name: "fallback"
      response: "系统繁忙，请稍后再试"
      trigger: "model_unavailable"
```

---

## 三、缓存机制

### 3.1 缓存类型

| 类型 | 说明 | TTL | 适用场景 |
|:---|:---|:---|:---|
| **会话缓存** | 多轮对话上下文复用 | 会话周期 | 同一会话的上下文 |
| **语义缓存** | 相似问题复用回答 | 1-24h | 重复问题、FAQ |
| **冷启动缓存** | 预热常用场景 | 长期 | 热门问题预加载 |
| **热数据缓存** | 保持热点数据 | 分钟级 | 高频访问知识 |

### 3.2 语义缓存设计

```python
class SemanticCache:
    def __init__(self, embedding_model, threshold=0.95):
        self.embedding_model = embedding_model
        self.threshold = threshold  # 相似度阈值
        self.cache = {}  # {query_embedding: answer}
    
    def get(self, query):
        """语义缓存查询"""
        query_emb = self.embedding_model.encode(query)
        
        for cached_emb, answer in self.cache.items():
            similarity = cosine_similarity(query_emb, cached_emb)
            if similarity >= self.threshold:
                return CacheHit(answer=answer, similarity=similarity)
        
        return CacheMiss()
    
    def set(self, query, answer):
        """写入缓存"""
        query_emb = self.embedding_model.encode(query)
        self.cache[query_emb] = answer
```

### 3.3 缓存策略配置

```yaml
cache:
  semantic:
    enabled: true
    threshold: 0.95
    max_size: 10000
    ttl: 86400  # 24小时
  
  session:
    enabled: true
    max_context_tokens: 100000
  
  warmup:
    enabled: true
    # 预热场景
    scenarios:
      - "热门产品FAQ"
      - "常见技术问题"
      - "标准流程查询"
```

---

## 四、灰度发布

### 4.1 灰度维度

| 维度 | 说明 | 示例 |
|:---|:---|:---|
| **用户维度** | 按用户 ID 分批 | VIP 用户先行 |
| **部门维度** | 按部门分批 | 技术部先行 |
| **场景维度** | 按使用场景分批 | 简单场景先行 |
| **版本维度** | 按模型版本分批 | 新版本小流量 |

### 4.2 灰度策略

```
┌─────────────────────────────────────────────────────────────────────┐
│                      灰度发布策略                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  阶段1：小流量验证（5%）                                            │
│  ├── 目标：验证基础功能正常                                        │
│  ├── 监控：错误率、基础指标                                        │
│  └── 判断：稳定则进入下一阶段，否则回滚                            │
│                                                                      │
│  阶段2：扩量验证（20%）                                            │
│  ├── 目标：验证性能、稳定性                                        │
│  ├── 监控：延迟、吞吐、资源使用                                    │
│  └── 判断：稳定则进入下一阶段，否则回滚                            │
│                                                                      │
│  阶段3：扩量验证（50%）                                            │
│  ├── 目标：验证全量功能                                            │
│  ├── 监控：业务指标、用户反馈                                      │
│  └── 判断：稳定则全量，否则回滚                                    │
│                                                                      │
│  阶段4：全量发布（100%）                                           │
│  └── 监控：持续监控，及时发现问题                                  │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 4.3 灰度配置

```yaml
# 灰度配置示例
gradual_rollout:
  enabled: true
  
  stages:
    - name: "canary"
      percentage: 5
      duration: "2h"
      criteria:
        error_rate: < 1%
        p99_latency: < 3000ms
        user_satisfaction: > 4.0
    
    - name: "expand_20"
      percentage: 20
      duration: "4h"
      criteria:
        error_rate: < 0.5%
        p99_latency: < 2000ms
    
    - name: "expand_50"
      percentage: 50
      duration: "8h"
      criteria:
        error_rate: < 0.3%
    
    - name: "full"
      percentage: 100
      criteria:
        error_rate: < 0.1%

# A/B 测试配置
ab_test:
  enabled: true
  
  experiments:
    - name: "new_rerank_model"
      variants:
        control: 50
        treatment: 50
      metrics:
        - recall_rate
        - user_satisfaction
```

---

## 五、模型成本治理

### 5.1 分层降本架构

```
┌─────────────────────────────────────────────────────────────────────┐
│                      分层降本架构                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  用户输入                                                            │
│      │                                                              │
│      ▼                                                              │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │ L1：小模型/Embedding 层（省钱）                           │   │
│  │                                                            │   │
│  │ 用途：                                                      │   │
│  │ • 意图分类（简单规则即可）                                 │   │
│  │ • 知识召回（Embedding 向量检索）                           │   │
│  │ • 初步过滤（无关问题直接拒绝）                             │   │
│  │                                                            │   │
│  │ 成本：$0.001-0.01 / 1000 Token                            │   │
│  └────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │ L2：知识召回层（精准）                                      │   │
│  │                                                            │   │
│  │ 用途：                                                      │   │
│  │ • 多路召回（BM25 + 向量）                                  │   │
│  │ • Rerank 重排                                              │   │
│  │                                                            │   │
│  │ 成本：向量数据库成本（极低）                               │   │
│  └────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │ L3：大模型生成层（质量）                                   │   │
│  │                                                            │   │
│  │ 用途：                                                      │   │
│  │ • 最终回答生成                                             │   │
│  │ • 复杂推理                                                 │   │
│  │                                                            │   │
│  │ 成本：$0.01-0.1 / 1000 Token（最高）                      │   │
│  └────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  节省比例：60-80%                                                   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 5.2 成本控制策略

| 策略 | 说明 | 节省比例 |
|:---|:---|:---|
| **小模型前置** | 用小模型做意图分类、路由 | 30-50% |
| **语义缓存** | 相似问题直接返回缓存 | 40-60% |
| **上下文压缩** | 压缩输入上下文长度 | 20-40% |
| **精简输出** | 限制输出长度 | 10-20% |
| **模型降级** | 简单问题用小模型 | 30-50% |

```yaml
# 成本控制配置
cost_control:
  intent_classification:
    model: "embedding-small"  # 小模型做分类
    fallback_model: "gpt-3.5-turbo"
  
  response_generation:
    simple_query:
      model: "gpt-3.5-turbo"  # 简单问题用小模型
    complex_query:
      model: "gpt-4"  # 复杂问题用大模型
  
  cache:
    enabled: true
    hit_rate_target: 0.4  # 40% 命中目标
  
  context:
    max_tokens: 8000
    compression_threshold: 0.6  # 超过 60% 窗口时压缩
```

---

## 六、相关文档

- [Agent 架构设计](./topic-02-agent-architecture.md)
- [RAG 全链路架构](./topic-03-rag-architecture.md)
- [多 Agent 协作](./topic-04-multi-agent.md)
- [企业 Agent 平台](./topic-06-enterprise-agent.md)

---

标签：工程化 / 稳定性治理 / 幻觉处理 / 限流熔断
归档：topics/ai-agent/
