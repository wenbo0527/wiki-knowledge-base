# Topic监控清单

> 自动化收集配置 - 尼克·弗瑞维护  
> 创建时间: 2026-04-21  
> 版本: v1.0

---

## 📋 监控配置概览

| Topic | 优先级 | 当前源数 | 目标源数 | 更新频率 | 状态 |
|:---|:---:|:---:|:---:|:---:|:---:|
| **AI-Native** | P0 | 2 | 15+ | 每日 | 📝 需扩充 |
| **Fintech** | P0 | 5 | 10+ | 每日 | 📝 需扩充 |
| **Knowledge Management** | P1 | 0 | 5+ | 每周 | 📝 待配置 |
| **Analysis Frameworks** | P1 | 0 | 5+ | 每周 | 📝 待配置 |
| **Algorithms** | P2 | 0 | 3+ | 每月 | 📝 待配置 |

---

## 🔬 AI-Native 专题监控

### 子专题划分

| 子专题 | 核心关键词 | 监控重点 | 完成度 |
|:---|:---|:---|:---:|
| **AI Programming** | Vibe Coding, Superpowers, Cursor | 新工具、工作流更新 | ★★★★★ |
| **Agent Engineering** | Multi-Agent, Memory, Tool Use | 框架选型、最佳实践 | ★★★☆☆ |
| **Skill Evaluation** | OpenAI Skill, Auto-grading | 评分系统、评估框架 | ★★★☆☆ |
| **AI Application** | Enterprise AI, Banking AI | 行业落地案例 | ★★★★☆ |
| **Business World Model** | Causal Inference, Ontology | 商业世界建模 | ★★★☆☆ |

### RSS源配置

#### 已配置 (2个)
| 名称 | URL | 频率 | 入库率 |
|:---|:---|:---:|:---:|
| AI News Weekly | https://www.ainewsweekly.com/feed | 每周 | 70% |
| OpenAI Blog | https://openai.com/blog/rss.xml | 不定期 | 90% |

#### 待配置 (13个)

**AI Programming & Vibe Coding**
| 名称 | URL | 优先级 | 理由 |
|:---|:---|:---:|:---|
| Cursor Blog | https://cursor.sh/blog/feed | P0 | Vibe Coding代表工具 |
| Claude Code Updates | https://www.anthropic.com/news/rss.xml | P0 | Agent工程标杆 |
| Vercel AI SDK | https://sdk.vercel.ai/docs/updates | P0 | AI应用开发框架 |
| GitHub Copilot Blog | https://github.blog/tag/copilot/feed | P1 | 主流AI编程助手 |

**Agent Engineering**
| 名称 | URL | 优先级 | 理由 |
|:---|:---|:---:|:---|
| AutoGen Blog (Microsoft) | https://microsoft.github.io/autogen/blog/rss.xml | P0 | Multi-Agent框架领导者 |
| CrewAI Blog | https://www.crewai.com/blog/rss.xml | P0 | 热门Agent编排框架 |
| LangChain Blog | https://blog.langchain.dev/rss.xml | P0 | Agent开发基础设施 |
| Semantic Kernel (Microsoft) | https://devblogs.microsoft.com/semantic-kernel/feed | P1 | 微软Agent SDK |

**Skill Evaluation & AI应用**
| 名称 | URL | 优先级 | 理由 |
|:---|:---|:---:|:---|
| AI Index Report (Stanford) | https://hai.stanford.edu/news/rss.xml | P1 | AI发展权威指标 |
| CB Insights AI Report | https://www.cbinsights.com/research/rss | P2 | 商业AI应用趋势 |

### GitHub监控

| 组织/仓库 | 监控重点 | 优先级 |
|:---|:---|:---:|
| microsoft/autogen | Multi-Agent框架更新 | P0 |
| crewAIInc/crewAI | Agent编排功能 | P0 |
| langchain-ai/langchain | 核心功能发布 | P0 |
| anthropic/anthropic-cookbook | 最佳实践更新 | P1 |
| OpenBMB/AgentVerse | Multi-Agent研究 | P1 |

### 关键人物/组织

