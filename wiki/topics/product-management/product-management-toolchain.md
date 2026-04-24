# 工具链与集成

> 产品管理方案的技术实现与工具集成
> 维护者：Tony Stark
> 最后更新：2026-04-13

---

## 🛠️ 工具链概览

```
┌─────────────────────────────────────────────────────────┐
│                      用户交互层                          │
│  - 飞书多维表格 (需求协作)                               │
│  - Wiki 文档 (知识沉淀)                                   │
│  - AI 问答服务 (智能查询)                                 │
├─────────────────────────────────────────────────────────┤
│                      服务层                              │
│  - Python AI Service (FastAPI)                           │
│  - Neo4j 图数据库                                        │
│  - 飞书开放平台 API                                      │
├─────────────────────────────────────────────────────────┤
│                      数据层                              │
│  - Neo4j: 产品层级结构 (Domain/Epic/Feature/Story)       │
│  - 飞书多维表格: 需求状态与协作                          │
│  - 本地文档: PRD、设计稿、代码                            │
└─────────────────────────────────────────────────────────┘
```

---

## 🗄️ Neo4j 图数据库

### 数据模型

```
(ProductDomain)-[:HAS_EPIC]->(Epic)-[:HAS_FEATURE]->(Feature)-[:HAS_STORY]->(Story)
```

### 节点类型

| 节点类型 | 说明 | 示例 |
|----------|------|------|
| ProductDomain | 产品域 | 数据工厂、营销增长、合规风控 |
| Epic | 史诗/业务模块 | 数据资产字典、客群中心 |
| Feature | 功能模块 | 资产列表、客群创建向导 |
| Story | 用户故事 | 资产列表页、创建表单 |

### 核心属性

```cypher
// Epic 节点属性
{
  id: "EPIC-DFD_DATA_ASSET",
  label: "数据资产字典",
  description: "管理数据资产的元信息和生命周期",
  status: "进行中",
  priority: "P0",
  productDomain: "数据工厂"
}

// Story 节点属性
{
  id: "STORY-ASSET_LIST_PAGE",
  label: "资产列表页",
  description: "作为数据管理员，我想要查看所有数据资产列表",
  acceptanceCriteria: [
    "功能可正常使用",
    "相关操作正常",
    "数据准确完整",
    "交互符合预期"
  ],
  status: "已完成",
  storyPoints: 5
}
```

### 连接配置

```yaml
# Neo4j 配置
uri: bolt://localhost:7687
username: neo4j
password: password123

# 当前数据统计
ProductDomain: 6 个
Epic: 23 个
Feature: 89 个
Story: 263 个
```

---

## 🤖 AI 问答服务

### 服务架构

```python
# AI Service (FastAPI)
├── main.py              # FastAPI 应用入口
├── ai_service.py        # AI 问答核心逻辑
├── neo4j_client.py      # Neo4j 数据库客户端
├── rag_engine.py        # RAG 检索增强
└── tony_integration.py  # Tony Stark 集成
```

### 核心功能

| 功能 | 说明 | 示例查询 |
|------|------|----------|
| 产品域查询 | 列出所有产品域 | "产品域有哪些？" |
| Epic 查询 | 查询特定产品域的 Epic | "数字风险有哪些 Epic？" |
| Feature 列表 | 列出所有 Feature | "Feature 列表" |
| Story 列表 | 列出所有 Story | "Story 列表" |
| 层级结构 | 查询完整层级 | "数据资产字典的层级结构" |

### API 接口

```python
# 查询接口
POST /api/v1/ai/query
{
  "question": "数字风险有哪些 Epic？"
}

# 返回格式
{
  "answer": "数字风险（ProductDomain: PD-RISK）包含以下 Epic：...",
  "sources": [
    {"type": "Epic", "id": "EPIC-RISK-EXT", "title": "外部数据管理"}
  ],
  "suggestions": ["还有哪些 Feature？", "Story 有哪些？"]
}
```

### 启动方式

```bash
# 启动 AI 服务
cd /Users/wenbo/Documents/project/product_managment/backend-python
python3 ai_service.py

# 服务地址
http://localhost:8081

# 健康检查
curl http://localhost:8081/api/v1/ai/health
```

