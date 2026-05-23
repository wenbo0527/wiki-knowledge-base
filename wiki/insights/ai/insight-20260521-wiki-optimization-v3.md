# Wiki知识库优化方案（索引导航 + 体系化内容）

> **版本**: v3.0
> **日期**: 2026-05-21
> **作者**: 尼克·弗瑞
> **场景**: Agent索引导航 / 人类体系化内容
> **状态**: 待执行

---

## 一、背景

### 1.1 问题背景

文博的Wiki知识库面临两个核心问题：

| 问题 | 说明 |
|:---|:---|
| **Agent找知识难** | 20+散落insight，Agent不知道该读哪个 |
| **人类阅读效率低** | insight碎片化，缺乏体系化综述 |

### 1.2 修正后的方向

| 方向 | 说明 | 不是 |
|:---|:---|:---|
| **索引导航** | 给Agent用的Wiki导航索引 | 不是SKILL（无需scripts/） |
| **体系化内容** | 给人类阅读的优化文档 | 不是模板（是内容重组） |

### 1.3 优化目标

- **Agent**：快速找到所需知识，执行任务
- **人类**：快速理解核心要点，降低阅读成本

---

## 二、方向一：索引导航

### 2.1 设计原则

| 原则 | 说明 |
|:---|:---|
| **按场景索引** | 不按文档类型，按Agent执行场景 |
| **执行路径清晰** | 场景→文档→步骤 |
| **渐进式** | 先索引高频场景，再扩展 |

### 2.2 索引结构

```
Wiki/INDEX/
├── index.md              # 导航总入口（所有Topic索引）
├── agent/
│   ├── design-patterns.md # Agent设计模式索引
│   ├── evaluation.md     # Agent评估体系索引
│   ├── skills.md         # Agent Skill工程索引
│   ├── harness.md        # Harness工程索引
│   └── memory.md         # 记忆架构索引
├── product/
│   └── pm-workflow.md    # 产品管理流程索引
└── fintech/
    └── overview.md       # 金融科技索引
```

### 2.3 索引文档结构

```markdown
# {Topic} 索引导航

> **版本**: v1.0
> **更新**: 2026-05-21
> **维护者**: 尼克·弗瑞

## 能力地图

| 场景 | 索引文档 | 说明 |
|:---|:---|:---|
| 场景A | path/to/docA.md | 核心参考 |
| 场景B | path/to/docB.md | 进阶参考 |

## 执行路径

### 场景：{场景名称}
**触发条件**：{什么情况下使用这个路径}

**步骤**：
1. 先读 {文档A} 的 {章节}
2. 再读 {文档B} 的 {章节}
3. 执行 {具体操作}

**注意事项**：
- {避坑提示}
```

### 2.4 Agent索引示例

```markdown
# Agent Design Patterns 索引导航

> **版本**: v1.0
> **更新**: 2026-05-21

## 能力地图

| 场景 | 索引文档 | 说明 |
|:---|:---|:---|
| 多Agent协作 | insights/agent/multi-agent-architecture-guide.md | Supervisor/Chain模式 |
| 上下文管理 | insights/agent/agent-memory-architecture.md | Core Memory设计 |
| Skill工程 | insights/agent/skillos.md | 渐进式披露 |
| 评估体系 | insights/agent/agent-evaluation-review.md | 四维评分模型 |
| 长任务治理 | insights/agent/agent-design-pattern-review.md | Checkpoint机制 |

## 执行路径

### 场景：需要设计多Agent协作
**触发条件**：用户说"多Agent"、"协作"、"Supervisor"

**步骤**：
1. 先读 `insights/agent/multi-agent-architecture-guide.md` 的"核心模式"章节
2. 再读 `insights/agent/harness-engineering/` 目录的"协作模式"
3. 参考 `insights/ai/insight-20260419-anthropic-multi-agent-patterns.md`

**注意事项**：
- 单Agent能完成就不用多Agent
- 上下文污染问题见 memory.md

### 场景：需要评估Agent能力
**触发条件**：用户说"评估"、"评测"、"benchmark"

**步骤**：
1. 读 `insights/agent/agent-evaluation-review.md` 的"评估框架"章节
2. 对照 `code-examples/skills/SKILL_EVALUATION.md` 的四维模型
3. 使用 `wiki/code-examples/skills/SKILL_SCORING_REPORT.md` 评分

### 场景：需要构建Agent Skill
**触发条件**：用户说"Skill"、"技能"、"编写Skill"

**步骤**：
1. 读 `insights/agent/skillos.md` 的"渐进式披露"章节
2. 参考 `insights/agent/agent-skills/skill-design.md`
3. 用 SKILL.md 模板编写
```