| 名称 | 平台 | 监控方式 | 优先级 |
|:---|:---|:---|:---:|
| Andrew Ng | Twitter/X | 关键词监控 | P0 |
| Andrej Karpathy | Twitter/X, YouTube | 视频/推文 | P0 |
| Yann LeCun | Twitter/X | 观点跟踪 | P1 |
| Sebastian Raschka | Newsletter | 技术文章 | P1 |
| Chip Huyen | Blog | 系统设计 | P1 |

---

## 💰 Fintech 专题监控

### 子专题划分

| 子专题 | 核心关键词 | 监控重点 |
|:---|:---|:---|
| **消费金融** | 助贷、现金贷、信用卡 | 监管政策、产品创新 |
| **AI+金融** | 智能风控、智能客服、大模型应用 | 落地案例、技术架构 |
| **支付清算** | 数字人民币、跨境支付 | 基础设施、政策动态 |
| **财富管理** | 智能投顾、资产配置 | 监管合规、用户体验 |

### RSS源配置

#### 已配置 (5个)
| 名称 | URL | 频率 | 入库率 |
|:---|:---|:---:|:---:|
| 21世纪经济报道 | https://www.21jingji.com/rss.xml | 每日 | 60% |
| 第一财经 | https://www.yicai.com/rss.xml | 每日 | 70% |
| 金融科技时代 | https://www.fintechinchina.com/feed | 每周 | 80% |
| 银行家杂志 | https://www.thebanker.com/rss | 每月 | 40% |
| 支付百科 | https://www.paybaike.com/feed | 每日 | 50% |

#### 待配置 (5个)

| 名称 | URL | 优先级 | 理由 |
|:---|:---|:---:|:---|
| 零壹财经 | https://www.01caijing.com/rss | P0 | 金融科技深度分析 |
| 看懂经济 | https://www.kandong.com/rss | P0 | 银行业务洞察 |
| 中国金融杂志 | https://www.zgjrzz.com/rss | P1 | 政策权威解读 |
| 消费金融网 | https://www.xffin.com/rss | P1 | 垂直领域动态 |
| 数字人民币 | https://www.dcpec.com/rss | P2 | CBDC专项追踪 |

---

## 📚 Knowledge Management 专题监控

### 核心关注点
- Personal Knowledge Management (PKM) 工具演进
- Second Brain / Zettelkasten 方法论更新
- 企业知识库/知识图谱技术
- 知识管理 + AI 结合（RAG、Embedding检索）

### RSS源配置 (待配置5个)

| 名称 | URL | 优先级 | 理由 |
|:---|:---|:---:|:---|
| Tiago Forte (Second Brain) | https://fortelabs.com/rss | P0 | Second Brain创始人 |
| Andy Matuschak | https://andymatuschak.org/rss | P0 | 知识管理研究者 |
| Obsidian Updates | https://obsidian.md/updates.rss | P0 | 主流PKM工具 |
| Notion Blog | https://www.notion.so/blog/rss | P1 | 协作知识库 |
| Mem.ai Blog | https://get.mem.ai/blog/rss | P1 | AI原生知识管理 |

---

## 🎯 Analysis Frameworks 专题监控

### 核心关注点
- 商业分析方法论更新
- 战略分析框架演进
- 技术雷达/趋势分析方法
- AI辅助分析工具

### RSS源配置 (待配置5个)

| 名称 | URL | 优先级 | 理由 |
|:---|:---|:---:|:---|
| McKinsey Insights | https://www.mckinsey.com/insights/rss | P0 | 顶级咨询公司 |
| BCG Perspectives | https://www.bcg.com/rss | P0 | 战略分析权威 |
| ThoughtWorks Radar | https://www.thoughtworks.com/radar/rss | P1 | 技术趋势分析 |
| Gartner Research | https://www.gartner.com/newsroom/rss | P1 | 行业分析 |
| CB Insights | https://www.cbinsights.com/research/rss | P1 | 创投分析 |

---

## 🔢 Algorithms 专题监控

### 核心关注点
- 因果推断最新研究
- 图神经网络/GNN应用
- 时序预测算法
- 可解释AI (XAI)

