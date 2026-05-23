# Agent 能力全景分析报告

> **版本**: v1.0
> **日期**: 2026-05-22
> **作者**: 尼克·弗瑞
> **分类**: Agent Architecture / Capability Framework
> **Tags**: #agent #capability #framework #multi-agent #skill #knowledge
> **方法论**: 情报综合分析

---

## 一、核心发现

### 1.1 能力体系全景

我们的Agent能力体系由**四层架构**支撑：

| 层级 | 内容 | 访问方式 | 代表组件 |
|:---:|:---|:---|:---|
| **L1** | OpenClaw原生能力 | 默认 | Session/Memory/工具集/多Agent通信 |
| **L2** | 基础设施 | Skill封装 | 知识库(Chroma)/Neo4j/飞书/任务系统 |
| **L3** | Skill能力 | openclaw skills | 公共Skill + 专属Skill |
| **L4** | 知识资产 | knowledge_search | Wiki/SOP/PRD/模板 |

### 1.2 三大支撑框架

| 框架 | 说明 | 状态 |
|:---|:---|:---:|
| **Karpathy LLM Wiki Pattern** | 三层架构：Sources → Wiki → Schema | ✅ 已建立 |
| **6大方法论** | tech-understanding/requirement-decision/product-design/data-driven/value-closed-loop/risk-control | ✅ 已建立 |
| **Agent能力框架** | 4层架构：L1原生 → L2基础 → L3 Skill → L4知识资产 | ✅ 今日更新 |

---

## 二、能力层级详解（Layered Architecture）

### 2.1 L1: OpenClaw 原生能力

**定义**：OpenClaw 开箱即用的基础能力，无需安装Skill。

```
┌─────────────────────────────────────────────────────┐
│  L1: OpenClaw 原生能力                              │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ✅ Session 管理      ── 跨会话记忆上下文            │
│  ✅ Memory Search    ── 检索全局记忆库               │
│  ✅ 基础工具集       ── read/write/edit/exec         │
│  ✅ Cron/Heartbeat   ── 定时任务和健康检查            │
│  ✅ 多Agent通信      ── sessions_send/派蒙中转        │
│  ✅ 飞书消息         ── 消息收发（配置后可用）        │
│                                                      │
└─────────────────────────────────────────────────────┘
```

**特点**：无需配置，默认拥有。

---

### 2.2 L2: 基础设施能力

**定义**：已部署的公共服务，通过Skill封装供Agent调用。

| 基础设施 | 用途 | 封装Skill | 负责人 |
|:---|:---|:---|:---|
| **知识库**（Chroma + bge-m3） | 语义检索团队文档 | `knowledge_search` | Tony |
| **Neo4j 图数据库** | 产品域结构、Epic/Feature/FP关系 | `requirement-breakdown` | Tony |
| **飞书文档** | 文档读写 | `feishu-doc` | - |
| **飞书知识库** | Wiki管理 | `feishu-wiki` | - |
| **飞书云盘** | 文件管理 | `feishu-drive` | - |
| **飞书权限** | 文档权限管理 | `feishu-perm` | - |
| **任务系统**（SQLite） | Agent任务看板 | `agent-task-board` | Tony |
| **RSS源** | 情报订阅 | Nick维护 | Nick |

---

### 2.3 L3: Skill能力

#### 3.1 公共Skill（所有Agent默认拥有）

| Skill | 用途 |
|:---|:---|
| **context-eng** | 上下文工程，避免session边界混乱 |
| **agent-daily-report** | 日报收集，团队统一日报流程 |
| **agent-task-board** | 任务管理，团队统一任务看板 |
| **clawhub** | Skill市场，搜索安装新Skill |
| **knowledge_search** | 知识库检索，访问L4知识资产 |
| **brainstorming** | 头脑风暴 |
| **humanizer** | 消除AI痕迹 |

#### 3.2 专属Skill（按Agent角色）

| Agent | 专属Skill | 数量 |
|:---|:---|:---:|
| **Tony** | requirement-understanding / requirement-supplement / requirement-breakdown / prd-generation / spec-driven / task-planning / epic-walkthrough / claude-code-orchestrator | 8 |
| **Nick** | Deep Research / multi-source-research / rss-intelligence | 3 |
| **Zhongli** | tdd-workflow / git-workflow / frontend-ui / code-review | 4 |

---

### 2.4 L4: 知识资产

**定义**：团队积累的文档、模板、案例等知识财富。

**访问方式**：
```python
knowledge_search(
    query="需求拆解 SOP 流程",
    doc_type="SOP",
    top_k=5
)
```