---

## 三、方向二：体系化内容

### 3.1 设计原则

| 原则 | 说明 |
|:---|:---|
| **整合碎片** | 将散落insight整合为综述 |
| **结论先行** | TL;DR + 关键洞察在前 |
| **结构清晰** | 目录 + 层级标题 |
| **持续更新** | 与新insight保持同步 |

### 3.2 综述文档结构

```markdown
# {Topic}综述

> **TL;DR**: 一句话总结核心观点

## 关键洞察
- 洞察1（来源：insight-A）
- 洞察2（来源：insight-B）
- 洞察3（来源：insight-C）

## 目录
- [背景](#背景)
- [核心框架](#核心框架)
- [最佳实践](#最佳实践)
- [实施建议](#实施建议)
- [相关文档](#相关文档)

---

## 背景
[背景说明，为什么重要]

## 核心框架
### 1. {框架名称}
[整合自多个insight的核心内容]

### 2. {框架名称}
[整合自多个insight的核心内容]

## 最佳实践
### 实践1
[案例 + 来源insight]

### 实践2
[案例 + 来源insight]

## 实施建议
1. [步骤1]
2. [步骤2]
3. [步骤3]

## 相关文档

| 文档 | 说明 | 来源 |
|:---|:---|:---|
| [docA.md](path) | 详细参考 | insight-A |
| [docB.md](path) | 详细参考 | insight-B |

---

*维护者: 尼克·弗瑞*
*最后更新: {日期}*
*版本: v1.0*
```

### 3.3 综述文档优先级

| 优先级 | 综述文档 | 覆盖insight数 | 说明 |
|:---:|:---|---:|:---|
| 🔴 | Agent设计模式综述 | 20+ | Agent核心能力 |
| 🔴 | Agent评估体系综述 | 10+ | 决策依据 |
| 🟠 | Harness工程综述 | 8+ | 技术底座 |
| 🟠 | 产品管理流程综述 | 6+ | 日常参考 |
| 🟡 | 金融科技综述 | 10+ | 行业背景 |

### 3.4 综述示例（Agent设计模式）

