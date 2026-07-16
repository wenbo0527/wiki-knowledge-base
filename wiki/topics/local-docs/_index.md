---
title: 本地文档库 · 索引
author: 尼克·弗瑞 🕵️
created: 2026-07-15
updated: 2026-07-15
tags: [local-docs, RAG, L-37, L-32, L-31]
source_layer: local
status: published
product_domain: PD-LOCAL-DOCS
doc_type: 其他
date: 2026-07-15
---


# 本地文档库 · 索引

> **目的**: 把 `Documents/文档仓库/` 6 个项目（976 个 .md）的过程产物系统化 RAG 化  
> **路径规范**: `wiki/topics/local-docs/<project>/` 镜像 `文档仓库/<project>/`  
> **Status**: 🟡 第一波（行业研究 7 篇）已落盘 · 后续 5 项目待启动

---

## 6 项目总览（7-15 11:06 实测）

| 项目 | 路径 | .md 数 | 价值评级 | RAG 化状态 |
|:---|:---|:---:|:---:|:---:|
| **行业研究** | `文档仓库/行业研究/` | 7 | ⭐⭐⭐⭐⭐ | ✅ 第一波（7/7） |
| cloud-agent-team | `文档仓库/cloud-agent-team/` | 20 | ⭐⭐⭐⭐ | 🟡 待启动 |
| AI team 产品化方案 | `文档仓库/AI team产品化方案/` | 3 | ⭐⭐⭐⭐ | 🟡 待启动 |
| 产品管理项目 | `文档仓库/产品管理项目/` | 146 | ⭐⭐⭐ | 🟡 待启动 |
| 个人网站输出 | `文档仓库/个人网站输出/` | 40 | ⭐⭐ | 🟡 待启动 |
| 数字社区项目 | `文档仓库/数字社区项目/` | 760 | ⭐⭐ | 🟡 待启动 |
| **合计** | — | **976** | — | **7 已落盘** |

---

## 行业研究（7 篇 · 第一波 · 7-15 11:06 落盘）

### 苏银 5 篇（5-18 · 跨 5 领域）

| 文档 | 主题 | 价值 |
|:---|:---|:---:|
| `2026-05-18-项目-苏银BI平台.md` | BI 平台 | ⭐⭐⭐ |
| `2026-05-18-项目-苏银埋点治理.md` | 埋点治理 | ⭐⭐⭐ |
| `2026-05-18-项目-苏银数据门户.md` | 数据门户 | ⭐⭐⭐ |
| `2026-05-18-项目-苏银策略优化.md` | 策略优化 | ⭐⭐⭐ |
| `2026-05-18-项目-苏银营销套件.md` | 营销套件 | ⭐⭐⭐⭐ |

### MarketAgentDemo 2 篇（5-19 · 多 Agent 协作）

| 文档 | 主题 | 价值 |
|:---|:---|:---:|
| `MarketAgentDemo/2026-05-19-多Agent协作完整案例.md` | 多 Agent 协作 | ⭐⭐⭐⭐⭐ |
| `MarketAgentDemo/2026-05-19-项目-MarketAgentTask处理框架Demo.md` | Task 处理框架 | ⭐⭐⭐⭐ |

---

## 跨层 metadata 规范（L-37 治本）

每个本地文档 frontmatter 必须含：

```yaml
---
title: 文档标题
source_layer: local   # 必填：wiki / getnote / local
source_path: 文档仓库原路径  # 必填：可追溯
product_domain: PD-RESEARCH
verified_at: 2026-07-15 11:06
agent_id: nick_fury
status: published
---
```

---

## 4 阶段 RAG 化路线图

| 阶段 | 项目 | 优先级 | 预估 |
|:---:|:---|:---:|:---:|
| 🔴 第一波 | 行业研究 7 篇 | ✅ 已落盘 | — |
| 🟠 第二波 | cloud-agent-team 20 篇 + AI team 产品化方案 3 篇 | ⭐⭐⭐⭐ | 4h |
| 🟡 第三波 | 产品管理项目 146 篇 | ⭐⭐⭐ | 8h |
| 🟢 第四波 | 个人网站输出 40 + 数字社区项目 760 = 800 篇 | ⭐⭐ | 持续 |

---

## RAG 召回率验证（L-15 端到端）

```bash
# 行业研究主题查询
curl -X POST http://localhost:8082/search \
  -H "Content-Type: application/json" \
  -d '{"query":"苏银 BI 平台", "top_k":5, "mode":"hybrid"}'
```

**期望**：返回 ≥ 1 条 `source_layer=local` 的苏银 BI 平台文档（MRR@10 ≥ 0.6）

---

*索引完稿: 2026-07-15 11:06 CST*
*作者: 尼克·弗瑞 🕵️*
*L-31 治本（路径规范）+ L-32 治本（不 hardcode / 必对账）+ L-37 治本（必 verify API）*
