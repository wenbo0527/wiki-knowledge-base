# OpenSpec + Superpowers 新项目全流程实战指南

> **情报日期**: 2026-04-21  
> **来源**: 运维有术 / 术哥无界 微信公众号  
> **原文**: https://mp.weixin.qq.com/s/7EpVsLbFznkngJbD7tFA9A  
> **分析师**: 尼克·弗瑞  
> **分类**: AI-Native / AI Programming / Best Practice  
> **关联专题**: [[ai-programming/README|AI编程]] | [[agent-engineering|Agent工程]] | [[skill-evaluation|Skill评估]]

---

## 🎯 核心洞察

### 1. AI编程的通病：上下文不一致

**核心问题**: AI编程助手擅长生成代码，但不擅长维护**上下文一致性**——需求、设计和代码三者之间缺少强制的对齐机制。

**症状**:
- 前后端对不上接口
- 需求改了但代码没同步
- AI助手写着写着就跑偏了

**解决方案**: OpenSpec + Superpowers

```
OpenSpec    →  管「要做什么」（What）
              ↓
         需求规约（结构化Markdown）
              ↓
Superpowers →  管「怎么做」（How）
              ↓
         标准化工程流程（7个Skill）
              ↓
         可运行代码
```

### 2. OpenSpec：用规约当团队的协作契约

**核心理念**: 写代码之前，先把要做什么写清楚，而且要写成**AI可读的格式**。

**不是**: PRD文档那种纯文本
**而是**: 结构化的Markdown文件，AI编程助手可以直接读取、理解、执行

**OpenSpec核心概念**:

```yaml
# OpenSpec 项目结构
openspec/
├── specs/                    # 当前系统的行为描述（真实来源）
│   └── <domain>/
│       └── spec.md          # 用 Given/When/Then 格式定义行为
├── changes/                  # 拟议的修改（每个变更一个文件夹）
│   └── <change-name>/
│       ├── proposal.md      # 意图和范围
│       ├── design.md        # 技术方案
│       ├── tasks.md         # 实现任务清单
│       └── specs/           # Delta 规约（具体变更内容）
└── config.yaml              # 项目配置
```

**关键机制 - Delta Spec**:

```markdown
## ADDED Requirements
- 新增的行为

## MODIFIED Requirements  
- 修改的行为

## REMOVED Requirements
- 废弃的行为
```

类比数据库的 WAL（Write-Ahead Log）：**先记录变更意图，归档时再合并到主规约**。

好处：
- 可以随时回退
- 不会污染原始数据

**DAG依赖管理**:

```
proposal（根节点）
    │
    ├── specs（依赖 proposal）
    │
    ├── design（依赖 proposal）
    │
    └── tasks（依赖 specs + design）
```

不能跳过 proposal 直接写 tasks。AI会按依赖顺序自动生成这些制品。

### 3. Superpowers：让AI编码代理按规矩干活

**核心理念**: 给AI编码代理装上一套**标准化的工作流程**。

**不是**: 简单的代码生成
**而是**: 7个核心工作流，覆盖从需求澄清到代码审查的全流程

**7个核心工作流**:

| 工作流 | 做什么 | 关键价值 |
|:---|:---|:---|
| **brainstorming** | 苏格拉底式对话，写代码之前先理清需求 | 避免后期返工 |
| **using-git-worktrees** | 创建隔离的Git工作空间 | 并行开发不冲突 |
| **writing-plans** | 把工作拆成2-5分钟可完成的小任务 | 可控的进度 |
| **subagent-driven-development** | 用子代理逐任务执行 | 自动化执行 |
| **test-driven-development** | 强制RED-GREEN-REFACTOR循环 | 质量保证 |
| **requesting-code-review** | 自动触发代码审查 | 团队规范 |
| **finishing-a-development-branch** | 完成分支，验证测试 | 干净收尾 |

**子代理驱动开发（Subagent-Driven Development）**:

三级审查层层过滤：

```
第1级：实现子代理
    └── 按TDD循环写代码
        │
        ↓ 完成后自动触发
        │
第2级：规约审查子代理（Spec Reviewer）
    └── 检查代码是否符合设计规约
        │
        ↓ 通过后自动触发
        │
第3级：代码质量审查子代理（Code Quality Reviewer）
    └── 检查代码风格、性能、最佳实践
        │
        ↓ 全部通过
        │
    标记任务完成
```

**关键设计**:
- 每个子代理在**隔离上下文**中运行
- 自动按依赖顺序执行
- 失败时自动重试或人工介入

### 4. OpenSpec + Superpowers 的协作闭环

