# EPIC-DFD_DATA_ASSET - 数据资产字典

> Epic 级别需求文档 | 产品域：PD-DFD（数据发现）
>
> 维护者：Tony Stark | 创建时间：2026-04-13 | 版本：v1.0

---

## 1. 基本信息

| 属性 | 值 |
|:---|:---|
| **Epic ID** | EPIC-DFD_DATA_ASSET |
| **Epic 名称** | 数据资产字典 |
| **产品域** | PD-DFD（数据发现 / Data Discovery） |
| **状态** | 建设中 |
| **优先级** | P0 |
| **负责人** | 待定 |
| **开始时间** | 2026-Q1 |
| **预计完成** | 2026-Q2 |

---

## 2. 价值主张

### 2.1 核心价值
统一管理数据资产的元信息和生命周期，实现数据资产的可见、可管、可用。

### 2.2 解决的问题
- 数据资产分散，缺乏统一管理视图
- 数据血缘关系不清晰，影响数据追溯
- 资产元信息不完整，影响数据发现和使用
- 资产生命周期管理混乱

### 2.3 预期收益
| 指标 | 基线 | 目标 | 提升 |
|:---|:---:|:---:|:---:|
| 数据资产发现效率 | 2小时 | 10分钟 | **12倍** |
| 数据血缘查询时间 | 30分钟 | 实时 | **即时** |
| 资产元信息完整度 | 40% | 95% | **+55%** |

---

## 3. 功能范围

### 3.1 功能模块拆解

```
EPIC-DFD_DATA_ASSET（数据资产字典）
│
├── FEATURE-DFD_ASSET_METADATA（资产元数据管理）
│   ├── STORY-ASSET_METADATA_MODEL（资产元模型定义）
│   ├── STORY-ASSET_METADATA_COLLECT（元数据采集）
│   ├── STORY-ASSET_METADATA_STORE（元数据存储）
│   └── STORY-ASSET_METADATA_QUERY（元数据查询）
│
├── FEATURE-DFD_ASSET_CATALOG（资产目录管理）
│   ├── STORY-CATALOG_TREE（目录树管理）
│   ├── STORY-CATALOG_CLASSIFY（资产分类）
│   ├── STORY-CATALOG_SEARCH（目录搜索）
│   └── STORY-CATALOG_BROWSE（资产浏览）
│
├── FEATURE-DFD_ASSET_LINEAGE（资产血缘追踪）
│   ├── STORY-LINEAGE_PARSE（血缘解析）
│   ├── STORY-LINEAGE_STORE（血缘存储）
│   ├── STORY-LINEAGE_QUERY（血缘查询）
│   └── STORY-LINEAGE_IMPACT（影响分析）
│
└── FEATURE-DFD_ASSET_LIFECYCLE（资产生命周期）
    ├── STORY-LIFECYCLE_STATE（状态机定义）
    ├── STORY-LIFECYCLE_TRANSITION（状态流转）
    ├── STORY-LIFECYCLE_APPROVAL（审批流程）
    └── STORY-LIFECYCLE_AUDIT（变更审计）
```

### 3.2 功能详细说明

#### 3.2.1 FEATURE-DFD_ASSET_METADATA（资产元数据管理）

**功能描述**：
定义和管理数据资产的元信息模型，支持元信息的采集、存储和查询。

**包含 Story**：

| Story ID | Story 名称 | 描述 | 验收标准 | 故事点 |
|:---|:---|:---|:---|:---:|
| STORY-ASSET_METADATA_MODEL | 资产元模型定义 | 定义数据资产的元信息字段和结构 | 1. 元模型包含：名称、描述、类型、所有者、标签等字段<br>2. 支持自定义字段扩展<br>3. 元模型版本管理 | 5 |
| STORY-ASSET_METADATA_COLLECT | 元数据采集 | 从数据源自动采集资产的元信息 | 1. 支持 JDBC、Hive、Kafka 等数据源<br>2. 支持定时采集和手动触发<br>3. 采集结果可预览和确认 | 8 |
| STORY-ASSET_METADATA_STORE | 元数据存储 | 将采集的元信息持久化存储 | 1. 支持版本历史记录<br>2. 支持变更对比<br>3. 支持批量导入导出 | 5 |
| STORY-ASSET_METADATA_QUERY | 元数据查询 | 提供元信息的检索和查看能力 | 1. 支持多条件组合查询<br>2. 支持全文搜索<br>3. 查询结果支持导出 | 5 |

#### 3.2.2 FEATURE-DFD_ASSET_CATALOG（资产目录管理）

**功能描述**：
提供数据资产的分类目录体系，支持资产的分类组织和目录化浏览。

**包含 Story**：

