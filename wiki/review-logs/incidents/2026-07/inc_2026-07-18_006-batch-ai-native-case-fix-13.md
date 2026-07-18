---
title: inc 2026 07 18 006 batch ai native case fix 13
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, incidents, 2026-07, deadlink-fix, batch]
date: 2026-07-18
---

# INC-2026-07-18-006: A 任务 · 批量修 AI Native/ 大小写敏感（13 处）

> **触发**: 2026-07-18 16:34 CST（文博"按顺序处理"授权）
> **关联**: INC-2026-07-18-005 + L-50.4（真死链 = 路径错 + 引用方修改）
> **状态**: ✅ Closed（13/13 修复 · 总死链 703→692）

---

## 📋 现象

P1.5 v3 算法揭穿后剩 703 死链，其中 `AI Native/` 类 16 处大小写敏感（实际可改 13 处）。

## 🔍 死链分类

| link | 频次 | 真位置 | 改法 |
|:---|:---:|:---|:---|
| `AI Native/Agent Engineering` | 8 | `topics/ai-native/agent-engineering.md` | 小写 + 加 topics/ |
| `AI Native/AI-Agent Design` | 4 | `insights/agent/agent-design-patterns/...` | 小写 + 改写 |
| `AI Native/Multi-Agent Systems` | 1 | `topics/ai-agent/topic-04-multi-agent.md` | 小写 + 加 topics/ |

**可批量改：13 处 / 8 文件**

## 🛠 修复（L-50.4 + L-50.8 治本）

### 3 个 Python regex 替换

```python
replacements = [
    (r'\[\[AI Native/Agent Engineering(\|[^\]]*)?\]\]', r'[[topics/ai-native/agent-engineering|Agent 工程化]]'),
    (r'\[\[AI Native/AI-Agent Design(\|[^\]]*)?\]\]', r'[[insights/agent/agent-design-patterns/insight-20260521-agent-design-pattern-review|AI Agent 设计模式]]'),
    (r'\[\[AI Native/Multi-Agent Systems(\|[^\]]*)?\]\]', r'[[topics/ai-agent/topic-04-multi-agent|Multi-Agent 系统]]'),
]
```

### 改写文件清单

| 文件 | 处数 |
|:---|:---:|
| insight-20260502-luo-fuli-openclaw.md | 2 |
| insight-20260426-vibe-analyzing-asktable.md | 2 |
| insight-20260426-lsdm-dataset-methodology.md | 1 |
| insight-20260411-demis-hassabis.md | 1 |
| insight-20260426-linjunyang-agent-thinking.md | 2 |
| insight-20260426-nextie-harness-multiagent.md | 3 |
| insight-20260426-adele-ai-performance.md | 1 |
| insight-20260426-gravitino-metadata-lake.md | 1 |
| **合计** | **13** |

## 📊 成果

| 指标 | Before A | After A | 变化 |
|:---|:---:|:---:|:---:|
| 总死链 | 703 | **692** | **-11** |
| AI Native/ 类 | 16 | 3 | -13 |

**剩余 3 个 `AI Native/`** = `AI-Evaluation` × 2 + `AI-Middleware` × 1（无对应文件，未修）

## 备份

`/tmp/wiki-ai-native-fix-20260718-163623/`

## 关联

- **INC-2026-07-18-007**（B 任务 insight 子目录 685 处修复）
- **L-50.4**（真死链修复治本）
- **L-50.8**（wiki-link regex alias 治本）

🕵️ 闭环完成 · 2026-07-18 16:36 CST