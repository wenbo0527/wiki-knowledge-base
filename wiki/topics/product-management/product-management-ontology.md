# 本体论设计

> 产品管理方案的知识图谱 Schema 与术语体系
> 维护者：Tony Stark
> 最后更新：2026-04-13

---

## 🎯 本体论目标

1. **统一术语**：建立产品管理领域的标准化术语体系
2. **知识结构化**：将产品知识组织为可查询、可推理的结构
3. **支持智能查询**：为 AI 问答提供语义基础
4. **促进协作**：统一团队语言，降低沟通成本

---

## 📐 核心实体类型

### 1. ProductDomain（产品域）

**定义**：产品的高层级分类，代表一个完整的业务领域

**属性**：
```cypher
(ProductDomain {
  id: "PD-{DOMAIN_CODE}",
  label: "产品域名称",
  description: "产品域描述",
  businessUnit: "所属业务单元",
  owner: "产品负责人",
  status: "活跃/下线/规划中"
})
```

**示例**：
- `PD-DATA` - 数据工厂
- `PD-MKT` - 营销增长
- `PD-RISK` - 合规风控

### 2. Epic（史诗）

**定义**：产品域下的业务模块，代表一个可独立交付的价值单元

**属性**：
```cypher
(Epic {
  id: "EPIC-{DOMAIN}_{MODULE}",
  label: "Epic 名称",
  description: "Epic 描述",
  status: "待办/进行中/已完成",
  priority: "P0/P1/P2/P3",
  productDomain: "所属产品域",
  completionRate: 0.75,  // 完成度百分比
  startDate: "2026-03-01",
  targetDate: "2026-06-30"
})
```

**示例**：
- `EPIC-DFD_DATA_ASSET` - 数据资产字典
- `EPIC-MKT_CROWD_CENTER` - 客群中心

### 3. Feature（功能）

**定义**：Epic 下的功能模块，代表一个内聚的功能单元

**属性**：
```cypher
(Feature {
  id: "FEATURE-{EPIC}_{FUNCTION}",
  label: "Feature 名称",
  description: "Feature 描述",
  status: "待办/进行中/已完成",
  priority: "P0/P1/P2/P3",
  epic: "所属 Epic",
  storyCount: 5,  // 包含的 Story 数量
  techStack: ["React", "Node.js", "MySQL"]
})
```

**示例**：
- `FEATURE-DFD_ASSET_OPERATE_DASHBOARD` - 资产运营工作台
- `FEATURE-MKT_CROWD_CREATE` - 客群创建向导

### 4. Story（用户故事）

**定义**：用户可感知的完整功能点，代表一个可独立交付的用户价值

**属性**：
```cypher
(Story {
  id: "STORY-{FEATURE}_{ACTION}",
  label: "Story 名称",
  description: "作为[角色]，我想要[功能]，以便[价值]",
  acceptanceCriteria: [
    "功能可正常使用",
    "相关操作正常",
    "数据准确完整",
    "交互符合预期"
  ],
  status: "待办/进行中/已完成",
  priority: "P0/P1/P2/P3",
  feature: "所属 Feature",
  storyPoints: 5,  // 故事点
  assignee: "负责人",
  feishuUrl: "飞书表格行链接"
})
```

**示例**：
- `STORY-ASSET_LIST_PAGE` - 资产列表页
- `STORY-CROWD_CREATE_WIZARD` - 客群创建向导

---

## 🔗 关系类型

### 1. 层级关系

```cypher
// ProductDomain 包含 Epic
(ProductDomain)-[:HAS_EPIC]->(Epic)

// Epic 包含 Feature
(Epic)-[:HAS_FEATURE]->(Feature)

// Feature 包含 Story
(Feature)-[:HAS_STORY]->(Story)
```

### 2. 依赖关系

```cypher
// Story 依赖其他 Story
(Story)-[:DEPENDS_ON]->(Story)

// Feature 依赖其他 Feature
(Feature)-[:DEPENDS_ON]->(Feature)
```

