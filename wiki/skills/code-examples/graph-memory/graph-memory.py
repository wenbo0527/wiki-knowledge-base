# Graph Memory - 图记忆实现

> 来源: insight-20260430-graph-memory-agent
> 核心概念: 记忆单元抽象为节点，关系抽象为边

---

## 1. 基础图结构

```python
"""
Graph Memory - 图记忆基础实现
来源: insight-20260430-graph-memory-agent
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple
from enum import Enum
from datetime import datetime
import uuid

class MemoryNodeType(Enum):
    EVENT = "event"           # 事件
    ENTITY = "entity"         # 实体
    CONCEPT = "concept"       # 概念
    OBSERVATION = "observation"  # 观测

@dataclass
class MemoryNode:
    """记忆节点"""
    id: str
    type: MemoryNodeType
    content: str
    embedding: Optional[List[float]] = None
    metadata: Dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    importance: float = 1.0  # 重要性评分
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "type": self.type.value,
            "content": self.content,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "importance": self.importance
        }

@dataclass
class MemoryEdge:
    """记忆边 - 表示节点间关系"""
    id: str
    source_id: str
    target_id: str
    relation_type: str  # semantic/temporal/causal/logical
    weight: float = 1.0
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "source": self.source_id,
            "target": self.target_id,
            "relation": self.relation_type,
            "weight": self.weight,
            "metadata": self.metadata
        }

class GraphMemory:
    """
    图记忆 - 基于图的智能体记忆系统
    
    核心概念:
    - 记忆单元(事件/实体/概念) → 节点
    - 关系(语义/时间/因果) → 边
    
    优势:
    - 显式关系建模
    - 支持多跳查询
    - 时序动态结构
    """
    
    def __init__(self):
        self.nodes: Dict[str, MemoryNode] = {}
        self.edges: Dict[str, MemoryEdge] = {}
        self.adjacency: Dict[str, Set[str]] = {}  # 邻接表
        self.reverse_adjacency: Dict[str, Set[str]] = {}
    
    def add_node(self, node: MemoryNode) -> str:
        """添加记忆节点"""
        self.nodes[node.id] = node
        if node.id not in self.adjacency:
            self.adjacency[node.id] = set()
            self.reverse_adjacency[node.id] = set()
        return node.id
    
    def add_edge(self, edge: MemoryEdge) -> str:
        """添加记忆边"""
        self.edges[edge.id] = edge
        
        # 更新邻接表
        if edge.source_id not in self.adjacency:
            self.adjacency[edge.source_id] = set()
        self.adjacency[edge.source_id].add(edge.target_id)
        
        if edge.target_id not in self.reverse_adjacency:
            self.reverse_adjacency[edge.target_id] = set()
        self.reverse_adjacency[edge.target_id].add(edge.source_id)
        
        return edge.id
    
    def add_triple(self, subject: str, predicate: str, obj: str, 
                   relation_type: str = "semantic") -> Tuple[str, str]:
        """添加三元组 - 知识图谱基本单元"""
        # 创建节点
        subject_id = self.add_node(MemoryNode(
            id=str(uuid.uuid4()),
            type=MemoryNodeType.ENTITY,
            content=subject
        ))
        
        obj_id = self.add_node(MemoryNode(
            id=str(uuid.uuid4()),
            type=MemoryNodeType.ENTITY,
            content=obj
        ))
        
        # 创建边
        edge_id = self.add_edge(MemoryEdge(
            id=str(uuid.uuid4()),
            source_id=subject_id,
            target_id=obj_id,
            relation_type=relation_type,
            metadata={"predicate": predicate}
        ))
        
        return subject_id, obj_id
    
    def query_hop(self, node_id: str, depth: int = 1) -> List[MemoryNode]:
        """
        多跳查询 - 图检索核心
        
        Args:
            node_id: 起始节点ID
            depth: 跳数
        
        Returns:
            路径上的所有节点
        """
        visited = {node_id}
        current_level = {node_id}
        result = [self.nodes[node_id]] if node_id in self.nodes else []
        
        for _ in range(depth):
            next_level = set()
            for nid in current_level:
                # 前向遍历
                if nid in self.adjacency:
                    for neighbor in self.adjacency[nid]:
                        if neighbor not in visited:
                            visited.add(neighbor)
                            next_level.add(neighbor)
                            if neighbor in self.nodes:
                                result.append(self.nodes[neighbor])
                # 反向遍历
                if nid in self.reverse_adjacency:
                    for neighbor in self.reverse_adjacency[nid]:
                        if neighbor not in visited:
                            visited.add(neighbor)
                            next_level.add(neighbor)
                            if neighbor in self.nodes:
                                result.append(self.nodes[neighbor])
            current_level = next_level
        
        return result
    
    def query_by_relation(self, relation_type: str) -> List[Tuple[MemoryNode, MemoryNode]]:
        """按关系类型查询"""
        results = []
        for edge in self.edges.values():
            if edge.relation_type == relation_type:
                if edge.source_id in self.nodes and edge.target_id in self.nodes:
                    results.append((
                        self.nodes[edge.source_id],
                        self.nodes[edge.target_id]
                    ))
        return results
    
    def get_subgraph(self, node_ids: List[str]) -> Dict:
        """提取子图 - 用于RAG"""
        nodes = {nid: self.nodes[nid].to_dict() 
                 for nid in node_ids if nid in self.nodes}
        
        edges = []
        for edge in self.edges.values():
            if edge.source_id in node_ids and edge.target_id in node_ids:
                edges.append(edge.to_dict())
        
        return {"nodes": nodes, "edges": edges}
    
    def summarize(self) -> Dict:
        """获取图谱摘要"""
        return {
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "node_types": {
                nt.value: sum(1 for n in self.nodes.values() if n.type == nt)
                for nt in MemoryNodeType
            },
            "relation_types": {
                rt: sum(1 for e in self.edges.values() if e.relation_type == rt)
                for rt in ["semantic", "temporal", "causal", "logical"]
            }
        }


# 使用示例
def main():
    memory = GraphMemory()
    
    # 添加记忆
    print("=== Graph Memory Demo ===\n")
    
    # 1. 添加三元组
    print("1. Adding triples...")
    memory.add_triple("用户", "反馈", "页面加载慢", "semantic")
    memory.add_triple("页面加载慢", "原因", "图片未压缩", "causal")
    memory.add_triple("图片未压缩", "影响", "用户体验下降", "effect")
    memory.add_triple("用户体验下降", "导致", "转化率降低", "causal")
    
    # 2. 添加事件记忆
    event_id = memory.add_node(MemoryNode(
        id=str(uuid.uuid4()),
        type=MemoryNodeType.EVENT,
        content="2026-04-30: 优化图片压缩算法",
        metadata={"date": "2026-04-30", "type": "optimization"}
    ))
    
    print(f"   Added event: {event_id}")
    
    # 3. 图谱摘要
    print(f"\n2. Graph Summary: {memory.summarize()}")
    
    # 4. 多跳查询
    print("\n3. Multi-hop query (2 hops)...")
    # 找到"用户"节点
    for node_id, node in memory.nodes.items():
        if node.content == "用户":
            results = memory.query_hop(node_id, depth=2)
            print(f"   From '用户', 2-hop neighbors:")
            for n in results:
                print(f"   - {n.content} ({n.type.value})")
            break


if __name__ == "__main__":
    main()
```

---

## 2. 框架对比

| 框架 | 核心特点 | 典型场景 |
|------|----------|----------|
| **Mem0** | 全流程图记忆，时序感知 | 会话智能体 |
| **Graphiti(Zep)** | 时序知识图谱，双时间建模 | 长对话 |
| **Cognee** | 可查询图嵌入 | 科学推理 |
| **LangMem** | LangChain集成 | 开发工具链 |

---

## 3. 记忆检索方法

| 方法 | 说明 |
|------|------|
| **语义检索** | 向量相似度邻近搜索 |
| **规则检索** | 时间/类型/置信度过滤 |
| **图检索** | 多跳遍历 |
| **强化学习检索** | 自主决策检索策略 |

---

## 4. 记忆演化机制

**内部自演化**:
- 合并冗余节点/边
- 抽象总结 (经验→规则)
- 推理补全 (A→B→C ⇒ A→C)
- 剪枝遗忘

**外部自探索**:
- 成功/失败经验编码
- 主动查缺补漏
- 反馈自适应

---

*来源: insight-20260430-graph-memory-agent*
*分析时间: 2026-04-30*
