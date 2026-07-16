# Context Management - 上下文管理模式

> 来源: insight-20260430-agent-harness-context-management
> 核心概念: 从Transcript Mode到Managed Working Set

---

## 1. 上下文分层模型

```python
"""
Context Manager - 上下文分层管理
来源: insight-20260430-agent-harness-context-management

核心思想:
- 传统模式: 按时间顺序堆砌消息 (Transcript Mode)
- 现代模式: 每轮生成最小可用视图 (Managed Working Set)
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime
import json

class ContentType(Enum):
    USER_TURN = "user_turn"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    ASSISTANT = "assistant"
    SYSTEM = "system"

@dataclass
class ContextItem:
    """上下文项"""
    id: str
    type: ContentType
    content: str
    size: int  # token count estimate
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "type": self.type.value,
            "content": self.content[:100] + "..." if len(self.content) > 100 else self.content,
            "size": self.size,
            "timestamp": self.timestamp.isoformat()
        }

@dataclass
class BudgetPolicy:
    """预算策略"""
    max_total_tokens: int = 100000
    max_file_read_size: int = 50000  # bytes
    max_tool_output_size: int = 10000  # chars
    compression_threshold: float = 0.8  # 压缩阈值

class ContextManager:
    """
    上下文管理器 - 实现Working Set模式
    
    分层架构:
    1. Session Log - 事件流/可回放
    2. Budget Gate - 限流/截断/分页
    3. Context View - 切片/摘要/预览
    4. State Layers - 事件层/数据层/记忆层
    """
    
    def __init__(self, policy: BudgetPolicy = None):
        self.policy = policy or BudgetPolicy()
        self.session_log: List[ContextItem] = []
        self.active_view: List[ContextItem] = []
        self.summary: Optional[str] = None
        self.overflow_storage: Dict[str, str] = {}  # 大内容存储
        
        # 状态分层
        self.event_layer: List[ContextItem] = []      # user turn / tool call
        self.data_layer: List[ContextItem] = []       # file slices / search index
        self.memory_layer: List[ContextItem] = []     # task state / user preferences
    
    def add_item(self, item: ContextItem) -> str:
        """添加上下文项"""
        self.session_log.append(item)
        
        # 路由到对应层
        if item.type in [ContentType.USER_TURN, ContentType.TOOL_CALL]:
            self.event_layer.append(item)
        elif item.type == ContentType.TOOL_RESULT:
            # 检查是否需要溢出存储
            if item.size > self.policy.max_tool_output_size:
                overflow_id = f"overflow_{item.id}"
                self.overflow_storage[overflow_id] = item.content
                # 替换为预览
                preview = item.content[:500] + f"\n...[overflow:{overflow_id}]"
                preview_item = ContextItem(
                    id=item.id + "_preview",
                    type=item.type,
                    content=preview,
                    size=len(preview),
                    metadata={**item.metadata, "overflow_id": overflow_id}
                )
                self.data_layer.append(preview_item)
            else:
                self.data_layer.append(item)
        else:
            self.memory_layer.append(item)
        
        self._rebuild_view()
        return item.id
    
    def _rebuild_view(self):
        """重建上下文视图"""
        current_size = 0
        self.active_view = []
        
        # 按优先级添加: 记忆层 > 事件层 > 数据层
        for layer in [self.memory_layer, self.event_layer, self.data_layer]:
            for item in reversed(layer):
                if current_size + item.size <= self.policy.max_total_tokens:
                    self.active_view.insert(0, item)
                    current_size += item.size
                else:
                    # 触发压缩
                    self._compress()
                    return
        
        # 检查是否需要压缩
        if current_size > self.policy.max_total_tokens * self.policy.compression_threshold:
            self._compress()
    
    def _compress(self):
        """压缩上下文 - 保持任务可续性"""
        print("Context compression triggered...")
        
        # 必须保留的关键状态
        critical_info = {
            "user_goal": None,
            "excluded_options": [],
            "error_fixes": [],
            "next_action": None
        }
        
        # 从session log中提取关键信息
        for item in self.session_log[-50:]:  # 最近50条
            if "goal" in item.metadata:
                critical_info["user_goal"] = item.metadata["goal"]
            if item.metadata.get("status") == "excluded":
                critical_info["excluded_options"].append(item.content)
            if item.metadata.get("status") == "error_fixed":
                critical_info["error_fixes"].append(item.content)
            if item.metadata.get("next_action"):
                critical_info["next_action"] = item.metadata["next_action"]
        
        # 生成压缩摘要
        self.summary = self._generate_summary(critical_info)
        
        # 保留关键状态，丢弃中间过程
        self.session_log = [item for item in self.session_log 
                           if item.type == ContentType.SYSTEM]
        self.data_layer = []
        
        # 添加摘要
        summary_item = ContextItem(
            id="compression_summary",
            type=ContentType.ASSISTANT,
            content=self.summary,
            size=len(self.summary),
            metadata={"is_summary": True}
        )
        self.session_log.append(summary_item)
        self.memory_layer = [summary_item]
        
        self._rebuild_view()
    
    def _generate_summary(self, critical_info: Dict) -> str:
        """生成压缩摘要"""
        lines = ["## Context Summary (Compressed)"]
        
        if critical_info["user_goal"]:
            lines.append(f"\n### User Goal\n{critical_info['user_goal']}")
        
        if critical_info["excluded_options"]:
            lines.append(f"\n### Excluded Options\n" + 
                        "\n".join(f"- {opt}" for opt in critical_info["excluded_options"][-5:]))
        
        if critical_info["error_fixes"]:
            lines.append(f"\n### Error Fixes\n" +
                        "\n".join(f"- {fix}" for fix in critical_info["error_fixes"][-5:]))
        
        if critical_info["next_action"]:
            lines.append(f"\n### Next Action\n{critical_info['next_action']}")
        
        return "\n".join(lines)
    
    def get_view(self) -> List[ContextItem]:
        """获取当前上下文视图"""
        return self.active_view
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "session_log_size": len(self.session_log),
            "active_view_size": len(self.active_view),
            "overflow_storage_size": len(self.overflow_storage),
            "layers": {
                "event": len(self.event_layer),
                "data": len(self.data_layer),
                "memory": len(self.memory_layer)
            }
        }
    
    def retrieve_overflow(self, overflow_id: str) -> Optional[str]:
        """检索溢出存储"""
        return self.overflow_storage.get(overflow_id)


# 使用示例
def main():
    print("=== Context Manager Demo ===\n")
    
    manager = ContextManager()
    
    # 添加上下文项
    manager.add_item(ContextItem(
        id="1",
        type=ContentType.SYSTEM,
        content="You are a helpful coding assistant",
        size=10
    ))
    
    manager.add_item(ContextItem(
        id="2",
        type=ContentType.USER_TURN,
        content="Help me implement a user authentication system",
        size=12,
        metadata={"goal": "user_auth_system"}
    ))
    
    # 添加工具调用
    for i in range(10):
        manager.add_item(ContextItem(
            id=f"tool_{i}",
            type=ContentType.TOOL_RESULT,
            content=f"Tool output {i}: " + "x" * 5000,  # 模拟大输出
            size=5000,
            metadata={"tool": "grep", "file": f"file_{i}.py"}
        ))
    
    print(f"Stats: {manager.get_stats()}")
    print(f"Active view items: {len(manager.get_view())}")


if __name__ == "__main__":
    main()
```

