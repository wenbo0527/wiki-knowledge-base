# Harness Engineering 落地实践：多源情报汇总

> 汇总来源：Martin Fowler、Cursor、Philipp Schmid、Latent Space、arxiv论文
> 整理时间：2026-04-17
> 维护者：尼克·弗瑞

---

## 📌 情报概览

| 来源 | 核心信息 |
|------|----------|
| Martin Fowler | Feedforward + Feedback 双层控制框架 |
| Cursor | 递归 Planner-Worker 模型，每小时1000 commit |
| Philipp Schmid | OS for AI 类比 + Bitter Lesson 警示 |
| Latent Space | Big Model vs Big Harness 路线之争 |
| arxiv 2603.05344 | Scaffolding + Harness + Context Engineering 三层架构 |

---

## 1️⃣ Martin Fowler：双层控制框架

### 核心概念：Guides (feedforward) + Sensors (feedback)

```
┌─────────────────────────────────────────────────────────────┐
│                    Harness 控制框架                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Guides (前馈控制)                                           │
│  └── 预测Agent行为，引导其做出好结果                         │
│  └── AGENTS.md、Skills、bootstrap脚本、linter规则            │
│                                                              │
│  Sensors (反馈控制)                                          │
│  └── Agent行动后，帮助其自我修正                              │
│  └── 测试、类型检查、结构分析、AI代码审查                      │
│                                                              │
│  关键洞察：                                                  │
│  • 纯Feedback：Agent重复犯同样错误                           │
│  • 纯Feedforward：Agent不知道规则是否有效                     │
│  • 两者结合：才能形成有效的控制系统                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 计算型 vs 推理型控制

| 类型 | 特点 | 示例 |
|------|------|------|
| **计算型 (Deterministic)** | CPU执行，毫秒级，可靠 | 测试、linter、类型检查 |
| **推理型 (Inferential)** | GPU/NPU执行，较慢，非确定性 | AI代码审查、LLM-as-judge |

### 三类 Harness

| 类型 | 目标 | 难度 |
|------|------|------|
| **Maintainability Harness** | 代码质量、可维护性 | 最容易（有大量现成工具） |
| **Architecture Fitness Harness** | 架构约束、边界检查 | 中等 |
| **Behaviour Harness** | 功能行为正确性 | 最难（目前没有好方案） |

### Keep Quality Left

```
开发阶段 → 集成阶段 → 部署阶段 → 生产运行
    ↑                                        ↑
  Fast Controls                          Continuous Sensors
  (linter, fast tests)                   (dead code, quality monitoring)
```

---

## 2️⃣ Cursor：Self-Driving Codebases

### 架构演进史

| 版本 | 架构 | 问题 |
|------|------|------|
| V1 | 单Agent | 复杂任务扛不住 |
| V2 | 多Agent共享状态文件 | 锁竞争，互相打架 |
| V3 | Planner→Executor→Workers→Judge | 太僵硬，角色过载 |
| V4 | 持续执行器 | 角色过载导致诡异行为 |
| **V5 (最终)** | **递归Planner-Worker** | **通过** |

### 最终架构：递归 Planner-Worker

```
Root Planner (全局视野，不写代码)
    ↓ 细分任务
Sub-Planner (完全拥有 delegated slice)
    ↓
Workers (独立操作，自己copy仓库)
    ↓
Handoff (包含done + notes + concerns + feedback)
    ↓
