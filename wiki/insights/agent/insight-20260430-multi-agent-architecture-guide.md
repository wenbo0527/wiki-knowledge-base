# Insight: 多智能体架构设计指南 - 从上下文边界到协作模式

> 原始链接: https://mp.weixin.qq.com/s/LNkT_xRhdh2iCxBQcVKpUQ
能力框架: capability-value-closed-loop capability-tech-understanding #capability-data-driven

> **来源**: 微信公众号 · AI前线
> **原始链接**: https://mp.weixin.qq.com/s/LNkT_xRhdh2iCxBQcVKpUQ
> **评级**: ⭐⭐⭐⭐⭐ (5/5)
> **标签**: Multi-Agent, Sub-Agent, Agent Team, 架构设计
> **存储时间**: 2026-04-30

---

## 核心发现

**Suryansh Tiwari的核心洞察**：
> "真正决定架构的是任务需要的协作方式，而非智能体数量"

多智能体架构的关键不是"拆分为几个角色"，而是**子任务之间是否共享上下文**。

---

## 两种主流架构模式对比

### Sub-Agent：隔离式并行架构

**工作流**：
1. 父代理（Parent Agent）分配任务
2. 子代理（Sub-Agent）独立执行
3. 仅返回结论（无中间过程）

**关键约束**：
- 子代理间**无直接通信**
- **不可再生新Agent**
- 流量需经父代理中转

**核心价值**：
| 价值 | 说明 |
|------|------|
| **隔离** | 避免子任务中间过程污染父上下文窗口 |
| **压缩** | 将复杂探索过程提炼为结构化结论 |
| **并行** | 多任务独立并发执行 |

**代码示例**：
```python
async def main():
    async for message in query(
        prompt="Review the authentication module for issues",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Grep", "Glob", "Agent"],
            agents={
                "security-reviewer": AgentDefinition(
                    description="Find vulnerabilities and security risks",
                    model="sonnet",
                ),
                "performance-optimizer": AgentDefinition(
                    description="Identify performance bottlenecks",
                    model="sonnet",
                ),
            },
        ),
    ):
        print(message)
```

### Agent Team：共享式协作架构

**工作流**：
- 通过**共享任务/状态层**实时同步进度
- 成员（Lead+Mates）点对点通信
- 动态调整任务执行

**适用场景**：
- 强依赖任务（如软件项目开发）
- 前端接口变更需后端即时感知
- 测试失败需开发同步上下文

**实现成本**：
- 状态共享（冲突处理、版本化）
- 通信协议
- Lead仲裁机制
- 调试复杂度高

---

## 常见架构误区

| 按角色拆分（错误） | 按上下文边界拆分（正确） |
|-------------------|------------------------|
| Planner→Developer→Tester→Reviewer | 根据上下文依赖程度决定是否拆分 |
| 每次交接导致信息丢失 | 共享上下文任务保留在同一Agent |
| 质量在多次handoff中逐步下降 | 减少通信成本，避免碎片化 |

---

## 五种核心编排原语

| 原语 | 说明 | 典型场景 |
|------|------|----------|
| **Prompt Chaining** | 线性任务流 | 抽取→翻译→润色 |
| **Routing** | 按任务特征分流 | 客服系统意图识别后派发 |
| **Parallelization** | 独立任务并发执行 | Sub-Agent标准形态 |
| **Orchestrator-Worker** | 中央调度+分布式执行 | 复杂任务分解 |
| **Evaluator-Optimizer** | 生成→评估→迭代 | 代码自检优化 |

---

## 架构选型判断框架

| 决策问题 | 对应方案 |
|----------|----------|
| 单个Agent能否完成任务？ | 能则优先单Agent，避免过度设计 |
| 子任务是否需共享中间过程？ | 否→Sub-Agent；是→Agent Team |
| 子任务是否需互相影响？ | 否→并行Sub-Agent；是→Agent Team |
| 是否仅为"看起来更高级"？ | 退回单Agent，先明确任务模型 |

---

## Sub-Agent vs Agent Team 关键差异

| 维度 | Sub-Agent | Agent Team |
|------|-----------|------------|
| **核心目标** | 执行·隔离·并行 | 协作·沟通·迭代 |
| **上下文** | 完全隔离 | 共享+实时同步 |
| **生命周期** | 一次性、无状态 | 持续存在、有状态 |
| **通信方式** | 不可互通，全经父代理 | 点对点+Lead协调 |
| **适用任务** | 独立、可拆、无依赖 | 强依赖、多步骤、需配合 |
| **系统复杂度** | 低、可预测 | 高、协调成本高 |

---

## 补充洞察

1. **工具描述的重要性**：Sub-Agent的`description`字段是路由关键，需清晰定义边界
2. **反向决策原则**：当协调成本高于收益时，单Agent反而更稳定
3. **架构动态调整**：同一任务在不同阶段可能需要不同架构

---

## 对OpenClaw Agent团队的启示

1. **上下文边界 > 角色划分**：先明确任务间的上下文依赖关系，再决定架构
2. **Sub-Agent优先**：独立任务优先使用Sub-Agent，避免过早引入Agent Team复杂度
3. **渐进式架构**：从单Agent→Sub-Agent→Agent Team逐步演进
4. **工具描述即契约**：`description`字段是路由信号，需精心设计

---

*分析时间: 2026-04-30*
*分析师: 尼克·弗瑞*
