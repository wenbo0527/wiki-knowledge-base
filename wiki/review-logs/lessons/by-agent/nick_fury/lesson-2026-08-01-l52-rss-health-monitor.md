# L-52: RSS 源健康监控治本（连续失败自动告警）

> **作者**: 尼克·弗瑞 🕵️
> **节点**: 2026-08-01 10:50 CST 闭环
> **关联**: INC-2026-08-01-001
> **入族**: L-52（族首 · RSS 源治理）

---

## 1️⃣ 元教训

> **fetcher 静默失败 + 无外部监控 = 死源堆积数月才被发现**

---

## 2️⃣ 4 子教训

### L-52.1 RSS 源健康必须主动监控（独立于 fetcher）

**踩坑**：fetcher 的 `failed_count` 不可信——它把"URL 死了"和"今天没新文章"混为一谈。

**治本**：
- ✅ 写独立的 `rss_source_health_monitor.py`，**实测每个 URL 真实状态**（HTTP + feedparser 双重验证）
- ✅ 不依赖 fetcher 自己的失败计数
- ✅ 状态持久化到 `data/rss_source_health_state.json`，保留 30 天历史

### L-52.2 连续失败阈值比单次失败更准

**踩坑**：偶发失败（DNS 抽风、源方临时维护）会误报。

**治本**：
- ✅ 阈值 = **连续失败 7 天**（ALERT_THRESHOLD = 7）
- ✅ 第 8 天才告警——给偶发失败 7 天恢复期
- ✅ 成功后自动清零连续失败计数

### L-52.3 治本 ≠ 一次性清理，必须有持续机制

**踩坑**：8-1 一次性剔除 24 条死源，但**未来还会有新源变死**。

**治本**：
- ✅ 每日 cron 跑健康监控（OpenClaw cron `3d8bd0cb-...`）
- ✅ 死源持续被发现 → 持续被剔除（自动治本循环）
- ⏳ **未来可加**：自动从 sources_full.json 剔除连续失败 ≥ 30 天的源（待文博拍板）

### L-52.4 重复配是隐藏的"双重浪费"

**踩坑**：5 个 URL 配了 10 条 = 每天抓 2 次，浪费抓取时间 × 2。

**治本**：
- ✅ 本次剔除时按 name 精确去重
- ⏳ **未来可加**：fetcher 加 `seen_urls` 去重逻辑（防未来再配重复）

---

## 3️⃣ 落地物

| # | 产物 | 路径 |
|:---:|:---|:---|
| 1 | 健康监控脚本 | `scripts/rss_source_health_monitor.py` (6375B) |
| 2 | OpenClaw cron | `3d8bd0cb-4e8a-4d73-8f84-1916a440fa2d` (每日 09:00) |
| 3 | 状态文件 | `data/rss_source_health_state.json` |
| 4 | 告警文件 | `data/rss_source_health_alert.log` |
| 5 | INC 文档 | `inc_2026-08-01_001-rss-sources-dead-cleanup.md` |

---

## 4️⃣ 预防机制 Checklist

- [ ] **新增 RSS 源**前必测（curl + feedparser 双重验证）
- [ ] **每周日 c3 cron** 跑一次健康盘点（汇总周成功率）
- [ ] **每月末**归档 30 天历史到 `data/rss_health_archive/YYYY-MM.json`
- [ ] **新增 cron** 必 grep argv + 同步 edit（L-34 铁律）

---

## 5️⃣ 与其他教训族的关系

| 关联 | 教训族 | 关系 |
|:---|:---|:---|
| **L-13** | OpenClaw 原生优先 | cron 必须用 OpenClaw cron，不用 launchd |
| **L-28** | 多源兜底必须 raise | 本次**未完全治本**（fetcher 仍静默失败，留待下次） |
| **L-34** | scripts 改造 + cron argv 同步 | 本次新增脚本 + cron 是干净路径（新增非改造）|
| **L-35** | cron delivery mode=none | 本次 cron 设 mode=none ✅ |
| **L-49** | argv 看门狗 | 健康监控是 argv 看门狗的兄弟机制 |

---

**🕵️ 尼克·弗瑞 · 2026-08-01 10:50 CST · L-52 族首 · 4 子教训 · 治本循环已启动**