| 知识资产 | 位置 | 索引状态 |
|:---|:---|:---:|
| **Wiki知识库** | `/Users/wenbo/Documents/project/Wiki/wiki/` | ✅ 已索引 |
| **PRD模板** | `文档仓库/产品管理项目/PRD/` | ✅ 已索引 |
| **SOP文档** | 知识库 | ✅ 已索引 |
| **参考案例** | Wiki concepts/ | ✅ 已索引 |

---

## 三、能力评估模型：七角模型

### 3.1 七角能力详解

| 角位 | 能力名称 | 核心要求 | 技术实现关键 | 对应层级 |
|:---:|:---|:---|:---|:---:|
| **第1角** | 目标解析能力 | 理解模糊指令，拆解为可执行任务链 | 意图识别+任务规划引擎 | L1 |
| **第2角** | 记忆系统 | 短期-任务-长期三层记忆 | 向量数据库+状态管理 | L2 |
| **第3角** | 人机协同能力 | 主动建议+关键确认+适时干预 | 主动交互+规则引擎 | L1 |
| **第4角** | 自我检查机制 | 识别幻觉边界+信息溯源+置信度标记 | 验证引擎+溯源系统 | L3 |
| **第5角** | 信噪比判断 | 可信度排序+降噪处理+摘要压缩 | 过滤算法+压缩引擎 | L1 |
| **第6角** | 结构化输出 | 按场景定制格式+可复用成果 | 模板引擎+知识沉淀 | L4 |
| **第7角** | 自主执行能力 | 规划-执行-验证-调整-交付闭环 | 工具调用+执行引擎 | L3 |

### 3.2 七角模型与四层架构映射

```
                    目标解析（第1角）
                        │
                       / \
                      /   \
                     /     \
                    /       \
                   /         \
结构化输出 ───────┼───────────┼───────────── 自主执行
（第6角）          │  L3 Skill  │             （第7角）
                   │           │
                   │  记忆系统  │
                   │  （第2角） │
                   │           │
                   │  自我检查  │
                   │  （第4角） │
                   └───────────┘
                        │
                   人机协同（第3角）
                   信噪比判断（第5角）
```

---

## 四、6大方法论体系

### 4.1 方法论全景

> 方法论 = 能力的实体化

| 方法论 | 解决的问题 | 核心问题 |
|:---|:---|:---|
| **技术理解** | 能不能做 | 技术选型、可行性评估 |
| **需求决策** | 该不该做 | 需求优先级、PRD规范 |
| **产品设计** | 怎么做 | UX设计、交互模式 |
| **数据驱动** | 如何闭环 | 指标体系、闭环构建 |
| **价值闭环** | 如何衡量 | ROI论证、TCO测算 |
| **风险防控** | 如何控制 | 风控机制、合规治理 |

### 4.2 方法论与能力层级映射

| 方法论 | 对应能力 | 说明 |
|:---|:---|:---|
| **技术理解** | L1/L2 | 技术选型能力、基础设施理解 |
| **需求决策** | L3/L4 | PRD生成、需求管理Skill |
| **产品设计** | L3/L4 | 产品设计Skill、模板库 |
| **数据驱动** | L2 | 知识库、Neo4j数据分析 |
| **价值闭环** | L4 | 知识资产、案例沉淀 |
| **风险防控** | L3 | 验证Skill、审查流程 |

---

## 五、知识管理：Karpathy LLM Wiki Pattern

### 5.1 三层架构

