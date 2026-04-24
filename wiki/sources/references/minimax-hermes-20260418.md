# MiniMax × Hermes：模型与Harness的双进化

> 来源：Datawhale公众号
> 发布时间：2026-04-18
> 原始链接：https://mp.weixin.qq.com/s/Nvq1umaa85vW-wwtfH95bA

## 核心摘要

本文通过对比不同AI Assistant的开场白设计，揭示了从"Prompt-Response单轮交互"到"持续运行任务框架"的范式转变，并深入分析了MiniMax与Hermes Agent团队的合作，以及MaxHermes如何实现模型与Harness的双进化。

## 关键观点

### 1. 产品哲学的演变

| 产品 | 开场白 | 背后的假设 |
|------|--------|-----------|
| ChatGPT | "Ask anything" | 价值在一问一答里 |
| DeepSeek | "给DSeek发送信息" | 简化交互 |
| OpenClaw | 无提示 | 假设你已经懂 |
| MaxHermes | "我们一起做事" | 价值在执行链条里 |

**核心转变**：从"单轮prompt-response"到"持续执行链条"

### 2. Harness的核心作用

> "模型像引擎，Harness更像机甲本身。只有引擎，能力再强也只是空转；真正让模型进入现实任务的，是外面这层系统。"

**Harness解决的四大问题**：
1. 记忆管理
2. 工具调用
3. 任务状态
4. 用户反馈

### 3. MaxHermes的独特能力

**自我进化机制**：
```
对话 → Skill沉淀 → 记忆增强 → 下一轮更懂你
```

**实测案例**：GitHub Repo分析
1. 第一轮：完成分析任务
2. 第二轮：用户要求先输出框架图再分析
3. 第三轮：用户要求将流程沉淀为Skill
4. 验证：发送新链接，MaxHermes自动调用已创建的Skill

### 4. MiniMax M2.7的技术特性

| 指标 | 数据 |
|------|------|
| RL Pipeline自动化率 | 70-80%由模型+Agent自主完成 |
| Skill Adherence | 97%（40+复杂Skill，2000+Token环境） |
| 人类参与 | 仅"判断与品味"测试 |

**迭代系统的核心理念**：
> "Human steer at every layer, Models build at every layer"

### 5. 模型+Harness双进化飞轮

```
┌─────────────────────────────────────────────────────────────┐
│                    双进化飞轮                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Hermes（经验沉淀）  ←→  M2.7（经验吸收）                   │
│        ↓                        ↓                           │
│   Skill/记忆积累         模型能力提升                        │
│        ↓                        ↓                           │
│   真实任务暴露问题  ←→  更高能力上限                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 与现有Wiki内容的关联

| Wiki专题 | 关联点 |
|----------|--------|
| `agent-engineering.md` | Harness定义、类型、失败模式 |
| `harness-engineering-deep-research.md` | Martin Fowler框架 |
| `claude-code-agent-farm.md` | 多Agent编排实战 |
| OpenClaw相关 | OpenClaw作为破冰产品 |

## 补充Insight

**新视角**：
- Harness不仅是舞台，更是与模型互相塑造的训练信号
- 自我进化的Harness + 自我进化的模型 = 相辅相成的关系
- 未来竞争焦点从"单次benchmark"转向"双向进化能力"

**实践启示**：
1. AI Agent产品设计应关注"长期使用中的能力沉淀"
2. 评价标准从"单次表现"转向"持续进化能力"
3. 模型与框架的匹配度影响最终能力上限

---
*归档时间：2026-04-22*
*来源：Datawhale公众号*
