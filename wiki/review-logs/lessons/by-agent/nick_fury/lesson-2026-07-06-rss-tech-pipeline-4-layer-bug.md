---
title: lesson 2026 07 06 rss tech pipeline 4 layer bug
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, lessons, by-agent]
date: 2026-07-15
---

# Lessons Learned · 2026-07-06（INC-2026-07-06-001 闭环）

> 关联: INC-2026-07-06-001（技术日报重复推送 + RSS 数据真空 7 天）
> 状态: ✅ Closed (B 方案 · 09:25→10:00)
> 维护者: 尼克·弗瑞 🕵️

---

## L-24: fetcher 和 analyzer 必须共享 articles 对象

**现象**：`daily_pipeline.py` 里 `RSSFetcher` 和 `IntelligenceAnalyzerV2` 是**两个独立实例**，各自加载盘上的 articles。

**根因流程**：
```
fetcher.fetch_all(limit=30)
  → fetcher.articles 加载 4946 篇（旧）→ 加 206 篇新 = 5152 → 写盘 ✅

analyzer.batch_analyze()
  → analyzer.articles 独立加载 4946 篇（**没拿到 fetcher 的新数据**）
  → analyze_article() 内部:
      self.articles[aid]['analyzed'] = True
      json.dump(self.articles, ...)  ← ❌ 用旧 4946 覆盖 fetcher 的 5152
```

**影响**：连续 7 天（6-29 ~ 7-6）RSS 抓取"跑成功"但实际数据没增长，用户看到的科技日报永远是 6-29 那一批 high priority 文章。

**修复**：
```python
# daily_pipeline.py __init__
self.fetcher = RSSFetcher(...)
self.analyzer = IntelligenceAnalyzerV2()
# L-24 修复: 共享 articles + 共享 db_path
self.analyzer.articles = self.fetcher.articles
self.analyzer.db_path = self.fetcher.db_path

# fetch_all 后再 sync 一次 (防止 fetcher 内部重赋值)
self._sync_analyzer_to_fetcher()
```

**教训**：
1. **两组件协作必须共享数据**：fetcher → analyzer 流程，共享 articles 引用，不要各自 load
2. **process 之间别用盘做 IPC**：盘加载有 race condition，引用共享更可靠
3. **py 进程内对象引用同步优于文件持久化**：fetcher 写盘 → analyzer 重 load 是慢且易出错的

**验证**：7-6 09:28 运行后 intelligence.json 从 4946 → 5152（+206）✅，30 天科技类从 73 → 241 篇

---

## L-25: 推送脚本必须读历史去重（L-25 · daily_tech_report 加 "已推过"过滤）

**现象**：7-5 和 7-6 技术日报 RSS 部分 5/5 完全相同（Microsoft Research 6-29 那 5 篇）。

**根因**：`read_yesterday_rss_top5()` 按 `priority desc + fetched_at desc` 排序，**30 天窗口不排除已推过的 title/url**。Microsoft Research 5 篇都是 high priority（⭐⭐⭐⭐⭐），fetched_at 都在 30 天内，7 天没新 high 顶掉 → 每天推同样 5 篇。

**修复**：在 `read_yesterday_rss_top5()` 加 3 步过滤——
```python
pushed_titles, pushed_urls = _load_pushed_history(days=7)

# 第一轮：排除 7 天已推过的
candidates = [(d, art) for d, art in recent 
              if art.get("title") not in pushed_titles 
              and art.get("url") not in pushed_urls]

# 第二轮：同源不超过 2 篇（防止单一来源垄断）
top5 = []
source_count = {}
for d, art in sorted(candidates, key=..., reverse=True):
    if source_count.get(art.get("source", ""), 0) >= 2:
        continue
    top5.append(art)
    source_count[art.get("source", "")] = source_count.get(art.get("source", ""), 0) + 1
    if len(top5) >= 5: break

# 第三轮：保底（候选不足 5 篇时从剩余补）
if len(top5) < 5: ...
```

