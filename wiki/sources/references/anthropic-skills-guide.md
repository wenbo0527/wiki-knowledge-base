# Anthropic Skills指南：让AI稳定干活的方法论

## 基本信息
- **来源**: 微信公众号（架构师 JiaGouX）
- **URL**: https://mp.weixin.qq.com/s/p3eEVXS6sFZ8gC4upRByJQ
- **原始PDF**: https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf
- **主题**: Anthropic官方Skills构建方法论

## 核心概念

### Skill vs MCP
| 层级 | MCP | Skill |
|------|-----|-------|
| **解决的问题** | AI能连什么工具 | 连上之后怎么把事办成 |
| **本质** | 基础设施层（厨房） | 知识层（菜谱） |
| **功能** | 提供实时数据访问和工具调用 | 固化工作流与最佳实践 |

> "Without skills: Users connect your MCP but don't know what to do next." 
> — 用户把MCP连上了，但发工单问"接下来干嘛"。

### Skill是什么
Skill是一组指令，打包成一个简单文件夹，用来教Claude处理特定任务或工作流。

类比：Skill是给AI的SOP。就像团队新人来了给他一份SOP，而不是每次从零解释。

**适合场景**：
- 有一套重复做的事（写周报、代码评审、投研报告、PRD、排障复盘）
- 有明确的流程和质量标准
- 希望输出稳定，不想每次碰运气

**不适合场景**：
- 灵机一动的提问
- 一次性的简单任务

## 三层渐进式披露（Progressive Disclosure）

这是整套Skill机制的灵魂。

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 1: YAML frontmatter                                  │
│  永远加载，只放最轻量信息——"我是谁，什么时候该用我"          │
├─────────────────────────────────────────────────────────────┤
│  Layer 2: SKILL.md 正文                                     │
│  只有Claude判断"相关"时才加载                                │
│  放具体步骤、模板、排错指南                                  │
├─────────────────────────────────────────────────────────────┤
│  Layer 3: references/、assets/、脚本                        │
│  只有真正需要时才打开                                        │
└─────────────────────────────────────────────────────────────┘
```

**设计直觉**：把"决策信息"做轻，把"执行细节"延迟加载。像代码的核心接口稳定、实现细节按需引入。也像前端的懒加载。

**硬性建议**：SKILL.md控制在5000词以内。写不下就挪到references/。

## description写法（最关键）

> ⚠️ description写废了，整个Skill就废了。

Claude不是看完整个Skill来决定是否使用，只看frontmatter里的description字段——几十个字就决定了被调用还是被无视。

### 必须同时回答两个问题
1. **What**：这个skill做什么
2. **When**：什么时候应该触发（用用户会说的话，不是技术术语）

### 好坏的例子

**坏（官方点名批评）**：
```
description: Helps with projects.
# 太泛，等于没写
```

```
description: Implements the Project entity model with hierarchical relationships.
# 太技术，用户不会这么说话
```

**好**：
```
description: Analyzes Figma design files and generates developer handoff documentation. 
Use when user uploads .fig file.
```

### 原则
> 把description当成产品的**入口文案**来写，别当成技术说明书。

## Skill设计原则

### 1. 可组合
Claude可能同时加载多个skill，你写的skill不能假设"自己是唯一规则"。

### 2. 可移植
同一套skill可以在Claude.ai、Claude Code、API上工作，不需要分别适配。

### 3. 最小可用格式
```yaml
---
name: your-skill-name
description: What it does. Use when user asks to [specific phrases].
---
```

## 与OpenClaw的关联

这个Skills框架和OpenClaw的Agent技能系统高度相关：
- OpenClaw的SKILL.md就是类似的设计
- Progressive Disclosure的理念可以应用到Agent的记忆分层
- description即"入口文案"的概念对Agent的HEARTBEAT.md编写有指导意义

## 相关主题
- [[agent-engineering]] - Agent工程
- [[ai-programming]] - AI编程实践

## 标签
#Anthropic #Skills #MCP #AI开发方法论 #Agent
