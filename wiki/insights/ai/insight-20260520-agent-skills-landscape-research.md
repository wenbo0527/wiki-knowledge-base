---
能力框架: #tech-understanding #product-design #data-driven
来源: 深度调研 | 研究时间: 2026-05-20 | 分类: AI Agent / Skill Engineering
Insight ID: insight-20260520-agent-skills-landscape-research
维护者: 尼克·弗瑞 | 更新: 2026-05-20

---

## 📌 执行摘要

**调研目标**：梳理Agent Skills领域的核心论文、工具平台和技术生态

**核心资源**：
1. **arXiv论文** (2605.07358): Agent Skills全景综述
2. **Awesome-Agent-Skills**: 论文配套社区资源库
3. **Skill-insight**: Skill全生命周期管理平台
4. **Skills Radar**: 技术成熟度雷达图

**核心洞察**：
- Agent Skills是Agent落地的关键载体，解决"Procedural Gap"问题
- Skill生命周期四阶段：表示→获取→检索→演化
- Skill超过40-50个后召回率从95%骤降至30%以下
- Skills Radar已追踪31项技术，分布在6大类别

---

## 一、核心论文：Agent Skills全景综述

### 1.1 论文信息

| 字段 | 值 |
|:---|:---|
| **标题** | A Comprehensive Survey on Agent Skills: Taxonomy, Techniques, and Applications |
| **作者** | Yingli Zhou, Wang Shu, Yaodong Su, Wenchuan Du, Yixiang Fang, Xuemin Lin |
| **arXiv** | 2605.07358v1 |
| **时间** | 2026年5月8日 |
| **类别** | Information Retrieval (cs.IR) |

### 1.2 核心定义

**论文对Agent Skill的定义**：

> A reusable procedural artifact that externalizes task-focused know-how: not only what can be done, but also **when to act, how to execute, what heuristics and failure modes matter, and how to judge completion**.

**形式化定义**：
```
S = (M, R, C)

其中：
- M (Main instruction): 主要指令文档，如SKILL.md、SOP、checklist
- R (Resources): 辅助资源，如参考资料、模板、helper scripts
- C (Conditions): 适用条件，如触发描述、元数据、dependencies
```

### 1.3 解决的问题：Procedural Gap

| 问题 | 说明 |
|:---|:---|
| **When** | 何时调用某个能力 |
| **How** | 如何协调多个步骤 |
| **Failure** | 如何处理失败 |
| **Validation** | 如何验证输出 |

### 1.4 生命周期四阶段

| 阶段 | 核心问题 | 代表主题 |
|:---|:---|:---|
| **Skill Representation** | 如何封装程序性知识？ | 文本Skill、代码Skill、混合Skill |
| **Skill Acquisition** | Skill从何而来？ | 人类衍生、经验衍生、任务衍生、语料衍生 |
| **Skill Retrieval & Selection** | 如何选择正确的Skill？ | 稠密/稀疏检索、层级检索、上下文路由 |
| **Skill Evolution** | Skill如何安全演进？ | 修订、验证、策略耦合、信任、版本管理 |

### 1.5 演进流程

```
experience / expertise / corpus / task
            ↓
      Skill Acquisition
            ↓
    Skill Representation
            ↓
   Retrieval + Selection
            ↓
       Execution
            ↓
  Feedback → Validation → Evolution → Governance
```

### 1.6 关键结论

**Agent vs Skills的分工**：
- **Agent**：处理高层意图解释、推理、规划
- **Skills**：形成操作层，使执行可复用、可检查、可组合、可治理

**Skills的重要性**：
- Scalability（可扩展性）
- Robustness（鲁棒性）
- Maintainability（可维护性）

### 1.7 开放挑战

| 挑战 | 说明 |
|:---|:---|
| Quality Control | Skill质量控制 |
| Interoperability | 互操作性 |
| Safe Updating | 安全更新 |
| Long-term Capability | 长期能力管理 |

---

## 二、Awesome-Agent-Skills 资源库

