# Subagent Patterns - 子智能体模式

> 来源: insight-20260430-claude-code-subagents

## 文件

- `subagent-pattern.py` - 子智能体调度器实现

## 核心概念

1. **隔离**: 探索过程在独立上下文执行
2. **压缩**: 50次工具调用 → 3行结论
3. **并行**: 互不依赖的任务可并发执行

## 关键模板

```markdown
---
name: code-reviewer
description: Review code quality, security, and maintainability.
tools: Read, Grep, Glob
model: sonnet
---
```

## 使用场景

| 场景 | 是否使用 |
|------|----------|
| 代码安全审查 | ✅ |
| 性能分析 | ✅ |
| API设计讨论 | ❌ |
| Bug调试 | ⚠️ |

---

*分析时间: 2026-04-30*
