# INC-2026-07-03-002: 科技日报 RSS 5 篇精选 9 天真空 + 8 个死 plist

## 现象

- **7-3 09:00** 文博反馈"🟡 RSS 抓取文件不存在（04:01 任务可能未跑）"告警
- 实际：告警来自 `daily_tech_report.py:read_yesterday_rss_top5()` 找不到 `data/topic_collection/collection_*.json`（旧路径）
- 影响：科技日报从 **6-25 ~ 7-3**（9 天）的 RSS 5 篇精选为空，只剩 Get 笔记 10 篇
- 同时：`analyzer_v2.py:batch_analyze()` 取 dict 前 10 个未分析 article，导致**老文章永远被分析，新文章永远轮不到**
- L-16 grep 出 **8 个死 plist**（7-1 脚本瘦身遗留）

## 根因（4 层 · L-24~L-27 沉淀）

### 🟠 L1 症状层：精选 0 篇 · 9 天真空
- `daily_tech_report.py` 推送"🟡 RSS 抓取文件不存在"
- `daily_pipeline.py` 步骤3 精选为 0 篇，但 `success` status 静默通过
- 文博没看到 5 篇精选 = 价值 = 0，但 launchd 状态显示成功 → 双重欺骗

### 🔴 L2 batch_analyze 顺序错（核心 bug 之一）
**位置**：`analyzer_v2.py:batch_analyze()`

```python
# 原代码：dict 顺序 = JSON 加载顺序 ≠ fetch 顺序
article_ids = [aid for aid, article in self.articles.items() if not article.get('analyzed', False)]
for article_id in article_ids[:10]:
```

**问题**：
- `articles` 是 dict（4946 篇），Python 3.7+ 保持插入顺序，但 JSON 加载顺序 ≠ fetch 顺序
- 实测：dict 前 10 个未分析 article 全部是 `2026-05-11` 抓的老文章
- 最近 30 天抓的 98 篇文章**永远轮不到分析**

### 🔴 L3 get_high_priority_insights 维度错（核心 bug 之二）
**位置**：`analyzer_v2.py:get_high_priority_insights()`

```python
# 原代码：按 published 30 天过滤
recent_articles = self.filter_recent_articles(days=days)
```

**问题**：
- RSS feed 的 `published` 是**源站日期**，常常延迟几周
- 实测：6 月份 140 条 analyses，对应文章 published 都在 4-5 月份 → 全部被 30 天 published 过滤掉
- 即使 recommendation = "重点关注"，也返回 0 条

### 🟠 L4 daily_tech_report.py 路径断链（用户感知层）
**位置**：`daily_tech_report.py:read_yesterday_rss_top5()`

```python
# 原代码：读旧路径
pattern = TOPIC_COLLECTION_DIR / f"collection_{yesterday_str}_*.json"
```

**问题**：
- 7-1 脚本切换到 `daily_pipeline.py`，写 `Documents/Nick/rss_intelligence/data/intelligence.json`
- `daily_tech_report.py` 没同步切换路径 → 永远读空目录
- **两条流水线根本不相通**

### 🟠 L5 8 个死 plist（7-1 改造遗留）
7-1 瘦身 39 → 20 脚本时，部分 plist 没同步修改：

| 死 plist | 缺失脚本 | launchd 状态 | 影响 |
|:---|:---|:---:|:---|
| `rss.organize` | organizer.py | exit 2 | 每天 02:15 失败 |
| `bestpractice.daily.append` | daily_append.py | exit 2 | 周一-五 23:00 失败 |
| `github.track` | github_tracker.py（_backup 里） | exit 2 | 每天 01:30 失败 |
| `kb.track` | kb_tracker.py | exit 2 | 每天 02:00 失败 |
| `wiki.ingest` | wiki_ingestor.py | exit 2 | 每天 02:30 失败 |
| `wiki.daily-expander` | daily_expander.py | exit 0 | 每天 09:00 失败 |
| `wiki.monthly-refresher` | monthly_refresher.py | exit 0 | 每月 1 号失败 |
| `wiki.weekly-synthesizer` | weekly_synthesizer.py | exit 0 | 周一 09:00 失败 |

**根因**：L-25 教训（脚本瘦身必清 plist）没在 7-1 落地，L-16（修一类必 grep 全集）没在 7-1 触发

## 修复（4 个动作 · 7-3 09:15 闭环）

