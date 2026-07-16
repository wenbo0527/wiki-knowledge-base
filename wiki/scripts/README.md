---
title: Wiki 工具脚本
author: 尼克·弗瑞 🕵️
product_domain: PD-WIKI
doc_type: 工具
tags: [scripts, rss, automation]
date: 2026-07-16
---

# 🛠 Wiki 工具脚本目录

> 维护者：🕵️ 尼克·弗瑞
> 数据截止：2026-07-16 19:30 CST
> 路径：`Wiki/wiki/scripts/`

---

## 目录说明

本目录存放 **Wiki 内部使用的工作流脚本和配置**（非 .md 文档）。文件类型包括 Python 脚本和 JSON 配置。

**与 nick_fury/scripts/ 的区别**：
- `nick_fury/scripts/`：Nick Agent 的推送 / 扫描 / 监控脚本
- `Wiki/scripts/`：Wiki 自身使用的工具（如 RSS 收集、自动分类）

---

## 当前文件清单

| 文件 | 类型 | 用途 | mtime |
|:---|:---|:---|:---:|
| `topic_auto_collect.py` | Python | Topic 自动收集系统 v1.0（RSS 采集 + 自动分类 + 入库决策）| 2026-04-21 |
| `rss_sources_expansion.json` | JSON | RSS 源扩展配置（4-21 写入）| 2026-04-21 |

---

## 关键依赖路径（topic_auto_collect.py）

- `P0_RSS_CONFIG` = `/Users/wenbo/.openclaw/workspace/agents/nick_fury/data/p0_rss_sources.json`
- `MONITORING_CONFIG` = `/Users/wenbo/Documents/project/Wiki/wiki/methodologies/process/topic-monitoring-config.md`
- `summary_path` = `~/.openclaw/workspace/agents/nick_fury/data/auto_collect_summary.md`

---

## 维护指南

- **新增**：建子目录或独立 .py 文件，README 同步登记
- **删除**：`/usr/bin/trash <file>`（不直接 rm）
- **改路径**：先 grep 全 Wiki 找引用 → 改 hardcoded path → verify

---

*创建：2026-07-16 19:35 CST · Wiki W1 Phase B 收尾同步*
*🕵️ 尼克·弗瑞*