```
┌─────────────────────────────────────────────────────────────────┐
│                    完整工作流闭环                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   OpenSpec（上游 - 管What）                                       │
│   ─────────────────────                                         │
│   /opsx:propose kanban-board                                    │
│       ↓                                                         │
│   brainstorming → proposal + specs                              │
│       ↓                                                         │
│   细化设计文档 → design + tasks                                 │
│       ↓                                                         │
│   拆分实现计划 → 子代理逐任务实现                                │
│       ↓                                                         │
│   /opsx:apply                                                   │
│       ↓                                                         │
│   规约审查 + 代码审查                                           │
│       ↓                                                         │
│   实现任务 → TDD循环                                            │
│       ↓                                                         │
│   完成分支                                                      │
│       ↓                                                         │
│   /opsx:archive                                                 │
│       ↓                                                         │
│   合并Delta Spec → specs/更新                                   │
│                                                                  │
│   Superpowers（下游 - 管How）                                    │
│   ────────────────────────                                       │
│   7个工作流 + 3级审查 + 子代理驱动                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

关键洞察:
1. OpenSpec的产物就是Superpowers的输入
2. 通过文件系统中的Markdown文件完成握手
3. 不依赖任何API调用或网络通信
4. 上游管What，下游管How，解耦但连贯
```

---

## 🔧 实战要点

### 衔接点一：tasks.md → writing-plans

- OpenSpec生成的tasks.md是**粗粒度**的任务清单
- Superpowers通过writing-plans技能拆成更细的实现步骤
- 每一步2-5分钟可完成

### 衔接点二：design.md → subagent-driven-development

- OpenSpec的design.md是技术方案
- Superpowers的子代理在写代码时会读取这份文档来理解上下文
- 确保代码实现与设计一致

### 衔接点三：specs/ → requesting-code-review

- Superpowers做代码审查时，把OpenSpec的行为规约当作审查标准
- 代码是否合规约，不是人说了算，是spec说了算

---

## 💡 核心洞察：AI时代的组织重构

### 角色坍缩：我们还需要前端和后端吗？

**判断**: 严格的前后端分工，正在被AI工具消解。

**理由**:
1. Superpowers的子代理可以同时处理后端API和前端组件——因为两者基于同一份spec.md。AI不关心自己是写后端还是写前端，只关心spec说了什么。
2. 这带来一个有意思的变化：**技术壁垒从会不会写代码变成了会不会写规约**。
3. 以前，前端工程师不碰后端，是因为不熟悉数据库设计、API框架、部署流程。但现在，只要spec.md把API行为描述清楚，AI就能生成后端代码。同理，后端工程师不需要懂React状态管理，AI能基于spec生成前端组件。

**限定**: 
- AI抹平的是**实现层**的壁垒，不是**设计层**的判断力。
- 知道什么时候用WebSocket而不是REST、什么时候需要乐观更新、怎么设计数据模型才能扛住未来半年的需求变化——这些决策能力，AI目前替代不了。

**更准确的说法**: 前后端的**技能分工**在坍缩，但**思维分工**还在。
- 懂用户交互思维的人和懂数据建模思维的人，依然有价值，只是他们不再需要用不同的编程语言来实现各自的想法。

### 协作进化：3人组会变成2人组吗？

**趋势判断**: 传统的前端 + 后端 + 架构师三人组，会逐渐演变为**架构师 + AI工具操作者**的两人结构。

**理由三点**:

**1. 规约成为核心资产。**
OpenSpec的设计哲学——Fluid not rigid（灵活而非死板）——指向一个趋势：**规约文件本身就是团队的核心知识资产**。谁控制规约，谁就控制了产品方向。架构师的角色从「画架构图给别人看」变成「写规约让AI执行」。

**2. AI工具的操作门槛在快速降低。**
Superpowers把写代码这件事标准化成了7个工作流。一个理解业务逻辑的人，即使编码能力一般，也能通过AI助手完成高质量的全栈实现。

**3. 并行开发的效率提升是实在的。**
前后端基于同一份规约同时开工，AI自动保证一致性，沟通成本大幅下降。

**风险点**: 如果项目的业务逻辑足够复杂，AI生成的代码可能需要大量人工审查和修正。这时候一个人操作AI反而成为瓶颈——审查速度跟不上生成速度。

**建议**: 
> 先别急着裁人。先试试让现有的架构师用OpenSpec管理需求，让一个开发者用Superpowers做全栈实现。跑一轮完整流程后，你自然知道团队需要几个人。

**核心洞察**: 
> 工具改变的是做事的方式，不是做事的人。能定义清楚问题的人，永远比只会执行方案的人稀缺。OpenSpec + Superpowers这套工具链，只是让这个事实暴露得更明显了。

---

## 🔗 关联资源

| 类型 | 资源 | 链接/说明 |
|:---|:---|:---|
| 工具 | OpenSpec | npm install -g @fission-ai/openspec@latest |
| 工具 | Superpowers | /plugin install superpowers@claude-plugins-official |
| 作者 | 术哥无界 | 运维有术 / 术哥无界 微信公众号 |
| 系列 | AI编程最佳实战「2026」系列 | 第19篇（本文） |
| 关联专题 | Vibe Coding | [[vibe-coding/README|Vibe Coding专题]] |
| 关联专题 | Agent Engineering | [[agent-engineering|Agent工程]] |
| 关联专题 | Skill Evaluation | [[skill-evaluation|Skill评估]] |

---

**维护者**: 尼克·弗瑞 🕵️  
**最后更新**: 2026-04-21  
**状态**: ✅ 已入库

**标签**: #OpenSpec #Superpowers #AIProgramming #Agent #BestPractice #VibeCoding
