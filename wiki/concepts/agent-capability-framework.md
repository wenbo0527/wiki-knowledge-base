---
title: agent capability framework
author: 尼克·弗瑞 🕵️
product_domain: PD-CONCEPT
doc_type: 其他
tags: [concepts]
date: 2026-05-23
---

# Agent 能力框架 - 公共 vs 专属能力划分

> **版本**: v1.1
> **日期**: 2026-05-22
> **制定者**: 派蒙（大总管）
> **状态**: 已发布

---

## 一、背景

随着 Agent 团队规模扩大，需要清晰区分：
1. **公共能力** - 所有 Agent 都需要的共享技能
2. **专属能力** - 特定 Agent 独有的专业技能

合理的划分可以：
- 避免能力重复安装，节省资源
- 明确每个 Agent 的职责边界
- 便于权限控制和访问管理

---

## 二、能力分层架构

Agent 能力体系分为 **4 层**，从底层到上层：

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent 能力体系                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ L4: 知识资产 - 文档、模板、案例                       │   │
│  │  访问方式: knowledge_search (Chroma+bge-m3)         │   │
│  └─────────────────────────────────────────────────────┘   │
│                           ↑                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ L3: Skill 能力 - 封装的专业技能                     │   │
│  │  访问方式: openclaw skills list / load              │   │
│  └─────────────────────────────────────────────────────┘   │
│                           ↑                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ L2: 基础设施 - 部署好的公共服务                      │   │
│  │  访问方式: Skill 封装（feishu-*, agent-*, etc）     │   │
│  └─────────────────────────────────────────────────────┘   │
│                           ↑                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ L1: OpenClaw 原生能力 - 开箱即用                     │   │
│  │  访问方式: 默认拥有，无需配置                        │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 三、层级详解

### L1: OpenClaw 原生能力（默认，所有 Agent 都有）

**定义**：OpenClaw 开箱即用的基础能力，无需安装 Skill。