```
┌─────────────────────────────────────────────────────────────┐
│              Karpathy LLM Wiki Pattern                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Layer 3: Schema (schema/)                                  │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ CLAUDE.md / AGENTS.md / SOUL.md                      │    │
│  │ 定义结构、约定、工作流，与LLM共同演进                 │    │
│  └─────────────────────────────────────────────────────┘    │
│                           ↑                                 │
│  Layer 2: Wiki (wiki/)                                      │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Insights / Concepts / Entities / Topics             │    │
│  │ LLM生成的Markdown文件，可更新，LLM完全拥有           │    │
│  └─────────────────────────────────────────────────────┘    │
│                           ↑                                 │
│  Layer 1: Sources (sources/)                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ wechat / reports / papers / docs / rss              │    │
│  │ 原始文档、URL、书籍，不可变，作为真相来源             │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 三种操作

| 操作 | 说明 | 产出 |
|:---|:---|:---|
| **Ingest** | 添加新资料，识别实体和概念，更新Wiki | 新增/更新页面 |
| **Query** | 用户提问，检索相关页面，综合生成回答 | 回答（有价值则存为Insight） |
| **Lint** | 定期检查：矛盾、过时、孤立、缺失 | 健康报告 |

### 5.3 我们的Sources体系

| 类型 | 说明 | 示例 |
|:---|:---|:---|
| **wechat** | 公众号文章 | 微信文章、36kr、虎嗅 |
| **reports** | 行业报告 | 艾瑞、IDC、麦肯锡 |
| **papers** | 学术论文 | arXiv、ACL、ICML |
| **docs** | 产品文档 | GitHub README、API Docs |
| **rss** | RSS订阅源 | 234个RSS源 |

---

## 六、Multi-Agent 协作模式

### 6.1 Agent角色分工

| Agent | 角色定位 | 核心能力 | 数量 |
|:---|:---|:---|:---:|
| **派蒙** | 大总管 | 协调、调度、信息路由 | - |
| **Tony** | 产品管理 | 需求理解→PRD→Neo4j拆解 | 8个Skill |
| **Nick** | 情报分析 | 深度研究、多源整合 | 3个Skill |
| **Zhongli** | 技术工程 | 代码、测试、前端 | 4个Skill |

### 6.2 协作流程

```
用户问题
    │
    ▼
┌─────────────────────────────────────────────────────┐
│                     派蒙                            │
│  - 理解问题                                        │
│  - 分解任务                                        │
│  - 分配给合适的Agent                                │
└─────────────────────────────────────────────────────┘
    │
    ├──► Tony（产品管理）
    │         │
    │         └──► requirement-understanding
    │                     ↓
    │                  requirement-breakdown
    │                     ↓
    │                  prd-generation
    │
    ├──► Nick（情报分析）
    │         │
    │         └──► Deep Research
    │                     ↓
    │                  multi-source-research
    │
    └──► Zhongli（技术工程）
              │
              └──► tdd-workflow
                          ↓
                       code-review
```

### 6.3 信息流

| 信息类型 | 来源 | 处理 | 输出 |
|:---|:---|:---|:---|
| **原始情报** | RSS/Wechat/Reports | Nick分析 | 简报/Wiki |
| **需求** | 用户/文档 | Tony解析 | PRD/Neo4j |
| **技术方案** | Tony需求 | Zhongli实现 | 代码/测试 |
| **知识资产** | 所有Agent | LLM处理 | Wiki沉淀 |

---

## 七、Skill能力体系

### 7.1 Skill分类框架

| 类别 | 说明 | Skill数量 |
|:---|:---|:---:|
| **Core** | PRD全链路 | 4 |
| **Framework** | 工程规范 | 2 |
| **Intelligence** | 情报收集 | 3 |
| **Utility** | 运营支持 | 2 |

### 7.2 Skill链路

```
需求输入
    │
    ├──► requirement-understanding（解析）
    │
    ├──► requirement-supplement（补充）
    │
    ├──► prd-generation（生成PRD）
    │
    ├──► requirement-breakdown（Neo4j拆解）
    │
    └──► spec-driven/code-review（执行）
```

### 7.3 Skill评估体系

| 维度 | 说明 | 权重 |
|:---|:---|:---:|
| **效果** | 任务完成度、输出质量 | 40% |
| **效率** | 时间消耗、资源占用 | 20% |
| **稳定** | 成功率、错误率 | 20% |
| **复用** | 适用场景数、扩展性 | 10% |
| **安全** | 数据保护、权限合规 | 10% |

---

## 八、能力成熟度模型

### 8.1 LLM Agent能力分级

| 级别 | 能力 | 代表 |
|:---|:---|:---|
| **L1** | 基础对话 | ChatGPT |
| **L2** | 工具调用 | GPT-4 + Functions |
| **L3** | 多步推理 | o1, Claude |
| **L4** | 自主规划 | Claude Agent |
| **L5** | 自我改进 | 未来方向 |

### 8.2 我们当前的成熟度

| 能力 | 当前级别 | 说明 |
|:---|:---:|:---|
| **Session/Memory** | 🟢 L3 | 跨会话记忆，情景记忆 |
| **工具调用** | 🟢 L3 | exec/browser/知识库 |
| **多步推理** | 🟢 L3 | in-depth-research |
| **自主规划** | 🟡 L4 | task-planning/requirement-breakdown |
| **Multi-Agent** | 🟡 L4 | 派蒙协调，三人协作 |
| **自我改进** | 🔴 L1 | 还未实现 |

### 8.3 提升路径

```
当前状态                    目标状态
─────────────────────────────────────
L3: 多步推理    →    L4: 自主规划    →    L5: 自我改进
    │                    │                    │
    ▼                    ▼                    ▼
