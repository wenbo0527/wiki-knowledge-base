# Karpathy LLM Wiki

> A pattern for building personal knowledge bases using LLMs.

## 📌 基本信息

| 属性 | 值 |
|------|-----|
| **来源** | GitHub Gist |
| **作者** | Andrej Karpathy (@karpathy) |
| **链接** | https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f |
| **收藏日期** | 2026-04-17 |
| **类型** | 方法论/知识管理 |
| **标签** | `#llm` `#wiki` `#knowledge-base` `#karpathy` |

---

## 💡 核心洞察

1. **知识复利**：Wiki 是持久复利的知识制品，不是每次查询重新发现
2. **人机分工**：人类负责 curation 和提问，LLM 负责维护工作
3. **三曾架构**：Raw Sources → Wiki → Schema
4. **矛盾标记**：新来源与旧信息冲突时自动标记
5. **Query 沉淀**：好答案存回 Wiki 成为新页面

---

## 🔗 与我们的关系

- **直接引用**：我们的 WIKI_MANAGEMENT_RULES.md v2.0 受此启发
- **核心借鉴**：Query 答案沉淀、矛盾标记、增量更新
- **工具建议**：Obsidian、qmd、Marp

---

## 📋 元数据

```yaml
title: Karpathy LLM Wiki
source: github-gist
url: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
author: Andrej Karpathy
saved_by: nick-fury
saved_date: 2026-04-17
last_checked: 2026-04-17
```

---

## 🔄 变更追踪

| 日期 | 检查人 | 状态 | 备注 |
|:----:|:------:|:----:|------|
| 2026-04-17 | 尼克·弗瑞 | 🆕 首次收藏 | - |

**追踪计划**：
- 每周一检查一次是否有更新
- 检查方式：`curl` 获取 Gist 内容，对比 hash

**更新时执行**：
1. 重新获取最新内容
2. 更新到 `sources/references/karpathy-llm-wiki.md`
3. 比较差异，识别新增洞察
4. 如有重大更新，通知派蒙

---

## 🔍 当前快照

| 属性 | 值 |
|------|-----|
| **Content Hash (SHA-256)** | `dc3efe98ae62f23dd08acad13aba2e95287beb20b6bec2f4af0423557fe37401` |
| **获取时间** | 2026-04-17 11:20 |