### 2.1 概述

GitHub资源库：https://github.com/JayLZhou/Awesome-Agent-Skills

**定位**：论文配套的社区资源收集，包含：
- 代表性论文
- Benchmark和评估协议
- 平台和仓库（发现、共享、治理Skills）
- 应用场景

**Star**: 54

### 2.2 论文分类体系

#### 0. 基础设施层

**工具、协议、检索、记忆**

| 论文/技术 | 出处 | 说明 |
|:---|:---|:---|
| Toolformer | NeurIPS 2023 | 工具学习 |
| ReAct | ICLR 2023 | 推理+行动 |
| HuggingGPT | arXiv 2023 | LLM作为控制器 |
| ToolLLM | arXiv 2023 | 工具学习 |
| **MCP** | Anthropic 2024 | Model Context Protocol |
| Function Calling | OpenAI 2023 | 函数调用 |
| RAG | NeurIPS 2020 | 检索增强生成 |
| DPR | EMNLP 2020 | 稠密检索 |
| MemGPT | arXiv 2023 | 记忆管理 |
| Think-in-Memory | arXiv 2023 | 思考记忆 |
| EverMemOS | arXiv 2026 | 持久记忆操作系统 |
| HyperMem | arXiv 2026 | 超记忆 |

#### 1. Skill Representation（技能表示）

**Text-Based Skills**：

| 论文 | 出处 | 说明 |
|:---|:---|:---|
| Reflexion | NeurIPS 2023 | 语言强化 |
| ExpeL | AAAI 2024 | 经验学习 |
| Buffer of Thoughts | NeurIPS 2024 | 思维缓冲 |
| Trace2Skill | arXiv 2026 | 轨迹到技能 |
| Ctx2Skill | arXiv 2026 | 上下文到技能 |

**Code-Backed Skills**：

| 论文 | 出处 | 说明 |
|:---|:---|:---|
| Voyager | NeurIPS 2023 | Minecraft中的终身Agent |
| SkillCraft | arXiv 2026 | 技能工艺 |
| PolySkill | ICLR 2026 | 多技能 |
| Inducing Programmatic Skills | arXiv 2025 | 程序化技能 |

**Hybrid Skills**：

| 论文 | 出处 | 说明 |
|:---|:---|:---|
| JARVIS-1 | TPAMI 2025 | 多模态Agent |
| Synapse | ICLR 2024 | 神经-符号混合 |

#### 2. Skill Acquisition（技能获取）

| 获取方式 | 说明 | 代表工作 |
|:---|:---|:---|
| **Human-derived** | 专家知识提取 | 手工编写SKILL.md |
| **Experience-derived** | 从执行经验学习 | Trace2Skill, Reflexion |
| **Task-derived** | 从任务分解获得 | AutoGen, LangGraph |
| **Corpus-derived** | 从语料库学习 | RAG, Knowledge Bases |

#### 3. Skill Retrieval & Selection（技能检索与选择）

| 技术 | 说明 |
|:---|:---|
| Dense Retrieval | 向量语义检索 |
| Sparse Retrieval | 关键词检索（BM25） |
| Generative Retrieval | 生成式检索 |
| Hierarchy/Graph | 层级/图结构检索 |
| Context-Aware Routing | 上下文感知路由 |
| Composition | 技能组合 |

#### 4. Skill Evolution & Governance（技能演化与治理）

| 方向 | 说明 |
|:---|:---|
| Revision | 持续修订 |
| Validation | 验证正确性 |
| Policy Coupling | 策略耦合 |
| Repository Evolution | 仓库演进 |
| Trust | 信任机制 |
| Rollback | 回滚能力 |
| Deprecation | 废弃管理 |

### 2.3 相关综述

| 论文 | 出处 | 主题 |
|:---|:---|:---|
| A Systematic Survey of Self-Evolving Agents | TechRxiv 2026 | 自主演进Agent |
| Externalization in LLM Agents | arXiv 2026 | Agent中的外部化 |
| SoK: Agentic Skills | arXiv 2026 | 技能系统化研究 |

