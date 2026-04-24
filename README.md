# Nick Wiki - 金融科技知识库

> 尼克·弗瑞的个人知识管理系统，基于Karpathy的LLM Wiki模式构建
> 多Agent协作知识库 - 派蒙（总协调）🤝 尼克·弗瑞（情报）🤝 钟离（技术）

---

## 📋 概述

**维护者**: 派蒙 & 尼克·弗瑞 & 钟离  
**更新**: 2026-04-13  
**核心规范**: [wiki/AGENT_COLLAB_GUIDE.md](wiki/AGENT_COLLAB_GUIDE.md)

---

## 👥 团队成员

| 角色 | 一句话定位 | 主要职责 |
|------|-----------|----------|
| **派蒙** | 项目协调者、大总管 | 任务分解、进度跟踪、协调桥接 |
| **尼克·弗瑞** 🕵️ | 情报与洞察专家 | 市场调研、竞品分析、行业洞察 |
| **钟离** ⚔️ | 技术架构专家 | 系统设计、技术选型、工程实践 |
| **文博** | 最终决策者 | 项目方向、关键决策 |

---

## 🗂️ 目录结构

```
Wiki/
├── README.md                        # 本文件
├── AGENT_COLLAB_GUIDE.md           # 核心协作指南 ⭐
│
├── wiki/                           # 核心知识库
│   ├── index.md                   # 全局索引
│   ├── log.md                    # 更新日志
│   │
│   ├── AGENT_COLLAB_GUIDE.md     # 协作指南 ⭐
│   │
│   ├── insights/                  # 行业洞察（尼克主写）⭐
│   │   └── insight-20260409-*.md
│   │
│   ├── topics/                    # 主题专题
│   │   ├── fintech/              # 金融科技专题
│   │   │   ├── README.md
│   │   │   ├── compliance.md
│   │   │   ├── data-platform.md
│   │   │   ├── infrastructure.md
│   │   │   ├── intelligent-systems.md
│   │   │   ├── llm-finance.md
│   │   │   ├── marketing-suite.md
│   │   │   ├── open-banking.md
│   │   │   ├── risk-management.md
│   │   │   └── product-solutions/
│   │   │
│   │   ├── ai-native/            # AI Native专题
│   │   │   ├── README.md
│   │   │   ├── ai-programming.md
│   │   │   ├── agent-engineering.md
│   │   │   ├── ai-application.md
│   │   │   └── openclaw-practices.md
│   │   │
│   │   ├── analysis-frameworks/  # 分析框架专题
│   │   │   ├── README.md
│   │   │   ├── hegang-framework.md
│   │   │   ├── majiangbo-framework.md
│   │   │   ├── caiyu-framework.md
│   │   │   └── 10-analysis-models.md
│   │   │
│   │   ├── ai-enterprise-implementation/  # 企业AI落地
│   │   │   └── enterprise-ai-implementation.md
│   │   │
│   │   ├── product-management/   # 产品管理专题
│   │   │   └── product-management-ontology.md
│   │   │
│   │   └── tech-ai.md           # AI技术总览
│   │
│   ├── entities/                  # 实体库
│   │   ├── companies/
│   │   │   ├── anthropic.md
│   │   │   ├── ant-group.md
│   │   │   ├── alipay.md
│   │   │   ├── apple.md
│   │   │   ├── bytedance.md
│   │   │   ├── cmb.md
│   │   │   ├── deepmind.md
│   │   │   ├── duxiaoman.md
│   │   │   ├── meituan.md
│   │   │   ├── msxf.md
│   │   │   ├── nvidia.md
│   │   │   ├── openai.md
│   │   │   ├── tencent.md
│   │   │   ├── tencent-cloud.md
│   │   │   ├── webank.md
│   │   │   └── zhaolian.md
│   │   ├── markets/
│   │   │   └── a-share.md
│   │   └── people/
│   │       ├── karpathy.md
│   │       └── li-feifei.md
│   │
│   ├── concepts/                  # 概念库
│   │   ├── ai-llm.md
│   │   ├── llm-agent.md
│   │   ├── llm-wiki-pattern.md
│   │   ├── rag.md
│   │   ├── good-questioning.md
│   │   └── scqa-framework.md
│   │
│   ├── projects/                   # 项目文档（派蒙维护）⭐
│   │   └── README.md              # 项目总览
│   │
│   └── process/                    # 流程规范
│       ├── ingest.md              # Ingest流程
│       └── lint.md                # Lint检查流程
│
├── sources/                       # 源数据
│   ├── best_practices/
│   │   ├── 01_核心领域_第一轮/
│   │   ├── 02_新兴领域_2026年/
│   │   └── 03_深度专题_待收集/
│   └── references/
│       ├── spec-coding-10days.md
│       ├── superpowers-ai-programming-workflow.md
│       └── anthropic-skills-guide.md
│
└── scripts/                       # 工具脚本
    ├── topic_ingest.py
    └── wiki_lint.py
```

---

## 📊 统计概览

| 类型 | 数量 | 状态 |
|------|------|------|
| **Insights** | 34个 | ✅ |
| **Topics** | 9个主目录 + 多个子专题 | ✅ |
| **Entities** | 20个（公司+人物+市场） | ✅ |
| **Concepts** | 7个 | ✅ |
| **Projects** | 0个 | 📝 待创建 |
| **Process SOPs** | 4个 | ✅ |

---

## 🔗 双向链接规范

```markdown
[[topic-id]]           # 链接到主题
[[entity-id]]          # 链接到实体
[[concept-id]]         # 链接到概念
[[insight-YYYYMMDD-xxx]]  # 链接到洞察
```

---

## 🔄 更新流程

| 操作 | 说明 | 执行人 |
|------|------|--------|
| **Ingest** | 消化新资料，更新Wiki | 尼克·弗瑞 |
| **Query** | 回答问题，存入insights | 尼克·弗瑞 |
| **Lint** | 健康检查，周日执行 | 派蒙 |
| **Project** | 项目协调与进度跟踪 | 派蒙 |

详见 [wiki/AGENT_COLLAB_GUIDE.md](wiki/AGENT_COLLAB_GUIDE.md)

## 📖 Wiki 管理细则

**核心文档**：[wiki/WIKI_MANAGEMENT_RULES.md](wiki/WIKI_MANAGEMENT_RULES.md)

包含：
- 知识分层体系（Insight/Topic/Entity/Concept/Project）
- 准入标准（5星评级体系）
- 保鲜机制（3个月自动标记）
- 运营节奏（每日/每周/每月）
- 质量标准
- 协作规范

---

## 🛠️ 工具脚本

| 脚本 | 用途 |
|------|------|
| `topic_ingest.py` | 主题内容摄取 |
| `wiki_lint.py` | Wiki健康检查 |

---

## 🔐 访问权限

- **T2机密**: Wiki内容，仅团队内部访问

---

## 📝 快速导航

| 导航 | 链接 |
|------|------|
| 核心协作指南 | [AGENT_COLLAB_GUIDE.md](wiki/AGENT_COLLAB_GUIDE.md) |
| 全局索引 | [index.md](wiki/index.md) |
| 更新日志 | [log.md](wiki/log.md) |
| 金融科技专题 | [fintech/README.md](wiki/topics/fintech/README.md) |
| AI Native专题 | [ai-native/README.md](wiki/topics/ai-native/README.md) |
| 分析框架专题 | [analysis-frameworks/README.md](wiki/topics/analysis-frameworks/README.md) |
| 项目总览 | [projects/README.md](wiki/projects/README.md) |

---

*情报是决策的基础。我不收集信息，我生产洞察。*

*最后更新：2026-04-16*