---

## 📊 飞书多维表格集成

### 表格结构

| App Token | 表格名称 | Table ID | 对应 Epic |
|:---|:---|:---|:---|
| ANhxbU3MDabWsysyeI8c4t0mnfe | Epic拆解确认-数据资产运营工具 | `tblrOKvY8x39AJxt` | EPIC-DFD_ASSET_OPERATE_TOOL |
| ANhxbU3MDabWsysyeI8c4t0mnfe | Epic拆解确认-数据资产字典 | `tbl0n8z93NuvGdpQ` | EPIC-DFD_DATA_ASSET |
| ANhxbU3MDabWsysyeI8c4t0mnfe | Epic拆解确认-数据要素字典 | `tblGZFkU1sODy0cp` | EPIC-DFD_DATA_ELEMENT |
| ANhxbU3MDabWsysyeI8c4t0mnfe | 客群中心需求拆解确认 | `tbltPK5MUVbaZhle` | EPIC-MKT_CROWD_CENTER |
| ANhxbU3MDabWsysyeI8c4t0mnfe | Epic 列表 | `tblW7i7YkT43oseM` | 所有 Epic |
| ANhxbU3MDabWsysyeI8c9f5f3aaee | Feature 列表 | `tblu5ICgSqW0HBoE` | 所有 Feature |

### 表格字段

```yaml
# Story 拆解确认表字段
- Story编号: 唯一标识
- Story名称: 简短描述
- 所属Feature: 关联的Feature
- 所属Epic: 关联的Epic
- 需求描述: 详细描述
- 验收标准: 4项标准
  - 功能可正常使用
  - 相关操作正常
  - 数据准确完整
  - 交互符合预期
- 状态: 待办/进行中/已完成
- 优先级: P0/P1/P2/P3
- 负责人: 开发负责人
- 备注: 其他信息
```

### 同步流程

```
┌─────────────────────────────────────────────────────────┐
│ Step 1: Neo4j 数据准备                                    │
│ - 确认 Epic/Feature/Story 结构完整                      │
│ - 验证所有节点属性完整                                    │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│ Step 2: 飞书表格创建                                      │
│ - 使用飞书 API 创建多维表格                              │
│ - 设置表格字段和格式                                      │
│ - 获取表格 token 和 ID                                    │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│ Step 3: 数据同步                                          │
│ - 从 Neo4j 读取 Story 数据                               │
│ - 批量写入飞书表格                                        │
│ - 验证数据完整性                                          │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│ Step 4: 链接生成与分发                                    │
│ - 生成表格分享链接                                        │
│ - 记录到 HEARTBEAT.md                                    │
│ - 通知相关协作方                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 本地开发环境

### 项目路径

```
/Users/wenbo/Documents/project/product_managment/
├── backend-python/           # Python AI 服务
│   ├── ai_service.py        # FastAPI 服务
│   ├── neo4j_client.py      # Neo4j 客户端
│   ├── tony_integration.py  # Tony Stark 集成
│   └── requirements.txt     # 依赖包
├── docs/                     # 文档
└── scripts/                  # 脚本工具
```

### 关键配置

```yaml
# Neo4j 配置
NEO4J_URI: bolt://localhost:7687
NEO4J_USER: neo4j
NEO4J_PASSWORD: password123

# AI 服务
AI_SERVICE_PORT: 8081
AI_SERVICE_HOST: localhost

# 飞书
FEISHU_APP_TOKEN: ANhxbU3MDabWsysyeI8c4t0mnfe
```

---

## 📚 关联内容

- [[product-management-ontology|本体论设计]] - 知识图谱 Schema 详解
- [[product-management-cases|实践案例]] - 具体 Epic 拆解案例
- [[concepts/llm-agent|LLM Agent]] - AI 拆解技术基础
- [[concepts/rag|RAG]] - 检索增强生成技术
- [[topics/ai-native/agent-engineering|Agent 工程]] - Agent 开发最佳实践

---

*"数据驱动 + 智能拆解 = 高效产品管理"*
*—— Tony Stark*