---

## 三、Skill-insight 平台

### 3.1 概述

**项目地址**：https://gitcode.com/openeuler/witty-skill-insight

**定位**：基于Agent生态的Skill生成优化与评估平台

**Slogan**：让Agent的Skill从"能用"到"好用"

**Star**: 36 | Fork: 33

### 3.2 为什么需要Skill-insight

| 问题 | 说明 |
|:---|:---|
| **Skill越多越不好用** | 相似文档生成大量冗余Skill，研究表明Skill超过40-50个后召回率从95%骤降至30%以下 |
| **执行过程看不见** | 评测只看"任务是否完成"，即使结果正确也可能跳过了关键步骤，埋下隐患 |
| **优化靠猜测** | 没有执行数据支撑，只能基于结果反复试错，无法定位具体瓶颈 |

### 3.3 核心能力

#### 🔨 Skill生成

- 一句话快速生成Skill
- 批量生成时自动去冗余、合相似、抽模式，减少Skill膨胀
- 支持从Markdown、PDF、目录、URL等多种数据源输入

#### 📊 多维评测与执行追溯

| 维度 | 指标 |
|:---|:---|
| **效果** | 准确率、Skill召回率、Skill提升率 |
| **效率** | 时延、调用次数 |
| **成本** | Token、模型费用、CPSR |

- 自动生成执行流程图，与Skill预期流程逐步对比，标识偏离、冗余与跳过
- 支持从Skill、框架、模型、任务四个维度交叉对比分析

#### 🔄 数据驱动的Skill自优化

- 基于评测归因结果，自动定位Skill缺陷并针对性修补
- 区分Skill设计问题与模型能力问题，避免"改错方向"
- 形成 **评测→归因→优化→再评测** 的持续改进闭环

### 3.4 支持框架

| Agent框架 | 采集方式 |
|:---|:---|
| **OpenCode** | 原生插件 |
| **Claude Code** | 日志旁路 |
| **OpenClaw** | 日志旁路 |

### 3.5 核心架构

```
┌─────────────────────────────────────────────────────────┐
│                  Skill-insight 架构                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │ Skill生成   │    │  执行采集   │    │  多维评测   │  │
│  │ Generation  │    │ Collection  │    │ Evaluation  │  │
│  └─────────────┘    └──────┬──────┘    └─────────────┘  │
│                            │                             │
│                            ▼                             │
│                    ┌─────────────┐                       │
│                    │  执行追溯   │                       │
│                    │ Trace Graph │                       │
│                    └──────┬──────┘                       │
│                            │                             │
│                            ▼                             │
│                    ┌─────────────┐                       │
│                    │  归因分析   │                       │
│                    │ Attribution │                       │
│                    └──────┬──────┘                       │
│                            │                             │
│                            ▼                             │
│                    ┌─────────────┐                       │
│                    │ Skill优化   │                       │
│                    │ Optimizer  │                       │
│                    └─────────────┘                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 3.6 技术特点

| 特点 | 说明 |
|:---|:---|
| **全生命周期闭环** | 生成→评测→优化→再评测 |
| **执行过程可视化** | 自动生成执行流程图 |
| **多维度评测** | 效果、效率、成本全覆盖 |
| **归因分析** | 区分Skill问题vs模型问题 |
| **批量去重** | 合相似、抽模式、防膨胀 |

---

## 四、Skills Radar 技术雷达

### 4.1 概述

**网站**：https://mangooai.github.io/skills-radar/

**定位**：追踪Skills技术，让Agent能力进化有迹可循

**数据**：
- 31项已收录技术
- 12项成熟期
- 17项成长期
- 2项探索期

### 4.2 六阶段技术分类

```
Skill生成 → Skill召回 → Skill执行 → Skill评测 → Skill优化 → Skill管理
  🏗️           🎯           ⚙️          📏         🚀         🛡️
