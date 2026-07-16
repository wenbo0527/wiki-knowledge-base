---
title: Wiki 知识库索引
description: Wiki 独立索引方案 - curated vs authored
category: documentation
tags: [knowledge-base, wiki, curated, authored, index]
author: Tony Stark
date: 2026-05-18
product_domain: PD-TOPIC
doc_type: 其他
---


# Wiki 知识库索引

> **版本**: v1.0
> **日期**: 2026-05-18
> **维护者**: Tony Stark

---

## 一、来源标签体系

| 来源 | 标签 | 说明 | 示例 |
|:---|:---|:---|:---|
| **Authored** | `authored` | 我们自己编写的 | 产品 PRD、SOP、技术方案 |
| **Curated** | `curated` | 收集的/外部的 | 行业报告、Wiki、竞品分析 |

### 产品域代码对应

| 产品域 | 来源 | 维护者 |
|:---|:---|:---|
| PD-DFD/DMT/DEX/MKT/RISK/COM | authored | Tony |
| PD-WIKI | curated | 团队共同 |
| PD-RESEARCH | curated | 尼克 |
| PD-TECH | authored | 钟离 |

---

## 二、索引架构

```
知识库/
├── index/
│   ├── authored/              # 我们编写的
│   │   ├── chunks.json        # 8,652 chunks
│   │   ├── vector_db/
│   │   └── manifest.json
│   └── curated/               # Wiki/收集的
│       ├── chunks.json        # 12,168 chunks (Wiki)
│       ├── vector_db/
│       └── manifest.json
└── scripts/
    ├── index_authored.py       # 索引 authored
    ├── index_curated.py       # 索引 curated
    └── index_wiki.py          # Wiki 专用索引
```

---

## 三、Wiki 索引

### 3.1 索引统计

| 指标 | 数值 |
|:---|:---:|
| Wiki 文档数 | 852 |
| Chunks 数 | 12,168 |
| 来源标签 | curated |
| 索引路径 | `index/curated/` |

### 3.2 索引命令

```bash
# 全量索引
python3 scripts/index_wiki.py --full --vectorize

# 增量索引（按天更新）
python3 scripts/index_wiki.py --vectorize

# 仅解析文档
python3 scripts/index_wiki.py
```

### 3.3 增量更新

Wiki 索引支持增量更新：
1. 检查文档修改时间 (mtime)
2. 仅索引有变化的文档
3. 更新 manifest.json 记录

---

## 四、API 筛选

### 按来源检索

```bash
# 仅检索 authored
curl -X POST http://localhost:8082/search \
  -d '{"query": "...", "filters": {"source": "authored"}}'

# 仅检索 curated
curl -X POST http://localhost:8082/search \
  -d '{"query": "...", "filters": {"source": "curated"}}'

# 全部检索（默认）
curl -X POST http://localhost:8082/search \
  -d '{"query": "..."}'
```

---

## 五、来源说明

### 5.1 Authored（我们编写的）

**特征**：
- Tony/钟离/尼克直接产出
- 有明确的产品管理结构
- PRD/SOP/技术方案格式

**文档类型**：
- PRD
- SOP
- 技术方案
- 模板
- 需求

### 5.2 Curated（收集的）

**特征**：
- 外部收集的资料
- Wiki 内容
- 行业报告
- 竞品分析

**文档类型**：
- 其他（行业报告、Wiki 文档等）

---

## 六、更新频率

| 来源 | 更新频率 | 触发方式 |
|:---|:---|:---|
| Authored | 按需 | 新需求/新文档时 |
| Wiki (Curated) | 按天 | 每日检查增量 |

---

## 七、验证

### 7.1 Wiki 检索验证

```python
# 测试 Wiki 检索
results = knowledge_search(
    query="如何做产品需求分析",
    filters={"source": "curated"},
    top_k=5
)
```

### 7.2 评估指标

| 指标 | Authored | Curated | 目标 |
|:---|:---:|:---:|:---:|
| MRR@10 | 1.000 | 待验证 | > 0.7 |
| Recall@10 | 0.810 | 待验证 | > 0.85 |

---

*最后更新: 2026-05-18*
