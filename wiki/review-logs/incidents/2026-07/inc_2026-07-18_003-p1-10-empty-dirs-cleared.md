---
title: inc 2026 07 18 003 p1 10 empty dirs cleared
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, incidents, 2026-07, wiki-cleanup, L-48]
date: 2026-07-18
---

# INC-2026-07-18-003: P1 清 10 个意外空目录 · 完美闭环

> **触发**: 2026-07-18 09:59 CST（文博"请继续"授权）
> **关联**: INC-2026-07-17-001（trash 副作用）+ L-48（trash 安全流程族）+ L-48.5（find -mindepth 1 治本）
> **状态**: ✅ Closed（10/10 成功 · 父目录全保留）

---

## 📋 现象

文博授权"按顺序走优化"，P1 任务是清 10 个意外空目录（区别于 13 个结构占位空目录）。

| # | 空目录 | 类别 |
|:---|:---|:---:|
| 1 | `.trash` | 占位 |
| 2 | `insights/research/investment` | 意外 |
| 3 | `insights/product-management/requirement` | 意外 |
| 4 | `tools/rss-intelligence` | 意外 |
| 5 | `sources/papers` | 意外 |
| 6 | `sources/rss` | 意外 |
| 7 | `sources/docs` | 意外 |
| 8 | `sources/wechat` | 意外 |
| 9 | `sources/reports` | 意外 |
| 10 | `review-logs/by-severity/high` | 意外 |

13 个结构占位空目录（`by-severity/{low,critical,medium}` / `archives/2026` / `lessons/by-agent/{tony,agatha,wenbo}` 等）保留。

## 🛠 修复（L-48 + L-48.5 治本）

### 步骤 1：L-48 三必查（每个目录）

```bash
REAL_SUBDIRS=$(find "$d" -mindepth 1 -type d 2>/dev/null | wc -l)
REAL_FILES=$(find "$d" -mindepth 1 -type f 2>/dev/null | wc -l)
SIZE=$(du -sh "$d" 2>/dev/null | cut -f1)
```

### 步骤 2：第一次执行踩坑（脚本 bug）

第一次执行 10/10 全部 SKIP，原因：`find -type d` 把**目录自身**算 1 个 subdir，导致误判"非空"。

**L-48.5 治本**：必查空目录必须用 `find -mindepth 1 -type d` 排除目录自身。

### 步骤 3：第二次执行 10/10 成功

```bash
rmdir "$d"  # 每个目录 0 子目录 + 0 文件 + 0 隐藏
```

| 目录 | 大小 | 结果 |
|:---|:---|:---:|
| `.trash` | 0B | ✅ REMOVED |
| `insights/research/investment` | 0B | ✅ REMOVED |
| `insights/product-management/requirement` | 0B | ✅ REMOVED |
| `tools/rss-intelligence` | 0B | ✅ REMOVED |
| `sources/papers` | 0B | ✅ REMOVED |
| `sources/rss` | 0B | ✅ REMOVED |
| `sources/docs` | 0B | ✅ REMOVED |
| `sources/wechat` | 0B | ✅ REMOVED |
| `sources/reports` | 0B | ✅ REMOVED |
| `review-logs/by-severity/high` | 0B | ✅ REMOVED |

### 步骤 4：父目录验证（L-48.3 第 3 项必查）

```
✅ wiki
✅ wiki/insights/research
✅ wiki/insights/product-management
✅ wiki/tools
✅ wiki/sources
✅ wiki/review-logs/by-severity
```

全部父目录保留 ✅

## 📊 成果

| 指标 | Before（7-18 09:11）| After P1（7-18 09:59）| 变化 |
|:---|:---:|:---:|:---:|
| **空目录总数** | **23** | **13** | **-10** ✅ |
| 意外空目录 | 10 | **0** | -10 |
| 结构占位空目录 | 13 | 13 | 0（保留）|
| 总文件数 | 1691 | 1694 | +3（孤立页面 +3）|
| 健康度 | 🟠 65/100 | 🟠 65/100 | cron 算法 bug 不变（L-50 闭环）|

**剩余 13 个空目录 = 全部结构占位**（review-logs/by-severity/{low,critical,medium} + archives/2026 + lessons/by-agent/{tony,agatha,wenbo} + lessons/by-topic/{product,collab,tech} + incidents/resolved + reviews/{monthly,weekly}）—— 预期保留。

## 💡 教训

| Lesson | 标题 | 治本 |
|:---|:---|:---|
| **L-48.5** 🆕 | find 必加 `-mindepth 1` 排除目录自身（否则 `find -type d` 把目录算 1）| ✅ 本次踩坑 |

## 关联

- **INC-2026-07-17-001**（trash 副作用 · process/ 目录被清空）—— L-48 起源
- **L-48**（trash 副作用必查目录结构族）
- **INC-2026-07-18-001**（cron 算法 bug）—— 健康度没变因为算法 bug
- **INC-2026-07-18-002**（5 wiki-link 路径修复）

## 闭环证据

```
wiki_auto_review.py 9:59 输出:
  健康度: 🟠 65/100
  空目录: 23 → 13 ✅
  死链: 1082 → 1090（cron 误报，L-50 闭环）
  孤立页面: 1605 → 1608
```

🕵️ 闭环完成 · 2026-07-18 09:59 CST