| 能力 | 说明 | 访问方式 |
|:-----|:-----|:---------|
| **Session 管理** | 跨会话记忆上下文 | 默认 |
| **Memory Search** | 检索全局记忆库（MEMORY.md、memory/*.md） | `memory_search` |
| **基础工具集** | read/write/edit/exec/sessions_send | 默认 |
| **Cron/Heartbeat** | 定时任务和健康检查 | Cron 配置 |
| **多 Agent 通信** | sessions_send / 派蒙中转协议 | 默认 |
| **飞书消息** | 消息收发（配置 channel 后可用） | channel 配置 |

**配置方式**：无需配置，OpenClaw 默认提供。

---

### L2: 基础设施能力（公共服务，所有 Agent 共享）

**定义**：已部署的公共服务，通过 Skill 封装供 Agent 调用。

| 基础设施 | 用途 | 封装 Skill | 负责人 |
|:---------|:-----|:----------|:-------|
| **知识库**（Chroma + bge-m3） | 语义检索团队文档、SOP、PRD、模板 | `knowledge_search` | Tony |
| **Neo4j 图数据库** | 产品域结构、Epic/Feature/FP 关系 | `requirement-breakdown` | Tony |
| **飞书文档** | 文档读写 | `feishu-doc` | - |
| **飞书知识库** | Wiki 管理 | `feishu-wiki` | - |
| **飞书云盘** | 文件管理 | `feishu-drive` | - |
| **飞书权限** | 文档权限管理 | `feishu-perm` | - |
| **任务系统**（SQLite） | Agent 任务看板 | `agent-task-board` | Tony |
| **RSS 源** | 情报订阅 | Nick 维护 | Nick |

**访问方式**：加载对应 Skill 后通过工具调用访问。

---

### L3: Skill 能力

#### 3.1 公共 Skill（所有 Agent 默认拥有）

| Skill | 用途 | 说明 |
|:------|:-----|:-----|
| **context-eng** | 上下文工程 | 避免 session 边界混乱 |
| **agent-daily-report** | 日报收集 | 团队统一日报流程 |
| **agent-task-board** | 任务管理 | 团队统一任务看板 |
| **clawhub** | Skill 市场 | 搜索安装新 Skill |
| **knowledge_search** | 知识库检索 | 访问 L4 知识资产 |
| **brainstorming** | 头脑风暴 | 建议新增为公共 |
| **humanizer** | 消除AI痕迹 | 建议新增为公共 |

#### 3.2 Tony 专属 Skill（产品管理流程）

| Skill | 用途 |
|:------|:-----|
| **requirement-understanding** | 需求理解，解析需求填充9项清单 |
| **requirement-supplement** | 需求补充，用户场景、功能边界、验收标准 |
| **requirement-breakdown** | 需求拆解，拆解到 Neo4j 图数据库 |
| **prd-generation** | PRD生成，生成 v5.0 规范文档 |
| **spec-driven** | 规范驱动开发，先写 PRD 再开发 |
| **task-planning** | 任务规划，拆解为可执行小任务 |
| **epic-walkthrough** | Epic 走查，检查 Neo4j 结构、文档完整性 |
| **claude-code-orchestrator** | Claude Code 任务编排，复杂任务分步执行 |

#### 3.3 Nick 专属 Skill（情报分析）

| Skill | 用途 |
|:------|:-----|
| **Deep Research** | 多源深度调研，系统性调查研究 |
| **multi-source-research** | 多源研究助手，网页/学术/社交媒体整合 |
| **rss-intelligence** | RSS 情报系统（自建） |

#### 3.4 Zhongli 专属 Skill（技术工程）

| Skill | 用途 |
|:------|:-----|
| **tdd-workflow** | 测试先行开发流，80%+ 覆盖率 |
| **git-workflow** | Git 工作流规范 |
| **frontend-ui** | 前端 UI 工程，Vue 3 + Arco Design |
| **code-review** | 多维度代码审查 |

#### 3.5 内容组 Skill（阿加莘/老六）

| Skill | 用途 | 所属 |
|:------|:-----|:-----|
| **brainstorming** | 头脑风暴 | 共享 |
| **humanizer** | 消除AI痕迹 | 共享 |
| **Deep Research** | 深度调研（内容方向） | 阿加莘 |

#### 3.6 投资分析 Skill（小二子）

| Skill | 用途 |
|:------|:-----|
| **multi-source-research** | 多源研究（投资分析方向） |

---

### L4: 知识资产（通过 knowledge_search 访问）

**定义**：团队积累的文档、模板、案例等知识财富。

**访问方式**：
```python
# 通过 knowledge_search Skill 访问 L4 知识资产
knowledge_search(
    query="需求拆解 SOP 流程",
    doc_type="SOP",
    top_k=5
)
```

| 知识资产 | 位置 | 索引到知识库 | 说明 |
|:---------|:-----|:------------|:-----|
| **Wiki 知识库** | `/Users/wenbo/Documents/project/Wiki/wiki/` | ✅ | 团队知识沉淀 |
| **PRD 模板** | `文档仓库/产品管理项目/PRD/` | ✅ | PRD v5.0 模板 |
| **SOP 文档** | 知识库 | ✅ | 标准操作流程 |
| **参考案例** | Wiki concepts/ | ✅ | 最佳实践 |
| **Agent 配置** | `workspace-agents/*/` | ❌ | 派蒙通过 memory_search 访问 |

---

## 四、两套搜索系统的分工

| 系统 | 用途 | 搜索内容 | 访问方式 |
|:-----|:-----|:---------|:---------|
| **memory_search** | Agent 记忆 | MEMORY.md、memory/*.md、session transcripts | 直接调用 |
| **knowledge_search** | 团队知识库 | Chroma 向量数据库（Wiki、SOP、PRD、模板） | 通过 Skill 调用 |

**原则**：
- **Agent 自身配置和记忆** → `memory_search`
- **团队知识资产（文档/模板/案例）** → `knowledge_search`

---

## 五、完整能力矩阵

| 层级 | 能力 | 派蒙 | Tony | Nick | Zhongli | 阿加莘 | 老六 | 麦麦 | 小二子 |
|:-----|:-----|:----:|:----:|:----:|:-------:|:------:|:----:|:----:|:------:|
| **L1 原生** | Session/Memory | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 |
| **L1 原生** | 基础工具集 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 |
| **L1 原生** | 多 Agent 通信 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 |
| **L2 基础** | 知识库(Chroma) | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 |
| **L2 基础** | Neo4j 图数据库 | - | 🟢 | - | - | - | - | - | - |
| **L2 基础** | 飞书集成 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 |
| **L2 基础** | 任务系统(SQLite) | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 |
| **L2 基础** | RSS 服务 | - | - | 🟢 | - | - | - | - | - |
| **L3 Skill** | 公共 Skill(7个) | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 |
| **L3 Skill** | Tony 需求流程 | - | 🟢 | - | - | - | - | - | - |
| **L3 Skill** | Nick 情报系统 | - | - | 🟢 | - | - | - | - | - |
| **L3 Skill** | Zhongli 工程 | - | - | - | 🟢 | - | - | - | - |
| **L3 Skill** | 阿加莘调研 | - | - | - | - | 🟢 | - | - | 🟡 |
| **L4 知识** | Wiki/SOP/PRD | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 |

**图例**：🟢 核心能力 | 🟡 辅助能力 | - 不适用

---

## 六、OpenClaw 实现方式

### 6.1 Skill 加载层级

| 层级 | 路径 | 可见范围 | 优先级 |
|:-----|:-----|:--------|:-------|
| **L1** | `<workspace>/skills` | 单个 Agent | 最高 |
| **L2** | `~/.openclaw/skills` | 所有 Agent | 中 |
| **L3** | OpenClaw Bundled | 所有 Agent | 低 |

**设计原则**：
- 公共 Skill → 放在 `~/.openclaw/skills/`（L2）
- 专属 Skill → 放在 `<workspace>/skills/`（L1）

### 6.2 Agent Allowlist 配置（可选）

通过 `openclaw.json` 的 `agents.list[].skills` 控制每个 Agent 的 Skill 可见性：

```json
{
  "agents": {
    "defaults": {
      "skills": [
        "context-eng",
        "agent-daily-report",
        "agent-task-board",
        "clawhub",
        "knowledge_search",
        "brainstorming",
        "humanizer"
      ]
    },
    "list": [
      {
        "id": "tony_stark",
        "skills": [
          "context-eng",
          "agent-daily-report",
          "agent-task-board",
          "clawhub",
          "knowledge_search",
          "brainstorming",
          "humanizer",
          "requirement-understanding",
          "requirement-supplement",
          "prd-generation",
          "spec-driven",
          "task-planning",
          "epic-walkthrough",
          "claude-code-orchestrator",
          "frontend-ui",
          "git-workflow",
          "code-review"
        ]
      },
      {
        "id": "nick_fury",
        "skills": [
          "context-eng",
          "agent-daily-report",
          "agent-task-board",
          "clawhub",
          "knowledge_search",
          "brainstorming",
          "humanizer",
          "Deep Research",
          "multi-source-research"
        ]
      },
      {
        "id": "zhongli",
        "skills": [
          "context-eng",
          "agent-daily-report",
          "agent-task-board",
          "clawhub",
          "knowledge_search",
          "brainstorming",
          "humanizer",
          "tdd-workflow",
          "frontend-ui",
          "git-workflow",
          "code-review"
        ]
      }
    ]
  }
}
```

---

## 七、实施计划

### Phase 1：现状梳理 ✅
- [x] 统计所有就绪 Skill（38个）
- [x] 分类公共 vs 专属
- [x] 创建能力矩阵

### Phase 2：配置实现（待定）
- [ ] 确定 Agent allowlist 配置策略
- [ ] 将专属 Skill 移动到 `<workspace>/skills/`
- [ ] 更新 OpenClaw 配置
- [ ] 验证各 Agent Skill 可见性

### Phase 3：文档沉淀
- [x] 更新 AGENTS.md 能力说明
- [ ] 更新各 Agent 的 SOUL.md 能力描述
- [x] 更新 _registry.md 分类索引

---

## 八、决策事项

| # | 问题 | 选项 |
|:---:|:---|:---|
| 1 | **是否启用 Agent allowlist** | A. 是，精确控制 / B. 否，全局共享 |
| 2 | **专属 Skill 存放位置** | A. `<workspace>/skills/` / B. 统一放全局 |
| 3 | **公共 Skill 范围** | A. 当前 7 个 / B. 扩展更多 |
| 4 | **谁来维护 allowlist** | A. 派蒙统一 / B. 各 Agent 自主 |

---

## 九、相关文档

| 文档 | 位置 | 说明 |
|:-----|:-----|:-----|
| OpenClaw 能力框架 | `concepts/openclaw-capability-framework.md` | OpenClaw 原生能力说明 |
| Skill Registry | `~/.openclaw/skills/_registry.md` | Skill 总清单 |
| Agent 七维评估 | `concepts/agent-seven-corners-model.md` | Agent 能力评估框架 |
| SKILL管理平台产品方案 | `文档仓库/.../主文档/SKILL管理平台产品方案-v1.0.md` | Tony 的管理平台规划 |

---

## 十、版本历史

| 版本 | 日期 | 说明 |
|:---:|:---:|:---|
| v1.0 | 2026-05-22 | 初始版本 |
| v1.1 | 2026-05-22 | 补充 L4 知识资产说明，修正两套搜索系统分工 |

---

*版本: v1.1*
*日期: 2026-05-22*
*制定者: 派蒙（大总管）*
*状态: 已发布*