```

| 阶段 | 成熟度 | 技术数量 |
|:---|:---:|:---:|
| Skill生成 | 🟡 成长期 | 6 |
| Skill召回 | 🟢 成熟期 | 5 |
| Skill执行 | 🟡 成长期 | 5 |
| Skill评测 | 🟢 成熟期 | 5 |
| Skill优化 | 🟡 成长期 | 5 |
| Skill管理 | 🟡 成长期 | 5 |

### 4.3 各阶段核心技术

#### 🏗️ Skill生成（Generation）- 0.51 成长期

| 技术 | 描述 | 评分 |
|:---|:---|:---:|
| Trace2Skill | 从执行轨迹中自动提取可复用技能 | 0.53 |
| D2Skill | 双粒度动态技能库，驱动策略-技能协同进化 | 0.51 |
| SkillX | 为Agent打造自动化构建、可复用的Skill库 | 0.44 |
| Memento-Skills | 让Agent自主设计Skill，实现自我进化 | 0.47 |
| SKILLRL | 通过技能的强化学习促进Agent自进化 | 0.49 |

#### 🎯 Skill召回（Recall/Routing）- 0.63 成熟期

| 技术 | 描述 | 评分 |
|:---|:---|:---:|
| SkillRouter | 破解大规模Skills选择难题的新范式 | 0.68 |
| SkillOrchestra | 基于技能的Agent路由策略，提升22.5% | 0.67 |
| Graph of Skills | 千级规模Skill库的结构感知检索方案 | 0.62 |
| AgentSkillOS | 生态级规模下技能的组织、编排与基准测试 | 0.61 |
| SkillNet | 创建、评估与连接AI技能 | 0.53 |

#### ⚙️ Skill执行（Execution）- 0.56 成长期

| 技术 | 描述 | 评分 |
|:---|:---|:---:|
| 渐进式披露 | 分阶段加载Skill内容，控制Token消耗 | 0.73 |
| SkVM | 给Skills做个编译器，一次编写，到处运行 | 0.50 |
| 执行流图 | 可视化Skill执行路径追踪 | 0.58 |
| Permission Sandboxing | Skill执行时的安全沙箱隔离 | 0.53 |
| Skill Pipeline | 多Skill协同的并行调度 | 0.44 |

#### 📏 Skill评测（Evaluation）- 0.63 成熟期

| 技术 | 描述 | 评分 |
|:---|:---|:---:|
| **Skill-insight** | 多维评测、执行追溯、归因分析 | **0.78** |
| SkillsBench | 衡量智能体技能在多样化任务中的表现的基准测试 | 0.63 |
| SkillProbe | 用Skill审计Skills安全漏洞 | 0.61 |
| Cross-Evaluation | 多Skill、多模型、多任务横向对比 | 0.53 |
| agent-skills-eval | Agent Skills评测框架，with_skill vs without_skill对比测试 | 0.61 |

#### 🚀 Skill优化（Optimization）- 0.56 成长期

| 技术 | 描述 | 评分 |
|:---|:---|:---:|
| **Skill-insight Optimizer** | 基于归因结果的自动修复 | 0.66 |
| SkillForge | 让企业级Agent Skills实现自主进化 | 0.53 |
| Iterative Optimizer | 多次评测-优化-再评测闭环 | 0.58 |
| SkillReducer | 为Skills瘦身40%，破解Token低效难题 | 0.51 |
| D2Skill | 根据模型能力动态调整Skill策略 | 0.51 |

#### 🛡️ Skill管理（Management）- 0.47 成长期

| 技术 | 描述 | 评分 |
|:---|:---|:---:|
| Agent Skills 标准 | 跨平台的Skill格式与协议标准 | 0.62 |
| Git-based Versioning | 基于Git的Skill版本控制 | 0.52 |
| AgentSkillOS | 生态级技能的组织、编排与生命周期管理 | 0.46 |
| SkillNet | 创建、评估与连接AI技能 | 0.40 |
| RBAC Permission | 基于角色的Skill权限管控 | 0.34 |

### 4.4 评分维度

| 维度 | 权重 | 说明 |
|:---|:---:|:---|
| **技术成熟度** | 30% | 概念验证到大规模应用的演进程度 |
| **创新性** | 25% | 技术的原创性和前沿程度 |
| **落地程度** | 25% | 在实际产品/项目中的应用广度 |
| **生态活跃度** | 20% | 社区贡献者数量、更新频率 |

### 4.5 成熟度分级

| 级别 | 评分范围 | 说明 |
|:---|:---:|:---|
| 🟢 成熟期 | > 0.6 | 已广泛落地，技术稳定 |
| 🟡 成长期 | 0.4 - 0.6 | 快速发展，有成熟应用 |
| 🔴 探索期 | < 0.4 | 早期研究概念 |

---

## 五、关键发现与洞察

### 5.1 核心洞察

**1. Skill是Agent落地的关键载体**

```
论文定义：Skill = 可复用程序性工件
- 解决"When/How/Failure/Validation"问题
- Agent负责高层推理，Skill负责操作执行
```

**2. Skill膨胀是核心痛点**

```
问题：Skill > 40-50个后，召回率从95%→30%
解决：批量去重、合相似、抽模式
工具：Skill-insight Optimizer（-40% Token）
```

**3. Skill生命周期已形成完整闭环**

```
表示 → 获取 → 检索 → 演化
  ↑                   │
  └───────────────────┘
      评测→归因→优化