| Story ID | Story 名称 | 描述 | 验收标准 | 故事点 |
|:---|:---|:---|:---|:---:|
| STORY-CATALOG_TREE | 目录树管理 | 管理资产分类目录的层级结构 | 1. 支持多级目录嵌套<br>2. 支持目录的增删改查<br>3. 支持目录拖拽排序 | 5 |
| STORY-CATALOG_CLASSIFY | 资产分类 | 将资产归属到对应的目录分类 | 1. 支持批量分类<br>2. 支持自动分类规则<br>3. 支持资产的多目录归属 | 5 |
| STORY-CATALOG_SEARCH | 目录搜索 | 在目录范围内搜索资产 | 1. 支持按目录筛选<br>2. 支持目录+关键字组合搜索<br>3. 搜索结果按目录分组 | 3 |
| STORY-CATALOG_BROWSE | 资产浏览 | 以目录视图方式浏览资产 | 1. 支持树形目录导航<br>2. 支持卡片/列表两种展示模式<br>3. 支持资产快捷操作 | 5 |

#### 3.2.3 FEATURE-DFD_ASSET_LINEAGE（资产血缘追踪）

**功能描述**：
追踪和分析数据资产的血缘关系，支持数据流向的追溯和影响分析。

**包含 Story**：

| Story ID | Story 名称 | 描述 | 验收标准 | 故事点 |
|:---|:---|:---|:---|:---:|
| STORY-LINEAGE_PARSE | 血缘解析 | 从 SQL/ETL 脚本中解析血缘关系 | 1. 支持常见 SQL 语句解析<br>2. 支持 ETL 配置解析<br>3. 解析结果准确率达到 95%+ | 13 |
| STORY-LINEAGE_STORE | 血缘存储 | 将解析的血缘关系持久化存储 | 1. 支持血缘版本管理<br>2. 支持增量更新<br>3. 血缘查询性能 < 1s | 8 |
| STORY-LINEAGE_QUERY | 血缘查询 | 提供血缘关系的查询和展示 | 1. 支持上下游血缘追溯<br>2. 支持可视化展示（血缘图）<br>3. 支持导出血缘报告 | 8 |
| STORY-LINEAGE_IMPACT | 影响分析 | 基于血缘进行变更影响分析 | 1. 支持变更影响范围评估<br>2. 支持影响结果导出<br>3. 支持与审批流程联动 | 5 |

#### 3.2.4 FEATURE-DFD_ASSET_LIFECYCLE（资产生命周期）

**功能描述**：
管理数据资产的全生命周期，包括状态流转、审批流程和变更审计。

**包含 Story**：

| Story ID | Story 名称 | 描述 | 验收标准 | 故事点 |
|:---|:---|:---|:---|:---:|
| STORY-LIFECYCLE_STATE | 状态机定义 | 定义资产生命周期的状态和流转规则 | 1. 支持自定义状态定义<br>2. 支持状态流转规则配置<br>3. 支持状态权限控制 | 5 |
| STORY-LIFECYCLE_TRANSITION | 状态流转 | 实现资产的状态变更和流转 | 1. 支持手动状态变更<br>2. 支持自动状态流转<br>3. 状态变更记录完整 | 5 |
| STORY-LIFECYCLE_APPROVAL | 审批流程 | 状态变更的审批流程管理 | 1. 支持自定义审批流程<br>2. 支持多级审批<br>3. 支持审批通知和催办 | 8 |
| STORY-LIFECYCLE_AUDIT | 变更审计 | 资产变更的审计日志记录 | 1. 记录所有变更操作<br>2. 支持变更对比<br>3. 支持审计报告导出 | 5 |

---

## 4. 非功能需求

### 4.1 性能要求

| 指标 | 要求 | 说明 |
|:---|:---:|:---|
| 元数据查询响应时间 | < 500ms | 单条资产元数据查询 |
| 血缘追溯查询时间 | < 2s | 上下游3层血缘查询 |
| 目录树加载时间 | < 1s | 完整目录树加载 |
| 批量导入性能 | > 1000条/分钟 | 资产元数据批量导入 |

### 4.2 可用性要求

| 指标 | 要求 | 说明 |
|:---|:---:|:---|
| 系统可用性 | 99.9% | 年度可用性目标 |
| 故障恢复时间 | < 30分钟 | RTO（恢复时间目标） |
| 数据丢失时间 | < 5分钟 | RPO（恢复点目标） |

### 4.3 安全要求

| 要求 | 说明 |
|:---|:---|
| 数据访问控制 | 基于角色的权限控制，细粒度到字段级别 |
| 操作审计 | 所有数据操作记录审计日志，保留180天 |
| 数据脱敏 | 敏感字段自动脱敏展示，支持自定义脱敏规则 |
| 传输加密 | 所有数据传输使用 TLS 1.2+ 加密 |

---

## 5. 依赖与关联

### 5.1 上游依赖

