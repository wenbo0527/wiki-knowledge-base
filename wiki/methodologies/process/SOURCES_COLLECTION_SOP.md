---
title: SOURCES COLLECTION SOP
author: 尼克·弗瑞 🕵️
product_domain: PD-PROCESS
doc_type: 其他
tags: [process]
date: 2026-05-23
---

# Sources 收集 SOP v1.0

> 版本: v1.0
> 创建时间: 2026-05-22
> 维护者: 尼克·弗瑞
> 状态: 正式发布

---

## 目的

根据 Karpathy LLM Wiki Pattern 的三层架构，Sources 是输入层（Layer 1），为 Insights 提供原始资料支撑。

---

## Sources 定义

| 类型 | 说明 | 示例 |
|:---|:---|:---|
| **原始文章** | 公众号、网站文章 | 微信文章、36kr、虎嗅 |
| **行业报告** | 第三方研究报告 | 艾瑞、IDC、麦肯锡 |
| **学术论文** | 学术研究成果 | arXiv、ACL、ICML |
| **产品文档** | 官方技术文档 | GitHub README、API Docs |

---

## 收集流程

### Step 1: 识别高价值来源

| 来源类型 | 识别标准 | 优先级 |
|:---|:---|:---:|
| **⭐⭐⭐⭐⭐** | 行业权威、独家数据 | 立即收集 |
| **⭐⭐⭐⭐** | 头部媒体、深度分析 | 24h内 |
| **⭐⭐⭐** | 中等价值 | 72h内 |
| **⭐⭐** | 参考价值 | 有空收集 |

### Step 2: 提取核心信息

**每个 Source 必须包含**：

```markdown
## Source: {标题}

### 元信息
- **来源**: {公众号/网站/报告}
- **链接**: {原始URL}
- **保存日期**: {YYYY-MM-DD}
- **评级**: ⭐⭐⭐⭐⭐
- **标签**: #source

### 一句话摘要
{核心观点，一句话概括}

### 关键发现（最多3条）
1. {发现1}
2. {发现2}
3. {发现3}

### 与现有知识的关联
- [[insight-xxx]] - 相关洞察
- [[concept-xxx]] - 相关概念

### 行动建议
- [ ] 下一步行动
```

### Step 3: 存储位置

| 来源类型 | 存储路径 |
|:---|:---|
| **公众号文章** | `sources/wechat/YYYY-MM-{slug}.md` |
| **行业报告** | `sources/review-logs/reports/YYYY-MM-{slug}.md` |
| **学术论文** | `sources/papers/YYYY-MM-{slug}.md` |
| **产品文档** | `sources/docs/{product}/{slug}.md` |

---

## 来源标记规范

### 标记格式

```markdown
> **来源**: {来源名称}
> **原始链接**: {URL}
> **保存日期**: {YYYY-MM-DD}
```

### 示例

```markdown
> **来源**: 微信公众 - AI末班车
> **原始链接**: https://mp.weixin.qq.com/s/xxxxx
> **保存日期**: 2026-05-22
```

---

## 质量标准

### 入库门槛

| 标准 | 要求 |
|:---|:---|
| **可追溯** | 必须有原始链接 |
| **有价值** | 评级 ≥ ⭐⭐⭐ |
| **有条理** | 包含上述模板字段 |

### 禁止入库

- ❌ 纯标题党内容
- ❌ 无原始链接
- ❌ 评级 < ⭐⭐⭐

---

## 与 Insights 的关联

**原则**：每个 Insight 必须对应至少一个 Source

```
Source（Layer 1）
    ↓ 支持
Insight（Layer 2）
    ↓ 提炼
Concept（Layer 3）
```

---

## 收集频率

| 类型 | 频率 | 目标数量/月 |
|:---|:---:|:---:|
| **公众号文章** | 每日 | 50+ |
| **行业报告** | 每周 | 10+ |
| **学术论文** | 每月 | 5+ |
| **产品文档** | 按需 | 5+ |

---

## 相关页面

- [[WIKI_MANAGEMENT_RULES]] - Wiki 管理细则
- [[llm-wiki-pattern]] - Karpathy LLM Wiki Pattern
- [[insight-20260429-Skill-insight进阶指南...]] - Skill进阶指南

---

*最后更新: 2026-05-22*
*维护者: 尼克·弗瑞 🕵️*