Planner 接收更新，继续规划
```

**关键设计**：
- Worker之间不通信，不共享状态
- Handoff机制让信息向上传递
- 无需全局同步或跨通信

### Cursor 关键洞察

1. **约束 > 指令**：告诉Agent"不要留TODO"比告诉它"完成所有实现"更有效
2. **具体数字**：说"生成20-100个任务"比说"生成很多任务"效果好
3. **接受错误率**：100%正确率会导致系统停滞，小的错误率可以接受
4. **反脆弱设计**：系统需要能承受单个Agent失败

---

## 3️⃣ Philipp Schmid：OS for AI Agent

### 计算机 vs AI Agent 对应

| 计算机组件 | Agent对应物 | 角色 |
|------------|------------|------|
| CPU | 模型 | 原始算力 |
| 内存 | 上下文窗口 | 有限、易失的工作记忆 |
| **操作系统** | **Agent Harness** | **管理上下文、处理启动、提供标准驱动** |
| 应用程序 | Agent | 跑在操作系统上的用户逻辑 |

### Bitter Lesson 警示

| 案例 | 教训 |
|------|------|
| Manus 6个月重构5次Harness | 别过度工程化 |
| LangChain 1年重架构3次 | 假设会快速淘汰 |
| Vercel 砍掉80%工具 | 简单更好 |

### 关键原则：Build to Delete

> "Make your architecture modular. New models will replace your logic. You must be ready to rip out code."

### The Harness is the Dataset

> "Competitive advantage is no longer the prompt. It is the trajectories your Harness captures."

---

## 4️⃣ Latent Space：路线之争

### Big Model 阵营

| 代表 | 观点 |
|------|------|
| Claude Code团队 | "所有秘密武器都在模型本身，我们追求最薄的包装" |
| Noam Brown | "Harness是拐杖，我们终将超越它" |

**论据**：推理模型出来后，之前搭建的复杂Agent系统一夜之间不需要了。

### Big Harness 阵营

| 代表 | 观点 |
|------|------|
| Jerry Liu (LlamaIndex) | "Model Harness就是一切" |
| Cursor $50B估值 | Harness公司的价值印证 |

**论据**：60%工作中使用AI，但完全委托给AI的任务只有0-20%。差距在Harness，不在模型。

### 护栏悖论

> "车速越快，护栏越重要"

模型越强，越需要精心设计的约束系统。

---

## 5️⃣ arxiv 2603.05344：三层架构

### Scaffolding + Harness + Context Engineering

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent 运行架构                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Scaffolding (脚手架)                                       │
│  └── 预执行阶段组装                                         │
│  └── 系统prompt编译、工具schema构建、sub-agent注册表填充      │
│  └── = 操作系统 BIOS 和引导程序                              │
│                                                              │
│  Harness (运行时编排)                                        │
│  └── 核心推理循环的包装层                                    │
│  └── 协调工具执行、上下文管理、安全执行、会话持久化           │
│  └── = 操作系统内核                                          │
│                                                              │
│  Context Engineering (上下文工程)                            │
│  └── Token预算管理                                           │
│  └── 什么信息该进来、该压缩、该丢弃                          │
│  └── = 操作系统内存管理                                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 公式

```
coding agent = AI model(s) + harness
```

---

## 6️⃣ Stripe Minions：Blueprint 编排

### 混合架构

```
Blueprint 编排 = 确定性节点 + Agentic节点

确定性节点（不调用LLM）：
- 运行 linter
- 推送更改
- 执行固定流程

Agentic节点（调用LLM）：
- 实现功能
- 修复CI失败
- 行使判断
```

### 关键约束

| 规则 | 原因 |
|------|------|
| **CI最多跑两轮** | 防止Agent在错误方向上无限重试 |
| **500工具但Agent只看到子集** | 工具越多越不准 |

---

## 📊 数据对比

| 案例 | 数据 | 关键发现 |
|------|------|----------|
| Nate B Jones | 同一模型，换Harness后42%→78% | Harness提升≈换一代模型 |
| LangChain | 改Harness后52.8%→66.5% | 排名从30+冲进前5 |
| Pi Research | 一下午改Harness提升15个LLM | 标题："Only the Harness Changed" |
| Vercel | 工具15→2，准确率80%→100% | 工具越少越准 |
| Cursor | 每小时1000 commit | 递归Planner-Worker有效 |
| Stripe | 每周1300+ PR | Blueprint编排有效 |

---

## 🏛️ 行业现状总结

### 共识
1. 模型 + Harness = Agent
2. 约束比指令更有效
3. 工具要精简
4. 反馈循环必不可少

### 分歧
1. Harness应该厚还是薄？
2. 最终会被模型替代吗？
3. 多少自主性是合适的？

### 待解决问题
1. Behaviour Harness（功能行为验证）还没有好方案
2. 如何评估Harness覆盖率？
3. Harness与模型更新如何同步？

---

## 🔗 参考资源

| 资源 | 链接 |
|------|------|
| Martin Fowler Harness Engineering | https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html |
| Cursor Self-Driving Codebases | https://cursor.com/blog/self-driving-codebases |
| Philipp Schmid - Agent Harness 2026 | https://www.philschmid.de/agent-harness-2026 |
| Latent Space - Is Harness Real | https://www.latent.space/p/ainews-is-harness-engineering-real |
| Stripe Minions | https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents |
| arxiv 2603.05344 | https://arxiv.org/abs/2603.05344 |

---

*维护者：尼克·弗瑞*
*整理时间：2026-04-17*
*情报等级：🟠机密*