```

**4. 评测是最成熟领域**

```
Skill-insight (0.78) - 多维评测+归因
SkillsBench (0.63) - Benchmark
SkillRouter (0.68) - 大规模选择
```

**5. 执行层技术评分最高**

```
渐进式披露 (0.73) - Token控制
执行流图 (0.58) - 可视化追踪
Permission Sandboxing (0.53) - 安全隔离
```

### 5.2 与OpenClaw的关联

| Skill Radar阶段 | OpenClaw实践 |
|:---|:---|
| Skill生成 | SKILL.md编写规范 |
| Skill召回 | skill-creator Skill |
| Skill评测 | rss-intelligence每日扫描 |
| Skill管理 | Wiki知识库沉淀 |

### 5.3 推荐关注技术

| 技术 | 评分 | 原因 |
|:---|:---:|:---|
| **Skill-insight** | 0.78 | 最完整的评测+优化闭环 |
| **渐进式披露** | 0.73 | Token控制实用 |
| **SkillRouter** | 0.68 | 解决大规模Skill选择 |
| **Trace2Skill** | 0.53 | 自动化Skill提取 |

---

## 六、行动建议

### 6.1 短期（1-3个月）

1. **完善SKILL.md规范**：参考Skill-insight的M=(M,R,C)结构
2. **建立评测机制**：用SkillsBench建立基线
3. **Skill去重**：检查现有Skill，消除冗余

### 6.2 中期（3-6个月）

1. **执行追溯**：参考Skill-insight，实现执行流程可视化
2. **批量优化**：用SkillReducer优化Token消耗
3. **渐进式披露**：实现Skill内容的分阶段加载

### 6.3 长期（6-12个月）

1. **自动化演进**：参考SkillForge，实现Skill自我进化
2. **归因分析**：区分Skill问题vs模型问题
3. **标准协议**：关注Agent Skills标准发展

---

## 参考资源

| 资源 | 地址 |
|:---|:---|
| 论文 | https://arxiv.org/abs/2605.07358 |
| Awesome-Agent-Skills | https://github.com/JayLZhou/Awesome-Agent-Skills |
| Skill-insight | https://gitcode.com/openeuler/witty-skill-insight |
| Skills Radar | https://mangooai.github.io/skills-radar/ |
| 知乎：Agent Skills全景 | https://zhuanlan.zhihu.com/p/2025509340916794370 |
| 知乎：Skill-insight | https://zhuanlan.zhihu.com/p/2032150871014895927 |
| 知乎：Skills Radar | https://zhuanlan.zhihu.com/p/2038679645248282694 |

