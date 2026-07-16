# Harness Engineering - Agent运行时工程化

> 来源: insight-20260419-harness-engineering
> 核心概念: Harness = Agent的操作系统

---

## 1. Harness核心组件

```python
"""
Harness Core - Agent运行时核心
来源: insight-20260419-harness-engineering

核心概念:
- Harness = Agent的操作系统
- 3类Harness: Feedforward / Feedback / Hybrid
- "The Harness is the Dataset"
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Callable
from enum import Enum
import time

class HarnessType(Enum):
    FEEDFORWARD = "feedforward"      # 单向处理
    FEEDBACK = "feedback"            # 反馈循环
    HYBRID = "hybrid"                # 混合模式

@dataclass
class ToolResult:
    """工具执行结果"""
    tool_name: str
    success: bool
    output: Any
    error: Optional[str] = None
    duration_ms: float = 0

@dataclass
class HarnessConfig:
    """Harness配置"""
    max_retries: int = 3
    timeout_ms: int = 30000
    enable_caching: bool = True
    enable_checkpointing: bool = True
    max_context_tokens: int = 100000

class BaseHarness:
    """
    基础Harness - Agent运行时核心
    
    职责:
    - 工具治理 (Tool Governance)
    - 状态管理 (State Management)
    - 失败恢复 (Failure Recovery)
    - 上下文窗口管理
    """
    
    def __init__(self, config: HarnessConfig = None):
        self.config = config or HarnessConfig()
        self.tools: Dict[str, Callable] = {}
        self.tool_usage_history: List[ToolResult] = []
        self.checkpoints: List[Dict] = []
    
    def register_tool(self, name: str, func: Callable):
        """注册工具"""
        self.tools[name] = func
        print(f"Registered tool: {name}")
    
    async def execute_tool(self, tool_name: str, **kwargs) -> ToolResult:
        """执行工具"""
        if tool_name not in self.tools:
            return ToolResult(
                tool_name=tool_name,
                success=False,
                output=None,
                error=f"Tool {tool_name} not found"
            )
        
        tool = self.tools[tool_name]
        start = time.time()
        
        try:
            result = await tool(**kwargs) if kwargs else await tool()
            duration = (time.time() - start) * 1000
            
            tool_result = ToolResult(
                tool_name=tool_name,
                success=True,
                output=result,
                duration_ms=duration
            )
            
            self._record_usage(tool_result)
            return tool_result
            
        except Exception as e:
            duration = (time.time() - start) * 1000
            return ToolResult(
                tool_name=tool_name,
                success=False,
                output=None,
                error=str(e),
                duration_ms=duration
            )
    
    def _record_usage(self, result: ToolResult):
        """记录工具使用"""
        self.tool_usage_history.append(result)
        
        # 保持历史在合理范围
        if len(self.tool_usage_history) > 1000:
            self.tool_usage_history = self.tool_usage_history[-500:]
    
    def get_tool_stats(self) -> Dict:
        """获取工具使用统计"""
        if not self.tool_usage_history:
            return {}
        
        stats = {}
        for result in self.tool_usage_history:
            if result.tool_name not in stats:
                stats[result.tool_name] = {"count": 0, "failures": 0, "total_ms": 0}
            stats[result.tool_name]["count"] += 1
            if not result.success:
                stats[result.tool_name]["failures"] += 1
            stats[result.tool_name]["total_ms"] += result.duration_ms
        
        return stats
    
    def checkpoint(self, state: Dict):
        """保存检查点"""
        self.checkpoints.append({
            "state": state,
            "timestamp": time.time()
        })
    
    def restore_checkpoint(self) -> Optional[Dict]:
        """恢复检查点"""
        if self.checkpoints:
            return self.checkpoints[-1]["state"]
        return None


class FeedforwardHarness(BaseHarness):
    """
    Feedforward Harness - 单向处理模式
    
    特点:
    - 输入 → 处理 → 输出
    - 无反馈循环
    - 适合简单任务
    """
    
    async def run(self, input_data: Any) -> Any:
        """运行"""
        # 1. 输入验证
        if not self._validate_input(input_data):
            raise ValueError("Invalid input")
        
        # 2. 工具调用
        results = []
        for tool_name, params in self._plan_tools(input_data):
            result = await self.execute_tool(tool_name, **params)
            results.append(result)
        
        # 3. 输出聚合
        return self._aggregate_output(results)


class FeedbackHarness(BaseHarness):
    """
    Feedback Harness - 反馈循环模式
    
    特点:
    - 输出反馈到输入
    - 迭代优化
    - 适合复杂任务
    """
    
    def __init__(self, config: HarnessConfig = None):
        super().__init__(config)
        self.max_iterations = 5
    
    async def run(self, input_data: Any, objective: str) -> Any:
        """运行"""
        current_output = input_data
        
        for i in range(self.max_iterations):
            # 1. 评估当前输出
            evaluation = await self._evaluate(current_output, objective)
            
            if evaluation["success"]:
                return current_output
            
            # 2. 基于反馈调整
            feedback = evaluation["feedback"]
            adjusted = await self._apply_feedback(current_output, feedback)
            
            current_output = adjusted
        
        return current_output
    
    async def _evaluate(self, output: Any, objective: str) -> Dict:
        """评估输出"""
        # 实际实现中调用LLM进行评估
        return {"success": False, "feedback": "Needs improvement"}
    
    async def _apply_feedback(self, output: Any, feedback: str) -> Any:
        """应用反馈"""
        return output


# 使用示例
async def main():
    print("=== Harness Engineering Demo ===\n")
    
    # 创建Harness
    harness = FeedforwardHarness()
    
    # 注册工具
    harness.register_tool("search", lambda query: f"Results for: {query}")
    harness.register_tool("read_file", lambda path: f"Content of: {path}")
    
    # 执行
    result = await harness.run({"query": "AI Agent"})
    print(f"Result: {result}")
    
    # 工具统计
    print(f"\nTool Stats: {harness.get_tool_stats()}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

---

## 2. 三类Harness对比

| 类型 | 特点 | 适用场景 |
|------|------|----------|
| **Feedforward** | 单向处理，无反馈 | 简单查询、文档处理 |
| **Feedback** | 输出反馈到输入，迭代优化 | 复杂推理、代码生成 |
| **Hybrid** | 结合两者 | 通用场景 |

---

## 3. Harness核心职责

| 职责 | 说明 |
|------|------|
| **工具治理** | 工具注册、权限、限流 |
| **状态管理** | 检查点、上下文维护 |
| **失败恢复** | 重试、断点续传 |
| **上下文窗口** | 分页、压缩、溢出存储 |

---

## 4. 关键洞察

> **"The Harness is the Dataset"**

Harness不仅是接口层，而是**捕获轨迹数据的核心资产**。

| 资产 | 价值 |
|------|------|
| 模型 | 通用能力 |
| Prompt | 任务定义 |
| **Harness** | **轨迹数据 = 竞争优势** |

---

*来源: insight-20260419-harness-engineering*
*分析时间: 2026-04-30*
