# Multi-Agent Routing - 多智能体路由模式

> 来源: insight-20260430-multi-agent-architecture-guide
> 核心洞察: "真正决定架构的是任务需要的协作方式，而非智能体数量"

---

## 1. 架构选型决策树

```
┌─────────────────────────────────────────────────────────────┐
│                   任务分析                                   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
            ┌───────────────────────────────┐
            │   单个Agent能否完成任务？      │
            └───────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                │                       │
               能                       否
                │                       │
                ▼                       ▼
        ┌─────────────┐       ┌─────────────────────┐
        │  使用单Agent │       │ 子任务是否需共享上下文？│
        │  避免过度设计│       └─────────────────────┘
        └─────────────┘                 │
                            ┌───────────┴───────────┐
                            │                       │
                           否                       是
                            │                       │
                            ▼                       ▼
                    ┌─────────────┐         ┌─────────────┐
                    │ Sub-Agent   │         │Agent Team   │
                    │ 隔离+并行   │         │共享+实时通信 │
                    └─────────────┘         └─────────────┘
```

---

## 2. Python实现：智能路由

```python
"""
Multi-Agent Router - 多智能体架构路由决策
来源: insight-20260430-multi-agent-architecture-guide
"""

from dataclasses import dataclass
from enum import Enum
from typing import List

class ArchitectureType(Enum):
    SINGLE = "single_agent"
    SUB_AGENT = "sub_agent"
    AGENT_TEAM = "agent_team"

@dataclass
class TaskContext:
    """任务上下文"""
    description: str
    estimated_complexity: str  # "low", "medium", "high"
    has_dependencies: bool
    needs_shared_context: bool
    requires_iteration: bool
    parallel_candidates: int

@dataclass  
class RoutingDecision:
    architecture: ArchitectureType
    reasoning: str
    agent_count: int
    recommendations: List[str]

class MultiAgentRouter:
    """多智能体架构路由器"""
    
    def route(self, context: TaskContext) -> RoutingDecision:
        # 规则1: 简单任务用单Agent
        if context.estimated_complexity == "low" and not context.has_dependencies:
            return RoutingDecision(
                architecture=ArchitectureType.SINGLE,
                reasoning="Simple task, no need for multi-agent complexity",
                agent_count=1,
                recommendations=["Start simple, escalate if needed"]
            )
        
        # 规则2: 需要迭代的任务
        if context.requires_iteration:
            return RoutingDecision(
                architecture=ArchitectureType.SINGLE,
                reasoning="Task requires iteration, shared context needed",
                agent_count=1,
                recommendations=["Use single agent with full context"]
            )
        
        # 规则3: 强依赖任务
        if context.needs_shared_context and context.has_dependencies:
            return RoutingDecision(
                architecture=ArchitectureType.AGENT_TEAM,
                reasoning="Strong dependencies + shared context required",
                agent_count=3,
                recommendations=["Implement shared state layer", "Define communication protocol"]
            )
        
        # 规则4: 独立可并行任务
        if context.parallel_candidates >= 2 and not context.needs_shared_context:
            return RoutingDecision(
                architecture=ArchitectureType.SUB_AGENT,
                reasoning=f"{context.parallel_candidates} independent tasks",
                agent_count=context.parallel_candidates,
                recommendations=["Use Sub-Agent for isolation", "Return only conclusions"]
            )
        
        return RoutingDecision(
            architecture=ArchitectureType.SINGLE,
            reasoning="Default to single agent",
            agent_count=1,
            recommendations=["Keep it simple"]
        )
```

---

## 3. Sub-Agent vs Agent Team 对比

| 维度 | Sub-Agent | Agent Team |
|------|-----------|------------|
| **核心目标** | 执行·隔离·并行 | 协作·沟通·迭代 |
| **上下文** | 完全隔离 | 共享+实时同步 |
| **生命周期** | 一次性 | 持续存在 |
| **通信** | 经父代理中转 | 点对点+Lead协调 |
| **适用场景** | 独立、可拆、无依赖 | 强依赖、多步骤 |
| **复杂度** | 低 | 高 |

---

## 4. 五种编排原语

| 原语 | 说明 | 典型场景 |
|------|------|----------|
| **Prompt Chaining** | 线性任务流 | 抽取→翻译→润色 |
| **Routing** | 按任务特征分流 | 客服意图识别后派发 |
| **Parallelization** | 独立任务并发 | Sub-Agent标准形态 |
| **Orchestrator-Worker** | 中央调度+分布式执行 | 复杂任务分解 |
| **Evaluator-Optimizer** | 生成→评估→迭代 | 代码自检优化 |

---

## 5. 常见误区

| 错误做法 | 正确做法 |
|----------|----------|
| 按角色拆分: Planner→Developer→Tester | 按上下文边界拆分 |
| 每次交接信息丢失 | 共享上下文任务保留在同一Agent |
| 质量在handoff中下降 | 减少通信成本 |

---

*来源: insight-20260430-multi-agent-architecture-guide*
*分析时间: 2026-04-30*
