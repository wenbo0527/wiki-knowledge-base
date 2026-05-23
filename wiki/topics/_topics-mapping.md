# Topics → 6大能力 映射规则

> 版本: v1.0
> 创建: 2026-05-12
> 说明: 所有Topics必须归入6大能力之一

---

## 6大能力

| 能力 | 说明 |
|:---|:---|
| **技术理解** | 能不能做 |
| **需求决策** | 该不该做 |
| **产品设计** | 怎么做 |
| **数据驱动** | 如何闭环 |
| **价值闭环** | 如何衡量 |
| **风险防控** | 如何控制 |

---

## Topics映射表

| Topic | → 能力 | 理由 |
|:---|:---|:---|
| **ai-agent** | 技术理解 | Agent技术选型/架构 |
| **ai-native** | 技术理解 | AI原生技术认知 |
| **ai-programming** | 技术理解 | AI编程工具/方法 |
| **ai-data-query** | 产品设计 | AI数据产品设计 |
| **ai-enterprise-implementation** | 价值闭环 | AI落地/ROI |
| **product-management** | 需求决策 | 需求优先级/PRD |
| **data-driven** 🆕 | 数据驱动 | AB实验/因果推断/指标体系 |
| **fintech** | 数据驱动 | 数据治理/指标体系 |
| **analysis-frameworks** | 需求决策 | 分析框架/决策方法 |
| **algorithms** | 技术理解 | 算法原理 |
| **knowledge-management** | 价值闭环 | 知识价值衡量 |
| **information-collection** | 需求决策 | 信息收集服务于决策 |
| **palantir-ontology** | 数据驱动 | 本体工程/数据建模 |

---

## 映射规则

### 技术理解
```
ai-agent / ai-native / ai-programming / algorithms
```

### 需求决策
```
product-management / analysis-frameworks / information-collection
```

### 产品设计
```
ai-data-query
```

### 数据驱动
```
data-driven / fintech / palantir-ontology
```

### 价值闭环
```
ai-enterprise-implementation / knowledge-management
```

### 风险防控
```
（暂无独立Topic，可归入ai-native或fintech）
```

---

## 新增Topics建议

| Topic | → 能力 | 说明 |
|:---|:---|:---|
| **data-engineering** | 技术理解 | 数仓/Hive/Spark/Flink |
| **risk-compliance** | 风险防控 | 合规/伦理/风控 |

---

## 检验清单

```
新Topic到达
    │
    ▼
这个Topic属于哪个能力？
    │
    ├─ 技术理解 → ai-agent/ai-native/ai-programming/algorithms
    ├─ 需求决策 → product-management/analysis-frameworks/information-collection
    ├─ 产品设计 → ai-data-query
    ├─ 数据驱动 → fintech/palantir-ontology
    ├─ 价值闭环 → ai-enterprise-implementation/knowledge-management
    └─ 风险防控 → （需要新建或归入其他）
```

---

*最后更新：2026-05-12*
*版本：v1.0*