### RSS源配置 (待配置3个)

| 名称 | URL | 优先级 | 理由 |
|:---|:---|:---:|:---|
| arXiv cs.LG | https://arxiv.org/rss/cs.LG | P0 | 机器学习最新论文 |
| Papers With Code | https://paperswithcode.com/rss | P0 | 算法+代码实现 |
| Distill.pub | https://distill.pub/rss | P1 | 可视化算法解释 |

---

## ⚙️ 技术实现方案

### 1. RSS采集架构

```
┌─────────────────────────────────────────────────────────────┐
│                    RSS采集系统架构                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  RSS源配置   │  │  定时任务    │  │  去重队列    │      │
│  │  (30+源)     │  │  (每2小时)   │  │  (Redis)     │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                  │                  │             │
│         └──────────────────┼──────────────────┘             │
│                            ▼                                │
│                   ┌─────────────────┐                      │
│                   │  内容处理器    │                      │
│                   │  - 提取TL;DR   │                      │
│                   │  - 分类Topic   │                      │
│                   │  - 评分       │                      │
│                   └────────┬────────┘                      │
│                            │                               │
│              ┌─────────────┼─────────────┐                 │
│              ▼             ▼             ▼                │
│       ┌─────────┐   ┌─────────┐   ┌─────────┐              │
│       │直接入库 │   │待审核   │   │丢弃    │              │
│       │(★★★+)  │   │(★★)     │   │(★)     │              │
│       └─────────┘   └─────────┘   └─────────┘              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 2. 自动化入库标准

| 评分 | 判断标准 | 处理方式 | 时效 |
|:---:|:---|:---|:---:|
| ★★★★★ | 突破性见解/头部厂商实践/独家数据 | 自动入库+立即通知 | <30分钟 |
| ★★★★ | 高质量案例分析/方法论总结/行业趋势 | 自动入库+每日汇总 | <2小时 |
| ★★★ | 有价值但需审核/增量有限/局部相关 | 待审核队列 | 每日批量 |
| ★★ | 参考价值一般/已过时/重复内容 | 暂存观察 | 每周清理 |
| ★ | 无价值/错误信息/误导性内容 | 直接丢弃 | 即时 |

### 3. Topic匹配规则

```yaml
AI-Native:
  keywords: ["AI Agent", "LLM", "大模型", "Vibe Coding", "Multi-Agent", "Skill", "RAG"]
  github_orgs: ["microsoft", "anthropics", "langchain-ai", "crewAIInc"]
  sources: 15
  
Fintech:
  keywords: ["数字银行", "智能风控", "消费金融", "数字人民币", "金融科技", "信贷"]
  sources: 10
  
Knowledge Management:
  keywords: ["PKM", "Second Brain", "Zettelkasten", "Obsidian", "RAG", "知识图谱"]
  sources: 5
```

---

## 📅 实施计划

### Phase 1: 基础配置 (本周)
- [ ] 配置RSS采集系统 (30个源)
- [ ] 部署去重队列 (Redis)
- [ ] 设置定时任务 (每2小时)
- [ ] 建立评分模型

### Phase 2: 自动化入库 (下周)
- [ ] 自动提取TL;DR
- [ ] Topic自动分类
- [ ] 自动评分系统
- [ ] 入库决策逻辑

### Phase 3: 审核队列 (第3周)
- [ ] 待审核队列UI
- [ ] 批量处理工具
- [ ] 审核历史记录
- [ ] 质量反馈闭环

---

## 🎯 成功指标

| 指标 | 当前值 | 目标值 | 时间线 |
|:---|:---:|:---:|:---:|
| RSS源数量 | 7 | 30+ | 2周内 |
| 自动入库率 | 0% | 70%+ | 1个月内 |
| 审核处理时效 | N/A | <24小时 | 1个月内 |
| 内容覆盖率 | 20% | 80%+ | 3个月内 |
| 人工介入率 | 100% | <30% | 3个月内 |

---

**维护者**: 尼克·弗瑞 🕵️  
**最后更新**: 2026-04-21  
**状态**: 📝 实施中