`_load_pushed_history(days=7)` 从 `PUSH_HISTORY_DIR/*.md` 解析 markdown 链接 `\[[title\]\(url\)]`，转成 (titles, urls) 集合。

**教训**：
1. **任何"每天推送 top-N"脚本必须读历史去重**：不然后 5 天永远推同样内容
2. **同源分散是底线**：单一来源 ≤ 2 篇，避免内容单调
3. **3 步过滤要分层**：先排除历史 → 再源限制 → 后保底补足

**验证**：7-6 重推内容完全变了：
| 位置 | 7-5 旧 | 7-6 新 |
|:---:|:---|:---|
| #1 | Vega (Microsoft Research, 重复) | Memora (Microsoft Research 新) |
| #2 | MagenticLite (重复) | SkillOpt (Microsoft Research 新) |
| #3 | Extending Human (重复) | Scaling Laws (Lilian Weng 新) |
| #4 | Data Formulator (重复) | slide decks (dynomight 新) |
| #5 | Ire LOTUSLITE (重复) | crc-rates (dynomight 新) |

5/5 替换 ✅

---

## L-26: launchd plist 失效的"自检恢复"模式

**现象**：`com.nickfury.rss.collect` plist 自 7-4 01:01:36 后再没自动触发。但 `last exit code = 0`（显示正常），`runs = 3`。

**根因诊断路径**：
```
last terminating signal = Terminated: 15  ← SIGTERM, 被 launchd kill
runs = 3, 但 launchd print 显示 event triggers active = 0  ← 触发器失效
```

**为什么 7-5/7-6 01:00 没跑**：
1. 7-4 01:01:36 之后某次（可能是 7-5 01:00）跑成功，但 intellgence.json **被 fetcher 写 5152 → analyzer 覆盖回 4946**（L-24 根因）
2. 后续 cron 触发后 analyzer 写入空操作（没有新文章可分析），但 pipeline 内部某个步骤 hang 住，被 launchd SIGTERM 杀掉
3. launchd SIGTERM 后，event trigger 进入 degraded state，**后续 cron 不再触发**

**修复**：手动 `launchctl unload + load`（实际是 bootout + bootstrap）重注册 event triggers，然后 `kickstart -k` 强制重启验证。

**7-7 01:00 cron 验证清单**：
- [ ] launchctl list 显示 com.nickfury.rss.collect
- [ ] state = not running (空闲) 但 trigger 注册
- [ ] 明早 7-7 之后看 /tmp/rss_collect.log mtime 是否更新
- [ ] intelligence.json 文章数是否增长

**教训**：
1. **launchd `last exit code = 0` 是延迟信号，不代表最近一次成功**：要看 `runs` 计数和最近 mtime
2. **SIGTERM 信号暗示 hang 或 kill**：不能用 exit code 0 判断无问题
3. **plutil -lint 不能诊断 trigger 失效**：launchd 状态需要 `launchctl print` 看 active count
4. **"持续不触发"恢复模式**：bootout → 重写 plist → bootstrap → kickstart -k 验证

---

## 综合教训（元教训）

| # | 教训 | 落地 |
|:---:|:---|:---|
| **L-24** | 两组件协作必须共享 articles 引用，别用盘做 IPC | daily_pipeline.py __init__ 同步 |
| **L-25** | "每天推送 top-N"必读历史去重 + 同源分散 | daily_tech_report.py _load_pushed_history |
| **L-26** | launchd trigger 失效要 bootout + bootstrap 重注册 | plist 重写脚本流程化 |

---

## 关联 INC

- **INC-2026-07-06-001**: 技术日报内容重复 + RSS 数据真空 7 天 → Closed ✅
- 详见：`/Users/wenbo/Documents/05_AgentOutput/agent_work/Nick/INC/INC-2026-07-06-001_technical_report_repeat.md`