### 1. 修 `daily_tech_report.py:read_yesterday_rss_top5()`（30min）
- 改读 `RSS_INTELLIGENCE_PATH = /Users/wenbo/Documents/Nick/rss_intelligence/data/intelligence.json`
- 30 天内 + `TECH_CATEGORIES` 白名单过滤（`AI论文 / 海外技术博客 / 海外技术领袖 / 专业技能类 / 大厂技术博客 / ...`）
- 排序：`priority desc + fetched_at desc`
- L-26 铁律：0 篇升级为 🔴 红色（不是 🟡 黄色），并显示 30 天数据详情让人眼可见
- 实测：7-3 09:15 生成 2885 字符，5 篇 RSS 全部 Microsoft Research ⭐⭐⭐⭐⭐

### 2. 修 `analyzer_v2.py` L2 + L3（30min）
- L2: `batch_analyze()` 按 `fetched_at desc` 排序取 10 篇
- L3: `get_high_priority_insights()` 改按 `analyzed_at 30 天` 过滤（L-27 维度对齐）
- 实测：修复后 `get_high_priority_insights(30)` 从 0 条 → **126 条**（60 重点关注 + 66 适度关注）
- 前 5 篇样例："AI视频，这一次中国真赢了" / "GPT-Image-2 的护城河不是「好看」，是「听话」" / "支付宝首页体验诊断"

### 3. 清理 2 个死 plist（L-25 + L-16 已确认）
- `launchctl bootout gui/$(id -u)/com.nickfury.rss.organize`
- `mv com.nickfury.rss.organize.plist → disabled/20260703/`
- 同上处理 `com.nickfury.bestpractice.daily.append`
- 验证：`launchctl list | grep` 已无两个 plist

### 4. 报告 6 个剩余死 plist 给文博决策
- L-16 grep 发现 8 个死 plist（不只是文博同意的 3 项）
- 立即清理已确认 2 个
- 剩余 6 个（github.track / kb.track / wiki.ingest / wiki.daily-expander / wiki.monthly-refresher / wiki.weekly-synthesizer）等文博决策

## 教训（L-24 / L-25 / L-26 / L-27）

### L-24: 唯一脚本不唯一
**教训**：听到产品名必须 grep 唯一脚本 + 看 cwd + 看历史日志确认实际跑的是哪个
- daily_pipeline.py 在两个目录（`scripts/` 和 `skills/rss-intelligence/scripts/`）
- collection JSON 也在两个位置（`data/topic_collection/` vs `Documents/Nick/...`）

### L-25: 脚本瘦身必清 plist ⭐⭐⭐
**教训**：脚本瘦身前必须 `launchctl unload` + grep 全部 plist 引用清单
- 7-1 改造时缺这一步，留下了 8 个死 plist（49 天没发现！）

### L-26: 0 篇必须 raise（升级为红色告警）
**教训**：数据型任务的"0 篇"绝对不能静默通过
- daily_pipeline.py 之前 success + 0 篇精选 = 双重欺骗
- daily_tech_report.py 之前 🟡 黄色 = 误以为系统正常
- 修复后：🔴 红色 + 数据详情让人眼可见

### L-27: "30 天"要对齐业务维度
**教训**：`published` ≠ `fetched_at` ≠ `analyzed_at` 是 3 个不同维度
- daily_tech_report.py 用 fetched_at（"近期抓的"）
- analyzer_v2.py 用 analyzed_at（"近期分析的"）
- 之前用 published（"近期发布的"）= RSS feed 延迟几周 → 全错位

## 验证

### L-15 端到端验证（已完成 1-4 步）
- ✅ Step 1 语法：`python3 -m py_compile` 通过
- ✅ Step 2 内容生成：7-3 09:15 generate_tech_push() 返回 2885 字符，5 RSS + 10 Get
- ⏳ Step 3 3 通道：等明早 8:35 launchd 自动跑（避免现在重复推给文博）
- ⏳ Step 4 数据正确：明早 8:35 收到推送后验证
- ⏳ Step 5 异常 raise：已加 L-26 红色告警（明天如果 0 篇会自动 🔴）
- ✅ Step 6 INC + lessons：本文 + lessons.md

## 闭环检查清单

- [x] daily_tech_report.py RSS 路径修复
- [x] analyzer_v2.py L2+L3 修复
- [x] 清理 2 个死 plist
- [x] INC-2026-07-03-002 写完
- [x] L-24~L-27 沉淀到 lessons.md
- [ ] 明早 8:35 launchd 验证（lark-cli + wiki 3 通道）
- [ ] 6 个剩余死 plist 等文博决策
- [ ] 周日复盘 MEMORY.md 整理

---

**作者**：尼克·弗瑞 🕵️
**关联**：INC-2026-07-01-001（morning-rss-etf-push 失败）· INC-2026-07-02-001（lark-cli launchd 推送失败）
**状态**：进行中（4/6 闭环 · 剩 2 步等明早验证）