### 3. 关联关系

```cypher
// Story 关联代码实现
(Story)-[:IMPLEMENTED_BY]->(CodeModule)

// Story 关联飞书表格行
(Story)-[:SYNCED_TO]->(FeishuRecord)
```

---

## 📝 术语词典

### 产品域术语

| 术语 | 英文 | 定义 | 示例 |
|------|------|------|------|
| 产品域 | Product Domain | 产品的高层级分类，代表一个完整的业务领域 | 数据工厂、营销增长 |
| Epic | Epic | 产品域下的业务模块，代表一个可独立交付的价值单元 | 数据资产字典、客群中心 |
| Feature | Feature | Epic 下的功能模块，代表一个内聚的功能单元 | 资产列表、客群创建向导 |
| Story | User Story | 用户可感知的完整功能点，代表一个可独立交付的用户价值 | 作为管理员，我想要查看资产列表 |
| 故事点 | Story Point | 相对估算单位，表示完成 Story 所需的工作量 | 1, 2, 3, 5, 8, 13 |
| 验收标准 | Acceptance Criteria | Story 完成必须满足的条件 | 功能正常、操作正常、数据准确、交互符合预期 |

### 技术术语

| 术语 | 英文 | 定义 | 关联技术 |
|------|------|------|----------|
| 图数据库 | Graph Database | 以图结构存储数据的数据库 | Neo4j |
| 本体论 | Ontology | 领域知识的正式、明确的规范 | OWL, RDF |
| 知识图谱 | Knowledge Graph | 结构化的语义知识库 | Neo4j + RDF |
| RAG | Retrieval-Augmented Generation | 检索增强生成技术 | LLM + 向量检索 |
| 向量数据库 | Vector Database | 存储向量嵌入的数据库 | 待集成 |

---

## 🔍 Cypher 查询示例

### 1. 查询产品域下的所有 Epic

```cypher
MATCH (pd:ProductDomain {id: "PD-DATA"})-[:HAS_EPIC]->(e:Epic)
RETURN e.id, e.label, e.status, e.completionRate
ORDER BY e.priority
```

### 2. 查询 Epic 的完整层级结构

```cypher
MATCH (e:Epic {id: "EPIC-DFD_DATA_ASSET"})-[:HAS_FEATURE]->(f:Feature)-[:HAS_STORY]->(s:Story)
RETURN e.label as Epic, 
       f.label as Feature, 
       s.label as Story,
       s.status as Status
ORDER BY f.id, s.id
```

### 3. 统计 Epic 的完成度

```cypher
MATCH (e:Epic)-[:HAS_FEATURE]->(f:Feature)-[:HAS_STORY]->(s:Story)
WITH e, 
     count(s) as totalStories,
     count(CASE WHEN s.status = "已完成" THEN 1 END) as completedStories
RETURN e.label as Epic,
       totalStories,
       completedStories,
       round(100.0 * completedStories / totalStories, 2) as completionRate
ORDER BY completionRate DESC
```

### 4. 查询待办的 Story

```cypher
MATCH (s:Story {status: "待办"})<-[:HAS_STORY]-(f:Feature)<-[:HAS_FEATURE]-(e:Epic)
RETURN e.label as Epic,
       f.label as Feature,
       s.label as Story,
       s.priority as Priority
ORDER BY s.priority, e.id
```

---

## 🔗 关联内容

- [[product-management-methodology|产品管理方法论]] - 四层架构详解
- [[product-management-toolchain|工具链与集成]] - 技术实现细节
- [[topics/fintech/data-platform|数据中台]] - 数据中台实践参考
- [[concepts/llm-agent|LLM Agent]] - AI 拆解技术基础

---

*"每个 Epic 拆解都是一次产品设计的练习，把复杂的业务需求转化为可执行的用户故事。"*
*—— Tony Stark*