```markdown
# Agent设计模式综述

> **TL;DR**: Agent设计模式分为三层（协作层/执行层/记忆层），核心原则是"单Agent优先"。

## 关键洞察
- 多Agent适用场景：独立调查/上下文污染/只读vs写/依赖关系/结果合并
- 上下文污染解决：Subagent上下文卫生管理（独立session/定期checkpoint）
- 记忆架构选择：按任务复杂度选择（core memory → vector store → temporal graph）

## 核心框架

### 1. 协作层：多Agent模式

| 模式 | 适用场景 | 文档 |
|:---|:---|:---|
| Supervisor | 任务分发+结果汇总 | multi-agent-architecture-guide.md |
| Chain | 顺序执行+依赖传递 | multi-agent-architecture-guide.md |
| Parallel | 独立任务+并行处理 | multi-agent-architecture-guide.md |

### 2. 执行层：Harness工程

| 组件 | 说明 | 文档 |
|:---|:---|:---|
| Planning | 任务拆解 | agent-harness-context-management.md |
| Tool | 工具调用 | harness-agent.md |
| Reflection | 自我检查 | agent-harness-context-management.md |

### 3. 记忆层：上下文管理

| 架构 | 适用场景 | 文档 |
|:---|:---|:---|
| Core Memory | 单Agent/简单任务 | agent-memory-architecture.md |
| Vector Store | 知识检索 | agent-memory-architecture.md |
| Temporal Graph | 时序关系 | agent-memory-architecture.md |

## 最佳实践

### 单Agent优先原则
只要单个Agent能干完且体感不差，就别折腾多Agent。
来源：insight-20260419-claude-design.md

### Subagent拆分检查清单
1. 独立调查 → 可以拆
2. 上下文污染 → 风险高，慎拆
3. 只读vs写 → 只读可以拆
4. 依赖关系 → 强依赖不拆
5. 结果合并 → 合并成本高则不拆

## 相关文档

| 文档 | 说明 |
|:---|:---|
| [multi-agent-architecture-guide.md](../agent/multi-agent-architecture-guide.md) | 多Agent架构 |
| [agent-memory-architecture.md](../agent/agent-memory-architecture.md) | 记忆架构 |
| [skillos.md](../agent/skillos.md) | Skill工程 |
| [agent-evaluation-review.md](../agent/agent-evaluation-review.md) | 评估体系 |
```

---

## 四、实施计划

### 4.1 第一阶段：索引导航

| 任务 | 产出 | 优先级 |
|:---|:---|:---:|
| 创建 INDEX/ 目录结构 | 目录 | 🔴 |
| 编写 Agent 索引导航 | agent/index.md | 🔴 |
| 编写 Product 索引导航 | product/index.md | 🟠 |
| 编写 Fintech 索引导航 | fintech/index.md | 🟡 |

### 4.2 第二阶段：体系化内容

| 任务 | 产出 | 优先级 |
|:---|:---:|:---:|
| 整合 Agent设计模式综述 | insights/agent/综述.md | 🔴 |
| 整合 Agent评估体系综述 | insights/agent/综述.md | 🔴 |
| 整合 Harness工程综述 | insights/agent/综述.md | 🟠 |
| 整合 产品管理综述 | insights/product/综述.md | 🟠 |

### 4.3 责任分工

| 任务 | 负责人 |
|:---|:---|
| INDEX目录创建 | 钟离 |
| Agent索引导航编写 | 尼克 |
| 体系化综述整合 | 尼克 |
| 批量文档更新 | 钟离 |

---

## 五、风险与应对

| 风险 | 影响 | 应对 |
|:---|:---|:---|
| **维护成本** | 综述与insight不同步 | 建立更新机制（周更） |
| **索引准确性** | Agent找不到正确文档 | 用文博反馈迭代 |
| **覆盖不全** | 高频场景遗漏 | 先覆盖高频，再扩展 |

---

## 六、文件清单

### 6.1 新建文件

```
Wiki/INDEX/
├── index.md              # 导航总入口
├── agent/
│   ├── design-patterns.md # Agent设计模式索引
│   ├── evaluation.md     # Agent评估索引
│   ├── skills.md         # Agent Skill索引
│   ├── harness.md        # Harness索引
│   └── memory.md         # 记忆架构索引
├── product/
│   └── pm-workflow.md    # 产品管理索引
└── fintech/
    └── overview.md       # 金融科技索引

Wiki/insights/agent/
├── Agent设计模式综述_v2.md    # 整合综述
└── Agent评估体系综述_v2.md    # 整合综述
```

### 6.2 更新文件

| 文件 | 更新内容 |
|:---|:---|
| insights/agent/*.md | 增加TL;DR + 关键洞察 |
| insights/product/*.md | 增加TL;DR + 关键洞察 |

---

*作者: 尼克·弗瑞*
*日期: 2026-05-21*
*状态: 待执行*