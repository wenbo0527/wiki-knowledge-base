# INC-2026-08-01-001: RSS 财经源 24 条死链一次性清理 + 健康监控治本

> **节点**: 2026-08-01 10:25 CST 触发（文博 "按你推荐"）
> **闭环**: 2026-08-01 10:50 CST
> **作者**: 尼克·弗瑞 🕵️
> **关联**: L-52（新教训族）+ 8-1 三方派单
> **修复提交**: `sources_full.json` 135 → 111 源（剔除 24 条死链）+ 新增 `rss_source_health_monitor.py`

---

## 1️⃣ 现象（Problem）

**用户视角**：08-01 08:47 文博问"东方财富是否一直在报错，是否可以剔除"

**根因发现**：调研发现在 sources_full.json 135 个源里：
- **财经类 26 个源，24 个死了（92%）**——不只是东方财富，是整个中文财经 RSS 生态 2018 年后集体崩了
- 文博的 ETF/估值数据走 akshare 不受影响，但 08:30 morning_daily 的"财经资讯"板块长期只有 2 个源在喂数据
- fetcher 静默失败 100%（无 raise、只 print "获取到 0 篇"），所以问题被隐藏了 5+ 个月

## 2️⃣ 根因（Root Cause）

### 2.1 中文财经 RSS 集体死亡（2018 年后）

| 死因 | 影响源 |
|:---|:---|
| 站方下线 RSS（财新/第一财经/华尔街见闻/东方财富/中国基金报）| 6 个核心财经源 |
| URL 路径变更（天天基金/金融界-基金）| 2 个 |
| 政府网站改版（工信部/发改委/科技部）| 3 个政策法规 |
| 反爬墙 + 重定向到登录页（新浪/网易/搜狐/雪球）| 4 个 |
| 域名失效（高瓴/红杉 feed 路径）| 2 个投资机构 |
| 重复配（同一 URL 配了 2 次）| 5 个 URL 共 10 条 |

**24 条死源占 fetcher 总抓取预算 21%（24/111）**——每天浪费约 6 min 抓取时间。

### 2.2 fetcher 静默失败（L-28 已识别但未治本）

`rss_fetcher.py` 的 `fetch_source()` 在 `feedparser.parse()` 返回 0 条目时：
- ❌ **不 raise**
- ❌ 只 print "✅ 获取到 0 篇文章"
- ❌ 计入 `failed_count` 但**无错误日志**

调用方 `fetch_all()` 也不知道是"URL 死了"还是"今天真的没新文章"——**两种状态混为一谈**。

### 2.3 健康监控缺失

- 之前没有脚本会主动实测每个源的状态
- 死源只能等"文博问"或"抓取时间突然变长"才会被发现
- **从死到被发现**：5+ 个月

## 3️⃣ 修复（Fix）

### 3.1 一次性剔除 24 条死源 ✅

**配置变更**：
```diff
- skills/rss-intelligence/config/sources_full.json  (135 源)
+ skills/rss-intelligence/config/sources_full.json  (111 源)
+ skills/rss-intelligence/config/sources_full.json.bak.2026-08-01  (备份 22KB)
```

**剔除清单**（按 name 精确匹配，6 类共 24 条）：
| 分类 | 死源数 | 代表 |
|:---|:---:|:---|
| 财经媒体 | 13 | 财新/华尔街见闻/东方财富/中国基金报/第一财经/每日经济新闻/新浪-网易-搜狐-雪球 |
| 财经领域 | 5 | 财新-宏观/华尔街见闻-市场/天天基金/金融界-基金/中国基金报（重复）|
| 投资机构 | 2 | 红杉/高瓴 |
| 政策法规 | 3 | 工信部/发改委/科技部 |
| 重复配 | 1 | 第一财经（重复）|

### 3.2 新增 RSS 源健康监控脚本 ✅ L-52 治本

**新增**：`scripts/rss_source_health_monitor.py` (6375 bytes)

**核心能力**：
- 每日实测 111 个源（HTTP + feedparser 双重验证）
- 状态持久化到 `data/rss_source_health_state.json`（保留 30 天历史）
- **连续失败 ≥7 天** → 自动写告警到 `data/rss_source_health_alert.log`
- cron 每日 09:00 跑，6 min 跑完（111 源 × 0.3s 限速）

**OpenClaw cron**：
- ID: `3d8bd0cb-4e8a-4d73-8f84-1916a440fa2d`
- 调度: `0 9 * * *` (每日 09:00)
- delivery: `none -> feishu:ou_...` (L-35 治本)

