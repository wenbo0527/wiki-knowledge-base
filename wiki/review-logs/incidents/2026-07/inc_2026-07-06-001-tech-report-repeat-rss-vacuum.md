# INC-2026-07-06-001: 技术日报内容重复 + RSS 数据真空 7 天

## 接单
- **时间**: 2026-07-06 09:02 GMT+8
- **报告人**: 文博
- **症状**: 今天的技术日报和昨天的条目是一样的，请检查
- **决策**: 选 B 方案（治本修复）2026-07-06 09:25

## 现象
- 7-6 08:35 推送的技术日报，RSS 部分 5 篇**完全等于** 7-5 推送的 5 篇
- 都是 Microsoft Research 6-29 那批 high priority 文章（Vega / MagenticLite / Extending Human Intelligence / Data Formulator / Ire LOTUSLITE）
- Get 笔记部分：今天 0 篇（昨天 4 篇）

## 根因
### 根因 1（数据真空 7 天）：daily_pipeline.py fetcher ↔ analyzer 数据覆盖

`/Users/wenbo/.openclaw/workspace/agents/nick_fury/skills/rss-intelligence/scripts/`

**bug 流程**：
```
fetcher.fetch_all() 
  → 加载旧 articles (4946) 
  → 加 206 篇新 → 5152 
  → _save_articles() 写盘 ✅

analyzer.batch_analyze()
  → 自己加载 articles (4946，独立副本)
  → analyze_article() 中：
     self.articles[aid]['analyzed'] = True
     json.dump(self.articles, ...)  ← ❌ 用 4946 覆盖了 fetcher 的 5152
```

analyzer_v2.py:588-589 在每篇分析后 json.dump，self.articles 是从盘加载的旧数据，覆盖 fetcher 刚写的新数据。

**证据**：
- intelligence.json mtime: 7-6 09:08:54（刚跑完 daily_pipeline）
- intelligence.json size: 17,226,427 bytes
- intelligence.json 实际文章数: **4946**（被覆盖了）
- 7-6 09:00 后入库: **0 篇**
- 最新 fetched_at: 2026-06-29 08:33:53（7 天前）
- pipeline_log.json 最后一条: 2026-07-04 01:01:36（再没成功跑过）

### 根因 2（去重缺失）：daily_tech_report.py 不读历史推送

`/Users/wenbo/.openclaw/workspace/agents/nick_fury/scripts/daily_tech_report.py`

- `read_yesterday_rss_top5()` 按 `priority desc + fetched_at desc` 排序
- 30 天窗口内，不排除已推过的 title
- Microsoft Research 那 5 篇都是 high priority，7 天没新 high 顶掉 → 每天推同样的 5 篇

### 根因 3（plist 触发失败）：com.nickfury.rss.collect 自 7-4 后再没跑过

- plist last exit code = 0（显示正常）
- runs = 3（最近 3 次都是 7-4 之前的）
- /tmp/rss_collect.log 最后一行: 7-4 01:01:36
- pipeline_log.json 最后一条: 7-4 01:01:36
- **根因待查**：可能 launchd 7-5/7-6 01:00 触发但脚本没跑成功（具体原因在修 plist 后查）

## 修复计划（B 方案 · 09:25 启动）

| # | 步骤 | 状态 |
|:---:|:---|:---:|
| 1 | INC-2026-07-06-001 创建 | ✅ |
| 2 | 修 daily_pipeline.py：fetcher.articles 共享给 analyzer | ✅ |
| 3 | 修 daily_tech_report.py：加 `_load_pushed_history(days=7)` 过滤 | ✅ |
| 4 | 修 plist 自动触发失败 | ✅ (kickstart 验证 exit 0) |
| 5 | 手动重跑 daily_pipeline → 4946 → 5152 | ✅ |
| 6 | 手动重推 daily_tech_report → 5/5 全换新 | ✅ |
| 7 | 7 步端到端验证（L-15） | ✅ |
| 8 | write lessons.md + L-24/25/26 | ✅ |
| 9 | write daily.md 回执 | ✅ |

## ✅ Closed · 2026-07-06 10:00

### 实际修复成果
- [x] daily_pipeline 修后跑（09:28 + 09:33），intelligence.json 4946 → **5152**（+206）
- [x] daily_tech_report 修后推一份"今日真版"（1938 字符），5 篇全换新
- [x] 文博收到 2/2 主通道（lark ✅ + wiki ✅ + sessions_send 跳过 launchd 预期）
- [x] com.nickfury.rss.collect 重写 plist + bootout/bootstrap + kickstart 验证 → `last exit code = 0` runs = 1
- [x] L-24/L-25/L-26 沉淀到 lessons/2026-07-06_lessons_L24-L26.md
- [x] daily/2026-07-06.md 已记录

### 验证证据
| 项目 | 修复前 | 修复后 |
|:---|:---|:---|
| intelligence.json 文章数 | 4946 | 5152 |
| intelligence.json size | 17,226,427 | 18,795,342 |
| 30 天科技类文章数 | 73 | 241 |
| 7-6 推送 RSS 5 篇 | Microsoft Research × 5（6-29 老）| Memora / SkillOpt / Scaling Laws / slide decks / crc rates |
| daily_pipeline 状态 | 7-4 后失败 | 7-6 09:33 exit 0 ✅ |
| launchd plist trigger active | 0 | 重新注册 + kickstart 验证 ✅ |

### 后续待办 (7-7 验证)
- [ ] 01:00 cron 是否触发，/tmp/rss_collect.log mtime 是否 7-7 01:02+
- [ ] intelligence.json 是否再增长（期望 > 5200）
- [ ] daily_tech_report 7-7 推送是否还有重复

---
**接单**: 2026-07-06 09:25 · **owner**: 尼克·弗瑞 · **Closed**: 2026-07-06 10:00