| 依赖项 | 说明 | 影响 |
|:---|:---|:---|
| PD-DFD 基础数据服务 | 数据资产的元数据采集依赖基础数据服务 | 阻塞 |
| 权限管理中心 | 资产的权限控制依赖统一权限服务 | 阻塞 |
| 消息通知服务 | 审批流程的通知依赖消息服务 | 非阻塞 |

### 5.2 下游依赖

| 依赖项 | 说明 |
|:---|:---|
| PD-MKT 数字营销 | 客群中心依赖数据资产进行人群筛选 |
| PD-RISK 数字风险 | 风控模型依赖资产血缘进行影响分析 |
| PD-DEX 数据探索 | 自助分析依赖资产目录进行数据发现 |

### 5.3 关联 Epic

| Epic ID | 关系 | 说明 |
|:---|:---:|:---|
| EPIC-DFD_DATA_ELEMENT | 依赖 | 数据要素字典依赖资产字典的基础元数据 |
| EPIC-DFD_ASSET_OPERATE_TOOL | 被依赖 | 资产运营工具依赖资产字典的核心能力 |
| EPIC-DFD_DATA_RESOURCE | 关联 | 数据资源与数据资产在业务上有重叠，需明确边界 |

---

## 6. 项目计划

### 6.1 里程碑

| 里程碑 | 时间 | 交付物 | 验收标准 |
|:---|:---:|:---|:---|
| M1 - 元数据管理上线 | 2026-04-30 | FEATURE-DFD_ASSET_METADATA 完整功能 | 所有 Story 验收通过，性能达标 |
| M2 - 资产目录上线 | 2026-05-15 | FEATURE-DFD_ASSET_CATALOG 完整功能 | 目录树管理、资产分类功能可用 |
| M3 - 血缘追踪上线 | 2026-06-15 | FEATURE-DFD_ASSET_LINEAGE 完整功能 | 血缘解析准确率 95%+ |
| M4 - 生命周期上线 | 2026-06-30 | FEATURE-DFD_ASSET_LIFECYCLE 完整功能 | 审批流程完整，审计日志完善 |
| M5 - Epic 完整交付 | 2026-07-15 | 所有 Feature 上线，文档完善 | 所有验收标准达成 |

### 6.2 迭代计划

| 迭代 | 时间 | 范围 | Story 数量 | 故事点 |
|:---:|:---:|:---|:---:|:---:|
| Sprint 1 | 04/13-04/26 | STORY-ASSET_METADATA_MODEL, STORY-ASSET_METADATA_COLLECT | 2 | 13 |
| Sprint 2 | 04/27-05/10 | STORY-ASSET_METADATA_STORE, STORY-ASSET_METADATA_QUERY, STORY-CATALOG_TREE | 3 | 13 |
| Sprint 3 | 05/11-05/24 | STORY-CATALOG_CLASSIFY, STORY-CATALOG_SEARCH, STORY-CATALOG_BROWSE | 3 | 13 |
| Sprint 4 | 05/25-06/07 | STORY-LINEAGE_PARSE, STORY-LINEAGE_STORE | 2 | 21 |
| Sprint 5 | 06/08-06/21 | STORY-LINEAGE_QUERY, STORY-LINEAGE_IMPACT | 2 | 13 |
| Sprint 6 | 06/22-07/05 | STORY-LIFECYCLE_STATE, STORY-LIFECYCLE_TRANSITION, STORY-LIFECYCLE_APPROVAL | 3 | 18 |
| Sprint 7 | 07/06-07/15 | STORY-LIFECYCLE_AUDIT, 整体联调优化 | 2+ | 10+ |

**总计：约 114 故事点，预计 7 个 Sprint（3.5 个月）**

---

## 7. 附录

### 7.1 术语表

| 术语 | 定义 |
|:---|:---|
| 数据资产 | 企业拥有的、具有业务价值的数据资源，包括数据库表、数据文件、API 等 |
| 元数据 | 描述数据的数据，包括技术元数据（字段类型、长度）、业务元数据（业务含义、所有者）等 |
| 数据血缘 | 数据从源头到最终使用的完整流转路径，包括上下游依赖关系 |
| 资产生命周期 | 数据资产从创建、使用、归档到销毁的完整过程 |

### 7.2 参考文档

| 文档 | 位置 | 说明 |
|:---|:---|:---|
| 产品管理方案全景指南 | [PRODUCT_MGMT_WIKI.md](./PRODUCT_MGMT_WIKI.md) | 整体架构和规划 |
| 数据资产 PRD | 飞书文档 | 详细需求文档 |
| Epic 拆解确认表 | 飞书多维表格 | Story 级别拆解和状态 |

### 7.3 变更记录

| 版本 | 日期 | 变更内容 | 变更人 |
|:---:|:---:|:---|:---:|
| v1.0 | 2026-04-13 | 初始版本创建 | Tony Stark |

---

*🦾 "我是天才，这点不用谦虚。我们一起把产品做成，还要做得漂亮。" — Tony Stark*