现有in-depth-        实现task-            建立自我
research             planning             反思机制
                     │
                     ▼
                实现epic-
                walkthrough
```

---

## 九、情报工作流（v4.0）

### 9.1 五阶段工作流

```
┌─────────────────────────────────────────────────────────────┐
│  情报收集 → 情报分析 → 情报Tag → 情报分发 → 知识沉淀         │
└─────────────────────────────────────────────────────────────┘
     ↓              ↓              ↓            ↓            ↓
   RSS抓取       质量评级      方法论Tag    飞书推送       Wiki归档
   GitHub        价值判断      故事线Tag    简报发送       Blog素材
   Get笔记       关联分析      类型Tag      即时推送       方法论Tag
```

### 9.2 方法论Tag体系

| Tag | 适用场景 |
|:---|:---|
| **tech-understanding** | AI技术选型、模型评估、技术原理 |
| **requirement-decision** | 需求优先级、PRD、决策框架 |
| **product-design** | UX设计、交互模式、AI产品设计 |
| **data-driven** | 数据治理、指标体系、闭环构建 |
| **value-closed-loop** | ROI、TCO、商业论证、价值量化 |
| **risk-control** | AI伦理、风控机制、合规治理 |

### 9.3 RSS Tag标注机制

每篇RSS文章需要打法论Tag：
- ✅ 打方法论Tag（对齐6大方法论）
- ✅ 打故事线Tag（fusion/empower/value）
- ✅ 打类型Tag（insight/concept/entity/topic）

---

## 十、结论与建议

### 10.1 能力体系总结

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent 能力全景                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Layer 4: 知识资产 ── Wiki/SOP/PRD/模板                     │
│      ↑                                                        │
│  Layer 3: Skill能力 ── Core(4) + Framework(2) + Intel(3)    │
│      ↑                                                        │
│  Layer 2: 基础设施 ── 知识库/Neo4j/飞书/任务系统              │
│      ↑                                                        │
│  Layer 1: 原生能力 ── Session/Memory/工具集/多Agent通信      │
│                                                              │
│  七角模型: 目标解析/记忆/人机协同/自我检查/信噪比/结构化/自主 │
│  6大方法论: 技术理解/需求决策/产品设计/数据驱动/价值闭环/风险 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 10.2 核心优势

| 优势 | 说明 |
|:---|:---|
| **四层架构清晰** | L1-L4职责分明，易于扩展 |
| **方法论对齐** | 6大方法论贯穿情报→知识→行动 |
| **Multi-Agent协作** | 派蒙协调，三人分工明确 |
| **Skill体系完善** | Core/Framework/Intelligence分离 |
| **知识管理规范** | Karpathy三层架构，Sources可追溯 |

### 10.3 待提升方向

| 方向 | 当前状态 | 目标 |
|:---|:---:|:---|
| **自我反思机制** | 🔴 无 | 建立L5自我改进能力 |
| **反馈闭环** | 🟡 弱 | 强化任务→结果→优化循环 |
| **知识溯源** | 🟡 部分 | 完善Sources体系覆盖 |
| **跨Agent记忆** | 🟡 Session | 建立共享长期记忆 |

### 10.4 行动建议

| 优先级 | 行动 | 产出 | 时间 |
|:---:|:---|:---|:---:|
| 🔴 | 建立自我反思机制 | 任务反思Skill | 1周 |
| 🟠 | 完善Sources体系 | Sources覆盖>80% | 2周 |
| 🟠 | 强化反馈闭环 | 任务→结果→优化 | 2周 |
| 🟡 | 跨Agent记忆共享 | 共享长期记忆 | 1月 |

---

## 📚 相关文档

| 文档 | 位置 |
|:---|:---|
| Agent能力框架 | `concepts/agent-capability-framework.md` |
| Agent七角模型 | `concepts/agent-seven-corners-model.md` |
| LLM Agent | `concepts/llm-agent.md` |
| LLM Wiki Pattern | `concepts/llm-wiki-pattern.md` |
| Skill基线报告 | `concepts/skill-baseline-report.md` |
| Skill评估框架 | `concepts/skill-benchmark-framework.md` |
| Skill分类 | `concepts/skill-classification.md` |

---

*分析时间: 2026-05-22*
*分析师: 尼克·弗瑞*
*方法论: 情报综合分析*
*标签: #tech-understanding #requirement-decision #data-driven #value-closed-loop*