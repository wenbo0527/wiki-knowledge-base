# Subagent Pattern - 子智能体模式

> 来源: insight-20260430-claude-code-subagents
> 核心价值: 隔离探索过程，保护主上下文

---

## 1. Subagent文件定义模板

```markdown
---
name: code-reviewer
description: Review code quality, security, and maintainability after code changes.
  Use after implementation, not for planning. Return P0/P1/P2级别问题.
tools: Read, Grep, Glob, Bash
model: sonnet
---

Return:
1. Affected files and why they matter
2. Compatibility risks
3. Tests to add/update
4. Unknowns requiring human confirmation

Do not edit files or propose broad refactors.
```

### 关键字段说明

| 字段 | 作用 | 示例 |
|------|------|------|
| `name` | 子代理标识 | `code-reviewer` |
| `description` | 路由契约 + 边界定义 | 明确"负责什么/不负责什么" |
| `tools` | 权限控制 | 仅允许必要工具 |
| `model` | 模型规格 | `sonnet` 适合快速任务 |

---

## 2. Python实现：Subagent调度器

```python
"""
Subagent调度器 - 隔离式并行执行
来源: Claude Code Subagents架构分析
"""

import asyncio
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum

class AgentStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class SubAgentResult:
    name: str
    status: AgentStatus
    output: Optional[str] = None
    error: Optional[str] = None
    duration_ms: float = 0

@dataclass
class AgentDefinition:
    name: str
    description: str
    tools: List[str]
    model: str = "sonnet"

class SubagentScheduler:
    """
    子智能体调度器
    
    核心价值:
    - 隔离: 探索过程在独立上下文执行
    - 压缩: 50次工具调用 → 3行结论
    - 并行: 互不依赖的任务可并发执行
    """
    
    def __init__(self):
        self.agents: Dict[str, AgentDefinition] = {}
        self.results: Dict[str, SubAgentResult] = {}
    
    def register_agent(self, agent: AgentDefinition):
        """注册子代理"""
        self.agents[agent.name] = agent
        print(f"Registered agent: {agent.name}")
        print(f"  Description: {agent.description}")
        print(f"  Tools: {', '.join(agent.tools)}")
    
    async def execute_isolated(
        self,
        agent_name: str,
        task: str,
        timeout: int = 300
    ) -> SubAgentResult:
        """
        隔离执行子任务
        
        Args:
            agent_name: 子代理名称
            task: 任务描述
            timeout: 超时时间(秒)
        
        Returns:
            SubAgentResult: 执行结果
        """
        if agent_name not in self.agents:
            return SubAgentResult(
                name=agent_name,
                status=AgentStatus.FAILED,
                error=f"Agent {agent_name} not found"
            )
        
        agent = self.agents[agent_name]
        print(f"\nExecuting: {agent_name}")
        print(f"Task: {task}")
        
        # 模拟执行 (实际使用时替换为真实的Agent调用)
        import time
        start = time.time()
        
        try:
            # 1. 创建隔离上下文
            isolated_context = self._create_isolated_context(agent, task)
            
            # 2. 执行任务
            result = await self._run_in_context(isolated_context, timeout)
            
            # 3. 压缩输出 - 50次调用 → 3行结论
            compressed = self._compress_output(result)
            
            return SubAgentResult(
                name=agent_name,
                status=AgentStatus.COMPLETED,
                output=compressed,
                duration_ms=(time.time() - start) * 1000
            )
        except Exception as e:
            return SubAgentResult(
                name=agent_name,
                status=AgentStatus.FAILED,
                error=str(e),
                duration_ms=(time.time() - start) * 1000
            )
    
    def _create_isolated_context(self, agent: AgentDefinition, task: str) -> Dict:
        """创建隔离上下文"""
        return {
            "agent": agent,
            "task": task,
            "tools": agent.tools,
            "mode": "isolated",  # 关键: 隔离模式
            "history": []
        }
    
    async def _run_in_context(self, context: Dict, timeout: int) -> str:
        """在隔离上下文中运行"""
        # 实际实现: 调用Claude Code API或其他Agent Runtime
        await asyncio.sleep(0.1)  # 模拟
        return f"Exploration result for: {context['task']}"
    
    def _compress_output(self, raw_output: str) -> str:
        """
        压缩输出
        
        核心思想: 50次工具调用过程 → 3行结论
        - 仅保留结构化结果
        - 关键摘要
        - 可验证证据
        """
        lines = raw_output.split('\n')
        
        # 模拟压缩过程
        compressed = [
            "## Summary",
            "- Key finding 1 with evidence",
            "- Key finding 2 with evidence", 
            "- Action required: ..."
        ]
        
        return '\n'.join(compressed)
    
    async def execute_parallel(
        self,
        tasks: List[tuple]
    ) -> List[SubAgentResult]:
        """
        并行执行多个独立任务
        
        Args:
            tasks: [(agent_name, task_description), ...]
        
        Returns:
            所有任务结果
        """
        print(f"\nParallel execution: {len(tasks)} tasks")
        
        coroutines = [
            self.execute_isolated(agent_name, task)
            for agent_name, task in tasks
        ]
        
        results = await asyncio.gather(*coroutines)
        
        for r in results:
            status_icon = "✅" if r.status == AgentStatus.COMPLETED else "❌"
            print(f"{status_icon} {r.name}: {r.status.value} ({r.duration_ms:.0f}ms)")
        
        return results


# 使用示例
async def main():
    scheduler = SubagentScheduler()
    
    # 注册子代理
    scheduler.register_agent(AgentDefinition(
        name="security-reviewer",
        description="Find vulnerabilities and security risks in code changes",
        tools=["Read", "Grep", "Glob"]
    ))
    
    scheduler.register_agent(AgentDefinition(
        name="performance-analyzer", 
        description="Identify performance bottlenecks and optimization opportunities",
        tools=["Read", "Grep", "Bash"]
    ))
    
    # 并行执行独立任务
    tasks = [
        ("security-reviewer", "Review authentication module for token validation issues"),
        ("performance-analyzer", "Analyze database query performance in user service"),
    ]
    
    results = await scheduler.execute_parallel(tasks)
    
    # 聚合结果
    print("\n" + "="*50)
    print("AGGREGATED RESULTS")
    print("="*50)
    for r in results:
        print(f"\n### {r.name}")
        print(r.output)


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 3. 使用场景对照表

| 场景 | 是否使用Subagent | 原因 |
|------|-----------------|------|
| 代码安全审查 | ✅ | 独立任务，可并行 |
| 性能分析 | ✅ | 独立任务，可并行 |
| 依赖影响分析 | ✅ | 隔离探索过程 |
| API设计讨论 | ❌ | 需要来回迭代 |
| 架构决策 | ❌ | 强依赖，需共享上下文 |
| Bug调试 | ⚠️ | 视复杂度决定 |

---

## 4. 常见陷阱

| 陷阱 | 正确做法 |
|------|----------|
| 任务描述模糊 | "检查认证模块的token校验风险，返回P0/P1/P2" |
| 过度返回过程 | 主Agent只需结论+证据+下一步 |
| 强依赖任务拆分 | 前端/后端/测试耦合任务不适合硬拆 |

---

*来源: insight-20260430-claude-code-subagents*
*分析时间: 2026-04-30*
