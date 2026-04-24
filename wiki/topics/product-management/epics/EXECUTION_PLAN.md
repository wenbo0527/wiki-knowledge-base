# Epic 文档并行执行计划

> 使用 Subagent 并行创建 Epic 文档
> 
> 制定者：Tony Stark | 时间：2026-04-13

---

## 1. 执行概览

| 项目 | 数值 |
|:---|:---:|
| **总 Epic 数** | 30 个 |
| **已创建** | 5 个 (PD-DFD 全部完成) |
| **待创建** | 25 个 |
| **并行度** | 4 个 Subagent |
| **预计完成时间** | 24 小时 |

---

## 2. 任务分组

将 25 个待创建 Epic 按产品域分组，分配给 4 个 Subagent 并行执行：

### Subagent A - 数字社区组 (4 个 Epic)

| # | Epic ID | Epic 名称 | 优先级 | 预计工时 |
|:---:|:---|:---|:---:|:---:|
| 1 | EPIC-COM_PORTAL_MANAGE | 门户管理 | P0 | 1.5h |
| 2 | EPIC-COM_PERM_MANAGE | 权限管理 | P0 | 1.5h |
| 3 | EPIC-COM_CONTENT_MANAGE | 内容管理 | P1 | 1.5h |
| 4 | EPIC-COM_NOTICE_MANAGE | 通知管理 | P1 | 1.5h |

### Subagent B - 数字风险组 (2 个 Epic)

| # | Epic ID | Epic 名称 | 优先级 | 预计工时 |
|:---:|:---|:---|:---:|:---:|
| 1 | EPIC-RISK_MODEL_BACKTRACE_OFFLINE | 模型回溯线下化 | P0 | 2h |
| 2 | EPIC-RISK_EXT_DATA_LIFECYCLE | 外部数据生命周期管理 | P0 | 2h |

### Subagent C - 数字营销组 (7 个 Epic)

| # | Epic ID | Epic 名称 | 优先级 | 预计工时 |
|:---:|:---|:---|:---:|:---:|
| 1 | EPIC-MKT_BENEFIT_CENTER | 权益中心 | P0 | 1h |
| 2 | EPIC-MKT_CROWD_CENTER | 客群中心 | P0 | 1.5h |
| 3 | EPIC-MKT_MANUAL_SALES_DESK | 人工电销工作台 | P1 | 1.5h |
| 4 | EPIC-MKT_MARKETING_CANVAS | 营销画布 | P1 | 1.5h |
| 5 | EPIC-MKT_REACH_SYSTEM | 触达系统 | P1 | 1.5h |
| 6 | EPIC-MKT_CAMPAIGN_MGMT | 营销活动管理 | P2 | 1.5h |
| 7 | EPIC-MKT_GROWTH_ANALYSIS | 增长分析中心 | P2 | 1.5h |

### Subagent D - 数据探索组 + 数据管理组 (12 个 Epic)

#### 数据探索组 (4 个 Epic)

| # | Epic ID | Epic 名称 | 优先级 | 预计工时 |
|:---:|:---|:---|:---:|:---:|
| 1 | EPIC-DEX_DATA_QUERY | 即席查询 | P0 | 1.5h |
| 2 | EPIC-DEX_SELF_SERVICE_ANALYSIS | 自助分析 | P0 | 1.5h |
| 3 | EPIC-DEX_INTELLIGENT_INSIGHT | 智能洞察 | P1 | 1.5h |
| 4 | EPIC-DEX_REPORT_CENTER | 报表中心 | P1 | 1.5h |

#### 数据管理组 (5 个 Epic)

| # | Epic ID | Epic 名称 | 优先级 | 预计工时 |
|:---:|:---|:---|:---:|:---:|
| 1 | EPIC-DMT_METADATA_MANAGE | 元数据管理 | P0 | 1.5h |
| 2 | EPIC-DMT_BIZ_CONCEPT_MANAGE | 业务概念管理 | P1 | 1.5h |
| 3 | EPIC-DMT_DATA_SERVICE | 数据服务 | P1 | 1.5h |
| 4 | EPIC-DMT_DATA_STD | 数据标准 | P2 | 1.5h |
| 5 | EPIC-DMT_DATA_QUALITY | 数据质量 | P2 | 1.5h |

#### 补充 Epic (3 个)

| # | Epic ID | Epic 名称 | 优先级 | 预计工时 |
|:---:|:---|:---|:---:|:---:|
| 1 | EPIC-RISK_REALTIME_DECISION | 实时决策引擎 | P1 | 1.5h |
| 2 | EPIC-DEX_COLLABORATION | 协作分享 | P2 | 1.5h |
| 3 | EPIC-MKT_CONTENT_MGMT | 内容管理中心 | P2 | 1.5h |

---

## 3. 执行方式

### 3.1 任务分配方式

使用 `sessions_spawn` 创建 4 个 subagent，每个 subagent 接收以下任务：

