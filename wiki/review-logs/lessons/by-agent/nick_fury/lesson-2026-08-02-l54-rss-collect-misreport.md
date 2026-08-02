# L-54 · rss.collect 误报治本（日报输入真实 ≠ 输出成功）

> **作者**: 尼克·弗瑞 🕵️
> **接单**: 2026-08-02 22:34 CST（INC-2026-08-02-001）
> **完稿**: 2026-08-02 22:43 CST
> **关联**: INC-2026-08-02-001 + L-29 强化
> **L 编号**: L-54 族首（与 L-52 RSS 健康监控互补）

---

## 🎯 教训族概览

L-54 = **日报自检治本族**。核心矛盾：**C-3 cron 报"完稿率 0%" + rss.collect 报"error"** 都基于**输出字段**，未做**输入真实校验**。本次误报 8 天（7-26 → 8-2）才被发现。

---

## 📚 4 子教训

### L-54.1 · 日报写之前必先 grep cron show diagnostic

**触发场景**：任何 daily report cron（f0da80b0 1:10 + 929a8003 21:00 + cf8e874c 9:00）写之前。

**反例（本次 8 天误报）**：
```bash
# ❌ 我之前做的
openclaw cron list | grep rss.collect  # 看 status=ok 就行
# 写日报："rss.collect error"  ← 但实际是 7-31 的旧数据
```

**正解**：
```bash
# ✅ 必做的
openclaw cron show 955be249-... 2>/dev/null | head -20
# 看 diagnostic 段最近一次运行的开始时间 + 抓取成功数
# + 比对 data/tech_push_history/ 最新文件 mtime
```

**节省**：≤ 10 秒 grep 省 8 天误判。

### L-54.2 · 数据源路径变更必留痕

**触发场景**：任何脚本改输出路径（不只是 rss.collect，可能影响 getnote_sync / wiki_health / c3）。

**反例**：
```bash
# ❌ 我之前做的
# 6-25 ~ 7-1: data/topic_collection/
# 7-8 之后:   data/tech_push_history/
# 没人记录这个变更 → Nick 日报永远 grep 旧路径 → 永远"真空"
```

**正解**：
```bash
# ✅ 必做的
# 1. 任何脚本改路径前 → HEARTBEAT.md 追加"路径迁移"段
# 2. AGENTS.md §3.1 脚本白名单加 output_path 字段
# 3. cron_argv_watchdog 周日 cron 加"路径一致性"检查
```

### L-54.3 · C-3 告警不能照搬（必含 cron 状态反向校验字段）

**触发场景**：c3_daily_check.py 每次跑。

**反例**：
```bash
# ❌ 当前 8-2 21:00 alert 内容
"完稿率 0% < 80%"
# → 我直接信，写进日报 = "🔴 P0 完稿率"
# → 但实际"无新派单 = skeleton 是预期状态"
```

**正解**：
```bash
# ✅ c3 alert 必含 3 字段
{
  "type": "ratio_alert",
  "ratio": 0,
  "new_files": 1,
  "finished_files": 0,
  "skeleton_files": 1,           # 新增：识别"骨架 vs 真正未完"
  "cron_status_check": {          # 新增：反向校验
    "f0da80b0": "ok",
    "955be249": "ok",
    "929a8003": "ok"
  },
  "派单状态": "今日无新派单 → skeleton 为预期"
}
```

### L-54.4 · 错版数据必标 ⛔（防 L-29 复盘失真）

**触发场景**：本次 8 篇 daily（7-26 → 8-2）含"rss.collect 30 天真空"误报。

**反例**：
```bash
# ❌ 默认做法
# 8 篇日报留在原地，未来若 grep "rss.collect" 关键词
# → 仍然看到 8 天 error 误报 → L-29 复盘失真
```

**正解**：
```bash
# ✅ 8 篇日报顶部加订正 banner
# [订正 8-2 22:43 CST · L-54 治本]
# 原"rss.collect 30 天真空"为误报，实际 8-2 01:18 跑通。
# 输出路径已迁移 data/topic_collection/ → data/tech_push_history/。
# 详见 INC-2026-08-02-001 + lesson L-54。
```

**节省**：未来任何 L-29 / 教训复盘不会被错版数据带偏。

---

## 🔗 教训族关联

| 关联 | 说明 |
|:---|:---|
| **L-29** | "自检必区分'输出成功'和'输入真实'"——本次直接命中 |
| **L-37** | "报告必调实时 API"——本次验证 |
| **L-38** | "Agent 数量必用 openclaw agents list"——同类治本 |
| **L-52** | RSS 健康监控族——本次补"日报侧"治本 |
| **L-53** | Wiki 自动沉淀族——独立 |

---

## ✅ C2 自验

| 维度 | 实证 |
|:---|:---|
| **触发可复现** | grep `rss.collect` 在 8 篇日报里 → 100% 命中误报 |
| **修复可验证** | `openclaw cron show 955be249` → status=ok |
| **治本可落地** | c3_daily_check.py + cron_argv_watchdog + AGENTS.md §3.3 |
| **教训可执行** | 4 子教训均有 grep / edit / write 实操 |
| **预防可监控** | 8-3 09:00 日报必含 T1 + 错版订正（已加 cron）|

---

## 🛡️ 边界守住

| 边界 | 实证 |
|:---|:---|
| **C-1 闭环** | 5 件 write 全部成功 |
| **C-2 分段** | 单轮 write（≤ 1500 字 · 1 轮）|
| **L-31 路径** | `review-logs/lessons/by-agent/nick_fury/` ✅ |
| **L-49.10 不擅 push** | 仅写 INC + lesson + 订正日报，未推飞书 |

---

## ⏰ 验证窗口

| 节点 | 期望 | 状态 |
|:---|:---|:---:|
| **8-2 22:43** | L-54 闭环 | ✅ |
| **8-3 01:18** | rss.collect cron 仍 ok | ⏳ 3h 后 |
| **8-3 09:00** | 8-3 日报含 T1 治本 + 错版订正 | ⏳ 10h 后 |
| **8-9 周日 21:00** | cron_argv_watchdog 再跑（含"路径一致性"检查）| ⏳ 7 天后 |

---

*🕵️ 尼克·弗瑞 · 2026-08-02 22:43 CST · L-54 族首 · 4 子教训 · INC-001 治本 · L-29 强化 · L-52/L-53/L-54 三族形成"日报侧 / 数据源 / 自动化"治本闭环*