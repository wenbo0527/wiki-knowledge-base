# Multi-Agent Routing - 多智能体路由

> 来源: insight-20260430-multi-agent-architecture-guide

## 文件

- `multi-agent-routing.py` - 架构路由决策实现

## 核心决策树

```
单Agent能否完成? 
├── 能 → 使用单Agent
└── 否 → 子任务需共享上下文?
         ├── 否 → Sub-Agent
         └── 是 → Agent Team
```

## 核心原则

1. 能用单Agent就不用多Agent
2. 独立任务 → Sub-Agent
3. 强依赖任务 → Agent Team

---

*分析时间: 2026-04-30*