```yaml
subagent_a_task:
  role: "Epic文档编写者 - 数字社区组"
  epics: [EPIC-COM_PORTAL_MANAGE, EPIC-COM_PERM_MANAGE, EPIC-COM_CONTENT_MANAGE, EPIC-COM_NOTICE_MANAGE]
  template: /path/to/9_chapter_template.md
  output_dir: /Users/wenbo/Documents/project/Wiki/wiki/topics/product-management/epics/

subagent_b_task:
  role: "Epic文档编写者 - 数字风险组"
  epics: [EPIC-RISK_MODEL_BACKTRACE_OFFLINE, EPIC-RISK_EXT_DATA_LIFECYCLE]
  ...

subagent_c_task:
  role: "Epic文档编写者 - 数字营销组"
  epics: [EPIC-MKT_BENEFIT_CENTER, EPIC-MKT_CROWD_CENTER, ...]
  ...

subagent_d_task:
  role: "Epic文档编写者 - 数据探索组+数据管理组"
  epics: [EPIC-DEX_DATA_QUERY, EPIC-DEX_SELF_SERVICE_ANALYSIS, EPIC-DMT_METADATA_MANAGE, ...]
  ...
```

### 3.2 文档模板要求

每个 Epic 文档必须包含以下 9 章节：

1. **产品总览** - 一句话定位、价值主张、业务流程、角色、约束、术语
2. **功能结构** - 按模块归档，每个子系统包含入口、逻辑、配置、坑点、依赖
3. **需求与迭代历史** - 需求记录、版本迭代、决策记录
4. **数据相关** - 指标口径、数据来源、埋点、报表
5. **规则与配置中心** - 分类规则、权限规则、流程配置
6. **架构与依赖** - 依赖图、上下游、接口、环境
7. **问题库 & FAQ** - 问题、原因、方案、预防
8. **方法论沉淀** - 拆解方法、设计原则、行业对比、工具流程
9. **参考资料** - 竞品、规范、资料、链接

### 3.3 参考示例文档

已完成的参考文档：
- `/epics/EPIC-DFD_DATA_ASSET.md` - 简化版
- `/epics/EPIC-DFD_DATA_ELEMENT.md` - 简化版
- `/epics/EPIC-DFD_ASSET_OPERATE_TOOL.md` - 简化版
- `/epics/EPIC-DFD_DATA_RESOURCE.md` - **完整9章节模板**
- `/epics/EPIC-DFD_UNIFIED_SEARCH.md` - **完整9章节模板**

---

## 4. 执行命令

### 4.1 启动 Subagent A（数字社区组）

```bash
# 使用 sessions_spawn 创建 subagent
sessions_spawn \
  --task "Epic文档编写任务 - 数字社区组" \
  --runtime subagent \
  --mode run \
  --label "epic-writer-com" \
  --lightContext true \
  --attachments '[{
    "name": "task_instructions.md",
    "content": "请为以下4个Epic创建完整的需求文档，每个文档必须包含9个标准章节。\n\nEpic列表：\n1. EPIC-COM_PORTAL_MANAGE - 门户管理\n2. EPIC-COM_PERM_MANAGE - 权限管理\n3. EPIC-COM_CONTENT_MANAGE - 内容管理\n4. EPIC-COM_NOTICE_MANAGE - 通知管理\n\n要求：\n- 文档路径：/Users/wenbo/Documents/project/Wiki/wiki/topics/product-management/epics/\n- 文档名：EPIC-{ID}.md\n- 必须包含9个标准章节\n- 参考示例：/epics/EPIC-DFD_DATA_RESOURCE.md\n\n完成后返回创建的文档列表。"
  }]'
```

### 4.2 启动其他 Subagent（B/C/D）

类似上述命令，修改任务描述中的 Epic 列表即可。

---

## 5. 监控与验收

### 5.1 进度追踪

| 检查点 | 时间 | 检查内容 |
|:---|:---:|:---|
| 启动检查 | T+0 | 确认4个subagent都已启动 |
| 进度检查 | T+6h | 检查各组完成进度 |
| 中期检查 | T+12h | 验证已完成文档质量 |
| 最终验收 | T+24h | 全部文档完成验收 |

### 5.2 验收标准

- [ ] 所有25个Epic文档都已创建
- [ ] 每个文档包含完整的9个章节
- [ ] 文档命名符合规范（`EPIC-{ID}.md`）
- [ ] 文档放置在正确的目录
- [ ] 文档内容符合 Epic 实际范围

---

## 6. 风险与应对

| 风险 | 影响 | 应对策略 |
|:---|:---:|:---|
| Subagent 执行超时 | 进度延迟 | 设置超时限制（2h/Epic），超时重试 |
| 文档质量不达标 | 需要返工 | 建立检查点，中期抽检质量 |
| 部分 Epic 信息不足 | 无法完成 | 先标记待补充，继续其他任务 |
| Subagent 并发限制 | 无法启动 | 分批启动，控制并发数 |

---

*🦾 "并行作战，高效执行。让 25 个 Epic 文档同时推进！" — Tony Stark*
