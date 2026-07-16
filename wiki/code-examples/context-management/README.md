---
title: README
author: 尼克·弗瑞 🕵️
product_domain: PD-CODE
doc_type: 其他
tags: [code-examples, context-management]
date: 2026-04-30
---

# Context Management - 上下文管理

> 来源: insight-20260430-agent-harness-context-management

## 文件

- `context-manager.py` - 上下文分层管理器

## 核心概念

| 模式 | 说明 |
|------|------|
| Transcript Mode | 按时间顺序堆砌消息 |
| Working Set | 每轮生成最小可用视图 |

## 分层架构

```
Session Log → Budget Gate → Context View → State Layers
```

## 压缩维度

- 用户目标
- 已排除方案
- 错误修复
- 下一步动作

---

*分析时间: 2026-04-30*