---

## 2. 文件读取策略

| 策略 | 实现 | 示例 |
|------|------|------|
| **Hard Cap** | 设置文件大小上限 | Claude Code: 256KB |
| **Offset/Limit** | 分页读取 | `Read(file, offset=0, limit=100)` |
| **Grep First** | 先搜索再读取 | 先grep定位再读相关行 |

---

## 3. 压缩维度

| 维度 | 必须保留 |
|------|----------|
| **目标** | 用户原始目标 |
| **文件** | 已读取文件列表 |
| **错误** | 错误信息和修复方案 |
| **计划** | 下一步行动计划 |

---

## 4. Harness自查清单

| # | 检查项 |
|---|--------|
| 1 | 工具预算：大内容工具是否设硬上限？ |
| 2 | 访问路径：截断内容是否提供继续访问方式？ |
| 3 | 分页参数：工具描述是否包含offset/limit？ |
| 4 | 压缩维度：是否分层保留任务状态？ |
| 5 | 工具边界：压缩时是否守住tool call/result完整性？ |
| 6 | 子体隔离：子智能体是否默认使用独立会话？ |
| 7 | 状态持久化：关键状态是否迁移至外部？ |
| 8 | 可观测性：是否监控token用量/截断/压缩？ |

---

*来源: insight-20260430-agent-harness-context-management*
*分析时间: 2026-04-30*