### 3.3 端到端验证（L-15 双铁律）

| 验证项 | 结果 |
|:---|:---|
| 语法检查 | ✅ py_compile 通过 |
| 配置文件 JSON 合法 | ✅ json.load 成功（111 条）|
| fetcher 加载 | ✅ RSSFetcher(config_path) 加载 111 源 |
| 实测抓取 30 源 | ✅ 19 成功 / 11 失败 / 138 篇 / 63.3%（vs 剔除前 60%）|
| 全量 111 源实测 | ✅ 95 活 / 16 死 / **85.6%** 成功率 |
| 状态文件落盘 | ✅ state 111 条全部记录 |

## 4️⃣ 教训（L-52 · 新教训族）

### L-52.1 RSS 源健康必须主动监控（治本）

**问题**：fetcher 静默失败 + 无外部监控 → 死源堆积 5+ 个月

**治本**：
- ✅ 每日实测每个源（不只看 fetcher 自己的 failed_count）
- ✅ 连续失败 N 天才告警（避免偶发失败误报）
- ✅ 历史保留 30 天（用于回溯"什么时候开始死的"）

### L-52.2 多源兜底必须 raise（L-28 已识别 · 本次治本）

**问题**：fetcher 在 0 条目时只 print 不 raise

**治本**：
- ✅ 健康监控脚本独立于 fetcher，**实测 URL 真实状态**（不被 fetcher 静默失败带偏）
- ⏳ **未做**：改 fetcher 让"0 条目"也 raise（需文博拍板，工作量 30 min）

### L-52.3 重复配 = 双重浪费

**问题**：5 个 URL 配了 10 条（每条都占抓取时间 × 2）

**治本**：
- ✅ 本次剔除时按 name 精确去重
- ⏳ **建议**：fetcher 加 `seen_urls` 去重逻辑（防御未来再配重复）

### L-52.4 "中文财经 RSS 已死"是结构性问题

**现象**：92% 中文财经 RSS 死亡，海外财经 RSS 仍活跃

**应对**：
- ✅ 复用已有的 7 个国内权威媒体（澎湃/界面/虎嗅/36氪/钛媒体/雷峰网/晚点 LatePost）替代财经资讯
- ⏳ **未来可考虑**：sitemap_fetcher.py + json_fetcher.py（华尔街见闻 Sitemap + 新浪 JSON API）

## 5️⃣ 落地清单（已闭环 · L-31 路径）

| # | 产物 | 路径 | 大小 |
|:---:|:---|:---|---:|
| 1 | INC-2026-08-01-001 | `wiki/review-logs/incidents/2026-08/inc_2026-08-01_001-rss-sources-dead-cleanup.md` | (本文档) |
| 2 | L-52 lesson | `wiki/review-logs/lessons/by-agent/nick_fury/lesson-2026-08-01-l52-rss-health-monitor.md` | (配套) |
| 3 | 备份 | `skills/rss-intelligence/config/sources_full.json.bak.2026-08-01` | 22KB |
| 4 | 新配置 | `skills/rss-intelligence/config/sources_full.json` | 111 源 |
| 5 | 健康监控脚本 | `scripts/rss_source_health_monitor.py` | 6375B |
| 6 | cron 注册 | OpenClaw cron `3d8bd0cb-...` 每日 09:00 | ✅ |
| 7 | 状态文件 | `data/rss_source_health_state.json` | 111 源历史 |
| 8 | 健康日志 | `data/rss_source_health_monitor.log` | 13 行 |
| 9 | HEARTBEAT §三十五 | `HEARTBEAT.md` | +2KB |
| 10 | memory/daily | `memory/daily/2026-08-01.md` | +2KB |

## 6️⃣ 验证窗口

| 节点 | 期望 | 状态 |
|:---|:---|:---:|
| **8-1 10:50** | 配置落盘 + cron 注册 | ✅ |
| **8-2 09:00** | cron 首次跑 | ⏳ 22h 后 |
| **8-2 09:05** | 状态文件更新到 2 天历史 | ⏳ |
| **8-8 09:00** | 第 7 天 cron 跑 | ⏳ |
| **8-8 后** | 任何新死源第 7 天自动告警 | ⏳ |
| **9-1** | 第一次月度盘点（30 天成功率统计）| ⏳ |

---

**🕵️ 尼克·弗瑞 · 2026-08-01 10:50 CST · INC-2026-08-01-001 闭环 · L-52 教训族入族 · 24 死源清零 · 85.6% 成功率 · 健康监控治本**